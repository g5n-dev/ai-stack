---
title: ReAct：让大模型学会边想边做
date: 2026-04-12 12:09:13+08:00
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
external_url: https://juejin.cn/post/7627365452814598154
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:50129af0018d6ea275e4a1bb739bf9ab096e66c4d2758262452171bd8d240f4a
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 16
captured_at: '2026-07-18T04:19:32.340185Z'
source_capture_sha256: sha256:43b9a0ed28b5bfd963e6dfc16bcbb3d9a62b9529c778fb20c8c48aa3fb20de97
source_capture_chars_original: 4020
source_publication_excerpt_chars: 675
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_04c992295c785d903f071a10efb12f717f407ca96b85ac787322c31f01c19e65
revision_id: rev_cdee17b0d1a7e571b01ac811a039f65c98edcc5c84d3e4928276d61bff0696f4
event_id: evt_27fcd077cc0ef390e787514304a732e240ba5803427941ebaf59bc9e076a4501
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-04-12T04:09:13Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7627365452814598154](<https://juejin.cn/post/7627365452814598154>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 本文已收录至GitHub，推荐阅读 👉
> Java随想录
> 微信公众号：Java随想录
> 传统聊天机器人相信大家都用过——你问一句，它答一句。线性，简单，但遇到复杂问题就露馅了。比如问"特斯拉股价相比去年涨了多少"，它要么瞎编，要么说"我无法获取实时信息"。
> 2022年，Google Research提出了ReAct框架。它要解决的就是这个问题：
> 让大模型像人一样，一边想一边做，做完再看结果，接着想下一步
> 。
> ReAct的核心原理
> 先看个例子
> 想象你在一个陌生城市旅行。
> 早上醒来，你想：今天天气怎么样？要不要带伞？
> 你打开天气APP看了一眼——有阵雨。
> 于是你调整计划：上午去博物馆躲雨，晚上再去看夜景。
> 这个"想→做→看→再想"的过程，就是ReAct在做的事。
> 三个阶段
> ReAct由三个部分构成：
> 思考（Thought）
> ：分析当前问题，决定下一步做什么。比如"用户问的是某国人口，我需要查数据"。
> 行动（Action）
> ：调用外部工具。输出格式类似
> search\(query="某国人口"\)
> 。
> 观察（Observation）
> ：工具返回结果，成为下一轮思考的依据。比如
> \{"population": "1.4亿"\}
> 。
> 循环往复，直到任务完成。
> 什么时候停下来
> 两种方式：
> 硬限制
> ：设个最大迭代数，比如
> max\_iterations=10
> ，到了就强制结束。
> 条件触发
> ：模型觉得自己很有把握了，或者连续失败好几次，就主动收手。
> 技术实现
> 工具怎么设计
> 三个原则：
> 原子性
> ：一个工具只做一件事。计算器就做计算，搜索就做搜索，别搞大而全。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
