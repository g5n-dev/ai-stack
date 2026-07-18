---
title: 用 SQL 调大模型？Hologres + 百炼，让数据开发直接“对话”AI
date: 2026-03-03 11:19:12+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- RAG
- 大语言模型
- Python
- 数据库
categories:
- 大模型
- 数据
scenarios:
- AI/ML项目
- 大语言模型
- RAG应用
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7612852020014661632
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:fdb5df48a3877d85243ad8bfe7266febe9864d3a41c10ed671ee4a6e65d85655
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 38
captured_at: '2026-07-18T04:18:31.079399Z'
source_capture_sha256: sha256:99f6459ecc93570cee74b18be1cdca47944d55ffc6762388950947cd457074db
source_capture_chars_original: 3987
source_publication_excerpt_chars: 786
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7612852020014661632](<https://juejin.cn/post/7612852020014661632>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 在数据团队的日常中，你是否也常听到这样的声音：
> “能不能让我用自然语言问数据？”
> “这个 PDF 合同里有没有风险条款？”
> “帮我检查下这个货架排放是否和规划一致。”
> 作为数据开发者，我们熟悉 SQL、数仓分层、ETL 流程，但面对这些需求，往往只能无奈摇头——因为它们背后是大模型、多模态、向量检索等“AI 工程”的地盘。而搭建一套 RAG 系统？那意味着 GPU 集群、LangChain、FastAPI、向量数据库……技术栈陡增，运维成本飙升。
> 但今天，我想告诉你：这些场景，其实用 SQL 就可以解决。
> 阿里云 Hologres 深度集成百炼大模型平台，推出 AI Function 能力——无需 Python，无需额外服务，用你熟悉的 SQL，直接调用大模型，实现从结构化数据到图片、PDF、视频的全模态智能分析。
> 为什么是 Hologres + 百炼？
> 传统 AI 方案存在三大痛点，而 Hologres + 百炼给出了精准解法：
> 1. AI 与数据割裂：
> 数据在数仓，模型在外网，来回搬运不仅慢，还存在安全风险。
> → Hologres 让模型“走进”数据，推理就在数据旁完成，数据不出库。
> 2. 工程成本高：
> 自建 LLM 服务需 GPU、API 网关、限流熔断……数据团队难以维护。
> → 百炼提供托管式大模型服务，Hologres 通过函数一键调用，零运维。
> 3. 技术栈不匹配：
> SQL 开发者不会写 LangChain，算法工程师不懂数仓分层。
> → 用 SQL 编排 AI 逻辑，让数据团队主导端到端 AI 应用。
> 百炼是什么？能为数据开发带来什么？
> 百炼是阿里云推出的一站式大模型开发与应用构建平台，集成了千问（Qwen）、DeepSeek、Kimi 等主流模型，支持文本生成、多模态理解（如 Qwen-VL）、Embedding、翻译等多种能力。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
