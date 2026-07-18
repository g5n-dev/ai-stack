---
title: Codex 工程化实践指南：深入理解 AGENTS.md、SKILL.md 与 MCP
date: 2026-03-14 23:04:01+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- MCP
- AI Agent
- Kotlin
- 命令行工具
- 数据库
categories:
- AI 工程
- 数据
scenarios:
- AI/ML项目
- 命令行工具
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7616666752521404416
aliases:
- /posts/20260315-juejin-codex-工程化实践指南深入理解-agentsmdskillmd-与-mcp-2/
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:1384196cac5977d8c8d18c734704dfaa6aeb88952c542a64f042c16bf9d49e99
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 43
captured_at: '2026-07-18T04:19:14.421176Z'
source_capture_sha256: sha256:6b1482c4754e95495292d1741397e50ab86a87b5890990207ef01d3b07cc138c
source_capture_chars_original: 4377
source_publication_excerpt_chars: 682
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7616666752521404416](<https://juejin.cn/post/7616666752521404416>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> AI 就像自动驾驶，其价值并非让没摸过方向盘的新手上路开车，而在于为熟练的驾驶者节约精力和时间。
> 在 Codex 的设计中，有三个非常关键的概念：
> AGENTS.md
> SKILL.md
> MCP（Model Context Protocol）
> 如果把 Codex 看成一个
> “AI 工程师”
> ，那么这三个概念相当于：
> 概念
> 角色
> AGENTS.md
> 团队开发规范
> SKILL.md
> 可复用工作流
> MCP
> 外部系统接口
> 注意这里的“团队开发规范”不是指人类工程师所组成的团队，而是包含 AI Agent 工程师在内的团队。
> 这三个组件共同构成了
> AI 工程协作的基础设施
> 。
> 本文将系统介绍这三个概念，并重点讨论：
> 它们分别是什么
> 解决了什么问题
> 如何在真实工程中使用
> 有哪些实践技巧
> 一、AGENTS.md：给 AI 写的工程手册
> 1.1 AGENTS.md 是什么
> 当我们让 AI 修改代码时，经常会遇到这样的问题：
> AI 修改了不该修改的模块
> AI 写的代码不符合团队规范
> AI 不知道项目架构
> AI 重复犯同样的错误
> 原因其实很简单：
> AI 并不了解该项目的设计规则、编码规范。
> 在真实团队中，新人工程师加入项目时，通常会阅读：
> 设计文档
> 需求定义书
> 架构说明
> coding style
> PR 规范
> 这些信息帮助新人快速理解项目。Codex 也是一样的。于是 OpenAI 引入了 AGENTS.md。
> 简单来说：
> AGENTS.md 是写给 AI agent 的工程文档。
> 它的作用类似于：
> 团队开发规范
> 项目背景文档信息文档
> 但对象不是人类，而是 AI。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
