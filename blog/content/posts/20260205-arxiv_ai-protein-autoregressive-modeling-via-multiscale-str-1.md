---
title: Protein Autoregressive Modeling via Multiscale Structure Generation
date: 2026-02-05 23:03:18+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.04883v1
aliases:
- /posts/20260206-arxiv_ai-protein-autoregressive-modeling-via-multiscale-str-1/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:61496159621f80145aedc7ea7611a58c177b159d50b7b04d449e4e48ef386faa
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 67
captured_at: '2026-07-18T04:10:53.549487Z'
source_capture_sha256: sha256:2dbe592e5eb7eb123dee6d4443ce4f5d0663dd8f5c533003a8faf84872571c17
source_capture_chars_original: 1499
source_publication_excerpt_chars: 1499
observation_id: obs_627b81ee6af575a8ca308ba3e6e2d36b237869652ba99818ad2dfe08ce77e10f
revision_id: rev_4e1ad8eb90377258bc52850c196242298dee1a7069361d68628f0ffd7a28e0a9
event_id: evt_547eb3ca2c95beca70e8eab4c8db449d97c2fda0450498b2b59b2eb5a47bc772
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-05T04:21:21Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.04883v1](<https://arxiv.org/abs/2602.04883v1>)
- **作者**: Yanru Qu, Cheng-Yen Hsieh, Zaixiang Zheng, Ge Liu, Quanquan Gu
- **分类**: cs.LG
- **论文时间**: 2026-02-04T18:59:49Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.04883v1.pdf](<https://arxiv.org/pdf/2602.04883v1.pdf>)

## 来源摘要/节选

> We present protein autoregressive modeling \(PAR\), the first multi-scale autoregressive framework for protein backbone generation via coarse-to-fine next-scale prediction. Using the hierarchical nature of proteins, PAR generates structures that mimic sculpting a statue, forming a coarse topology and refining structural details over scales. To achieve this, PAR consists of three key components: \(i\) multi-scale downsampling operations that represent protein structures across multiple scales during training; \(ii\) an autoregressive transformer that encodes multi-scale information and produces conditional embeddings to guide structure generation; \(iii\) a flow-based backbone decoder that generates backbone atoms conditioned on these embeddings. Moreover, autoregressive models suffer from exposure bias, caused by the training and the generation procedure mismatch, and substantially degrades structure generation quality. We effectively alleviate this issue by adopting noisy context learning and scheduled sampling, enabling robust backbone generation. Notably, PAR exhibits strong zero-shot generalization, supporting flexible human-prompted conditional generation and motif scaffolding without requiring fine-tuning. On the unconditional generation benchmark, PAR effectively learns protein distributions and produces backbones of high design quality, and exhibits favorable scaling behavior. Together, these properties establish PAR as a promising framework for protein structure generation.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
