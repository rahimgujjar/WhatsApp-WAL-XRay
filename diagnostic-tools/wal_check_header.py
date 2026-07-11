#!/usr/bin/env python3
"""
wal_check_header.py

Diagnostic utility to verify the cryptographic encryption state of Write-Ahead Log (WAL)
database components by analyzing low-level header byte allocations and framing matrices.
"""

import argparse
import binascii
import sys
import os

def check_header(target_path: str) -> None:
    try:
        with open(target_path, 'rb') as f:
            header = f.read(32)
            print(f"[*] WAL Header (First 4 bytes): {binascii.hexlify(header[:4]).decode('utf-8').upper()}")

            f.read(24)

            page_data = f.read(16)
            primary_byte = page_data[0]
            print(f"[*] First Page Byte: {hex(primary_byte).upper()}")

            print("-" * 50)
            if primary_byte == 0x0D:
                print("RESULT: File is DECRYPTED (Ready to read).")
            else:
                print("RESULT: File is ENCRYPTED (Needs Key).")
                print(f"      (Expected 0x0d, but got {hex(primary_byte).upper()})")
            print("-" * 50)

    except IOError as e:
        print(f"[!] Access Exception: Unable to read target file. {e}")
        sys.exit(1)
    except Exception as e:
        print(f"[!] System Exception: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="WAL Cryptographic State Auditor")
    parser.add_argument("path", help="Full path to the target .db-wal asset")
    args = parser.parse_args()

    if not os.path.exists(args.path):
        print(f"[!] Error: Target asset not located at {args.path}")
        sys.exit(1)

    check_header(args.path)

if __name__ == "__main__":
    main()