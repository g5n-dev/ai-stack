---
title: 'VLK: Learning Humanoid Loco-Manipulation from Synthetic Interactions in Reconstructed
  Scenes'
date: 2026-06-30 23:30:05+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2606.30645v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:5bd71657ff69ab8dbb35bd4293b6cfabfccb2d42ffbbb5e3ffe1c716d8f7c0ce
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 92
captured_at: '2026-07-18T04:30:14.398876Z'
source_capture_sha256: sha256:308da9794c2b53c778314ea98f1eddf5caef1ef0875a78a73273f45674fd9b97
source_capture_chars_original: 1248
source_publication_excerpt_chars: 1248
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2606.30645v1](<https://arxiv.org/abs/2606.30645v1>)
- **作者**: Yen-Jen Wang, Jiaman Li, Sirui Chen, Takara E. Truong, Pei Xu, Pieter Abbeel, Rocky Duan, Koushil Sreenath, Angjoo Kanazawa, Carmelo Sferrazza, Guanya Shi, Karen Liu
- **分类**: cs.RO
- **论文时间**: 2026-06-29T17:59:55Z
- **论文 PDF**: [https://arxiv.org/pdf/2606.30645v1.pdf](<https://arxiv.org/pdf/2606.30645v1.pdf>)

## 来源摘要/节选

> Perception-based humanoid loco-manipulation requires connecting egocentric observations and task instructions to whole-body motion. Learning this mapping requires synchronized egocentric images, language commands, and robot-compatible kinematic trajectories, yet no existing data source provides this complete tuple at scale. We address this bottleneck by generating vision-language-kinematics \(VLK\) supervision synthetically in reconstructed scenes. Our pipeline leverages 3D Gaussian Splatting to reconstruct metric-scale indoor environments, synthesizes navigation and object-interaction trajectories using privileged scene information, and renders paired egocentric observations after the fact. We produce 48,000 paired trajectories with no human intervention and train a VLK policy that predicts short-horizon whole-body kinematic trajectories. A whole-body tracker converts these predictions into actions on the physical humanoid. We evaluate on the physical Unitree G1 performing navigation and single-object transport, demonstrating that synthesized interactions in reconstructed scenes provide effective supervision for sim-to-real perception-based humanoid loco-manipulation. Project Website: https://vision-language-kinematics.github.io/

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
