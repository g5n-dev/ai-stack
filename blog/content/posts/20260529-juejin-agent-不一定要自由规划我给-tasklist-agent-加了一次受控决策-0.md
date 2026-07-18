---
title: Agent 不一定要自由规划：我给 Tasklist Agent 加了一次受控决策
date: 2026-05-29 08:16:20+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- MCP
- AI Agent
categories:
- AI 工程
scenarios:
- AI/ML项目
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7645147525191696422
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:6eed5d9413cb11285e48a14d2a964019803ce8634347f74dec2e5f3e1ba9aec6
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 41
captured_at: '2026-07-18T04:21:33.107203Z'
source_capture_sha256: sha256:9efeecb860af6c33892ffc82e5245cb822e0b46cd1d262452df36485ae180dac
source_capture_chars_original: 6000
source_publication_excerpt_chars: 746
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7645147525191696422](<https://juejin.cn/post/7645147525191696422>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 本文基于
> AI Mind
> 项目真实实现整理。
> GitHub：
> github.com/HWYD/ai-min…
> 对应代码版本：
> v0.1.1
> AI Mind 是一个正在持续升级的 Next.js AI Chat 项目。它从最基础的本地聊天开始，逐步加入流式协议、工具调用、MCP、Skill 和 Agent 能力。
> 如果这篇文章或者 AI Mind 项目对你有所帮助，也欢迎到 GitHub 给项目点个 Star，这会是对我继续更新很大的鼓励。
> 很多 Agent 文章会默认走向一个方向：让模型自己规划、自己选工具、自己决定下一步，最好还能循环执行。但在这个版本里，我选择了一个更保守的方案：
> 不给 Tasklist Agent 无限自由，只在原有固定流程里增加一次受控的规划决策。
> 在 v0.1.0 中，AI Mind 已经有了第一个受控 Tasklist Agent：用户通过
> /tasklist + @docs://versions/\*.md
> 显式引用版本方案后，系统会读取方案、生成任务清单草稿、执行结构校验，并在必要时最多自动修正一次。
> 这个设计的好处是边界清楚：入口明确、资源明确、工具明确、自动修正次数也明确，普通聊天链路不会被 Agent 逻辑污染。
> 但它的问题也很明显：流程太固定。
> 如果版本方案信息不足、上下文缺失，或者用户输入已经超出 Tasklist Agent 的处理边界，v0.1.0 只能继续往下生成，或者直接失败。它缺少一个中间判断：
> 当前信息到底适不适合继续生成任务清单？
> 所以 v0.1.1 的主题可以概括为：一次受控规划决策。它只在原有受控链路里增加一次规划决策（Planning Decision）：让模型在运行时白名单允许的 5 类动作中选择下一步。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
