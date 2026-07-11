#!/usr/bin/env python3
import sqlite3
import struct
import binascii
import os
import time
import sys
import zlib
import argparse
from datetime import datetime
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

try:
    import win32file
    import win32con
except ImportError:
    print("[-] Error: 'pywin32' is not installed. Run: pip install pywin32")
    sys.exit(1)

# --- CONSTANTS ---
# Standard SQLite page sizes and WAL frame headers
PAGE_SIZE = 4096
FRAME_HEADER_SIZE = 24
WAL_HEADER_SIZE = 32
FRAME_SIZE = FRAME_HEADER_SIZE + PAGE_SIZE
FORENSIC_DB = "forensic_viewer.db"

# ==============================================================================
# 1. STRICT TYPE MAPPING (Reverse-Engineered Application States)
# ==============================================================================
# This dictionary maps the proprietary integer codes found in Column 16
# to their actual human-readable application states.
WA_MEDIA_TYPES = {
    0: "text",
    1: "image",
    2: "audio",
    3: "video",
    5: "location_latlong",
    8: "document",
    9: "url_text",
    10: "video_note",
    11: "location_group",
    19: "sticker",
    29: "reaction",
    1001: "status_or_ai",
    1006: "revoke_everyone",
    1016: "image_hd",
    1017: "video_hd",
    1020: "poll",
    1025: "admin_revoke",
    1027: "edit_text",       # Indicates message was modified post-sending
    1039: "audio_voice",
    1046: "view_once_media"  # Ephemeral media (Image/Video/Audio)
}

# ==============================================================================
# 2. DATABASE ENGINE (Sanitized Output Logging)
# ==============================================================================
def init_db():
    """Initializes the local SQLite database to store intercepted forensic telemetry."""
    conn = sqlite3.connect(FORENSIC_DB)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS messages_master (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        key_id TEXT,
        chat_jid TEXT,
        from_me INTEGER,
        timestamp INTEGER,
        raw_type_id INTEGER,
        mapped_type TEXT,
        text_content TEXT,
        media_url TEXT,
        media_mime TEXT,
        media_key TEXT,
        local_path TEXT,
        parent_key_id TEXT,
        edit_id TEXT,
        quoted_text_hint BLOB,
        protobuf_blob BLOB,
        captured_at TEXT
    )''')
    conn.commit()
    conn.close()

def insert_event(data):
    """Inserts deduplicated parsed rows into the telemetry database."""
    conn = sqlite3.connect(FORENSIC_DB)
    c = conn.cursor()
    try:
        # Deduplication check using Key ID, Timestamp, and Edit ID to track modifications
        c.execute("SELECT id FROM messages_master WHERE key_id=? AND timestamp=? AND edit_id=?",
                  (data['key_id'], data['timestamp'], data['edit_id']))
        if c.fetchone() is None:
            c.execute('''INSERT INTO messages_master (
                key_id, chat_jid, from_me, timestamp, raw_type_id, mapped_type,
                text_content, media_url, media_mime, media_key, local_path,
                parent_key_id, edit_id, quoted_text_hint, protobuf_blob, captured_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (
                data['key_id'], data['chat_jid'], data['from_me'], data['timestamp'],
                data['raw_type_id'], data['mapped_type'],
                data['text_content'], data['media_url'], data['media_mime'],
                data['media_key'], data['local_path'],
                data['parent_key_id'], data['edit_id'],
                data['quoted_text_hint'], data['protobuf_blob'],
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ))
            conn.commit()
            print(f"[+] CAPTURED: {data['mapped_type']} ({data['raw_type_id']}) | {data['key_id']}")
    except Exception as e:
        print(f"[!] DB Insert Error: {e}")
    finally:
        conn.close()

# ==============================================================================
# 3. SQLITE VARINT PARSING & CRYPTOGRAPHY
# ==============================================================================
def parse_record(payload):
    """
    Parses a raw SQLite record payload.
    Reads the header to determine serial types, then extracts the data sequentially.
    """
    if not payload: return []
    cursor = 0

    def read_varint_internal(data, offset):
        """Reads a SQLite Variable-Length Integer (Varint)."""
        value = 0
        for i in range(9):
            if offset + i >= len(data): return value, i
            byte = data[offset + i]
            value = (value << 7) | (byte & 0x7f)
            # If the MSB is 0, this is the last byte of the varint
            if (byte & 0x80) == 0: return value, i + 1
        return value, 9

    header_size, len_read = read_varint_internal(payload, cursor)
    cursor += len_read
    header_end = header_size
    serial_types = []

    # Extract all serial types from the record header
    while cursor < header_end:
        stype, len_read = read_varint_internal(payload, cursor)
        serial_types.append(stype)
        cursor += len_read

    values = []
    # Map serial types to actual data formats (Null, Integer, Float, Blob, Text)
    for stype in serial_types:
        if stype == 0: values.append(None)
        elif 1 <= stype <= 4:
            length = stype
            val = int.from_bytes(payload[cursor:cursor+length], 'big')
            values.append(val)
            cursor += length
        elif stype == 5:
            val = int.from_bytes(payload[cursor:cursor+6], 'big')
            values.append(val)
            cursor += 6
        elif stype == 6:
            val = int.from_bytes(payload[cursor:cursor+8], 'big')
            values.append(val)
            cursor += 8
        elif stype == 7:
            values.append(0.0) # Float placeholder
            cursor += 8
        elif stype == 8: values.append(0)
        elif stype == 9: values.append(1)
        elif stype >= 12 and (stype % 2 == 0):
            # Even types >= 12 are BLOBs
            length = (stype - 12) // 2
            values.append(payload[cursor:cursor+length])
            cursor += length
        elif stype >= 13 and (stype % 2 == 1):
            # Odd types >= 13 are TEXT
            length = (stype - 13) // 2
            text_data = payload[cursor:cursor+length]
            try: values.append(text_data.decode('utf-8', errors='replace'))
            except: values.append(str(text_data))
            cursor += length
    return values

def parse_sqlite_page(page_bytes, page_id):
    """
    Parses a decrypted SQLite page.
    Filters for Leaf Table pages (0x0D) and extracts cell pointers.
    """
    # 0x0D indicates a B-Tree Leaf Table Page containing actual data
    if page_bytes[0] != 0x0D: return []
    num_cells = struct.unpack('>H', page_bytes[3:5])[0]
    parsed_rows = []
    pointer_array_start = 8

    def read_varint_internal(data, offset):
        value = 0
        for i in range(9):
            if offset + i >= len(data): return value, i
            byte = data[offset + i]
            value = (value << 7) | (byte & 0x7f)
            if (byte & 0x80) == 0: return value, i + 1
        return value, 9

    for i in range(num_cells):
        ptr_offset = pointer_array_start + (i * 2)
        cell_start = struct.unpack('>H', page_bytes[ptr_offset:ptr_offset+2])[0]
        if cell_start == 0 or cell_start >= PAGE_SIZE: continue
        cursor = cell_start

        # Read payload size and row ID
        payload_size, len_read = read_varint_internal(page_bytes, cursor)
        cursor += len_read
        row_id, len_read = read_varint_internal(page_bytes, cursor)
        cursor += len_read

        # Handle potential payload overflow/truncation
        available_bytes = PAGE_SIZE - cursor
        actual_read_size = min(payload_size, available_bytes)
        payload_data = page_bytes[cursor : cursor + actual_read_size]

        columns = parse_record(payload_data)
        if columns:
            parsed_rows.append({"RowID": row_id, "Columns": columns})
    return parsed_rows

def decrypt_frame(frame_data, page_no, key_bytes):
    """
    Decrypts the AES-OFB encrypted SQLite frames.
    The Initialization Vector (IV) is derived from the Page Number (Little Endian)
    appended with the last 12 bytes of the frame data.
    """
    try:
        iv = struct.pack('<I', page_no) + frame_data[-12:]
        cipher = Cipher(algorithms.AES(key_bytes), modes.OFB(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        return decryptor.update(frame_data) + decryptor.finalize()
    except: return None

# ==============================================================================
# 4. MAIN INTERCEPTOR LOOP
# ==============================================================================
def run_forensic_parser(wal_full_path, key_hex):
    """Main execution loop: Memory-maps the WAL, checks salts, and intercepts frames."""
    init_db()
    try:
        key_bytes = binascii.unhexlify(key_hex)
    except Exception as e:
        print(f"[!] Invalid Key Format: {e}")
        sys.exit(1)

    print(f"[*] DETERMINISTIC FORENSIC PARSER STARTED")
    print(f"[*] Target WAL: {wal_full_path}")
    print(f"[*] STRICT TYPE ENFORCEMENT ACTIVE")

    seen_crcs = set()
    last_global_salt = None

    while True:
        hfile = None
        try:
            # Use Win32 API to create a shared read handle, avoiding file lock race conditions
            hfile = win32file.CreateFile(
                wal_full_path,
                win32con.GENERIC_READ,
                win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
                None,
                win32con.OPEN_EXISTING,
                0, 0
            )

            # Read up to 10MB blindly into active RAM for analysis
            win32file.SetFilePointer(hfile, 0, win32con.FILE_BEGIN)
            _, wal_data = win32file.ReadFile(hfile, 10 * 1024 * 1024)
            win32file.CloseHandle(hfile)
            hfile = None

            if len(wal_data) < 32:
                time.sleep(0.05); continue

            # Extract Global Salts to detect WAL resets/checkpoints
            global_salt1 = struct.unpack('>I', wal_data[16:20])[0]
            global_salt2 = struct.unpack('>I', wal_data[20:24])[0]
            current_salt_combo = (global_salt1, global_salt2)

            if current_salt_combo != last_global_salt:
                seen_crcs.clear()
                last_global_salt = current_salt_combo

            cursor = WAL_HEADER_SIZE

            # Iterate through all available frames
            while cursor + FRAME_SIZE <= len(wal_data):
                frame_chunk = wal_data[cursor : cursor + FRAME_SIZE]
                frame_header = frame_chunk[:FRAME_HEADER_SIZE]
                page_data = frame_chunk[FRAME_HEADER_SIZE:]

                # Verify Frame Salts match Global Salts (Ensures data is live, not dead disk sectors)
                f_salt1 = struct.unpack('>I', frame_header[8:12])[0]
                f_salt2 = struct.unpack('>I', frame_header[12:16])[0]

                if f_salt1 == global_salt1 and f_salt2 == global_salt2:
                    frame_crc = zlib.crc32(frame_chunk)

                    # Deduplicate based on frame checksum
                    if frame_crc not in seen_crcs:
                        seen_crcs.add(frame_crc)
                        page_no = struct.unpack('>I', frame_header[0:4])[0]

                        decrypted = decrypt_frame(page_data, page_no, key_bytes)
                        if decrypted:
                            rows = parse_sqlite_page(decrypted, page_no)
                            for row in rows:
                                cols = row['Columns']

                                # Message rows typically contain 50+ columns
                                if len(cols) >= 50:
                                    try:
                                        raw_type = cols[16] if isinstance(cols[16], int) else -1
                                        mapped_type_name = WA_MEDIA_TYPES.get(raw_type, f"UNKNOWN_{raw_type}")

                                        # Map columns to schema
                                        event = {
                                            'chat_jid': str(cols[1]) if cols[1] else None,
                                            'from_me': cols[2],
                                            'key_id': str(cols[3]) if cols[3] else "Unknown",
                                            'parent_key_id': str(cols[4]) if cols[4] else None,
                                            'edit_id': str(cols[5]) if cols[5] else None,
                                            'timestamp': cols[11],
                                            'text_content': str(cols[8]) if cols[8] else None,
                                            'raw_type_id': raw_type,
                                            'mapped_type': mapped_type_name,
                                            'media_url': str(cols[13]) if cols[13] else None,
                                            'media_mime': str(cols[15]) if cols[15] else None,
                                            'media_key': None,
                                            'local_path': str(cols[26]) if cols[26] else None,
                                            'quoted_text_hint': None,
                                            'protobuf_blob': None
                                        }

                                        # Caption Override
                                        if cols[22]:
                                            event['text_content'] = str(cols[22])

                                        # Extract Encrypted Media Key (Col 23)
                                        if isinstance(cols[23], bytes):
                                            event['media_key'] = binascii.hexlify(cols[23]).decode()

                                        # Extract Protobuf payloads for advanced analysis
                                        if isinstance(cols[30], bytes):
                                            event['quoted_text_hint'] = cols[30]
                                        if isinstance(cols[39], bytes):
                                            event['protobuf_blob'] = cols[39]

                                        insert_event(event)
                                    except Exception as e:
                                        pass
                cursor += FRAME_SIZE
            time.sleep(0.05)
        except KeyboardInterrupt:
            print("[*] Stopping Forensic Parser...")
            break
        except Exception as e:
            if hfile:
                try: win32file.CloseHandle(hfile)
                except: pass
            time.sleep(0.1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Deterministic SQLite WAL Forensic Parser")
    parser.add_argument("--wal", required=True, help="Path to the target .db-wal file")
    parser.add_argument("--key", required=True, help="64-character hex decryption key")

    args = parser.parse_args()

    if not os.path.exists(args.wal):
        print(f"[!] Error: WAL file not found at {args.wal}")
        sys.exit(1)

    run_forensic_parser(args.wal, args.key)