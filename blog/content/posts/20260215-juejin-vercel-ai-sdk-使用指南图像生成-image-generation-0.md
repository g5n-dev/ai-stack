---
title: 🚀 Vercel AI SDK 使用指南：图像生成 (Image Generation)
date: 2026-02-15 08:49:57+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- TypeScript
categories: []
scenarios: []
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7606224197803261971
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:2e7688816621b176b399f4a0b0e51eca6ca6dc1b1b23765c89afc1e99ec320f1
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 44
captured_at: '2026-07-18T04:17:19.685801Z'
source_capture_sha256: sha256:77089b107921f55b320fba1f90971a0d0898020e0c5d5f17aacd405b15c274b5
source_capture_chars_original: 3213
source_publication_excerpt_chars: 800
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7606224197803261971](<https://juejin.cn/post/7606224197803261971>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 在 AI 应用开发中，除了文本对话，
> 图像生成
> 也是一个非常热门的需求。Vercel AI SDK Core 在 v6 版本中提供了标准化的
> generateImage
> 函数，让你能够用统一的 API 调用 DALL-E 3、Google Imagen、Midjourney \(via Fal\) 等多种顶级图像模型。
> 本文将带你深入了解如何使用 Vercel AI SDK 进行图像生成，涵盖基础用法、尺寸控制、批量生成以及错误处理。
> 🛠️ 前置准备
> 首先，确保你已经安装了
> ai
> SDK 和对应的模型提供商库（这里以 OpenAI 为例）：
> Bash
> npm install ai @ai-sdk/openai
> Ensure you have your API key configured \(e.g.,
> OPENAI\_API\_KEY
> in your
> .env
> file\).
> 1. 基础用法：生成第一张图片
> generateImage
> 是核心函数。你只需要指定模型和提示词（prompt），即可获取生成的图像数据。
> TypeScript
> import
> \{ generateImage \}
> from
> 'ai'
> ;
> import
> \{ openai \}
> from
> '@ai-sdk/openai'
> ;
> import
> fs
> from
> 'fs'
> ;
> async
> function
> main
> \(
> \) \{
> const
> \{ image \} =
> await
> generateImage
> \(\{
> model
> : openai.
> image
> \(
> 'dall-e-3'
> \),
> prompt
> :
> '一只戴着赛博朋克眼镜的猫，在霓虹灯闪烁的东京街头'
> ,
>   \}\);
> // image 对象包含 base64 和 uint8Array 两种格式
> console
> .
> log
> \(
> 'Image generated success…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
