---
title: 'MCP tool design: Practical approaches and tradeoffs | Amazon Web Services'
date: 2026-07-09 23:40:17+08:00
draft: false
entry_kind: auto
tags:
- 博客与播客
- MCP
- AI Agent
- 大语言模型
- 生成式 AI
- 命令行工具
- 数据库
categories:
- 大模型
- 数据
scenarios:
- AI/ML项目
- 大语言模型
- 命令行工具
source: blogs_podcasts
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://aws.amazon.com/blogs/machine-learning/mcp-tool-design-practical-approaches-and-tradeoffs
aliases:
- /posts/20260710-blogs_podcasts-mcp-tool-design-practical-approaches-and-tradeoffs-0/
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:09ae401cf008fb69d3ecd0e7fe625a02c39b997df4c7b7871f5467b126eb95e4
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 73
captured_at: '2026-07-18T04:21:52.989917Z'
source_capture_sha256: sha256:892c937a2315d5d250f682bc49b2b047923d9c24b90286a15e9c706461d2fe07
source_capture_chars_original: 5749
source_publication_excerpt_chars: 769
source_truncation_reason: historical_capture_limit,historical_publication_excerpt_limit
observation_id: obs_2e309060a5831bee97a688e85e84ac47e98c931a1145ed0756c20784f718485d
revision_id: rev_af6d0111bcd2be92f992b2f0e65069be3217d6c031e5811b560342dd09d83ced
event_id: evt_c5bbf95f84a9b169c6d5f467c2dec089a65be7277fb52c30fe26a41e2bdd1890
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: blogs\_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/mcp-tool-design-practical-approaches-and-tradeoffs](<https://aws.amazon.com/blogs/machine-learning/mcp-tool-design-practical-approaches-and-tradeoffs>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> When Model Context Protocol \(MCP\) tools underperform, the cause is rarely the protocol itself but the tool design. Many teams start by exposing an existing API as-is and trusting the agent to figure out the rest. It is a natural way to extend APIs to agentic systems and generative AI coding tools. For straightforward use cases, it can work. But often it does not.
>
> You must design your tools for how large language models \(LLMs\) and agentic systems work. Without this, you risk failed tool calls, wrong parameter values, and retries that waste context and degrade performance. In this post, we show where MCP tool design goes wrong and how to fix it with practical context engineering approaches.
>
> Two problems are behind most of these failures. The first is bloat .…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
