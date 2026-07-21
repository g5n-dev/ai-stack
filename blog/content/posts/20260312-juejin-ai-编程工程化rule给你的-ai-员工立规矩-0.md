---
title: AI 编程工程化：Rule——给你的 AI 员工立规矩
date: 2026-03-12 14:57:45+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- MCP
- TypeScript
- JavaScript
- 数据库
categories:
- AI 工程
- 数据
scenarios:
- AI/ML项目
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7616193982246862867
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:c34e497897c50dc680bcdc7030e04b172e97af24d78258adfd9df243f1529f92
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 27
captured_at: '2026-07-18T04:19:09.603922Z'
source_capture_sha256: sha256:a063329e9df751a02e93e68a2413105738195ab848005efee72c6487e8071b22
source_capture_chars_original: 4607
source_publication_excerpt_chars: 764
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_4eb0a22a627d177aa917137a3c700eabdedd8a0c12ff474518c19dfab373a37d
revision_id: rev_90f5eaaa37f072dc2e1bf05de03ab6e18d249837677d41a52a5cc39c96cbfa8a
event_id: evt_5d10fcfe6670f3620c6eecfddb9794f47fca52113ec5082bb4a70bd6b732258c
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-03-12T06:57:45Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7616193982246862867](<https://juejin.cn/post/7616193982246862867>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 上一篇我说过，用 AI 编程工具，本质上就是在带一个能力超强但什么都不知道的
> 「新员工」
> 。
> 这篇专门讲第一件事：
> 给它立规矩。
> 在 Claude Code 的体系里，这个东西叫 Rule。
> 没有规矩，会发生什么
> 先说一个我自己经历过的真实场景。
> 刚开始用 AI 编程的时候，我手里有一个很多项目都在用的公共组件，是 Vue 2 + JavaScript 写的。我让 AI 帮我把它重构成 Vue 3 + TypeScript，并迁移到新的组件库开发框架。
> 当时我什么 Rule 都没有，直接选中目录，跟 AI 说：
> “帮我重构为 Vue 3 + TS，并迁移到新组件库开发框架”
> 然后就开始和 AI 来回拉扯。
> 折腾了好几轮，组件确实是“能跑了”，但问题也一堆：
> 有些地方用了 Options API，有些地方用了 Composition API，代码风格前后不一致
> 业务逻辑、样式、交互代码全塞在一个
> .vue
> 文件里，没有任何拆分
> 明明项目里已经有原子组件和 utils，它还是重新写了一套
> AI 写完后没跑 ESLint，留下了一堆 warning
> 甚至还顺手删了一个“看起来没用”的文件
> 最离谱的是：
> 它删完还一本正经地告诉我 ——
> “已经清理了无用代码。”
> 问题其实不在 AI。
> 不是 AI 不聪明，而是它根本不知道你的规矩。
> 没人告诉它：
> 项目统一用
> Composition API
> 组件逻辑需要
> 拆分模块
> 优先复用
> 已有组件和工具函数
> 提交前必须
> 跑 ESLint
> 哪些文件是
> 绝对不能动的
> 所以它只能按照
> 自己的理解
> 去写代码。
> 而 AI 的理解，大概率是：
> “我觉得这样也行。”
> 于是就出现了各种风格混乱、重复造轮子、甚至误删文件的问题。
> 没有规矩，AI 就只能靠猜。
> 而一旦开始“猜”，结果就很容易失控。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
