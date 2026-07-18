---
title: LangChain中的RAG Loader：从网页加载文档并实现智能分割与检索
date: 2026-03-11 03:01:56+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- RAG
- 大语言模型
- JavaScript
- 数据库
categories:
- 大模型
- 数据
scenarios:
- AI/ML项目
- 大语言模型
- RAG应用
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7615484384251707407
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:2f95c4edfa03914d185cf0ab09e0053f5c03899d9a41cbb5ab2670e3b910b157
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 39
captured_at: '2026-07-18T04:18:51.081459Z'
source_capture_sha256: sha256:57f426788af0fc4bc13461333f71424ad9ccf48a3bd7d16688c6db6478c61014
source_capture_chars_original: 5846
source_publication_excerpt_chars: 788
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7615484384251707407](<https://juejin.cn/post/7615484384251707407>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 在当今的AI开发领域，
> R
> e
> t
> r
> i
> e
> v
> a
> l
> −
> A
> u
> g
> m
> e
> n
> t
> e
> d
> G
> e
> n
> e
> r
> a
> t
> i
> o
> n
> （
> R
> A
> G
> ）
> Retrieval-Augmented Generation（RAG）
> R
> e
> t
> r
> i
> e
> v
> a
> l
> −
> A
> ug
> m
> e
> n
> t
> e
> d
> G
> e
> n
> er
> a
> t
> i
> o
> n
> （
> R
> A
> G
> ）
> 技术已成为构建智能应用的核心组成部分。它通过从外部来源检索相关信息来增强大语言模型的生成能力，避免了模型幻觉问题，并提升了响应的准确性和相关性。其中，
> 文档加载（Loader）
> 和
> 分割（Splitter）
> 是 RAG 流程中的关键步骤。本文将深入探讨
> LangChain
> 框架中这些组件的使用方式，结合实际代码示例，分享从网页加载文档、进行语义分割、嵌入向量存储到最终检索并回答问题的完整实践过程。通过这个分享，希望能帮助大家更好地理解和应用 RAG 技术在实际项目中的落地。
> RAG Loader的基础概念
> RAG的核心在于“检索增强生成”，它将知识库中的信息作为模型输入的补充来源。Loader是负责从各种数据源加载原始文档的工具，而Splitter则将这些文档切割成更小的、可管理的片段（chunks），以便后续的向量嵌入和检索。
> 在LangChain中，Loader支持多种文件类型和来源，包括本地文件、数据库、网页等。这使得开发者可以灵活地从互联网或内部系统中提取数据。特别是社区模块@langchain/community，它提供了丰富的Loader实现，涵盖了PDF、CSV、JSON等多种格式。对于网页内容，CheerioWebBaseLoader是一个强大工具，它利用Cheerio库（一个后端CSS选择器库）来解析HTML，就像操作前端DOM节点一样，允许开发者指定选择器来提取特定元素。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
