---
title: 我用 AI 撸了个开源"万能预览器"：浏览器直接打开 Office、CAD 和 3D 模型
date: 2026-04-07 15:28:00+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- AI Agent
categories:
- AI 工程
scenarios:
- AI/ML项目
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7625910143542525986
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:1fe2fd6e2432931f92207cb0fc4a1802f5e0ed2d00eb3cc4a6db9e4f5a6956a7
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 45
captured_at: '2026-07-18T04:19:30.231334Z'
source_capture_sha256: sha256:9faed431ac67d054e340250d40b3b8cd8bbe54e647c08858f8fdc0cc9908a3f4
source_capture_chars_original: 2192
source_publication_excerpt_chars: 751
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7625910143542525986](<https://juejin.cn/post/7625910143542525986>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 最近一直在深耕 AI Agent 与大模型应用，比如 JitKnow AI 知识库、JitWord协同AI文档、Pxcharts 超级表格，同时也持续在给大家分享 GitHub 上真正能落地、能解决实际问题的优质AI开源项目。
> 两周前发布了我们开源的文档预览SDK——jit-viewer。
> 目前在npm上已有 2.1k 的下载量，我们也在持续更新迭代，满足更多开发者的需求。
> github：
> github.com/jitOffice/j…
> 国内镜像：
> gitee.com/lowcode-chi…
> 在 AI Coding的帮助下，我加速了迭代频率，今天很高兴和大家分享Jit-Viewer最新版本 V1.3.0.
> 什么是 Jit-Viewer
> 简单来说，它是一个
> 纯前端的文件预览引擎
> 。不需要后端转换服务，不需要安装任何插件，几行代码就能让浏览器具备"专业软件"的预览能力。
> 过去我们 preview 文件，要么调用微软/Google 的在线接口（有隐私风险），要么自建转换服务（服务器成本高）。
> jit-viewer 的思路很直接：
> 把解析能力搬到浏览器端
> 。下面我就和大家分享一下最新版本的更新内容。
> 1. 支持CAD文件预览功能
> 事情的起因很简单：工程团队在处理设计稿交付时，总是要在微信里发"麻烦安装个 CAD 看图软件"或者"这个 3D 模型我截图给你"。
> 作为一位写过无数款文档编辑器、多维表格的开发者，我突然意识到——
> 为什么我们不能在浏览器里直接预览这些文件？
> 没有安装包，没有兼容性问题，打开链接就能看。这不应该是 2026 年的标配吗？
> 于是借助 AI， 我在 Jit-viewer sdk中支持了CAD文件的预览。
> 目前线上已提供demo测试，大家也可以体验测试一下。
> 2.…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
