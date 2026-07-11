# WhatsApp-WAL-XRay: Deterministic-WAL-Parsing-Framework

**Independent Client-Side Vulnerability Research (Oct 2025 – Early Dec 2025)**

## 📑 Executive Summary
WAL-XRay is a custom memory-mapping and database forensic suite engineered to audit client-side data leakage in native Windows (UWP/WinUI) messaging environments. 

This research successfully reverse-engineered the platform’s proprietary local storage mechanics, demonstrating how server-side privacy controls (deleted messages, timeline of edited messages, view-once media, ephemeral statuses, and live reaction histories) could be bypassed by extracting "ghost data" directly from active SQLite Write-Ahead Logs (`.db-wal`).

*⚠️ **Responsible Disclosure Note:** This tool has been refactored into a command-line forensic framework. Hardcoded targets and keys have been removed to prevent weaponization. The vendor has since migrated to a WebView2 architecture, indirectly deprecating the native framework audited in this repository. The author assumes no liability and is not responsible for any unethical or unauthorized usage of this forensic toolset.*

---

## 🏗️ Systems Architecture & Core Engine (`/core-engine`)
Instead of relying on standard SQLite libraries, this framework was orchestrated from first principles using AI-assisted development to construct a low-level, deterministic binary parser[cite: 17]. 

* **`wal_forensic_parser.py`**: The primary targeted interception engine[cite: 17]. It utilizes Windows API shared handles to blindly ingest the `.db-wal` file from active RAM. It actively decrypts AES-OFB frames, parses variable integers (Varints) at the byte level, and extracts live telemetry into a structured database without triggering OS file-lock race conditions.

### Usage
The engine requires the user to supply their own target database and DP-API extracted AES-OFB key.
```bash
python wal_forensic_parser.py --wal "C:\path\to\messages.db-wal" --key "<64-character-hex-key>"

```

---

## 🔐 Data Privacy & PII Compliance (`/diagnostic-tools`)

A critical component of this forensic research was ensuring the safe handling of intercepted Personally Identifiable Information (PII) and the systematic sanitization of extracted databases.

* **`replace_global_pii.py`**: A cryptographic pseudonymizer deploying deterministic HMAC-SHA256 logic. It automatically identifies and redacts international phone numbers and non-regional identifiers to ensure zero PII is exposed during analysis.


* **`log_cleaner.py`**: A data sanitization pipeline designed to deduplicate transient database events and strip metadata noise. It generates cryptographic signatures for each structural frame to drop redundant telemetry blocks safely.


* **`remove_events.py`**: A modular telemetry filtering engine. It operates via CLI to execute logical AND/OR evaluations and RegEx pattern matching, systematically stripping background network noise, system header fragments, and automated handshakes from the working dataset.



---

## 🔬 Diagnostic Tooling (`/diagnostic-tools`)

Prior to building the core engine, the database architecture was blindly reverse-engineered using custom diagnostic scripts designed to probe, map, and classify unknown binary structures.

* **`wal_universal_mapper.py`**: A heavy-duty discovery scanner. It blindly maps any SQLite WAL file, iteratively guessing data types across all columns, and recursively decodes unknown Protobuf structures (wire types 0, 1, 2, 5) to generate a raw Schema Blueprint.


* **`wal_pattern_finder.py`**: A heuristic regex scanner and threat intelligence engine. It classifies unknown structural payloads into standardized parent-child relationship matrices to build actionable data maps.


* **`thumbnail_extract.py`**: A forensic binary carver. It is engineered to ingest raw hexadecimal strings extracted from Protobuf columns and reconstruct ephemeral media payloads (such as encrypted view-once thumbnails) into standard image files (low quality: like thumbnails).


* **`wal_check_header.py`**: A cryptographic state auditor. It verifies the active decryption state of the database by analyzing low-level header byte allocations and confirming the `0x0D` decrypted leaf table signature.


* **`wal_debug_cols.py`**: An endpoint routing telemetry scanner. It parses operational blocks to map, validate, and extract standard architectural network endpoints (JIDs, LIDs, and Broadcast channels).


* **`wal_inspect_col_ranges.py`**: A structural schema integrity auditor. It cross-references extracted data against baseline definitions to flag anomalous, corrupted, or nested data types residing in unexpected parameter columns.


* **`wal_io_latency_tester.py`**: A low-level system diagnostic framework. It monitors write-ahead log I/O latency to quantify the disparity between OS-reported virtual cache limits and the true physical byte stream.



---

## 📂 Proof of Work & Schemas (`/schemas-and-logs`)

To maintain strict ethical boundaries, no raw `.db` or `.wal` files are included in this repository. Instead, comprehensive architectural documentation and sanitized analytical logs are provided.

* **`WhatsApp-DBs_Architectural_Schema.md`**: The master reverse-engineered state mapping of the proprietary application's database schema.


* **`Vulnerability_Mapping_Scenarios.md`**: Architectural threat models and behavioral case studies. This document maps front-end user interface actions (e.g., edits, view-once, reactions) to their corresponding low-level SQLite row generation mechanics.


* **`WhatsApp_States_Types.md`**: A reference index mapping the proprietary integer codes extracted from local database columns to their operational states (e.g., mapping `1027` to Message Edit or `1046` to Ephemeral Media).


* **`WAL_Sanitization_Pipeline.md`**: The strict sequential execution pipeline deployed via the `remove_events.py` engine. It documents the step-by-step CLI deployment required to filter raw logs into clean analytical assets.


* **`WA-WAL_Telemetry_State_Ledger.md`**: The generated threat intelligence output from the heuristic ledger scanner (`wal_pattern_finder.py`), detailing structural payloads and sub-classifications.


* **`Undeniable_Output_of_Working_WAL_Parser.md`**: Sanitized proof-of-concept output demonstrating the core engine's ability to heuristically classify transient data events, extract JSON matrices, and isolate Media Key payloads in real-time.



---

## 🛡️ Vendor Mitigation Remarks

In early 2026, the vendor addressed these local data leakage issues by deprecating the native UWP framework entirely and shifting to a Chromium-based WebView2 wrapper.

While this transition successfully closed the `.db-wal` interception vector by migrating data handling to browser-based storage (IndexedDB), it bypassed the structural flaw rather than resolving the native SQLite implementation. This mitigation strategy resulted in a heavier, online-dependent application, sacrificing raw OS performance and degrading offline capabilities to maintain a unified codebase.
