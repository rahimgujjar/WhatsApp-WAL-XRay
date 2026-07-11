# Application State Type Definitions & Forensic Anomalies

This reference table maps the proprietary integer codes extracted from local database structural columns to their operational states. Crucially, it highlights discrepancies between expected documentation and empirical data structures captured during live memory extraction.

| Raw Type ID | Operational Classification | Expected Standard | Observed Forensic Anomalies & MIME Types |
| :--- | :--- | :--- | :--- |
| **0** | `TEXT_STANDARD` | Standard chat text | `text/plain` |
| **1** | `MEDIA_IMAGE` | Image / Photo | `image/jpeg` |
| **2** | `MEDIA_AUDIO` | Generic audio media | `audio/ogg; codecs=opus`, `audio/mpeg` |
| **3** | `MEDIA_VIDEO` | Standard video payload | `video/mp4` |
| **5** | `CONTACT_VCARD` | Shared Contact (vCard) | **Anomaly:** Empirical testing reveals raw geographical coordinates logged here instead (e.g., `72.7066022, 32.0856843`). |
| **8** | `MEDIA_DOCUMENT` | General File Transfer | Captures massive variations: `application/pdf`, `application/zip`, `text/html`, `application/json`, `text/x-python`, `application/vnd.android.package-archive`. **Anomaly:** Bizarrely captures `image/jpeg` in specific payload states. |
| **9** | `TEXT_EXTENDED_URL` | External routing links | Frequently mixed with raw localized text/Urdu in bulk replies. |
| **10** | `MEDIA_VOICE_NOTE` | Push-to-Talk Audio | **Anomaly:** Documented universally as short audio, but empirical parsing only surfaced `video/mp4` headers in this field. |
| **11** | `TELEMETRY_LOCATION` | Geo-location | Captures raw coordinate data overlapping with Type 5 behaviors (e.g., `72.7066022, 32.0856843`). |
| **19** | `MEDIA_STICKER` | Sticker payloads | `image/webp` |
| **29** | `STATE_REACTION` | Emoji Reactions | Handles both reaction applications and revocation states. |
| **1001** | `STATE_STATUS_AI` | Generative AI / Status | Maps to AI markdown text *and* user status updates (videos, pics, text configurations). |
| **1006** | `ACTION_REVOKE_ALL` | Universal Message Delete | Bypasses admin checks; standard user deletion flag covering all media types. |
| **1016** | `MEDIA_IMAGE_HD` | High-Def Image | `image/jpeg` |
| **1017** | `MEDIA_VIDEO_HD` | High-Def Video | `video/mp4` |
| **1020** | `INTERACTIVE_POLL` | User Polls | Generates voting configurations. |
| **1025** | `ACTION_ADMIN_REVOKE` | Group Admin Delete | Explicit administrative purge command. |
| **1027** | `ACTION_EDIT_TEXT` | Content Modification | Post-transmission message edit states (Preserves Edit ID trace). |
| **1039** | `MEDIA_AUDIO_OGG` | High-quality audio | `audio/ogg; codecs=opus` |
| **1046** | `MEDIA_EPHEMERAL` | View-Once Restrictions | Flags images, videos, and audio for single-view destruction loops. |