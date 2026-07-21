---
title: Go + Eino 构建 AI Agent（二）：Tool Calling
date: 2026-02-22 09:52:55+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- AI Agent
- 大语言模型
categories:
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7608759940799266866
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:fd3d3b8f2be022460400c14a209528e564a63a314dbee7be928c09ea271c1c43
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 37
captured_at: '2026-07-18T04:17:33.532406Z'
source_capture_sha256: sha256:63d26f093ee2aa34b8e2cec331a43edd6e75c1e5d6d0acf4a014bd3e5916ee5f
source_capture_chars_original: 4721
source_publication_excerpt_chars: 561
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_be1710ded87c8ec96f87f16a46ce262f85915e639c7928b78fa20fc10c85c5aa
revision_id: rev_f9b48054456940566a4999705c694ec2ec2a45312d84547d60a87023397672bd
event_id: evt_b7115d294a1efd54b6d8c42cd56ce7abb766f80d1f9f93cb4633101c1c26d391
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-22T01:52:55Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7608759940799266866](<https://juejin.cn/post/7608759940799266866>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> TL;DR:
> Tool Calling 让 LLM 能够调用外部函数。Eino 提供
> utils.InferTool
> 从 Go 函数自动推断工具定义，通过
> chatModel.BindTools\(\)
> 绑定工具，模型返回的
> response.ToolCalls
> 包含要调用的工具和参数。
> Tool Calling 流程
> 用户问题 → LLM 分析 → 返回 ToolCalls → 执行工具 → 结果返回 LLM → 最终回答
> 关键点：
> LLM
> 不执行
> 工具，只决定调用哪个工具、传什么参数
> 你的代码负责
> 执行工具
> 并把结果返回给 LLM
> LLM 基于工具结果生成最终回答
> 定义工具
> 方式一：InferTool（推荐）
> 从 Go 函数自动推断工具的 JSON Schema：
> type
> WeatherInput
> struct
> \{
> 	City
> string
> \`json:"city" jsonschema:"description=城市名称，如：北京、上海"\`
> \}
> type
> WeatherOutput
> struct
> \{
> 	City
> string
> \`json:"city"\`
> Temperature
> int
> \`json:"temperature"\`
> Condition
> string
> \`json:"condition"\`
> \}…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
