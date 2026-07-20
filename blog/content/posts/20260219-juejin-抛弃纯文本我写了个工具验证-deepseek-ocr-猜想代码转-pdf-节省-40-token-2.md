---
title: 抛弃纯文本？我写了个工具验证 DeepSeek-OCR 猜想：代码转 PDF 节省 40% Token
date: 2026-02-19 13:39:39+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- RAG
- 大语言模型
- Python
- 命令行工具
categories:
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
- RAG应用
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7606732842490331151
aliases:
- /posts/20260219-juejin-抛弃纯文本我写了个工具验证-deepseek-ocr-猜想代码转-pdf-节省-40-token-3/
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:fd2fe8593b052d816cc211797c672ba58661a8ab8fa2977ad06d5f412c213d6c
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 51
captured_at: '2026-07-18T04:17:28.930451Z'
source_capture_sha256: sha256:6d102f90bba94052b9facbdb1f763afc719282c6651d417b4d6a3aef119a208b
source_capture_chars_original: 1981
source_publication_excerpt_chars: 678
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_9e07b0458561fca4e0bb668ac1c70862cd796d5d5608ede0f80547543e5ee8f9
revision_id: rev_9c5d800e54ece4ee90c213ec9c19dccf02799046186bc7498f215db7ee39da94
event_id: evt_efd9109059252fce6d8486b2a9cda6bb635204b97f17a183d96085d2a683d3e2
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-19T05:39:39Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7606732842490331151](<https://juejin.cn/post/7606732842490331151>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 引言：Token 还是不够用？
> 作为一名重度依赖 Claude和 Gemini辅助编程的开发者，我经常遇到一个尴尬的场景：
> 我想让 AI 重构一个模块，但这个模块依赖错综复杂。当我试图把整个 monorepo 的相关文件丢进对话框时，Token 瞬间爆炸，或者因为上下文过长（Lost in the Middle），模型开始胡言乱语。
> 传统的 RAG（检索增强生成）通过切片（Chunking）解决了容量问题，但破坏了代码的
> 整体结构感
> 。
> 直到最近，我读到了 DeepSeek 团队的论文
> DeepSeek-OCR
> 和另一篇
> Text or Pixels?
> ，它们提出了一个反直觉的观点：
> 对于结构化数据（如代码、表格），视觉编码（Vision Encoder）比文本编码（Text Tokenizer）效率更高。
> 于是我造了个轮子 ——
> Pixrep
> 。
> 什么是 Pixrep？
> 简单来说，它是一个 Python CLI 工具，能把你的整个代码仓库“拍”成一组结构化的、带语法高亮和语义分析的 PDF。
> GitHub:
> github.com/TingjiaInFu…
> 核心原理：为什么“看图”比“读字”更省 Token？
> 我们在写代码时，为了可读性会使用大量的缩进、换行和空格。在 Text Tokenizer 眼里，这些都是昂贵的 Token。
> 而在 Vision Model 眼里，代码的缩进、层级关系就是一张图上的几何结构。现代多模态模型的 Vision Encoder（如 ViT）通过 Patch 处理图像，对于稀疏的文本结构，压缩率极高。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
