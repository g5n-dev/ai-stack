---
title: Leveraging LLM Parametric Knowledge for Fact Checking without Retrieval
date: 2026-03-06 23:44:05+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
- AI Agent
- 大语言模型
categories:
- 论文
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2603.05471v1
aliases:
- /posts/20260307-arxiv_ai-leveraging-llm-parametric-knowledge-for-fact-check-9/
- /posts/20260308-arxiv_ai-leveraging-llm-parametric-knowledge-for-fact-check-9/
- /posts/20260309-arxiv_ai-leveraging-llm-parametric-knowledge-for-fact-check-9/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:8b8f0b26b085f3bba47f8f3cfa64ff1beba5ba701d790a9fad124a4cc273c3d5
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 71
captured_at: '2026-07-18T04:27:16.435086Z'
source_capture_sha256: sha256:8508a58b1679ffe74bcfbc09030ef40e726501ea48677b49cc9977a3433e608b
source_capture_chars_original: 1605
source_publication_excerpt_chars: 1605
observation_id: obs_ed993ce93a0da489ae9fa1470029443af927e902710cad7284eb6239e3ca70dc
revision_id: rev_02bf4a7b00293751e79cef7803a711f62509053c5b940c5b52c83befd59970fc
event_id: evt_f9982024f6c4805093fe430df616d29ed9a9b4bb2dab6762fe4d90234b40c209
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.05471v1](<https://arxiv.org/abs/2603.05471v1>)
- **作者**: Artem Vazhentsev, Maria Marina, Daniil Moskovskiy, Sergey Pletenev, Mikhail Seleznyov, Mikhail Salnikov, Elena Tutubalina, Vasily Konovalov, Irina Nikishina, Alexander Panchenko, Viktor Moskvoretskii
- **分类**: cs.CL
- **论文时间**: 2026-03-05T18:42:51Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.05471v1.pdf](<https://arxiv.org/pdf/2603.05471v1.pdf>)

## 来源摘要/节选

> Trustworthiness is a core research challenge for agentic AI systems built on Large Language Models \(LLMs\). To enhance trust, natural language claims from diverse sources, including human-written text, web content, and model outputs, are commonly checked for factuality by retrieving external knowledge and using an LLM to verify the faithfulness of claims to the retrieved evidence. As a result, such methods are constrained by retrieval errors and external data availability, while leaving the models intrinsic fact-verification capabilities largely unused. We propose the task of fact-checking without retrieval, focusing on the verification of arbitrary natural language claims, independent of their source. To study this setting, we introduce a comprehensive evaluation framework focused on generalization, testing robustness to \(i\) long-tail knowledge, \(ii\) variation in claim sources, \(iii\) multilinguality, and \(iv\) long-form generation. Across 9 datasets, 18 methods and 3 models, our experiments indicate that logit-based approaches often underperform compared to those that leverage internal model representations. Building on this finding, we introduce INTRA, a method that exploits interactions between internal representations and achieves state-of-the-art performance with strong generalization. More broadly, our work establishes fact-checking without retrieval as a promising research direction that can complement retrieval-based frameworks, improve scalability, and enable the use of such systems as reward signals during training or as components integrated into the generation process.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
