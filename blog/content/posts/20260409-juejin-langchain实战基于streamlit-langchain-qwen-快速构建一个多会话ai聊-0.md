---
title: LangChain实战：基于Streamlit+ LangChain + Qwen 快速构建一个多会话AI聊天页面
date: 2026-04-09 05:36:14+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- RAG
- 大语言模型
- 机器学习
- Python
- 数据库
categories:
- 大模型
- 数据
scenarios:
- AI/ML项目
- 大语言模型
- RAG应用
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7626208064598573108
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:3060fac586f0f8c5553e6647fc1966e1c9c58ea49546b5beca5cb3a5f38f0152
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 57
captured_at: '2026-07-18T04:19:31.110951Z'
source_capture_sha256: sha256:8754c7df22cda383ac96299e121f6b08e7b1dae8bf6ba7882a2f7331fd1ef282
source_capture_chars_original: 5999
source_publication_excerpt_chars: 793
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_872376d7541613fc6743b19ac2e32df5bc0f79a23f2a7c8ef0a488c4de332816
revision_id: rev_5ac6f84a7e39a5144ed61915505c2f33251984cbbd2a9ab48f2654592853c452
event_id: evt_ce7f4721cad714e6aa7ab77b4b922587ba6ba3a53768a155fa8a6458d446e37f
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-04-08T21:36:14Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7626208064598573108](<https://juejin.cn/post/7626208064598573108>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 在大模型应用开发中，对话系统是最常见的场景之一。LangChain 作为大模型应用开发框架，在 v1.0 版本中进行了架构大重构，摒弃了旧版冗余组件，引入了更简洁、可扩展的 LCEL（LangChain 表达式语言），让开发者能更高效地构建对话应用。
> 本文将手把手教你，使用 Streamlit（前端交互）+ LangChain v1.0+（大模型调用与流程管理）+ 通义千问（大模型），实现一个功能完整、架构规范的多会话AI聊天页面，支持会话新建、切换、删除、清空，以及本地会话持久化、流式输出等核心功能，全程采用 LangChain v1.0+ 新版写法，彻底抛弃旧版 Chain 和 Memory 组件。
> 一、技术选型与核心优势
> 在开始编码前，先明确各技术栈的选型原因和核心优势，确保整个技术架构简洁、高效、可维护。
> 1. 前端：Streamlit
> Streamlit 是一款专为数据科学和机器学习开发者设计的 Web 应用框架，无需前端开发经验，用 Python 代码即可快速构建交互式页面。选择它的核心原因：
> 开发效率极高：几行代码就能实现聊天输入框、会话列表、消息展示等核心组件，无需编写 HTML/CSS/JS。
> 原生支持聊天组件：
> st.chat\_message
> 、
> st.chat\_input
> 可直接实现聊天界面，无需额外封装。
> 会话状态管理：
> st.session\_state
> 可轻松保存会话数据、当前选中会话等状态，刷新页面不丢失（配合本地文件持久化，实现长期保存）。
> 流式输出支持：通过
> st.empty\(\)
> 占位符，可轻松实现 AI 回复的“打字机效果”，提升用户体验。
> 2. 大模型框架：LangChain v1.0+
> LangChain v1.0+ 相比旧版（v0.x）有了根本性的架构优化，核心优势的是引入了 LCEL，让大模型调用流程更简洁、更灵活。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
