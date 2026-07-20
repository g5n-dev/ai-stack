---
title: 'PyraTok: Language-Aligned Pyramidal Tokenizer for Video Understanding and
  Generation'
date: 2026-01-25 12:39:55+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2601.16210v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:28782edda080fd75c31d25a82a2ada26591631a7ac3a8d83d644d6f83e566983
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 84
captured_at: '2026-07-18T04:08:56.487166Z'
source_capture_sha256: sha256:6900e145d5785e38d97c3193ac9e0ee6a76c0310e5d1d67deb1e1b3e244954db
source_capture_chars_original: 1168
source_publication_excerpt_chars: 1168
observation_id: obs_b4da3e6b258410c7157f62971dc11bd37c53e9f1551b1f0651a608048ec7a419
revision_id: rev_23ac62cc5ed3d081c713e6ef5e331baa160a9a6bd2cbc31e7e0a24f021f5aca3
event_id: evt_509eecfbe17184f1435fc08a2f89357dd968fcc3a2331bf99c085a9cdd337cb7
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2601.16210v1](<https://arxiv.org/abs/2601.16210v1>)
- **作者**: Onkar Susladkar, Tushar Prakash, Adheesh Juvekar, Kiet A. Nguyen, Dong-Hwan Jang, Inderjit S Dhillon, Ismini Lourentzou
- **分类**: cs.CV
- **论文时间**: 2026-01-22T18:58:55Z
- **论文 PDF**: [https://arxiv.org/pdf/2601.16210v1.pdf](<https://arxiv.org/pdf/2601.16210v1.pdf>)

## 来源摘要/节选

> Discrete video VAEs underpin modern text-to-video generation and video understanding systems, yet existing tokenizers typically learn visual codebooks at a single scale with limited vocabularies and shallow language supervision, leading to poor cross-modal alignment and zero-shot transfer. We introduce PyraTok, a language-aligned pyramidal tokenizer that learns semantically structured discrete latents across multiple spatiotemporal resolutions. PyraTok builds on a pretrained video VAE and a novel Language aligned Pyramidal Quantization \(LaPQ\) module that discretizes encoder features at several depths using a shared large binary codebook, yielding compact yet expressive video token sequences. To tightly couple visual tokens with language, PyraTok jointly optimizes multi-scale text-guided quantization and a global autoregressive objective over the token hierarchy. Across ten benchmarks, PyraTok delivers state-of-the-art \(SOTA\) video reconstruction, consistently improves text-to-video quality, and sets new SOTA zero-shot performance on video segmentation, temporal action localization, and video understanding, scaling robustly to up to 4K/8K resolutions.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
