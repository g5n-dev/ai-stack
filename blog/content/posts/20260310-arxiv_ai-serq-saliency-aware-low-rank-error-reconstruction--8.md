---
title: 'SERQ: Saliency-Aware Low-Rank Error Reconstruction for LLM Quantization'
date: 2026-03-10 02:45:40+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
- 大语言模型
categories:
- 论文
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2603.08185v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:8217e8bc2ea4dd0a406c0d401cfb85c603bcf9f493c9ddba75f96b9d2c7f96ca
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 71
captured_at: '2026-07-18T04:27:35.108002Z'
source_capture_sha256: sha256:ac0001c65eaffb53175fecb9f1a24df8d9756c17ea3f7841f8fa028e9db23d4a
source_capture_chars_original: 1832
source_publication_excerpt_chars: 1832
observation_id: obs_1830c9b03eebaad19f7278e2f2d1237695fc2382d7432feeee3f8d59ad7aa516
revision_id: rev_3023d1c0fe87d54e167b84f97dda79d42dc2dbcb85b777a2e2c38d4d02db1771
event_id: evt_a3fef483c769f1956d1f8f9bb1b0808c03ecee5d8bdcae11b038f678dadc8627
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.08185v1](<https://arxiv.org/abs/2603.08185v1>)
- **作者**: Yeonsik Park, Hyeonseong Kim, Seungkyu Choi
- **分类**: cs.LG
- **论文时间**: 2026-03-09T10:04:12Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.08185v1.pdf](<https://arxiv.org/pdf/2603.08185v1.pdf>)

## 来源摘要/节选

> Post-training quantization \(PTQ\) has emerged as a prevailing technique for deploying large language models \(LLMs\) efficiently in terms of both memory and computation, across edge devices and server platforms. Existing PTQ methods primarily aim to reduce precision in weights and activations by mitigating quantization errors caused by channel-wise outlier activations \(e.g., pre-quantization scaling, online transformations, or low-rank error reconstruction\). Among these approaches, error reconstruction with low-rank adaptation \(LoRA\) has proven particularly effective, as it introduces a lightweight auxiliary computation path without requiring heavy optimization or additional online layers. However, prior studies reveal severe accuracy degradation under W4A4 settings, and conventional low-rank adaptations rely on two sequential factors, necessitating intermediate quantization during inference and thereby limiting low-precision efficiency. In this work, we propose SERQ, a saliency-aware error reconstruction method for low-bit LLM inference that employs a single low-rank compensation matrix. SERQ preserves efficient 4-bit matrix multiplication in linear layers by jointly mitigating quantization errors arising from both activation and weight saliency through three stages: \(1\) static activation flattening, \(2\) saliency-aware error reconstruction, and \(3\) offline weight permutation. The method incurs additional computation only for low-rank error reconstruction via a single decomposition, while all other operations are performed offline, thereby keeping latency overhead minimal. Empirically, SERQ outperforms prior error reconstruction methods under both W4A8 and W4A4 settings, and achieves higher accuracy than state-of-the-art rotation-based W4A4 approaches, while substantially reducing calibration complexity.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
