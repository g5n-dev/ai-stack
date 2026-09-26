---
title: "SemMSA: Latent Semantic-Aided Robust Multimodal Sentiment Analysis with Incomplete Data"
date: 2026-09-26T15:43:29+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "cs.CL", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:dd2e0ffb52e737a280b01368efe24a9a3d67fc542038901573c6619c7ba59b0b"
source_payload_sha256: "sha256:5b981237f4419009fc67d3a858f13f40df7bf3237f021ba38ccb6ecfc9f7d4af"
observation_id: obs_d272faf7bfac150149db780abefb0cd882a19c57be58894d00542d6884cee58f
event_id: evt_82e92af26d2041cc0ef87bb66d8e6589d6a99ab485bd003b804c49792dca123c
revision_id: rev_f7998bf481ebed0f2c5449f66c184dd648085e5c0aae2386c3b7b5c4fba0b84a
source_published_at: 2026-09-24T17:55:31Z
first_seen_at: 2026-09-26T07:53:10Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 87
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2609.30238v1
parent_observation_id: null
last_seen_at: 2026-09-26T07:40:19.996214Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.30238v1](http://arxiv.org/abs/2609.30238v1)
- **发布域名**: arxiv.org
- **分类**: cs.CL
- **作者**: Wenhao Li、Zhibin Wu、Chong Xiao 等

## 来源摘要/节选

> Recent research on Multimodal Sentiment Analysis (MSA) has focused on learning from language, visual, and acoustic modalities with incomplete data to infer human sentiment. Most studies typically compensate for missing information by reconstructing modality features or designing complicated fusion mechanisms. However, these methods still suffer from spurious generation and noisy guidance due to the lack of high-level semantic grounding in partially observed multimodal evidence. To address these issues, we propose SemMSA, a latent semantic-aided framework that constructs rich sentiment-relevant semantics with LLMs, fully integrating with all modalities via anchor-free spectral alignment. It mainly consists of Cross-modal Semantic Refinement (CSR) and Cross-modal Spectral Alignment (CSA). Specifically, CSR first adaptively extracts visual and acoustic representations by corresponding adapters to form a unified multimodal prefix with language in the frozen LLM embedding space. It then iteratively produces continuous discriminative semantic states through a token-efficient latent refinement process without decoding explicit text. Next, CSA simultaneously aligns the refined semantics with all modalities by enhancing the dominant spectral component of their kernel Gram matrix. This captures global nonlinear dependencies among all representations without relying on a predefined anchor modality. In addition, an instance-level spectral separation constraint preserves cross-sample discriminability and mitigates representation collapse. Extensive experiments on SIMS, MOSI, and MOSEI benchmarks demonstrate that SemMSA achieves state-of-the-art performance.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。