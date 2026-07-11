#!/usr/bin/env python3
"""
wal_debug_cols.py

Parses operational telemetry blocks to map and validate standard architectural
routing endpoints (JIDs, LIDs, and Broadcast channels).
"""

import re
import sys
import argparse
import os
from typing import List

COL_REGEX = re.compile(r"\s*Col\s+(\d+)\s*:\s*(.*)")

def get_pattern_name(value: str) -> str:
    v = value.strip()
    if re.match(r"^<BLOB len=\d+>$", v): return "TYPE: BINARY BLOB"
    if re.match(r"^\d+@s\.whatsapp\.net$", v): return "TYPE: USER JID (@s.whatsapp.net)"
    if re.match(r"^\d+:\d+@s\.whatsapp\.net$", v): return "TYPE: COMPOUND USER JID (Phone:Device@s.whatsapp.net)"
    if re.match(r"^status@broadcast$", v): return "TYPE: BROADCAST STATUS (@broadcast)"
    if re.match(r"^\d+@g\.us$", v): return "TYPE: GROUP JID (@g.us)"
    if re.match(r"^\d+:\d+@g\.us$", v): return "TYPE: COMPOUND GROUP JID (Phone-Time@g.us)"
    if re.match(r"^\d+@lid$", v): return "TYPE: LID (@lid)"
    if re.match(r"^\d+:\d+@lid$", v): return "TYPE: COMPOUND LID (Phone:Instance@lid)"

    if len(v) in (20, 32) and re.match(r"^[A-F0-9]+$", v):
        return f"TYPE: HEX KEY ({len(v)} chars)"

    if v.isdigit():
        if len(v) == 13 and v.startswith("17"): return "TYPE: TIMESTAMP (Milliseconds)"
        if len(v) == 10 and v.startswith("17"): return "TYPE: TIMESTAMP (Seconds)"
        if v in ("0", "1"): return "TYPE: BOOLEAN INT (0/1)"
        return "TYPE: INTEGER (Raw Number)"

    if "http://" in v or "https://" in v: return "TYPE: URL / LINK"
    return "TYPE: TEXT STRING"

def scan_telemetry_blocks(lines: List[str], target_cols: set) -> None:
    event_starts = [i for i, l in enumerate(lines) if l.lstrip().startswith("[EVENT]")]
    if not event_starts:
        print("No [EVENT] blocks found.")
        sys.exit(0)

    for idx, start in enumerate(event_starts):
        end = event_starts[idx + 1] - 1 if idx + 1 < len(event_starts) else len(lines) - 1
        found = []

        for i in range(start, end + 1):
            m = COL_REGEX.match(lines[i])
            if m:
                c = int(m.group(1))
                raw_data = m.group(2).rstrip("\n")
                if c in target_cols:
                    found.append((c, i + 1, raw_data, get_pattern_name(raw_data)))

        if found:
            print(f"EVENT {start + 1}-{end + 1}:")
            for c, lineno, raw, dtype in found:
                print(f"  Col {c} @ line {lineno}: raw='{raw}'  ->  {dtype}")
            print("-" * 40)

def main():
    parser = argparse.ArgumentParser(description="Endpoint Routing Telemetry Scanner")
    parser.add_argument("--file", default="data_source.txt", help="Path to the log file (default: data_source.txt)")
    parser.add_argument("--cols", nargs="+", type=int, default=[1, 2], help="Target columns to audit (default: 1 2)")
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"[!] Error: File not found at {args.file}")
        sys.exit(1)

    with open(args.file, "r", encoding="utf-8", errors="ignore") as fh:
        raw_lines = fh.readlines()

    scan_telemetry_blocks(raw_lines, set(args.cols))

if __name__ == "__main__":
    main()