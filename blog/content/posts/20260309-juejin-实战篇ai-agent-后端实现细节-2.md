---
title: 实战篇：AI Agent 后端实现细节
date: 2026-03-09 10:32:53+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- RAG
- AI Agent
categories:
- AI 工程
scenarios:
- AI/ML项目
- RAG应用
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7615014502552502310
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:09c449ddbf5cf938c39a3af99081705dbbe3d38ab2ada6312f9bc2490eed99dc
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 19
captured_at: '2026-07-18T04:18:44.514536Z'
source_capture_sha256: sha256:a7a17e9add848113b2849ed434c2b8713a78e9a0616f8d8d5f867fd4ef2f36cd
source_capture_chars_original: 5475
source_publication_excerpt_chars: 800
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7615014502552502310](<https://juejin.cn/post/7615014502552502310>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 本节补充第四章中后端相关的实现细节，包括多模型适配、RAG 管线、生成 Pipeline、以及 JSON 容错处理。
> 4.1 多模型提供商的统一接入
> Agent 开发中，你几乎不可能只用一个模型。不同模型擅长不同的事，而且模型厂商的定价、速率限制、区域可用性都在变。设计一个可插拔的多模型架构很有必要。
> Provider 注册表模式
> 用 Map 做一个模型到 Provider 类的映射：
> // ai.service.ts
> private
> providers =
> new
> Map
> &lt;
> string
> ,
> new
> \(
> config
> :
> AIProviderConfig
> \) =&gt;
> AIProvider
> &gt;\(\[
>   \[
> 'gpt-4o'
> ,
> OpenAIProvider
> \],
>   \[
> 'claude-sonnet-4-5-20250929'
> ,
> ClaudeProvider
> \],
>   \[
> 'doubao-seed-2-0-pro'
> ,
> DoubaoProvider
> \],
>   \[
> 'gemini-2.0-flash'
> ,
> GeminiProvider
> \],
> \]\);
> // 根据模型名获取 Provider 实例
> getProvider
> \(
> modelId
> :
> string
> \):
> AIProvider
> \{
> const
> ProviderClass
> =
> this
> .
> providers
> .
> get
> \(modelId\);
> if
> \(!
> ProviderClass
> \)
> throw
> new
> Error
> \(
> \`Unsupported model:
> $\{modelId\}
> \`
> \);
> const
> config =
> this
> .
> getConfigForModel
> \(modelId\);
> return
> new
> ProviderClass
> \(config\);
> \}
> 动态 API Key 路由
> 不同前缀的模型走不同的 A…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
