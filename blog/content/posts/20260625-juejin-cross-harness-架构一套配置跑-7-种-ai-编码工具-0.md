---
title: Cross-Harness 架构——一套配置跑 7 种 AI 编码工具
date: 2026-06-25 08:12:06+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- MCP
- AI Agent
- Python
- Rust
- TypeScript
- Go
- 命令行工具
categories:
- AI 工程
scenarios:
- AI/ML项目
- 命令行工具
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7654919203225550867
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:4f1a712cae7b0bb53f3119e64eb5a5cce8bdbe420ca4cd2578be369148f88381
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 35
captured_at: '2026-07-18T04:21:46.197461Z'
source_capture_sha256: sha256:377022bdc8df70b89bea5bc08f1bb3555e11e81c46e4890b90fb13cc6dd11a8a
source_capture_chars_original: 6000
source_publication_excerpt_chars: 796
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_67a95e2b185ce157085e79a0c356310abc526788f08ae3ebfc5c5ee2b964cdfe
revision_id: rev_48bd5db4d0a961b6f5bcf20a560e5d672e0b606ed9a014ee1278a0037c27b18b
event_id: evt_bbeb0daa4f6de982f8435b3c477daddde85b1a6ab1c7f49e1692d6ce19457bf3
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-06-25T00:12:06Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7654919203225550867](<https://juejin.cn/post/7654919203225550867>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> Cross-Harness 架构——一套配置跑 7 种 AI 编码工具
> 前四篇讲的能力（token 管理、memory、learning、安全）都是在一个工具内的优化。但现实是：
> AI 编码工具百花齐放
> 。你的团队里可能有人用 Claude Code、有人用 Cursor、有人用 Codex——每个工具的配置格式完全不同，最佳实践无法跨工具共享。
> ECC 从一开始的 "Everything Claude Code" 进化成了 "ecc-universal"——一个跨 7 种 AI 编码工具的"Agent 操作系统"。它的核心设计问题是：
> 怎么让同一套 agents/skills/rules/hooks 在不同 harness 上运行？
> 源仓库：
> affaan-m/everything-claude-code
> 碎片化问题
> 2026 年中，主流的 AI 编码工具（agent harness）至少有这些：
> 工具
> 配置方式
> 约束格式
> Claude Code
> .claude/
> + CLAUDE.md + settings.json
> Skills: Markdown, Hooks: JSON
> OpenAI Codex
> .codex/config.toml
> + agents/\*.toml
> TOML + Markdown
> Cursor
> .cursor/rules/
> + hooks.json
> Markdown + JS hooks
> Gemini CLI
> .gemini/GEMINI.md
> 单文件 Markdown
> Zed
> 编辑器内配置
> 编辑器 API
> OpenCode
> TypeScript 插件
> TS/JS
> Copilot CLI
> .github/copilot-instructions.md
> Markdown
> 同一个"写代码前先写测试"的规则，在每个工具里要写一遍、格式各不相同。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
