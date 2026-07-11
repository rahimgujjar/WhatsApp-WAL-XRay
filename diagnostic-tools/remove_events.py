#!/usr/bin/env python3
"""
remove_events.py

Telemetry Event Filtering Engine
A modular structural parser designed to strip background noise, internal routing flags,
and unallocated fragments from forensic log arrays via logical AND/OR evaluations and
RegEx pattern matching.
"""
from __future__ import annotations
import re
import argparse
import sys
import os
from typing import List, Tuple, Dict, Any, Optional

DEFAULT_TARGET_FILE = "data_source.txt"

def classify_telemetry_type(value: str) -> str:
    """Maps raw string parameters to their underlying database architectural types."""
    v = value.strip()
    if re.match(r"^<BLOB len=\d+>$", v): return "TYPE: BINARY BLOB"
    if re.match(r"^\d+:\d+@lid$", v): return "TYPE: COMPOUND LID (Phone:Instance@lid)"
    if re.match(r"^\d+@s\.whatsapp\.net$", v): return "TYPE: USER JID (@s.whatsapp.net)"
    if re.match(r"^status@broadcast$", v): return "TYPE: BROADCAST STATUS (@broadcast)"
    if re.match(r"^\d+@g\.us$", v): return "TYPE: GROUP JID (@g.us)"
    if re.match(r"^\d+@lid$", v): return "TYPE: LID (@lid)"
    if re.match(r"^\d+-\d+@g\.us$", v): return "TYPE: COMPOUND GROUP JID (Phone-Time@g.us)"
    if re.match(r"^\d+-\d+@lid$", v): return "TYPE: COMPOUND LID (Phone-Time@lid)"
    if len(v) in (20, 32) and re.match(r"^[A-F0-9]+$", v): return f"TYPE: HEX KEY ({len(v)} chars)"

    if v.isdigit():
        length = len(v)
        if length == 13 and v.startswith("17"): return "TYPE: TIMESTAMP (Milliseconds)"
        if length == 10 and v.startswith("17"): return "TYPE: TIMESTAMP (Seconds)"
        if v in ("0", "1"): return "TYPE: BOOLEAN INT (0/1)"
        return "TYPE: INTEGER (Raw Number)"

    if "https://" in v or "http://" in v: return "TYPE: URL / LINK"
    return "TYPE: TEXT STRING"

def load_telemetry_lines(path: str) -> List[str]:
    with open(path, "r", encoding="utf-8", errors="ignore") as fh:
        return fh.readlines()

def write_telemetry_inplace(path: str, lines: List[str]) -> None:
    with open(path, "w", encoding="utf-8") as fh:
        fh.writelines(lines)

def segment_telemetry_blocks(lines: List[str]) -> List[Tuple[int, int]]:
    """Identifies and indexes independent structural frames within the raw log."""
    event_starts = [i for i, line in enumerate(lines) if line.lstrip().startswith("[EVENT]")]
    blocks: List[Tuple[int, int]] = []
    for idx, start in enumerate(event_starts):
        end = (event_starts[idx + 1] - 1) if idx + 1 < len(event_starts) else (len(lines) - 1)
        blocks.append((start, end))
    return blocks

def compile_logical_conditions(and_string: Optional[str]) -> List[Dict[str, Any]]:
    """Parses user-provided argument strings into actionable validation rulesets."""
    if not and_string:
        return []
    parts = and_string.split("&")
    conditions: List[Dict[str, Any]] = []
    for p in parts:
        p = p.strip()
        if not p: continue

        m = re.match(r"^Col\s*(\d+)\s*=(.*)$", p, flags=re.IGNORECASE)
        if m:
            col = int(m.group(1))
            raw_val = m.group(2).strip()
            alts = [a.strip() for a in raw_val.split("|") if a.strip()]
            parsed_alts = []

            for alt in alts:
                if alt.upper().startswith("TYPE:"):
                    parsed_alts.append(("type", alt))
                elif alt.upper().startswith("REGEX:"):
                    pattern = alt[len("REGEX:"):].strip()
                    try: cre = re.compile(pattern)
                    except re.error as e: raise ValueError(f"Invalid REGEX for Col{col}: {e}")
                    parsed_alts.append(("regex", cre))
                elif alt.upper().startswith("CONTAINS:"):
                    parsed_alts.append(("contains", alt[len("CONTAINS:"):].strip()))
                else:
                    parsed_alts.append(("raw", alt))

            types = set(t for t, _ in parsed_alts)
            if len(types) == 1:
                t = parsed_alts[0][0]
                vals = [v for _, v in parsed_alts]
                if t == "regex": conditions.append({"col": col, "match_type": "regex_list", "value": vals})
                else: conditions.append({"col": col, "match_type": t + "_list", "value": vals})
            else:
                conditions.append({"col": col, "match_type": "mixed", "value": parsed_alts})
        else:
            m2 = re.match(r"^Col\s*(\d+)$", p, flags=re.IGNORECASE)
            if m2:
                col = int(m2.group(1))
                conditions.append({"col": col, "match_type": "exists", "value": None})
            else:
                raise ValueError(f"Invalid condition format: '{p}'")
    return conditions

def extract_column_matrix(lines: List[str], start: int, end: int) -> Dict[int, List[Tuple[int, str, str]]]:
    """Maps dynamic field indices to their respective raw values and resolved types."""
    col_entries: Dict[int, List[Tuple[int, str, str]]] = {}
    col_regex = re.compile(r"\s*Col\s+(\d+)\s*:\s*(.*)")
    for i in range(start, end + 1):
        m = col_regex.match(lines[i])
        if m:
            c = int(m.group(1))
            raw = m.group(2).rstrip("\n").strip()
            dtype = classify_telemetry_type(raw)
            col_entries.setdefault(c, []).append((i, raw, dtype))
    return col_entries

def evaluate_structural_match(raw: str, dtype: str, cond: Dict[str, Any]) -> bool:
    """Executes the validation rule against the isolated column element."""
    mt = cond["match_type"]
    val = cond["value"]

    if mt == "exists": return True
    if mt == "raw": return raw == val
    if mt == "contains": return val in raw
    if mt == "type": return dtype == val
    if mt == "regex": return val.search(raw) is not None
    if mt == "raw_list": return any(raw == v for v in val)
    if mt == "contains_list": return any(v in raw for v in val)
    if mt == "type_list": return any(dtype == v for v in val)
    if mt == "regex_list": return any(v.search(raw) is not None for v in val)
    if mt == "mixed":
        for t, v in val:
            if t == "type" and dtype == v: return True
            if t == "raw" and raw == v: return True
            if t == "contains" and v in raw: return True
            if t == "regex" and v.search(raw): return True
        return False
    return False

def check_logical_and_constraints(col_entries: Dict[int, List[Tuple[int, str, str]]], conditions: List[Dict[str, Any]]) -> Tuple[bool, List[int]]:
    if not conditions: return False, []

    for cond in conditions:
        if not col_entries.get(cond["col"]): return False, []

    for cond in conditions:
        entries = col_entries.get(cond["col"], [])
        matched = any(evaluate_structural_match(raw, dtype, cond) for (_, raw, dtype) in entries)
        if matched: return False, []

    examples: List[int] = []
    for cond in conditions:
        entries = col_entries.get(cond["col"], [])
        if entries: examples.append(entries[0][0] + 1)
        if len(examples) >= 3: break

    return True, examples

def unify_deletion_ranges(ranges: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """Merges contiguous exclusion blocks for efficient memory operations."""
    if not ranges: return []
    ranges = sorted(ranges, key=lambda x: x[0])
    merged: List[Tuple[int, int]] = []
    cur_s, cur_e = ranges[0]

    for s, e in ranges[1:]:
        if s <= cur_e + 1: cur_e = max(cur_e, e)
        else:
            merged.append((cur_s, cur_e))
            cur_s, cur_e = s, e

    merged.append((cur_s, cur_e))
    return merged

def build_regex_alternatives(value: Optional[str]) -> List[Tuple[str, Any]]:
    if not value: return []
    alts = [a.strip() for a in value.split("|") if a.strip()]
    out: List[Tuple[str, Any]] = []

    for alt in alts:
        if alt.upper().startswith("REGEX:"):
            pat = alt[len("REGEX:"):].strip()
            try: cre = re.compile(pat)
            except re.error as e: raise ValueError(f"Invalid REGEX in pattern list: {e}")
            out.append(("regex", cre))
        else:
            out.append(("contains", alt))
    return out

def verify_column_exclusion(raw: str, alts: List[Tuple[str, Any]]) -> bool:
    for kind, spec in alts:
        if kind == "contains":
            if spec in raw: return True
        else:
            if spec.search(raw): return True
    return False

def execute_pipeline_filtering(path: str, conditions: List[Dict[str, Any]], min_cols: Optional[int] = None,
                               dry_run: bool = False, verbose: bool = False, invert: bool = False,
                               remove_col_has_alts: Optional[List[Tuple[str, Any]]] = None,
                               remove_any_col_has_alts: Optional[List[Tuple[str, Any]]] = None,
                               inspect_col: int = 6) -> Dict[str, Any]:
    lines = load_telemetry_lines(path)
    blocks = segment_telemetry_blocks(lines)

    if verbose: print(f"[*] Diagnostics: Total structural frames indexed = {len(blocks)}")

    to_remove: List[Tuple[int, int]] = []
    removal_examples: List[Tuple[int, int, List[int]]] = []
    col_line_re = re.compile(r"\s*Col\s+(\d+)\s*:")

    for (start, end) in blocks:
        col_count = sum(1 for i in range(start, end + 1) if col_line_re.match(lines[i]))

        remove_by_mincols = False
        if min_cols is not None and col_count < min_cols:
            remove_by_mincols = True
            if verbose: print(f"[*] Block {start+1}-{end+1} mapped for exclusion (Insufficient Density: {col_count} < {min_cols})")

        col_entries = extract_column_matrix(lines, start, end)
        remove_by_and, examples = check_logical_and_constraints(col_entries, conditions)

        remove_by_col_has = False
        if remove_col_has_alts:
            if entries := col_entries.get(inspect_col):
                if any(verify_column_exclusion(raw, remove_col_has_alts) for (_, raw, _) in entries):
                    remove_by_col_has = True
                    if verbose: print(f"[*] Block {start+1}-{end+1} mapped by Target Column regex filter")

        remove_by_any_col_has = False
        if remove_any_col_has_alts:
            for entries in col_entries.values():
                if any(verify_column_exclusion(raw, remove_any_col_has_alts) for (_, raw, _) in entries):
                    remove_by_any_col_has = True
                    if verbose: print(f"[*] Block {start+1}-{end+1} mapped by Global Matrix regex filter")
                    break

        matched = remove_by_mincols or remove_by_and or remove_by_col_has or remove_by_any_col_has
        if invert: matched = not matched

        if matched:
            to_remove.append((start, end))
            removal_examples.append((start + 1, end + 1, examples))

    matched_blocks = len(to_remove)
    if matched_blocks == 0:
        return {"removed_count": 0, "removed_ranges": [], "message": "[-] No matrices matched the defined criteria."}

    merged = unify_deletion_ranges(to_remove)
    new_lines: List[str] = []
    range_idx = 0
    current_range = merged[range_idx] if merged else None

    for i, line in enumerate(lines):
        while current_range and i > current_range[1]:
            range_idx += 1
            current_range = merged[range_idx] if range_idx < len(merged) else None
        if current_range and current_range[0] <= i <= current_range[1]:
            continue
        new_lines.append(line)

    message = f"Would safely drop {matched_blocks} frames from {os.path.basename(path)} (Dry-Run mode)." if dry_run else f"[+] Successfully purged {matched_blocks} frames from {os.path.basename(path)}."
    if not dry_run: write_telemetry_inplace(path, new_lines)

    return {"removed_count": matched_blocks, "removed_ranges": removal_examples, "message": message, "merged_count": len(merged)}

def parse_args():
    p = argparse.ArgumentParser(description="Operational Telemetry Filtering Engine")
    p.add_argument("--file", "-f", default=DEFAULT_TARGET_FILE, help="Path to target log file")
    p.add_argument("--and", dest="and_cond", help="Logical AND validation matrix")
    p.add_argument("--min-cols", type=int, help="Enforce minimum column density threshold")
    p.add_argument("--remove-col-has", help="Regex/Literal exclusions for targeted inspect column")
    p.add_argument("--remove-any-col-has", help="Regex/Literal exclusions mapped against all columns")
    p.add_argument("--col", type=int, default=6, help="Target column integer for standard inspection (Default: 6)")
    p.add_argument("--invert", action="store_true", help="Invert validation boolean")
    p.add_argument("--dry-run", action="store_true", help="Calculate deletions without structural writes")
    p.add_argument("--quiet", action="store_true", help="Suppress block-level diagnostic reporting")
    p.add_argument("--verbose", action="store_true", help="Enable microsecond diagnostic output")
    return p.parse_args()

def main():
    args = parse_args()
    if not args.and_cond and args.min_cols is None and not args.remove_col_has and not args.remove_any_col_has:
        print("[-] Initialization Error: Pipeline requires minimum of 1 filter condition.", file=sys.stderr)
        sys.exit(2)

    if not os.path.isfile(args.file):
        print(f"[-] Access Exception: Targeted asset not located at {args.file}", file=sys.stderr)
        sys.exit(2)

    try:
        conditions = compile_logical_conditions(args.and_cond) if args.and_cond else []
        remove_col_has_alts = build_regex_alternatives(args.remove_col_has) if args.remove_col_has else []
        remove_any_col_has_alts = build_regex_alternatives(args.remove_any_col_has) if args.remove_any_col_has else []
    except ValueError as e:
        print(f"[-] Parsing Error: {e}", file=sys.stderr)
        sys.exit(2)

    print("=== Telemetry Filtering Engine ===")
    print(f"[*] Target Asset  : {args.file}")
    print(f"[*] Logics (AND)  : {args.and_cond if args.and_cond else 'Disabled'}")
    print(f"[*] Density Floor : {args.min_cols if args.min_cols is not None else 'Disabled'}")
    print(f"[*] Execution Mode: {'Read-Only (Dry Run)' if args.dry_run else 'Destructive Write'}")
    print("==================================\n")

    result = execute_pipeline_filtering(args.file, conditions, min_cols=args.min_cols,
                                        dry_run=args.dry_run, verbose=args.verbose, invert=args.invert,
                                        remove_col_has_alts=remove_col_has_alts,
                                        remove_any_col_has_alts=remove_any_col_has_alts,
                                        inspect_col=args.col)

    print(f"\n{result['message']}")
    if result["removed_count"] and not args.quiet:
        print("[*] Exclusion Array Sample Logs:")
        for start_line, end_line, examples in result["removed_ranges"]:
            ex_str = ", ".join(str(x) for x in examples) if examples else "Header Matrix"
            print(f"    - Lines {start_line}-{end_line} | Trigger references: {ex_str}")

if __name__ == "__main__":
    main()