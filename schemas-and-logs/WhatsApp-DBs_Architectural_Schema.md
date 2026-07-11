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

## syncd.dec.db

### Collections

```sql
CREATE TABLE Collections
(Collection TEXT NOT NULL, Version INTEGER NOT NULL, LtHash BLOB NOT NULL, PRIMARY KEY (Collection))

```

### DownloadedPatches

```sql
CREATE TABLE DownloadedPatches
(Collection INTEGER NOT NULL, Version INTEGER NOT NULL, Node BLOB NOT NULL, NodeType INTEGER NOT NULL, HasKey BOOL NOT NULL, IsExternal BOOL NOT NULL, PatchMac BLOB, SnapshotMac BLOB, KeyId BLOB, PRIMARY KEY (Collection, Version))

```

### KeyRequestPendingDevices

```sql
CREATE TABLE KeyRequestPendingDevices
(KeyId TEXT NOT NULL, DeviceId INTEGER NOT NULL, Timestamp INTEGER NOT NULL, ReceivedAnswer INTEGER NOT NULL, PRIMARY KEY (KeyId, DeviceId))

```

### SyncdKeys

```sql
CREATE TABLE SyncdKeys
(Epoch INTEGER NOT NULL, DeviceId INTEGER NOT NULL, KeyData BLOB NOT NULL, Fingerprint TEXT NOT NULL, Timestamp INTEGER NOT NULL, StaleTimestamp INTEGER, AdvFingerprint BLOB, PRIMARY KEY (Epoch, DeviceId))

```

### metadata

```sql
CREATE TABLE metadata (version INTEGER)

```

## settings.dec.db

### Settings

```sql
CREATE TABLE Settings (Key INT PRIMARY KEY, Value)

```

### TosAcceptanceStatus

```sql
CREATE TABLE TosAcceptanceStatus (NoticeId INT PRIMARY KEY, Status TINYINT NOT NULL)

```

### metadata

```sql
CREATE TABLE metadata (version INTEGER)

```

## emojidict.dec.db

### emojidict

```sql
CREATE TABLE emojidict
(Id INTEGER PRIMARY KEY, l TEXT NOT NULL, e TEXT NOT NULL, t TEXT NOT NULL )

```

### emojistate

```sql
CREATE TABLE emojistate
(lang TEXT PRIMARY KEY, t INTEGER, fs INTEGER NON NULL, ft INTEGER, etag TEXT , top TEXT)

```

### metadata

```sql
CREATE TABLE metadata (version INTEGER)

```

## concur.dec.db

### Bots

```sql
CREATE TABLE Bots
(DbJid TEXT NOT NULL PRIMARY KEY, PersonaId TEXT, Name TEXT,Description TEXT,Tag TEXT,Attributes TEXT,Category TEXT,Avatar TEXT,Prompts TEXT, IsMetaCreated INTEGER, CreatorName TEXT, CreatorUrl TEXT)

```

### MembershipApprovalRequests

```sql
CREATE TABLE MembershipApprovalRequests
(GroupJid TEXT NOT NULL, JoinerJid TEXT NOT NULL, ParentGroupJid TEXT, RequestedByJid TEXT NOT NULL, RequestMethod INTEGER NOT NULL, CreatedAt INTEGER NOT NULL, PRIMARY KEY (GroupJid, JoinerJid))

```

### PeerDataRequest

```sql
CREATE TABLE PeerDataRequest
(PeerDataRequestId INTEGER NOT NULL PRIMARY KEY, MessageKeyId INTEGER, DateTimeTriedRequest INTEGER, PeerDeviceJid TEXT,RequestTries INTEGER DEFAULT 0,PeerDataRequestMessage BLOB,IsOnFlight BIT DEFAULT 0)

```

### PeerReadReceipt

```sql
CREATE TABLE PeerReadReceipt
(Id INTEGER NOT NULL PRIMARY KEY, TargetMessageId INTEGER NOT NULL, Jid TEXT NOT NULL)

```

### ReportingTokens

```sql
CREATE TABLE ReportingTokens
(MessageKey TEXT NOT NULL PRIMARY KEY, ReportingTag BLOB, ReportingTokenContent BLOB,Version INTEGER,Timestamp INTEGER)

```

### metadata

```sql
CREATE TABLE metadata (version INTEGER)

```

## axolotl.dec.db

### fast_ratchet_sender_keys

```sql
CREATE TABLE fast_ratchet_sender_keys (id INTEGER PRIMARY KEY AUTOINCREMENT, group_id TEXT NOT NULL, sender_id TEXT NOT NULL, record BLOB NOT NULL)

```

### identities

```sql
CREATE TABLE identities (id INTEGER PRIMARY KEY AUTOINCREMENT, recipient_id TEXT UNIQUE, registration_id INTEGER, public_key BLOB, private_key BLOB, next_prekey_id INTEGER, timestamp INTEGER, next_signed_prekey_id INTEGER, ident_msg_num INTEGER, pending_public_key BLOB)

```

### message_base_key

```sql
CREATE TABLE message_base_key (id INTEGER PRIMARY KEY AUTOINCREMENT, msg_key_remote_jid TEXT NOT NULL, msg_key_from_me BOOLEAN NOT NULL, msg_key_id TEXT NOT NULL, last_alice_base_key BLOB NOT NULL, timestamp INTEGER)

```

### prekeys

```sql
CREATE TABLE prekeys (id INTEGER PRIMARY KEY AUTOINCREMENT, prekey_id INTEGER UNIQUE, sent_to_server BOOLEAN, direct_distribution BOOLEAN, record BLOB)

```

### sender_keys

```sql
CREATE TABLE sender_keys (id INTEGER PRIMARY KEY AUTOINCREMENT, group_id TEXT NOT NULL, sender_id TEXT NOT NULL, record BLOB NOT NULL, creation_timestamp INTEGER DEFAULT 1766499712)

```

### session_log

```sql
CREATE TABLE session_log (id INTEGER PRIMARY KEY AUTOINCREMENT, device_id TEXT NOT NULL, group_id TEXT NULL, operation_type TINYINT NOT NULL, reason TEXT NULL, timestamp INTEGER NOT NULL )

```

### sessions

```sql
CREATE TABLE sessions (id INTEGER PRIMARY KEY AUTOINCREMENT, recipient_id TEXT UNIQUE, record BLOB, timestamp INTEGER)

```

### signed_prekeys

```sql
CREATE TABLE signed_prekeys (id INTEGER PRIMARY KEY AUTOINCREMENT, prekey_id INTEGER UNIQUE, timestamp INTEGER, record BLOB)

```

### sqlite_sequence

```sql
CREATE TABLE sqlite_sequence(name,seq)

```

## abprops.dec.db

IT IS COMPLETELY EMPTY, NOTHING RETURNS AFTER RUNNING THIS COMMAND:

```sql
SELECT name, sql
FROM sqlite_master
WHERE type='table'
ORDER BY name;

```

## calls.dec.db

IT IS COMPLETELY USELESS FOR OUR WORK, AS I THINK.

## contacts.dec.db

### BlockList

```sql
CREATE TABLE BlockList
(
   BlockListID INTEGER PRIMARY KEY,
   Members TEXT,
   LastUpdate INTEGER,
   Dhash TEXT
)

```

### ChangeNumberRecords

```sql
CREATE TABLE ChangeNumberRecords
(
   RecordId INTEGER PRIMARY KEY,
   OldJid TEXT,
   NewJid TEXT,
   Timestamp INTEGER
)

```

### ChatPictures

```sql
CREATE TABLE ChatPictures
(
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
)

```

### ChatTrustedContactTokenSenders

```sql
CREATE TABLE ChatTrustedContactTokenSenders
(
   ChatTokenSenderId INTEGER PRIMARY KEY,
   Jid TEXT,
   Timestamp INTEGER
)

```

### ChatTrustedContactTokens

```sql
CREATE TABLE ChatTrustedContactTokens
(
   ChatTokenId INTEGER PRIMARY KEY,
   Jid TEXT,
   TcToken BLOB,
   TcTokenTimestamp INTEGER
)

```

### ClientCapabilities

```sql
CREATE TABLE ClientCapabilities
(
   ClientCapID INTEGER PRIMARY KEY,
   Jid TEXT,
   LastUpdate INTEGER,
   Category INTEGER,
   Value INTEGER
)

```

### ContextSettings

```sql
CREATE TABLE ContextSettings
(
   ContextKey INTEGER PRIMARY KEY,
   ContextValue BLOB
)

```

### ConversionRecords

```sql
CREATE TABLE ConversionRecords
(
   RecordId INTEGER PRIMARY KEY,
   ConversionJid TEXT,
   Timestamp INTEGER,
   PhoneNumber TEXT,
   Source TEXT,
   Data BLOB,
   LastActionTimestamp INTEGER
)

```

### PhoneNumbers

```sql
CREATE TABLE PhoneNumbers
(
   PhoneNumberID INTEGER PRIMARY KEY,
   RawPhoneNumber TEXT,
   Jid TEXT,
   IsNew INTEGER
)

```

### SyncDMutations

```sql
CREATE TABLE SyncDMutations
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
)

```

### SyncDPendingMutations

```sql
CREATE TABLE SyncDPendingMutations
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
)

```

### UserStatuses

```sql
CREATE TABLE UserStatuses
(
   StatusID INTEGER PRIMARY KEY,
   Jid TEXT,
   JidNotificationHash TEXT,
   LidNotificationHash TEXT,
   PhotoPath TEXT,
   PhotoHash BLOB,
   Status TEXT,
   StatusExpiryInSec INTEGER,
   DateTimeSet INTEGER,
   ContactName TEXT,
   FirstName TEXT,
   PushName TEXT,
   UserName TEXT,
   DisplayNameFromServer TEXT,
   DbLid TEXT,
   IsInDeviceContactList INTEGER,
   IsSidelistSynced INTEGER,
   IsInDevicePhonebook INTEGER,
   IsWaUser INTEGER,
   PhoneNumberKind INTEGER,
   VerifiedName INTEGER,
   VerifiedNameCertificateDetailsSerialized BLOB,
   VerifiedLevel INTEGER,
   HostStorage INTEGER,
   ActualActors INTEGER,
   PrivacyModeTs INTEGER,
   InternalPropertiesProtobuf BLOB,
   ShouldSync INTEGER,
   ShouldSaveOnPrimaryAb INTEGER,
   HasPnBeenShared INTEGER,
   WasRecentlyRemovedFromAddressbook INTEGER,
   DefaultEphemeralMessagesDurationSecs INTEGER,
   DefaultEphemeralMessagesDurationLastChangedTime INTEGER,
   LastUsyncTime INTEGER
)

```

### WaScheduledTasks

```sql
CREATE TABLE WaScheduledTasks
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
)

```

### metadata

```sql
CREATE TABLE metadata(version int)

```

### sqlite_stat1

```sql
CREATE TABLE sqlite_stat1(tbl,idx,stat)

```

## messages.dec.db

### AddonOrphans

```sql
CREATE TABLE AddonOrphans
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
)

```

### AdvUserInfos

```sql
CREATE TABLE AdvUserInfos
(
   DbUserJid TEXT PRIMARY KEY,
   Timestamp INTEGER,
   RawId INTEGER,
   CurrentIndex INTEGER,
   ExpectedTs INTEGER,
   ExpectedTsLastDeviceJobTs INTEGER,
   ExpectedTsUpdateTs INTEGER
)

```

### ContactVCards

```sql
CREATE TABLE ContactVCards
(
   VCardId INTEGER PRIMARY KEY,
   Jid TEXT,
   MessageId INTEGER
)

```

### ContextSettings

```sql
CREATE TABLE ContextSettings
(
   ContextKey INTEGER PRIMARY KEY,
   ContextValue BLOB
)

```

### Conversations

```sql
CREATE TABLE Conversations
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
)

```

### DanglingDeliveryReceipts

```sql
CREATE TABLE DanglingDeliveryReceipts
(
   DeliveryReceiptId INTEGER PRIMARY KEY,
   Data BLOB
)

```

### DeletedTemplateButtonReplyMessages

```sql
CREATE TABLE DeletedTemplateButtonReplyMessages
(
   Id INTEGER PRIMARY KEY,
   KeyRemoteJid TEXT,
   KeyFromMe INTEGER,
   KeyId TEXT,
   SelectedIndex INTEGER
)

```

### DeviceCapabilities

```sql
CREATE TABLE DeviceCapabilities
(
   RecordId INTEGER PRIMARY KEY,
   DbDeviceJid TEXT,
   ChatLockSupport INTEGER,
   Protobuf BLOB
)

```

### DevicesOwnerships

```sql
CREATE TABLE DevicesOwnerships
(
   RecordId INTEGER PRIMARY KEY,
   User TEXT,
   Device TEXT,
   DeviceVersion INTEGER,
   AdvKeyIndex INTEGER
)

```

### EmojiSelectedIndexes

```sql
CREATE TABLE EmojiSelectedIndexes
(
   EmojiID INTEGER PRIMARY KEY,
   EmojiCode TEXT,
   Selection INTEGER
)

```

### EmojiUsages

```sql
CREATE TABLE EmojiUsages
(
   EmojiID INTEGER PRIMARY KEY,
   EmojiCode TEXT,
   UsageWeight INTEGER
)

```

### EventResponses

```sql
CREATE TABLE EventResponses
(
   ResponseId INTEGER PRIMARY KEY,
   ResponderJid TEXT,
   ParentKeyFromMe INTEGER,
   ParentKeyId TEXT,
   ParentKeyRemoteJid TEXT,
   SenderTimestampMs INTEGER,
   RsvpType INTEGER
)

```

### Events

```sql
CREATE TABLE Events
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
)

```

### FrequentChatScores

```sql
CREATE TABLE FrequentChatScores
(
   ID INTEGER PRIMARY KEY,
   Jid TEXT,
   DefaultScore INTEGER,
   ImageScore INTEGER,
   VideoScore INTEGER
)

```

### GroupParticipants

```sql
CREATE TABLE GroupParticipants
(
   GroupParticipantStateId INTEGER PRIMARY KEY,
   GroupJid TEXT,
   MemberJid TEXT,
   Flags INTEGER,
   DevicesNeedingSenderKey BLOB,
   DevicesWithSenderKey BLOB
)

```

### HistorySyncChunkStatuses

```sql
CREATE TABLE HistorySyncChunkStatuses
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
)

```

### InactiveReceipts

```sql
CREATE TABLE InactiveReceipts
(
   InactiveReceiptId INTEGER PRIMARY KEY,
   DbChatJid TEXT,
   DbParticipantJid TEXT,
   KeyId TEXT,
   TimestampUtc INTEGER
)

```

### JidInfos

```sql
CREATE TABLE JidInfos
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
)

```

### KeepInChatMessages

```sql
CREATE TABLE KeepInChatMessages
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
)

```

### LabelConversations

```sql
CREATE TABLE LabelConversations
(
   RecordId INTEGER PRIMARY KEY,
   LabelId INTEGER,
   Jid TEXT
)

```

### LabelMessages

```sql
CREATE TABLE LabelMessages
(
   RecordId INTEGER PRIMARY KEY,
   LabelId INTEGER,
   MessageId INTEGER
)

```

### Labels

```sql
CREATE TABLE Labels
(
   LabelId INTEGER PRIMARY KEY,
   Name TEXT,
   Color INTEGER,
   PredefinedId INTEGER
)

```

### LocalFiles

```sql
CREATE TABLE LocalFiles
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
)

```

### MessageMiscInfos

```sql
CREATE TABLE MessageMiscInfos
(
   ID INTEGER PRIMARY KEY,
   MessageId INTEGER,
   ErrorCode INTEGER,
   BackgroundId TEXT,
   TargetFilename TEXT,
   AlternateUploadUri TEXT,
   ImageBinaryInfo BLOB,
   TranscoderData BLOB
)

```

### Messages

```sql
CREATE TABLE Messages
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
)

```

### MessagesFts

```sql
CREATE VIRTUAL TABLE MessagesFts USING fts5(content='MessagesHelperViewForFts', content_rowid=MessageID, KeyRemoteJid UNINDEXED, Data, MediaName, MediaCaption, LocationDetails, Tags, prefix=2, tokenize='unicode61')

```

### MessagesFts_config

```sql
CREATE TABLE 'MessagesFts_config'(k PRIMARY KEY, v) WITHOUT ROWID

```

### MessagesFts_data

```sql
CREATE TABLE 'MessagesFts_data'(id INTEGER PRIMARY KEY, block BLOB)

```

### MessagesFts_docsize

```sql
CREATE TABLE 'MessagesFts_docsize'(id INTEGER PRIMARY KEY, sz BLOB)

```

### MessagesFts_idx

```sql
CREATE TABLE 'MessagesFts_idx'(segid, term, pgno, PRIMARY KEY(segid, term)) WITHOUT ROWID

```

### OrphanedReceipts

```sql
CREATE TABLE OrphanedReceipts
(
   OrphanedReceiptId INTEGER PRIMARY KEY,
   DbChatJid TEXT,
   KeyId TEXT,
   DbSenderJid TEXT,
   Status INTEGER,
   IsReadSelfReceipt INTEGER,
   Timestamp INTEGER
)

```

### PastParticipants

```sql
CREATE TABLE PastParticipants
(
   PastParticipantStateId INTEGER PRIMARY KEY,
   GroupJid TEXT,
   MemberJid TEXT,
   LeaveTime INTEGER,
   LeaveReason INTEGER
)

```

### PeerMessages

```sql
CREATE TABLE PeerMessages
(
   PeerMessageDataId INTEGER PRIMARY KEY,
   MessageKeyId TEXT,
   DeviceId INTEGER,
   MsgType INTEGER,
   Status INTEGER,
   Data BLOB
)

```

### PendingMessages

```sql
CREATE TABLE PendingMessages
(
   PendingMessagesId INTEGER PRIMARY KEY,
   KeyRemoteJid TEXT,
   KeyId TEXT,
   Timestamp INTEGER,
   ProtobufMessage BLOB,
   RemoteResource TEXT,
   PendingMsgPropertiesProtobuf BLOB
)

```

### PersistentActions

```sql
CREATE TABLE PersistentActions
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
)

```

### PinInChatMessages

```sql
CREATE TABLE PinInChatMessages
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
)

```

### PlaceHolderReceipts

```sql
CREATE TABLE PlaceHolderReceipts
(
   CipherTextReceiptId INTEGER PRIMARY KEY,
   KeyRemoteJid TEXT,
   ParticipantJid TEXT,
   KeyId TEXT,
   IsCipherText INTEGER,
   IsMdPlaceholder INTEGER
)

```

### PollVotes

```sql
CREATE TABLE PollVotes
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
)

```

### PollVotesOptions

```sql
CREATE TABLE PollVotesOptions
(
   RecordId INTEGER PRIMARY KEY,
   PollVoteId INTEGER,
   VoteId INTEGER
)

```

### PostponedReceipts

```sql
CREATE TABLE PostponedReceipts
(
   PostponedReceiptId INTEGER PRIMARY KEY,
   TargetJid TEXT,
   ParticipantJid TEXT,
   KeyId TEXT,
   TimestampLong INTEGER
)

```

### QuickReplies

```sql
CREATE TABLE QuickReplies
(
   QuickReplyId TEXT PRIMARY KEY,
   Shortcut TEXT,
   Message TEXT,
   Count INTEGER
)

```

### Reactions

```sql
CREATE TABLE Reactions
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
)

```

### ReceiptState

```sql
CREATE TABLE ReceiptState
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
)

```

### RevokeResendExtraDevicesForMsgs

```sql
CREATE TABLE RevokeResendExtraDevicesForMsgs
(
   RevokeResendMissingId INTEGER PRIMARY KEY,
   MessageId INTEGER,
   DbDeviceJids TEXT
)

```

### ServerSyncVersions

```sql
CREATE TABLE ServerSyncVersions
(
   Collection TEXT PRIMARY KEY,
   Version INTEGER,
   LtHash BLOB
)

```

### Stickers

```sql
CREATE TABLE Stickers
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
)

```

### SyncDMutations

```sql
CREATE TABLE SyncDMutations
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
)

```

### SyncDPendingMutations

```sql
CREATE TABLE SyncDPendingMutations
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
)

```

### WaScheduledTasks

```sql
CREATE TABLE WaScheduledTasks
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
)

```

### WaStatuses

```sql
CREATE TABLE WaStatuses
(
   StatusId INTEGER PRIMARY KEY,
   MessageId INTEGER,
   MessageKeyId TEXT,
   Jid TEXT,
   Timestamp INTEGER,
   IsViewed INTEGER,
   IsChecked INTEGER
)

```

### metadata

```sql
CREATE TABLE metadata(version int)

```

### sqlite_sequence

```sql
CREATE TABLE sqlite_sequence(name,seq)

```

### sqlite_stat1

```sql
CREATE TABLE sqlite_stat1(tbl,idx,stat)

```