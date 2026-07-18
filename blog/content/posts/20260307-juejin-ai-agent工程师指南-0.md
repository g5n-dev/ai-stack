---
title: ai-agent工程师指南
date: 2026-03-07 22:28:45+08:00
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
external_url: https://juejin.cn/post/7614065532690268206
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:89156bf086fdf06e185436c7632388195e74b92f28e8d92dff8bd2c25befc0e0
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 13
captured_at: '2026-07-18T04:18:40.443405Z'
source_capture_sha256: sha256:fa8535dea7cec1c674eaf9fcd6d3eac5320f91d7c998a2af6a9eadd6c51a9de9
source_capture_chars_original: 1217
source_publication_excerpt_chars: 798
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7614065532690268206](<https://juejin.cn/post/7614065532690268206>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 一些基本概念
> 1 Zero-shot &amp; Few-shot 是什么？
> 1. Zero-shot（零样本）
> 不给例子，直接让模型做。
> 不提供任何参考样例
> 只告诉模型
> 任务是什么
> 完全靠模型本身能力去理解、推理
> 例子
> 把下面句子分类成积极 / 消极：这部电影太好看了！
> 这就是
> zero-shot
> 。
> 2. Few-shot（少样本 / 小样本）
> 给几个例子，再让模型做。
> 给
> 1～10 个左右的示例
> 告诉模型：
> 我要你像这样输出
> 模型照着格式、逻辑去做
> 例子
> 分类：今天心情很好 → 积极分类：这部电影好无聊 → 消极分类：这家店味道超赞 →？
> 这就是
> few-shot
> 。
> 一句话总结
> Zero-shot：不给例子，直接干。
> Few-shot：给几个例子，照着干。
> 2 RAG 是什么？
> RAG = Retrieval-Augmented Generation\*\*\*\*检索增强生成
> 一句话：
> 先从外部资料里查相关内容 → 再把查到的内容喂给大模型 → 让模型基于真实资料回答。
> 3 Embedding 模型 是什么？
> 一句话：
> 把文字、图片、声音等信息，变成一串数字（向量），让计算机能 “看懂、比较、计算”。
> 1. 核心作用
> 人理解文字靠语义，计算机只认数字。Embedding 模型做的就是：
> 把 “语义” → 变成 “向量”
> 比如：
> “苹果” → \[0.1, 0.5, -0.2, …\]
> “香蕉” → \[0.12, 0.48, -0.19, …\]
> “汽车” → \[ -0.8, 0.1, 0.3, …\]
> 语义越接近，向量越接近。
> 2. 它能干什么？（最常见用途）
> 搜索
> 搜 “好吃的水果”，能找到苹果、香蕉，而不是汽车。
> 推荐
> 你看了 A 文章，给你推语义相似的 B 文章。
> 知识库问答 / RAG
> 把文档变成 embedding，用户提问也转成 embedding，
> 找最相似的段落
> 。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
