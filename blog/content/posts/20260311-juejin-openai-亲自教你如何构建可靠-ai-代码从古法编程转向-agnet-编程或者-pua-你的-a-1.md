---
title: OpenAI 亲自教你如何构建可靠 AI 代码，从古法编程转向 Agnet 编程，或者 PUA 你的 AI
date: 2026-03-11 00:55:38+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- AI Agent
- 大语言模型
- 命令行工具
categories:
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
- 命令行工具
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7615455795723976739
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:5e1111016939274ab37b461ba7a61639ee2cb6ca4a49e73e3f87425b5fa4a4ed
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 53
captured_at: '2026-07-18T04:18:51.369351Z'
source_capture_sha256: sha256:428897fc8445d69f1beb105542ed1ceddda01d03e1a766c4439b8fbb421b2b3c
source_capture_chars_original: 5468
source_publication_excerpt_chars: 712
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_7bebd772b1695d9d78513ff6c5f901359e4c0bc55ddfdddfd34e9b2d478a1351
revision_id: rev_7dba9ab4ef1ee46d56658bc3d635ad6268dcc60847adcecc23d360364a7a1176
event_id: evt_6afb0e48d00f32cfd61284e7d3248969dc938f7c7477824bcca770ec24726a6d
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-03-10T16:55:38Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7615455795723976739](<https://juejin.cn/post/7615455795723976739>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 其实在不少 AI Coding 的内容下，一直有不少人说，AI 写的代码不够好用，甚至感觉很傻，是不是自己的大模型能力不行？为什么感觉我的 AI 和别人的 AI 好像不是一个东西？这个效果怎么可以上生产？
> 实际上还真不是，虽然说不同大模型的能力上限确实是一个原因，但是实际
> 你对 AI 工程的管理方式，还有你使用的 Agent 工具，也是影响 AI 编程结果的核心因素
> ，例如：
> 同样是 Claude ，但是它在 Claude Code、Cursor、Antigravity 、Copilot、OpenCode、Kiro 和 Junie 里的表现可是天差地别，孰好孰坏就不用我多说了吧？
> 另外
> 你是在单纯 Prompt AI 还是管理 AI 工程
> ，整个生产体验也会不一样，用 AI 不是说完几句话就可以不管等结果，比如常见的 SDD （Spec-Driven Development）的开发管理方式，它就需要很多文档来进行迭代、记录和索引：
> 当然，我们今天要说的是 OpenAI 的 AI 工程实践，讲的是：
> OpenAI 如何使用 Codex ，在五个月内完全不使用任何人工代码来构建并发布一款产品
> 。
> 首先 OpenAI 明确了一个核心观点：
> 软件工程的核心正在从「写代码」转向「构建 AI 执行系统」（harness），工程师不再是“写代码的人”，而是设计 AI 工作环境的人
> 。
> 他们主要是做了一个真实的生产实验，通过 3 名工程师，在五个月的时间，完全通过 codex 完成一个 100 万行代码的项目，期间所有代码、测试、CI、文档都由 Codex agents 自动生成，而人主要负责定义规则、结构和流程。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
