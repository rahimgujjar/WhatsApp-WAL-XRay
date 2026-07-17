---
layout: post
title: "Carving Ghosts: Reverse-Engineering WhatsApp WAL"
permalink: /Forensic-Research-Archive/
---

# Reverse-Engineering WhatsApp’s Windows Client: Finding Deleted Messages and View-Once Media in the Write-Ahead Log

Security research rarely begins with a grand objective to dismantle a global platform's architecture. It usually starts with a simple, localized annoyance.

During my undergraduate studies in Information Technology, a university class representative sent a message to our group chat and immediately deleted it. When asked what the message contained, he flatly refused to tell me. Frustrated and angry, I decided to see if I could recover it myself. I noticed that the native Windows WhatsApp application (the older UWP version) stored files locally on my computer. After some research, I learned that WhatsApp keeps a local database, but it is heavily encrypted using Windows DPAPI (Data Protection API).

To bypass the encryption container, I found an open-source tool called ZAPiXDESK, developed by forensic researcher **Alberto Magno** (GitHub: [`kraftdenker`](https://github.com/kraftdenker/ZAPiXDESK/tree/main)). Many thanks to Alberto for making this tool publicly available. I used the tool's PowerShell script (`ZAPiXDESK.ps1`) and its closed-source executable strictly to extract my system's DPAPI key. Once I possessed the decryption key, I configured my own Python environment to handle the database analysis (later building my parser — [`wal_forensic_parser.py`](https://github.com/rahimgujjar/WhatsApp-WAL-XRay/blob/main/core-engine/wal_forensic_parser.py)).

I opened the decrypted `messages.db` file using DB Browser for SQLite and started digging. Luckily, I actually found the class representative's deleted message sitting as a remnant inside a Protobuf column. However, when I tried to repeat the process with other deleted messages, it failed. I realized that finding his message was just a fluke; WhatsApp's main database was inconsistent, and that specific message was just a leftover garbage value. Although, after some time, when I decrypted `messages.db` again, I realized that exact message became invisible. It looked like WhatsApp heals itself, or maybe it was just my *illusion*. Realizing the main database was an unreliable forensic source, I shifted my focus to the physical storage layer: the SQLite Write-Ahead Log (`messages.db-wal`).

## Volatile Transaction Persistence (The "Sync-and-Store" Flaw)

The WAL file is where SQLite temporarily stores transaction data before merging it into the main database. Because of how WhatsApp's asynchronous synchronization operated across devices, the server would deliver the actual encrypted message payload to my computer before it processed and delivered the subsequent "Delete" command.

This created a Volatile Transaction Persistence flaw. The raw message data was actively written to the physical `.db-wal` file on the local disk. The application's UI would hide the data, but the un-checkpointed memory frames remained completely intact in the log. It simply meant that whenever a message came, I would catch or capture it at exactly that moment, leaving no place to run ✊.

Since there was no existing tool capable of extracting this messy, transient data in real-time, I engineered a custom Python parser to actively memory-map and decode the SQLite Varints on the fly.

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

## What Could Be Recovered (The Forensic Timeline)

This method provided a forensic-level timeline that standard modified applications (such as GBWhatsApp) generally do not provide, even though they could theoretically implement similar capabilities. While modded APKs are powerful (albeit unofficial and often in violation of WhatsApp's Terms of Service) and can block delete requests based on user preferences, my parser passively reconstructed complete historical states:

- **Deleted Content:** Full recovery of deleted text messages, documents, audio, video, contact vCards, WhatsApp Business event details, and interactive polls. This included deterministic confusion of poll selections—like exactly who selected which option, how many times it was changed, or removed.

- **Status Telemetry:** You could see exactly who liked your status and then unliked it again (like a friend who is no longer your friend, but still cares, or your ex-GF). It even allowed you to watch statuses and skip or view the ads WhatsApp inserted between them without WhatsApp ever knowing that you had viewed them. Although I later discovered that WhatsApp already provides users with a similar feature, this approach was still more effective because WhatsApp itself would never know that you had viewed them.

- **Message Edits:** Capturing the original text, the edited text, and the precise modification timestamps when the exact message was edited, re-edited, and edited again... onward.

- **Reaction Histories:** Extracting a millisecond-level timeline of user reactions (e.g., tracking the exact moment a user added an emoji, removed it, and replaced it). This helps you capture bullshitters spamming WhatsApp groups or your DMs by changing or doing vulgar reactions.

- **Limitations:** Full-resolution ephemeral [View-Once disappearing messages] media and audio payloads were not recoverable, as the full high-res files never reached the Windows client architecture.

## The Ephemeral [View-Once] Logic Flaw

While building the parser, I discovered a severe architectural logic flaw regarding ephemeral [View-Once messages] media. Obviously, I couldn't view a View-Once photo on the Windows app, as WhatsApp restricted that feature to mobile devices.

However, if I picked up my phone and simply quoted that unread View-Once message in a standard reply, my phone's local software would generate a low-quality thumbnail of the hidden image and attach it to the reply metadata. The server—most likely acting as a blind router—would then blindly trust that reply packet (thumbnail included) and route it to my Windows desktop. (Note: I am 90% sure this only worked for unread messages. If I quoted it after it was already read, it likely wouldn't work depending on WhatsApp's memory management).

My parser, along with my [`thumbnail_extract.py`](https://github.com/rahimgujjar/WhatsApp-WAL-XRay/blob/main/diagnostic-tools/thumbnail_extract.py) script, successfully extracted these thumbnails directly from the desktop's WAL logs. As proven by my extracted JSON data, these were extremely low-quality images (ranging from 1.8 KB to 3.5 KB, with resolutions like 45×100 or 55×100). While text was illegible, facial recognition and context were easily identifiable. Crucially, this logical flaw completely bypassed the intended privacy restriction without me ever actually opening the View-Once message at any point in my life 😏😁.

## Undeniable Proof

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
   And Much MORE ...
```

## The Threat Perspective (A Passive Shadow Client)

What started as a trick to recover a single message evolved into a highly capable Proof-of-Concept. I utilized my parser to engineer a passive "shadow client" running in the background. Because my script actively intercepted, decrypted, and filtered the raw SQLite I/O streams directly from the disk, it required absolutely zero modifications or reverse-engineering of the official WhatsApp binary.

This is a critical threat vector. Unlike modded applications that actively break code signatures and trigger anti-tamper bans, this approach was completely passive, undetectable (though I won't exaggerate, maybe WhatsApp could discover it), and allowed for the silent 🤫 harvesting of disappearing data and deleted timelines.

## Responsible Publication & Final Thoughts

I had no malicious intent with this research. I was never planning to turn this into a commercial tool or sell it. In fact, by the time I completed the research in early 2026, WhatsApp had already replaced the original Windows UWP client with a newer WebView-based client within three to four weeks.

Technically, I could have published the research soon after that because the original target no longer existed. However, I deliberately waited to ensure that no capable malicious actor could directly misuse my work. Additionally, at that time, I barely had any public online presence. I only created my GitHub profile relatively recently because I was previously busy with personal side projects and never really thought about documenting my work publicly. I never earned any money from this research, nor was I paid or rewarded for it.

Although this research certainly had the potential for malicious use—and such misuse could have been very serious if someone had turned it into a fully developed tool—that is precisely why responsible publication mattered. The techniques were difficult to detect and, in several areas, provided more detailed forensic insight than existing approaches.

While this particular implementation is no longer practical because the original client has changed, the underlying concept was never the difficult part. Once the relevant data is available, the remaining work becomes comparatively straightforward. The real challenge—and the real vulnerability—was extracting and understanding that data in the first place.
