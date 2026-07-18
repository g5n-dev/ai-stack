---
title: Temperature 与 Top-p：控制模型输出的两个参数
date: 2026-06-23 12:51:35+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- 大语言模型
categories:
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7654335287171973170
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:2edf7b17edd65455950248baada0ba60139e1749bd79953e9f9804cbfb6d4911
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 31
captured_at: '2026-07-18T04:21:45.276497Z'
source_capture_sha256: sha256:e3c4680caa7f4c8a1c6493f97aeca1499dfa4409222d8899f8ebd839149fc491
source_capture_chars_original: 3297
source_publication_excerpt_chars: 654
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7654335287171973170](<https://juejin.cn/post/7654335287171973170>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 一、前置基础：大模型生成文本的核心逻辑
> 在理解两个参数前，先要搞懂大语言模型的生成本质，这是所有采样参数的底层前提：
> 自回归生成机制
> 大语言模型生成文本是
> 逐 token 生成
> 的：输入上文内容后，模型会预测 “下一个位置所有可能出现的 token” 的概率，从中选一个输出；再把这个输出的 token 加入上文，继续预测下一个，循环往复直到生成结束。我们看到模型 “一句话一句话输出”，底层其实是一个词一个词依次预测出来的。
> logits 与 Softmax 层
> 模型内部计算后，首先会给每个候选 token 输出一个原始分数（叫 logits），分数越高代表模型认为这个 token 越可能是下一个词。而
> Softmax
> 是模型输出层的计算函数，作用是把所有原始分数，转换成「0~1 之间、总和为 1」的标准概率分布，这样每个 token 都有了自己的出现概率。
> 采样
> 从 Softmax 输出的概率分布里，选出一个 token 作为最终输出的过程，就叫采样。Temperature 和 Top-p 都是用来
> 干预采样过程、控制输出随机性
> 的参数，只是作用的维度完全不同。
> 二、Temperature（温度参数）：调节概率分布的陡峭程度
> Temperature 作用于模型输出层 Softmax 的概率分布，
> 控制概率分布的"尖锐程度"
> ：
> 温度参数直接作用在 Softmax 的计算过程中，核心作用是
> 拉大或缩小不同 token 之间的概率差距
> ，也就是控制概率分布的 “尖锐 / 平坦程度”。
> 1.…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
