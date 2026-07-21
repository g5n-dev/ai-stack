---
title: 🦐 PP-Claw（皮皮虾）：用 Go 复刻一个轻量级 AI Agent 全栈解决方案
date: 2026-03-06 00:00:49+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- MCP
- AI Agent
- 大语言模型
- Python
- TypeScript
- 命令行工具
categories:
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
- 命令行工具
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7613552054946840619
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:e50d27ebe3f5bb74656b95d8eeeee098a34ba40281f4661eec646d51fc480fdc
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 43
captured_at: '2026-07-18T04:18:38.506089Z'
source_capture_sha256: sha256:8f9a7eca799a4685c953196add4822f9e85cc5e150b824b403c1299ea64879fd
source_capture_chars_original: 5005
source_publication_excerpt_chars: 649
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_e74a1d13759916cd709b464e279192a14834699745dd6674fc9a6168e6ebd36f
revision_id: rev_fb0b8e365fbff6efbd8823e9a33259ebabb29f97fc9c6143d896f7f86bc526f8
event_id: evt_f11ee8fdab897250a48e94436dfb84eab38fe0bb4364b703e8445637795bc4a7
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-03-05T16:00:49Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7613552054946840619](<https://juejin.cn/post/7613552054946840619>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 📖 项目背景
> 三个项目的传承关系
> 要理解 PP-Claw，首先要了解它的"家族谱系"：
> 🦞
> OpenClaw
> （小龙虾）是一个功能极其强大的开源个人 AI 助手，用 TypeScript 编写，代码量高达
> 430,000+ 行
> 。它支持 WhatsApp、Telegram、Slack、Discord、Signal、iMessage 等 20+ 聊天平台，具备语音交互、Canvas 渲染、多 Agent 协作等企业级能力。OpenClaw 的 Logo 是一只龙虾 🦞，项目名中的 "Claw" 就是"爪子"的意思。
> 🐈
> Nanobot
> （纳米机器人）受 OpenClaw 启发而生，是它的
> 超轻量 Python 复刻版
> 。Nanobot 的作者观察到 OpenClaw 虽强大但过于庞大（430K+ 行代码），对于研究和学习门槛太高，于是用
> ~4,000 行 Python 核心代码
> （仅 OpenClaw 的 1%!）实现了其大部分核心功能：多渠道接入、MCP 协议、记忆系统、技能扩展、定时任务等。Nanobot 证明了 AI Agent 不需要那么复杂。
> 🦐 PP-Claw（皮皮虾）
> 则是在深入研究 Nanobot 源码后，用
> Go 语言对 Nanobot 进行的 1:1 完整复刻
> 。之所以叫"皮皮虾"，是延续了 OpenClaw "甲壳类动物" 的命名传统——OpenClaw 是龙虾 🦞，PP-Claw 就做虾界最凶猛的皮皮虾（学名：螳螂虾）🦐。
> 为什么要再用 Go 重写一遍？…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
