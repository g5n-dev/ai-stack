---
title: 一天一个开源项目（第76篇）：Cangjie Skill —— 将书本知识炼金为 AI 智能体可执行的技能
date: 2026-04-18 15:02:15+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- MCP
- AI Agent
- 大语言模型
categories:
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7629654731762090027
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:54ed3a2cae2aaddba6931154272250cdd22672da38c290570fbce8d14c4137ae
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 53
captured_at: '2026-07-18T04:19:36.663735Z'
source_capture_sha256: sha256:d8fdfeccd6e7d54082ab70b66508e83bf02573a3118276789db2c2c5452e7b31
source_capture_chars_original: 1801
source_publication_excerpt_chars: 797
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7629654731762090027](<https://juejin.cn/post/7629654731762090027>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 1. 简介
> Cangjie Skill
> （仓颉技能）是一个极具创新性的开源知识管理与 AI 提示词工程项目。它的核心目标是\*\*“把书变成技能”\*\*。
> 在传统的知识获取中，我们阅读一本书，记下笔记，但这些内容往往是静止的、易忘的。Cangjie Skill 提供了一套完整的 methodology（方法论）和工具链，旨在将非虚构类高质量书籍（如《穷查理宝典》、《原则》、巴菲特致股东信等）中的核心方法论、决策模型和智慧，结构化地提炼成 AI 智能体可以理解并执行的
> Skill（技能包）
> 。
> 2. 为什么需要 Cangjie Skill？
> 在 AI 时代，我们面临两个痛点：
> 上下文爆炸与丢失：
> 将整本书扔给 LLM（大语言模型）虽然可行，但往往会造成“信息淹没”或“中间丢失”现象，AI 很难精准提取并应用书中的深层逻辑。
> 从认知到行动的鸿沟：
> 传统的读书笔记是给“人”看的叙事，而 AI Agent 需要的是结构化的“工具”。
> Cangjie Skill 通过
> 知识解耦
> ，将庞杂的书本内容拆解为独立、模块化、可检索的技能单元，让 AI 在处理具体问题时，能够像调用 API 一样调用这些人类智慧。
> 3. 核心特性
> RIA-TV++ 方法论：
> 这是项目的灵魂，基于赵周的“拆书”法（RIA）进行了 AI 时代的升级：
> R \(Reading\)
> ：阅读原著，获取原始信息。
> I \(Interpretation\)
> ：重构解读，建立逻辑联系。
> A \(Appropriation\)
> ：拆为己用，设计应用场景。
> TV \(Triple Verification\)
> ：三重验证（跨域交叉证据、预测力、非显而易见性），确保提炼出的技能是真知灼见而非空洞废话。
> ++ \(Agent Execution\)
> ：增加 AI 执行步骤（Execution）和边界定义（Boundary），使其成为可落地的代码式指令。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
