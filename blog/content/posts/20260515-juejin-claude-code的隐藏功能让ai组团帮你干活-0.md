---
title: Claude Code的隐藏功能：让AI组团帮你干活
date: 2026-05-15 10:42:29+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- AI Agent
- 数据库
categories:
- AI 工程
- 数据
scenarios:
- AI/ML项目
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7639733278732894258
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:6073c56510ee34f2945156ff8d544a0757b8b1bbae076fc053e4aed51adc166b
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 26
captured_at: '2026-07-18T04:21:24.262233Z'
source_capture_sha256: sha256:49e3b38ec10fcbc07495d14cb529057b15619c7d7d10d03f38d65d25dff887d9
source_capture_chars_original: 4392
source_publication_excerpt_chars: 800
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7639733278732894258](<https://juejin.cn/post/7639733278732894258>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 大家好，我是子昕。
> 上周我用Claude Code分析一个老项目，十几万行代码那种。
> 我让它搜支付模块相关的逻辑，它翻了几十个文件，搜完之后我发现对话上下文已经被撑满了。
> 后面再问问题，回答质量直线下降，有效信息全被搜索结果淹没了。
> 这个问题其实一直存在：
> AI的上下文窗口就那么大，塞太多中间过程进去，后面的对话质量必然下降
> 。
> 后来我反应过来，Claude Code有两个专门解决这个问题的功能：
> Subagent
> 和
> Agent Teams
> 。
> 很多人不知道，但用过之后真的回不去了。
> 简单说：
> Subagent（子智能体）
> ：让Claude派一个“分身”去干活，干完把结果带回来，你的主对话保持干净
> Agent Teams（智能体团队）
> ：让多个子智能体组成团队，分工协作，适合复杂的多模块任务
> 今天把这两个功能掰开了讲。
> 一、Subagent：派个分身去干活
> 解决什么问题
> 你在和Claude对话，遇到一个子任务——比如搜索代码、审查某个模块、调查一个bug。
> 如果让Claude直接在当前对话里做，所有搜索过程、中间文件内容全堆在上下文里，越聊越臃肿。
> Subagent的思路：
> 不在主对话里做，派一个独立的子智能体去做
> 。
> 它有自己独立的上下文，干完活把结果返回给主Claude，主Claude看完之后把关键信息总结给你。你的主对话从头到尾是干净的。
> 可以同时派多个，互不干扰。
> 怎么用
> 直接跟Claude说就行：
> 帮我搜索项目中所有支付相关的代码，不要污染当前对话
> 或者更直接：
> 用子智能体帮我做个代码审查，看看 src/auth/ 目录有没有安全隐患
> Claude会自动判断需不需要派子智能体，自动选择合适的类型，自动生成任务描述。你不需要写任何参数。
> 一个容易疑惑的点
> ：子智能体看不到你和主Claude之前的对话内容，但它能访问你的整个项目目录——能读文件、搜代码、执行命令。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
