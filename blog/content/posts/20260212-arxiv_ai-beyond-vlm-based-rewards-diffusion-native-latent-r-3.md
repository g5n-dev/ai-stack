---
title: 'Beyond VLM-Based Rewards: Diffusion-Native Latent Reward Modeling'
date: 2026-02-12 23:40:07+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.11146v1
aliases:
- /posts/20260213-arxiv_ai-beyond-vlm-based-rewards-diffusion-native-latent-r-3/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:4338ecfee522153e549886b7da16bec6250c7d58611d9a16105b0c3cd53162b7
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 65
captured_at: '2026-07-18T04:14:51.451682Z'
source_capture_sha256: sha256:f533e4976426cec27f63eecb49e73c6abb42dcc377a96050594d6196d3fed952
source_capture_chars_original: 1345
source_publication_excerpt_chars: 1345
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.11146v1](<https://arxiv.org/abs/2602.11146v1>)
- **作者**: Gongye Liu, Bo Yang, Yida Zhi, Zhizhou Zhong, Lei Ke, Didan Deng, Han Gao, Yongxiang Huang, Kaihao Zhang, Hongbo Fu, Wenhan Luo
- **分类**: cs.CV
- **论文时间**: 2026-02-11T18:57:29Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.11146v1.pdf](<https://arxiv.org/pdf/2602.11146v1.pdf>)

## 来源摘要/节选

> Preference optimization for diffusion and flow-matching models relies on reward functions that are both discriminatively robust and computationally efficient. Vision-Language Models \(VLMs\) have emerged as the primary reward provider, leveraging their rich multimodal priors to guide alignment. However, their computation and memory cost can be substantial, and optimizing a latent diffusion generator through a pixel-space reward introduces a domain mismatch that complicates alignment. In this paper, we propose DiNa-LRM, a diffusion-native latent reward model that formulates preference learning directly on noisy diffusion states. Our method introduces a noise-calibrated Thurstone likelihood with diffusion-noise-dependent uncertainty. DiNa-LRM leverages a pretrained latent diffusion backbone with a timestep-conditioned reward head, and supports inference-time noise ensembling, providing a diffusion-native mechanism for test-time scaling and robust rewarding. Across image alignment benchmarks, DiNa-LRM substantially outperforms existing diffusion-based reward baselines and achieves performance competitive with state-of-the-art VLMs at a fraction of the computational cost. In preference optimization, we demonstrate that DiNa-LRM improves preference optimization dynamics, enabling faster and more resource-efficient model alignment.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
