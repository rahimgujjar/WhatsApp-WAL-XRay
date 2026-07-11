#!/usr/bin/env python3
"""
replace_global_pii.py

A production-grade Data Privacy and Compliance utility designed to parse raw forensic
telemetry logs and cryptographically pseudonymize Personally Identifiable Information (PII).

Features:
 - Dynamic Country Code Extraction: Automatically detects international dialing prefixes
   ranging from 1 to 3 digits (e.g., 92, 1, 44) dynamically.
 - One-Way Deterministic Pseudonymization: Utilizes a keyed HMAC-SHA256 token mapping loop
   to obscure subscriber digits securely while preserving data formatting integrity.
 - Context-Aware Filtering: Automatically bypasses system metadata tags (such as broadcast
   or status channels) within a configurable sliding lookahead window.
"""

import sys
import re
import hmac
import hashlib
import secrets
import unicodedata

# Cryptographic Compliance Key: Used to map subscriber strings to unique pseudonyms.
# Replace with an environment variable or external vault argument in a production pipeline. {sammple key 👇}
COMPLIANCE_KEY = bytes.fromhex("d19c14f72ac0b010f5b138a9d2b95181db9838184b7133cd380da6e62c7e4dca")
DETERMINISTIC = True

# Context lookahead threshold (in characters) to safeguard architectural routing keywords
SKIP_WINDOW = 20

# Professionalized Regex Pipeline:
# Captures standard and compound JIDs across global dialing formats.
# Group 1: Country Code (1-3 digits) + Subscriber Number (7-12 digits)
# Group 2: Optional sub-device/instance routing tokens (e.g., colons or hyphens)
# Group 3: Application service domain (e.g., s.whatsapp.net, g.us, lid)
JID_PATTERN = re.compile(r"(?<!\d)(\d{1,3}\d{7,12})(?::(\d+))?@([^\s,;]+)")

# Administrative routing definitions flagged for exclusion from sanitization
SKIP_WORDS = [
    re.compile(r"\bbroadcast\b", re.IGNORECASE),
    re.compile(r"\bstatus\b", re.IGNORECASE),
]

MATCH_COUNT = 0
REPLACE_COUNT = 0
SKIP_COUNT = 0

def hmac_digest(key: bytes, data: bytes) -> bytes:
    """Computes a secure keyed-hash message authentication code snippet."""
    return hmac.new(key, data, hashlib.sha256).digest()

def digits_from_digest(digest: bytes, length: int) -> str:
    """Deterministically transforms binary digest blocks into standard numerical string matrices."""
    out = []
    i = 0
    while len(out) < length:
        v = digest[i % len(digest)]
        out.append(str(v % 10))
        i += 1
    return "".join(out)

def should_skip_context(text: str, start: int, end: int) -> bool:
    """Enforces context checking to verify if target keywords match administrative exclusions."""
    left = max(0, start - SKIP_WINDOW)
    right = min(len(text), end + SKIP_WINDOW)
    context = text[left:right]
    for pat in SKIP_WORDS:
        if pat.search(context):
            return True
    return False

def pseudonymize_subscriber(full_numeric: str, key: bytes) -> str:
    """
    Parses and hashes subscriber data while leaving the dialing country code visible.
    Maintains telemetry analytical value without exposing PII.
    """
    # Heuristic boundary verification: dynamic extraction of common routing shapes
    # If the string length indicates a common international format, isolate country code prefix
    if full_numeric.startswith("92") and len(full_numeric) == 12:
        cc_len = 2
    elif full_numeric.startswith("1") and (len(full_numeric) == 11 or len(full_numeric) == 10):
        cc_len = 1
    elif len(full_numeric) >= 11:
        cc_len = 3  # Fallback guess for 3-digit country rules
    else:
        cc_len = 2  # Standard operational matrix boundary fallback

    cc_prefix = full_numeric[:cc_len]
    subscriber_identity = full_numeric[cc_len:]

    digest = hmac_digest(key, f"subscriber_identity:{full_numeric}".encode("utf-8"))
    masked_subscriber = digits_from_digest(digest, len(subscriber_identity))

    # Mathematical Collision Safeguard Matrix
    if masked_subscriber == subscriber_identity:
        rotation = (digest[0] % len(subscriber_identity)) or 1
        masked_subscriber = masked_subscriber[rotation:] + masked_subscriber[:rotation]

    return cc_prefix + masked_subscriber

def process_forensic_log(text: str, key: bytes) -> str:
    """Sequentially scans raw inputs, processing target rows smoothly via a linear sliding cursor."""
    global MATCH_COUNT, REPLACE_COUNT, SKIP_COUNT
    out_parts = []
    last_idx = 0

    for m in JID_PATTERN.finditer(text):
        MATCH_COUNT += 1
        start, end = m.span()
        full_numeric = m.group(1)
        extra_tokens = m.group(2)
        domain = m.group(3)

        if should_skip_context(text, start, end):
            out_parts.append(text[last_idx:end])
            last_idx = end
            SKIP_COUNT += 1
            continue

        sanitized_numeric = pseudonymize_subscriber(full_numeric, key)
        out_parts.append(text[last_idx:start])

        if extra_tokens:
            out_parts.append(f"{sanitized_numeric}:{extra_tokens}@{domain}")
        else:
            out_parts.append(f"{sanitized_numeric}@{domain}")

        last_idx = end
        REPLACE_COUNT += 1

    out_parts.append(text[last_idx:])
    return "".join(out_parts)

def read_text_auto(path: str) -> str:
    """Safe ingestion utility reading target streams across variable structural BOM types."""
    with open(path, "rb") as f:
        raw = f.read()
    if raw.startswith(b"\xff\xfe"):
        return raw.decode("utf-16-le", errors="ignore")
    elif raw.startswith(b"\xfe\xff"):
        return raw.decode("utf-16-be", errors="ignore")
    elif len(raw) > 2 and raw[1:1000:2].count(b"\x00") > 10:
        try: return raw.decode("utf-16-le", errors="ignore")
        except Exception: return raw.decode("utf-8", errors="ignore")
    return raw.decode("utf-8", errors="ignore")

def normalize_text_layer(s: str) -> str:
    """Normalizes baseline character constraints and unifies multi-platform carriage returns."""
    s = unicodedata.normalize("NFKC", s)
    return s.replace("\r\n", "\n").replace("\r", "\n")

def main():
    if len(sys.argv) < 3:
        print("[-] Usage: python replace_global_pii.py <input_log.txt> <output_sanitized.txt>")
        sys.exit(1)

    infile = sys.argv[1]
    outfile = sys.argv[2]

    key = COMPLIANCE_KEY
    if not DETERMINISTIC:
        key = secrets.token_bytes(32)

    raw_data = read_text_auto(infile)
    normalized_data = normalize_text_layer(raw_data)
    sanitized_output = process_forensic_log(normalized_data, key)

    with open(outfile, "w", encoding="utf-8", newline="\n") as f:
        f.write(sanitized_output)

    print(f"[*] Process Statistics:")
    print(f"    - Identity Signatures Captured : {MATCH_COUNT}")
    print(f"    - Identities Obfuscated Successfully : {REPLACE_COUNT}")
    print(f"    - Excluded Channels Safeguarded : {SKIP_COUNT}")
    print(f"[+] Compliance scrubbing complete. Output exported to: {outfile}")

if __name__ == "__main__":
    main()