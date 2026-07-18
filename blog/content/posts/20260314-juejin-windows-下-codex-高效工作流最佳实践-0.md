---
title: Windows 下 Codex 高效工作流最佳实践
date: 2026-03-14 13:30:56+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- AI Agent
- Python
- Java
- Kotlin
- 命令行工具
categories:
- AI 工程
scenarios:
- AI/ML项目
- 命令行工具
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7616660809600516134
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:9a8a0dbd0de7e56c1479ca6547ba2c14def06f345def3e381feacdc4f66df58f
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 25
captured_at: '2026-07-18T04:19:14.173457Z'
source_capture_sha256: sha256:a0c86a1ac700e494a3a2ea5b86d101ed406efb42c0d7ef0d839e742901eed2bc
source_capture_chars_original: 6000
source_publication_excerpt_chars: 703
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7616660809600516134](<https://juejin.cn/post/7616660809600516134>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 舍弃今日，只为明朝。我喜欢痛苦，因为痛苦意味着，生命中那些不完美的地方正在被修补。
> 本文系笔者在阅读
> 《OpenAI Codex 最佳实践》
> 的基础上，补充了部分个人心得。以话题列表的方式展开。
> Codex 不是 Chatbot，而是 AI Agent。不要把它当作临时性的对话助手，它就像是一名小组成员，一位中级软件工程师，需要时间来培养。在初始阶段，他对项目、代码、任务一无所知，随着慢慢了解和提升，处理起需求来也会更加得心应手。
> 我现在更习惯把 Codex 看成一个驻留在终端里的初级到中级开发搭档：它擅长
> 阅读文件、编辑代码、执行命令、总结问题
> ，但要向着什么目标改、是否值得改、改动边界在哪里、是否符合团队规范，最后仍然需要开发者自己把关。只要这个角色定位明确，很多期待落差就会自然消弭。
> 因此，在与他交流的过程中，要格外注意
> Prompt（提示词）的质量
> ，不要问空泛抽象的问题，例如“为什么这个脚本报错”。问题越模糊，对 AI 思考的约束就越弱，得到精确回答的概率就越低。
> 因此，我想讨论的第一个话题是 ——
> 如何撰写高质量的提示词。
> GCCO
> —— 高质量 Prompt 的写作公式
> AI Agent 背后的大模型，掌握了人类几千年历史以来全部信息，其认知储备远超地球上任何一个自然人。这固然是好事，他无所不知，无所不晓。不论我们问什么问题，都能得到答案。但能力太过强大、知识太过丰富，没有边界的 AI 就像一把双刃剑，这在一些场景下并非是好事。如果提问者的问题不够明确，很容易把 AI 引导到错误的方向上越走越远，不仅无法完成正常的任务，还会空耗 token，造成时间和金钱的双重损失。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
