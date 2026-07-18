---
title: 'MC-Search: Evaluating and Enhancing Multimodal Agentic Search with Structured
  Long Reasoning Chains'
date: 2026-03-03 02:52:12+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
- RAG
- AI Agent
- 大语言模型
categories:
- 论文
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
- RAG应用
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2603.00873v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:bcac3cc35764d1addb2cc80ee472510f6fd83dc33a403736d8ac8ed69741b5b2
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 99
captured_at: '2026-07-18T04:26:34.932328Z'
source_capture_sha256: sha256:01fd7845e1578e8a4e1598bd663a1688da5562ff3a2259a1742ebbb7af41fc68
source_capture_chars_original: 1413
source_publication_excerpt_chars: 1413
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.00873v1](<https://arxiv.org/abs/2603.00873v1>)
- **作者**: Xuying Ning, Dongqi Fu, Tianxin Wei, Mengting Ai, Jiaru Zou, Ting-Wei Li, Hanghang Tong, Yada Zhu, Hendrik Hamann, Jingrui He
- **分类**: cs.AI
- **论文时间**: 2026-03-01T02:25:57Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.00873v1.pdf](<https://arxiv.org/pdf/2603.00873v1.pdf>)

## 来源摘要/节选

> With the increasing demand for step-wise, cross-modal, and knowledge-grounded reasoning, multimodal large language models \(MLLMs\) are evolving beyond the traditional fixed retrieve-then-generate paradigm toward more sophisticated agentic multimodal retrieval-augmented generation \(MM-RAG\). Existing benchmarks, however, mainly focus on simplified QA with short retrieval chains, leaving adaptive planning and multimodal reasoning underexplored. We present MC-Search, the first benchmark for agentic MM-RAG with long, step-wise annotated reasoning chains spanning five representative reasoning structures. Each example specifies sub-questions, retrieval modalities, supporting facts, and intermediate answers, with fidelity ensured by HAVE \(Hop-wise Attribution and Verification of Evidence\), resulting in 3,333 high-quality examples averaging 3.7 hops. Beyond answer accuracy, MC-Search introduces new process-level metrics for reasoning quality, stepwise retrieval and planning accuracy. By developing a unified agentic MM-RAG pipeline, we benchmark six leading MLLMs and reveal systematic issues such as over- and under-retrieval and modality-misaligned planning. Finally, we introduce Search-Align, a process-supervised fine-tuning framework leveraging verified reasoning chains, showing that our data not only enables faithful evaluation but also improves planning and retrieval fidelity in open-source MLLMs.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
