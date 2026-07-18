---
title: 小龙虾居然比你更健忘？OpenClaw 记忆系统指南，让它永远记住你
date: 2026-03-16 20:59:01+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- AI Agent
- TypeScript
- 数据库
categories:
- AI 工程
- 数据
scenarios:
- AI/ML项目
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7617697070365032494
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:e6d7fa6405ab0b5bb0e2ce0ea8cc67f685e8e50b6e4fc00755398346fe959d9d
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 34
captured_at: '2026-07-18T04:19:19.537882Z'
source_capture_sha256: sha256:03e35e31a3b93b3881d29eaf530f74674bca904765b9b55c6a4363cb78c8fdaa
source_capture_chars_original: 5293
source_publication_excerpt_chars: 703
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7617697070365032494](<https://juejin.cn/post/7617697070365032494>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 每次重启会话，AI 就变成"第一次见面"的陌生人？这篇文章教你用 OpenClaw 的记忆系统，彻底解决这个让人崩溃的问题。
> 开篇：一个真实的崩溃现场
> 你跟 AI 聊了整整两个小时，教了它你的写作风格、技术偏好、工作流习惯……
> 然后第二天打开新会话。
> 它问你："你是做什么工作的？"
> 你：……
> 这不是 bug，这是所有基于大模型的 AI 助手的"原罪"——
> 上下文窗口是有限的，会话结束了，记忆就消失了。
> 但 OpenClaw 在这件事上，走了一条非常务实的路。
> OpenClaw 记忆系统的核心哲学：文件就是真理
> 先说结论：
> OpenClaw 的记忆不在云端，不在数据库，就在你本地的 Markdown 文件里。
> 源码里有一句话说得特别直接：
> "The files are the source of truth; the model only 'remembers' what gets written to disk."
> 翻译一下：文件是唯一的事实来源，模型只"记住"写入磁盘的内容。
> 这个设计思路让人拍案叫绝——简单、透明、可控。你随时可以打开文件看、改、删，完全掌握 AI 记住了什么。
> 记忆文件的两层架构
> OpenClaw 把记忆分成两类，各司其职：
> 第一层：每日日志
> memory/YYYY-MM-DD.md
> 存放路径：
> ~/.openclaw/workspace/memory/2026-03-16.md
> 定位：
> 流水账
> ，今天发生了什么、讨论了什么、做了什么决定
> 特点：仅追加（append-only），会话开始时自动读取今天和昨天的内容
> 想象它是你的工作日报——不需要精炼，但要记录。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
