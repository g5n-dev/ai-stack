---
title: 'Turning the TIDE: Cross-Architecture Distillation for Diffusion Large Language
  Models'
date: 2026-04-30 23:11:36+08:00
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
external_url: https://arxiv.org/abs/2604.26951v1
aliases:
- /posts/20260501-arxiv_ai-turning-the-tide-cross-architecture-distillation-f-0/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:012be519f8f201532a51be2b958500d9de2f3b174820f2a6f0f1de9f8c6b3464
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 85
captured_at: '2026-07-18T04:29:27.867360Z'
source_capture_sha256: sha256:ab9830a140d04d0fd55382c45231c0be5de30b2eee5b93e2c6bc1aa005f838fb
source_capture_chars_original: 1269
source_publication_excerpt_chars: 1269
observation_id: obs_ff828733629db0030e092f28db31381966844392dd1fb6c1e2cdc0ebb5ecbc1e
revision_id: rev_9034e853905daeee0325b04757df22d71ec687048776817403c43522aa52f1fc
event_id: evt_776fc9620d4c55659e6eceb7c1c86aaed9e6498dbc2802a70188b012d84a9f0f
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2604.26951v1](<https://arxiv.org/abs/2604.26951v1>)
- **作者**: Gongbo Zhang, Wen Wang, Ye Tian, Li Yuan
- **分类**: cs.CL
- **论文时间**: 2026-04-29T17:59:01Z
- **论文 PDF**: [https://arxiv.org/pdf/2604.26951v1.pdf](<https://arxiv.org/pdf/2604.26951v1.pdf>)

## 来源摘要/节选

> Diffusion large language models \(dLLMs\) offer parallel decoding and bidirectional context, but state-of-the-art dLLMs require billions of parameters for competitive performance. While existing distillation methods for dLLMs reduce inference steps within a single architecture, none address cross-architecture knowledge transfer, in which the teacher and student differ in architecture, attention mechanism, and tokenizer. We present TIDE, the first framework for cross-architecture dLLM distillation, comprising three modular components: \(1\) TIDAL, which jointly modulates distillation strength across training progress and diffusion timestep to account for the teacher's noise-dependent reliability; \(2\) CompDemo, which enriches the teacher's context via complementary mask splitting to improve predictions under heavy masking; and \(3\) Reverse CALM, a cross-tokenizer objective that inverts chunk-level likelihood matching, yielding bounded gradients and dual-end noise filtering. Distilling 8B dense and 16B MoE teachers into a 0.6B student via two heterogeneous pipelines outperforms the baseline by an average of 1.53 points across eight benchmarks, yielding notable gains in code generation, where HumanEval scores reach 48.78 compared to 32.3 for the AR baseline.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
