---
title: 'MonarchRT: Efficient Attention for Real-Time Video Generation'
date: 2026-02-13 23:30:43+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.12271v1
aliases:
- /posts/20260214-arxiv_ai-monarchrt-efficient-attention-for-real-time-video--7/
- /posts/20260215-arxiv_ai-monarchrt-efficient-attention-for-real-time-video--7/
- /posts/20260216-arxiv_ai-monarchrt-efficient-attention-for-real-time-video--7/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:619d56aab9d9b37d373719830a82aaf8d5a55f017a3d6120ef0d68aee29aef10
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 61
captured_at: '2026-07-18T04:15:06.314161Z'
source_capture_sha256: sha256:eb693af40e442a3ac1ed2e790aa1fa4dee4e8811d90f26233fd5db2a92698e4e
source_capture_chars_original: 1903
source_publication_excerpt_chars: 1903
observation_id: obs_0591d65a509592636ce60d9a3325f6c37ec228deedb8883aa90b45be5c16d47b
revision_id: rev_91b54a5018e3af26413dec05c60b3f969dbbc1bebabbe611e90bc8946d40174d
event_id: evt_337b65b78b17df2a9147992e47ad8dbd144f606613a465d511402f30847e8b6e
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-13T06:19:22Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.12271v1](<https://arxiv.org/abs/2602.12271v1>)
- **作者**: Krish Agarwal, Zhuoming Chen, Cheng Luo, Yongqi Chen, Haizhong Zheng, Xun Huang, Atri Rudra, Beidi Chen
- **分类**: cs.CV
- **论文时间**: 2026-02-12T18:56:53Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.12271v1.pdf](<https://arxiv.org/pdf/2602.12271v1.pdf>)

## 来源摘要/节选

> Real-time video generation with Diffusion Transformers is bottlenecked by the quadratic cost of 3D self-attention, especially in real-time regimes that are both few-step and autoregressive, where errors compound across time and each denoising step must carry substantially more information. In this setting, we find that prior sparse-attention approximations break down, despite showing strong results for bidirectional, many-step diffusion. Specifically, we observe that video attention is not reliably sparse, but instead combines pronounced periodic structure driven by spatiotemporal position with dynamic, sparse semantic correspondences and dense mixing, exceeding the representational capacity of even oracle top-k attention. Building on this insight, we propose Monarch-RT, a structured attention parameterization for video diffusion models that factorizes attention using Monarch matrices. Through appropriately aligned block structure and our extended tiled Monarch parameterization, we achieve high expressivity while preserving computational efficiency. We further overcome the overhead of parameterization through finetuning, with custom Triton kernels. We first validate the high efficacy of Monarch-RT over existing sparse baselines designed only for bidirectional models. We further observe that Monarch-RT attains up to 95% attention sparsity with no loss in quality when applied to the state-of-the-art model Self-Forcing, making Monarch-RT a pioneering work on highly-capable sparse attention parameterization for real-time video generation. Our optimized implementation outperforms FlashAttention-2, FlashAttention-3, and FlashAttention-4 kernels on Nvidia RTX 5090, H100, and B200 GPUs respectively, providing kernel speedups in the range of 1.4-11.8X. This enables us, for the first time, to achieve true real-time video generation with Self-Forcing at 16 FPS on a single RTX 5090.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
