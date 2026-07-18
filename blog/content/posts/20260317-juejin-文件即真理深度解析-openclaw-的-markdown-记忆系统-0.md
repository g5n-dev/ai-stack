---
title: 文件即真理：深度解析 OpenClaw 的 Markdown 记忆系统
date: 2026-03-17 03:25:32+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- AI Agent
- Python
- TypeScript
- 数据库
categories:
- AI 工程
- 数据
scenarios:
- AI/ML项目
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7617728986829733915
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:9602266485759d1cf36e0ac6200d0467d4dffa55a134c04a9739f369fb94f946
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 35
captured_at: '2026-07-18T04:19:21.866564Z'
source_capture_sha256: sha256:558bc865b78dc01daf25dcbec7bead956c6f104e483f9b9dba2816887abf82a0
source_capture_chars_original: 4205
source_publication_excerpt_chars: 790
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7617728986829733915](<https://juejin.cn/post/7617728986829733915>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 文件即真理：深度解析 OpenClaw 的 Markdown 记忆系统
> 大多数 AI Agent 的记忆，存在于对话窗口里，窗口关闭，记忆消失。
> OpenClaw 选择了一条不同的路：
> 把文件系统当成 Agent 的大脑
> 。
> 一、问题的起点：AI Agent 为什么会"失忆"？
> 用过 AI Agent 的人都有过这种体验——
> 你昨天跟它聊了两个小时，把项目背景、技术选型、你的偏好全都解释了一遍。今天打开新对话，它又变成了一个什么都不知道的陌生人。你只能重新解释一遍，然后再重新解释一遍。
> 这不是 AI 不够聪明，是
> 记忆层没有设计好
> 。
> 传统 Agent 的记忆存在于
> 上下文窗口
> 里。上下文窗口是易失的、有限的，一旦超出长度限制，早期的内容就会被截断丢弃。每次新对话，一切清零。
> OpenClaw 给出的答案很简单，也很彻底：
> 文件不会消失。把记忆写进文件。
> 二、文件即 OS：OpenClaw 的核心哲学
> OpenClaw 最底层的设计理念，是把
> 文件系统当成 Agent 的操作系统
> 。
> 在这套体系里，一切皆是文件：
> 组件
> 文件
> 作用
> Agent 人格
> SOUL.md
> 定义语气、个性、角色边界
> 行为准则
> policy.md
> 约束 Agent 的行为边界
> 长期记忆
> MEMORY.md
> 跨会话持久保存的核心知识
> 短期日志
> memory/YYYY-MM-DD.md
> 当日操作记录，仅追加
> 工具说明
> TOOLS.md
> 用户维护的工具笔记和配置
> 自动任务
> HEARTBEAT.md
> 定期执行任务的检查清单
> 不是数据库，不是向量存储，不是云端服务。
> 就是一堆 Markdown 文件，放在你的本地文件系统里，Git 可以追踪，文本编辑器可以打开，人类可以直接读写。
> 这种设计有一个好处，大多数系统都做不到：
> 透明
> 。你不需要猜测 Agent "记得什么"，打开文件夹就能看到。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
