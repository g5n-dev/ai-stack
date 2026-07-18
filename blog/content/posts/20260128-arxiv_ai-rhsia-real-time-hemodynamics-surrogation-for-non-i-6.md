---
title: 'RHSIA: Real-time Hemodynamics Surrogation for Non-idealized Intracranial Aneurysms'
date: 2026-01-28 07:28:04+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
- 深度学习
categories:
- 论文
scenarios:
- AI/ML项目
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2601.19876v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:0a281b1617acb17b17ffb36ec9dfa34e8077b871b6d9ed2a5f6c3002faeea978
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 82
captured_at: '2026-07-18T04:09:30.311520Z'
source_capture_sha256: sha256:fcf51a9ad2cc6e986b8a2f5f7872c950487022b2a4e27c93a99e3f08641938be
source_capture_chars_original: 1670
source_publication_excerpt_chars: 1670
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2601.19876v1](<https://arxiv.org/abs/2601.19876v1>)
- **作者**: Yiying Sheng, Wenhao Ding, Dylan Roi, Leonard Leong Litt Yeo, Hwa Liang Leo, Choon Hwai Yap
- **分类**: cs.LG
- **论文时间**: 2026-01-27T18:39:58Z
- **论文 PDF**: [https://arxiv.org/pdf/2601.19876v1.pdf](<https://arxiv.org/pdf/2601.19876v1.pdf>)

## 来源摘要/节选

> Extensive studies suggested that fluid mechanical markers of intracranial aneurysms \(IAs\) derived from Computational Fluid Dynamics \(CFD\) can indicate disease progression risks, but to date this has not been translated clinically. This is because CFD requires specialized expertise and is time-consuming and low throughput, making it difficult to support clinical trials. A deep learning model that maps IA morphology to biomechanical markers can address this, enabling physicians to obtain these markers in real time without performing CFD. Here, we show that a Graph Transformer model that incorporates temporal information, which is supervised by large CFD data, can accurately predict Wall Shear Stress \(WSS\) across the cardiac cycle from IA surface meshes. The model effectively captures the temporal variations of the WSS pattern, achieving a Structural Similarity Index \(SSIM\) of up to 0.981 and a maximum-based relative L2 error of 2.8%. Ablation studies and SOTA comparison confirmed its optimality. Further, as pulsatile CFD data is computationally expensive to generate and sample sizes are limited, we engaged a strategy of injecting a large amount of steady-state CFD data, which are extremely low-cost to generate, as augmentation. This approach enhances network performance substantially when pulsatile CFD data sample size is small. Our study provides a proof of concept that temporal sequences cardiovascular fluid mechanical parameters can be computed in real time using a deep learning model from the geometric mesh, and this is achievable even with small pulsatile CFD sample size. Our approach is likely applicable to other cardiovascular scenarios.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
