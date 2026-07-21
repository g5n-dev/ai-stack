---
title: Amazon SageMaker AI Async Inference now supports inline request payloads |
  Amazon Web Services
date: 2026-06-17 23:45:46+08:00
draft: false
entry_kind: auto
tags:
- 博客与播客
- Python
- Docker
categories: []
scenarios:
- 云原生/容器
source: blogs_podcasts
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://aws.amazon.com/blogs/machine-learning/amazon-sagemaker-ai-async-inference-now-supports-inline-request-payloads
aliases:
- /posts/20260618-blogs_podcasts-amazon-sagemaker-ai-async-inference-now-supports-i-0/
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:f0e9fa6a2eaa199ae88432827a6451811d77861c2f4a85975ab5a35fbd31c069
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 94
captured_at: '2026-07-18T04:21:42.990102Z'
source_capture_sha256: sha256:8f8645bde095f687a0faa5d285dbd0426515cc7196f186f3e59bd56011c92db9
source_capture_chars_original: 5778
source_publication_excerpt_chars: 766
source_truncation_reason: historical_capture_limit,historical_publication_excerpt_limit
observation_id: obs_be8678e1f85de5d3fe92e22fc1a835faa3d6742e491f975e9fdd90737d2f148b
revision_id: rev_62f452749ea47a167f91f48f25f7d349465059175936f3a14081f6134d9de7a5
event_id: evt_cc7e8e3b907db32da49f61b522b3f0192e76649eedf155ffd7b9e4fe698cdbe3
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: blogs\_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/amazon-sagemaker-ai-async-inference-now-supports-inline-request-payloads](<https://aws.amazon.com/blogs/machine-learning/amazon-sagemaker-ai-async-inference-now-supports-inline-request-payloads>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> Today, we’re announcing inline payload support for Amazon SageMaker AI Async Inference. Customers can now send inference payloads directly in the request body of the InvokeEndpointAsync API, removing the need to upload input data to Amazon Simple Storage Service \(Amazon S3\) before each invocation.
>
> For payloads up to 128,000 bytes, this removes an entire network round-trip, simplifies client-side code, and reduces the operational surface area of asynchronous inference workloads.
>
> In this post, we explain the motivation behind this feature, walk through the customer experience before and after, and show you how to start using inline payloads today.
>
> You can use Amazon SageMaker AI Async Inference to queue inference requests and process them asynchronously.…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
