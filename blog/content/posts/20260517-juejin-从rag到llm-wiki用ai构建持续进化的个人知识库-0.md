---
title: 从RAG到LLM Wiki：用AI构建持续进化的个人知识库
date: 2026-05-17 03:38:57+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- RAG
- AI Agent
- 大语言模型
categories:
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
- RAG应用
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7640091786766598207
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:07ca2467a26ec33f03cdbbc69872d5124717f5c557fee1057359709304b5c0ba
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 29
captured_at: '2026-07-18T04:21:25.111367Z'
source_capture_sha256: sha256:74b209af895dd9258e03baccf9197614d111411a758aed345e8736c03846ce7b
source_capture_chars_original: 4025
source_publication_excerpt_chars: 795
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7640091786766598207](<https://juejin.cn/post/7640091786766598207>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 自从大模型诞生以来，我们主动或者被动接收到的信息越来越多，信息爆炸是我们每个人必须面对的问题。如果想提升自己的效率，就得从这些信息中精确筛选出有用的部分，避免自己被淹没在信息的海洋里。试想一下，比如你现在看到一篇文章，随手点了收藏，以为过后就会仔细去阅读，但是很多时候往往进了收藏夹之后就会吃灰。就算哪天真的想起来要看一下收藏夹的文章，如果收藏夹中已经有了大量的文章，且杂乱无序，这时候整理起来也费劲，往往会让人没有想看的欲望。
> 主流的个人知识库管理工具，主要还是利用了RAG的思想，即：上传文件，查询时检索片段，生成答案。这意味着每次提问，LLM都会重复执行一遍检索，然后根据上下文回答，整个过程没有积累，没有综合，更没有交叉引用。
> 一、LLM Wiki是什么
> 基本原理
> LLM WiKi是Andrej Karpathy提出的一种基于LLM构建个人知识库的设想，这种构建的思路与RAG不同。当你添加一篇新资料时，LLM不只是索引它以备后用，而是
> 阅读它、提取关键信息、并将其整合到现有 Wiki 中
> 。这个过程会不断更新实体页面、修订主题摘要、标注新旧数据的矛盾之处、强化或修改正在演化的综合分析。
> 三层架构
> LLM Wiki由三层组成：
> 1. 原始资料层 \(raw/\)
> 上传的源文档集合，可以是文章、论文、图片等形式的数据。这些是不可变的，LLM只读不改，也被称为真相来源（source of truth）。
> 2. Wiki层 \(wiki/\)
> 由LLM生成和维护的Markdown文件目录。包括摘要、实体页面、概念页面、对比分析、综述等。完全由LLM来维护这个文件目录，包括创建页面、在新资料到来时更新、维护交叉引用、保持一致性等操作。
> 3. Schema层
> 一个配置文档（如 CLAUDE.md、AGENTS.md 或 SCHEMA.md），告诉LLMWiki的结构约定、工作流程。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
