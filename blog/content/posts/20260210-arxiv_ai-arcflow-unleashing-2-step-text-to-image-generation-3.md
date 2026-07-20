---
title: 'ArcFlow: Unleashing 2-Step Text-to-Image Generation via High-Precision Non-Linear
  Flow Distillation'
date: 2026-02-10 22:46:04+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.09014v1
aliases:
- /posts/20260211-arxiv_ai-arcflow-unleashing-2-step-text-to-image-generation-3/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:e1703a546239baedd0d30b12d97ba1862bcdc5d6ad0a82d9b16a89f11b66dc22
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 99
captured_at: '2026-07-18T04:14:24.737190Z'
source_capture_sha256: sha256:cd5fded20d26499d43d87f6bb9aec9182355e804c058358173764343174185a6
source_capture_chars_original: 1824
source_publication_excerpt_chars: 1824
observation_id: obs_cb025aa259374f7e8c52dd1a93bb8a1ccc2623a19e31761992d572949d358f28
revision_id: rev_37a8156586a9613d53114e704274954cba1c6d658971f0858c9fd32fd56ab3d9
event_id: evt_07c7aace31e00040d2ee76a1eba44c7b60d8663ab37fd63dd9b812d5ad6a851e
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.09014v1](<https://arxiv.org/abs/2602.09014v1>)
- **作者**: Zihan Yang, Shuyuan Tu, Licheng Zhang, Qi Dai, Yu-Gang Jiang, Zuxuan Wu
- **分类**: cs.CV
- **论文时间**: 2026-02-09T18:56:14Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.09014v1.pdf](<https://arxiv.org/pdf/2602.09014v1.pdf>)

## 来源摘要/节选

> Diffusion models have achieved remarkable generation quality, but they suffer from significant inference cost due to their reliance on multiple sequential denoising steps, motivating recent efforts to distill this inference process into a few-step regime. However, existing distillation methods typically approximate the teacher trajectory by using linear shortcuts, which makes it difficult to match its constantly changing tangent directions as velocities evolve across timesteps, thereby leading to quality degradation. To address this limitation, we propose ArcFlow, a few-step distillation framework that explicitly employs non-linear flow trajectories to approximate pre-trained teacher trajectories. Concretely, ArcFlow parameterizes the velocity field underlying the inference trajectory as a mixture of continuous momentum processes. This enables ArcFlow to capture velocity evolution and extrapolate coherent velocities to form a continuous non-linear trajectory within each denoising step. Importantly, this parameterization admits an analytical integration of this non-linear trajectory, which circumvents numerical discretization errors and results in high-precision approximation of the teacher trajectory. To train this parameterization into a few-step generator, we implement ArcFlow via trajectory distillation on pre-trained teacher models using lightweight adapters. This strategy ensures fast, stable convergence while preserving generative diversity and quality. Built on large-scale models \(Qwen-Image-20B and FLUX.1-dev\), ArcFlow only fine-tunes on less than 5% of original parameters and achieves a 40x speedup with 2 NFEs over the original multi-step teachers without significant quality degradation. Experiments on benchmarks show the effectiveness of ArcFlow both qualitatively and quantitatively.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
