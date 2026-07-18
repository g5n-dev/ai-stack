---
title: Vercel Serverless 调国内 AI 接口 504？Edge Runtime 救了我
date: 2026-05-02 02:57:46+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- RAG
categories:
- AI 工程
scenarios:
- AI/ML项目
- RAG应用
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7634711670124216370
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:2d3e351b852e98cbe9db998fb4fad4e4919f350cdfe775baa508ab7f4e17a847
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 48
captured_at: '2026-07-18T04:19:46.620175Z'
source_capture_sha256: sha256:7908ddf974fa943df8118d56536a29858a5c4638f40e7fbd9e99375954081a3a
source_capture_chars_original: 5093
source_publication_excerpt_chars: 800
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7634711670124216370](<https://juejin.cn/post/7634711670124216370>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> Mobile 端 AI 对话请求在 Vercel 上稳定 504 超时，本地却秒回。CORS 报错是假的，区域配置也没用。最终发现是 Vercel Serverless（AWS Lambda）到国内 DashScope 的网络出口根本不通。一行
> export const runtime = "edge"
> 切到 Cloudflare 边缘网络，3 秒完成。这篇文章把排查过程、根因分析和解决方案一次性讲清楚。
> 0. 前景提要：项目架构与问题背景
> 先交代项目架构，方便理解后续为什么 Web 端和 Mobile 端表现不同。
> 项目结构
> My-Notion/
> # pnpm workspace Monorepo
> ├── apps/
> │   ├── web/
> # Web 端（Next.js）
> │   └── mobile/
> # Mobile 端（Expo / React Native）
> ├── packages/
> │   └── ai/
> # AI 核心逻辑（共享包）
> │       ├── server/
> #   streamChat、streamRAG、ConvexDataSource...
> │       ├── config/
> #   模型配置、Base URL
> │       ├── tools/
> #   WebSearch 等工具
> │       └── rag/
> #   向量检索逻辑
> └── services/
>     └── ai/
> # AI 网关（Hono），独立部署到 Vercel
> ├── api/
> #   Vercel Serverless / Edge 入口
> └── src/
> #   路由、Convex 数据源、Sentry
> 为什么 Mobile 不直接用 Web 端的 API
> Web 端的 AI 路由（
> /api/chat
> 、
> /api/rag-stream
> ）…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
