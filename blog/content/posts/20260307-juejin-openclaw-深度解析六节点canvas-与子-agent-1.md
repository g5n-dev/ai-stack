---
title: OpenClaw 深度解析（六）：节点、Canvas 与子 Agent
date: 2026-03-07 15:54:42+08:00
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
external_url: https://juejin.cn/post/7614205951335301130
aliases:
- /posts/20260307-juejin-openclaw-深度解析六节点canvas-与子-agent-2/
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:35ba438d1a5ce0449251c7cdb6af917674acb5bcd19a9415dd418cd7b9cbe5a8
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 35
captured_at: '2026-07-18T04:18:40.972300Z'
source_capture_sha256: sha256:0238371867beacd9d262a79cb5e94b13451d5e5c28e8f35776134857c5020b54
source_capture_chars_original: 6000
source_publication_excerpt_chars: 602
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_ed4a54f163b451095080c8f644ac56bc461bcbcada96f21d6da4a35d1cd3aaba
revision_id: rev_5cdf5ac1e20571181d9da0f02076440d3582e3b0cd0ece77396381600495e684
event_id: evt_b43d76859c97558c9a36cf1754b7c08688b7010deefa0300b318b915ab0d4259
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-03-07T07:54:42Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7614205951335301130](<https://juejin.cn/post/7614205951335301130>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 场景：AI 助手的"边界问题"
> 把 OpenClaw 当作个人 AI 助手使用一段时间后，会遇到几个让单进程模型力不从心的场景：
> 远程执行
> ：你想让 AI 帮你在家里的 Linux 服务器上跑一段脚本，但 OpenClaw Gateway 运行在 Mac 上——AI 怎么触达那台服务器的 Shell？
> 手机上的交互 UI
> ：你想在手机上看到 AI 生成的实时仪表盘，并且能点击按钮触发下一步操作——AI 怎么向移动端 WebView 推送 UI，WebView 里的点击又怎么反馈给 AI？
> 并行任务
> ：你让 AI 帮你整理 1000 封邮件——用一个 Agent 串行处理太慢了，能不能派出多个 AI 同时干？
> 这三个场景分别对应 OpenClaw 的三个核心扩展机制：
> Node Host（节点主机）
> 、
> Canvas + A2UI
> 、
> 子 Agent（Sub-agent）
> 。
> 一、Node Host：让 AI 触达远程机器
> 问题：Gateway 和执行目标不在同一台机器
> Gateway 负责对话管理和 Agent 执行，但
> system.run
> （执行 Shell 命令）这类工具需要在
> 目标机器
> 上运行——可能是远程服务器、NAS、Raspberry Pi，或者同一台 Mac 上受限环境的另一个进程。
> Node
> 是解决这个问题的抽象：一个独立进程，连接到 Gateway，响应执行请求。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
