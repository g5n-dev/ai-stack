---
title: Agent 系列（16）：工具链设计——让 LLM 用对工具的五个原则
date: 2026-06-08 23:04:00+08:00
draft: false
entry_kind: auto
tags:
- 掘金
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
external_url: https://juejin.cn/post/7649040940744605759
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:e1c3132429029d63c59164e30072dbe3523ce4f5879f0fe9d0270359112a5064
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 35
captured_at: '2026-07-18T04:21:37.672853Z'
source_capture_sha256: sha256:d7ba7cd6ebfa0d325bf43db23636747acbfd9fe4aa9d618b5909fd2b18904609
source_capture_chars_original: 5821
source_publication_excerpt_chars: 673
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7649040940744605759](<https://juejin.cn/post/7649040940744605759>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 工具文档是写给 LLM 的，不是写给人的
> 你有没有写过这样的工具文档：
> @lc\_tool
> def
> get\_data
> \(
> query:
> str
> \) -&gt;
> str
> :
> """Get data."""
> ...
> 这对人类来说是糟糕的文档，对 LLM 来说更糟——它不知道这个工具做什么、什么时候调它、传什么参数。
> 工具设计有三条核心维度：
> 描述质量（LLM 选不选你）、错误处理（出错时崩不崩）、粒度设计（参数好不好提取）
> 。本文用实验数据说话。
> Demo 1：描述质量——真正影响工具选择的条件
> 对比同一个天气工具的两个版本：
> # 版本 A：模糊
> @lc\_tool
> def
> weather\_vague
> \(
> city:
> str
> \) -&gt;
> str
> :
> """Get data."""
> ...
> # 版本 B：精准
> @lc\_tool
> def
> weather\_precise
> \(
> city:
> str
> \) -&gt;
> str
> :
> """Get current weather for a city.
>
>     Returns temperature \(Celsius\) and condition \(sunny / cloudy / rainy / unknown\).
>     Use this whenever the user asks about weather, temperature, or sky conditions
>     for a specific city. Pass the city name as a plain string, e.g.…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
