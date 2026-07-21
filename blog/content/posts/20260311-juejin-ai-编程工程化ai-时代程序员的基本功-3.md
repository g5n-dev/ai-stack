---
title: AI 编程工程化：AI 时代程序员的基本功
date: 2026-03-11 22:41:15+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- MCP
- AI Agent
- 大语言模型
- 数据库
categories:
- 大模型
- 数据
scenarios:
- AI/ML项目
- 大语言模型
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7615791413089075241
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:43b4f98ce66d7ab8e76af06427b03946c26d03bee810da184c2973ddeef09de7
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 21
captured_at: '2026-07-18T04:18:50.868739Z'
source_capture_sha256: sha256:6592088563816913db1356490d48e0e8c0eed924a8017fcd2cdf3bbd2be9ea73
source_capture_chars_original: 4959
source_publication_excerpt_chars: 787
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_1523e06f88c135548139f26f65172e856a50b98cda3b2b09e367293035d10ee0
revision_id: rev_cc63b3b752843098f1384bd2417f7e8f8668483a087681fa160320f607c9ff77
event_id: evt_4a31e5a43e1db075c25cdb4b4025597541c09d80d14ca181c5fe453584fe970f
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-03-11T14:41:15Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7615791413089075241](<https://juejin.cn/post/7615791413089075241>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 好久不见，各位朋友。
> 最近这段时间，我一直在折腾 AI 编程。新项目、老项目，只要能用 AI 的地方，我几乎都试了一遍。
> 说实话，一开始我对它的期待并不高。过去几年各种 AI 工具我也用过不少，大多数都是演示看起来很厉害，但真正用在项目里，总感觉差点意思。
> 但这次不太一样。
> 有几个瞬间，我真的被震住了。
> 在真实项目里，原本要花几天甚至一周才能完成的活，AI 几十分钟就帮我搞定了。
> 我明显感觉到自己的开发节奏正在悄悄改变。
> 我试了很多 AI 编程工具，也对比过多个大语言模型，结论其实很直接：在编程这件事上，Claude Code 目前是最好用的。
> 不只是代码写得好，它对工程化的理解，也比大多数工具都深得多。像
> MCP、Skill
> 这些概念，都是它率先提出的，后来很多工具才开始跟进。
> 但我刚开始用 Claude Code 的时候，完全没有发挥出它的能力。
> 当时我在做一个老项目的技术栈升级，整体代码需要重构。我直接让 Claude Code 上手干，没做分析，没写 Plan，也没有任何规则约束。
> 我以为它能自己搞清楚方向。
> 结果很糟糕。
> 改完之后代码风格前后不一致，代码也没有进行合理拆分，逻辑还有几处出了问题。Review 起来非常痛苦，后面还花了很长时间去返工和调试才跑通。
> 后来我慢慢意识到一件事：
> AI 最大的问题，其实不是能力不够，而是你没有给它边界。
> 如果没有工程意识，AI 只会把混乱放大。
> Claude Code 其实已经提供了一整套机制来解决这个问题——只是大多数人根本没有用到。
> 这篇文章，我就以 Claude Code 为例，结合这段时间 AI 编程的实践，把这套 AI 编程工程化体系讲清楚。
> 先想象一个场景
> 你是技术负责人，公司新招了一个能力极强的开发者。
> 代码写得飞快，什么语言都会，24 小时不休息。
> 但问题是——他对你的项一无所知。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
