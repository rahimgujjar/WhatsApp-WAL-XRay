# WhatsApp Databases Schema Documentation
**Research Artifact: Architectural Blueprint**

## Overview
This document provides a complete structural mapping of the local SQLite database architecture recovered during independent forensic research into WhatsApp's desktop messaging environment (UWP/WinUI framework).

These schema definitions were programmatically extracted to facilitate the reverse-engineering of messaging state, binary blob structures (Protobuf), and internal metadata relationships. For environments where static schema extraction was restricted, the custom `wal_universal_mapper.py` utility was utilized to dynamically map database structures and validate field relationships at the binary level. This documentation serves as the foundational architectural blueprint for the `WhatsApp-WAL-XRay` forensic framework.

## Repository Context
- **Utility:** These blueprints were used to develop deterministic parsing logic for identifying transient data states (e.g., edited messages, ephemeral media).
- **Compliance:** All personally identifiable information (PII) has been stripped from this schema; only structural definitions and table metadata are preserved to maintain ethical and privacy standards.
- **Scope:** This schema covers the primary operational databases utilized by the native client, including message persistence, contact management, and cryptographic identity storage.

---
## 🗄️ syncd.dec.db

<table>
  <thead>
    <tr>
      <th align="left" width="220">Table Name</th>
      <th align="left" width="680">Schema Definition</th>
    </tr>
  </thead>
</table>
<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>Collections</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE Collections (
  Collection TEXT NOT NULL, Version INTEGER NOT NULL, 
  LtHash BLOB NOT NULL, PRIMARY KEY (Collection)
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>
<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>DownloadedPatches</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE DownloadedPatches (
  Collection INTEGER NOT NULL, Version INTEGER NOT NULL, Node BLOB NOT NULL, 
  NodeType INTEGER NOT NULL, HasKey BOOL NOT NULL, IsExternal BOOL NOT NULL, 
  PatchMac BLOB, SnapshotMac BLOB, KeyId BLOB, PRIMARY KEY (Collection, Version)
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>
<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>KeyRequestPendingDevices</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE KeyRequestPendingDevices (
  KeyId TEXT NOT NULL, DeviceId INTEGER NOT NULL, 
  Timestamp INTEGER NOT NULL, ReceivedAnswer INTEGER NOT NULL, 
  PRIMARY KEY (KeyId, DeviceId)
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>
<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>SyncdKeys</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE SyncdKeys (
  Epoch INTEGER NOT NULL, DeviceId INTEGER NOT NULL, KeyData BLOB NOT NULL, 
  Fingerprint TEXT NOT NULL, Timestamp INTEGER NOT NULL, StaleTimestamp INTEGER, 
  AdvFingerprint BLOB, PRIMARY KEY (Epoch, DeviceId)
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>
<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>metadata</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE metadata (
  version INTEGER
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

---
## 🗄️ settings.dec.db

<table>
  <thead>
    <tr>
      <th align="left" width="220">Table Name</th>
      <th align="left" width="680">Schema Definition</th>
    </tr>
  </thead>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>Settings</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE Settings (
  Key INT PRIMARY KEY,
  Value
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>TosAcceptanceStatus</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE TosAcceptanceStatus (
  NoticeId INT PRIMARY KEY,
  Status TINYINT NOT NULL
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>metadata</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE metadata (
  version INTEGER
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

---
## 🗄️ emojidict.dec.db

<table>
  <thead>
    <tr>
      <th align="left" width="220">Table Name</th>
      <th align="left" width="680">Schema Definition</th>
    </tr>
  </thead>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>emojidict</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE emojidict (
  Id INTEGER PRIMARY KEY,
  l TEXT NOT NULL,
  e TEXT NOT NULL,
  t TEXT NOT NULL
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>emojistate</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE emojistate (
  lang TEXT PRIMARY KEY,
  t INTEGER,
  fs INTEGER NON NULL,
  ft INTEGER,
  etag TEXT,
  top TEXT
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>metadata</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE metadata (
  version INTEGER
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

---
## 🗄️ concur.dec.db

<table>
  <thead>
    <tr>
      <th align="left" width="220">Table Name</th>
      <th align="left" width="680">Schema Definition</th>
    </tr>
  </thead>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>Bots</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE Bots (
  DbJid TEXT NOT NULL PRIMARY KEY,
  PersonaId TEXT,
  Name TEXT,
  Description TEXT,
  Tag TEXT,
  Attributes TEXT,
  Category TEXT,
  Avatar TEXT,
  Prompts TEXT,
  IsMetaCreated INTEGER,
  CreatorName TEXT,
  CreatorUrl TEXT
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>MembershipApprovalRequests</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE MembershipApprovalRequests (
  GroupJid TEXT NOT NULL,
  JoinerJid TEXT NOT NULL,
  ParentGroupJid TEXT,
  RequestedByJid TEXT NOT NULL,
  RequestMethod INTEGER NOT NULL,
  CreatedAt INTEGER NOT NULL,
  PRIMARY KEY (GroupJid, JoinerJid)
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>PeerDataRequest</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE PeerDataRequest (
  PeerDataRequestId INTEGER NOT NULL PRIMARY KEY,
  MessageKeyId INTEGER,
  DateTimeTriedRequest INTEGER,
  PeerDeviceJid TEXT,
  RequestTries INTEGER DEFAULT 0,
  PeerDataRequestMessage BLOB,
  IsOnFlight BIT DEFAULT 0
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>PeerReadReceipt</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE PeerReadReceipt (
  Id INTEGER NOT NULL PRIMARY KEY,
  TargetMessageId INTEGER NOT NULL,
  Jid TEXT NOT NULL
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>ReportingTokens</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE ReportingTokens (
  MessageKey TEXT NOT NULL PRIMARY KEY,
  ReportingTag BLOB,
  ReportingTokenContent BLOB,
  Version INTEGER,
  Timestamp INTEGER
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>metadata</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE metadata (
  version INTEGER
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

---
## 🗄️ axolotl.dec.db

<table>
  <thead>
    <tr>
      <th align="left" width="220">Table Name</th>
      <th align="left" width="680">Schema Definition</th>
    </tr>
  </thead>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>fast_ratchet_sender_keys</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE fast_ratchet_sender_keys (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  group_id TEXT NOT NULL,
  sender_id TEXT NOT NULL,
  record BLOB NOT NULL
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>identities</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE identities (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  recipient_id TEXT UNIQUE,
  registration_id INTEGER,
  public_key BLOB,
  private_key BLOB,
  next_prekey_id INTEGER,
  timestamp INTEGER,
  next_signed_prekey_id INTEGER,
  ident_msg_num INTEGER,
  pending_public_key BLOB
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>message_base_key</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE message_base_key (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  msg_key_remote_jid TEXT NOT NULL,
  msg_key_from_me BOOLEAN NOT NULL,
  msg_key_id TEXT NOT NULL,
  last_alice_base_key BLOB NOT NULL,
  timestamp INTEGER
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>prekeys</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE prekeys (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  prekey_id INTEGER UNIQUE,
  sent_to_server BOOLEAN,
  direct_distribution BOOLEAN,
  record BLOB
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>sender_keys</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE sender_keys (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  group_id TEXT NOT NULL,
  sender_id TEXT NOT NULL,
  record BLOB NOT NULL,
  creation_timestamp INTEGER DEFAULT 1766499712
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>session_log</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE session_log (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  device_id TEXT NOT NULL,
  group_id TEXT NULL,
  operation_type TINYINT NOT NULL,
  reason TEXT NULL,
  timestamp INTEGER NOT NULL
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>sessions</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE sessions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  recipient_id TEXT UNIQUE,
  record BLOB,
  timestamp INTEGER
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>signed_prekeys</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE signed_prekeys (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  prekey_id INTEGER UNIQUE,
  timestamp INTEGER,
  record BLOB
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>sqlite_sequence</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE sqlite_sequence (
  name,
  seq
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

---

## 🗄️ contacts.dec.db

<table>
  <thead>
    <tr>
      <th align="left" width="220">Table Name</th>
      <th align="left" width="680">Schema Definition</th>
    </tr>
  </thead>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>BlockList</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE BlockList (
  BlockListID INTEGER PRIMARY KEY,
  Members TEXT,
  LastUpdate INTEGER,
  Dhash TEXT
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>ChangeNumberRecords</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE ChangeNumberRecords (
  RecordId INTEGER PRIMARY KEY,
  OldJid TEXT,
  NewJid TEXT,
  Timestamp INTEGER
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>ChatPictures</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE ChatPictures (
  IsSmallPhotoInvalid INTEGER,
  IsLargePhotoInvalid INTEGER,
  ChatPictureId INTEGER PRIMARY KEY,
  Jid TEXT,
  WaPhotoId TEXT,
  LocalPhotoId TEXT,
  NotAvailable INTEGER,
  ServerPhotoId TEXT,
  LastPictureCheck INTEGER,
  BlockPictureRequestUntil INTEGER,
  PictureData BLOB,
  ThumbnailData BLOB
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>ChatTrustedContactTokenSenders</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE ChatTrustedContactTokenSenders (
  ChatTokenSenderId INTEGER PRIMARY KEY,
  Jid TEXT,
  Timestamp INTEGER
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>ChatTrustedContactTokens</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE ChatTrustedContactTokens (
  ChatTokenId INTEGER PRIMARY KEY,
  Jid TEXT,
  TcToken BLOB,
  TcTokenTimestamp INTEGER
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>ClientCapabilities</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE ClientCapabilities (
  ClientCapID INTEGER PRIMARY KEY,
  Jid TEXT,
  LastUpdate INTEGER,
  Category INTEGER,
  Value INTEGER
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>ContextSettings</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE ContextSettings (
  ContextKey INTEGER PRIMARY KEY,
  ContextValue BLOB
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>ConversionRecords</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE ConversionRecords (
  RecordId INTEGER PRIMARY KEY,
  ConversionJid TEXT,
  Timestamp INTEGER,
  PhoneNumber TEXT,
  Source TEXT,
  Data BLOB,
  LastActionTimestamp INTEGER
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

---
## 🗄️ messages.dec.db

<table>
  <thead>
    <tr>
      <th align="left" width="220">Table Name</th>
      <th align="left" width="680">Schema Definition</th>
    </tr>
  </thead>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>AddonOrphans</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE AddonOrphans
(
   RecordId INTEGER PRIMARY KEY,
   ParentKeyId TEXT,
   ParentKeyFromMe INTEGER,
   DbParentKeyRemoteJid TEXT,
   DbParentKeyParticipantJid TEXT,
   KeyId TEXT,
   KeyFromMe INTEGER,
   DbKeyRemoteJid TEXT,
   DbKeyParticipantJid TEXT,
   AddonType INTEGER,
   TimestampMs INTEGER,
   Payload BLOB
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>AdvUserInfos</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE AdvUserInfos
(
   DbUserJid TEXT PRIMARY KEY,
   Timestamp INTEGER,
   RawId INTEGER,
   CurrentIndex INTEGER,
   ExpectedTs INTEGER,
   ExpectedTsLastDeviceJobTs INTEGER,
   ExpectedTsUpdateTs INTEGER
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>ContactVCards</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE ContactVCards
(
   VCardId INTEGER PRIMARY KEY,
   Jid TEXT,
   MessageId INTEGER
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>ContextSettings</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE ContextSettings
(
   ContextKey INTEGER PRIMARY KEY,
   ContextValue BLOB
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>Conversations</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE Conversations
(
   ConversationID INTEGER PRIMARY KEY,
   Jid TEXT,
   JidType INTEGER,
   ParentJid TEXT,
   ComposingText TEXT,
   ComposingTextMetadata BLOB,
   DraftTimestamp INTEGER,
   Timestamp INTEGER,
   GroupOwner TEXT,
   GroupCreationT INTEGER,
   MembershipBannerDismissedAt INTEGER,
   GroupSubject TEXT,
   GroupSubjectT INTEGER,
   GroupAnnounceOnlyVId INTEGER,
   GroupInfoParticipantsVId INTEGER,
   GroupSubjectOwner TEXT,
   GroupSubjectPerformanceHint BLOB,
   LastMessageID INTEGER,
   TypingIndicatorKeyId TEXT,
   EffectiveFirstMessageID INTEGER,
   UnreadMessageCount INTEGER,
   UnreadMentionCount INTEGER,
   FirstUnreadMessageID INTEGER,
   LastOpenedMessageID INTEGER,
   MuteExpiration INTEGER,
   IsArchived INTEGER,
   IsSyncMutated INTEGER,
   Status INTEGER,
   Flags INTEGER,
   AutomuteTimer INTEGER,
   SortKey INTEGER,
   ModifyTag INTEGER,
   UnreadTileCount INTEGER,
   ParticipantDevicesHash TEXT,
   InternalPropertiesProtobuf BLOB,
   GroupDescription TEXT,
   GroupDescriptionT INTEGER,
   GroupDescriptionOwner TEXT,
   GroupDescriptionId TEXT,
   EphemeralMessagesExpirationInSec INTEGER,
   DbEphemeralMessagesLastChangeTimestamp INTEGER,
   DbEphemeralMessagesLastNotificationTimestamp INTEGER,
   DbEphemeralMessagesChangedByDeviceJid TEXT,
   EphemeralMessagesChangeInitiator INTEGER,
   PhashFromHistorySync TEXT,
   HistorySyncStatus INTEGER,
   GrowthLockType TEXT,
   GrowthLockExpiration INTEGER,
   LastJoinedTimestamp INTEGER,
   LidOriginType INTEGER,
   ParticipantCount INTEGER,
   DbAccountId TEXT,
   DbPnJid TEXT
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>DanglingDeliveryReceipts</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE DanglingDeliveryReceipts
(
   DeliveryReceiptId INTEGER PRIMARY KEY,
   Data BLOB
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>DeletedTemplateButtonReplyMessages</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE DeletedTemplateButtonReplyMessages
(
   Id INTEGER PRIMARY KEY,
   KeyRemoteJid TEXT,
   KeyFromMe INTEGER,
   KeyId TEXT,
   SelectedIndex INTEGER
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>DeviceCapabilities</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE DeviceCapabilities
(
   RecordId INTEGER PRIMARY KEY,
   DbDeviceJid TEXT,
   ChatLockSupport INTEGER,
   Protobuf BLOB
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>DevicesOwnerships</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE DevicesOwnerships
(
   RecordId INTEGER PRIMARY KEY,
   User TEXT,
   Device TEXT,
   DeviceVersion INTEGER,
   AdvKeyIndex INTEGER
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>EmojiSelectedIndexes</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE EmojiSelectedIndexes
(
   EmojiID INTEGER PRIMARY KEY,
   EmojiCode TEXT,
   Selection INTEGER
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>EmojiUsages</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE EmojiUsages
(
   EmojiID INTEGER PRIMARY KEY,
   EmojiCode TEXT,
   UsageWeight INTEGER
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>EventResponses</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE EventResponses
(
   ResponseId INTEGER PRIMARY KEY,
   ResponderJid TEXT,
   ParentKeyFromMe INTEGER,
   ParentKeyId TEXT,
   ParentKeyRemoteJid TEXT,
   SenderTimestampMs INTEGER,
   RsvpType INTEGER
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>Events</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE Events
(
   EventId INTEGER PRIMARY KEY,
   CreatorJid TEXT,
   KeyId TEXT,
   KeyRemoteJid TEXT,
   IsCancelled INTEGER,
   Name TEXT,
   Description TEXT,
   CallLink TEXT,
   StartTime INTEGER,
   EndTime INTEGER,
   LocationName TEXT,
   Address TEXT,
   Latitude REAL,
   Longitude REAL
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>FrequentChatScores</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE FrequentChatScores
(
   ID INTEGER PRIMARY KEY,
   Jid TEXT,
   DefaultScore INTEGER,
   ImageScore INTEGER,
   VideoScore INTEGER
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>GroupParticipants</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE GroupParticipants
(
   GroupParticipantStateId INTEGER PRIMARY KEY,
   GroupJid TEXT,
   MemberJid TEXT,
   Flags INTEGER,
   DevicesNeedingSenderKey BLOB,
   DevicesWithSenderKey BLOB
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>HistorySyncChunkStatuses</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE HistorySyncChunkStatuses
(
   RecordId INTEGER PRIMARY KEY,
   SyncType INTEGER,
   ChunkOrder INTEGER,
   MessageKeyId TEXT,
   LocalPath TEXT,
   SyncInitiatedTime INTEGER,
   SyncDownloadedTime INTEGER,
   SyncCompletedTime INTEGER,
   SentReceipt INTEGER,
   HistorySyncNotification BLOB,
   InlineData BLOB,
   DownloadAttempts INTEGER,
   IsMediaRetryPending INTEGER,
   SyncDownloadExpiryTime INTEGER,
   Progress INTEGER
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>InactiveReceipts</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE InactiveReceipts
(
   InactiveReceiptId INTEGER PRIMARY KEY,
   DbChatJid TEXT,
   DbParticipantJid TEXT,
   KeyId TEXT,
   TimestampUtc INTEGER
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>JidInfos</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE JidInfos
(
   ID INTEGER PRIMARY KEY,
   Jid TEXT,
   MuteExpirationUtc INTEGER,
   NotificationSound TEXT,
   RingTone TEXT,
   IsSuspicious INTEGER,
   PromptedVCards INTEGER,
   SupportsFullEncryption INTEGER,
   SaveMediaToPhone INTEGER,
   Wallpaper TEXT,
   IsStatusMuted INTEGER,
   StatusAutoDownloadQuota INTEGER,
   FavoriteOrder INTEGER
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>KeepInChatMessages</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE KeepInChatMessages
(
   RecordId INTEGER PRIMARY KEY,
   ParentKeyId TEXT,
   ParentKeyFromMe INTEGER,
   DbParentKeyRemoteJid TEXT,
   DbParentKeyParticipantJid TEXT,
   KeyId TEXT,
   DbSenderJid TEXT,
   KeepType INTEGER,
   TimestampMs INTEGER,
   KeepCount INTEGER
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>LabelConversations</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE LabelConversations
(
   RecordId INTEGER PRIMARY KEY,
   LabelId INTEGER,
   Jid TEXT
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>LabelMessages</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE LabelMessages
(
   RecordId INTEGER PRIMARY KEY,
   LabelId INTEGER,
   MessageId INTEGER
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>Labels</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE Labels
(
   LabelId INTEGER PRIMARY KEY,
   Name TEXT,
   Color INTEGER,
   PredefinedId INTEGER
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>LocalFiles</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE LocalFiles
(
   LocalFileID INTEGER PRIMARY KEY,
   LocalFileUri TEXT,
   Sha1Hash BLOB,
   ReferenceCount INTEGER,
   FileType INTEGER,
   FileSize INTEGER,
   MsgRefCount INTEGER,
   StatusRefCount INTEGER,
   ThumbRefCount INTEGER,
   StickerRefCount INTEGER,
   QuotedMediaRefCount INTEGER
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>MessageMiscInfos</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE MessageMiscInfos
(
   ID INTEGER PRIMARY KEY,
   MessageId INTEGER,
   ErrorCode INTEGER,
   BackgroundId TEXT,
   TargetFilename TEXT,
   AlternateUploadUri TEXT,
   ImageBinaryInfo BLOB,
   TranscoderData BLOB
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>Messages</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE Messages
(
   MessageID INTEGER PRIMARY KEY AUTOINCREMENT,
   KeyRemoteJid TEXT,
   KeyFromMe INTEGER,
   KeyId TEXT,
   ParentKey TEXT,
   EditId TEXT,
   Status INTEGER,
   RemoteResource TEXT,
   Data TEXT,
   BinaryData BLOB,
   DataFileName TEXT,
   TimestampLong INTEGER,
   PushName TEXT,
   MediaUrl TEXT,
   MediaIp TEXT,
   MediaMimeType TEXT,
   MediaWaType INTEGER,
   MediaSize INTEGER,
   MediaDurationSeconds INTEGER,
   MediaOrigin TEXT,
   MediaName TEXT,
   MediaHash BLOB,
   MediaCaption TEXT,
   MediaKey BLOB,
   Latitude REAL,
   Longitude REAL,
   LocalFileUri TEXT,
   LocationDetails TEXT,
   LocationUrl TEXT,
   TextPerformanceHint BLOB,
   QuoteTextPerformanceHint BLOB,
   TextSplittingHint BLOB,
   FtsStatus INTEGER,
   ParticipantDevicesHash TEXT,
   IsStarred INTEGER,
   KeepInChat INTEGER,
   Flags INTEGER,
   ExtraFlags INTEGER,
   InternalPropertiesProtobuf BLOB,
   ProtoBuf BLOB,
   QuotedMediaFileUri TEXT,
   ServerReceivedTimestamp INTEGER,
   Tags TEXT,
   ForwardingScore INTEGER,
   DbExpirationTimestamp INTEGER,
   TemplateBytes BLOB,
   TemplateButtonReplyBytes BLOB,
   HistoricalHostStorage INTEGER,
   HistoricalActualActors INTEGER,
   HistoricalPrivacyModeTs INTEGER,
   IsPrivacyConflict INTEGER,
   Reactions TEXT,
   ReactionsCount INTEGER,
   CommentsCounter BLOB,
   DbAccountId TEXT,
   ThumbnailDirectPath TEXT,
   ThumbnailSha256 BLOB,
   ThumbnailEncSha256 BLOB,
   SupportPayload TEXT
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>MessagesFts</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE VIRTUAL TABLE MessagesFts USING fts5(
  content='MessagesHelperViewForFts',
  content_rowid=MessageID,
  KeyRemoteJid UNINDEXED,
  Data,
  MediaName,
  MediaCaption,
  LocationDetails,
  Tags,
  prefix=2,
  tokenize='unicode61'
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>MessagesFts_config</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE 'MessagesFts_config'(k PRIMARY KEY, v) WITHOUT ROWID</code></pre>
      </td>
    </tr>
  </tbody>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>MessagesFts_data</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE 'MessagesFts_data'(id INTEGER PRIMARY KEY, block BLOB)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>MessagesFts_docsize</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE 'MessagesFts_docsize'(id INTEGER PRIMARY KEY, sz BLOB)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>MessagesFts_idx</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE 'MessagesFts_idx'(segid, term, pgno, PRIMARY KEY(segid, term)) WITHOUT ROWID</code></pre>
      </td>
    </tr>
  </tbody>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>OrphanedReceipts</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE OrphanedReceipts
(
   OrphanedReceiptId INTEGER PRIMARY KEY,
   DbChatJid TEXT,
   KeyId TEXT,
   DbSenderJid TEXT,
   Status INTEGER,
   IsReadSelfReceipt INTEGER,
   Timestamp INTEGER
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>PastParticipants</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE PastParticipants
(
   PastParticipantStateId INTEGER PRIMARY KEY,
   GroupJid TEXT,
   MemberJid TEXT,
   LeaveTime INTEGER,
   LeaveReason INTEGER
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>PeerMessages</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE PeerMessages
(
   PeerMessageDataId INTEGER PRIMARY KEY,
   MessageKeyId TEXT,
   DeviceId INTEGER,
   MsgType INTEGER,
   Status INTEGER,
   Data BLOB
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>PendingMessages</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE PendingMessages
(
   PendingMessagesId INTEGER PRIMARY KEY,
   KeyRemoteJid TEXT,
   KeyId TEXT,
   Timestamp INTEGER,
   ProtobufMessage BLOB,
   RemoteResource TEXT,
   PendingMsgPropertiesProtobuf BLOB
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>PersistentActions</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE PersistentActions
(
   ActionID INTEGER PRIMARY KEY,
   ActionType INTEGER,
   ActionDataString TEXT,
   Attempts INTEGER,
   AttemptsLimit INTEGER,
   ExpirationTime INTEGER,
   Jid TEXT,
   FromMe INTEGER,
   Id TEXT
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>PinInChatMessages</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE PinInChatMessages
(
   RecordId INTEGER PRIMARY KEY,
   KeyId TEXT,
   KeyFromMe INTEGER,
   DbKeyRemoteJid TEXT,
   DbKeyParticipantJid TEXT,
   ParentKeyId TEXT,
   ParentKeyFromMe INTEGER,
   DbParentKeyRemoteJid TEXT,
   DbParentKeyParticipantJid TEXT,
   TimestampMs INTEGER,
   DbParentMessageId INTEGER,
   DbSenderJid TEXT,
   ExpiryTimestampMs INTEGER,
   PinType INTEGER,
   DurationInSecs INTEGER
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>PlaceHolderReceipts</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE PlaceHolderReceipts
(
   CipherTextReceiptId INTEGER PRIMARY KEY,
   KeyRemoteJid TEXT,
   ParticipantJid TEXT,
   KeyId TEXT,
   IsCipherText INTEGER,
   IsMdPlaceholder INTEGER
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>PollVotes</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE PollVotes
(
   RecordId INTEGER PRIMARY KEY,
   ParentKeyId TEXT,
   ParentKeyFromMe INTEGER,
   DbParentKeyRemoteJid TEXT,
   DbParentParticipantJid TEXT,
   DbVoterJid TEXT,
   SentMsTimestamp INTEGER,
   OrphanEncIv BLOB,
   OrphanEncPayload BLOB
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>PollVotesOptions</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE PollVotesOptions
(
   RecordId INTEGER PRIMARY KEY,
   PollVoteId INTEGER,
   VoteId INTEGER
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>PostponedReceipts</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE PostponedReceipts
(
   PostponedReceiptId INTEGER PRIMARY KEY,
   TargetJid TEXT,
   ParticipantJid TEXT,
   KeyId TEXT,
   TimestampLong INTEGER
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>QuickReplies</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE QuickReplies
(
   QuickReplyId TEXT PRIMARY KEY,
   Shortcut TEXT,
   Message TEXT,
   Count INTEGER
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>Reactions</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE Reactions
(
   ReactionId INTEGER PRIMARY KEY,
   ParentMessageID INTEGER,
   KeyRemoteJid TEXT,
   KeyFromMe INTEGER,
   KeyId TEXT,
   ParentKeyRemoteJid TEXT,
   ParentKeyFromMe INTEGER,
   ParentKeyId TEXT,
   RemoteResource TEXT,
   ParentRemoteResource TEXT,
   Text TEXT,
   SenderTimestampMs INTEGER,
   GroupingKey TEXT,
   BinaryData BLOB
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>ReceiptState</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE ReceiptState
(
   ReceiptStateId INTEGER PRIMARY KEY,
   MessageId INTEGER,
   Jid TEXT,
   Timestamp INTEGER,
   DbDevicesUndeliveredInfo BLOB,
   DbDevicesDelivered BLOB,
   ReceivedByTimestamp INTEGER,
   DbReceivedByJid TEXT,
   ReadByTimestamp INTEGER,
   DbReadByJid TEXT,
   PlayedByTimestamp INTEGER,
   DbPlayedByJid TEXT
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>RevokeResendExtraDevicesForMsgs</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE RevokeResendExtraDevicesForMsgs
(
   RevokeResendMissingId INTEGER PRIMARY KEY,
   MessageId INTEGER,
   DbDeviceJids TEXT
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>ServerSyncVersions</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE ServerSyncVersions
(
   Collection TEXT PRIMARY KEY,
   Version INTEGER,
   LtHash BLOB
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>Stickers</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE Stickers
(
   StickerID INTEGER PRIMARY KEY,
   Url TEXT,
   FileHash BLOB,
   EncodedFileHash BLOB,
   MediaKey BLOB,
   MimeType TEXT,
   Height INTEGER,
   Width INTEGER,
   LocalFileUri TEXT,
   DateTimeStarred INTEGER,
   DateTimeSent INTEGER,
   PackId TEXT,
   DirectPath TEXT,
   FileLength INTEGER,
   UsageWeight INTEGER,
   DateTimeUploaded INTEGER,
   DateTimeTriedUpload INTEGER,
   UploadTries INTEGER,
   DateTimeTriedDownload INTEGER,
   DownloadTries INTEGER,
   IsAvatar INTEGER,
   IsLottie INTEGER,
   SourceDeviceJid TEXT
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>SyncDMutations</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE SyncDMutations
(
   Status INTEGER,
   Epoch INTEGER,
   DeviceId INTEGER,
   OrphanEntityId TEXT,
   RecordId INTEGER PRIMARY KEY,
   DbIndexParams TEXT,
   SyncDIndex TEXT,
   DbValue BLOB,
   Operation INTEGER,
   Type INTEGER,
   DbType TEXT,
   KeyId BLOB,
   Mac BLOB,
   FeatureVersion INTEGER,
   Collection INTEGER
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>SyncDPendingMutations</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE SyncDPendingMutations
(
   RecordId INTEGER PRIMARY KEY,
   DbIndexParams TEXT,
   SyncDIndex TEXT,
   DbValue BLOB,
   Operation INTEGER,
   Type INTEGER,
   DbType TEXT,
   KeyId BLOB,
   Mac BLOB,
   FeatureVersion INTEGER,
   Collection INTEGER
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>WaScheduledTasks</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE WaScheduledTasks
(
   TaskID INTEGER PRIMARY KEY,
   TaskType INTEGER,
   LookupKey TEXT,
   DbJid TEXT,
   BinaryData BLOB,
   Attempts INTEGER,
   AttemptsLimit INTEGER,
   ExpirationUtc INTEGER,
   Restriction INTEGER
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>WaStatuses</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE WaStatuses
(
   StatusId INTEGER PRIMARY KEY,
   MessageId INTEGER,
   MessageKeyId TEXT,
   Jid TEXT,
   Timestamp INTEGER,
   IsViewed INTEGER,
   IsChecked INTEGER
)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>metadata</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE metadata(version int)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>sqlite_sequence</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE sqlite_sequence(name,seq)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

<table>
  <tbody>
    <tr>
      <td valign="top" width="220"><code>sqlite_stat1</code></td>
      <td valign="top" width="680">
        <pre><code>CREATE TABLE sqlite_stat1(tbl,idx,stat)</code></pre>
      </td>
    </tr>
  </tbody>
</table>
