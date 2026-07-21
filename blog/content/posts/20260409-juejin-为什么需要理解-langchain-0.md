---
title: LangChain设计与实现-第1章-为什么需要理解 LangChain
date: 2026-04-09 14:32:24+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- RAG
- AI Agent
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
external_url: https://juejin.cn/post/7626595191144529920
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:f63c0594b4ba64b9932902ce595ded6bb449c2916ea38405e1fa70ba196ce7e9
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 36
captured_at: '2026-07-18T04:19:31.178510Z'
source_capture_sha256: sha256:750f50007dc3a49d7939e9367767901e284f63bf37f161581da6c2649fa42e07
source_capture_chars_original: 5931
source_publication_excerpt_chars: 699
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_60d3d6151c8ee9d787b7fb644449ce19f6c0e5a338fb32577104076718ae0a2c
revision_id: rev_9dd66f0f9aa6a3ec670c2c0d39fb52e7e0b660411890edd61418d6f518d6a7d1
event_id: evt_ca8ccc4cc16127559715dccabd581f133b2bd0c4f96c9b2faec2fde6faabce75
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-04-09T06:32:24Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7626595191144529920](<https://juejin.cn/post/7626595191144529920>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 第1章 为什么需要理解 LangChain
> 本书章节导航
> 前言
> 第1章 为什么需要理解 LangChain
> （当前）
> 第2章 架构总览
> 第3章 Runnable 与 LCEL 表达式语言
> 第4章 消息系统与多模态
> 第5章 语言模型抽象层
> 第6章 提示词模板引擎
> 第7章 输出解析与结构化输出
> 第8章 工具系统
> 第9章 文档加载与文本分割
> 第10章 向量存储与检索器
> 第11章 Chain 组合模式
> 第12章 回调与可观测性
> 第13章 记忆与会话管理
> 第14章 Agent 架构与执行循环
> 第15章 工具调用与 Agent 模式
> 第16章 序列化与配置系统
> 第17章 Partner 集成架构
> 第18章 设计模式与架构决策
> 本章基于 LangChain 1.0.3 / langchain-core 1.2.26 源码分析。源码路径：
> libs/
> 目录。
> 当我们站在 2025 年回望 AI 应用开发的演进历程，会发现一个有趣的规律：每一次底层模型能力的跃迁，都会催生出一个新的应用框架浪潮。从最初手写 HTTP 请求调用 OpenAI API，到使用各种轻量封装库，再到如今以 LangChain 为代表的完整应用框架生态——这个过程并非偶然，而是由真实的工程痛点驱动的必然选择。
> LangChain 是当前 LLM 应用开发领域使用最广泛的框架。它的核心仓库在 GitHub 上拥有超过 10 万颗星，PyPI 周下载量常年维持在百万级。然而，对于大多数开发者而言，LangChain 仍然是一个"会用但不理解"的黑盒。本书的使命，就是带领读者打开这个黑盒，从源码层面理解其设计哲学与实现细节。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
