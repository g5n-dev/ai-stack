---
title: 从 textarea 到 AI 输入框：用 Tiptap 实现 / 命令、@ 引用和结构化请求
date: 2026-05-12 00:17:36+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- MCP
- AI Agent
categories:
- AI 工程
scenarios:
- AI/ML项目
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7638465964879593506
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:c617e1c7dcf8d949ef71eeb17d9ab4ee3121456f1fd64eacdab75886b3b6632a
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 47
captured_at: '2026-07-18T04:21:22.933642Z'
source_capture_sha256: sha256:e3ccaff3b561ee0f406578c2d0cedc4561c7d98b7aaa6efc2e0b9529c6b4d1ed
source_capture_chars_original: 1543
source_publication_excerpt_chars: 735
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_06b3c6bad7827bf3169982d2b09f8e24b47a28cfc1554089adae93cc6a290ced
revision_id: rev_b121813b4a0250f9569f3766611bb2f8bb6ddcd1cf9a4a4abb1fafb23b63cefb
event_id: evt_faaf93aca277ac018582db4f5150916885a3c83a3a545dc7aec98ddfa7bdf44f
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-05-11T16:17:36Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7638465964879593506](<https://juejin.cn/post/7638465964879593506>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 本文基于
> AI Mind
> 项目真实实现整理。
> GitHub：
> github.com/HWYD/ai-min…
> 对应代码版本：
> v0.0.12
> AI Mind 是一个正在持续升级的 Next.js AI Chat 项目。它从最基础的本地聊天开始，逐步加入流式协议、工具调用、MCP、Skill 和 Agent 能力。
> 如果这篇文章或者 AI Mind 项目对你有所帮助，也欢迎到 GitHub 给项目点个 Star，这会是对我继续更新很大的鼓励。
> 在一个 AI 应用刚开始做聊天功能时，
> textarea
> 往往已经够用了。
> 用户输入一段自然语言，前端把它发给后端，后端拿到消息数组，模型开始生成回答。这个链路简单、直接，也足够支撑最早期的问答场景。
> 但当项目里慢慢出现 Skill（任务能力层）、Tool（可执行工具）、Resource（可读取上下文）、Prompt（可注入模型的提示模板）、MCP 能力（通过 MCP 接入的外部能力）之后，我开始遇到一个更具体的问题：用户输入不再只是一段自然语言。
> 它开始同时表达三件事：
> 这一轮我想做什么
> 这一轮我要引用哪个上下文
> 这一轮真正的自然语言问题是什么
> 普通
> textarea
> 能承载第三件事，却很难稳定承载前两件事。
> 这也是 AI Mind 在
> v0.0.12
> 里升级输入层的原因。
> 先简单介绍一下项目背景。AI Mind 是一个按版本持续演进的 AI Native Runtime Skeleton（AI 原生运行时骨架），不是一次性做完的 AI 产品。它从本地聊天闭环开始，逐步长出结构化流式协议、工具调用、多工具运行时、Skill 运行时、MCP 接入、能力表面，以及后续会开始推进的 Agent / 数据层能力。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
