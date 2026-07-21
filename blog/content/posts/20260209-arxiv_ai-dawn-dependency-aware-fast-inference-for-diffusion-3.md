---
title: 'DAWN: Dependency-Aware Fast Inference for Diffusion LLMs'
date: 2026-02-09 23:42:37+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
- 大语言模型
categories:
- 论文
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.06953v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:bbde19f3a969b92751290f6c076c88fb38ac6b812002d2bdf5df21ebff7059b7
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 56
captured_at: '2026-07-18T04:11:20.263833Z'
source_capture_sha256: sha256:cd8d7efe949f01165cad972e6f77bc9df24faa68417fdba210e84f580cf30d42
source_capture_chars_original: 1403
source_publication_excerpt_chars: 1403
observation_id: obs_101ddeda70e2f4e0e3bae5ea8a8bfde1ef2315fe21f6b5d1a33d83cf92e5b19c
revision_id: rev_dcc67cda87f8c61f248d9f8b41f96f6d75e942b55161d171c0d9efbac0ab68d8
event_id: evt_932ecd23e37bcf14d22b12915d8477f445effb049888317f78be5ba02e00c18e
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-09T06:52:16Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.06953v1](<https://arxiv.org/abs/2602.06953v1>)
- **作者**: Lizhuo Luo, Zhuoran Shi, Jiajun Luo, Zhi Wang, Shen Ren, Wenya Wang, Tianwei Zhang
- **分类**: cs.CL
- **论文时间**: 2026-02-06T18:51:29Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.06953v1.pdf](<https://arxiv.org/pdf/2602.06953v1.pdf>)

## 来源摘要/节选

> Diffusion large language models \(dLLMs\) have shown advantages in text generation, particularly due to their inherent ability for parallel decoding. However, constrained by the quality--speed trade-off, existing inference solutions adopt conservative parallel strategies, leaving substantial efficiency potential underexplored. A core challenge is that parallel decoding assumes each position can be filled independently, but tokens are often semantically coupled. Thus, the correct choice at one position constrains valid choices at others. Without modeling these inter-token dependencies, parallel strategies produce deteriorated outputs. Motivated by this insight, we propose DAWN, a training-free, dependency-aware decoding method for fast dLLM inference. DAWN extracts token dependencies and leverages two key motivations: \(1\) positions dependent on unmasked certain positions become more reliable, \(2\) simultaneously unmasking strongly coupled uncertain positions induces errors. Given those findings, DAWN leverages a dependency graph to select more reliable unmasking positions at each iteration, achieving high parallelism with negligible loss in generation quality. Extensive experiments across multiple models and datasets demonstrate that DAWN speedups the inference by 1.80-8.06x over baselines while preserving the generation quality. Code is released at https://github.com/lizhuo-luo/DAWN.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
