---
title: Decoupled Diffusion Sampling for Inverse Problems on Function Spaces
date: 2026-02-02 19:22:59+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2601.23280v1
aliases:
- /posts/20260203-arxiv_ai-decoupled-diffusion-sampling-for-inverse-problems--2/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:44836e362ce45f851ed795cff412725f45cf7b46db774d985b8b89b446ab5924
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 68
captured_at: '2026-07-18T04:10:04.354932Z'
source_capture_sha256: sha256:1482b1d66cbf75104e702c1194f02a6a3174477d4a57766e187435dc8b0280f9
source_capture_chars_original: 1098
source_publication_excerpt_chars: 1098
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2601.23280v1](<https://arxiv.org/abs/2601.23280v1>)
- **作者**: Thomas Y. L. Lin, Jiachen Yao, Lufang Chiang, Julius Berner, Anima Anandkumar
- **分类**: cs.LG
- **论文时间**: 2026-01-30T18:54:49Z
- **论文 PDF**: [https://arxiv.org/pdf/2601.23280v1.pdf](<https://arxiv.org/pdf/2601.23280v1.pdf>)

## 来源摘要/节选

> We propose a data-efficient, physics-aware generative framework in function space for inverse PDE problems. Existing plug-and-play diffusion posterior samplers represent physics implicitly through joint coefficient-solution modeling, requiring substantial paired supervision. In contrast, our Decoupled Diffusion Inverse Solver \(DDIS\) employs a decoupled design: an unconditional diffusion learns the coefficient prior, while a neural operator explicitly models the forward PDE for guidance. This decoupling enables superior data efficiency and effective physics-informed learning, while naturally supporting Decoupled Annealing Posterior Sampling \(DAPS\) to avoid over-smoothing in Diffusion Posterior Sampling \(DPS\). Theoretically, we prove that DDIS avoids the guidance attenuation failure of joint models when training data is scarce. Empirically, DDIS achieves state-of-the-art performance under sparse observation, improving $l\_2$ error by 11% and spectral error by 54% on average; when data is limited to 1%, DDIS maintains accuracy with 40% advantage in $l\_2$ error compared to joint models.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
