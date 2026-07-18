---
title: 'SenCache: Accelerating Diffusion Model Inference via Sensitivity-Aware Caching'
date: 2026-03-02 02:56:17+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.24208v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:992e675458aa750c6046f0b6f956e8f7e65628c339ddd5961b54f51c4d59f4f5
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 78
captured_at: '2026-07-18T04:26:19.677155Z'
source_capture_sha256: sha256:314eb862c643644016daac498182d5ced14700ae45e3f16819ce2fe2213b5551
source_capture_chars_original: 1339
source_publication_excerpt_chars: 1339
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.24208v1](<https://arxiv.org/abs/2602.24208v1>)
- **作者**: Yasaman Haghighi, Alexandre Alahi
- **分类**: cs.CV
- **论文时间**: 2026-02-27T17:36:09Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.24208v1.pdf](<https://arxiv.org/pdf/2602.24208v1.pdf>)

## 来源摘要/节选

> Diffusion models achieve state-of-the-art video generation quality, but their inference remains expensive due to the large number of sequential denoising steps. This has motivated a growing line of research on accelerating diffusion inference. Among training-free acceleration methods, caching reduces computation by reusing previously computed model outputs across timesteps. Existing caching methods rely on heuristic criteria to choose cache/reuse timesteps and require extensive tuning. We address this limitation with a principled sensitivity-aware caching framework. Specifically, we formalize the caching error through an analysis of the model output sensitivity to perturbations in the denoising inputs, i.e., the noisy latent and the timestep, and show that this sensitivity is a key predictor of caching error. Based on this analysis, we propose Sensitivity-Aware Caching \(SenCache\), a dynamic caching policy that adaptively selects caching timesteps on a per-sample basis. Our framework provides a theoretical basis for adaptive caching, explains why prior empirical heuristics can be partially effective, and extends them to a dynamic, sample-specific approach. Experiments on Wan 2.1, CogVideoX, and LTX-Video show that SenCache achieves better visual quality than existing caching methods under similar computational budgets.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
