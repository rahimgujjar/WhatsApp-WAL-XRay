---
layout: post
title: "Carving Ghosts: Reverse-Engineering WhatsApp WAL"
permalink: /Forensic-Research-Archive/
status: "Responsible Disclosure"
research_date: "Oct – Early Dec 2025"
date: 2026-07-11
enable_code_collapse: true
---

# Finding ␡ Messages & View-Once Media in WAL

> Security research rarely begins with a grand objective to dismantle a global platform's architecture. It usually starts with a simple, localized annoyance.

During my undergraduate studies in Information Technology, a university class representative sent a message to our group chat and immediately deleted it. When asked what the message contained, he flatly refused to tell me. Frustrated and angry, I decided to see if I could recover it myself. 

I noticed that the native Windows WhatsApp application (the older UWP version) stored files locally on my computer. After some research, I learned that WhatsApp keeps a local database, but it is heavily encrypted using **Windows DPAPI (Data Protection API)**.

## Bypassing the DPAPI Encryption Container

To bypass the encryption container, I found an open-source tool called ZAPiXDESK, developed by forensic researcher **Alberto Magno** (GitHub: [`kraftdenker`](https://github.com/kraftdenker/ZAPiXDESK/tree/main)). 
* Many thanks to Alberto for making this tool publicly available. 
* I used the tool's PowerShell script (`ZAPiXDESK.ps1`) and its closed-source executable strictly to extract my system's DPAPI key. 

Once I possessed the decryption key, I configured my own Python environment to handle the database analysis (later building my parser — [`wal_forensic_parser.py`](https://github.com/rahimgujjar/WhatsApp-WAL-XRay/blob/main/core-engine/wal_forensic_parser.py)).

## Inconsistencies in Primary Database Storage

I opened the decrypted `messages.db` file using DB Browser for SQLite and started digging. Luckily, I actually found the class representative's deleted message sitting as a remnant inside a Protobuf column. However, when I tried to repeat the process with other deleted messages, it failed. 

I realized that finding his message was just a fluke; WhatsApp's main database was inconsistent, and that specific message was just a leftover garbage value. Although, after some time, when I decrypted `messages.db` again, I realized that exact message became invisible. It looked like WhatsApp heals itself, or maybe it was just my *illusion*. 

**Realizing the main database was an unreliable forensic source, I shifted my focus to the physical storage layer: the SQLite Write-Ahead Log (`messages.db-wal`).**

***

## Volatile Transaction Persistence (The "Sync-and-Store" Flaw)

The WAL file is where SQLite temporarily stores transaction data before merging it into the main database. Because of how WhatsApp's asynchronous synchronization operated across devices, the server would deliver the actual encrypted message payload to my computer before it processed and delivered the subsequent "Delete" command.

This created a **Volatile Transaction Persistence** flaw. 
* The raw message data was actively written to the physical `.db-wal` file on the local disk. 
* The application's UI would hide the data, but the un-checkpointed memory frames remained completely intact in the log. 
* It simply meant that whenever a message came, I would catch or capture it at exactly that moment, leaving no place to run ✊.

> Since there was no existing tool capable of extracting this messy, transient data in real-time, I engineered a custom Python parser to actively memory-map and decode the SQLite Varints on the fly.

## Iterative Engineering & AI Assistance

I didn't accomplish this in a single attempt. I made many mistakes first. I spent time understanding the different data types, figuring out the schema, and experimenting with various approaches. Before writing the final parser, I built Several small utility scripts, some are given below:

- [`wal_pattern_finder.py`](https://github.com/rahimgujjar/WhatsApp-WAL-XRay/blob/main/diagnostic-tools/wal_pattern_finder.py): A heuristic engine to classify payloads.

- [`remove_events.py`](https://github.com/rahimgujjar/WhatsApp-WAL-XRay/blob/main/diagnostic-tools/remove_events.py): A filtering engine to strip background noise.

- [`WAL_Sanitization_Pipeline.md`](https://github.com/rahimgujjar/WhatsApp-WAL-XRay/blob/main/schemas-and-logs/WAL_Sanitization_Pipeline.md) & [`WA-WAL_Telemetry_State_Ledger.md`](https://github.com/rahimgujjar/WhatsApp-WAL-XRay/blob/main/schemas-and-logs/WA-WAL_Telemetry_State_Ledger.md): To map and document the behavioral matrices.

- [`WhatsApp_States_Types.md`](https://github.com/rahimgujjar/WhatsApp-WAL-XRay/blob/main/schemas-and-logs/WhatsApp_States_Types.md): To categorize status types (e.g., 1027 for edits, 1046 for View-Once).

- [`thumbnail_extract.py`](https://github.com/rahimgujjar/WhatsApp-WAL-XRay/blob/main/diagnostic-tools/thumbnail_extract.py): Extracts low-resolution View-Once thumbnails directly from the SQLite WAL.

And the Final Parser:

- [`wal_forensic_parser.py`](https://github.com/rahimgujjar/WhatsApp-WAL-XRay/blob/main/core-engine/wal_forensic_parser.py): The FINAL forensic parser developed during this research.

All of that troubleshooting and iterative work happened before the final script was created. The overall logic, research process, and architecture were my own; I only relied on AI to help write the syntax itself.

***

## What Could Be Recovered (The Forensic Timeline) 🔍

This method provided a **forensic-level timeline** that standard modified applications (such as GBWhatsApp) generally do not provide, even though they could theoretically implement similar capabilities. While modded APKs are powerful *(albeit unofficial and often in violation of WhatsApp's Terms of Service)* and can block delete requests based on user preferences, my parser **passively reconstructed complete historical states**:

- **Deleted Content:** Full recovery of deleted text messages, documents, audio, video, contact vCards, WhatsApp Business event details, and interactive polls. This excluded **deterministic tracking of poll selections**—identifying exactly who selected which option, the frequency of changes, or if a vote was removed. Although you can get the exact poll questions and it was theoretically possible, I did not find the exact parsing logic for it, but it is still possible.

- **Status Telemetry:** The ability to precisely track user interactions with status updates, such as identifying when a user viewed or reacted to a status and subsequently withdrew that reaction. It also allowed for the **covert viewing of statuses** and bypassing inserted advertisements without triggering read receipts server-side. While WhatsApp natively offers read-receipt toggles, this method remained entirely invisible to the application *(WhatsApp)* itself.

- **Message Edits:** Capturing the **original payload, the edited variations, and precise modification timestamps** across multiple sequential edits.

- **Reaction Histories:** Extracting a **millisecond-level timeline of user reactions**, capturing the exact moment a user added, removed, or rapidly replaced emoji reactions (effectively logging spam or inappropriate reaction behavior in groups or direct messages).

- **Limitations:** Full-resolution ephemeral media (View-Once disappearing messages) and audio payloads were not recoverable, as the **high-resolution files never populated within the local Windows client architecture**.

***

## The Ephemeral [View-Once] Logic Flaw ⚠️

While building the parser, I discovered a severe architectural logic flaw regarding ephemeral [View-Once messages] media. Obviously, I couldn't view a View-Once photo on the Windows app, as WhatsApp restricted that feature to mobile devices.

### The Cross-Device Routing Vulnerability

However, if I picked up my phone and simply quoted that unread View-Once message in a standard reply, my phone's local software would generate a low-quality thumbnail of the hidden image and attach it to the reply metadata. 

**The server—most likely acting as a blind router—would then blindly trust that reply packet (thumbnail included) and route it to my Windows desktop.** 
*(Note: I am 90% sure this only worked for unread messages. If I quoted it after it was already read, it likely wouldn't work depending on WhatsApp's memory management).*

### Data Extraction & Privacy Bypass

My parser, along with my [`thumbnail_extract.py`](https://github.com/rahimgujjar/WhatsApp-WAL-XRay/blob/main/diagnostic-tools/thumbnail_extract.py) script, successfully extracted these thumbnails directly from the desktop's WAL logs. As proven by my extracted JSON data, these were extremely low-quality images (ranging from 1.8 KB to 3.5 KB, with resolutions like 45×100 or 55×100). 

While text was illegible, facial recognition and context were easily identifiable. **Crucially, this logical flaw completely bypassed the intended privacy restriction without me ever actually opening the View-Once message at any point in my life😊.**

***

## Undeniable Proof

> **Forensic Verification & Reproducibility Notice⚠️⚠️:** The core parsing logic is fully open-source, allowing for rigorous methodological review over baseless speculation. While the raw `messages.db-wal` cannot be published due to strict Personal Identifiable Information (PII) constraints, and the target architecture is now deprecated, the forensic artifacts remain preserved. Serious researchers seeking to verify these claims beyond the repository code may contact me *(gmail: prime.logic05@gmail.com)* for a **controlled, authenticated demonstration** of the extraction process. 

To prove this wasn't fabricated, here is a sanitized excerpt from my [`Undeniable_Output_of_Working_WAL_Parser.md`](https://github.com/rahimgujjar/WhatsApp-WAL-XRay/blob/main/schemas-and-logs/Undeniable_Output_of_Working_WAL_Parser.md). Notice the raw Protocol Buffer structure, the exact timestamps, and the specific Meta CDN URL signatures (e.g., `oh=01_Q5...`) that authenticate media access:

```md
### [EVENT] Time: 16:56:03.525 | Page: 26584 | RowID: 6175
   Col 1: 120363183762064855@g.us
   Col 2: 0
   Col 3: AC76B81CCF99EE40AF2037FB8F46E06A
   Col 6: 18
   Col 7: 221672019906599@lid
   Col 9: <BLOB len=617>
   Col 11: 1764779560
   Col 13: https://mmg.whatsapp.net/v/t62.7161-24/563995364_865380376357302_5231409772810161712_n.enc?ccb=11-4&oh=01_Q5Aa3QHmc886cCWvSSkvTmru1Jxfs9sTo5PN7YChZBo_Qq66Hw&oe=698204E1&_nc_sid=5e03e0&mms3=true
   Col 15: video/mp4
   Col 16: 3
   Col 17: 768684
   Col 18: 24
   Col 21: <BLOB len=32>
   Col 22: 🧐🧐🧐
   Col 23: <BLOB len=32>
   Col 24: 0
   Col 25: 0
   Col 26: shared\transfers\2026_0\VID-20260105-WA0001.mp4
   Col 29: <BLOB len=54>
   Col 32: 1
   Col 34: 0
   Col 35: 0
   Col 36: 0
   Col 37: 0
   Col 38: <BLOB len=418>
   Col 39: <BLOB len=307>
   Col 41: 1764779560
   Col 42: WaTagMedia WaTagVideo video/mp4 Ue4368275059bf171eade5e21d6689997ffdddf52 Cddab0bf276f2d2e26cea6cddd6cf459210e97f95
   Col 43: 1
   Col 44: 1764779560
   Col 49: 0
   Col 50: 0
   Col 51: 😢👍
   Col 52: 2
### [EVENT] Time: 14:47:02.652 | Page: 26584 | RowID: 6175
   Col 1: 120363183762064855@g.us
   Col 2: 0
   Col 3: AC76B81CCF99EE40AF2037FB8F46E06A
   Col 6: 18
   Col 7: 221672019906599@lid
   Col 11: 1764779560
   Col 15: video/mp4
   Col 16: 1006
   Col 17: 0
   Col 18: 0
   Col 21: <BLOB len=32>
   Col 22: 0
   Col 23: <BLOB len=32>
   Col 24: 0
   Col 25: 0
   Col 29: <BLOB len=54>
   Col 32: 1
   Col 34: 0
   Col 35: 0
   Col 36: 0
   Col 37: 0
   Col 38: <BLOB len=418>
   Col 39: <BLOB len=307>
   Col 41: 1764779560
   Col 43: 0
   Col 44: 1764779560
   Col 49: 0
   Col 50: 0
   Col 51: 0
   Col 52: 0
### [EVENT] Time: 16:50:45.766 | Page: 26584 | RowID: 6175
   Col 1: 120363183762064855@g.us
   Col 2: 0
   Col 3: AC76B81CCF99EE40AF2037FB8F46E06A
   Col 6: 18
   Col 7: 221672019906599@lid
   Col 11: 1764779560
   Col 15: video/mp4
   Col 16: 1025
   Col 17: 0
   Col 18: 0
   Col 21: <BLOB len=32>
   And much more...
```
> To get more Understanding, check out this file on GitHub: [`Undeniable_Output_of_Working_WAL_Parser.md`](https://github.com/rahimgujjar/WhatsApp-WAL-XRay/blob/main/schemas-and-logs/Undeniable_Output_of_Working_WAL_Parser.md).

***

## The Threat Perspective: A Passive "Shadow Client"

What started as a trick to recover a single message evolved into a **sophisticated forensic data extraction framework**. I utilized my parser to engineer a **passive "shadow client"** running in the background. Because my script actively intercepted, decrypted, and filtered the raw SQLite I/O streams **directly from active RAM—bypassing OS file-lock race conditions**—it required **absolutely zero modifications or reverse-engineering** of the official WhatsApp binary.

This is a critical threat vector for post-exploitation data gathering. Unlike third-party modded applications ***(such as GB WhatsApp or Plus WhatsApp)*** that alter application code and carry a severe risk of account bans, this approach was completely passive. **While it underperforms modded clients in recovering View-Once media** (achieving only a ~40% success rate focused on thumbnails rather than full audio/video), **it completely excels in operational security**. It is **highly stealthy, generating zero network footprint**, and allowed for the covert exfiltration of disappearing data and deleted timelines with **virtually zero risk of an account ban**.

***

## Responsible Publication & Final Thoughts

**This research was driven entirely by technical curiosity, with absolutely no malicious intent or commercial motivation.** By the time I finalized this framework in early 2026, WhatsApp had already begun migrating away from the native UWP client to a **newer WebView2 architecture**.

> While I could have published these findings immediately since the target application was effectively obsolete, I deliberately chose to **delay the release**. I wanted to ensure that no malicious actor could weaponize the methodology during the transition period. 

Furthermore, my focus at the time was purely on private research; I only recently established a public GitHub presence to begin documenting my work for the broader community. It is important to note that this project was **completely independent**—I was never paid, rewarded, or otherwise compensated for this research.

**The potential for misuse was undeniably significant.** If weaponized into a fully deployed tool with a dedicated user interface, this passive interception framework would have been **incredibly difficult to detect**, offering a deeper, more invasive timeline than conventional forensic approaches **without any risk of an account ban**. That inherent danger is exactly why adhering to responsible publication principles was paramount.

Today, the specific implementation detailed here is no longer viable against current WhatsApp desktop clients. However, the true value of this research never lay in the code itself. 
* Once the relevant data is accessible, writing the script is comparatively straightforward. 
* **The real challenge—and the fundamental vulnerability exposed here—was the methodology** required to extract, map, and comprehend that volatile data in the first place.

***

## References

**Due to the highly specific niche of this research, no direct academic or technical references existed detailing data extraction from the SQLite WAL artifacts specifically for the native Windows WhatsApp UWP client (as of my research🙏). Consequently, this entire forensic methodology was developed from scratch. The similar and related references that were found are provided below, serving as peripheral context rather than direct guides:**

* [WhatsApp Desktop and Web Live Forensics (Alberto Magno)](https://medium.com/@alberto.magno/whatsapp-desktop-and-web-live-forensics-4n6-233f640e9fb3)
* [Python: Opening a file without creating a lock (StackOverflow)](https://stackoverflow.com/questions/14388608/python-opening-a-file-without-creating-a-lock)
* [bring2lite: Structural Concept & Tool for Forensic Data Analysis & Recovery of ␡ SQLite Records](https://doi.org/10.1016/j.diin.2019.04.017)
* [Making the Invisible Visible – Techniques for Recovering Deleted SQLite Data Records](https://www.semanticscholar.org/paper/Making-the-Invisible-Visible-%E2%80%93-Techniques-for-Pawlaszczyk-Hummert/c584a7ab6c7870f7cfb7cd2b2d6b38c2f1f41d31)
