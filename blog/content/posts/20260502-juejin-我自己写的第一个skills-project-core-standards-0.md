---
title: 我自己写的第一个skills--project-core-standards
date: 2026-05-02 11:11:10+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- AI Agent
- TypeScript
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
external_url: https://juejin.cn/post/7634860379345092617
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:586c02e28efb3951f63793fc6aa6b16246bf13dadf1c61507c65c926a59e5532
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 38
captured_at: '2026-07-18T04:19:46.806024Z'
source_capture_sha256: sha256:bdd0bf50de1b5a29fee67a71d3b327f463411bd92bc5b06ca479678ac279eb8d
source_capture_chars_original: 2633
source_publication_excerpt_chars: 516
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7634860379345092617](<https://juejin.cn/post/7634860379345092617>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 背景
> 用 AI 写代码一段时间后，我发现一个很反直觉的问题：我们其实已经有一些“最佳实践”，但它们无法复用：
> A 项目调教好的 AI，在 B 项目完全失忆
> 规则散落在 prompt / 文档 / IDE 配置中，无法版本化
> 每次新项目，都在重复“驯化 AI”
> 既然代码可以用 Git 管理、用 NPM 分发，为什么 AI 规范还停留在“复制粘贴”？
> 本质问题是：
> 我一直把规则当“文本”，而不是“代码”。
> 把规则当代码看
> 如果把 AI 规则当作代码，它应该具备三个能力：
> 可组合（Composable）
> → 不同规则可以拆分、复用
> 可分发（Distributable）
> → 像 npm 包一样安装
> 可演进（Versioned）
> → 有版本、有变更记录
> 否则它就不是工程资产，而只是碎片化经验沉淀。一个规范，如果不能被 install，那它本质上只是不成体系的经验。
> Skill 的最小抽象模型
> 那问题来了：
> 一个“可安装的 AI 规范”，在工程上到底长什么样？
> 最小结构其实非常简单：
> my-skill/
> ├── SKILL.md
> ├── rules/
> ├──
> package
> .json
> 但真正的关键不是结构，而是它解决的问题。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
