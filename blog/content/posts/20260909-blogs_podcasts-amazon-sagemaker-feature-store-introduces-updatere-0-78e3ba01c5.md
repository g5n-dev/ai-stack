---
title: "Amazon SageMaker Feature Store introduces UpdateRecord for feature-level writes"
date: 2026-09-09T02:43:01+08:00
draft: false
entry_kind: "auto"
tags: ["生成式 AI", "机器学习", "Amazon Machine Learning", "Amazon SageMaker AI", "Announcements", "Artificial Intelligence", "Intermediate (200)", "Technical How-to"]
categories: []
source: "blogs_podcasts"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:4520ca2049af9e7c3f0ded8eb36dfbd31bff5490f08c2f5c6373b38e2c2570ec"
source_payload_sha256: "sha256:a006874310098ea1cf6cbc1f4e7f86fb2978ac39e7f96cd3bf58349362dfc518"
observation_id: obs_78e3ba01c51c635935b63f3b8f4fc27b0604adf8969e087a04f36cbabadc307f
event_id: evt_7b547ecff6b256282da4c1920d2ce2d1f00819b39a7a769683b82e96fe97ed43
revision_id: rev_5d582ecb1d9e78d1608d2ea043df65f6e1f95f114fb8bf3643fce6e52e20d7c1
source_published_at: 2026-09-08T18:29:15Z
first_seen_at: 2026-09-08T18:53:36Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 79
description: "当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。"
external_url: https://aws.amazon.com/blogs/machine-learning/amazon-sagemaker-feature-store-introduces-updaterecord-for-feature-level-writes
parent_observation_id: null
last_seen_at: 2026-09-10T00:00:00Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/amazon-sagemaker-feature-store-introduces-updaterecord-for-feature-level-writes](https://aws.amazon.com/blogs/machine-learning/amazon-sagemaker-feature-store-introduces-updaterecord-for-feature-level-writes)
- **发布域名**: aws.amazon.com

## 来源摘要/节选

> We are excited to announce feature-level writes for Amazon SageMaker Feature Store. Amazon SageMaker Feature Store is a fully managed, purpose-built repository to store, share, and manage machine learning (ML) features, the processed data used for training models and generating predictions. With the new UpdateRecord API, you can now update one or more feature values in a single call without reading or rewriting the entire record. This capability is available for both the Standard (Amazon DynamoDB-backed) and In-Memory (Amazon ElastiCache-backed) online store tiers.
>
> The challenge: Full-record writes for every change
>
> A Feature Group is a logical collection of features that are related, and are used by one or more ML models to either train a new model or generate inference predictions. Until now, updating even a single feature value in a feature group required a full read-modify-write cycle using PutRecord. If your fraud-scoring pipeline needed to refresh a customer’s risk_score, your application had to:
>
> Read the complete record (all features) by using GetRecord.
>
> Merge the new value in application code.
>
> Write the entire record back with PutRecord.
>
> This pattern added extra latency per update, consumed unnecessary read capacity, and introduced race conditions when multiple pipelines concurrently updated different features in the same record. In the worst case, one pipeline’s write could silently overwrite another’s. This is a classic lost-update problem.
>
> Beyond latency and correctness issues, the read-modify-write pattern also carries a cost overhead. The additional GetRecord calls required before each write generate extra Read Capacity Units (RCUs) charges. For customers operating at scale with wide feature groups and high update frequencies, these costs add up quickly.
>
> Introducing UpdateRecord
>
> The UpdateRecord API call removes the read-modify-write cycle. You provide only the features that you want to change, and Amazon SageMaker Feature Store applies the updates atomically to the existing record. Features you don’t include in the request are preserved as-is.
>
> UpdateRecord API data flow
>
> The following diagram illustrates how the UpdateRecord API processes a partial write request and synchronizes with the offline store.
>
> Figure 1: UpdateRecord API data flow to the online and offline stores
>
> The client application calls the UpdateRecord API with only the changed features. The Feature Store service validates AWS Identity and Access Management (IAM) permissions, checks EventTime ordering to reject stale writes, and performs an atomic merge. The blue arrow represents the single operation that writes only the changed features to the online store. Meanwhile, a full record snapshot is automatically replicated to the offline store to keep training datasets accurate. Multiple pipelines (clickstream, purchases, scoring) each write their own features independently to the same record. No coordination is needed.
>
> Request shape
>
> POST /FeatureGroup/{FeatureGroupName}/Record
>
> {
>
> "RecordIdentifierValueAsString": "user_123",
>
> "Features": [
>
> { "FeatureName": "risk_score", "ValueAsString": "0.87" },
>
> { "FeatureName": "last_login", "ValueAsString": "2026-07-21T08:15:00Z" }
>
> ],
>
> "TtlDuration": { // optional
>
> "Unit": "Days",
>
> "Value": 30
>
> }
>
> }
>
> FeatureGroupName — the target feature group.
>
> RecordIdentifierValueAsString — the primary key of the record to update. The record must already exist (UpdateRecord is not an upsert).
>
> Features — a list of one or more feature values to set. Up to 100 features per call.
>
> TtlDuration (optional) — override or set a per-record time-to-live (TTL). If provided, EventTime must also be present.
>
> Updating EventTime: To also update the EventTime (one of two required fields) stored with the record, provide a new value in the Features parameter list. For the update to persist, this EventTime must be newer (a later timestamp) than the existing EventTime stored for the record. Otherwise, the entire update record call is rejected with an HTTP 409 error.
>
> For more Error details, refer to this documentation.
>
> Things to know: New storage format Standard_V2
>
> The Amazon SageMaker Feature Store online storage has traditionally offered two tiers, each with its own backend storage provider. Standard Tier is backed by Amazon DynamoDB, and the In-Memory Tier is backed by Amazon ElastiCache (Redis OSS). There is now a new storage format for the Standard Tier named Standard_V2. This represents a different serialization format that supports additional capabilities such as feature-level writes.
>
> Note: If using the In-Memory tier, no new storage type is needed and feature-level writes work on all existing In-Memory feature groups out of the box.
>
> Using feature-level writes with the Standard Tier will require the new Standard_V2 storage format. You opt in at feature group creation time with this syntax:
>
> import boto3
>
> sm = boto3.client("sagemaker")
>
> sm.create_feature_group(
>
> FeatureGroupName="user-profile-fg",
>
> RecordIdentifierFeatureName="user_id",
>
> EventTimeFeatureName="event_time",
>
> OnlineStoreConfig={
>
> "EnableOnlineStore": True,
>
> "StorageType": "Standard_V2" # enables feature-level writes
>
> },
>
> FeatureDefinitions=[
>
> {"FeatureName": "user_id", "FeatureType": "String"},
>
> {"FeatureName": "event_time", "FeatureType": "String"},
>
> {"FeatureName": "risk_score", "FeatureType": "Fractional"},
>
> {"FeatureName": "last_login", "FeatureType": "String"},
>
> {"FeatureName": "balance", "FeatureType": "Fractional"},
>
> ],
>
> )
>
> Migrating existing feature groups from Standard to Standard_V2
>
> If you already have feature groups on the original Standard storage type, you can migrate to Standard_V2 to benefit from feature-level writes and maintain the same capabilities from Standard tier. The following sections describe two migration strategies. Your choice depends on your sensitivity to downtime, your preferred migration timing, and whether you want the option to roll back.
>
> Strategy A: Bulk migration with Feature Processor
>
> Use the Feature Processor SDK to read records from the existing Standard feature group and re-ingest them into a new Standard_V2 feature group.
>
> Pros: You control the timing. The original feature group stays intact during migration. Rollback is straightforward, because you switch back to the old feature group.
>
> Cons: This strategy requires a managed migration job. You pay the full read and write cost for the entire dataset upfront. You must update application clients to point to the new feature group name.
>
> Strategy B: In-place controlled switchover with UpdateFeatureGroup API
>
> Call UpdateFeatureGroup with OnlineStoreConfig.StorageType = “Standard_V2” to flip the feature group’s storage format in place:
>
> import boto3
>
> sm = boto3.client("sagemaker")
>
> sm.update_feature_group(
>
> FeatureGroupName="my-existing-fg",
>
> OnlineStoreConfig={"StorageType": "Standard_V2"}
>
> )
>
> Once the feature group is declared to be in Standard_V2 format, Calls to PutRecord or BatchWriteRecord update the underlying format to Standard_V2.
>
> This approach requires zero downtime and charges migration cost only for records that are actually touched. It preserves existing application code, because the feature group name and API endpoints remain unchanged. The switch to Standard_V2 is irreversible, and cold records that are never written linger in the legacy format until touched.
>
> Recommendation: For most customers, Strategy B (in-place UpdateFeatureGroup) is the preferred approach because of zero downtime and pay-per-touch economics. Use Strategy A only if you require a fully reversible migration path or need to rename or restructure the feature group.
>
> EventTime: Temporal ordering built in
>
> UpdateRecord supports the same EventTime-based ordering as PutRecord. When you include an EventTime in your request:
>
> If the provided EventTime is newer than or equal to the record’s current EventTime, the update is applied and the record’s EventTime advances.
>
> If the provided EventTime is earlier than the record’s current EventTime, the update is rejected with a 409 ConflictException. This helps prevent stale or out-of-order events from overwriting fresher data.
>
> When EventTime is omitted, the update applies new feature changes while the existing EventTime on the record is left unchanged. This is ideal for multi-pipeline architectures where different pipelines own different features and don’t share a single event clock.
>
> Use cases
>
> The following use cases demonstrate how UpdateRecord simplifies common feature engineering workflows.
>
> Streaming feature hydration
>
> Real-time and streaming scenarios typically require data generated by multiple streams that occur at different frequencies.
>
> Scenario: A real-time clickstream pipeline receives page_views and session_duration data every few seconds, and a nightly batch pipeline refreshes lifetime_value and customer_segment data. With UpdateRecord, each pipeline submits only the features it owns to the core record, with no coordination and no lost updates.
>
> Backfilling new features
>
> With Amazon SageMaker Feature Store, you can modify the table schema that backs the feature group to add new columns (features).
>
> Scenario: Your team adds preferred_language and notification_opt_in to an existing feature group. Instead of rewriting every record, you call UpdateRecord with only the new field values. Existing feature values remain untouched.
>
> Error correction at scale
>
> When a data science or MLOps team discovers discrepancies in existing feature data, they can now take action to correct it efficiently.
>
> Scenario: A data-quality job discovers that customer_segment is miscategorized for 50,000 records. With UpdateRecord, you can fix one field across thousands of records without risking corruption of other feature values.
>
> High-velocity feature updates
>
> Feature Groups often contain multiple fields of transactional data, even though these fields are generated or received at different times.
>
> Scenario: A fraud detection system receives transaction_velocity on every card swipe. With UpdateRecord, each write touches only the single feature that changed, which eliminates the overhead of full-record writes at scale.
>
> Multi-producer feature groups for enterprise entities
>
> Large organizations often model their Feature Store around core business entities, one feature group per entity type, with dozens of independent producers contributing features to the same records.
>
> Scenario: An enterprise maintains a single feature group per business entity (for example, customer, policy, vehicle). The group holds millions of records and hundreds of features produced by different teams, batch extract, transform, and load (ETL) jobs, streaming analytics, and real-time scoring engines. Without UpdateRecord, each producer must read the full record, inject its subset, and write back the entire entity. This creates compaction jobs, race conditions, and monthly costs in read and write operations. With UpdateRecord, each producer writes only its own features atomically, which removes the need for custom compaction solutions.
>
> Fine-grained access control
>
> UpdateRecord integrates with IAM so you can control exactly who can update which features. Two new IAM condition keys are available:
>
> sagemaker:IsUpdateRecord (Bool) — distinguish partial-update operations from full PutRecord writes.
>
> sagemaker:UpdatableFeatures (ArrayOfString) — restrict which feature names a principal is allowed to update.
>
> Example: Allow updates only to non-sensitive features
>
> {
>
> "Effect": "Allow",
>
> "Action": "sagemaker:PutRecord",
>
> "Resource": "arn:aws:sagemaker:*:*:feature-group/user-profile-fg",
>
> "Condition": {
>
> "Bool": { "sagemaker:IsUpdateRecord": "true" },
>
> "ForAllValues:StringEquals": {
>
> "sagemaker:UpdatableFeatures": ["age", "score", "last_activity"]
>
> }
>
> }
>
> }
>
> This policy allows the principal to call UpdateRecord on age, score, and last_activity but blocks updates to any other features (for example, ssn or salary) and blocks direct PutRecord calls entirely.
>
> Backward compatibility
>
> Existing IAM policies that deny sagemaker:PutRecord automatically block UpdateRecord as well. No customer migration is required for security controls to take effect.
>
> Offline store integration
>
> Updates made through UpdateRecord flow to the offline store automatically through the same replication pipeline used by PutRecord. Each update emits a complete record snapshot to the offline store, helping you maintain accurate training datasets and historical analytics.
>
> Record must exist. UpdateRecord is strictly a modify operation. Call PutRecord first to create the record.
>
> Feature names must be defined. You can’t add features that aren’t in the feature group’s schema. Use PutRecord for schema-conformant full writes.
>
> Record identifier is immutable. The primary key can’t be modified by using UpdateRecord.
>
> TTL requires EventTime. If you specify a TtlDuration, you must also include EventTime in the request.
>
> Pricing
>
> UpdateRecord follows the same pricing model as PutRecord. For the Standard tier, DynamoDB write capacity unit (WCU) charges are based on the item size after the update. However, you save on the read capacity that was previously required for the read-modify-write pattern. Consult the Amazon SageMaker Feature Store pricing page for details.
>
> Getting started today
>
> Feature-level writes with UpdateRecord is available today in all AWS Regions where Amazon SageMaker Feature Store is offered. To get started:
>
> Create a feature group with StorageType: Standard_V2 (Standard tier) or use any existing In-Memory feature group.
>
> Ingest records using PutRecord as usual.
>
> Call UpdateRecord to update individual features without rewriting the full record.
>
> For more information, see the Amazon SageMaker Feature Store Developer Guide and the UpdateRecord API Reference.
>
> Conclusion
>
> Feature-level writes with the UpdateRecord API to remove the read-modify-write cycle that previously added extra ms of latency to every partial update. UpdateRecord reduces latency, lowers data-transfer costs for single-feature updates, and helps minimize the risk of lost updates in multi-pipeline architectures.
>
> Combined with fine-grained IAM controls and automatic offline store replication, teams can build more efficient and reliable feature engineering workflows. Whether refreshing a single risk score in real time or orchestrating dozens of independent producers writing to shared enterprise-wide feature groups, UpdateRecord simplifies the path from raw data to production-ready features.
>
> To learn more, see the Amazon SageMaker Feature Store Developer Guide, the UpdateRecord API Reference, or get started on the AWS Management Console.
>
> About the authors
>
> Mona Mona
>
> Mona is a Specialist Solutions Architect at AWS, focused on machine learning infrastructure and AI/ML services. She helps customers design and optimize their ML pipelines using Amazon SageMaker.
>
> Ioan Catana
>
> Ioan is a Senior Artificial Intelligence and Machine Learning Specialist Solutions Architect at AWS. He helps customers develop and scale their ML solutions and generative AI applications in the AWS Cloud. Ioan has over 25 years of experience, mostly in software architecture design and cloud engineering.
>
> Paul Hargis
>
> Paul is a Principal Solutions Architect at AWS specializing in machine learning and data engineering. He works with enterprise customers to build scalable ML platforms.
>
> Romik Amipara
>
> Romik is a software engineer on the SageMaker Feature Store team, passionate about building elegant, scalable systems that bring big data and machine learning to people’s fingertips. His interests lie at the intersection of distributed systems and the rapidly evolving world of AI, with a focus on building reliable infrastructure that enables intelligent applications at scale.
>
> Siamak Nariman
>
> Siamak is a Senior Product Manager at AWS. He is focused on AI/ML technology, ML model management, and ML governance to improve overall organizational efficiency and productivity. He has extensive experience automating processes and deploying various technologies.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。