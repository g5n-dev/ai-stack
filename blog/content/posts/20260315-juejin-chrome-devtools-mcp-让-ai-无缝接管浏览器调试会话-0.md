---
title: Chrome DevTools MCP 让 AI 无缝接管浏览器调试会话
date: 2026-03-15 01:07:53+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- MCP
- 命令行工具
categories:
- AI 工程
scenarios:
- AI/ML项目
- 命令行工具
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7616660062761943074
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:1c2e7e7da3a6fc6aebbad4393ec70fcf2d6e79d500f1361ab8e161256c235211
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 36
captured_at: '2026-07-18T04:19:15.572681Z'
source_capture_sha256: sha256:68f1c7bce5caf67e284ed0a602b680780427c82b73638081a1b0586cec0a203f
source_capture_chars_original: 1947
source_publication_excerpt_chars: 764
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7616660062761943074](<https://juejin.cn/post/7616660062761943074>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> Chrome DevTools MCP 让 AI 无缝接管浏览器调试会话
> Chrome DevTools MCP 服务器近期新增了一项开发者期待已久的功能：编码助手可以直接接入现有的浏览器会话。
> 借助这一能力，编码助手可以：
> 复用已登录的浏览器会话
> ：假设需要修复一个需要登录才能访问的问题，编码助手现在可以直接使用当前的浏览会话，无需再次登录。
> 接入活跃调试会话
> ：当在 Chrome DevTools 的网络面板中发现失败的请求时，可以选中该请求并让编码助手调查问题。同样的功能也适用于 Elements 面板中选中的元素。这种在手动调试与 AI 辅助之间无缝切换的能力，为调试流程带来了新的可能性。
> 自动连接功能是 Chrome DevTools MCP 连接 Chrome 实例的现有方式的补充。当然，以下方式仍然可用：
> 使用 Chrome DevTools MCP 专属的用户配置文件运行 Chrome（当前默认方式）
> 通过远程调试端口连接到正在运行的 Chrome 实例
> 在隔离的临时配置文件中运行多个 Chrome 实例
> 工作原理
> Chrome M144（当前处于 Beta 版本）新增了一项功能，允许 Chrome DevTools MCP 服务器请求远程调试连接。这一新流程建立在 Chrome 现有的远程调试能力之上。默认情况下，Chrome 中禁用远程调试连接，开发者需要先在
> chrome://inspect#remote-debugging
> 中明确启用该功能。
> 当 Chrome DevTools MCP 服务器配置
> --autoConnect
> 选项后，它会连接到活跃的 Chrome 实例并请求远程调试会话。为避免恶意滥用，每次服务器请求远程调试会话时，Chrome 都会向用户显示对话框请求许可。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
