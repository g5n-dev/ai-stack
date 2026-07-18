---
title: 'From Semantics to Pixels: Coarse-to-Fine Masked Autoencoders for Hierarchical
  Visual Understanding'
date: 2026-03-11 22:41:14+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2603.09955v1
aliases:
- /posts/20260312-arxiv_ai-from-semantics-to-pixels-coarse-to-fine-masked-aut-7/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:ca32752a89c9297ae98c0fff9a534b271b50f4e376a1c53c1e3bf51dab2092c7
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 98
captured_at: '2026-07-18T04:27:47.713351Z'
source_capture_sha256: sha256:48fc1b446a4ead3f027ee45cec4f27ccf5490be1c164a8030cc8ac9ba9f24f42
source_capture_chars_original: 1464
source_publication_excerpt_chars: 1464
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.09955v1](<https://arxiv.org/abs/2603.09955v1>)
- **作者**: Wenzhao Xiang, Yue Wu, Hongyang Yu, Feng Gao, Fan Yang, Xilin Chen
- **分类**: cs.CV
- **论文时间**: 2026-03-10T17:51:12Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.09955v1.pdf](<https://arxiv.org/pdf/2603.09955v1.pdf>)

## 来源摘要/节选

> Self-supervised visual pre-training methods face an inherent tension: contrastive learning \(CL\) captures global semantics but loses fine-grained detail, while masked image modeling \(MIM\) preserves local textures but suffers from "attention drift" due to semantically-agnostic random masking. We propose C2FMAE, a coarse-to-fine masked autoencoder that resolves this tension by explicitly learning hierarchical visual representations across three data granularities: semantic masks \(scene-level\), instance masks \(object-level\), and RGB images \(pixel-level\). Two synergistic innovations enforce a strict top-down learning principle. First, a cascaded decoder sequentially reconstructs from scene semantics to object instances to pixel details, establishing explicit cross-granularity dependencies that parallel decoders cannot capture. Second, a progressive masking curriculum dynamically shifts the training focus from semantic-guided to instance-guided and finally to random masking, creating a structured learning path from global context to local features. To support this framework, we construct a large-scale multi-granular dataset with high-quality pseudo-labels for all 1.28M ImageNet-1K images. Extensive experiments show that C2FMAE achieves significant performance gains on image classification, object detection, and semantic segmentation, validating the effectiveness of our hierarchical design in learning more robust and generalizable representations.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
