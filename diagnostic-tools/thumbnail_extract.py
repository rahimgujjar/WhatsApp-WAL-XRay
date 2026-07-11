#!/usr/bin/env python3
"""
thumbnail_extract.py

Forensic Binary Carving Utility
Designed to ingest raw hexadecimal strings extracted from protobuf columns (e.g., Column 39)
and reconstruct the underlying media payloads (such as encrypted view-once thumbnails) into
standard file formats.
"""

import argparse
import binascii
import sys
import os

def carve_binary_payload(hex_data: str, output_path: str) -> None:
    """Decodes a hex string and writes the raw binary stream to the specified output asset."""
    try:
        # Strip potential whitespace or newlines from raw log copies
        clean_hex = hex_data.replace(" ", "").replace("\n", "").replace("\r", "")
        binary_data = binascii.unhexlify(clean_hex)

        with open(output_path, "wb") as f:
            f.write(binary_data)

        print(f"[+] Extraction Successful: Payload carved and exported to '{output_path}'")
    except binascii.Error:
        print("[-] Error: Invalid hexadecimal payload provided. Ensure data is not truncated.")
        sys.exit(1)
    except Exception as e:
        print(f"[-] System Error during extraction: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Forensic Media Payload Extractor")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--hex", help="Direct hexadecimal string input")
    group.add_argument("--file", help="Path to a text file containing the hex string")

    parser.add_argument("--out", default="recovered_artifact.jpg", help="Output file path (default: recovered_artifact.jpg)")

    args = parser.parse_args()

    hex_payload = ""
    if args.file:
        if not os.path.exists(args.file):
            print(f"[-] Error: Input file not found at {args.file}")
            sys.exit(1)
        with open(args.file, "r", encoding="utf-8") as f:
            hex_payload = f.read()
    else:
        hex_payload = args.hex

    print("[*] Initiating Binary Carving Sequence...")
    carve_binary_payload(hex_payload, args.out)

if __name__ == "__main__":
    main()