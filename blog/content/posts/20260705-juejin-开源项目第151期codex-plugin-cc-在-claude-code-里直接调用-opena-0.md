---
title: 开源项目第151期：codex-plugin-cc — 在 Claude Code 里直接调用 OpenAI Codex
date: 2026-07-05 05:14:40+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- AI Agent
- JavaScript
- 命令行工具
categories:
- AI 工程
scenarios:
- AI/ML项目
- 命令行工具
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7658565939235700771
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:b6c6b91b1d48e48723bb6467c0210b88a29d2629a220c10f9fdf79cd8de503ee
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 60
captured_at: '2026-07-18T04:21:50.697763Z'
source_capture_sha256: sha256:25426c42a4df6653abd893e7171e276de16607be2d83e78425e2c813a4def563
source_capture_chars_original: 5231
source_publication_excerpt_chars: 682
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_337606b452eac146427d3a91b0ffbfe0394cc3e8e3930e3808e346380f6d3d0b
revision_id: rev_2400c9de2eea754d959591360639f9fc0bae32cce3ff4de5a0ef663dada11c51
event_id: evt_79314e6f60b53b36f4861498a0be217c50c4b560acbc379108c068f4c5c76111
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-04T21:14:40Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7658565939235700771](<https://juejin.cn/post/7658565939235700771>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 引言
> "Use Codex from Claude Code to review code or delegate tasks."
> 这是「每日一个开源项目」系列的
> 第 151 篇
> 。今天的项目是
> codex-plugin-cc
> —— 一款让你在 Claude Code 工作流里直接呼叫 OpenAI Codex 的官方插件。
> 这件事本身就值得说一说：这是 OpenAI 官方为 Anthropic 的 Claude Code 写的插件。两家公司在模型层面是直接竞争对手，但在 agent 层面，这个插件的存在暗示了一个新的趋势 —— AI coding agents 正在走向跨厂商协作而非封闭生态。
> 24,582 颗 Star，项目创建于 2026 年 3 月，距今不过几个月。
> 你会学到什么
> 7 条核心命令的具体作用及适用场景
> 对抗性审查（
> /codex:adversarial-review
> ）的独特价值
> Review Gate：Stop Hook 拦截机制的工作原理与风险
> 后台任务管理：background 模式与状态追踪
> 会话转移：把 Claude Code 的上下文带入 Codex 继续执行
> 前提知识
> 使用过 Claude Code 的基本命令
> 了解 Claude Code 的插件/技能机制
> 基本了解 OpenAI Codex CLI
> 项目背景
> 概述
> codex-plugin-cc 是 OpenAI 官方发布的 Claude Code 插件，桥接 Claude Code 和本地安装的 Codex CLI（
> @openai/codex
> ）。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
