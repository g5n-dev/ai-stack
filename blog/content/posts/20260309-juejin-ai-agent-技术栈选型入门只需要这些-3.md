---
title: AI Agent 技术栈选型：入门只需要这些
date: 2026-03-09 10:32:53+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- RAG
- AI Agent
- 大语言模型
- Kubernetes
- Docker
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
external_url: https://juejin.cn/post/7614769648597745714
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:46927b2322d9afc964217370f37d81f2941e554e0744b969e0854ba6d708d997
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 22
captured_at: '2026-07-18T04:18:44.110381Z'
source_capture_sha256: sha256:3d3e248d46e6fd5834b144811f0e390e9e7f043307203c6f7b47e072693a52d3
source_capture_chars_original: 4094
source_publication_excerpt_chars: 499
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7614769648597745714](<https://juejin.cn/post/7614769648597745714>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 本章目标：帮你在一堆技术名词里做减法，只留下"现在就需要"的东西。
> 刚接触 Agent 开发，最容易犯的错误就是
> 技术栈焦虑
> ——LangChain、LangGraph、LlamaIndex、CrewAI、AutoGen、Dify、向量数据库、知识图谱……名词太多，不知道从哪下手。
> 真相是：你第一个 Agent 项目，只需要 4 样东西。
> 2.1 一个 LLM API —— 先跑通，别纠结
> Agent 的"大脑"就是大语言模型。你需要一个能调用的 LLM API。
> 入门推荐：选一个，立刻注册，拿到 API Key。
> 选项
> 优势
> 适合场景
> OpenAI \(GPT-4o\)
> 生态最成熟，教程最多
> 英文为主的项目
> Anthropic \(Claude\)
> 长上下文、代码能力强
> 需要处理长文档
> 豆包 \(Doubao\)
> 国内直连、中文优化
> 国内部署、中文场景
> DeepSeek
> 性价比高、推理能力强
> 预算敏感的项目
> 新手常见纠结：
> "我应该用哪个模型？GPT-4o 还是 Claude？"
> 答案：都行，先用一个跑通。
> 模型切换的成本很低（改一个 API 地址和 Key），但一直在选型上犹豫的成本很高。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
