#!/usr/bin/env python3
"""
wal_universal_mapper.py

Universal SQLite WAL Schema Mapping Engine
This diagnostic utility scans raw Write-Ahead Log (WAL) components, parses leaf-table cells,
and iteratively maps all column data. It deploys a recursive decoding matrix to extract
embedded Protobuf architectures (wire types 0, 1, 2, 5) and generates a comprehensive
Schema Blueprint Summary for reverse-engineering proprietary data structures.
"""

import struct
import binascii
import sys
import os
import argparse

# ---------------------------------------------------------
# Cryptographic & Varint Decoding Primitives
# ---------------------------------------------------------

def decode_sqlite_varint(data: bytes, offset: int) -> tuple:
    """Decodes SQLite variable-length integers (big-endian 7-bit groups)."""
    value = 0
    for i in range(9):
        if offset + i >= len(data):
            raise IndexError("sqlite_varint: Data boundary exceeded")
        b = data[offset + i]
        value = (value << 7) | (b & 0x7f)
        if (b & 0x80) == 0:
            return value, offset + i + 1
    return value, offset + 9

def decode_pb_varint(data: bytes, offset: int) -> tuple:
    """Decodes Protobuf variable-length integers (base-128 little-endian)."""
    value = 0
    shift = 0
    start = offset
    while True:
        if offset >= len(data):
            raise IndexError("pb_varint: Data boundary exceeded")
        b = data[offset]
        offset += 1
        value |= (b & 0x7f) << shift
        if not (b & 0x80):
            return value, offset
        shift += 7
        if offset - start > 10:
            raise ValueError("pb_varint: Integer length constraint violated")

# ---------------------------------------------------------
# SQLite Record Parsing Architecture
# ---------------------------------------------------------

def extract_sqlite_record(payload: bytes) -> list:
    """
    Parses SQLite record headers and maps serial types to byte chunks.
    Truncated columns (exceeding payload bounds) return None.
    """
    cols = []
    try:
        header_size, cur = decode_sqlite_varint(payload, 0)
    except Exception:
        return []

    types = []
    while cur < header_size:
        try:
            st, cur = decode_sqlite_varint(payload, cur)
            types.append(st)
        except Exception:
            return []

    data_cur = header_size
    for st in types:
        length = 0
        if st >= 12:
            length = (st - 12) // 2 if st % 2 == 0 else (st - 13) // 2
        elif st in (0, 8, 9):
            length = 0
        elif st in (1, 2, 3, 4):
            length = st
        elif st == 5:
            length = 6
        elif st in (6, 7):
            length = 8

        if data_cur + length > len(payload):
            cols.append((st, None))
            break

        cols.append((st, payload[data_cur:data_cur + length]))
        data_cur += length

    return cols

# ---------------------------------------------------------
# Recursive Protobuf Extraction Engine
# ---------------------------------------------------------

VALID_WIRES = {0, 1, 2, 5}

def verify_printable_utf8(b: bytes) -> bool:
    """Verifies if a byte chunk contains clean, printable UTF-8 strings."""
    try:
        s = b.decode('utf-8')
    except Exception:
        return False
    return len(s) > 0 and all((c.isprintable() or c.isspace()) for c in s)

def evaluate_protobuf_matrix(blob: bytes, indent: int = 0, max_depth: int = 6) -> tuple:
    """
    Recursively probes binary blobs for structured Protobuf arrays.
    Returns formatted diagnostic lines and a set of structural fields for the summary.
    """
    lines = []
    fields = set()
    sp = " " * indent
    off = 0

    # Pre-flight check: Valid wire tag required
    try:
        tag, _ = decode_pb_varint(blob, 0)
        if (tag & 0x07) not in VALID_WIRES:
            return None, None
    except Exception:
        return None, None

    while off < len(blob):
        try:
            tag, off = decode_pb_varint(blob, off)
        except Exception:
            lines.append(sp + "[-] DECODE ERROR: Invalid tag structure")
            return lines, fields

        field = tag >> 3
        wire = tag & 0x07
        fields.add((field, wire))

        if wire == 0:
            try:
                val, off = decode_pb_varint(blob, off)
                lines.append(f"{sp}Field {field} (VARINT): {val}")
            except Exception:
                lines.append(sp + f"[-] Field {field} (VARINT): DECODE ERROR")
                return lines, fields

        elif wire == 1:
            if off + 8 > len(blob):
                lines.append(sp + f"[-] Field {field} (64-BIT): TRUNCATED")
                return lines, fields
            val = blob[off:off + 8]
            off += 8
            lines.append(f"{sp}Field {field} (64-BIT HEX): {binascii.hexlify(val).decode().upper()}")

        elif wire == 5:
            if off + 4 > len(blob):
                lines.append(sp + f"[-] Field {field} (32-BIT): TRUNCATED")
                return lines, fields
            val = blob[off:off + 4]
            off += 4
            lines.append(f"{sp}Field {field} (32-BIT HEX): {binascii.hexlify(val).decode().upper()}")

        elif wire == 2:
            try:
                length, off = decode_pb_varint(blob, off)
            except Exception:
                lines.append(sp + f"[-] Field {field} (LEN): DECODE ERROR")
                return lines, fields

            if off + length > len(blob):
                available = len(blob) - off
                chunk = blob[off:len(blob)]
                off = len(blob)
                lines.append(f"{sp}Field {field} (BYTES) Len={length} [TRUNCATED, extracted {available}] HEX={binascii.hexlify(chunk).decode().upper()}...")
                fields.add((field, wire, length))
                return lines, fields

            chunk = blob[off:off + length]
            off += length
            fields.add((field, wire, length))

            if length == 0:
                lines.append(f"{sp}Field {field} (BYTES) Len=0")
                continue

            if verify_printable_utf8(chunk):
                s = chunk.decode('utf-8')
                lines.append(f"{sp}Field {field} (STRING): \"{s}\"")
                continue

            # Nested Protobuf Recursion
            if indent // 2 < max_depth:
                nested_lines, nested_fields = evaluate_protobuf_matrix(chunk, indent=indent + 2, max_depth=max_depth)
                if nested_lines is not None:
                    lines.append(f"{sp}Field {field} (SUBMESSAGE) Len={length}:")
                    for nl in nested_lines:
                        lines.append(nl)
                    if nested_fields:
                        for nf in nested_fields:
                            fields.add((field, 'sub', nf))
                    continue

            # Binary Fallback
            hexv = binascii.hexlify(chunk).decode().upper()
            lines.append(f"{sp}Field {field} (BYTES/HEX) Len={length}: {hexv}")
        else:
            lines.append(sp + f"[-] Field {field} (UNKNOWN WIRE {wire})")
            return lines, fields

    return lines, fields

# ---------------------------------------------------------
# Telemetry Aggregation Structures
# ---------------------------------------------------------

class StructuralColumnStats:
    """Aggregates metrics for the Schema Blueprint Summary."""
    def __init__(self):
        self.present_count = 0
        self.type_counts = {}
        self.protobuf_field_counts = {}
        self.protobuf_field_lengths = {}

    def note_type(self, t: str):
        self.type_counts[t] = self.type_counts.get(t, 0) + 1

    def note_proto_fields(self, fields: set):
        for f in fields:
            if isinstance(f, tuple) and len(f) >= 1:
                field_num = f[0]
                self.protobuf_field_counts[field_num] = self.protobuf_field_counts.get(field_num, 0) + 1
                if len(f) >= 3 and isinstance(f[2], int):
                    self.protobuf_field_lengths.setdefault(field_num, set()).add(f[2])

# ---------------------------------------------------------
# Main Execution Pipeline
# ---------------------------------------------------------

def execute_wal_mapping(wal_path: str, out_path: str) -> None:
    page_size = 4096
    total_rows = 0
    col_stats = {}

    print(f"[*] Initializing Universal WAL Schema Mapping Engine...")
    print(f"[*] Target Asset: {os.path.basename(wal_path)}")

    try:
        with open(wal_path, "rb") as f, open(out_path, "w", encoding="utf-8") as out:
            f.seek(32)
            frame_idx = 0

            while True:
                hdr = f.read(24)
                if len(hdr) < 24: break
                page = f.read(page_size)
                if len(page) < page_size: break
                frame_idx += 1

                if page and page[0] == 0x0D:
                    try: num_cells = struct.unpack(">H", page[3:5])[0]
                    except Exception: continue

                    cell_ptr_off = 8
                    for ci in range(num_cells):
                        if cell_ptr_off + 2 > page_size: break
                        ptr = struct.unpack(">H", page[cell_ptr_off:cell_ptr_off + 2])[0]
                        cell_ptr_off += 2
                        if ptr >= page_size: continue

                        try:
                            payload_size, s_len = decode_sqlite_varint(page, ptr)
                            rowid, r_len = decode_sqlite_varint(page, ptr + s_len)
                        except Exception: continue

                        header_len = s_len + r_len
                        content_off = ptr + header_len
                        content_end = content_off + payload_size

                        if content_end <= page_size:
                            payload = page[content_off:content_end]
                            truncated = False
                        else:
                            payload = page[content_off:page_size]
                            truncated = True

                        cols = extract_sqlite_record(payload)
                        total_rows += 1
                        out.write(f"\n[+] [FRAME {frame_idx}] [ROW ID {rowid}]\n")

                        if not cols:
                            out.write("  [-] ERROR: Record header unparsable or columns absent\n")
                            if truncated: out.write("  [!] WARNING: Payload truncated within WAL frame constraints\n")
                            out.write("-" * 65 + "\n")
                            continue

                        for idx, (st, data) in enumerate(cols):
                            if idx not in col_stats:
                                col_stats[idx] = StructuralColumnStats()
                            col_stats[idx].present_count += 1
                            col_label = f"Col {idx}"

                            if st in (0,):
                                col_stats[idx].note_type('NULL')
                                out.write(f"  {col_label} (NULL): NULL\n")
                                continue

                            if st in (1, 2, 3, 4, 5, 6, 7, 8, 9):
                                if data is None:
                                    col_stats[idx].note_type('TRUNCATED')
                                    out.write(f"  {col_label} (NUM): [TRUNCATED]\n")
                                    continue
                                try:
                                    if st == 1: val = struct.unpack(">b", data)[0]
                                    elif st == 2: val = struct.unpack(">h", data)[0]
                                    elif st == 3: val = int.from_bytes(data, byteorder='big', signed=True)
                                    elif st == 4: val = struct.unpack(">i", data)[0]
                                    elif st == 5: val = int.from_bytes(data, byteorder='big', signed=True)
                                    elif st == 6: val = struct.unpack(">q", data)[0]
                                    elif st == 7: val = struct.unpack(">d", data)[0]
                                    elif st == 8: val = 0
                                    elif st == 9: val = 1
                                    else: val = None

                                    col_stats[idx].note_type('NUM')
                                    out.write(f"  {col_label} (NUM): {val}\n")
                                except Exception:
                                    col_stats[idx].note_type('NUM_DECODE_ERROR')
                                    out.write(f"  {col_label} (NUM): [DECODE ERROR]\n")
                                continue

                            if st >= 12:
                                is_blob = (st % 2 == 0)
                                if data is None:
                                    col_stats[idx].note_type('TRUNCATED')
                                    out.write(f"  {col_label} ({'BLOB' if is_blob else 'TEXT'}): [TRUNCATED]\n")
                                    continue

                                if not is_blob:
                                    try:
                                        txt = data.decode('utf-8')
                                        col_stats[idx].note_type('TEXT')
                                        out.write(f"  {col_label} (TEXT): \"{txt}\"\n")
                                    except Exception:
                                        col_stats[idx].note_type('TEXT_AS_HEX')
                                        out.write(f"  {col_label} (TEXT/HEX): {binascii.hexlify(data).decode().upper()}\n")
                                    continue

                                proto_lines, proto_fields = evaluate_protobuf_matrix(data, indent=2)
                                if proto_lines is None:
                                    col_stats[idx].note_type('BLOB')
                                    out.write(f"  {col_label} (BLOB) Len={len(data)} HEX={binascii.hexlify(data).decode().upper()}\n")
                                else:
                                    col_stats[idx].note_type('PROTOBUF')
                                    col_stats[idx].note_proto_fields(proto_fields)
                                    out.write(f"  {col_label} (PROTOBUF) Len={len(data)}:\n")
                                    for pl in proto_lines:
                                        out.write("    " + pl + "\n")
                                continue

                            col_stats[idx].note_type('UNKNOWN')
                            if data is None:
                                out.write(f"  {col_label} (SERIAL {st}): [TRUNCATED]\n")
                            else:
                                out.write(f"  {col_label} (SERIAL {st}): HEX={binascii.hexlify(data).decode().upper()}\n")

                        if truncated:
                            out.write("  [!] WARNING: Database payload exceeds WAL local framing constraints.\n")
                        out.write("-" * 65 + "\n")

            # Schema Blueprint Summary Generation
            out.write("\n===========================================================\n")
            out.write("               SCHEMA BLUEPRINT SUMMARY                    \n")
            out.write("===========================================================\n")
            out.write(f"Total Structural Matrices Scanned: {total_rows}\n\n")

            if total_rows == 0:
                out.write("[-] Analytics Failed: No rows identified. Verify WAL integrity.\n")
                return

            for idx in sorted(col_stats.keys()):
                stats = col_stats[idx]
                present_pct = (stats.present_count / total_rows) * 100.0
                dominant = max(stats.type_counts.items(), key=lambda x: x[1])[0] if stats.type_counts else "UNKNOWN"

                proto_summary = ""
                if stats.protobuf_field_counts:
                    parts = []
                    for fnum in sorted(stats.protobuf_field_counts.keys()):
                        cnt = stats.protobuf_field_counts[fnum]
                        lengths = stats.protobuf_field_lengths.get(fnum, set())
                        if lengths:
                            length_notes = ",".join(str(l) for l in sorted(lengths))
                            key_note = " [Encryption Key Identified]" if 32 in lengths else ""
                            parts.append(f"{fnum} (Identified {cnt}x, len={length_notes}){key_note}")
                        else:
                            parts.append(f"{fnum} (Identified {cnt}x)")
                    proto_summary = "\n      └─ Protobuf Architecture: " + ", ".join(parts)

                out.write(f"Column {idx}: Dominant Type -> {dominant} (Allocation Rate: {present_pct:.1f}%)")
                if proto_summary:
                    out.write(proto_summary)
                out.write("\n")

            out.write("\n[END OF REPORT]\n")
            print(f"[+] Extraction Complete. Threat Intel Report exported to: {out_path}")

    except Exception as e:
        print(f"[!] System Exception during schema mapping: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Universal WAL Schema Mapping Engine")
    parser.add_argument("wal", help="Path to the target SQLite .db-wal asset")
    parser.add_argument("--out", default="wal_universal_map.txt", help="Export path for the blueprint summary")
    args = parser.parse_args()

    if not os.path.exists(args.wal):
        print(f"[!] Initialization Failure: WAL asset not located at {args.wal}")
        sys.exit(1)

    execute_wal_mapping(args.wal, args.out)

if __name__ == "__main__":
    main()