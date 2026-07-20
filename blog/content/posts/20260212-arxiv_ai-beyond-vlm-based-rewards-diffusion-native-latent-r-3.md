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
observation_id: obs_2ccc44f95e8ec65c1a6365cfc7d0732b217633bb2d9213b18e85fd23bf776b31
revision_id: rev_bc919d9f6b43107c7fd892becad8a2d9125d76d5c9a71713e4bd0185fc572e06
event_id: evt_f69e8757b6e3e5ec6592025e198310762867944017c6c5f67bd024e61cd2c948
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
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
