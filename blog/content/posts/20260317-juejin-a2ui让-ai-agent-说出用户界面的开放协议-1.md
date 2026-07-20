---
title: A2UI：让 AI Agent "说出"用户界面的开放协议
date: 2026-03-17 12:14:38+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- MCP
- AI Agent
- 大语言模型
- JavaScript
- Docker
categories:
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
- 云原生/容器
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7618032821014446099
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:708dff77c182980b6b48359108633121b9f7240f7b68f8c126840f6729b2524a
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 29
captured_at: '2026-07-18T04:19:21.177205Z'
source_capture_sha256: sha256:01f288a34c10cfcb3a053be4b94719b78461ad4daca7fdf4a82a7c2c81e15d70
source_capture_chars_original: 5694
source_publication_excerpt_chars: 771
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_918b55c9c43e4346ee158cc3e905ca30aaf77b7a341ae1166183a5769057431b
revision_id: rev_75f3c1ab43ab111650bc76875dc0996cdf777b2c5f673e560b9a5fa96e434a1a
event_id: evt_905fad8334b4955bd0dbba0ecf535253e9f72fcec20281ed200e59b13d4368b3
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-03-17T04:14:38Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7618032821014446099](<https://juejin.cn/post/7618032821014446099>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 引言：Agent 时代的 UI 困境
> 想象这样一个场景——你对一个 AI 助手说："帮我订一张明天晚上 7 点的两人桌。" 如果 Agent 只能回复文本，接下来将是一连串低效的对话："请问哪一天？""什么时间？""几位？"……一个本可以用一个表单瞬间解决的事情，变成了五六个回合的文字乒乓球。
> 更好的方式显然是：Agent 直接生成一个表单界面，带有日期选择器、时间选择器、人数输入框和确认按钮。用户在 UI 上操作，一次提交，搞定。
> 但这件"显然更好"的事情，在技术上却极其棘手。Agent 可能运行在远程服务器上，甚至跨越组织的信任边界。它不能直接操控你的 UI，只能发送消息。传统的方案——在 iframe 中嵌入 Agent 返回的 HTML/JavaScript——不仅笨重、风格割裂，还引入了严重的安全隐患。
> Google 发起的开源项目
> A2UI（Agent-to-User Interface）
> 就是为了解决这个问题而生的。它定义了一种让 Agent "说 UI" 的通用语言：Agent 发送声明式的 JSON 消息来描述界面的意图，客户端应用用自己原生的组件库来渲染。安全如数据，表达如代码。
> 一、A2UI 是什么？一句话理解核心理念
> A2UI 是一个
> 声明式 UI 协议
> ，而不是一个框架。它的核心思想可以拆成三层：
> Agent 生成一段 JSON，描述"我想展示一个标题、一个日期选择器和一个按钮"。这段 JSON 通过任意传输通道（A2A 协议、WebSocket、SSE 等）到达客户端。客户端的 A2UI 渲染器读取 JSON，将抽象的组件描述映射为自己代码库中的原生组件——可以是 Flutter Widget、Angular Component、Lit Web Component 或 React 组件。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
