---
title: 一天一个开源项目（第36篇）：EverMemOS - 跨 LLM 与平台的长时记忆 OS，让 Agent 会记忆更会推理
date: 2026-02-28 15:33:20+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- RAG
- AI Agent
- 大语言模型
- Python
- Docker
categories:
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
- RAG应用
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7611479802548092955
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:91ba1c0dab5266dbb593ae8ab78fb19d68a0208c17e5d45f14e5535c75c13519
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 60
captured_at: '2026-07-18T04:18:24.720794Z'
source_capture_sha256: sha256:c0cc773c6b39eb4aa26732c18b3b3a4d92efeaee234d90a418d52381c51649bc
source_capture_chars_original: 3746
source_publication_excerpt_chars: 800
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7611479802548092955](<https://juejin.cn/post/7611479802548092955>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 引言
> "More than memory — it's foresight.（不止于记忆，更是预见。）"
> 这是「一天一个开源项目」系列的第 36 篇文章。今天介绍的项目是
> EverMemOS
> （
> GitHub
> ）。
> 对话式 Agent 若只有「当前轮」的上下文，换会话就忘、跨平台不互通，很难做真正的长期陪伴与个性化。
> EverMemOS
> 是 EverMind-AI 开源的
> 长时记忆操作系统
> ：从对话中
> 结构化抽取
> 记忆（Encoding）、按
> 情节与画像
> 组织与巩固（Consolidation）、在需要时
> 智能检索
> 注入上下文（Retrieval），并支持情节记忆、事实、偏好、关系等多模态记忆类型。在
> LoCoMo
> 长上下文记忆基准上达到
> 93% 推理准确率
> ，且用
> Milvus、Elasticsearch、MongoDB、Redis
> 等生产级组件，通过
> REST API
> 与任意 LLM 集成，适合做跨 LLM、跨平台的 Agent 记忆底座。
> 为什么值得看？
> 🎯
> 93% LoCoMo 准确率
> ：在长上下文记忆与推理基准上表现领先
> 🏗️
> 生产级栈
> ：Milvus 向量库、Elasticsearch、MongoDB、Redis，企业可用
> 🔌
> 易集成
> ：REST API，与模型无关，任意 LLM 都可接入
> 📊
> 多模态记忆
> ：Episodes（情节）、Facts（事实）、Preferences（偏好）、Relations（关系）
> 🔍
> 多种检索
> ：BM25、向量、混合、Agentic 检索可配置
> 📄
> 论文与文档
> ：有架构说明、API 文档、Demo、评估指南
> 你将学到什么
> EverMemOS 的定位与三阶段流程（Encoding → Consolidation → Retrieval）
> 多模态记忆类型与检索策略（轻量 vs Agentic）
> 快速开始：Docker + uv、环境…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
