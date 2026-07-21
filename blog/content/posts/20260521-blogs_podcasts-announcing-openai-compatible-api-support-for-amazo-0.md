---
title: Announcing OpenAI-compatible API support for Amazon SageMaker AI endpoints
  | Amazon Web Services
date: 2026-05-21 04:06:47+08:00
draft: false
entry_kind: auto
tags:
- 博客与播客
- AI Agent
- 大语言模型
- Python
- Docker
categories:
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
- 云原生/容器
source: blogs_podcasts
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://aws.amazon.com/blogs/machine-learning/announcing-openai-compatible-api-support-for-amazon-sagemaker-ai-endpoints
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:41cfc9b60963e39eba9a5888f2d8e8b6aa322caa956ee90ee9b527db1eca6e53
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 96
captured_at: '2026-07-18T04:21:28.670452Z'
source_capture_sha256: sha256:2e904831a23a75a2ed7d021e15c888a3af985fbc693cacac49265a3d6d1d336e
source_capture_chars_original: 5384
source_publication_excerpt_chars: 711
source_truncation_reason: historical_capture_limit,historical_publication_excerpt_limit
observation_id: obs_0eceb2b55eb6f2bb4a890c4d04e11f8ffdedda16748e95d8a3ed3af5e1fde0d7
revision_id: rev_ad9f6d9f5ff24e77d7eba3c9dcfbe927d20537006a3efcc74ca59f26580815a6
event_id: evt_7d76913688978d70bf36506ce94feff9e4035065d38905aea4aa67f142f682ee
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: blogs\_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/announcing-openai-compatible-api-support-for-amazon-sagemaker-ai-endpoints](<https://aws.amazon.com/blogs/machine-learning/announcing-openai-compatible-api-support-for-amazon-sagemaker-ai-endpoints>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> Today, Amazon SageMaker AI introduces OpenAI-compatible API support for real-time inference endpoints. If you use the OpenAI SDK, LangChain, or Strands Agents, you can now invoke models on SageMaker AI by changing only your endpoint URL. You don’t need a custom client, a SigV4 wrapper, or code rewrites.
>
> With this launch, SageMaker AI endpoints expose an /openai/v1 path that accepts Chat Completions requests and returns responses as is from the container, including streaming. OpenAI endpoints are turned on for all endpoints and inference components using standard SageMaker AI APIs and SDK.
>
> SageMaker AI routes based on the endpoint name in the URL, so any OpenAI-compatible client works out of the box.…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
