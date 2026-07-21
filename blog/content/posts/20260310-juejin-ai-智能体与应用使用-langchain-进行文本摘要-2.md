---
title: AI 智能体与应用——使用 LangChain 进行文本摘要
date: 2026-03-10 05:11:10+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- AI Agent
- 大语言模型
- Python
categories:
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7615147223628414991
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:6fd1ebf5e5c6f579e370d258d99a4dd93543acf139812d0bd9d3502095cbdaf9
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 30
captured_at: '2026-07-18T04:18:47.672648Z'
source_capture_sha256: sha256:559553323a2bde3260cdac1488bfe20d20d8941781002aff044496148519d95d
source_capture_chars_original: 6000
source_publication_excerpt_chars: 731
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_03cb6a8754deeac3e0e66769cbb15f7c3d5230379355314bb1ad2633e5015918
revision_id: rev_d975e0a77b38dca2bd15c7dde873764830e1d159873c766797b153a04a053b5d
event_id: evt_78688bc2cfb0b0d4d215f6cebb754525108fc4fbdaa15857e19b465d3a7f9d48
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-03-09T21:11:10Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7615147223628414991](<https://juejin.cn/post/7615147223628414991>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 本章涵盖以下内容：
> 对超过 LLM 上下文窗口的大型文档进行摘要
> 跨多份文档进行摘要
> 在第 1 章中，我们探讨了三类主要的 LLM 应用：摘要引擎、聊天机器人和 AI 智能体。在本章中，你将开始使用 LangChain 构建实用的摘要链，尤其会重点使用
> LangChain Expression Language（LCEL）
> 来处理各种真实场景。所谓
> 链（chain）
> ，就是一系列相互连接的操作序列：前一步的输出会成为后一步的输入——这种形式非常适合自动化诸如摘要这样的任务。这部分内容也将为下一章中构建一个更高级的摘要引擎打下基础。
> 摘要引擎对于自动化处理海量文档摘要至关重要。即使借助 ChatGPT 之类的工具，如果完全手工完成这类工作，也会既不现实、又成本高昂。以摘要引擎作为 LLM 应用开发的切入点，是一种非常务实的做法：它不仅能为后续更复杂的项目提供坚实基础，也能很好地展示 LangChain 的能力，而这些能力我们将在后续章节中继续深入。
> 在正式开始构建之前，我们会先看几种不同的摘要技术。它们分别适用于特定场景，包括大型文档、内容汇总，以及结构化数据处理等。你在第 2 章中已经通过
> PromptTemplate
> 练习过对小文档做摘要，因此这里我们将跳过那部分，直接聚焦更复杂的示例。
> 3.1 对大于上下文窗口的文档进行摘要
> 正如第 1 章提到的，每个 LLM 都有一个提示大小上限，也就是所谓的
> 上下文窗口（context window）
> 。虽然主流 LLM 的上下文窗口一直在增大，但你仍然可能遇到这样的情况：某份文档的长度超过了你所选模型的 token 限制。在这种情况下，你可以使用
> MapReduce
> 方法，如图 3.1 所示。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
