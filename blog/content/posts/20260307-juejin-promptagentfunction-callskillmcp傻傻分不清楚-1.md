---
title: Prompt、Agent、Function Call、Skill、MCP，傻傻分不清楚？
date: 2026-03-07 02:49:40+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- MCP
- AI Agent
- Java
- 数据库
categories:
- AI 工程
- 数据
scenarios:
- AI/ML项目
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7614205951297732654
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:caa2738bd7458385e5f8b345bfabcc565dfdd3f1c7b2b73048ea82b3b5d395c8
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 44
captured_at: '2026-07-18T04:18:40.760524Z'
source_capture_sha256: sha256:232d8cff64c432c764b59c71a15c8d7b90077840d62e9a62c4e8aad819056151
source_capture_chars_original: 6000
source_publication_excerpt_chars: 800
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_e99fe83fd4043587ed5ec6ee87ceabdbd7d172f1bb3fce17ff7c79d600471a42
revision_id: rev_d9b2ffdb151b3941bd63b046e2ab5e21035814aa89982b4f54981b7f7b25f648
event_id: evt_3c3507e74fffe1a41175303220a8e2e8f88ee9fb656c2873c851a8f554b65def
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-03-06T18:49:40Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7614205951297732654](<https://juejin.cn/post/7614205951297732654>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 前言
> 最近AI越来越火了。
> 我发现里面有很多概念有些小伙伴有点分不清楚，比如：Prompt、Agent、Function Call、Skill、MCP等。
> 今天这篇文章专门跟大家一起聊聊这个话题，希望对你会有所帮助。
> 更多项目实战在项目实战网：
> java突击队
> 核心概念关系图
> 先上干货，这张图让你从整体上理解这五个概念是如何分层递进的：
> 一句话概括
> ：
> Prompt
> 是你跟AI说的“人话”
> Function Call
> 让AI能“动手干活”
> Agent
> 让AI会“思考规划”
> Skill
> 是AI的“职业技能证书”
> MCP
> 是AI世界的“USB接口”
> 下面我们一层一层拆开揉碎了讲，每层都有Java代码示例。
> 第一层：Prompt——和AI对话的“普通话”
> 1.1 什么是Prompt？
> Prompt（提示词）
> 就是你输入给AI的文本指令。
> 它就像你去餐厅点菜时说的“来一份宫保鸡丁”，AI就是那个服务员，听懂你的话然后给你上菜。
> 在Java里，调用AI模型的第一步就是构造Prompt。
> 我用最简单的Spring AI示例来演示：
> import
> org.springframework.ai.chat.ChatClient;
> import
> org.springframework.ai.chat.prompt.Prompt;
> import
> org.springframework.ai.chat.prompt.SystemPrompt;
> import
> org.springframework.ai.chat.prompt.UserPrompt;
> @Service
> public
> class
> AIService
> \{
> private
> final
> ChatClient chatClient;
> public
> AIService
> \(ChatClient chatClient\)
> \{
> this
> .chatC…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
