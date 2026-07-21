---
title: 我把本地文档 RAG 做成了可用系统：Flask + Vue3 + LangChain + FAISS（多知识库 + 流式输出）
date: 2026-03-12 11:11:52+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- RAG
- 大语言模型
- Python
- Docker
categories:
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
- RAG应用
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7616184939038572579
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:5b341fc23e6d3f740290b98b1d9ac3bd4591f066eb14758e5f3e21faa7c54d2b
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 64
captured_at: '2026-07-18T04:19:10.757447Z'
source_capture_sha256: sha256:d03917f41a3133dacfe65f74f02d245f43bb30ec6132e04ac9e13fc9301eef70
source_capture_chars_original: 2542
source_publication_excerpt_chars: 753
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_6758314faaa234ea601162732340301aeb2df8eeeb299d10f6fb2b16b64dc091
revision_id: rev_6fcdc1681ae037dd21033630fa49fc7a24fdbd4a14274ab691c1e4e40dd47ac9
event_id: evt_3af64558805897f885737cc3a4837d2241c6375122d1926f36c28a29ac9fdb19
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-03-12T03:11:52Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7616184939038572579](<https://juejin.cn/post/7616184939038572579>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 我把本地文档 RAG 做成了可用系统：Flask + Vue3 + LangChain + FAISS（多知识库 + 流式输出）
> 很多 RAG Demo 都停留在“能回答一次问题”，但真正要用起来，至少还要解决这几件事：
> 多个知识库隔离（不同业务、不同团队互不影响）
> 文档管理（上传、列表、删除、URL 入库）
> 多轮会话记忆（不仅是检索，还要记住上下文）
> 流式输出（边生成边展示，减少等待焦虑）
> 我把这些做成了一个完整项目：
> docs-rag-chat
> 。
> 技术栈是
> Flask + Vue3 + LangChain + FAISS
> ，后端支持按
> app\_id
> 隔离知识库，前端支持实时流式渲染答案。
> 项目地址：
> https://github.com/eagle1949/docs-rag-chat
> 项目图片：
> 1. 项目结构和整体链路
> 核心链路可以概括为：
> 文档入库：上传文件 / URL 抓取
> 文档切分：按 chunk 切成可检索片段
> 向量化存储：写入 FAISS
> 问答检索：相似召回 + LLM 生成
> 会话记忆：摘要 + 最近对话
> 流式返回：SSE token 推送到前端
> 简化架构：
> Vue3 Frontend
>   -&gt; Flask RAG API
>      -&gt; DocumentLoader \(md/txt/pdf/url\)
>      -&gt; DocumentSplitter \(chunk=500, overlap=50\)
>      -&gt; FAISS VectorStore \(Qianfan Embeddings\)
>      -&gt; ChatOpenAI \(Moonshot by default\)
>      -&gt; SummaryBufferMemory \(session level\)
> 2.…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
