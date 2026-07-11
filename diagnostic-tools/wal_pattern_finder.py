#!/usr/bin/env python3
"""
pattern_finder.py

Automated engine that recursively scans outputs, classifying structural
payloads into standardized parent-child relationship matrices.
"""

import re
import glob
import os
import sys
import string
import argparse

_re_user_jid = re.compile(r"^\d+@s\.whatsapp\.net$")
_re_group_jid = re.compile(r"^\d+@g\.us$")
_re_lid = re.compile(r"^\d+@lid$")
_re_compound_lid = re.compile(r"^\d+-\d+@lid$")
_re_compound_group = re.compile(r"^\d+-\d+@g\.us$")
_re_compound_user = re.compile(r"^\d+-\d+@s\.whatsapp\.net$")
_re_hex20_32 = re.compile(r"^[A-Fa-f0-9]{20}$|^[A-Fa-f0-9]{32}$")

def is_hex_string(s: str) -> bool:
    return all(ch in string.hexdigits for ch in s)

def get_pattern_name(value: str) -> tuple:
    v = value.strip()

    if v.startswith("<BLOB len=") and v.endswith(">"):
        return ("BINARY BLOB", v)
    if v.startswith("[MEDIA KEY]:"):
        hexpart = v[len("[MEDIA KEY]:"):].strip()
        if hexpart and is_hex_string(hexpart):
            return ("BINARY BLOB", f"MEDIA KEY ({len(hexpart)} hex chars)")
        return ("BINARY BLOB", "MEDIA KEY (non-hex)")
    if v == "<BINARY STRING>":
        return ("BINARY BLOB", "<BINARY STRING>")
    if v == "<FLOAT>":
        return ("REAL", "<FLOAT>")

    if _re_user_jid.match(v): return ("TEXT STRING", "USER JID (@s.whatsapp.net)")
    if v == "status@broadcast": return ("TEXT STRING", "BROADCAST STATUS (@broadcast)")
    if _re_group_jid.match(v): return ("TEXT STRING", "GROUP JID (@g.us)")
    if _re_lid.match(v): return ("TEXT STRING", "LID (@lid)")
    if _re_compound_lid.match(v): return ("TEXT STRING", "COMPOUND LID (Phone-Time@lid)")
    if _re_compound_group.match(v): return ("TEXT STRING", "COMPOUND GROUP JID (Phone-Time@g.us)")
    if _re_compound_user.match(v): return ("TEXT STRING", "COMPOUND USER JID (Phone-Instance@s.whatsapp.net)")

    if "@" in v and v.endswith("@s.whatsapp.net") and (":" in v or "/" in v or "-" in v):
        return ("TEXT STRING", "COMPOUND USER JID (Phone/Any_RAW INTEGER:Instance@s.whatsapp.net)")

    if _re_hex20_32.match(v):
        return ("TEXT STRING", f"HEX KEY ({len(v)} chars)")

    if v.isdigit():
        length = len(v)
        if length == 13 and v.startswith("17"): return ("INTEGER (Raw Number)", "TIMESTAMP (Milliseconds)")
        if length == 10 and v.startswith("17"): return ("INTEGER (Raw Number)", "TIMESTAMP (Seconds)")
        if v in ("0", "1"): return ("INTEGER (Raw Number)", "BOOLEAN INT (0/1)")
        return ("INTEGER (Raw Number)", None)

    try:
        _ = float(v)
        if "." in v or "e" in v.lower() or "E" in v:
            return ("REAL", "<FLOAT>")
    except ValueError:
        pass

    if v.startswith("http://") or v.startswith("https://") or v.startswith("www."):
        return ("TEXT STRING", "URL / LINK")

    return ("TEXT STRING", None)

def analyze_logs(target_pattern: str, output_file: str) -> None:
    print("[*] Starting 'The Heuristic Ledger Classifier' (safe mode)...")

    files = glob.glob(target_pattern)
    if not files:
        print(f"[!] No files found matching {target_pattern}")
        return

    col_analysis = {}
    line_regex = re.compile(r"\s*Col\s+(\d+):\s+(.*)")

    for file_path in files:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as fh:
                for lineno, line in enumerate(fh, start=1):
                    if "[EVENT]" in line:
                        continue
                    m = line_regex.match(line)
                    if not m:
                        continue

                    col_idx = int(m.group(1))
                    raw_val = m.group(2)
                    parent, child = get_pattern_name(raw_val)

                    if col_idx not in col_analysis:
                        col_analysis[col_idx] = {}
                    parent_bucket = col_analysis[col_idx].setdefault(parent, {})
                    child_label = child if child is not None else "<PARENT ONLY>"

                    examples = parent_bucket.setdefault(child_label, set())
                    if len(examples) < 3:
                        examples.add(f"{os.path.basename(file_path)}:{lineno}")
        except Exception as e:
            print(f"[!] Error reading {file_path}: {e}", file=sys.stderr)

    with open(output_file, 'w', encoding='utf-8') as report:
        report.write("========================================================\n")
        report.write("      THE HEURISTIC LEDGER CLASSIFIER - SAFE REPORT     \n")
        report.write("========================================================\n\n")
        if not col_analysis:
            report.write("[No column data detected]\n\n")
        else:
            for col_idx in sorted(col_analysis.keys()):
                report.write(f"COLUMN {col_idx}:\n")
                for parent in sorted(col_analysis[col_idx].keys()):
                    report.write(f"   PARENT: {parent}\n")
                    child_map = col_analysis[col_idx][parent]
                    children_sorted = sorted([c for c in child_map.keys() if c != "<PARENT ONLY>"])
                    if "<PARENT ONLY>" in child_map:
                        children_sorted.append("<PARENT ONLY>")

                    for child in children_sorted:
                        if child == "<PARENT ONLY>":
                            report.write("      - (no child type detected; value classified as parent only)\n")
                        else:
                            report.write(f"      - CHILD: {child}\n")

                        examples = sorted(list(child_map[child])) if child in child_map else []
                        if examples:
                            report.write(f"          Examples (file:line): {'; '.join(examples)}\n")
                        else:
                            report.write("          Examples (file:line): None captured\n")
                    report.write("   " + "-" * 36 + "\n")
                report.write("-" * 60 + "\n")
        report.write("\n[END OF REPORT]\n")

    print(f"[*] Done. Report written to '{output_file}'.")

def main():
    parser = argparse.ArgumentParser(description="Heuristic Ledger Classification Engine")
    parser.add_argument("--pattern", default="Undeniable_Output_of_Working_WAL_Parser.md", help="Input file path or wildcard pattern")
    parser.add_argument("--out", default="WA-WAL_Telemetry_State_Ledger.md", help="Output path for the generated report")
    args = parser.parse_args()

    analyze_logs(args.pattern, args.out)

if __name__ == "__main__":
    main()