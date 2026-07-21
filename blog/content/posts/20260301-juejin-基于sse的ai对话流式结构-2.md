---
title: 基于SSE的AI对话流式结构
date: 2026-03-01 10:57:35+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- Docker
categories: []
scenarios:
- 云原生/容器
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7611424094525620265
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:d4120c5fbbdb149e9aa990e21868d925f289a1353cc2c4f3579f2f8b408fb89b
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 14
captured_at: '2026-07-18T04:18:26.453404Z'
source_capture_sha256: sha256:8641034d9894a20e451506d8f8df2be38790f4bdf354f98feef9acd43af2652f
source_capture_chars_original: 6000
source_publication_excerpt_chars: 800
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_2bb8da604721adfeb0c7aed3a8b04b5959df030333e0976a60cca33db322c76c
revision_id: rev_762995e780dfd2289d1fc86427695b7dc13a536512de813f1badeee22e80301e
event_id: evt_4c1cad79795a464990237a9cf09b9cee9bc89765590c10b8072b05cfa6a0e443
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-03-01T02:57:35Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7611424094525620265](<https://juejin.cn/post/7611424094525620265>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 本文章是基于当前AI业务项目梳理的一份SSE流式结构，简单介绍了一下，当前我们实现的AI流式消息的思路，其中可能有很多不合理的地方，欢迎大佬指正和建议🌹
> 一、整体架构
> 二、流式消息字段
> 首先提供一段完整的处理的消息格式
> \[
>     \{
> "msg\_id"
> :
> "xxx"
> ,
> "content"
> : \[
>             \{
> "content"
> :
> "调用联网搜索工具，查询北京近期天气。"
> ,
> "is\_finished"
> :
> false
> ,
> "type"
> :
> "text"
> ,
> "type\_end"
> :
> true
> \},
>             \{
> "content"
> : \[
>                     \{
> "content"
> :
> "我来帮您查询北京最近的天气情况。"
> ,
> "is\_finished"
> :
> false
> ,
> "type"
> :
> "text"
> ,
> "type\_end"
> :
> true
> \},
>                     \{
> "content"
> :
> "联网搜索"
> ,
> "is\_finished"
> :
> false
> ,
> "params"
> : \{
> "click"
> :
> true
> ,
> "icon"
> :
> "https://xxxx/xxxx.png"
> ,
> "id"
> :
> "web\_search"
> ,
> "status"
> :
> "end"
> ,
> "data\_detail"
> : \{
> "input"
> :
> "北京天气 2026年2月13日"
> ,
> "output"
> : \[
>                                     \{
> "content"
> : \[
>                                             \{
> "desc"
> :
> "2026年02月13日北京天气预报"
> ,
> "source"
> :
> "搜狐"
> ,
> "title"
> :…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
