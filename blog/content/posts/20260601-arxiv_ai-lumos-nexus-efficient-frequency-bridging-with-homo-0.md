---
title: 'Lumos-Nexus: Efficient Frequency Bridging with Homogeneous Latent Space for
  Video Unified Models'
date: 2026-06-01 21:35:17+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2605.31603v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:25debb0f1ea0cd20cc5504497b4645a944c39d358582e0ff20758d63fa0d04ba
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 96
captured_at: '2026-07-18T04:29:58.207159Z'
source_capture_sha256: sha256:7ed26bee5ba374e107b965863c9fec9b601f3d58ad5f2eae0a648bf692dc11e3
source_capture_chars_original: 1456
source_publication_excerpt_chars: 1456
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2605.31603v1](<https://arxiv.org/abs/2605.31603v1>)
- **作者**: Jiazheng Xing, Hangjie Yuan, Lingling Cai, Xinyu Liu, Yujie Wei, Fei Du, Hai Ci, Tao Feng, Jiasheng Tang, Weihua Chen, Fan Wang, Yong Liu
- **分类**: cs.CV
- **论文时间**: 2026-05-29T17:59:50Z
- **论文 PDF**: [https://arxiv.org/pdf/2605.31603v1.pdf](<https://arxiv.org/pdf/2605.31603v1.pdf>)

## 来源摘要/节选

> Connector-based video unified models have demonstrated strong capability in instruction-grounded video synthesis, but integrating a large high-fidelity generator into the unified training loop is computationally prohibitive, limiting achievable visual quality. We therefore propose Lumos-Nexus, a training-efficient unified video generation framework that facilitates the development of strong reasoning-driven generation capabilities while significantly enhancing visual fidelity. Lumos-Nexus adopts a two-stage design: 1\) During training, only a lightweight generator is aligned with the understanding block to learn to take in reasoning-driven semantic control. 2\) During inference, we introduce Unified Progressive Frequency Bridging \(UPFB\) to progressively hand off generation to a high-capacity pretrained generator in the shared latent space, enabling coarse-to-fine refinement and producing high-fidelity videos without compromising reasoning quality. To fill the gap in reasoning-driven video generation benchmarks, we introduce VR-Bench, which assesses a model's capability to translate inferred intent into coherent and semantically aligned video content. Extensive experiments demonstrate that Lumos-Nexus achieves substantial gains in visual realism and temporal coherence on VBench, while exhibiting strong reasoning-based generative performance on VR-Bench. Code and models are available at https://jiazheng-xing.github.io/nexus-lumos-home/.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
