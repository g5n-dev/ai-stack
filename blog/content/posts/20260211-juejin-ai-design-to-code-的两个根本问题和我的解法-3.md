---
title: AI Design-to-Code 的两个根本问题，和我的解法
date: 2026-02-11 09:27:49+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- 大语言模型
- TypeScript
- Docker
categories:
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
- 云原生/容器
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7605157203591299099
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:05167718c5d3e08fee74c3e8afcbee7a480c5784b327064e6b13d9ece8fcaed2
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 31
captured_at: '2026-07-18T04:17:11.520054Z'
source_capture_sha256: sha256:291c67a095890f41d2ee21b69efcf9c2ef65b79b778338898934397f224b2680
source_capture_chars_original: 6000
source_publication_excerpt_chars: 755
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_89ef57034b5957910a312b98741b934118446e246cb7c32cd0e99f8aafd1d437
revision_id: rev_86aac84ee550693440b574b63f63af8b8421aba23521587b639eded7a5568680
event_id: evt_d82eb87917fe8f66a9178f00ff1a717250b8c9afa4da5416218067b8e1f3955a
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-11T01:27:49Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7605157203591299099](<https://juejin.cn/post/7605157203591299099>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> AI 写业务逻辑已经很顺手，但设计稿还原？样式丢、布局乱、代码难维护。这不是模型不够强，是我们喂给它的输入不对。
> 落地过程中，我发现 AI D2C 的困难归结为两个根本问题。
> 问题一：AI 没有空间认知
> LLM 是序列模型，处理的是 token 流，不是二维平面。当它看到：
> \{
> "x"
> :
> 285
> ,
> "y"
> :
> 725
> ,
> "width"
> :
> 700
> ,
> "height"
> :
> 440
> \}
> \{
> "x"
> :
> 1005
> ,
> "y"
> :
> 725
> ,
> "width"
> :
> 370
> ,
> "height"
> :
> 440
> \}
> \{
> "x"
> :
> 285
> ,
> "y"
> :
> 1165
> ,
> "width"
> :
> 340
> ,
> "height"
> :
> 400
> \}
> 它看到的是三组数字，不是「第一行两张卡片并排，第二行一张卡片靠左」。
> 人看设计稿是空间扫描
> — 一眼看出对齐、等距、分栏。
> LLM 看坐标是数值推理
> — 要算
> 1005 - 285 = 720
> ，再跟
> width: 700
> 比较，才能推断「这两个元素是水平排列的」。而数值推理恰恰是 LLM 最弱的能力之一。
> 这导致几类典型错误：
> 空间关系
> 人的判断
> LLM 容易犯的错
> 水平对齐
> y 值接近就是一行
> 把 y=725 和 y=730 判断成两行
> 等分布局
> 三个等宽元素占满容器
> 生成固定 px 而不是 flex:1
> 嵌套层级
> 小元素在大元素内部
> 坐标包含关系算错，层级打平
> 间距规律
> 所有模块间距 20px
> 部分写 20，部分写 16，不一致
> 本质原因：Transformer 的自注意力机制是在 token 维度上建立关联的，它没有内置的二维坐标系。它理解「猫坐在垫子上」比理解「x=100 的元素在 x=500 的元素左边」要容易得多——前者是语言语义，后者是空间计算。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
