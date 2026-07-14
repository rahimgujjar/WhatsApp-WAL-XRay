# Raw Evidence & Parser Output [Proof-of-Work]

## DISCLAIMER:
This file contains synthetic, sanitized telemetry extracted via the WAL-XRay
forensic engine. While the architectural formatting, column allocations, and
payload structures represent exact 1:1 behavioral mappings of the native SQLite
Write-Ahead Log (Here Specifically, `WhatsApp`), Mostly sensitive data has been
mathematically altered or generated.

Personally Identifiable Information (PII), regional dialing codes, cryptographic
media keys, contact routing IDs, and embedded URLs are strictly dummy values
injected to preserve the realism of the forensic formatting without exposing
live user data. Expired or dead-end routing domains may be present for structural
accuracy.

## PURPOSE:
This export serves as undeniable proof-of-work, demonstrating the engine's ability
to blindly memory-map transient `.db-wal` frames, decode variable integers, and
extract nested Protobuf architectures in real-time before OS-level checkpoints occur.

***

### [EVENT] Time: 16:56:03.525 | Page: 26584 | RowID: 6175
```
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
```
### [EVENT] Time: 14:47:02.652 | Page: 26584 | RowID: 6175
```
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
```
### [EVENT] Time: 16:50:45.766 | Page: 26584 | RowID: 6175
```
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
```
### [EVENT] Time: 14:14:43.399 | Page: 30263 | RowID: 10175
```
   Col 1: 155834935959676@lid
   Col 2: 0
   Col 3: A548E3E079C8A4130C1BAB525C96D8C8
   Col 6: 8
   Col 11: 1764778192
   Col 15: video/mp4
   Col 16: 1006
   Col 17: 0
   Col 18: 0
   Col 21: <BLOB len=32>
   Col 23: <BLOB len=32>
   Col 24: 0
   Col 25: 0
   Col 32: 0
   Col 34: 0
   Col 35: 0
   Col 36: 0
   Col 37: 0
   Col 38: <BLOB len=371>
   Col 39: <BLOB len=310>
   Col 41: 1764778192
   Col 43: 0
   Col 44: 0
   Col 49: 0
   Col 50: 0
   Col 52: 0
   Col 54: 155834935959676@lid
```
### [EVENT] Time: 16:01:43.044 | Page: 30138 | RowID: 10182
```
   Col 1: 120363405979135311@g.us
   Col 2: 0
   Col 3: A53A27A824430FC28750C016D84DBC6C
   Col 6: 8
   Col 7: 155834935959676@lid
   Col 8: john
   Col 11: 1764774169
   Col 16: 0
   Col 17: 0
   Col 18: 0
   Col 24: 0
   Col 25: 0
   Col 32: 0
   Col 34: 0
   Col 35: 0
   Col 36: 0
   Col 37: 0
   Col 38: <BLOB len=71>
   Col 41: 1764774169
   Col 43: 0
   Col 44: 0
   Col 49: 0
   Col 50: 0
   Col 52: 0
```
### [EVENT] Time: 15:47:07.246 | Page: 30138 | RowID: 10181
```
   Col 1: 155834935959676@lid
   Col 2: 0
   Col 3: A5DCDE0D6F24F8550A398135F3BFF87B
   Col 6: 8
   Col 8: ali
   Col 11: 1764774097
   Col 16: 0
   Col 17: 0
   Col 18: 0
   Col 24: 0
   Col 25: 0
   Col 32: 0
   Col 34: 0
   Col 35: 0
   Col 36: 0
   Col 37: 0
   Col 38: <BLOB len=71>
   Col 41: 1764774097
   Col 43: 0
   Col 44: 0
   Col 49: 0
   Col 50: 0
   Col 52: 0
   Col 54: 155834935959676@lid
```
### [EVENT] Time: 15:47:38.734 | Page: 30138 | RowID: 10181
```
   Col 1: 155834935959676@lid
   Col 2: 0
   Col 3: A5DCDE0D6F24F8550A398135F3BFF87B
   Col 5: A5FDDEAA395EEC71B1D48A2FA202566B
   Col 6: 8
   Col 8: *zain*
   Col 11: 1764774097
   Col 16: 0
   Col 17: 0
   Col 18: 0
   Col 24: 0
   Col 25: 0
   Col 32: 0
   Col 34: 0
   Col 35: 0
   Col 36: 2
   Col 37: 0
   Col 38: <BLOB len=79>
   Col 41: 1764774097
   Col 43: 0
   Col 44: 0
   Col 49: 0
   Col 50: 0
   Col 52: 0
   Col 54: 155834935959676@lid
```
### [EVENT] Time: 15:16:23.981 | Page: 30138 | RowID: 10183
```
   Col 1: 155834935959676@lid
   Col 2: 0
   Col 3: A5FDDEAA395EEC71B1D48A2FA202566B
   Col 6: 8
   Col 8: *zain*
   Col 11: 1764774219
   Col 16: 1027
   Col 17: 0
   Col 18: 0
   Col 24: 0
   Col 25: 0
   Col 32: 0
   Col 34: 0
   Col 35: 0
   Col 36: 0
   Col 37: 0
   Col 38: <BLOB len=42>
   Col 41: 1764774219
   Col 43: 0
   Col 44: 0
   Col 52: 0
   Col 54: 155834935959676@lid
```
### [EVENT] Time: 15:49:17.863 | Page: 30094 | RowID: 9698
```
   Col 1: 155834935959676@lid
   Col 2: 0
   Col 3: A58D41F7B713226A70D766FAE1D770B4
   Col 5: A535B2394CADFB8F9CF1D3B4F91386B8
   Col 6: 8
   Col 11: 1764779763
   Col 16: 1006
   Col 17: 0
   Col 18: 0
   Col 24: 0
   Col 25: 0
   Col 32: 0
   Col 34: 0
   Col 35: 0
   Col 36: 0
   Col 37: 0
   Col 38: <BLOB len=209>
   Col 41: 1764779763
   Col 43: 0
   Col 44: 0
   Col 49: 0
   Col 50: 0
   Col 52: 0
   Col 54: 155834935959676@lid
```
### [EVENT] Time: 16:49:19.378 | Page: 30138 | RowID: 10181
```
   Col 1: 155834935959676@lid
   Col 2: 0
   Col 3: A5DCDE0D6F24F8550A398135F3BFF87B
   Col 5: A5FDDEAA395EEC71B1D48A2FA202566B
   Col 6: 8
   Col 11: 1764774097
   Col 16: 1006
   Col 17: 0
   Col 18: 0
   Col 24: 0
   Col 25: 0
   Col 32: 0
   Col 34: 0
   Col 35: 0
   Col 36: 0
   Col 37: 0
   Col 38: <BLOB len=125>
   Col 41: 1764774097
   Col 43: 0
   Col 44: 0
   Col 49: 0
   Col 50: 0
   Col 52: 0
   Col 54: 155834935959676@lid
```
### [EVENT] Time: 16:57:58.160 | Page: 30138 | RowID: 10182
```
   Col 1: 120363405979135311@g.us
   Col 2: 0
   Col 3: A53A27A824430FC28750C016D84DBC6C
   Col 5: A5F438E0C1567BF8F506D27EA64E096C
   Col 6: 8
   Col 7: 155834935959676@lid
   Col 8: Zubair
   Col 11: 1764774169
   Col 16: 0
   Col 17: 0
   Col 18: 0
   Col 24: 0
   Col 25: 0
   Col 32: 0
   Col 34: 0
   Col 35: 0
   Col 36: 2
   Col 37: 0
   Col 38: <BLOB len=79>
   Col 41: 1764774169
   Col 43: 0
   Col 44: 0
   Col 49: 0
   Col 50: 0
   Col 52: 0
```
### [EVENT] Time: 16:49:30.958 | Page: 30138 | RowID: 10182
```
   Col 1: 120363405979135311@g.us
   Col 2: 0
   Col 3: A53A27A824430FC28750C016D84DBC6C
   Col 5: A5F438E0C1567BF8F506D27EA64E096C
   Col 6: 8
   Col 7: 155834935959676@lid
   Col 8: Zubair
   Col 11: 1764774169
   Col 16: 0
   Col 17: 0
   Col 18: 0
   Col 24: 0
   Col 25: 0
   Col 32: 0
   Col 34: 0
   Col 35: 0
   Col 36: 2
   Col 37: 0
   Col 38: <BLOB len=79>
   Col 41: 1764774169
   Col 43: 0
   Col 44: 0
   Col 49: 0
   Col 50: 0
   Col 52: 0
```
### [EVENT] Time: 16:59:28.637 | Page: 30138 | RowID: 10182
```
   Col 1: 120363405979135311@g.us
   Col 2: 0
   Col 3: A53A27A824430FC28750C016D84DBC6C
   Col 5: A5F438E0C1567BF8F506D27EA64E096C
   Col 6: 8
   Col 7: 155834935959676@lid
   Col 11: 1764774169
   Col 16: 1025
   Col 17: 0
   Col 18: 0
   Col 24: 0
   Col 25: 0
   Col 32: 0
   Col 34: 0
   Col 35: 0
   Col 36: 0
   Col 37: 0
   Col 38: <BLOB len=145>
   Col 41: 1764774169
   Col 43: 0
   Col 44: 0
   Col 49: 0
   Col 50: 0
   Col 52: 0
```
### [EVENT] Time: 16:34:58.788 | Page: 30138 | RowID: 10182
```
   Col 1: 120363405979135311@g.us
   Col 2: 0
   Col 3: A53A27A824430FC28750C016D84DBC6C
   Col 5: A5F438E0C1567BF8F506D27EA64E096C
   Col 6: 8
   Col 7: 155834935959676@lid
   Col 11: 1764774169
   Col 16: 1006
   Col 17: 0
   Col 18: 0
   Col 24: 0
   Col 25: 0
   Col 32: 0
   Col 34: 0
   Col 35: 0
   Col 36: 0
   Col 37: 0
   Col 38: <BLOB len=145>
   Col 41: 1764774169
   Col 43: 0
   Col 44: 0
   Col 49: 0
   Col 50: 0
   Col 52: 0
```
### [EVENT] Time: 14:47:13.758 | Page: 30263 | RowID: 10176
```
   Col 1: 155834935959676@lid
   Col 2: 0
   Col 3: A53B7F9D76805EAED4CFFF0E79686311
   Col 6: 8
   Col 11: 1764778236
   Col 13: https://mmg.whatsapp.net/v/t62.7117-24/562013024_897006192713959_7655019266773048502_n.enc?ccb=11-4&oh=01_Q5Aa3gEg9UDk4IPKMhFGPVj5vs31GcacOtDyEIxu292KkPSO-Q&oe=698A37A1&_nc_sid=5e03e0&mms3=true
   Col 15: audio/ogg; codecs=opus
   Col 16: 2
   Col 17: 38829
   Col 18: 17
   Col 19: live
   Col 21: <BLOB len=32>
   Col 23: <BLOB len=32>
   Col 24: 0
   Col 25: 0
   Col 32: 0
   Col 34: 0
   Col 35: 0
   Col 36: 0
   Col 37: 0
   Col 38: <BLOB len=346>
   Col 41: 1764778236
   Col 43: 0
   Col 44: 0
   Col 49: 0
   Col 50: 0
   Col 52: 0
   Col 54: 155834935959676@lid
```
### [EVENT] Time: 16:52:12.191 | Page: 30263 | RowID: 10176
```
   Col 1: 155834935959676@lid
   Col 2: 0
   Col 3: A53B7F9D76805EAED4CFFF0E79686311
   Col 6: 8
   Col 11: 1764778236
   Col 15: audio/ogg; codecs=opus
   Col 16: 1006
   Col 17: 0
   Col 18: 0
   Col 19: live
   Col 21: <BLOB len=32>
   Col 23: <BLOB len=32>
   Col 24: 0
   Col 25: 0
   Col 32: 0
   Col 34: 0
   Col 35: 0
   Col 36: 0
   Col 37: 0
   Col 38: <BLOB len=380>
   Col 41: 1764778236
   Col 43: 0
   Col 44: 0
   Col 49: 0
   Col 50: 0
   Col 52: 0
   Col 54: 155834935959676@lid
```
### [EVENT] Time: 15:20:06.751 | Page: 29724 | RowID: 8936
```
   Col 1: 120363400531513549@g.us
   Col 2: 0
   Col 3: AC3F364AB801AD7BC76F1D985EE7A1E4
   Col 6: 18
   Col 7: 6919511101563@lid
   Col 11: 1764775362
   Col 13: https://mmg.whatsapp.net/v/t62.7117-24/612747609_1944935556419566_8470609040255130694_n.enc?ccb=11-4&oh=01_Q5Aa3gGkdEZvk4NCzcFkTmcUIHlTu_JpHTNg-HjDhDKluWca_w&oe=698704A6&_nc_sid=5e03e0&mms3=true
   Col 15: audio/ogg; codecs=opus
   Col 16: 2
   Col 17: 137625
   Col 18: 59
   Col 21: <BLOB len=32>
   Col 23: <BLOB len=32>
   Col 24: 0
   Col 25: 0
   Col 26: shared\transfers\2026_1\AUD-20260108-WA0001.opus
   Col 29: <BLOB len=6>
   Col 32: 1
   Col 34: 0
   Col 35: 0
   Col 36: 0
   Col 37: 0
   Col 38: <BLOB len=345>
   Col 39: <BLOB len=378>
   Col 41: 1764775362
   Col 42: WaTagMedia WaTagAudio audio/ogg; codecs=opus U8d987b45901b4d1fc819385c49a74212dc000295 C454d259aec35096381b385e46bad6dca2c4fba86
   Col 43: 1
   Col 44: 0
   Col 49: 0
   Col 50: 0
   Col 52: 0
```
### [EVENT] Time: 15:34:40.007 | Page: 29724 | RowID: 8936
```
   Col 1: 120363400531513549@g.us
   Col 2: 0
   Col 3: AC3F364AB801AD7BC76F1D985EE7A1E4
   Col 6: 18
   Col 7: 6919511101563@lid
   Col 11: 1764775362
   Col 15: audio/ogg; codecs=opus
   Col 16: 1006
   Col 17: 0
   Col 18: 0
   Col 21: <BLOB len=32>
   Col 23: <BLOB len=32>
   Col 24: 0
   Col 25: 0
   Col 29: <BLOB len=6>
   Col 32: 1
   Col 34: 0
   Col 35: 0
   Col 36: 0
   Col 37: 0
   Col 38: <BLOB len=345>
   Col 39: <BLOB len=378>
   Col 41: 1764775362
   Col 42: WaTagMedia WaTagAudio audio/ogg; codecs=opus U8d987b45901b4d1fc819385c49a74212dc000295 C454d259aec35096381b385e46bad6dca2c4fba86
   Col 43: 1
   Col 44: 0
   Col 49: 0
   Col 50: 0
   Col 52: 0
```
### [EVENT] Time: 16:16:15.138 | Page: 29724 | RowID: 8936
```
   Col 1: 120363400531513549@g.us
   Col 2: 0
   Col 3: AC3F364AB801AD7BC76F1D985EE7A1E4
   Col 6: 18
   Col 7: 6919511101563@lid
   Col 11: 1764775362
   Col 15: audio/ogg; codecs=opus
   Col 16: 1025
   Col 17: 0
   Col 18: 0
   Col 21: <BLOB len=32>
   Col 23: <BLOB len=32>
   Col 24: 0
   Col 25: 0
   Col 29: <BLOB len=6>
   Col 32: 1
   Col 34: 0
   Col 35: 0
   Col 36: 0
   Col 37: 0
   Col 38: <BLOB len=345>
   Col 39: <BLOB len=378>
   Col 41: 1764775362
   Col 42: WaTagMedia WaTagAudio audio/ogg; codecs=opus U8d987b45901b4d1fc819385c49a74212dc000295 C454d259aec35096381b385e46bad6dca2c4fba86
   Col 43: 1
   Col 44: 0
   Col 49: 0
   Col 50: 0
   Col 52: 0
```
### [EVENT] Time: 14:43:36.687 | Page: 29848 | RowID: 10166
```
   Col 1: 280784057462786@lid
   Col 2: 0
   Col 3: ACBA8E3553D475FD91EEC0DCEEAA410B
   Col 6: 8
   Col 9: <BLOB len=495>
   Col 11: 1764775831
   Col 13: https://mmg.whatsapp.net/v/t62.7118-24/612765914_2127169768054786_143187812771273264_n.enc?ccb=11-4&oh=01_Q5Aa3gFcyFW39S5S-VRhs8NdyyJny7AHykEs14kfMhv1Dg46sg&oe=698A2D3B&_nc_sid=5e03e0&mms3=true
   Col 15: image/jpeg
   Col 16: 1
   Col 17: 46659
   Col 18: 0
   Col 21: <BLOB len=32>
   Col 23: <BLOB len=32>
   Col 24: 0
   Col 25: 0
   Col 26: shared\transfers\2026_1\IMG-20260111-WA0001.jpg
   Col 32: 1
   Col 34: 0
   Col 35: 0
   Col 36: 0
   Col 37: 0
   Col 38: <BLOB len=263>
   Col 39: <BLOB len=581>
   Col 41: 1764775831
   Col 42: WaTagMedia WaTagImage image/jpeg U475ac7981a85b7e7737b17383fa35bb69cfc3096 C475ac7981a85b7e7737b17383fa35bb69cfc3096
   Col 43: 0
   Col 44: 0
   Col 49: 0
   Col 50: 0
   Col 52: 0
   Col 54: 280784057462786@lid
```
### [EVENT] Time: 14:07:29.831 | Page: 29848 | RowID: 10166
```
   Col 1: 280784057462786@lid
   Col 2: 0
   Col 3: ACBA8E3553D475FD91EEC0DCEEAA410B
   Col 6: 8
   Col 11: 1764775831
   Col 15: image/jpeg
   Col 16: 1006
   Col 17: 0
   Col 18: 0
   Col 21: <BLOB len=32>
   Col 23: <BLOB len=32>
   Col 24: 0
   Col 25: 0
   Col 32: 0
   Col 34: 0
   Col 35: 0
   Col 36: 0
   Col 37: 0
   Col 38: <BLOB len=263>
   Col 39: <BLOB len=581>
   Col 41: 1764775831
   Col 43: 0
   Col 44: 0
   Col 49: 0
   Col 50: 0
   Col 52: 0
   Col 54: 280784057462786@lid
```
### [EVENT] Time: 15:25:29.643 | Page: 29260 | RowID: 6114
```
   Col 1: 10446
   Col 2: 239049558216809@lid
   Col 3: 1
   Col 4: ACC2FD2698DC28D36854FA2CE9D679AB
   Col 5: 239049558216809@lid
   Col 6: 0
   Col 7: AC153E0FCE5C0A8978E8B16588E5B2D1
   Col 10: 🆘
   Col 11: 1764776881182
```
### [EVENT] Time: 15:39:46.160 | Page: 29260 | RowID: 6110
```
   Col 1: 10446
   Col 2: 239049558216809@lid
   Col 3: 0
   Col 4: ACE522241A065570C0CE1FBA7E19D55E
   Col 5: 239049558216809@lid
   Col 6: 0
   Col 7: AC153E0FCE5C0A8978E8B16588E5B2D1
   Col 10: 😂
   Col 11: 1764776881182
```
### [EVENT] Time: 14:45:28.935 | Page: 29260 | RowID: 6111
```
   Col 1: 10448
   Col 2: 239049558216809@lid
   Col 3: 0
   Col 4: AC1EBD8E32A802A699E62D177D3E9422
   Col 5: 239049558216809@lid
   Col 6: 1
   Col 7: AC649549C1D37D27F6A70F7955642733
   Col 10: 😹
   Col 11: 1764776934957
```
### [EVENT] Time: 16:20:04.783 | Page: 29260 | RowID: 6112
```
   Col 1: 10449
   Col 2: 239049558216809@lid
   Col 3: 0
   Col 4: AC5C725E9FC658B1DCA9E0E236E1BBE0
   Col 5: 239049558216809@lid
   Col 6: 1
   Col 7: AC83EE2E13AFD600E015BC7B6777466F
   Col 10: 😹
   Col 11: 1764776927029
```
### [EVENT] Time: 14:30:05.342 | Page: 29260 | RowID: 6113
```
   Col 1: 10449
   Col 2: 239049558216809@lid
   Col 3: 1
   Col 4: ACA45F010A16D92EE03C7A136F01DC03
   Col 5: 239049558216809@lid
   Col 6: 1
   Col 7: AC83EE2E13AFD600E015BC7B6777466F
   Col 10: 💢
   Col 11: 1764776945115
```
### [EVENT] Time: 16:01:15.860 | Page: 30022 | RowID: 6025
```
   Col 1: 9618
   Col 2: 120363406995998132@g.us
   Col 3: 1
   Col 4: 3EB0F172FF9FD6B7632B98
   Col 5: 120363406995998132@g.us
   Col 6: 0
   Col 7: 3EB0F172FF9FD6B7632B98
   Col 9: 146428437495959@lid
   Col 10: 😁
   Col 11: 1764779624269
```
### [EVENT] Time: 14:01:13.132 | Page: 30022 | RowID: 6026
```
   Col 1: 9640
   Col 2: 120363406995998132@g.us
   Col 3: 0
   Col 4: AC293F632BF7D0D6DC65E8609501D40E
   Col 5: 120363406995998132@g.us
   Col 6: 0
   Col 7: 3EB074A752B50A3A93AD1B
   Col 8: 262341115510805@lid
   Col 9: 146428437495959@lid
   Col 10: 👍🏻
   Col 11: 1764772663242
```
### [EVENT] Time: 16:20:40.478 | Page: 30097 | RowID: 6033
```
   Col 1: 9655
   Col 2: 120363406995998132@g.us
   Col 3: 0
   Col 4: ACF6D5AB2628B5BA8BBFCAD954EE846E
   Col 5: 120363406995998132@g.us
   Col 6: 0
   Col 7: 3EB00067786BEBD5179434
   Col 8: 84640954085395@lid
   Col 9: 146428437495959@lid
   Col 10: 👍
   Col 11: 1764779157815
```
### [EVENT] Time: 16:47:15.910 | Page: 30097 | RowID: 6039
```
   Col 1: 9691
   Col 2: 120363393869517850@g.us
   Col 3: 0
   Col 4: AC2E047A6A2587469E5FE51A495C3319
   Col 5: 120363393869517850@g.us
   Col 6: 1
   Col 7: 3FDBE7202B1085527200
   Col 8: 154146426626124@lid
   Col 10: 🫡
   Col 11: 1764779591310
```
### [EVENT] Time: 14:19:24.557 | Page: 30097 | RowID: 6040
```
   Col 1: 9691
   Col 2: 120363393869517850@g.us
   Col 3: 1
   Col 4: 3F144503F859B9914D99
   Col 5: 120363393869517850@g.us
   Col 6: 1
   Col 7: 3FDBE7202B1085527200
   Col 10: 👍
   Col 11: 1764779601633
```
### [EVENT] Time: 16:28:51.460 | Page: 29640 | RowID: 6121
```
   Col 1: 10462
   Col 2: 244744936493106@lid
   Col 3: 1
   Col 4: ACC7E795A8DFB23CEDFB7EBCE8A52BA5
   Col 5: 244744936493106@lid
   Col 6: 1
   Col 7: AC9448B66C567728BD8D5EFA935CB4CB
   Col 10: 🦧
   Col 11: 1764779932124
```
### [EVENT] Time: 16:42:28.018 | Page: 29640 | RowID: 6119
```
   Col 1: 10462
   Col 2: 244744936493106@lid
   Col 3: 0
   Col 4: 3F618D01395002406668
   Col 5: 244744936493106@lid
   Col 6: 1
   Col 7: AC9448B66C567728BD8D5EFA935CB4CB
   Col 10: 🚌
   Col 11: 1764779941244
```
### [EVENT] Time: 15:36:13.903 | Page: 29640 | RowID: 6120
```
   Col 1: 10464
   Col 2: 244744936493106@lid
   Col 3: 1
   Col 4: AC102659D34DCA6750B2AE6AA7D06AA9
   Col 5: 244744936493106@lid
   Col 6: 0
   Col 7: 3F32FC0E97A217F289BD
   Col 10: 🛰️
   Col 11: 1764779907107
```
### [EVENT] Time: 14:46:01.596 | Page: 29640 | RowID: 6122
```
   Col 1: 10464
   Col 2: 244744936493106@lid
   Col 3: 0
   Col 4: 3FBA723969BBF13F9887
   Col 5: 244744936493106@lid
   Col 6: 0
   Col 7: 3F32FC0E97A217F289BD
   Col 10: 🔤
   Col 11: 1764779963602
```
### [EVENT] Time: 15:52:59.602 | Page: 29274 | RowID: 10527
```
   Col 1: status@broadcast
   Col 2: 0
   Col 3: A53A1970BF43B48B418E07B2EFDB096D
   Col 6: 8
   Col 7: 923489076556@s.whatsapp.net
   Col 9: <BLOB len=1569>
   Col 11: 1764775813
   Col 13: https://mmg.whatsapp.net/v/t62.7118-24/564756376_1574922720408612_1114545405262449158_n.enc?ccb=11-4&oh=01_Q5Aa3gGIuZKO103kOw8QOf-ZFZJvWKh1F_QYXrg-8PECH70Eng&oe=698C0DB2&_nc_sid=5e03e0&mms3=true
   Col 15: image/jpeg
   Col 16: 1
   Col 17: 26708
   Col 18: 0
   Col 21: <BLOB len=32>
   Col 23: <BLOB len=32>
   Col 24: 0
   Col 25: 0
   Col 32: 254
   Col 34: 0
   Col 35: 0
   Col 36: 0
   Col 37: 0
   Col 38: <BLOB len=285>
   Col 39: <BLOB len=536>
   Col 41: 1764775813
   Col 43: 0
   Col 44: 0
   Col 49: 0
   Col 50: 0
   Col 52: 0
```
### [EVENT] Time: 16:52:59.467 | Page: 29278 | RowID: 6058
```
   Col 1: 10527
   Col 2: status@broadcast
   Col 3: 1
   Col 4: AC0A5BECFA1EA3ED6FAC3E6C3A5AC7BC
   Col 5: status@broadcast
   Col 6: 0
   Col 7: A53A1970BF43B48B418E07B2EFDB096D
   Col 8: 923290988871@s.whatsapp.net
   Col 9: 923489076556@s.whatsapp.net
   Col 10: 💚
   Col 11: 1764777362430
```
### [EVENT] Time: 15:33:24.021 | Page: 29290 | RowID: 10527
```
   Col 1: status@broadcast
   Col 2: 0
   Col 3: A53A1970BF43B48B418E07B2EFDB096D
   Col 6: 8
   Col 7: 923489076556@s.whatsapp.net
   Col 9: <BLOB len=1569>
   Col 11: 1764775813
   Col 13: https://mmg.whatsapp.net/v/t62.7118-24/564756376_1574922720408612_1114545405262449158_n.enc?ccb=11-4&oh=01_Q5Aa3gGIuZKO103kOw8QOf-ZFZJvWKh1F_QYXrg-8PECH70Eng&oe=698C0DB2&_nc_sid=5e03e0&mms3=true
   Col 15: image/jpeg
   Col 16: 1
   Col 17: 26708
   Col 18: 0
   Col 21: <BLOB len=32>
   Col 23: <BLOB len=32>
   Col 24: 0
   Col 25: 0
   Col 32: 254
   Col 34: 0
   Col 35: 0
   Col 36: 0
   Col 37: 0
   Col 38: <BLOB len=285>
   Col 39: <BLOB len=536>
   Col 41: 1764775813
   Col 43: 0
   Col 44: 0
   Col 49: 0
   Col 50: 0
   Col 51: 💚
   Col 52: 1
```
### [EVENT] Time: 16:46:59.842 | Page: 29270 | RowID: 6123
```
   Col 1: 10493
   Col 2: status@broadcast
   Col 3: 0
   Col 4: A5B89DC7FC7A29EBF748F1871601ABD6
   Col 5: status@broadcast
   Col 6: 1
   Col 7: AC3E83649AF62E18E073D55E9BF92813
   Col 8: 923489076556@s.whatsapp.net
   Col 10: 💚
   Col 11: 1764781178779
```
### [EVENT] Time: 14:05:33.136 | Page: 29275 | RowID: 10493
```
   Col 1: status@broadcast
   Col 2: 0
   Col 3: AC3E83649AF62E18E073D55E9BF92813
   Col 6: 8
   Col 8: My Today Status😘
   Col 11: 1764775801
   Col 16: 9
   Col 17: 0
   Col 18: 0
   Col 24: 0
   Col 25: 0
   Col 32: 254
   Col 34: 0
   Col 35: 0
   Col 36: 0
   Col 37: 0
   Col 38: <BLOB len=89>
   Col 39: <BLOB len=89>
   Col 41: 1764775801
   Col 43: 0
   Col 44: 0
   Col 49: 0
   Col 50: 0
   Col 51: 💚
   Col 52: 1
```
### [EVENT] Time: 15:05:08.779 | Page: 29280 | RowID: 6124
```
   Col 1: 10493
   Col 2: status@broadcast
   Col 3: 0
   Col 4: A575F7BC49D85E46D53F195022BBFAB3
   Col 5: status@broadcast
   Col 6: 1
   Col 7: AC3E83649AF62E18E073D55E9BF92813
   Col 8: 923489076556@s.whatsapp.net
   Col 11: 1764781194968
```
### [EVENT] Time: 16:43:43.203 | Page: 29285 | RowID: 10493
```
   Col 1: status@broadcast
   Col 2: 0
   Col 3: AC3E83649AF62E18E073D55E9BF92813
   Col 6: 8
   Col 8: My Today Status😘
   Col 11: 1764775801
   Col 16: 9
   Col 17: 0
   Col 18: 0
   Col 24: 0
   Col 25: 0
   Col 32: 254
   Col 34: 0
   Col 35: 0
   Col 36: 0
   Col 37: 0
   Col 38: <BLOB len=89>
   Col 39: <BLOB len=89>
   Col 41: 1764775801
   Col 43: 0
   Col 44: 0
   Col 49: 0
   Col 50: 0
   Col 52: 0
```
### [EVENT] Time: 15:14:55.925 | Page: 30374 | RowID: 10522
```
   Col 1: status@broadcast
   Col 2: 0
   Col 3: A5DB515949D6E346EE818D10347CC87C
   Col 6: 8
   Col 9: <BLOB len=845>
   Col 11: 1764775039
   Col 13: https://mmg.whatsapp.net/v/t62.7161-24/566660098_1891253108145410_8819344814262064293_n.enc?ccb=11-4&oh=01_Q5Aa3gEDahvzVJfow9P6ufy-7deznJYF1pMBGXTfoROOwvRAmA&oe=698C03AA&_nc_sid=5e03e0&mms3=true
   Col 15: video/mp4
   Col 16: 3
   Col 17: 402236
   Col 18: 2
   Col 21: <BLOB len=32>
   Col 22: Back to work
   Col 23: <BLOB len=32>
   Col 24: 0
   Col 25: 0
   Col 29: <BLOB len=54>
   Col 32: 0
   Col 34: 0
   Col 35: 0
   Col 36: 0
   Col 37: 0
   Col 38: <BLOB len=359>
   Col 39: <BLOB len=507>
   Col 41: 1764775039
   Col 43: 0
   Col 44: 0
   Col 49: 0
   Col 50: 0
   Col 52: 0
   Col 55: /v/t62.36147-24/561766452_1251000016924903_1453441803908797759_n.enc?ccb=11-4&oh=01_Q5Aa3gGKKSJI4coEfUq0GurX8RpDikTCFKXheIDprhVQwSD1iA&oe=698C08C5&_nc_sid=5e03e0
   Col 56: <BLOB len=32>
   Col 57: <BLOB len=32>
```
### [EVENT] Time: 16:24:21.616 | Page: 29262 | RowID: 10193
```
   Col 1: 120363405979135311@g.us
   Col 2: 1
   Col 3: AC9DF887BD4A1759610E2ADD8ACFFB94
   Col 6: 11
   Col 11: 1764774830
   Col 16: 1046
   Col 17: 0
   Col 18: 0
   Col 24: 0
   Col 25: 0
   Col 29: <BLOB len=68>
   Col 32: 254
   Col 34: 0
   Col 35: 0
   Col 36: 0
   Col 37: 0
   Col 38: <BLOB len=59>
   Col 41: 1764774830
   Col 43: 0
   Col 44: 0
   Col 52: 0
   Col 53: 155834935959676@lid
```
### [EVENT] Time: 14:16:17.962 | Page: 29262 | RowID: 10193
```
   Col 1: 120363405979135311@g.us
   Col 2: 1
   Col 3: A589A77FC1571BAE5044C84E735AB895
   Col 6: 4
   Col 11: 1764776458
   Col 16: 1025
   Col 17: 0
   Col 18: 0
   Col 24: 0
   Col 25: 0
   Col 29: <BLOB len=69>
   Col 32: 254
   Col 33: 2:dbjIZNdL
   Col 34: 0
   Col 35: 0
   Col 36: 0
   Col 37: 0
   Col 38: <BLOB len=80>
   Col 41: 1764776458
   Col 43: 0
   Col 44: 0
   Col 52: 0
```
### [EVENT] Time: 16:07:10.962 | Page: 30386 | RowID: 10554
```
   Col 1: 120363405979135311@g.us
   Col 2: 0
   Col 3: A5AD1CAEC37D37BF18EDD4BC87D25682
   Col 6: 8
   Col 7: 155834935959676@lid
   Col 8: BEGIN:VCARD
VERSION:3.0
N:;;;;
FN:eulin
TEL;type=Mobile;ufone=923398420665:+92 339 8420665
X-WA-BIZ-NAME:eulin
END:VCARD
   Col 11: 1764779047
   Col 16: 4
   Col 17: 0
   Col 18: 0
   Col 20: eulin
   Col 24: 0
   Col 25: 0
   Col 32: 1
   Col 34: 0
   Col 35: 0
   Col 36: 0
   Col 37: 0
   Col 38: <BLOB len=71>
   Col 41: 1764779047
   Col 42: WaTagContact U60894e31d40cd617f1c7d306e87ac66d4135f0f7 C10f3b00117656e3c11f43ff069b8633a035f5615
   Col 43: 0
   Col 44: 0
   Col 49: 0
   Col 50: 0
   Col 52: 0
```
### [EVENT] Time: 15:21:47.642 | Page: 30386 | RowID: 10554
```
   Col 1: 120363405979135311@g.us
   Col 2: 0
   Col 3: A5AD1CAEC37D37BF18EDD4BC87D25682
   Col 6: 8
   Col 7: 155834935959676@lid
   Col 11: 1764779047
   Col 16: 1006
   Col 17: 0
   Col 18: 0
   Col 24: 0
   Col 25: 0
   Col 32: 0
   Col 34: 0
   Col 35: 0
   Col 36: 0
   Col 37: 0
   Col 38: <BLOB len=105>
   Col 41: 1764779047
   Col 43: 0
   Col 44: 0
   Col 49: 0
   Col 50: 0
   Col 52: 0
```
### [EVENT] Time: 15:16:31.776 | Page: 30388 | RowID: 10558
```
   Col 1: 120363405979135311@g.us
   Col 2: 0
   Col 3: A5FC88EE4FD70A0C39B2CAA91A26B113
   Col 6: 8
   Col 7: 155834935959676@lid
   Col 9: <BLOB len=2817>
   Col 11: 1764780197
   Col 16: 5
   Col 17: 0
   Col 18: 0
   Col 24: <FLOAT>
   Col 25: <FLOAT>
   Col 27:
   Col 32: 3
   Col 34: 0
   Col 35: 0
   Col 36: 0
   Col 37: 0
   Col 38: <BLOB len=71>
   Col 41: 1764780197
   Col 42: WaTagLocation U60894e31d40cd617f1c7d306e87ac66d4135f0f7 C10f3b00117656e3c11f43ff069b8633a035f5615
   Col 43: 0
   Col 44: 0
   Col 49: 0
   Col 50: 0
   Col 52: 0
```
### [EVENT] Time: 15:49:21.495 | Page: 30401 | RowID: 10558
```
   Col 1: 120363405979135311@g.us
   Col 2: 0
   Col 3: A5FC88EE4FD70A0C39B2CAA91A26B113
   Col 6: 8
   Col 7: 155834935959676@lid
   Col 11: 1764780197
   Col 16: 1006
   Col 17: 0
   Col 18: 0
   Col 24: <FLOAT>
   Col 25: <FLOAT>
   Col 32: 0
   Col 34: 0
   Col 35: 0
   Col 36: 0
   Col 37: 0
   Col 38: <BLOB len=117>
   Col 41: 1764780197
   Col 43: 0
   Col 44: 0
   Col 49: 0
   Col 50: 0
   Col 52: 0
```
### [EVENT] Time: 14:29:20.231 | Page: 30404 | RowID: 10571
```
   Col 1: 120363405979135311@g.us
   Col 2: 0
   Col 3: A52492AD3D6CB97BFDADA9904CD76F41
   Col 6: 8
   Col 7: 155834935959676@lid
   Col 11: 1764772883
   Col 16: 1043
   Col 17: 0
   Col 18: 0
   Col 24: 0
   Col 25: 0
   Col 32: 0
   Col 34: 0
   Col 35: 0
   Col 36: 0
   Col 37: 0
   Col 38: <BLOB len=93>
   Col 41: 1764772883
   Col 43: 0
   Col 44: 0
   Col 49: 0
   Col 50: 0
   Col 52: 0
```
### [EVENT] Time: 14:29:41.143 | Page: 121 | RowID: 1
```
   Col 1: 155834935959676@lid
   Col 2: A52492AD3D6CB97BFDADA9904CD76F41
   Col 3: 120363405979135311@g.us
   Col 4: 0
   Col 5: Good morning 🌞
   Col 6: proxy --hostname 0.0.0.0 --port 8080 --log-level c
   Col 7: https://call.whatsapp.com/voice/lArEUkQVWfpRPlyKFJIl4L
   Col 8: 1764777600
   Col 9: 1764774000
   Col 10: UK
   Col 12: 0
   Col 13: 0
```
### [EVENT] Time: 15:49:37.297 | Page: 30404 | RowID: 10571
```
   Col 1: 120363405979135311@g.us
   Col 2: 0
   Col 3: A52492AD3D6CB97BFDADA9904CD76F41
   Col 5: A5296341BF19DF62072237BB94136DF7
   Col 6: 8
   Col 7: 155834935959676@lid
   Col 11: 1764772883
   Col 16: 1043
   Col 17: 0
   Col 18: 0
   Col 24: 0
   Col 25: 0
   Col 32: 0
   Col 34: 0
   Col 35: 0
   Col 36: 2
   Col 37: 0
   Col 38: <BLOB len=99>
   Col 41: 1764772883
   Col 43: 0
   Col 44: 0
   Col 49: 0
   Col 50: 0
   Col 52: 0
```
### [EVENT] Time: 16:30:48.967 | Page: 30404 | RowID: 10573
```
   Col 1: 120363405979135311@g.us
   Col 2: 0
   Col 3: A5296341BF19DF62072237BB94136DF7
   Col 6: 8
   Col 7: 155834935959676@lid
   Col 11: 1764772952
   Col 16: 1027
   Col 17: 0
   Col 18: 0
   Col 24: 0
   Col 25: 0
   Col 32: 0
   Col 34: 0
   Col 35: 0
   Col 36: 0
   Col 37: 0
   Col 38: <BLOB len=43>
   Col 41: 1764772952
   Col 43: 0
   Col 44: 0
   Col 52: 0
```
### [EVENT] Time: 14:54:39.590 | Page: 121 | RowID: 1
```
   Col 1: 155834935959676@lid
   Col 2: A52492AD3D6CB97BFDADA9904CD76F41
   Col 3: 120363405979135311@g.us
   Col 4: 0
   Col 5: Good night 😴
   Col 6: proxy --hostname 0.0.0.0 --port 8080 --log-level c
   Col 7: https://call.whatsapp.com/video/HuGaTFXQw288xq6tDpeeru
   Col 8: 1764777600
   Col 10: UK
   Col 12: 0
   Col 13: 0
```
### [EVENT] Time: 15:43:56.333 | Page: 30404 | RowID: 10571
```
   Col 1: 120363405979135311@g.us
   Col 2: 0
   Col 3: A52492AD3D6CB97BFDADA9904CD76F41
   Col 5: A579BF51BECB443D7536CFC1E56A2E48
   Col 6: 8
   Col 7: 155834935959676@lid
   Col 11: 1764772883
   Col 16: 1043
   Col 17: 0
   Col 18: 0
   Col 24: 0
   Col 25: 0
   Col 32: 0
   Col 34: 0
   Col 35: 0
   Col 36: 2
   Col 37: 0
   Col 38: <BLOB len=91>
   Col 41: 1764772883
   Col 43: 0
   Col 44: 0
   Col 49: 0
   Col 50: 0
   Col 52: 0
```
### [EVENT] Time: 15:17:54.102 | Page: 30404 | RowID: 10575
```
   Col 1: 120363405979135311@g.us
   Col 2: 0
   Col 3: A579BF51BECB443D7536CFC1E56A2E48
   Col 6: 8
   Col 7: 155834935959676@lid
   Col 11: 1764773033
   Col 16: 1027
   Col 17: 0
   Col 18: 0
   Col 24: 0
   Col 25: 0
   Col 32: 0
   Col 34: 0
   Col 35: 0
   Col 36: 0
   Col 37: 0
   Col 38: <BLOB len=43>
   Col 41: 1764773033
   Col 43: 0
   Col 44: 0
   Col 52: 0
```
### [EVENT] Time: 15:23:18.750 | Page: 121 | RowID: 1
```
   Col 1: 155834935959676@lid
   Col 2: A52492AD3D6CB97BFDADA9904CD76F41
   Col 3: 120363405979135311@g.us
   Col 4: 0
   Col 5: The END
   Col 6: 💀💀💀💀
   Col 8: 1764777600
   Col 9: 1764774000
```
### [EVENT] Time: 15:17:29.625 | Page: 30404 | RowID: 10571
```
   Col 1: 120363405979135311@g.us
   Col 2: 0
   Col 3: A52492AD3D6CB97BFDADA9904CD76F41
   Col 5: A579BF51BECB443D7536CFC1E56A2E48
   Col 6: 8
   Col 7: 155834935959676@lid
   Col 11: 1764772883
   Col 16: 1006
   Col 17: 0
   Col 18: 0
   Col 24: 0
   Col 25: 0
   Col 32: 0
   Col 34: 0
   Col 35: 0
   Col 36: 0
   Col 37: 0
   Col 38: <BLOB len=125>
   Col 41: 1764772883
   Col 43: 0
   Col 44: 0
   Col 49: 0
   Col 50: 0
   Col 52: 0
```
### [EVENT] Time: 14:26:48.539 | Page: 130 | RowID: 1
```
   Col 1: 244744936493106@lid
   Col 2: 0
   Col 3: A54C36A09F860C59D18E5A13683FDEFF
   Col 4: 120363405979135311@g.us
   Col 5: 1764777232080
   Col 6: 1
```
### [EVENT] Time: 14:52:05.628 | Page: 130 | RowID: 2
```
   Col 1: 143177466024097@lid
   Col 2: 0
   Col 3: A54C36A09F860C59D18E5A13683FDEFF
   Col 4: 120363405979135311@g.us
   Col 5: 1764777218379
   Col 6: 3
```
### [EVENT] Time: 15:08:08.656 | Page: 130 | RowID: 2
```
   Col 1: 143177466024097@lid
   Col 2: 0
   Col 3: A54C36A09F860C59D18E5A13683FDEFF
   Col 4: 120363405979135311@g.us
   Col 5: 1764777241965
   Col 6: 2
```
### [EVENT] Time: 15:30:36.367 | Page: 30389 | RowID: 10602
```
   Col 1: 120363405979135311@g.us
   Col 2: 0
   Col 3: A51011C5590A8A181C40110E3E68F434
   Col 6: 18
   Col 7: 155834935959676@lid
   Col 9: <BLOB len=3962>
   Col 11: 0
   Col 16: 0
   Col 17: 0
   Col 18: 0
   Col 24: 0
   Col 25: 0
   Col 29: <BLOB len=6>
   Col 32: 0
   Col 34: 0
   Col 35: 0
   Col 36: 0
   Col 37: 0
   Col 38: <BLOB len=53>
   Col 41: 0
   Col 43: 0
   Col 44: 0
   Col 49: 0
   Col 50: 0
   Col 52: 0
```
### [EVENT] Time: 14:53:03.380 | Page: 30343 | RowID: 10602
```
   Col 1: 120363405979135311@g.us
   Col 2: 0
   Col 3: A51011C5590A8A181C40110E3E68F434
   Col 6: 18
   Col 7: 155834935959676@lid
   Col 11: 1764780430
   Col 16: 1006
   Col 17: 0
   Col 18: 0
   Col 24: 0
   Col 25: 0
   Col 32: 0
   Col 34: 0
   Col 35: 0
   Col 36: 0
   Col 37: 0
   Col 38: <BLOB len=89>
   Col 41: 1764780430
   Col 43: 0
   Col 44: 0
   Col 49: 0
   Col 50: 0
   Col 52: 0
```
### [EVENT] Time: 15:19:27.181 | Page: 30316 | RowID: 10372
```
   Col 1: 244744936493106@lid
   Col 2: 1
   Col 3: 3F532D17FE05713A4611
   Col 6: 18
   Col 9: <BLOB len=2373>
   Col 10: C:\Users\User\AppData\Local\Packages\5319275A.WhatsAppDesktop_cv1g1gvanyjgm\LocalState\shared\transfers\2026_1\bin-1837918186-3F532D17FE05713A4611-o
   Col 11: 1764777411
   Col 13: https://mmg.whatsapp.net/o1/v/t24/f2/m239/AQNT5KnSQwJKqq5i8xkQwnEl_Jwv_SQZ7SQLi7kh2HCWL0bCrzzYVu3iuRgR9XNlJmQ2IBhWgPAknU56oYIDNP2_StRx3CWVWwvP67cISQ?ccb=9-4&oh=01_Q5Aa3gErZlo2csSNEjI5l5Zu7zcVYeYkxLil1REXTovRii4G7w&oe=698B2F52&_nc_sid=e6ed6c&mms3=true
   Col 15: image/jpeg
   Col 16: 1
   Col 17: 78030
   Col 18: 0
   Col 20: AQNT5KnSQwJKqq5i8xkQwnEl_Jwv_SQZ7SQLi7kh2HCWL0bCrzzYVu3iuRgR9XNlJmQ2IBhWgPAknU56oYIDNP2_StRx3CWVWwvP67cISQ?ccb=9-4&oh=01_Q5Aa3gErZlo2csSNEjI5l5Zu7zcVYeYkxLil1REXTovRii4G7w&oe=698B2F52&_nc_sid=e6ed6c&mms3=true
   Col 21: <BLOB len=32>
   Col 22: tera ka kia ha?
   Col 23: <BLOB len=32>
   Col 24: 0
   Col 25: 0
   Col 26: shared\transfers\2026_1\c3e3ecd944b441ecab179c84cd46898a.jpg
   Col 29: <BLOB len=60>
   Col 32: 1
   Col 34: 0
   Col 35: 0
   Col 36: 0
   Col 37: 0
   Col 38: <BLOB len=318>
   Col 41: 1764777414
   Col 42: WaTagMedia WaTagImage WaSenderMe image/jpeg Ucdf02137940876b39476f948c7796c46cfdcbca7 Cb1943e4b628663eb8a3e190048f2ca3800a89875
   Col 43: 0
   Col 44: 0
   Col 49: 0
   Col 52: 0
   Col 54: 244744936493106@lid
```
### [EVENT] Time: 14:43:14.900 | Page: 30395 | RowID: 10620
```
   Col 1: 244744936493106@lid
   Col 2: 1
   Col 3: 3FD518393E650926AAAB
   Col 6: 18
   Col 9: <BLOB len=6131>
   Col 11: 0
   Col 16: 0
   Col 17: 0
   Col 18: 0
   Col 21: <BLOB len=32>
   Col 23: <BLOB len=32>
   Col 24: 0
   Col 25: 0
   Col 29: <BLOB len=52>
   Col 32: 0
   Col 34: 0
   Col 35: 0
   Col 36: 0
   Col 37: 0
   Col 38: <BLOB len=318>
   Col 41: 0
   Col 43: 0
   Col 44: 0
   Col 49: 0
   Col 52: 0
```
### [EVENT] Time: 14:07:02.423 | Page: 30395 | RowID: 10620
```
   Col 1: 244744936493106@lid
   Col 2: 1
   Col 3: 3FD518393E650926AAAB
   Col 6: 18
   Col 11: 1764773291
   Col 16: 1016
   Col 17: 0
   Col 18: 0
   Col 24: 0
   Col 25: 0
   Col 32: 254
   Col 34: 0
   Col 35: 0
   Col 36: 0
   Col 37: 0
   Col 38: <BLOB len=4>
   Col 41: 0
   Col 43: 0
   Col 44: 0
   Col 52: 0
```

***
