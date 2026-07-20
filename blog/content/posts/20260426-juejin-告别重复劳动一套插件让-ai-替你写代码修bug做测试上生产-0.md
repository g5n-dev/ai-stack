---
title: 告别重复劳动：一套插件让 AI 替你写代码、修Bug、做测试、上生产
date: 2026-04-26 21:29:00+08:00
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
external_url: https://juejin.cn/post/7632872949415067658
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:b3c72f7bcdba6368c913cbe65c4539d7fc945705c5cada7b113ba8d2ff8c165c
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 34
captured_at: '2026-07-18T04:19:41.821770Z'
source_capture_sha256: sha256:12ab2a237f7027f7ad84b253d28c5df6aaae201d0ec566cedb85e079ab7b6be6
source_capture_chars_original: 5333
source_publication_excerpt_chars: 602
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_5f9aac0f56fbf3e6808390e79c57c3ff7fe133b7d6d0b76728715471ab5e32de
revision_id: rev_800fc567b93e740b113e76ee03e5bac53e5bdb90270f4c08e6d85dee461a08e3
event_id: evt_d043d08d795614f2a3a25a0f99d751c413b0ff6ad705d88c524f960da42a560d
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-04-26T13:29:00Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7632872949415067658](<https://juejin.cn/post/7632872949415067658>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> Claude Code 团队 AI 插件实践：从新人上线到全栈自动化的渐进式指南
> 特别鸣谢
> ：本文由
> 南京大翼航空
> 团队实践沉淀而成，感谢团队在 AI 辅助研发领域的持续探索与投入。
> 后续规划
> ：本文为 dw 插件生态的总览。后续将为每个 skill 单独撰写详细教程文章，涵盖实战案例、配置细节和踩坑经验，敬请关注。
> 本文涉及的研发规范体系均基于 Claude Code 的
> 插件机制
> 实现。插件是 Claude Code 官方提供的扩展方式，支持自定义命令、Skill、Hook、Agent 等，是目前团队级 AI 研发规范的推荐落地形态。
> 开篇：我们为什么要做这套插件
> 在团队引入 Claude Code 做 AI 辅助开发后，我们很快遇到了几个共性问题：
> 新人上手陡峭
> ：不知道有哪些 skill、怎么装、怎么用
> AI 改动污染主分支
> ：直接在当前分支让 AI 改代码，心里不踏实
> 重复踩坑无沉淀
> ：同一个 Bug 换了个人又让 AI 从头排查
> 全栈流程割裂
> ：后端接口、前端页面、测试各跑各的，契约对不齐
> 命令安全无保障
> ：担心 AI 一个
> rm -rf /
> 把环境搞崩
> 于是我们设计了一套团队级插件
> dw
> ，核心思路是
> Skills + Agent Team
> ：Skills 封装可复用的研发流程，Agent Team 负责多角色协作编排，配合 9 个渐进式 Skill 覆盖完整研发链路。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
