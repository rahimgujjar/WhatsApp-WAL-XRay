#!/usr/bin/env python3
"""
wal_inspect_col_ranges.py

Analyzes forensic data structures to flag transactional matrices containing
anomalous or corrupted data types within targeted parameter columns.
"""

import sys
import argparse
import os
from remove_events import load_lines, find_event_blocks, collect_columns_in_block

def is_string_or_int_dtype(dtype_string: str) -> bool:
    safe_types = ["TEXT STRING", "INTEGER", "BOOLEAN", "TIMESTAMP", "URL"]
    return any(safe in dtype_string.upper() for safe in safe_types)

def audit_column_anomalies(path: str, inspect_col: int) -> None:
    lines = load_lines(path)
    blocks = find_event_blocks(lines)
    count = 0

    for idx, (s, e) in enumerate(blocks, 1):
        cols = collect_columns_in_block(lines, s, e)
        col_entries = cols.get(inspect_col)

        if not col_entries:
            continue

        any_ok = any(is_string_or_int_dtype(dtype) for (_i, _raw, dtype) in col_entries)

        if not any_ok:
            count += 1
            print(f"BLOCK #{idx} lines {s + 1}-{e + 1}")
            for (_i, raw, dtype) in col_entries:
                print(f"  Col{inspect_col} @ line {_i + 1}: raw='{raw}'  dtype='{dtype}'")
            print("-" * 40)

    print("Total flagged blocks:", count)

def main():
    parser = argparse.ArgumentParser(description="Structural Schema Integrity Auditor")
    parser.add_argument("--file", default="data_source.txt", help="Target telemetry log for schema validation")
    parser.add_argument("--col", type=int, default=6, help="Primary validation column (default: 6)")
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"[!] Error: File not located at {args.file}")
        sys.exit(1)

    audit_column_anomalies(args.file, args.col)

if __name__ == "__main__":
    main()