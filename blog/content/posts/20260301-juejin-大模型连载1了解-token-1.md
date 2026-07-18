---
title: 大模型连载1：了解 Token
date: 2026-03-01 23:04:57+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- 自然语言处理
categories:
- AI 工程
scenarios:
- AI/ML项目
- 自然语言处理
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7611830146090008622
aliases:
- /posts/20260302-juejin-大模型连载1了解-token-3/
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:d690c75d4f25914f57b36d84a99a95b0d88eb71da272d4aa4e2f83061702ad98
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 15
captured_at: '2026-07-18T04:18:26.563883Z'
source_capture_sha256: sha256:fa3489de71e1cdc9d2d4f70bcf3b073deaabf851926debfc57880252ed3f3487
source_capture_chars_original: 2327
source_publication_excerpt_chars: 758
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7611830146090008622](<https://juejin.cn/post/7611830146090008622>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 可以说，学习自然语言处理、大模型、Transformer 任何一个技术，都离不开 token这个概念。
> 本专栏就从这个最基础的概念开始讲起。
> 多年前，第一次接触到自然语言处理模型 BERT。当时在评估这个模型的性能时，领导说这个模型的性能需要达到了 200 token 每秒，虽然知道这是一个性能指标，但是对 token 这个概念却不是很清晰。
> 因为当时接触视觉模型多一些，在视觉模型的性能评估中，有一个关键指标叫做 fps（Frames Per Second），通俗理解就是一秒钟可以处理的图片数。
> fps 数值越大，说明模型吞吐性能越好.
> 而在语言或者文本模型中，模型处理的不再是图片，而是一个个的文字（单词），这其中，token 便是一个最基础的概念了。
> 作为本专栏的第一篇文章，有必要先来学习一下到底什么是 token？
> 什么是 token？
> 在计算机相关领域中，token 通常是指一串
> 字符或符号
> 。
> 比如微信公众平台的密钥，就被称作一个 token，其实就是一长串的字符串。
> 在人工智能领域，尤其是自然语言处理\(Natural Language Processing, NLP\)领域中， "token" 指的是
> 处理文本时所能处理的最小单元或基本元素
> 。
> 它可以是一个单词、一个词组、一个标点符号、一个子词或者一个字符。
> 目前很多大模型的收费定价都是以 token 为单位，比如 OpenAI 的 GPT4 模型的收费标准为：1K 个 token 收费 0.01 刀。
> 如果你使用 OpenAI 提供的 GPT4 接口做程序开发，你需要给他们付费。
> 假设你做文本生成的任务，让模型帮你写小作文，这个收费标准大概就是写 1k\(1024\)个字，就要收你 0.01 刀（7分钱）。
> 如何理解 token ？…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
