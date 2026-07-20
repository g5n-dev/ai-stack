---
title: OpenClaw 深度解析（八）：Skill 系统——让 LLM 按需学习工作流
date: 2026-03-10 07:05:59+08:00
draft: false
entry_kind: auto
tags:
- 掘金
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
external_url: https://juejin.cn/post/7614889731939909659
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:afa5a3b876f77501813bb9cf5531b34a17cec68e6f565957e1ba65abb8d186cb
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 40
captured_at: '2026-07-18T04:18:48.347438Z'
source_capture_sha256: sha256:3622b4ca876f287ee29a5ba743aa26501526ccf3fd995809f0cf246a9b052e23
source_capture_chars_original: 1208
source_publication_excerpt_chars: 645
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_d2a664459ef1fa91656e597c7f902009841a5e94350d41a45ca43ab3034b68b9
revision_id: rev_e5b2b484ff3c004193657c7a3004b52b890d0531a3d9dab74e9fc2c29f3fafea
event_id: evt_e2d7112bc943d34b36d8966887128b59c920f84b327851f3a9c6a9b6f47ff95f
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-03-09T23:05:59Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7614889731939909659](<https://juejin.cn/post/7614889731939909659>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 场景：AI 怎么知道用哪个命令？
> 你问 OpenClaw：「帮我查一下上海今天的天气。」
> AI 回复了一段
> curl "wttr.in/Shanghai?format=3"
> 的命令，执行后准确拿到了天气数据。
> 但这里有个问题值得深究——LLM 是一个语言模型，它并不天然知道"查天气要用
> wttr.in
> "，也不知道"管理 GitHub PR 用
> gh
> CLI"，更不知道"控制 Spotify 用
> spotify-player
> "。
> 显然有什么东西在"教"它这些。但如果把 50 个工具的完整文档全部塞进系统提示里，光文档本身就会把上下文窗口撑满。
> 这就是
> Skill 系统
> 要解决的问题：
> 文档规模问题
> ：50+ 个工具，每个都有详细文档——全部预加载会把 LLM 的上下文撑爆。
> 工具可用性问题
> ：
> gh
> CLI 没装、
> spotify-player
> 没配置环境变量——向 LLM 暴露不可用的工具毫无意义还会引发错误。
> 工作流标准化问题
> ：工具的用法需要让 LLM 精确理解和遵循，不能靠 LLM "猜"。
> 用户体验问题
> ：用户想通过
> /weather 上海
> 直接触发，而不是每次都打一段自然语言。
> 一、SKILL.md：给 LLM 看的文档格式
> 为什么是 Markdown 而不是代码？
> Skill 不是一段程序——它是"给 LLM 看的操作手册"。LLM 理解自然语言和 Markdown，所以最合理的格式就是带 YAML frontmatter 的 Markdown 文件。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
