---
title: '手把手从 0 诠释大模型 API 的本质: Tools + MCP + Skills'
date: 2026-02-15 07:07:48+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- MCP
- AI Agent
- 大语言模型
- TypeScript
- 命令行工具
categories:
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
- 命令行工具
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7606548472221990954
aliases:
- /posts/20260215-juejin-手把手从-0-诠释大模型-api-的本质-tools-mcp-skills-1/
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:10cf6d9beaf261e4fdabb9268289a6241f944d7fb85e27e460e7aa4f29ccd71f
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 42
captured_at: '2026-07-18T04:17:19.849153Z'
source_capture_sha256: sha256:611ea625722c717f32e6639ca15aa270b7ead1314c651e9c544854b3211e731c
source_capture_chars_original: 3811
source_publication_excerpt_chars: 681
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7606548472221990954](<https://juejin.cn/post/7606548472221990954>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 本文写于 2026 年 02 月 15 日.
> 如今 AI Agent 的各种新概念层出不穷:
> Tools
> MCP
> Skills
> 许多人都会有这样的疑问: Tools 和 MCP 有什么区别? 我用了 MCP 还需要 Tools 吗? Skills 是取代 MCP 的吗? 本文会从 LLM API 的底层设计开始, 一步步介绍 Tools 和 MCP 的区别, 手动实现一个非常简易的 MCP \(简易到你会觉得"就这?"\), 最后简单提一下 Skills.
> 几个重要事实
> 大模型是无状态的
> , 它对你们的过往对话一点都没有记忆. 每次调用 LLM API, 都是一次全新的请求, 就像换了一个完全陌生的人说话.
> 大模型本身的开发\(或许\)很难, 需要很强的数学知识. 但是大模型应用开发不难, 做纯工程开发的传统程序员也可以很快上手.
> MCP 和 Skills 都是纯工程层面的设施, 和 AI 毫无关系. 也就是说, 在这两个概念出现以前, 你完全可以自己实现一套类似的机制, 不需要 LLM API 支持.
> 基于以上几个事实, 本文会选择 Anthropic API 来解释. 因为 OpenAI 的 Responses API 提供了一个叫做
> previous\_response\_id
> 的参数,
> 很容易误导人以为 LLM 本身有记忆功能
> . 但实际上 LLM 是没有记忆的, 这个
> previous\_response\_id
> 并不会给 LLM 使用, 而是 OpenAI 的服务层面的工程设施, 相当于 OpenAI 帮我们存了历史记录, 然后发给 LLM.…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
