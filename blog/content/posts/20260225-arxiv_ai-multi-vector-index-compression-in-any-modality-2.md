---
title: Multi-Vector Index Compression in Any Modality
date: 2026-02-25 23:30:40+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.21202v1
aliases:
- /posts/20260226-arxiv_ai-multi-vector-index-compression-in-any-modality-2/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:a1759b8ef390fe7ecea7783d75a98ccd87489af1be2aa8a2dbd6d25d78b669be
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 46
captured_at: '2026-07-18T04:16:49.996029Z'
source_capture_sha256: sha256:aaf37948ced10e4065a84277cc86e498d01595a97c4618c2390df0893d6c062a
source_capture_chars_original: 1321
source_publication_excerpt_chars: 1321
observation_id: obs_5306db7ad5e9ad6cb0cbbebe03ee2235f203daf9b38ca6e25b27409ba040c8fe
revision_id: rev_1aff4b355659951cdc0b052d352c7a6f9a9acb43c7b9d6857b5bb9a74ebcbe8c
event_id: evt_9b21fabd56ff03d70ba33e0685284cf8a21ff677027e07538b0759f62d5f20c8
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.21202v1](<https://arxiv.org/abs/2602.21202v1>)
- **作者**: Hanxiang Qin, Alexander Martin, Rohan Jha, Chunsheng Zuo, Reno Kriz, Benjamin Van Durme
- **分类**: cs.IR
- **论文时间**: 2026-02-24T18:57:33Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.21202v1.pdf](<https://arxiv.org/pdf/2602.21202v1.pdf>)

## 来源摘要/节选

> We study efficient multi-vector retrieval for late interaction in any modality. Late interaction has emerged as a dominant paradigm for information retrieval in text, images, visual documents, and videos, but its computation and storage costs grow linearly with document length, making it costly for image-, video-, and audio-rich corpora. To address this limitation, we explore query-agnostic methods for compressing multi-vector document representations under a constant vector budget. We introduce four approaches for index compression: sequence resizing, memory tokens, hierarchical pooling, and a novel attention-guided clustering \(AGC\). AGC uses an attention-guided mechanism to identify the most semantically salient regions of a document as cluster centroids and to weight token aggregation. Evaluating these methods on retrieval tasks spanning text \(BEIR\), visual-document \(ViDoRe\), and video \(MSR-VTT, MultiVENT 2.0\), we show that attention-guided clustering consistently outperforms other parameterized compression methods \(sequence resizing and memory tokens\), provides greater flexibility in index size than non-parametric hierarchical clustering, and achieves competitive or improved performance compared to a full, uncompressed index. The source code is available at: github.com/hanxiangqin/omni-col-press.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
