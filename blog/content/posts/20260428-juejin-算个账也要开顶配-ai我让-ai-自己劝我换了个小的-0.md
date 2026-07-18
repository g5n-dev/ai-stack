---
title: 算个账也要开顶配 AI？我让 AI 自己劝我换了个小的
date: 2026-04-28 23:33:32+08:00
draft: false
entry_kind: auto
tags:
- 掘金
categories: []
scenarios: []
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7633684246477733924
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:fb2f2f614694b64ee466b330364695a9ee503bf6b9f5f49ffed0361a0616a72b
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 27
captured_at: '2026-07-18T04:19:43.142743Z'
source_capture_sha256: sha256:0b567014c5441357b018ab61db60321f29ae41427a50f1a327df37bbcd9d6edc
source_capture_chars_original: 2757
source_publication_excerpt_chars: 764
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7633684246477733924](<https://juejin.cn/post/7633684246477733924>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 其实我自己每个月在 AI 上花的钱不少，Claude、GPT、GLM 都有订阅。但其实有很大一部分预算其实是花在处理生活琐事上的——记账、外卖归类、做一个消费数据分析。这种活差不多每天都得跑一遍，所以token 烧得也不少，尤其是有时候开了深度思考的模型反而更容易给错数据。
> 后来我才反应过来，手里订阅一个不少，结果我一直在拿 Opus 的钱让它当我的计算器。有点奢侈了，所以我准备切换思路看看有没有节省token的办法。
> 一、我发现一个反直觉的事
> 在日常生活当中，我的直觉一直是有钱就上好的贵的效果肯定更好。Claude 4.7 Opus、GPT-5.5、深度思考模式，能切就切。
> 但是在我每天真正在干的活，尤其是一些琐事的数据整理计算：
> 把这个月的外卖订单按时间段算个总和
> 信用卡账单按"餐饮 / 打车 / 订阅"分一下类
> 一份消费明细 CSV 导进去问几个问题（这个月在哪吃得最多 / 哪几笔有点过了）
> 报销之前把几张发票的金额加一加
> 这些活其实顶配模型也都能干。Claude、GPT 我都试过，最后都跑出来了。问题是跑得不太对劲。
> 最直观的就是慢。一份几百行的消费明细，开了思考模式之后我能看着它"思考 6 秒""思考 11 秒"——其实本质只是这些数据相加而已没有很复杂的内容。
> 核心教训：简单数据 + 量大 + 重复，顶配模型在这种场景反而碍事。
> 二、在 OpenClaw 里试了百灵两个模型，最后选了 flash
> 我现在配模型的入口是 OpenClaw（之前文章写过怎么搭）。这次把蚂蚁百灵的两个挂上去对比着用：
> Ling-2.6-1T
> ：1 万亿总参数，每个 token 激活约 63B。属于真要分析事情那一档
> Ling-2.6-flash
> ：总参数 104B，每次只激活 7.4B
> flash 这个有点意思。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
