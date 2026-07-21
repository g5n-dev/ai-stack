---
title: Workflow 系列（01）：基础理论——三种执行模型与 Anthropic 5 种模式
date: 2026-06-27 16:41:06+08:00
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
external_url: https://juejin.cn/post/7655880842009559040
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:f730e7f8b4a3903d4ab7de7f8494b52dd5ba0f797f1509c27a8959534815db4d
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 45
captured_at: '2026-07-18T04:21:46.497641Z'
source_capture_sha256: sha256:9aa03fe38116a0b58e7a78518405a32f5bf08ef8e8c3f26378dcde71bcb4088f
source_capture_chars_original: 5041
source_publication_excerpt_chars: 656
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_926eca18e75813f14bdb0c117042a60ee5645964b75bb38325398a62aa4e17fc
revision_id: rev_04d2cc81bf9ef012a3b35505788a59465683c3276ca6bd11826c8df7a7604b02
event_id: evt_7a947f66303824eb2ca0c359a27b36eb338941f33c24ecbefd75bf05711a4a70
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-06-27T08:41:06Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7655880842009559040](<https://juejin.cn/post/7655880842009559040>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 工作流不是流程图
> 传统工作流是确定性的：每个节点是一段代码，分支条件是布尔表达式，失败是预定义的异常类型。相同输入给相同输出，跑一百次和跑一次结果一样。
> Agent Workflow 打破了这个假设：
> 传统 Workflow（Airflow / n8n）：
>   节点        = Python 函数 / API 调用（确定性）
>   分支条件    = x &gt;
> 0
> （布尔表达式）
>   失败处理    =
> try
> /
> except
> （预定义异常类型）
>
> Agent Workflow：
>   节点        = LLM + 工具（输出不确定）
>   分支条件    = 置信度 ≥
> 95
> %（语义判断）
>   失败处理    = 重试 + 人工升级 + 语义降级
> Agent Workflow 是三种本质不同的执行模型之一，而不是流程图的升级。
> 三种执行模型
> DAG（有向无环图）
> 控制流在执行前完全确定，节点之间只能向前，不能回头。
> 代表：Airflow、n8n、GitHub Actions
> 用途：数据管道、ETL、定时任务
>
> 特点：
>   → 结构可视化，执行顺序透明
>   → 不支持循环（Agent 的重试逻辑需要变通处理）
>   → 适合确定性数据处理，不适合需要动态分支的 AI 任务
> 状态机
> 系统有有限个"状态"，事件触发状态转移。当前状态 + 事件 → 下一个状态。
> 代表：
> LangGraph
> 、自研
> Workflow
> （基于
> JSON
> 状态文件）
> 用途：有分支、有重试、有人工确认门的业务流程…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
