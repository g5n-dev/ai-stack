---
title: 03:多 LLM 提供商统一接入：Provider 模式与 LiteLLM 实践
date: 2026-02-22 07:40:33+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- 大语言模型
categories:
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7608129931918409728
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:31d11d7c1e2334fc08e1a67149ac64a2eb22d1e5867e216e944cc02afacf4449
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 40
captured_at: '2026-07-18T04:17:33.288056Z'
source_capture_sha256: sha256:a660d54925d086c0856f7818e39a0bc300d8a6dbe512dc8b7606ceca7644fdde
source_capture_chars_original: 4156
source_publication_excerpt_chars: 800
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_ca61d17d93b4c832347b5f8383287501dcdc5c28002e9cd6437fdf58bd7b91ca
revision_id: rev_5cdd92405660e58671c2da1542c9ce080ebc6c0ce26b98a056b30656f4dfa753
event_id: evt_70d1b7f9d7ae60aafe12b4c5ba5f559cfb03b3bd77bc7bc8b32c88e002735d22
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-21T23:40:33Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7608129931918409728](<https://juejin.cn/post/7608129931918409728>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 引言
> AI 应用面临的一个核心挑战是如何优雅地支持多个 LLM 提供商。CountBot 通过 Provider 抽象模式 + LiteLLM 适配层，实现了对 9+ 种 LLM 提供商的统一接入。本文将深入分析这一设计。
> 架构设计
> 三层抽象
> AgentLoop
> ↓ 调用统一接口
> LLMProvider \(抽象基类\)
>     ↓ 具体实现
> LiteLLMProvider
>     ↓ 委托
> LiteLLM 库 → OpenAI / Anthropic / DeepSeek / Gemini / ...
> Provider 抽象基类
> class
> LLMProvider
> \(
> ABC
> \):
> def
> \_\_init\_\_
> \(
> self, api\_key, api\_base, default\_model, timeout=
> 120.0
> , max\_retries=
> 3
> \):
>         self.api\_key = api\_key
>         self.api\_base = api\_base
>         self.default\_model = default\_model
>         self.timeout = timeout
>         self.max\_retries = max\_retries
> @abstractmethod
> async
> def
> chat\_stream
> \(
> self, messages, tools=
> None
> , model=
> None
> ,
>         max\_tokens=
> 4096
> , temperature=
> 0.7
> , \*\*kwargs
> \) -&gt; AsyncIterator\[StreamChunk\]:
> pass
> 关键设计决策：
> 流式优先
> ：
> chat\_stream
> 返回
> AsyncIterator\[StreamChunk\]
> ，而非一…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
