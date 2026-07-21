---
title: AI大模型小白手册｜Embedding 与向量数据库
date: 2026-03-05 22:28:24+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- Python
- 数据库
categories:
- 数据
scenarios: []
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7613594282119479315
aliases:
- /posts/20260306-juejin-ai大模型小白手册embedding-与向量数据库-2/
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:66d3e553756a79608c2bedb6c5d8550b46cfb26d43f82d4fc4fdef947d830d10
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 26
captured_at: '2026-07-18T04:18:36.387221Z'
source_capture_sha256: sha256:e4a69aa9eb44e4d00dfa5ad5584d7e5920027371d3fe2eaa69813a01c2b2f5ac
source_capture_chars_original: 5761
source_publication_excerpt_chars: 786
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_2c3e277c118ef34cbc5d2fcdead5a9c26913c6a34388545462202936b6c30214
revision_id: rev_0228f0212664e691130aa8f8575e6ec4f2aea16d4b95bdcd6f22d33bbff1c993
event_id: evt_21effd067f6a5d5e75901c8c3ce90d543898e60dca295c12156c8b0eb2cfcdae
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-03-05T14:28:24Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7613594282119479315](<https://juejin.cn/post/7613594282119479315>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 前言
> 在人工智能快速发展的今天，大模型虽能理解并生成人类语言，却高度依赖外部工具来高效处理和检索海量信息。其中，
> Embedding（嵌入）
> 技术将文本、图像等复杂数据转化为计算机可计算的向量，而
> 向量数据库
> 则专门用于存储和快速检索这些高维向量，从而实现语义级别的相似性匹配。这两项技术共同构成了现代AI应用如智能问答、推荐系统和知识库检索的基石。
> 本手册专为AI初学者设计，旨在用通俗易懂的方式讲解Embedding的基本原理、主流模型特点、向量数据库的核心功能及典型使用场景，并通过简单示例帮助你快速上手。
> 大模型系列系列目录（持续更新）：
> AI大模型小白手册｜基础原理篇
> AI大模型小白手册 | API调用的魔法指南
> AI大模型小白手册｜如何像工程师一样写Prompt？
> 一、为什么我们需要“Embedding”？
> 想象一下，你正在做一个酒店推荐网站。用户看了“希尔顿西雅图机场酒店”，你想给他推荐风格、描述最相似的其他酒店。但问题是：
> 酒店没有“标签”，只有文字描述（比如：“靠近机场，安静舒适，免费WiFi”）。
> 计算机看不懂文字，它只懂数字！
> 这时候，我们就需要一种方法：把文字变成数字向量，而且要保证意思相近的文字，对应的向量也靠得很近。这个过程，就叫 Embedding（嵌入）。
> Embedding的本质
> Embedding 的本质就是：
> 将一个我们人类或计算机难以直接处理的事物（比如一个单词“苹果”、一张图片、一段视频），通过某种数学方法，强行将其“嵌入”到一个多维度的数学空间中，变成一个由一系列数字组成的“坐标”（向量）
> 或者简单说：
> Embedding 就是把现实中的东西转换成一串固定长度的数字，让计算机能“理解”它们的含义和关系。
> 这个“坐标”的神奇之处在于：
> 1.它保留了“语义”信息：坐标里的每个维度，都代表了该事物的某种潜在特征。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
