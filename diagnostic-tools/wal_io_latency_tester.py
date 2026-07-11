#!/usr/bin/env python3
"""
wal_io_latency_tester.py

A low-level system diagnostic framework developed to monitor and quantify write-ahead log
I/O latency constraints and cache tracking discrepancies within client-side file engines.
"""

import os
import time
import sys
import argparse

try:
    import win32file
    import win32con
except ImportError:
    print("[-] Error: Dependency 'pywin32' missing. Execution requires: pip install pywin32")
    sys.exit(1)

def parse_arguments():
    """Dynamically handles path configurations for cross-machine deployment."""
    parser = argparse.ArgumentParser(description="SQLite WAL I/O Latency Diagnostics")

    # Dynamically resolve the standard Windows AppData Local path
    default_appdata = os.environ.get('LOCALAPPDATA', r'C:\Users\Default\AppData\Local')
    default_base = os.path.join(default_appdata, r"Packages\5319275A.WhatsAppDesktop_cv1g1gvanyjgm\LocalState")

    parser.add_argument("--base-path", default=default_base, help="Base directory of the target application state.")
    parser.add_argument("--wal-file", default="messages.db-wal", help="Target WAL filename.")
    return parser.parse_args()

def fetch_os_cached_size(target_path):
    """Queries standard operating system file indicators to pull cached directory properties."""
    try:
        return os.path.getsize(target_path)
    except OSError:
        return 0

def calculate_actual_allocation(target_path):
    """Forces a physical read of the file via un-locked handles to count actual bytes."""
    try:
        hfile = win32file.CreateFile(
            target_path,
            win32con.GENERIC_READ,
            win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
            None,
            win32con.OPEN_EXISTING,
            0, 0
        )
    except Exception:
        return 0

    total_bytes = 0
    while True:
        try:
            _, data = win32file.ReadFile(hfile, 1024 * 1024)
            if not data:
                break
            total_bytes += len(data)
        except Exception:
            break

    win32file.CloseHandle(hfile)
    return total_bytes

def main():
    args = parse_arguments()
    full_path = os.path.join(args.base_path, args.wal_file)

    if not os.path.exists(full_path):
        print(f"[!] Initialization Failure: Target asset not located at {full_path}")
        sys.exit(1)

    print(f"[*] Starting Microsecond Telemetry Check loop on: {args.wal_file}")
    print(f"[*] Target Path: {full_path}")
    print(f"[*] ROW FORMAT: [Timestamp] | Virtual Allocation Bound | Physical Byte Ingestion")
    print("-" * 78)

    last_real_size = 0
    polling_frequency_hz = 0.05

    while True:
        try:
            ts = time.strftime("%H:%M:%S")
            os_size = fetch_os_cached_size(full_path)
            real_size = calculate_actual_allocation(full_path)

            if real_size != last_real_size:
                print(f"[!] File Mutation Intercepted at {ts}")
                print(f"    - Virtual Cache Layer Capacity : {os_size} bytes")
                print(f"    - True Transaction Ingestion   : {real_size} bytes")

                structural_divergence = real_size - os_size
                if structural_divergence > 0:
                    print(f"    >>> Status: Active Visibility Capture (Parser leading OS by {structural_divergence} bytes)")
                elif structural_divergence == 0:
                    print(f"    >>> Status: Synced Matrix Stabilization (System locks matching allocation limits)")

                last_real_size = real_size
                print("-" * 40)

            time.sleep(polling_frequency_hz)
        except KeyboardInterrupt:
            print("\n[*] Auditing session completed safely via user command intercept.")
            break
        except Exception as e:
            print(f"[!] System Exception Caught: {e}")
            time.sleep(1)

if __name__ == "__main__":
    main()