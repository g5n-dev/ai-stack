---
title: 1万美金的账单，烧麻了！bull这个skills让数据推理质量更好，更省！
date: 2026-03-06 07:31:16+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- AI Agent
- Docker
categories:
- AI 工程
scenarios:
- AI/ML项目
- 云原生/容器
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7613808397826719753
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:f3fd67bc07cdc702b7f3b0c22d1de3a23ed5e618026c7b4d8e7ee6282e76eec8
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 37
captured_at: '2026-07-18T04:18:37.806500Z'
source_capture_sha256: sha256:11d1cf55b3256e9000a128c2a5388d5c006c723be1cdc9643dde3b32ee7cb948
source_capture_chars_original: 3567
source_publication_excerpt_chars: 749
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7613808397826719753](<https://juejin.cn/post/7613808397826719753>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 原创：小姐姐味道（微信公众号ID：xjjdog），欢迎分享，转载请保留出处。
> 现在的Agent已经很聪明了
> 先说清楚一件事：2026年的AI Agent，不是2023年的ChatGPT。
> Codex、Claude Code、Cursor这些Agent，内置了大量工具能力。它们会用ripgrep搜代码、会分块读取大文件、会写Python脚本在本地执行、会用shell命令处理数据。不会傻到把一个10MB的日志文件一股脑塞进上下文。
> 但是，"聪明"和"够用"是两回事。
> Agent的内置能力是通用的：读文件、搜文本、跑脚本。当数据处理需求超出这些通用能力时，Agent就开始用笨办法——多轮对话、反复读文件、写临时脚本、一步步拼凑结果。每一轮都在消耗推理token。
> 这不是LLM笨，是Agent手里的工具不够专业。
> GitHub:
> github.com/agi-now/bul…
> Agent内置能力的天花板在哪
> 以下几个场景，是当前主流Agent用内置工具处理时，效率明显不足的：
> 1. 结构化数据的聚合分析
> Agent拿到一个5万行的NDJSON日志文件。要回答"哪个服务报错最多"。
> Agent的做法：写一段Python脚本，用json模块逐行解析，用dict做计数，排序输出。这个过程中，Agent需要：推理数据结构→编写脚本→执行→可能debug→读取输出→再推理。一个简单的GROUP BY，Agent可能要花3-5轮推理才搞定。
> 如果再追问"按小时统计错误趋势"、"关联另一个文件做JOIN"呢？Agent得重新写脚本，每多一个需求就多几轮推理。
> 每一轮推理都是token。问题不是单次贵不贵，是积少成多。
> 一个数据分析任务如果需要5轮推理，每轮消耗几千token用于思考和生成脚本。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
