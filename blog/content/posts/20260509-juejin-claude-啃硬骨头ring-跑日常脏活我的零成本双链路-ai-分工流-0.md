---
title: Claude 啃硬骨头，Ring 跑日常脏活：我的零成本双链路 AI 分工流
date: 2026-05-09 08:54:09+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- 命令行工具
categories: []
scenarios:
- 命令行工具
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7637702426624458787
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:e1fec624af8daa2f7bbf36f4cdf3b11882c0805d50e5afb15c20a056beb4f8b0
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 38
captured_at: '2026-07-18T04:19:50.296768Z'
source_capture_sha256: sha256:313cce4956192a8f68e32c1ff3b6aca796fb22a2d7b689c0b14cfa365004a1b2
source_capture_chars_original: 4309
source_publication_excerpt_chars: 784
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7637702426624458787](<https://juejin.cn/post/7637702426624458787>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 从 DeepSeek 切到 Ring 2.6 这一天，数据筛选的活我省了一截
> 挂
> :free
> 标签的模型这一年我试过不少，多数都是写两行 hello world 撑不住日常的水平，跑两下就劝退。Ring 2.6 我本来也没抱什么期待，顺手接进 opencode 试了试，结果一周下来发现，这次不太一样。
> 蚂蚁的 Ring 2.6 上 OpenRouter 了，完全免费。数据筛选我以前都用 DeepSeek 跑，这周切到 Ring 试了下，响应快得意外，固定那套评分标准它接得住，复杂的活给 Claude，主链路 token 反而省了一截。
> 先把背景两句说清楚。Ring 2.6 是蚂蚁开源的 1T 推理模型，63B 激活参数，256K 上下文，5 月 8 号刚上线。它在 OpenRouter 上挂的是完全免费档——
> $0/M input + $0/M output
> ，不是按周限期，也不是新用户 trial，就是在 free tier 里挂着，能用就能薅。
> 现阶段限时免费一周，可以先去尝尝鲜，如果可以在接着付费体验。
> 我用的是 opencode 这个 AI CLI\(Claude Code 同生态的开源替代）。加一段 JSON 配置就能把 Ring 2.6 当模型源接进 opencode，跟着我在 Claude / DeepSeek 这套老链路里跑日常活。
> 我自己的体验浓缩成一句话就是：响应快得有点意外。之前我数据筛选那条线一直是 DeepSeek 在跑，按调用量算每天也要花钱。切到 Ring 2.6 之后这块的钱直接停了，筛选质量在我那套固定 rubric 下也没掉。主链路 Claude 一点没动，但旁边多了一条免费的简单活通道。
> 下面写清楚三件事：怎么把 Ring 2.6 接进 opencode、它在我这能干哪些活、Claude 我留给什么场景。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
