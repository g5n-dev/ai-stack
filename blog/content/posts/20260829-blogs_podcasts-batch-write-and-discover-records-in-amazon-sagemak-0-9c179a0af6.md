---
title: "Batch write and discover records in Amazon SageMaker Feature Store"
date: 2026-08-29T10:14:23+08:00
draft: false
entry_kind: "auto"
tags: ["生成式 AI", "机器学习", "Amazon Machine Learning", "Amazon SageMaker AI", "Announcements", "Artificial Intelligence", "Intermediate (200)", "Technical How-to"]
categories: []
source: "blogs_podcasts"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:2ea6083d287739122445551f94ba462c66bf0e7011b1c86e3728db2a312c9ac2"
source_payload_sha256: "sha256:67a50aab1219e2ff3145f83fa52581081d0f8fb4017daba2307b915ddab52679"
observation_id: obs_9c179a0af67d39a7b30ee5b96d2a545b4f735b192f9bf86803afdd3d217082eb
event_id: evt_404b82defaee7679ecf342426a3007256b7c76b848a863c50fcb091be821ad0d
revision_id: rev_e70c59a861022c5214b3b4be95f8ea62fb80408421817551e93cb34c90302771
source_published_at: 2026-08-28T19:31:05Z
first_seen_at: 2026-08-29T02:22:56Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 66
description: "当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。"
external_url: https://aws.amazon.com/blogs/machine-learning/batch-write-and-discover-records-in-amazon-sagemaker-feature-store
parent_observation_id: null
last_seen_at: 2026-09-01T00:00:00Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/batch-write-and-discover-records-in-amazon-sagemaker-feature-store](https://aws.amazon.com/blogs/machine-learning/batch-write-and-discover-records-in-amazon-sagemaker-feature-store)
- **发布域名**: aws.amazon.com

## 来源摘要/节选

> Amazon SageMaker Feature Store is a fully managed, purpose-built repository to store, share, and manage features for machine learning (ML) models. It provides low-latency online serving for real-time inference, an offline store for historical retention and training feature data, and supports both streaming and batch ingestion patterns.
>
> As ML platforms mature, two operational gaps surface repeatedly. First, teams running high-throughput feature pipelines must call PutRecord (which writes a single feature record to the online store) in a loop. This means one API call per record, per feature group, which creates connection overhead and poor throughput. A fraud-detection pipeline ingesting 10,000 records per second across five feature groups must sustain 50,000 individual API calls per second only to keep features current. A second challenge is that teams using the In-Memory storage tier have no way to browse or enumerate records stored in the online store. If record identifiers are lost through a bug or pipeline failure, those records become permanently unrecoverable. There is no offline store for the In-Memory tier to fall back on, no Amazon Athena query to run, and no API to discover what exists.
>
> Today, we are announcing two new APIs for Amazon SageMaker Feature Store:
>
> BatchWriteRecord — Write up to 25 records across multiple feature groups in a single API call, with partial-success semantics, per-record time-to-live (TTL) control, and the same EventTime-based ordering guarantees as PutRecord.
>
> ListRecords — Enumerate record identifiers within a feature group using pagination. Works with both Standard (Amazon DynamoDB-backed) and In-Memory (Redis-backed) storage tiers.
>
> In this post, we walk through each API with code examples you can use to get started.
>
> Prerequisites
>
> To follow along with the examples in this post, you need:
>
> An AWS account with permissions to create Amazon SageMaker AI resources.
>
> An Amazon SageMaker AI execution role with access to Amazon Simple Storage Service (Amazon S3) and AWS Glue, and permissions to interact with Feature Store data plane APIs. The following AWS Identity and Access Management (IAM) policy shows the minimum required permissions:
>
> {
>
> "Version": "2012-10-17",
>
> "Statement": [
>
> {
>
> "Effect": "Allow",
>
> "Action": [
>
> "sagemaker:BatchWriteRecord",
>
> "sagemaker:PutRecord",
>
> "sagemaker:ListRecords"
>
> ],
>
> "Resource": "arn:aws:sagemaker:*:*:feature-group/*"
>
> }
>
> ]
>
> }
>
> Boto3 (latest version) or SageMaker Python SDK v3.8.0 or later.
>
> One or more existing feature groups with records ingested (if you are new to Feature Store, see the end-to-end workshop notebook).
>
> BatchWriteRecord
>
> The BatchWriteRecord API tackles the throughput limits of single-record ingestion. The following sections explain the problem it solves and how it works.
>
> The challenge with single-record ingestion
>
> The existing PutRecord API in Feature Store writes one record to one feature group per call. Each call performs a conditional write: the record is persisted as the “latest” version only if its EventTime, included in the request, is newer than the existing record. If the condition fails, the record is still written as a historical version for the offline store.
>
> This design provides strong ordering guarantees, but at scale it forces an N×M calling pattern (N records × M feature groups), creating connection overhead and tail latency that limit throughput.
>
> How BatchWriteRecord works
>
> BatchWriteRecord accepts up to 25 entries in a single request, targeting one or more feature groups simultaneously. Each record succeeds or fails independently. This is a partial-success API, meaning individual record failures do not fail the entire request.
>
> The API preserves the same EventTime-based ordering as PutRecord:
>
> If the incoming record’s EventTime is newer than the existing record, it becomes the latest version in the online store.
>
> If not, the record is written as a historical version to the offline store (for feature groups with offline storage).
>
> Records that fail for other reasons (authentication/validation errors, service throttling) are returned in the response with error details and the original record.
>
> The requests that are unprocessed will be returned in response as UnprocessedEntries which can be retried.
>
> Request structure
>
> {
>
> "Entries": [
>
> {
>
> "FeatureGroupName": "click-features",
>
> "Record": [
>
> {"FeatureName": "user_id", "ValueAsString": "user-123"},
>
> {"FeatureName": "event_time", "ValueAsString": "2026-06-05T12:00:00Z"},
>
> {"FeatureName": "click_count", "ValueAsString": "42"}
>
> ],
>
> "TargetStores": ["OnlineStore", "OfflineStore"],
>
> "TtlDuration": {"Unit": "Days", "Value": 7}
>
> },
>
> {
>
> "FeatureGroupName": "login-features",
>
> "Record": [
>
> {"FeatureName": "user_id", "ValueAsString": "user-456"},
>
> {"FeatureName": "event_time", "ValueAsString": "2026-06-05T12:00:01Z"},
>
> {"FeatureName": "login_count", "ValueAsString": "18"}
>
> ],
>
> "TargetStores": ["OnlineStore", "OfflineStore"]
>
> }
>
> ]
>
> }
>
> The response returns only the records that failed:
>
> {
>
> "Errors": [
>
> {
>
> "Entry": {
>
> "FeatureGroupName": "string",
>
> "Record": [
>
> {
>
> "FeatureName": "string",
>
> "ValueAsString": "string",
>
> "ValueAsStringList": ["string"]
>
> }
>
> ],
>
> "TargetStores": ["string"],
>
> "TtlDuration": {
>
> "Unit": "string",
>
> "Value": number
>
> }
>
> },
>
> "ErrorCode": "string",
>
> "ErrorMessage": "string"
>
> }
>
> ],
>
> "UnprocessedEntries": [
>
> {
>
> "FeatureGroupName": "string",
>
> "Record": [
>
> {
>
> "FeatureName": "string",
>
> "ValueAsString": "string",
>
> "ValueAsStringList": ["string"]
>
> }
>
> ],
>
> "TargetStores": ["string"],
>
> "TtlDuration": {
>
> "Unit": "string",
>
> "Value": number
>
> }
>
> }
>
> ]
>
> }
>
> Records not listed in Errors or UnprocessedEntries succeeded. Your application should retry only the failed records using exponential backoff for retriable errors.
>
> Code example: Batch ingestion with Boto3
>
> import boto3
>
> featurestore_runtime = boto3.client("sagemaker-featurestore-runtime")
>
> response = featurestore_runtime.batch_write_record(
>
> Entries=[
>
> {
>
> "FeatureGroupName": "click-features",
>
> "Record": [
>
> {"FeatureName": "user_id", "ValueAsString": "user-123"},
>
> {"FeatureName": "event_time", "ValueAsString": "2026-06-05T12:00:00Z"},
>
> {"FeatureName": "click_count", "ValueAsString": "42"},
>
> ],
>
> "TargetStores": ["OnlineStore", "OfflineStore"],
>
> },
>
> {
>
> "FeatureGroupName": "login-features",
>
> "Record": [
>
> {"FeatureName": "user_id", "ValueAsString": "user-456"},
>
> {"FeatureName": "event_time", "ValueAsString": "2026-06-05T12:00:01Z"},
>
> {"FeatureName": "login_count", "ValueAsString": "18"},
>
> ],
>
> "TargetStores": ["OnlineStore", "OfflineStore"],
>
> },
>
> ]
>
> )
>
> if response["Errors"]:
>
> for error in response["Errors"]:
>
> print(f"Record {error['Entry']}, ErrorCode: {error['ErrorCode']} Failed: {error['ErrorMessage']}")
>
> if response["UnprocessedEntries"]:
>
> for unprocessed in response["UnprocessedEntries"]:
>
> print(f"Unprocessed: {unprocessed['FeatureGroupName']}")
>
> if not response["Errors"] and not response["UnprocessedEntries"]:
>
> print("All records written successfully.")
>
> Code example: Writing across multiple feature groups
>
> You can target multiple feature groups in a single request. Records are grouped by feature group and processed independently:
>
> featurestore_runtime = boto3.client("sagemaker-featurestore-runtime")
>
> response = featurestore_runtime.batch_write_record(
>
> Entries=[
>
> {
>
> "FeatureGroupName": "user-profile-features",
>
> "Record": [
>
> {"FeatureName": "user_id", "ValueAsString": "user-123"},
>
> {"FeatureName": "event_time", "ValueAsString": "2026-06-05T12:00:00Z"},
>
> {"FeatureName": "age", "ValueAsString": "34"},
>
> {"FeatureName": "region", "ValueAsString": "us-west-2"},
>
> ],
>
> "TargetStores": ["OnlineStore"],
>
> },
>
> {
>
> "FeatureGroupName": "click-features",
>
> "Record": [
>
> {"FeatureName": "user_id", "ValueAsString": "user-123"},
>
> {"FeatureName": "event_time", "ValueAsString": "2026-06-05T12:00:00Z"},
>
> {"FeatureName": "click_count", "ValueAsString": "42"},
>
> ],
>
> "TargetStores": ["OnlineStore", "OfflineStore"],
>
> },
>
> ]
>
> )
>
> A failure in one feature group does not affect records destined for other feature groups.
>
> TTL (Time-to-Live) support
>
> BatchWriteRecord supports TTL at three levels of precedence, shown in the following priority order:
>
> Record-level TTL — Set with TtlDuration on individual entries. Takes highest priority.
>
> Request-level TTL — A default TtlDuration at the top level of the request, applied to entries without a record-level TTL.
>
> Feature-group-level TTL — The TTL configured on the feature group itself, applied when neither record-level nor request-level TTL is set.
>
> Key considerations
>
> Maximum 25 entries per request. This limit applies to the total number of entries across all feature groups in a single request.
>
> Partial-success semantics: Unlike transactional APIs, BatchWriteRecord does not roll back successful writes if some records fail. Design your retry logic to re-submit only the records returned in Errors.
>
> Similar IAM model as PutRecord: The caller must have sagemaker:BatchWriteRecord and sagemaker:PutRecord permission on the Amazon Resource Name (ARN) of each target feature group. Per-feature-group authorization is checked before processing.
>
> EventTime ordering is preserved: BatchWriteRecord uses conditional writes to maintain the same latest-record-wins semantics as PutRecord. A stale record cannot overwrite a newer one in the online store.
>
> TargetStores flexibility: Each entry can independently target OnlineStore, OfflineStore, or both (defaults to the feature group’s enabled stores), giving you fine-grained control over where each record lands.
>
> ListRecords
>
> The ListRecords API closes the gap in record discovery for both storage tiers. The following sections explain the problem it solves and how it works.
>
> The challenge with record discovery
>
> Feature Store supports PutRecord, GetRecord, and DeleteRecord, but all require the caller to know the exact record identifier. There is no API to browse or enumerate records within a feature group.
>
> For the Standard tier, the workaround is querying the offline store by using Amazon Athena. This requires offline store configuration, adds cost, and is not real-time.
>
> For the In-Memory tier, the situation is critical. There is no corresponding offline store by default. If record identifiers are lost, those records are completely unrecoverable. You cannot discover them, and you cannot delete them. This leads to phantom data, wasted storage costs, and potential compliance risks when data subjects request deletion.
>
> How ListRecords works
>
> ListRecords enumerates record identifiers within a feature group using pagination. It returns only active, non-deleted, non-expired records that are ready to be used with GetRecord or DeleteRecord.
>
> The API works with both storage tiers:
>
> Standard tier (Amazon DynamoDB): Scans the online store, returning identifier of the latest version of each record. Soft-deleted and expired records are automatically excluded.
>
> In-Memory tier (Redis): Scans keys and filters out soft-deleted records and internal system keys. Returns record identifiers extracted from key names.
>
> Request and response structure
>
> POST /FeatureGroup/{FeatureGroupName}/ListRecords
>
> Request body:
>
> Initial call
>
> {
>
> "MaxResults": 50
>
> }
>
> Or
>
> {
>
> "MaxResults": 50,
>
> "NextToken": "eyJjdXJzb3IiOi4uLn0="
>
> }
>
> Response:
>
> {
>
> "RecordIdentifiers": [
>
> "user-001",
>
> "user-002",
>
> "user-003"
>
> ],
>
> "NextToken": "eyJuZXh0IjoiLi4ufQ=="
>
> }
>
> When NextToken is absent in the response, pagination is complete.
>
> Code example: Enumerate all records in a feature group
>
> import boto3
>
> featurestore_runtime = boto3.client("sagemaker-featurestore-runtime")
>
> all_identifiers = []
>
> next_token = None
>
> while True:
>
> params = {
>
> "FeatureGroupName": "user-profile-features",
>
> "MaxResults": 100,
>
> }
>
> if next_token:
>
> params["NextToken"] = next_token
>
> response = featurestore_runtime.list_records(**params)
>
> all_identifiers.extend(response["RecordIdentifiers"])
>
> next_token = response.get("NextToken")
>
> if not next_token:
>
> break
>
> print(f"Found {len(all_identifiers)} active records.")
>
> Code example: Clean up orphaned records
>
> A common use case is identifying and deleting records that are no longer needed. This is critical for In-Memory tier feature groups, where orphaned records persist indefinitely:
>
> import boto3
>
> featurestore_runtime = boto3.client("sagemaker-featurestore-runtime")
>
> # Step 1: Enumerate all record identifiers
>
> all_ids = []
>
> next_token = None
>
> while True:
>
> params = {"FeatureGroupName": "session-features", "MaxResults": 100}
>
> if next_token:
>
> params["NextToken"] = next_token
>
> response = featurestore_runtime.list_records(**params)
>
> all_ids.extend(response["RecordIdentifiers"])
>
> next_token = response.get("NextToken")
>
> if not next_token:
>
> break
>
> # Step 2: Compare against your application's active session list
>
> active_sessions = get_active_sessions() # Your application logic
>
> orphaned = [rid for rid in all_ids if rid not in active_sessions]
>
> # Step 3: Delete orphaned records
>
> for record_id in orphaned:
>
> featurestore_runtime.delete_record(
>
> FeatureGroupName="session-features",
>
> RecordIdentifierValueAsString=record_id,
>
> EventTime="2026-06-05T12:00:00Z",
>
> )
>
> print(f"Deleted {len(orphaned)} orphaned records.")
>
> Pagination behavior
>
> Page size: Configurable through MaxResults (default 10, maximum 100).
>
> Token format: Opaque, encrypted string. Do not parse or construct tokens. Pass them through unchanged.
>
> Ordering: Results are not guaranteed to be in any particular order.
>
> Concurrent writes: If records are written or deleted during pagination, you may observe duplicates or gaps. This is documented behavior.
>
> Token scope: Tokens are tied to a specific feature group and account and cannot be reused across either.
>
> Key considerations
>
> Record identifiers only. The current release returns record identifiers without feature values. Use GetRecord or BatchGetRecord to retrieve full records for the identifiers you need.
>
> Automatic filtering. The API excludes soft-deleted records, expired records (Standard tier TTL), and internal system keys (In-Memory tier). You see only active, retrievable records.
>
> IAM permission. The caller must have sagemaker:ListRecords permission on the feature group ARN.
>
> Both tiers supported. ListRecords works identically from the caller’s perspective regardless of whether the feature group uses Standard or In-Memory storage.
>
> Putting it together
>
> These two APIs complement each other naturally. Consider a compliance workflow that verifies complete data deletion for a user across multiple feature groups:
>
> import boto3
>
> featurestore_runtime = boto3.client("sagemaker-featurestore-runtime")
>
> feature_groups = ["user-profiles", "click-history", "purchase-signals"]
>
> user_to_delete = "user-789"
>
> # Step 1: Find and delete the user across all feature groups
>
> for fg_name in feature_groups:
>
> all_ids = []
>
> next_token = None
>
> while True:
>
> params = {"FeatureGroupName": fg_name, "MaxResults": 100}
>
> if next_token:
>
> params["NextToken"] = next_token
>
> response = featurestore_runtime.list_records(**params)
>
> all_ids.extend(response["RecordIdentifiers"])
>
> next_token = response.get("NextToken")
>
> if not next_token:
>
> break
>
> if user_to_delete in all_ids:
>
> featurestore_runtime.delete_record(
>
> FeatureGroupName=fg_name,
>
> RecordIdentifierValueAsString=user_to_delete,
>
> EventTime="2026-06-05T23:59:59Z",
>
> )
>
> print(f"Deleted '{user_to_delete}' from {fg_name}")
>
> # Step 2: Log the deletion event using BatchWriteRecord
>
> featurestore_runtime.batch_write_record(
>
> Entries=[
>
> {
>
> "FeatureGroupName": "deletion-audit-log",
>
> "Record": [
>
> {"FeatureName": "request_id", "ValueAsString": "del-001"},
>
> {"FeatureName": "event_time", "ValueAsString": "2026-06-05T23:59:59Z"},
>
> {"FeatureName": "user_id", "ValueAsString": user_to_delete},
>
> {"FeatureName": "status", "ValueAsString": "completed"},
>
> {"FeatureName": "feature_groups_cleaned", "ValueAsString": "3"},
>
> ],
>
> "TargetStores": ["OnlineStore", "OfflineStore"],
>
> }
>
> ]
>
> )
>
> Cleanup
>
> To avoid ongoing charges, delete feature groups you created while following this walkthrough. For In-Memory tier feature groups, use ListRecords to enumerate records and DeleteRecord to remove them before deleting the feature group.
>
> Conclusion
>
> BatchWriteRecord and ListRecords provide key enhancements in the data plane of Amazon SageMaker Feature Store. BatchWriteRecord reduces the API call volume for high-throughput ingestion by up to 25x while preserving the EventTime-based ordering guarantees that keep your online store correct. ListRecords unlocks record discovery and lifecycle management. This is critical for In-Memory tier customers who previously had no way to enumerate or clean up their data.
>
> Together, these APIs support patterns that were previously difficult or impossible: bulk ingestion pipelines with fewer connections and lower latency, compliance workflows that can verify complete data deletion, and operational tooling that can browse feature group contents in real time.
>
> For more information, see the Feature Store documentation, the Feature Store API reference, the offline store configuration documentation, and the What’s New announcement.
>
> For background on Feature Store capabilities, explore these related posts:
>
> Understanding the Key Capabilities of Amazon SageMaker Feature Store.
>
> Accelerate ML Feature Pipelines with new capabilities in Amazon SageMaker Feature Store.
>
> Using Streaming Ingestion with Amazon SageMaker Feature Store.
>
> About the authors
>
> Harshil Shah
>
> Harshil is a Senior Solutions Architect at AWS with a deep passion for modernizing customer applications. He works with media and entertainment customers to help them build and integrate AI into their existing tech stacks.
>
> Dhaval Shah
>
> Dhaval is a Senior Solutions Architect at AWS. He works with customers to design and build production ML systems, with a focus on feature engineering, generative AI, and scalable data architectures.
>
> Chirag Pandey
>
> Chirag is a software engineer at AWS interested in building reliable and scalable infrastructure for AI/ML workloads.
>
> Siamak Nariman
>
> Siamak is a Senior Product Manager at AWS. He is focused on AI/ML technology, ML model management, and ML governance to improve overall organizational efficiency and productivity. He has extensive experience automating processes and deploying various technologies.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。