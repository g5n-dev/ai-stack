---
title: Langchain入门到精通0x01：结果解析器
date: 2026-03-11 03:01:56+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- 数据库
categories:
- 数据
scenarios: []
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7615506537834889226
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:bb3059f6ebd06282d3996310500c365244bc82d74eaca03c6c542351d22be08e
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 24
captured_at: '2026-07-18T04:18:51.177871Z'
source_capture_sha256: sha256:974be6b05aa8d5ab6ecddd8fc159944f3a8499f48668747be79e2b4e2370a004
source_capture_chars_original: 3177
source_publication_excerpt_chars: 785
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_24231413a81f4c7dc8b17cb6343785d6cc5c9c60af4ab42605cd9df2ab3023f6
revision_id: rev_4795f5de10a20b78a36a8bbf7a7f0d4e1efb2bfe8579784bc70120469fa617e9
event_id: evt_3b14259e172f4532180bf0a16b13b74e63bf119e76dd734206612f021df37d17
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-03-10T19:01:56Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7615506537834889226](<https://juejin.cn/post/7615506537834889226>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> Result Parser
> 上一篇
> 学习了什么是langchain和prompt templete。那么，很多时候大模型直接返回的数据并不能满足各个项目的具体需求，
> 如何将大模型自由、非结构化的文本输出，转化为程序可稳定、高效处理的结构化数据
> ？
> langchain提供了几个标准的接口来实现这个目的。今天就挨个来学习下几个常用的解析器接口。
> StrOutputParser
> 字符串解析器
> 。用于清理模型输出，去除多余换行等，返回纯净字符串。它是最常用的“兜底”解析器。
> parser
> = StrOutputParser\(\)
> chain
> = prompt | model | parser
> JsonOutputParser
> Json格式解析器。
> parser
> = JsonOutputParser\(\)
> chain
> = prompt | model | parser
> CommaSeparatedListOutputParser
> 逗号分隔列表解析器
> 。适用于生成标签、关键词、选项列表等场景。比如生成csv格式的常常也用到这个。
> parser
> = CommaSeparatedListOutputParser\(\)
> chain
> = prompt | model | parser
> DatetimeOutputParser
> 日期解析器
> 。
> 将人类模糊、灵活的自然语言时间描述，精准、可靠地转换为程序可计算的
> datetime
> 对象
> 。
> parser
> = DatetimeOutputParser\(\)
> chain
> = prompt | client | parser
> PydanticOutputParser
> 基于Pydantic模型的结构化解析
> 。这是
> 企业级应用中最核心、最推荐的解析器
> 。它通过定义严格的Pydantic数据模型来确保输出结构的质量和类型安全。
> # 1.…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
