---
title: 'Sketch2Colab: Sketch-Conditioned Multi-Human Animation via Controllable Flow
  Distillation'
date: 2026-03-03 23:28:17+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
- AI Agent
categories:
- 论文
scenarios:
- AI/ML项目
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2603.02190v1
aliases:
- /posts/20260304-arxiv_ai-sketch2colab-sketch-conditioned-multi-human-animat-8/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:ecb7b7a15d856bc9a905bec2384cc780c6ec44ed4b93f506af2803ddcc5b7abd
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 89
captured_at: '2026-07-18T04:26:38.668400Z'
source_capture_sha256: sha256:f1acd5a3355e8a7c9f09751ed004cb5a94d666b7de585cc5f744871776720cf4
source_capture_chars_original: 1366
source_publication_excerpt_chars: 1366
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.02190v1](<https://arxiv.org/abs/2603.02190v1>)
- **作者**: Divyanshu Daiya, Aniket Bera
- **分类**: cs.CV
- **论文时间**: 2026-03-02T18:52:51Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.02190v1.pdf](<https://arxiv.org/pdf/2603.02190v1.pdf>)

## 来源摘要/节选

> We present Sketch2Colab, which turns storyboard-style 2D sketches into coherent, object-aware 3D multi-human motion with fine-grained control over agents, joints, timing, and contacts. Conventional diffusion-based motion generators have advanced realism; however, achieving precise adherence to rich interaction constraints typically demands extensive training and/or costly posterior guidance, and performance can degrade under strong multi-entity conditioning. Sketch2Colab instead first learns a sketch-driven diffusion prior and then distills it into an efficient rectified-flow student operating in latent space for fast, stable sampling. Differentiable energies over keyframes, trajectories, and physics-based constraints directly shape the student's transport field, steering samples toward motions that faithfully satisfy the storyboard while remaining physically plausible. To capture coordinated interaction, we augment the continuous flow with a continuous-time Markov chain \(CTMC\) planner that schedules discrete events such as touches, grasps, and handoffs, modulating the dynamics to produce crisp, well-phased human-object-human collaborations. Experiments on CORE4D and InterHuman show that Sketch2Colab achieves state-of-the-art constraint adherence and perceptual quality while offering significantly faster inference than diffusion-only baselines.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
