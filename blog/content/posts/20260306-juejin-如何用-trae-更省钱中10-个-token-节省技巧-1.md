---
title: 如何用 TRAE 更省钱（中）｜10 个 Token 节省技巧
date: 2026-03-06 11:07:04+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- AI Agent
- TypeScript
categories:
- AI 工程
scenarios:
- AI/ML项目
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7613709178717962275
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:eecfc7304f4f9e06d923cdde2b6a2c5952197e2a35ad0fd58080363a61912756
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 31
captured_at: '2026-07-18T04:18:39.334969Z'
source_capture_sha256: sha256:324b8c00642ccd633a7347bb15c0311429a6dbc1d3072423308ea17754377c85
source_capture_chars_original: 6000
source_publication_excerpt_chars: 786
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7613709178717962275](<https://juejin.cn/post/7613709178717962275>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 本文作者：云舒，TRAE 产品运营
> 我们在
> 上一篇
> 已经带大家认识了 Token 和上下文窗口，那在 TRAE 中究竟应该如何节省 Token 呢？本文将从 AI Coding 的六问心法出发，到 10 个具体场景的小技巧，手把手教你如何用 TRAE 更省钱！
> Token 花销的构成
> 我们在上一篇的文章中已经理解了 Token 的概念，这里简单回顾一下，你与大模型进行一次对话的成本，可以简单理解为一个公式：
> 总费用 = 未命中缓存的输入 Token× 输入单价 + 输出 Token× 输出单价 + 缓存 Token× 缓存单价（如有）
> 输入 Token：
> 你发给模型的所有内容，包括本轮提问、历史对话摘要、通过 \*
> #
> \*引用的代码/文件/文档等。
> 输出 Token：
> 模型返回给你的所有内容，包括文字回复、代码产物、工具调用信息等。
> 缓存 Token：
> 部分模型为优化长对话与重复请求，缓存历史上下文计算状态所消耗的 Token。后续收到相似请求时可直接复用，减少重新推理与 Token 消耗。
> 因此，
> 输入和引用的上下文体量、多轮交互的长度、选用模型的差异以及工具调用返回内容的多少
> ，都会直接影响最终的 Token 消耗与费用。
> AI Coding 的六问心法
> 在正式开始介绍节省 Token 的技巧之前，先帮你建立一个更重要的共识：
> 好的提问，比任何“省流小窍门”都更关键。
> 这 6 个问题就是所有技巧的底层“检查清单”，几乎适用于你与 AI 交互的所有场景。
> 你可以把它们当成一张“提问前体检单”：问题没想清楚的地方，用这 6 个问题补齐；表达不够清楚的部分，用这 6 个问题重新打磨。
> 不仅能从源头减少大量无效 Token 消耗，还能让 AI 的回答更聚焦、更可用！
> 「目标是否唯一」如果任务复杂，先拆解，再分步执行。当你切换任务时，建议新开一个对话。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
