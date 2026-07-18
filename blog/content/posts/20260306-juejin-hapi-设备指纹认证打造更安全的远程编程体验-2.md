---
title: HAPI + 设备指纹认证：打造更安全的远程编程体验
date: 2026-03-06 09:25:00+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- AI Agent
- TypeScript
- 数据库
categories:
- AI 工程
- 数据
scenarios:
- AI/ML项目
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7613772968724643875
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:2902310749e4868095b3c0daddcc0f24b815004b50e13f320547a67b9fc9ff5b
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 26
captured_at: '2026-07-18T04:18:38.147454Z'
source_capture_sha256: sha256:eff516d723083ef4caf9a98bbcd5dc16f77ed89bdb96dcaf5828ad80ec6828d0
source_capture_chars_original: 4666
source_publication_excerpt_chars: 775
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7613772968724643875](<https://juejin.cn/post/7613772968724643875>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 最近在用 HAPI 这个去中心化 AI 代理平台，体验了"Vibe Coding"的自由感——在咖啡馆、徒步时也能远程控制本地开发环境。但在实际使用中发现了安全隐患：原生的 JWT Token 认证在多设备场景下缺少设备级管控。于是我 fork 了项目，新增了设备指纹认证功能，实现"设备 + Token"的双因素验证。
> 这篇文章分享从使用者到贡献者的完整实践过程，包括 HAPI 项目介绍、安全问题分析、设备指纹认证的前后端实现，以及实际部署经验。
> HAPI 是什么
> HAPI 是一个去中心化的 AI 代理平台，支持"Vibe Coding"理念——随时随地自由编程，AI 代理在后台为你工作。
> 核心特性
> Vibe Coding 理念
> 去徒步、去喝咖啡，或者只是放松一下。你的 AI 代理在后台为你工作，只有在需要你确认时，才会通过即时通讯应用通知你。
> 去中心化架构
> 每个用户运行自己的 hub，数据留在本地。不像其他云服务把你的代码和会话存储在中心化服务器上，HAPI 让你完全掌控数据主权。
> 远程控制
> 通过 PWA 或即时通讯应用（如 Telegram）访问本地开发环境。会话驻留在你的电脑上，手机只是一个窗口。本地就是原生 Claude Code 或 Codex，外出时切换到手机，双空格键瞬间切回本地。
> 即时通讯集成
> 距离与控制的完美平衡。通过 Telegram 或其他应用，只在真正需要你输入时才通知你。
> 技术栈
> TypeScript + Hono 框架 + SQLite，单二进制部署，零配置启动。
> 架构设计
> graph TB
>     subgraph remote\["远程访问"\]
>         phone\["📱 手机端&lt;br/&gt;PWA应用"\]
>         im\["💬 即时通讯&lt;br/&gt;Telegram等"\]
>     end…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
