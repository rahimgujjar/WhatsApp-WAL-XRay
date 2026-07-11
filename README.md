# WhatsApp-WAL-XRay: Deterministic-WAL-Parsing-Framework

**Independent Client-Side Vulnerability Research (Oct 2025 – Early Dec 2025)**

## 📑 Executive Summary
WAL-XRay is a custom memory-mapping and database forensic suite engineered to audit client-side data leakage in native Windows (UWP/WinUI) messaging environments. 

This research successfully reverse-engineered the platform’s proprietary local storage mechanics, demonstrating how server-side privacy controls (deleted messages, view-once media, ephemeral statuses, and live reaction histories) could be bypassed by extracting "ghost data" directly from active SQLite Write-Ahead Logs (`.db-wal`).

*⚠️ **Responsible Disclosure Note:** This tool has been refactored into a command-line forensic framework. Hardcoded targets and keys have been removed to prevent weaponization. The vendor has since migrated to a WebView2 architecture, indirectly deprecating the native framework audited in this repository. The author assumes no liability and is not responsible for any unethical or unauthorized usage of this forensic toolset.*

---

## 🏗️ Systems Architecture & Core Engine (`/core-engine`)
Instead of relying on standard SQLite libraries, this framework was orchestrated from first principles using AI-assisted development to construct a low-level, deterministic binary parser. 

**Technical Capabilities:**
* **Blind Memory Ingestion:** Utilizes Windows API shared handles to blindly read the `.db-wal` file directly from active RAM, avoiding file-lock race conditions.
* **Byte-Level Structural Parsing:** Iterates through raw SQLite frames, manually parsing variable integers (Varints) and mapping proprietary serial types without standard database queries.
* **Heuristic Media Mapping:** Integrates custom type dictionaries to identify and extract specific internal states (e.g., mapping `1046` to view-once media, identifying Protobuf media keys).
* **Integrity Validation:** Actively calculates `zlib.crc32` checksums against frame headers to differentiate live transaction data from dead disk sectors.

### Usage
The engine requires the user to supply their own target database and DP-API extracted AES-OFB key.
```bash
python wal_forensic_parser.py --wal "C:\path\to\messages.db-wal" --key "<64-character-hex-key>"
```
---

## 🔐 Data Privacy & PII Compliance (`/core-engine`)
A critical component of this forensic research was ensuring the safe handling of intercepted Personally Identifiable Information (PII) during the telemetry phase. 

* **Cryptographic Pseudonymization (`replace_92_and_more.py`):** Engineered a deterministic HMAC-SHA256 pseudonymizer to automatically identify and redact regional (+92) phone numbers, as well as non-regional identifiers, from the data stream to ensure zero PII is ever revealed.
* **Data Sanitization (`log_cleaner.py`):** Established a pipeline that deduplicated transient database events while preserving the heuristic metadata for structural analysis, ensuring zero sensitive user data was exposed during compilation.

---

## 🔬 Diagnostic Tooling (`/diagnostic-tools`)
Prior to building the core engine, the database architecture was reverse-engineered using custom diagnostic scripts:
* **`wal_universal_mapper.py`:** A heavy-duty scanner that blindly maps any SQLite WAL file, guessing data types and recursively decoding Protobuf structures to generate a raw Schema Blueprint.
* **`pattern_finder.py`:** A heuristic regex scanner built to classify unknown binary blobs into human-readable definitions.

---

## 📂 Proof of Work (`/schemas-and-logs`)
To maintain strict ethical boundaries, no raw `.db` or `.wal` files are included in this repository. Instead, sanitized forensic outputs are provided as proof of architectural mapping:
* **`WhatsApp-DB_Architectural_Schema.md`:** The reverse-engineered state mapping of the proprietary application.
* **`Undeniable_Output_of_Working_WAL_Parser.txt`:** Example output proving the engine's ability to heuristically classify transient data events and extract JSON/Media Key payloads in real-time.

---

## 🛡️ Vendor Mitigation Remarks
In early 2026, the vendor addressed these local data leakage issues by deprecating the native UWP framework entirely and shifting to a Chromium-based WebView2 wrapper. 

While this transition successfully closed the `.db-wal` interception vector by migrating data handling to browser-based storage (IndexedDB), it bypassed the structural flaw rather than resolving the native SQLite implementation. This mitigation strategy resulted in a heavier, online-dependent application, sacrificing raw OS performance and degrading offline capabilities to maintain a unified codebase.
