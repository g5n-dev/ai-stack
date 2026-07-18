---
title: 'Act Wisely: Cultivating Meta-Cognitive Tool Use in Agentic Multimodal Models'
date: 2026-04-10 21:54:42+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
- AI Agent
categories:
- 论文
scenarios:
- AI/ML项目
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2604.08545v1
aliases:
- /posts/20260411-arxiv_ai-act-wisely-cultivating-meta-cognitive-tool-use-in--0/
- /posts/20260412-arxiv_ai-act-wisely-cultivating-meta-cognitive-tool-use-in--0/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:877675f1c7285df9c2fb4bf267e1f8baddaa83e88a110eb776288c147289c2b0
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 76
captured_at: '2026-07-18T04:29:12.103286Z'
source_capture_sha256: sha256:1ee4b1e09da6e0e61d8ce970b06d436c3a7eb5c3393ab7d2cf89c4d74ecd7d4a
source_capture_chars_original: 1734
source_publication_excerpt_chars: 1734
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2604.08545v1](<https://arxiv.org/abs/2604.08545v1>)
- **作者**: Shilin Yan, Jintao Tong, Hongwei Xue, Xiaojun Tang, Yangyang Wang, Kunyu Shi, Guannan Zhang, Ruixuan Li, Yixiong Zou
- **分类**: cs.CV
- **论文时间**: 2026-04-09T17:59:57Z
- **论文 PDF**: [https://arxiv.org/pdf/2604.08545v1.pdf](<https://arxiv.org/pdf/2604.08545v1.pdf>)

## 来源摘要/节选

> The advent of agentic multimodal models has empowered systems to actively interact with external environments. However, current agents suffer from a profound meta-cognitive deficit: they struggle to arbitrate between leveraging internal knowledge and querying external utilities. Consequently, they frequently fall prey to blind tool invocation, resorting to reflexive tool execution even when queries are resolvable from the raw visual context. This pathological behavior precipitates severe latency bottlenecks and injects extraneous noise that derails sound reasoning. Existing reinforcement learning protocols attempt to mitigate this via a scalarized reward that penalizes tool usage. Yet, this coupled formulation creates an irreconcilable optimization dilemma: an aggressive penalty suppresses essential tool use, whereas a mild penalty is entirely subsumed by the variance of the accuracy reward during advantage normalization, rendering it impotent against tool overuse. To transcend this bottleneck, we propose HDPO, a framework that reframes tool efficiency from a competing scalar objective to a strictly conditional one. By eschewing reward scalarization, HDPO maintains two orthogonal optimization channels: an accuracy channel that maximizes task correctness, and an efficiency channel that enforces execution economy exclusively within accurate trajectories via conditional advantage estimation. This decoupled architecture naturally induces a cognitive curriculum-compelling the agent to first master task resolution before refining its self-reliance. Extensive evaluations demonstrate that our resulting model, Metis, reduces tool invocations by orders of magnitude while simultaneously elevating reasoning accuracy.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
