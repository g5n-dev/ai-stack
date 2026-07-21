---
title: 「AI学习笔记」RNN
date: 2026-04-13 16:34:45+08:00
draft: false
entry_kind: auto
tags:
- 掘金
categories: []
scenarios: []
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7628067175560413226
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:238df466096e987940aa635899216f54968dc8d44265b2cfe5d1ea9dd669e9f7
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 11
captured_at: '2026-07-18T04:19:32.723966Z'
source_capture_sha256: sha256:21bedac16e4ea17c90cf94a9d9f29e619489b8e53b4651b117c6678f8fc9de1f
source_capture_chars_original: 1314
source_publication_excerpt_chars: 718
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_f84ad9ed68d77663e1dce437b1023e271c67a87fe873d8d4d3366d79a5cebf2a
revision_id: rev_4b2faee4920d0e38f68bf6146c0526cfca9ab817cacd5fe2a22a4fb2a2099e14
event_id: evt_8aaf4562fd382abaa3e70c68162f4c7d06813402ad050523b08de73d875fe2e7
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-04-13T08:34:45Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7628067175560413226](<https://juejin.cn/post/7628067175560413226>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 从一个小白的角度学习AI，如果有任何问题，欢迎指出
> 从 RNN 简单介绍
> 在 Transformer 出现之前，序列建模领域的主角长期是 RNN 及其变体。
> 如果把这段历史简化成一句话：
> RNN 先解决“能处理序列”，Seq2Seq 解决“输入输出不等长”，Attention 再解决“信息压缩与长距离依赖”
> 。
> 这篇文章按我的学习顺序整理，尽量把关键概念说清楚。
> 一、解决了什么问题
> 在早期神经网络里，前馈网络（FNN）更擅长固定长度输入，不天然适合语言这种“先后有序、长度不固定”的数据。
> RNN（循环神经网络）出现后，主要带来了三点能力：
> 能够建模词序
> ：RNN 按时间步（token 顺序）逐个处理输入；
> 能够建模上下文依赖
> ：通过隐藏状态传递历史信息；
> 支持不定长输入
> ：句子长度不需要固定模板。
> 也就是说，当前时刻的结果不只看当前输入，还会受到历史输入影响。
> 二、RNN 的基本结构与公式
> 一个标准 RNN 单元通常包含以下变量：
> \(X\_t\)：第 \(t\) 个时间步的输入（一个 token 的向量表示）
> \(S\_t\)（或 \(h\_t\)）：隐藏状态（内部记忆）
> \(O\_t\)：第 \(t\) 个时间步的输出
> \(U\)：输入到隐藏层的权重矩阵
> \(W\)：隐藏状态到隐藏状态的循环权重矩阵
> \(V\)：隐藏层到输出层的权重矩阵
> 从公式可以看出，当前隐藏状态 \(S\_t\) 由两部分决定：
> 当前输入 \(X\_t\)
> 上一时刻隐藏状态 \(S\_\{t-1\}\)。
> 因此，RNN 的“记忆”本质上是通过隐藏状态在时间维度上传递的。
> 三、RNN 的优势与问题
> 3.1 优势
> RNN 的优势在于它第一次让神经网络能“顺着时间”理解序列，尤其适用于语言、语音等时序数据。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
