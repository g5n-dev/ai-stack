---
title: 04:工具系统设计：从抽象基类到 JSON Schema 的完整实现
date: 2026-02-22 07:40:33+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- AI Agent
- 大语言模型
categories:
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7607989878778019892
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:3e40aec3725d9fb3c29802f290c74efe1def5f643abcbdd9a62c2cf4aa4918f2
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 34
captured_at: '2026-07-18T04:17:33.275286Z'
source_capture_sha256: sha256:558d65c97304c5b49753600f76203b60629e00d8305f537fd8c507b1addfdcd0
source_capture_chars_original: 4099
source_publication_excerpt_chars: 800
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_f237f41dabc6ad08e5b600f528a75e6ccaccfdb7ee694d9a231ed2dc23f89f02
revision_id: rev_b48fac7772c3e0a9a2c8ee9977282d86b1c5e6ea5b91b2743f0175520c35db99
event_id: evt_90f6437657f8f2a73b3c7bbb625cd185add49948cf5645129002174609f8d8ef
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-21T23:40:33Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7607989878778019892](<https://juejin.cn/post/7607989878778019892>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 引言
> 工具调用（Function Calling）是现代 AI Agent 的核心能力。CountBot 实现了一套完整的工具系统，包含 12+ 内置工具，支持参数验证、审计日志和动态注册。本文将深入分析其设计与实现。
> 工具抽象基类
> class
> Tool
> \(
> ABC
> \):
>     \_TYPE\_MAP = \{
> "string"
> :
> str
> ,
> "integer"
> :
> int
> ,
> "number"
> : \(
> int
> ,
> float
> \),
> "boolean"
> :
> bool
> ,
> "array"
> :
> list
> ,
> "object"
> :
> dict
> ,
>     \}
> @property
> @abstractmethod
> def
> name
> \(
> self
> \) -&gt;
> str
> : ...
> @property
> @abstractmethod
> def
> description
> \(
> self
> \) -&gt;
> str
> : ...
> @property
> @abstractmethod
> def
> parameters
> \(
> self
> \) -&gt;
> dict
> \[
> str
> ,
> Any
> \]: ...
> @abstractmethod
> async
> def
> execute
> \(
> self, \*\*kwargs:
> Any
> \) -&gt;
> str
> : ...
> 设计要点：
> 使用
> @property
> +
> @abstractmethod
> 确保子类必须提供元数据
> parameters
> 返回标准 JSON Schema，与 OpenAI Function Calling 格式完全兼容
> execute
> 统一返回
> str
> ，简化结果处理
> 参数验证系统
> Tool 基类内置了递归的 JSON Schema 验证器：
> def
> validate\_params
> \(
> self, params:
> dict
> \[
> str
> ,
> Any
> \]
> \) -&gt;
> list
> \[
> str
> \]:
>     s…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
