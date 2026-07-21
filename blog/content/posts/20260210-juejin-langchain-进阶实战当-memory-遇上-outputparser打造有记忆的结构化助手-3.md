---
title: LangChain 进阶实战：当 Memory 遇上 OutputParser，打造有记忆的结构化助手
date: 2026-02-10 21:20:19+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- AI Agent
- 大语言模型
- JavaScript
- Docker
categories:
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
- 云原生/容器
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7605051978872078355
aliases:
- /posts/20260211-juejin-langchain-进阶实战当-memory-遇上-outputparser打造有记忆的结构化助手-3/
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:74dba836cc6cb2610953d42e0e7a34b5a03017501cd43fb2aeb1ec1df7484d4b
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 51
captured_at: '2026-07-18T04:17:09.242523Z'
source_capture_sha256: sha256:6f6cfdb481174b0940055454d7d158a6974d378422001db2241bad054866a830
source_capture_chars_original: 4902
source_publication_excerpt_chars: 785
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_30d3dac7086db4f236faec29f1e0a57e8cc95630dd2827b981966de2025fca1f
revision_id: rev_b69f43c479b8dd21c8de595b99e328e473bfa0553e870692d947d3eea45c4945
event_id: evt_8596500aaf27d16fe71a3a0ad62c76d6c38932a0ca08b0110df188958ece37c3
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-10T13:20:19Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7605051978872078355](<https://juejin.cn/post/7605051978872078355>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 在当前的 LLM 应用开发中，我们经常陷入两个极端的场景：
> 记性好的话痨
> ：类似于 ChatBot，能记住上下文，聊天体验流畅，但输出全是不可控的自然语言。
> 一次性的 API
> ：类似于信息提取工具，能返回标准的 JSON 数据，但它是“无状态”的，每一轮调用都是全新的开始。
> 然而，在复杂的业务系统中，我们往往需要二者兼备：
> 既要像人一样拥有记忆上下文的能力，又要像传统 API 一样返回严格的结构化数据（JSON）。
> 本文将基于 LangChain \(LCEL\) 体系，讲解如何将
> Memory \(记忆模块\)
> 与
> OutputParser \(输出解析器\)
> 结合，打造一个既懂业务逻辑又能规范输出的智能助手。
> 第一部分：记忆的载体 \(Review\)
> 我们在之前的工程实践中已经明确：LLM 本身是无状态的（Stateless）。为了维持对话的连续性，我们需要在应用层手动维护历史消息。
> 在 LangChain 中，RunnableWithMessageHistory 是实现这一功能的核心容器。它的工作原理非常直观：
> 读取
> ：在调用大模型前，从存储介质（Memory）中读取历史对话。
> 注入
> ：将历史对话填充到 Prompt 的占位符（Placeholder）中。
> 保存
> ：模型返回结果后，将“用户输入”和“AI 回复”追加到 Memory 中。
> 这是让 AI “拥有记忆”的基础设施。
> 第二部分：输出的规整 \(The Parser\)
> 模型原生的输出是 BaseMessage 或纯文本字符串。直接在业务代码中使用 JSON.parse\(\) 处理模型输出是非常危险的，原因如下：
> 幻觉与废话
> ：模型可能会在 JSON 前后添加 "Here is your JSON" 之类的自然语言。
> 格式错误
> ：Markdown 代码块符号（\`\`\`json）会破坏 JSON 结构。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
