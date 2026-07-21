---
title: 《「潇楠WEB3哨兵」Agent 全栈架构：从记忆系统到技能扩展，桌面端 AI 投研助手的完整技术实现》
date: 2026-05-05 11:04:22+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- AI Agent
- Python
- 数据库
categories:
- AI 工程
- 数据
scenarios:
- AI/ML项目
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7635866179564584994
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:d2f35c7dcce09bc636d15880fe57630b5a6e08b70a0ca9f810af71b9462297e2
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 52
captured_at: '2026-07-18T04:19:48.489579Z'
source_capture_sha256: sha256:3d16bae760bba243412373080ca9bd5b560e1d8ad1fea64433319cf4e647526b
source_capture_chars_original: 1387
source_publication_excerpt_chars: 521
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_00a33ec5ffd795a1f0de93cb8c2c122593cffe9858d66ba3533be0772554aeb7
revision_id: rev_24db07f672e0cf6671500d38d33848d919691873ef069cc71615a6f57d68f8bc
event_id: evt_a76d7f271a67932b6c71afdd3114b6165aa494a7b732c491530788a0f315fe8c
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-05-05T03:04:22Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7635866179564584994](<https://juejin.cn/post/7635866179564584994>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 引言
> 在「潇楠WEB3哨兵」这个多链监控交易系统里，EVM/SOL 双链监控负责“眼睛”，电报 Bot 负责“嘴巴”，而 Agent 是最后一个也是最重要的拼图——它是整个软件的“大脑”。
> 它不是一个独立的聊天机器人。它能读取本地监控数据库里的历史交易，能调用合约分析工具实时解读市场，能通过右下角弹窗主动联系用户，甚至能从你们的长期对话中提炼你的交易风格。
> 本文将从架构层面，逐一拆解 Agent 的六个核心技术模块：Mixin 混入架构、多模型智能路由、五层记忆体系、身份固化与后悔药、零代码技能扩展、定时自驱与主动感知。每个模块都有代码、有原理、有坑与反思。
> 一、Mixin 混入架构：Agent 如何嵌入桌面应用
> Agent 不是一个独立进程。它和主窗口、电报助手、SWAP 模块共享同一个 Python 环境，通过 Mixin 模式混入到
> Api
> 类中。
> 为什么不用独立进程？三个原因：
> Agent 需要直接访问主进程的
> window
> 对象，用来弹出右下角通知。
> Agent 需要访问同一个 SQLite 数据库连接，用来读写记忆。
> Agent 的定时任务需要在同一个 asyncio 事件循环里执行，不能和 WSS 监控抢循环。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
