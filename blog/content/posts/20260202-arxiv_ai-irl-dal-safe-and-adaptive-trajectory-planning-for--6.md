---
title: 'IRL-DAL: Safe and Adaptive Trajectory Planning for Autonomous Driving via
  Energy-Guided Diffusion Models'
date: 2026-02-02 19:22:59+08:00
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
external_url: https://arxiv.org/abs/2601.23266v1
aliases:
- /posts/20260203-arxiv_ai-irl-dal-safe-and-adaptive-trajectory-planning-for--6/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:4acb62fc7163e7c97c713e96da774c969d449e1960b71654ac700486f0eaab15
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 104
captured_at: '2026-07-18T04:10:15.469098Z'
source_capture_sha256: sha256:cdc7cc24ce5bd3857ac008264e52a0d86728c87f30e6c5df4b0d64acdb9a0ecf
source_capture_chars_original: 1248
source_publication_excerpt_chars: 1248
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2601.23266v1](<https://arxiv.org/abs/2601.23266v1>)
- **作者**: Seyed Ahmad Hosseini Miangoleh, Amin Jalal Aghdasian, Farzaneh Abdollahi
- **分类**: cs.RO
- **论文时间**: 2026-01-30T18:34:10Z
- **论文 PDF**: [https://arxiv.org/pdf/2601.23266v1.pdf](<https://arxiv.org/pdf/2601.23266v1.pdf>)

## 来源摘要/节选

> This paper proposes a novel inverse reinforcement learning framework using a diffusion-based adaptive lookahead planner \(IRL-DAL\) for autonomous vehicles. Training begins with imitation from an expert finite state machine \(FSM\) controller to provide a stable initialization. Environment terms are combined with an IRL discriminator signal to align with expert goals. Reinforcement learning \(RL\) is then performed with a hybrid reward that combines diffuse environmental feedback and targeted IRL rewards. A conditional diffusion model, which acts as a safety supervisor, plans safe paths. It stays in its lane, avoids obstacles, and moves smoothly. Then, a learnable adaptive mask \(LAM\) improves perception. It shifts visual attention based on vehicle speed and nearby hazards. After FSM-based imitation, the policy is fine-tuned with Proximal Policy Optimization \(PPO\). Training is run in the Webots simulator with a two-stage curriculum. A 96\\% success rate is reached, and collisions are reduced to 0.05 per 1k steps, marking a new benchmark for safe navigation. By applying the proposed approach, the agent not only drives in lane but also handles unsafe conditions at an expert level, increasing robustness.We make our code publicly available.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
