---
title: 什么 AI 写 Android 最好用？官方做了一个基准测试排名
date: 2026-03-09 01:01:37+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- AI Agent
- 大语言模型
- Docker
categories:
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
- 云原生/容器
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7614897667961143347
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:6dea73bca304e5ecb69def4e008e60c012ad8ce7928238016ec7c03b32d60e28
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 32
captured_at: '2026-07-18T04:18:44.780677Z'
source_capture_sha256: sha256:8ee40c4a2405d10995a3c3360a7dca3c6364e5e07b5d67f090463fb6a0e1e86c
source_capture_chars_original: 4409
source_publication_excerpt_chars: 667
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7614897667961143347](<https://juejin.cn/post/7614897667961143347>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 近日，谷歌发布一个了
> Android Bench
> ，目的是衡量大语言模型在 Android 开发里的表现，
> 而结果上是 Gemini-3.1 pro 遥遥领先，这个结论你认可吗
> ？
> 从感性层面确实也挺好理解，毕竟谷歌的大模型跑自己的系统，有最好的 Score 不是很正常吗？但是从理性角度，我们需要知道这个 Bench 是如何测评出来结果
> 。
> Android Bench 的设计灵感来源于 SWE-bench，但专门针对 Android/移动端开发场景进行了定制，这在一定程度和之前
> 小红书的 SWE-Bench Mobile 测试大模型
> 类似，但是小红书更偏向真实业务场景，而 Android Bench 更倾向于通用场景的技能测试。
> Android Bench 采用了一个严格的
> 两阶段分离架构
> ：
> 阶段 1：推理 \(Inference / Agent\)
> 阶段 2：评估 \(Evaluation / Verifier\)
> 所以，从流程上你可以看出来，它的客观性在于
> 基于功能（Patch Verifier）而非形式的验证
> ，在这里 AI
> 不看过程看结果
> ， Android Bench 不会根据 AI 生成的代码是否与结果代码完全一致来打分，而是将 AI 生成的代码补丁（Patch）应用到真实的 Android 项目中，然后
> 运行项目自带的自动化测试套件来测试
> 。
> 当然，也就是 AI 修复了 Bug 并且通过了所有单元测试/集成测试，它就得分，所以也存在一些局限。
> 而为了保证这个这个基准的公正性，主要靠七个机制来维持：
> 1.…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
