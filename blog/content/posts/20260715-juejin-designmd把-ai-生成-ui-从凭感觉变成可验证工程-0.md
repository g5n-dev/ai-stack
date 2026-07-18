---
title: DESIGN.md：把 AI 生成 UI 从凭感觉变成可验证工程
date: 2026-07-15 11:26:59+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- AI Agent
- 命令行工具
categories:
- AI 工程
scenarios:
- AI/ML项目
- 命令行工具
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7662319290113294376
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:8d1ddc8173a433aaeab99d73bc630b2f6da45a110fb2c99eda8ee309253d401e
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 32
captured_at: '2026-07-18T04:21:54.891069Z'
source_capture_sha256: sha256:86920be6f2ff68df88d7156922b4208c1b12e529e32e25c4416ab9da140939ca
source_capture_chars_original: 6000
source_publication_excerpt_chars: 785
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7662319290113294376](<https://juejin.cn/post/7662319290113294376>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 让 AI 写一个能运行的页面，今天已经不难。
> 难的是让它连续写五个页面，仍然像同一个产品；换一次会话、换一个 Agent、改一轮需求之后，颜色、圆角、层级、留白和交互状态仍然不漂移。
> 很多团队的做法，是在 Prompt 里反复补形容词：
> 做得现代一点、简洁一点、高级一点，像一线 SaaS 产品。
> 这类描述的问题不是不够长，而是不够具体。Google 的
> DESIGN.md
> 哲学文档直接指出，类似 “modern、clean、trustworthy、premium” 的词只描述了一个模糊区域，模型最后往往会落到这个区域的平均值，于是生成一个似曾相识的通用界面。
> DESIGN.md
> 解决的，正是这种“让模型自己补全设计”的问题。
> DESIGN.md 到底是什么
> 按 Google Labs 当前公开规范，
> DESIGN.md
> 是一种面向 Coding Agent 的视觉身份描述格式。一个文件包含两层内容：
> 最小结构大致如下：
> ---
> version: alpha
> name: Signal Desk
> colors:
>   primary:
> "#182230"
> tertiary:
> "#5B5BD6"
> surface:
> "#FFFFFF"
> rounded:
>   sm: 6px
> components:
>   button-primary:
>     backgroundColor:
> "\{colors.tertiary\}"
> textColor:
> "\{colors.surface\}"
> rounded:
> "\{rounded.sm\}"
> ---
> ## Overview
> 像一本运维记录册与安静的航空仪表盘：紧凑、克制、事实优先。
> 它不是一个用渐变和悬浮卡片制造氛围的营销后台。
> ## Do&amp;#x27;s and Don&amp;#x27;ts
> - Do 让发布状态先于次要指标被看见。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
