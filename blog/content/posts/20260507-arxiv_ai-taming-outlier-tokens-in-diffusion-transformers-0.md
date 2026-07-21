---
title: Taming Outlier Tokens in Diffusion Transformers
date: 2026-05-07 23:28:57+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2605.05206v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:fbc217877d38abfd5c3a742b8e93a87813d3afee22d2d4059a4472e6674d37b5
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 47
captured_at: '2026-07-18T04:29:31.582048Z'
source_capture_sha256: sha256:64bc9531c7dc17fa1a7ceae416999e969b9c7c806651db99e1a84e4aaa4ad172
source_capture_chars_original: 1286
source_publication_excerpt_chars: 1286
observation_id: obs_0d8c804fb8e2119cb1dd1ca575071219a61ddbe1eb77b53c2ef7ee0c718b05ab
revision_id: rev_1449e91ef7621d7fbe0350035e0d485a69218f09880bb672cbf16e5985a64e5b
event_id: evt_83c139d25cc7f9f2943af5e7952541f94ec339c135e4ae32fba82766d8e6fdea
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2605.05206v1](<https://arxiv.org/abs/2605.05206v1>)
- **作者**: Xiaoyu Wu, Yifei Wang, Tsu-Jui Fu, Liang-Chieh Chen, Zhe Gan, Chen Wei
- **分类**: cs.CV
- **论文时间**: 2026-05-06T17:59:42Z
- **论文 PDF**: [https://arxiv.org/pdf/2605.05206v1.pdf](<https://arxiv.org/pdf/2605.05206v1.pdf>)

## 来源摘要/节选

> We study outlier tokens in Diffusion Transformers \(DiTs\) for image generation. Prior work has shown that Vision Transformers \(ViTs\) can produce a small number of high-norm tokens that attract disproportionate attention while carrying limited local information, but their role in generative models remains underexplored. We show that this phenomenon appears in both the encoder and denoiser of modern Representation Autoencoder \(RAE\)-DiT pipelines: pretrained ViT encoders can produce outlier representations, and DiTs themselves can develop internal outlier tokens, especially in intermediate layers. Moreover, simply masking high-norm tokens does not improve performance, indicating that the problem is not only caused by a few extreme values, but is more closely related to corrupted local patch semantics. To address this issue, we introduce Dual-Stage Registers \(DSR\), a register-based intervention for both components: trained registers when available, recursive test-time registers otherwise, and diffusion registers for the denoiser. Across ImageNet and large-scale text-to-image generation, these interventions consistently reduce outlier artifacts and improve generation quality. Our results highlight outlier-token control as an important ingredient in building stronger DiTs.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
