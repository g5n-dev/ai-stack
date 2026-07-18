---
title: Claude Code 之父的技巧分享：用"拉尔夫循环"让 AI 替你死磕
date: 2026-02-18 07:39:44+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- AI Agent
- 大语言模型
- Python
- TypeScript
- Go
categories:
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7607261340566257683
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:43bf2becfb8c8aa5287a8c3bf24a59e96ba0fc12e605c523a8ff8e544f633372
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 37
captured_at: '2026-07-18T04:17:25.656682Z'
source_capture_sha256: sha256:04aeaae3b287a6d8f5b30cd47e6e882637872b3a4cd3d8e04d090f53b3dc9a4b
source_capture_chars_original: 3315
source_publication_excerpt_chars: 800
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7607261340566257683](<https://juejin.cn/post/7607261340566257683>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 本文已收录到
> AI编程一站式导航
> 。本文链接：\[03.9 2026 年最佳 AI 编码工具完全指南\]\(
> code.ai80.vip/ai-tool-gui…
> 2026 年最佳 AI 编码工具完全指南\) 强烈推荐：AI编程巴士网站：
> 稳定纯净的ClaudeCode套餐供应
> ；
> Claude Code 联合创始人 Boris Cherny 最近晒了组数据，挺炸裂的：30 天提交 259 个 PR，每行代码都是 Claude + Opus 4.5 写的；47 天里有 46 天在用，最长一个 session 跑了 1 天 18 小时。
> 他分享了 13 条心得，今天单聊第 12 条——
> "长时间运行的任务，用ralph-wiggum插件。"
> 这不只是个插件。搞懂它背后的原理，你对 AI Agent 的认知会上一个台阶。
> 一、先说说什么是拉尔夫循环
> 最近这个概念挺火。简单讲，就是你给 Agent 一个任务，Agent 跑了很多轮之后觉得"我做完了"想退出——这时候拉尔夫会拦截这个退出，把同样的 prompt 再喂一遍。
> 关键是：Agent 之前的上下文还在（有的持久化到文件里，有的直接复用上下文），之前改过的代码也保留着。于是 Agent 从上次停下的地方继续干活。
> 这个场景你可以这么理解：实习生觉得自己做完了就停了，老板甩着鞭子说"没完呢，继续"，一直干到老板满意为止。
> 本质上，这是通过多轮迭代来解决一个老问题：LLM 上下文窗口有限，导致 Agent 难以很好地完成长任务。
> 效果有多夸张？流传最广的案例是，有个老哥靠这个机制"鞭打"Agent，跑了一个 3 个月的循环，直接干出了一门完整的编程语言（后面会详细聊）。
> 二、理解一组概念：Context Rot vs In-Context Learning
> 用 Ralph 跑长任务，上下文窗口是核心战场。随着对话变长，上下文不断增加。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
