---
title: Agent First Engineering
date: 2026-03-05 12:40:40+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- AI Agent
categories:
- AI 工程
scenarios:
- AI/ML项目
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7613552054946332715
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:f63ad41e99bd161b574094f1761d72055e7d771e5db6b2fbd9233dbbd7321fc4
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 23
captured_at: '2026-07-18T04:18:36.117889Z'
source_capture_sha256: sha256:7bc568756aea03292d71279d54ee947a09c22b5b5f1c976584f0d0653cdf4521
source_capture_chars_original: 2747
source_publication_excerpt_chars: 790
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_4568c030ba8a15f37fe43637c896ea4c9e54559200f907a5f76693d70da4d5ac
revision_id: rev_281c97212d2c4f4afdbb78d96b10e17b6400b2fa964b891caf6cec16e061c3e7
event_id: evt_8d230888c24be13dffa6cd4911b2dab5b4447617798d4e298e83521e73c572e2
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7613552054946332715](<https://juejin.cn/post/7613552054946332715>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 👀 最新、最有用的AI编程姿势，总来自「知识药丸」
> 《贾杰的AI编程秘籍》
> 付费合集，共10篇，现已完结。30元交个朋友，学不到真东西找我退钱；）
> 以及我的墨问合集《100个思维碎片》，1块钱100篇，现已完结。（文末有订阅方式
> 质量更顶的《又100个思维碎片》不定期更新中，与你探讨AI编程2.0等有意思的话题（文末有订阅方式
> 写在前面
> 最近读到一篇来自 OpenAI 工程师 Ryan Lopopolo 的文章，讲的是他们团队用 Codex 构建一个内部产品的全程——
> 0 行人工代码
> ，历时 5 个月，百万行代码级别。
> 我第一反应是：这不是噱头吗？
> 看完之后发现，这不是在炫耀 AI 有多强，而是在认真回答一个问题：
> 当 AI 真的能写代码了，工程师该干什么？
> 这篇是我自己的学习笔记，从一个旁观者的角度整理，希望对你也有用。
> 一个反常识的结论
> 我们习惯于认为，AI 辅助编程的瓶颈在 AI 本身——模型够不够聪明、上下文够不够长。
> 但这个团队的经历说的恰恰相反：
> 早期进度慢，不是因为 Codex 不够强，而是因为环境太烂了。
> 工具缺失、文档混乱、结构不清晰——这些"人类勉强能接受"的环境，对 AI 是致命的。AI 没法靠直觉补全信息，没法靠经验猜测意图，它只能用它能"看到"的东西。
> 这个结论挺刺激的：
> 我们以为在优化 AI，其实在优化自己的工程环境。
> 工程师的角色变了
> 以前我们说"用 AI 提效"，潜台词是：AI 帮你写，你来审。
> 但这个团队做的是另一回事——工程师不再写代码，而是在设计
> 让 AI 能写好代码的环境
> 。
> 具体来说是三件事：拆解目标、构建脚手架、建立反馈回路。
> 有点像从"出租车司机"变成了"城市规划师"。司机关注的是怎么走这条路，规划师关注的是怎么把路修好，让所有车都能跑快。
> 给 AI 地图，不是说明书
> 这是整篇文章我觉得最有价值的一个洞察。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
