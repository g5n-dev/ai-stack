---
title: 'SOTAlign: Semi-Supervised Alignment of Unimodal Vision and Language Models
  via Optimal Transport'
date: 2026-02-27 23:20:57+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.23353v1
aliases:
- /posts/20260228-arxiv_ai-sotalign-semi-supervised-alignment-of-unimodal-vis-3/
- /posts/20260301-arxiv_ai-sotalign-semi-supervised-alignment-of-unimodal-vis-3/
- /posts/20260302-arxiv_ai-sotalign-semi-supervised-alignment-of-unimodal-vis-3/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:87432ac69178e576688a9b280c9325f3016d35b40f4d8ccae1a89ef973d3df22
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 96
captured_at: '2026-07-18T04:30:44.821176Z'
source_capture_sha256: sha256:d9138c7322af6cba53eb46ffcd8c24b4f687e082d201590f663aeca754e8afdf
source_capture_chars_original: 1211
source_publication_excerpt_chars: 1211
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.23353v1](<https://arxiv.org/abs/2602.23353v1>)
- **作者**: Simon Roschmann, Paul Krzakala, Sonia Mazelet, Quentin Bouniot, Zeynep Akata
- **分类**: cs.LG
- **论文时间**: 2026-02-26T18:55:06Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.23353v1.pdf](<https://arxiv.org/pdf/2602.23353v1.pdf>)

## 来源摘要/节选

> The Platonic Representation Hypothesis posits that neural networks trained on different modalities converge toward a shared statistical model of the world. Recent work exploits this convergence by aligning frozen pretrained vision and language models with lightweight alignment layers, but typically relies on contrastive losses and millions of paired samples. In this work, we ask whether meaningful alignment can be achieved with substantially less supervision. We introduce a semi-supervised setting in which pretrained unimodal encoders are aligned using a small number of image-text pairs together with large amounts of unpaired data. To address this challenge, we propose SOTAlign, a two-stage framework that first recovers a coarse shared geometry from limited paired data using a linear teacher, then refines the alignment on unpaired samples via an optimal-transport-based divergence that transfers relational structure without overconstraining the target space. Unlike existing semi-supervised methods, SOTAlign effectively leverages unpaired images and text, learning robust joint embeddings across datasets and encoder pairs, and significantly outperforming supervised and semi-supervised baselines.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
