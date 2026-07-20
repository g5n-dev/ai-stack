---
title: 13-KV Cache与位置编码表：大模型推理加速的核心技术
date: 2026-03-02 05:21:09+08:00
draft: false
entry_kind: auto
tags:
- 掘金
categories: []
scenarios: []
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7612129754633011227
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:e24e6f3a3b0b5d346aece9c4f34f57679a2228d2f9703a764d8cc87bc4245e09
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 30
captured_at: '2026-07-18T04:18:28.373533Z'
source_capture_sha256: sha256:d34668e7f32f69231f400cb979f5db456a640ddd448ec867b18c8a8e9ff4c4d0
source_capture_chars_original: 6000
source_publication_excerpt_chars: 799
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_f8bfdf2a6f40f2e8bb3ae202cc9e7d92c45a7771368dea4e5acb409536d247ed
revision_id: rev_cbc4d9ecfedd7c5b5a2afdd5862986f7c37b04c70953551c4e8f05ad45884a86
event_id: evt_cb3ec55daa38a3186b193ff3d70bce43d8bca4b0d77d3c34cf564897b3924a78
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-03-01T21:21:09Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7612129754633011227](<https://juejin.cn/post/7612129754633011227>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 从自回归生成说起
> 在前面的章节中，我们学习了大模型的核心原理：给定前面的Token序列，预测下一个Token。但是，当我们实际使用大模型进行文本生成时，会遇到一个严重的
> 性能问题
> 。
> 自回归生成的过程
> 假设我们要让模型生成一句话："今天天气真好"（5个Token）
> 第1步
> ：输入提示词"今天"
> 输入序列：\["今天"\]（1个Token）
> 模型计算注意力，输出：\["天气"\]
> 第2步
> ：继续生成
> 输入序列：\["今天", "天气"\]（2个Token）
> 模型
> 重新
> 计算这2个Token的注意力，输出：\["真"\]
> 第3步
> ：继续生成
> 输入序列：\["今天", "天气", "真"\]（3个Token）
> 模型
> 重新
> 计算这3个Token的注意力，输出：\["好"\]
> 注意到问题了吗？
> 每次生成新Token时，模型都要重新计算前面所有Token的注意力！
> 重复计算的代价
> 让我们用数学来量化这个问题。
> 注意力计算回顾
> 在注意力机制中，对于每个Token，我们需要计算：
> Q
> =
> X
> ⋅
> W
> Q
> \(Query\)
> K
> =
> X
> ⋅
> W
> K
> \(Key\)
> V
> =
> X
> ⋅
> W
> V
> \(Value\)
> Output
> =
> softmax
> \(
> Q
> ⋅
> K
> T
> d
> k
> \)
> ⋅
> V
> \\begin\{aligned\}
> Q &amp;= X \\cdot W\_Q \\quad \\text\{\(Query\)\} \\\\
> K &amp;= X \\cdot W\_K \\quad \\text\{\(Key\)\} \\\\
> V &amp;= X \\cdot W\_V \\quad \\text\{\(Value\)\} \\\\
> \\text\{Output\} &amp;= \\text\{softmax\}\\left\(\\frac\{Q \\cdot K^T\}\{\\sqrt\{d\_k&#125;&#125;\\right\) \\cdot V
> \\end\{aligned\}
> Q
> K
> V
> Output
> ​
> =
> X
> ⋅
> W
> Q
> ​
> \(Query\)
> =
> X
> ⋅
> W…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
