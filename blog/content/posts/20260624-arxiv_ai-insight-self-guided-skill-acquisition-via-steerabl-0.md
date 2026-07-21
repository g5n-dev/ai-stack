---
title: 'InSight: Self-Guided Skill Acquisition via Steerable VLAs'
date: 2026-06-24 22:00:08+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2606.24884v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:b329493f1fe767231542e8d807fc7c6130d597813e452cfc3cdc7df6d4245c9b
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 57
captured_at: '2026-07-18T04:30:09.568344Z'
source_capture_sha256: sha256:9b58951b8616fdba0dc45e89ed9bf5ddb8793dbd2c4228fd26b8fe65dcb9b793
source_capture_chars_original: 1402
source_publication_excerpt_chars: 1402
observation_id: obs_dc5f14e9c77719626b45337e8783c25b4e92b9c8c1a5baac6590f8c74134f438
revision_id: rev_109960d43dd8741a062a618f882c3041009fd18fbe37e1ea1a79a8bd41808034
event_id: evt_bc4c3221ec1bff776367c698310e9aa59b704e3e1f8032d440d9c6551f0d2421
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2606.24884v1](<https://arxiv.org/abs/2606.24884v1>)
- **作者**: Maggie Wang, Lars Osterberg, Stephen Tian, Ola Shorinwa, Jiajun Wu, Mac Schwager
- **分类**: cs.RO
- **论文时间**: 2026-06-23T17:59:01Z
- **论文 PDF**: [https://arxiv.org/pdf/2606.24884v1.pdf](<https://arxiv.org/pdf/2606.24884v1.pdf>)

## 来源摘要/节选

> Vision-language-action \(VLA\) models can learn manipulation skills from demonstrations, but their capabilities are bounded by the skills in the training data. We present InSight, a framework that unlocks autonomous skill acquisition by rendering VLAs steerable at the primitive-action level \(e.g., "move gripper to the bowl", "lift upward", "pour the bottle"\). InSight consists of two primary stages: \(1\) an automated segmentation pipeline that partitions demonstrations into labeled primitives via VLM plan decomposition and end-effector poses to enable VLA primitive steerability, and \(2\) a VLM-guided data flywheel that identifies missing primitives required to accomplish a novel task, autonomously attempts demonstrations of the missing primitives with VLM-proposed low-level control, and automatically labels, stores, and integrates successful demonstrations into the VLA training set. We evaluate InSight across simulation and real-world manipulation tasks, including block flipping, drawer closing, sweeping, twisting, and pouring, without any human demonstrations of these target skills. Once learned, these primitives can be composed to execute novel, long-horizon tasks without additional human demonstrations. Our findings demonstrate that primitive steerability provides a practical foundation for continual skill acquisition in VLA policies. Project website: https://insight-vla.github.io.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
