---
title: 零成本本地大模型！用 Next.js + Ollama + Qwen3 打造流式聊天应用
date: 2026-03-17 01:17:58+08:00
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
external_url: https://juejin.cn/post/7617728986828816411
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:0d6f781d5d4362d00122ca9ba0e1194a4be40fdf6a388e81a1e4b59c8c91c686
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 44
captured_at: '2026-07-18T04:19:22.207059Z'
source_capture_sha256: sha256:9e01b3580e8cf53912cecb021fc7585930f25866fdaaf9e371535bf1293277b1
source_capture_chars_original: 6000
source_publication_excerpt_chars: 750
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_97f71b612c5f8c2cfd91a2ea0ad677d042d191f96b018339376d32b246a735d6
revision_id: rev_5c0574c45e6e21cb49b74562d8cd194aa466d5881aaa94f29e4f678b43a03d58
event_id: evt_adc1f3c21440a7edba86e39da09c71b898f5436301e6072f9a78106b517b3b1e
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-03-16T17:17:58Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7617728986828816411](<https://juejin.cn/post/7617728986828816411>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 本文基于
> AI Mind
> 项目真实实现整理。
> GitHub：
> github.com/HWYD/ai-min…
> 对应代码版本：
> v0.0.1
> AI Mind 是一个正在持续升级的 Next.js AI Chat 项目。它从最基础的本地聊天开始，逐步加入流式协议、工具调用、MCP、Skill 和 Agent 能力。
> 如果这篇文章或者 AI Mind 项目对你有所帮助，也欢迎到 GitHub 给项目点个 Star，这会是对我继续更新很大的鼓励。
> 大家好！今天我来给大家分享一个非常实用的技术实现：如何在本地零成本搭建一个可以流式输出的 AI 聊天应用。不需要昂贵的 API 密钥，也不需要复杂的配置，跟着我一步步来，你也能拥有属于自己的本地 AI 助手！
> 一、先看效果
> 最终我们能实现这样一个功能：
> 在本地运行大模型（Qwen3:4B）
> Next.js 作为后端服务，实现流式转发
> 前端实时展示 AI 的响应，打字机效果拉满
> 二、准备工作
> 1. 安装并启动 Ollama
> Ollama 是一个非常优秀的本地大模型运行工具，支持各种主流开源模型。
> 下载安装：
> 访问
> Ollama 官网
> 下载对应系统的安装包，Windows/macOS/Linux 都支持。
> 验证安装：
> 安装完成后，打开终端运行：
> ollama --version
> 如果看到版本号，说明安装成功啦！
> 2. 下载 Qwen3:4B 模型
> Qwen 是阿里开源的系列模型，Qwen3:4B 体积小、速度快，非常适合在普通电脑上运行。
> 在终端中运行：
> ollama pull qwen3:4b
> 等待下载完成后，我们可以测试一下：
> ollama run qwen3:4b
> 如果能正常和 AI 对话，说明模型已经准备好了！按
> Ctrl+C
> 退出。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
