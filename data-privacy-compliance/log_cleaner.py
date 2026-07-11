#!/usr/bin/env python3
"""
log_cleaner.py

Data Sanitization and Deduplication Pipeline
Audits raw SQLite Write-Ahead Log events to systematically detect, isolate, and remove
Personally Identifiable Information (PII) such as phone numbers, while generating
cryptographic signatures to drop redundant telemetry blocks.
"""

import os
import re
import unicodedata
import argparse
from typing import List, Tuple

# Pre-compiled Operational Regex Rules for PII Detection
JID_RE = re.compile(r"\b\+?92\d{9,}\S*@\S+\b", re.IGNORECASE)
GROUP_RE = re.compile(r"\b\+?92\d{6,}-\d+@\S+\b", re.IGNORECASE)
NUM_CORE_RE = re.compile(r"\b(?:\+?92)\d{9,}\b")
GENERIC_PHONE_RE = re.compile(r"\b\d{9,15}\b")
PHONE_REGEXES = [JID_RE, GROUP_RE, NUM_CORE_RE, GENERIC_PHONE_RE]

COL_LINE_RE = re.compile(r"^\s*Col\s+(\d+)\s*:\s*(.*)$", re.IGNORECASE)

def normalize_telemetry_text(s: str) -> str:
    """Enforces standard character constraints across volatile parsed data matrices."""
    if s is None:
        return ""
    s = unicodedata.normalize("NFKC", s)
    s = s.lstrip("\ufeff")
    s = "".join(ch for ch in s if not unicodedata.category(ch).startswith("C"))
    s = re.sub(r"\s+", " ", s)
    return s.strip()

def segment_event_blocks(content: str) -> List[str]:
    """Divides monolithic log files into discrete transactional arrays."""
    parts = content.split("[EVENT]")
    events = []
    for p in parts:
        if not p.strip():
            continue
        events.append("[EVENT]" + p)
    return events

def detect_pii_signatures(ev_body: str, debug_lines: List[str], idx: int) -> bool:
    """Cross-references structural event rows against active compliance patterns."""
    norm_body = normalize_telemetry_text(ev_body)

    # Granular Column-Level Analysis
    for line in ev_body.splitlines():
        m = COL_LINE_RE.match(line)
        if not m:
            continue
        colnum = int(m.group(1))
        raw_val = m.group(2)
        norm_val = normalize_telemetry_text(raw_val)

        for rx in PHONE_REGEXES:
            if rx.search(norm_val):
                debug_lines.append(f"Event#{idx} FLAG: Col{colnum} matched compliance regex={rx.pattern}\n")
                return True

        digits = re.sub(r"\D", "", norm_val)
        if len(digits) >= 9:
            debug_lines.append(f"Event#{idx} FLAG: Col{colnum} numeric_core triggered\n")
            return True

    # Broad Event-Level Analysis
    for rx in PHONE_REGEXES:
        if rx.search(norm_body):
            debug_lines.append(f"Event#{idx} FLAG: Event payload matched regex={rx.pattern}\n")
            return True

    digits_event = re.sub(r"\D", "", norm_body)
    if len(digits_event) >= 11 and NUM_CORE_RE.search(digits_event):
        debug_lines.append(f"Event#{idx} FLAG: Event numeric core fallback triggered\n")
        return True

    return False

def generate_deduplication_signature(ev: str, key_cols: Tuple[int,int]=(1,52)) -> str:
    """Constructs a deterministic canonical state string to identify redundant frames."""
    body = ev[len("[EVENT]"):]
    cols = {}
    for line in body.splitlines():
        m = COL_LINE_RE.match(line)
        if not m:
            continue
        colnum = int(m.group(1))
        cols[colnum] = normalize_telemetry_text(m.group(2))

    key_vals = [cols.get(c, "") for c in key_cols]
    if any(key_vals):
        return "KEYSIG::" + "||".join(key_vals)

    sorted_lines = [f"Col{k}:{cols[k]}" for k in sorted(cols.keys())]
    return "COLSORT::" + "|".join(sorted_lines)

def main():
    parser = argparse.ArgumentParser(description="PII Sanitization and Deduplication Engine")
    parser.add_argument("--input", required=True, help="Path to the raw forensic log file")
    parser.add_argument("--out", default="cleaned_final.txt", help="Export path for sanitized logs")
    parser.add_argument("--debug-log", default="matches_debug.txt", help="Export path for flagged compliance matches")
    parser.add_argument("--dry-run", action="store_true", help="Flag matches without deleting them from the output")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"[!] Initialization Failure: Target asset not located at {args.input}")
        return

    with open(args.input, "r", encoding="utf-8-sig", errors="replace") as fh:
        content = fh.read()

    events = segment_event_blocks(content)
    total = len(events)
    print(f"[*] Pipeline initialized. Total structural frames loaded: {total}")

    cleaned = []
    seen_signatures = set()
    deleted_by_phone = 0
    deleted_dupe = 0
    debug_lines = []

    for idx, ev in enumerate(events, start=1):
        body = ev[len("[EVENT]"):]

        # Phase 1: PII Compliance Filtering
        if detect_pii_signatures(body, debug_lines, idx):
            deleted_by_phone += 1
            if args.dry_run:
                cleaned.append(ev)
            continue

        # Phase 2: Hash-Based Deduplication
        sig = generate_deduplication_signature(ev)
        if sig in seen_signatures:
            deleted_dupe += 1
            continue

        seen_signatures.add(sig)
        cleaned.append(ev)

    with open(args.debug_log, "w", encoding="utf-8") as dbg:
        dbg.write("".join(debug_lines) or "No compliance matches flagged.\n")

    with open(args.out, "w", encoding="utf-8") as out:
        out.write("".join(cleaned))

    print("-" * 60)
    print(f"    - Compliance Flags Triggered (PII Removed): {deleted_by_phone}")
    print(f"    - Redundant Matrices Dropped: {deleted_dupe}")
    print(f"    - Total Sanitized Outputs Remaining: {len(cleaned)}")
    print(f"[+] Output exported safely to: {args.out}")
    print("-" * 60)

if __name__ == "__main__":
    main()