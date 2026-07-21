---
title: RAG 系列（十二）：高级分块策略——Parent-Child 与 Contextual Retrieval
date: 2026-05-10 03:23:34+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- RAG
- 大语言模型
- Python
categories:
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
- RAG应用
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7637839076003659827
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:ed983029dc8dc5b4acebf0f72f7a8b77752fd6acb4e2685bb9ffaa8037db4057
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 54
captured_at: '2026-07-18T04:19:50.626752Z'
source_capture_sha256: sha256:81214ab83f970ef4fa30378be88f8005d186cc58ca96ddc33bbaf61926a9843b
source_capture_chars_original: 5392
source_publication_excerpt_chars: 564
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_b9fda635f6707a40b921345f3012b6e5992b8893f6c0fe025a9b1e0ee249e8f7
revision_id: rev_f14c0ea8cc47a9ebcbebd1c9e1681c9dca8faf7d308a9de346db7b9290a73cb4
event_id: evt_a1379bcdac5349fe61aeb8f28676be0f657d7b93f42105b6cbb3107c4d7e7ac8
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-05-09T19:23:34Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7637839076003659827](<https://juejin.cn/post/7637839076003659827>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 分块的两难困境
> RAG 系统里有一个经典矛盾：
> Chunk 太小
> ：向量匹配精准，但返回给 LLM 的内容是片段，缺乏上下文，无法完整回答问题
> Chunk 太大
> ：内容完整，但语义太分散，embedding 质量下降，检索命中率降低
> 这不是调参能解决的问题，而是 Naive 分块的结构性缺陷。
> 小块适合检索，大块适合生成
> ——这两个需求本来就是矛盾的，用同一个尺寸的 chunk 同时满足两者，必然顾此失彼。
> 本篇介绍两种突破这一困境的方案：
> Parent-Child Chunking
> ：用小块做检索，命中后返回对应的大块
> Contextual Retrieval
> （Anthropic 方案）：给每个 Chunk 加上文档上下文描述，让 embedding 更"聪明"
> Parent-Child Chunking
> 核心思路
> 索引阶段：
>   父文档（
> 800
> 字）→ 存储在 docstore（InMemoryStore）
>   ↓ 切割
>   子 Chunk（
> 200
> 字）→ 存入向量库
>
> 检索阶段：
> query
> → 向量检索匹配子 Chunk（精准）
>   → 找到子 Chunk 对应的父文档
>   → 返回父文档给 LLM（完整）
> 检索用的是小 chunk，LLM 拿到的是大 chunk。两个需求，各自最优，互不干扰。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
