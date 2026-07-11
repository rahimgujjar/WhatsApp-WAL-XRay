# Data Sanitization and Filtering Pipeline

This document defines the strict sequential CLI commands deployed via the `remove_events.py` engine to systematically sanitize raw forensic database logs.

## Phase 1: Structural Artifact & Metadata Purge

Clears unallocated system pointers and unparsed binary blocks.

### Purge system header noise and index elements
```
python remove_events.py --file data_source.txt --col 0 --quiet
```

### Drop unparsed physical storage fragments
```
python remove_events.py --file data_source.txt --col 1 --type "BINARY BLOB" --quiet
```
```
python remove_events.py --file data_source.txt --col 1 --type "BOOLEAN INT (0/1)" --quiet
```
```
python remove_events.py --file data_source.txt --and "Col5=TYPE: BINARY BLOB" --quiet
```

### Filter fragmented data frames lacking structural density (minimum 6 metrics)
```
python remove_events.py --file data_source.txt --min-cols 6 --quiet
```

## Phase 2: Administrative Control Filters

Strips systemic metadata mapped to internal devices and background sync loops.

### Filter access control metadata structures
```
python remove_events.py --file data_source.txt --and "Col1=TYPE: GROUP JID (@g.us)&Col2=TYPE: LID (@lid)&Col3=TYPE: BOOLEAN INT (0/1)&Col4=TYPE: BINARY BLOB" --quiet
```
```
python remove_events.py --file data_source.txt --and "Col1=TYPE: INTEGER (Raw Number)&Col2=TYPE: LID (@lid)&Col3=TYPE: INTEGER (Raw Number)&Col4=TYPE: BINARY BLOB" --quiet
```

### Drop internal loop tracking and automated instances
```
python remove_events.py --file data_source.txt --and "Col1=TYPE: LID (@lid)&Col51=TYPE: LID (@lid)" --quiet
```
```
python remove_events.py --file data_source.txt --and "Col1=TYPE: LID (@lid)&Col2=TYPE: COMPOUND LID (Phone:Instance@lid)" --quiet
```

### Purge standard symmetric handshake metrics
```
python remove_events.py --file data_source.txt --and "Col1=TYPE: USER JID (@s.whatsapp.net)&Col52=TYPE: USER JID (@s.whatsapp.net)" --quiet
```
```
python remove_events.py --file data_source.txt --and "Col3=TYPE: USER JID (@s.whatsapp.net)" --quiet
```
```
python remove_events.py --file data_source.txt --and "Col1=TYPE: USER JID (@s.whatsapp.net)" --quiet
```

## Phase 3: Media Payload Routing Exclusion

Bypasses active media transfers to optimize text-analysis threads.

### Optimize arrays by dropping redundant status identifiers and audio
```
python remove_events.py --file data_source.txt --and "Col16=7" --quiet
```
```
python remove_events.py --file data_source.txt --and "Col2=TYPE: BOOLEAN INT (0/1)&Col15=audio/ogg; codecs=opus" --quiet
```

### Isolate general multi-media transfers (Images, Videos, Word Docs)
```
python remove_events.py --file data_source.txt --and "Col2=TYPE: BOOLEAN INT (0/1)&Col15=image/jpeg" --quiet
```
```
python remove_events.py --file data_source.txt --and "Col2=TYPE: BOOLEAN INT (0/1)&Col15=video/mp4" --quiet
```
```
python remove_events.py --file data_source.txt --and "Col2=TYPE: BOOLEAN INT (0/1)&Col15=application/vnd.openxmlformats-officedocument.wordprocessingml.document" --quiet
```

## Phase 4: State Validation & Context Masking

Drops standard action-tracking lines by mapping specific baseline evaluation types.

### Filter active status states (Message modifications and deletions)
```
python remove_events.py --file data_source.txt --and "Col2=TYPE: BOOLEAN INT (0/1)&Col16=1027" --quiet
```
```
python remove_events.py --file data_source.txt --and "Col2=TYPE: BOOLEAN INT (0/1)&Col16=1006" --quiet
```

### Drop Broadcast and Standard Status Metrics
```
python remove_events.py --file data_source.txt --and "Col1=TYPE: BROADCAST STATUS (@broadcast)&Col2=TYPE: BOOLEAN INT (0/1)&Col7=TYPE: USER JID (@s.whatsapp.net)" --quiet
```

### Purge standard telemetry state codes
```
python remove_events.py --file data_source.txt --and "Col2=TYPE: BOOLEAN INT (0/1)&Col16=29" --quiet
```
```
python remove_events.py --file data_source.txt --and "Col16=29" --quiet
```
```
python remove_events.py --file data_source.txt --and "Col16=1" --quiet
```
```
python remove_events.py --file data_source.txt --and "Col16=1000" --quiet
```
```
python remove_events.py --file data_source.txt --and "Col16=1001" --quiet
```
```
python remove_events.py --file data_source.txt --and "Col16=1046" --quiet
```
```
python remove_events.py --file data_source.txt --and "Col16=1047" --quiet
```
```
python remove_events.py --file data_source.txt --and "Col16=19" --quiet
```

### Enforce Identity Mapping Constraints
```
python remove_events.py --file data_source.txt --and "Col11=TYPE: TIMESTAMP (Milliseconds)&Col11=TYPE: TIMESTAMP (Seconds)&Col11=TYPE: BOOLEAN INT (0/1)" --quiet
```
```
python remove_events.py --file data_source.txt --and "Col6=TYPE: LID (@lid)" --invert --quiet
```

## Phase 5: Deep Regex and Trace Masking

Final sweep targeting granular routing values mapped in anomalous locations.

### Enforce Targeted Identifier Group Scrubbing via standard REGEX matrices
```
python remove_events.py --file data_source.txt --remove-non-string-int --quiet
```
```
python remove_events.py --file data_source.txt --remove-col-has "@g.us|@s.whatsapp.net|@lid|248558649385029:8@lid|REGEX:\d+:\d+@lid" --col 6 --quiet
```
```
python remove_events.py --file data_source.txt --remove-any-col-has "REGEX:\d+:\d+@lid|REGEX:\d+:\d+@s\.whatsapp\.net|REGEX:\d+:\d+@g\.us" --quiet
```

### Drop residual generic texts, numerical records, and URL mappings
```
python remove_events.py --file data_source.txt --and "Col3=TYPE: COMPOUND LID (Phone:Instance@lid)" --quiet
```
```
python remove_events.py --file data_source.txt --and "Col1=TYPE: TEXT STRING" --quiet
```
```
python remove_events.py --file data_source.txt --and "Col8=TYPE: TEXT STRING&Col2=TYPE: BOOLEAN INT (0/1)&Col16=0" --quiet
```
```
python remove_events.py --file data_source.txt --and "Col8=TYPE: INTEGER (Raw Number)&Col2=TYPE: BOOLEAN INT (0/1)&Col16=0" --quiet
```
```
python remove_events.py --file data_source.txt --and "Col8=TYPE: URL / LINK&Col2=TYPE: BOOLEAN INT (0/1)&Col16=0" --quiet
```
```
python remove_events.py --file data_source.txt --and "Col8=TYPE: URL / LINK&Col2=TYPE: BOOLEAN INT (0/1)&Col16=9" --quiet
```