---
title: 🚀 Vercel AI SDK 使用指南：流式传输 (Streaming)
date: 2026-02-11 03:18:02+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- TypeScript
categories: []
scenarios: []
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7605107459065708590
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:066a8ab17fda441aeefe87556fc0954e5f31ce1580bdb9cba41547c70442dd80
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 37
captured_at: '2026-07-18T04:17:11.723300Z'
source_capture_sha256: sha256:1095c56d2ad69aaa5d87f380e8b2a3fa8995226354b6490c5dfc2308d98e6cf8
source_capture_chars_original: 3591
source_publication_excerpt_chars: 777
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7605107459065708590](<https://juejin.cn/post/7605107459065708590>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 🌟 为什么选择流式传输 \(Streaming\)？
> 在传统模式（Blocking UI）下，如果大模型生成一篇 500 字的文章需要 10 秒，用户就必须在白屏前干等 10 秒。 而在
> 流式模式（Streaming UI）
> 下，模型生成第一个字时，前端就能立即显示。
> 传统模式
> ：请求 -&gt; 等待10s -&gt; 一次性显示全部 -&gt; 结束
> 流式模式
> ：请求 -&gt; 0.5s显示首字 -&gt; 持续蹦字 -&gt; 结束
> Vercel AI SDK 的核心
> streamText
> 函数让这一过程变得极度简单。
> 🛠️ 准备工作
> 1. 环境要求
> Node.js 18+
> 一个国内大模型的 API Key（本文以
> DeepSeek
> 为例，Kimi/通义千问同理）
> 2. 初始化项目
> 创建一个文件夹并初始化：
> Bash
> mkdir
> ai-streaming-demo
> cd
> ai-streaming-demo
> npm init -y
> 3. 安装核心依赖
> 我们需要安装
> ai
> （核心库）和
> @ai-sdk/openai
> （兼容层）。
> 为什么装 openai？因为绝大多数国内大模型（DeepSeek, Moonshot, Qwen）都完美兼容 OpenAI 的接口协议！这是最通用的方案。
> Bash
> npm install ai @ai-sdk/openai dotenv
> # 如果使用 TypeScript \(推荐\)
> npm install -D tsx typescript @types/node
> 💻 实战代码：接入国内大模型
> 我们将创建一个名为
> index.ts
> 的文件，演示如何在 Node.js 环境下通过流式传输调用 DeepSeek。
> 第一步：配置“万能适配器”
> 国内大模型通常提供“OpenAI 兼容接口”，我们只需要修改
> baseURL
> 和
> apiKey
> 。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
