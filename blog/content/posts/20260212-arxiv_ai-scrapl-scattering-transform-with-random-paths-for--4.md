---
title: 'SCRAPL: Scattering Transform with Random Paths for Machine Learning'
date: 2026-02-12 23:40:07+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
- 机器学习
- 计算机视觉
- Python
categories:
- 论文
scenarios:
- AI/ML项目
- 计算机视觉
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.11145v1
aliases:
- /posts/20260213-arxiv_ai-scrapl-scattering-transform-with-random-paths-for--4/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:630005b31bfa93ce7b290a97f1611c7f41b77828c41105a80ea8ae6462e6f308
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 67
captured_at: '2026-07-18T04:15:02.573604Z'
source_capture_sha256: sha256:c5bd877c77cf7d24e51ab36ee2f5adaa3ab068330d13bfd7e7bfb7fb96152e1b
source_capture_chars_original: 1337
source_publication_excerpt_chars: 1337
observation_id: obs_938bc58471260467104c614298051adf790ba2819b7a1b4814f7258fc29f4e2f
revision_id: rev_a45579be219bd5b07f16dc5b37a7901a08897befe063da63d714c075289c19cd
event_id: evt_4a90a6c209594f6186f6517ffe306d21300fc856563f8d676aef724392248336
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.11145v1](<https://arxiv.org/abs/2602.11145v1>)
- **作者**: Christopher Mitcheltree, Vincent Lostanlen, Emmanouil Benetos, Mathieu Lagrange
- **分类**: cs.SD
- **论文时间**: 2026-02-11T18:57:08Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.11145v1.pdf](<https://arxiv.org/pdf/2602.11145v1.pdf>)

## 来源摘要/节选

> The Euclidean distance between wavelet scattering transform coefficients \(known as paths\) provides informative gradients for perceptual quality assessment of deep inverse problems in computer vision, speech, and audio processing. However, these transforms are computationally expensive when employed as differentiable loss functions for stochastic gradient descent due to their numerous paths, which significantly limits their use in neural network training. Against this problem, we propose "Scattering transform with Random Paths for machine Learning" \(SCRAPL\): a stochastic optimization scheme for efficient evaluation of multivariable scattering transforms. We implement SCRAPL for the joint time-frequency scattering transform \(JTFS\) which demodulates spectrotemporal patterns at multiple scales and rates, allowing a fine characterization of intermittent auditory textures. We apply SCRAPL to differentiable digital signal processing \(DDSP\), specifically, unsupervised sound matching of a granular synthesizer and the Roland TR-808 drum machine. We also propose an initialization heuristic based on importance sampling, which adapts SCRAPL to the perceptual content of the dataset, improving neural network convergence and evaluation performance. We make our code and audio samples available and provide SCRAPL as a Python package.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
