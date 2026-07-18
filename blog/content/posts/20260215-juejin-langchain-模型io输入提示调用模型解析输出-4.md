---
title: LangChain 模型I/O：输入提示、调用模型、解析输出
date: 2026-02-15 12:10:18+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- 大语言模型
- Python
categories:
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7606183276774096959
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:b0c34c75a07d36680a2c501368d6e3e80bf8597b2cdf76ef92cf3e9e1c327de0
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 30
captured_at: '2026-07-18T04:17:19.400403Z'
source_capture_sha256: sha256:5d3a3e174f546fee628b81a61fda72ade73d6c4db2cc13848ece735a4c3e8e58
source_capture_chars_original: 5443
source_publication_excerpt_chars: 613
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7606183276774096959](<https://juejin.cn/post/7606183276774096959>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 从这节课开始，我们将对 LangChain 中的六大核心组件一一进行详细的剖析。
> 模型
> 位于 LangChain 框架的最底层，它是基于语言模型构建的应用的核心元素，因为所谓 LangChain 应用开发，就是以 LangChain 作为框架，通过 API 调用大模型来解决具体问题的过程。
> 整个 LangChain 框架的逻辑都是由 LLM 这个发动机来驱动的。没有模型，LangChain 这个框架也就失去了它存在的意义
> Model I/O
> 我们可以把对模型的使用过程拆解成三块，分别是输入提示（对应图中的 Format）、调用模型（对应图中的 Predict）和输出解析（对应图中的 Parse）。这三块形成了一个整体，因此在 LangChain 中这个过程被统称为 Model I/O（Input/Output）
> 在模型 I/O 的每个环节，LangChain 都为咱们提供了模板和工具，快捷地形成调用各种语言模型的接口。
> 提示模板
> ：使用模型的第一个环节是把提示信息输入到模型中，你可以创建 LangChain 模板，根据实际需求动态选择不同的输入，针对特定的任务和应用调整输入。
> 语言模型
> ：LangChain 允许你通过通用接口来调用语言模型。这意味着无论你要使用的是哪种语言模型，都可以通过同一种方式进行调用，这样就提高了灵活性和便利性。
> 输出解析
> ：LangChain 还提供了从模型输出中提取信息的功能。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
