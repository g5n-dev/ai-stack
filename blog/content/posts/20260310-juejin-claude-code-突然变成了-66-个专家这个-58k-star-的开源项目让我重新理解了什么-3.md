---
title: Claude Code 突然变成了 66 个专家？这个 5.8k Star 的开源项目，让我重新理解了什么叫"会用 AI"
date: 2026-03-10 07:05:59+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- Rust
- Kotlin
- Swift
- 数据库
categories:
- 数据
scenarios: []
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7615202491505082402
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:8e2827e12635698d69536e9cbc5c668d106481875648e179146b4d00ab7a6361
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 61
captured_at: '2026-07-18T04:18:48.050985Z'
source_capture_sha256: sha256:1ff109671079c6832102be15fdd64b5388f6bbfa3d16104214bedaff543a771b
source_capture_chars_original: 3104
source_publication_excerpt_chars: 789
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_67f4bdc3d7ca2c606aa8daa6fde3bf70ff0ce24e6a0ae57698851662f81ecdc8
revision_id: rev_5a0e25b67a076dc5ad48eec2328f242ff6895405e6ee35e89e880f6408c3a57a
event_id: evt_fd526d0e21756ee0e981133b3fdca4dd7514a52d5347e5fda51aaec7758cf8ab
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-03-09T23:05:59Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7615202491505082402](<https://juejin.cn/post/7615202491505082402>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 前两天在 GitHub 上刷到一个项目，看完之后说实话——
> 沉默了大概三秒钟
> 。
> 不是因为技术多炸裂，而是因为它让我意识到：
> 大多数人用 Claude Code，可能只用了它 5% 的能力。
> 这个项目叫
> claude-skills
> ，作者 Jeff Smolinski，目前 5.8k Star，370 Fork。
> 它做了一件事：
> 给 Claude Code 装上 66 个"专家大脑"，让它在不同场景下自动切换身份。
> 你说"帮我实现 JWT 认证"，它不是一个泛泛的 AI 在回答你，而是一个
> NestJS 安全专家
> 在帮你写代码。
> 你说"优化一下这段 SQL"，接手的是一个
> 数据库调优专家
> ，带着 PostgreSQL 的最佳实践来的。
> 这不是换了个 prompt。这是换了个人。
> 先说它到底做了什么
> claude-skills 本质上是一套
> Claude Code 的技能插件系统。
> 它把全栈开发中你可能遇到的所有场景，拆成了
> 12 个大类、66 个专业技能
> ，每个技能背后都有独立的知识库和行为规范。
> 来感受一下这 66 个"专家"的阵容：
> 后端与框架专家
> 前端专家
> 数据与基础设施
> 安全与质量
> AI / ML 方向
> 还有 Rust、Go、C++、Swift、Kotlin、Spark、WebSocket、GraphQL、Shopify、WordPress、Salesforce、游戏开发、嵌入式系统……
> 66 个。
> 覆盖了一个全栈团队从前端到后端、从安全到运维、从 AI 到游戏的全部技能树。
> 真正牛的不是数量，是"自动切换"
> 很多人看到这里可能会想：不就是 66 个 system prompt 吗？
> 不是。
> claude-skills 做了一件更聪明的事——
> Context-Aware Activation（上下文感知激活）
> 。
> 你不需要手动选择用哪个技能。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
