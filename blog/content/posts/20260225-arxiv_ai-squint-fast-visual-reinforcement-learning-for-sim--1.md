---
title: 'Squint: Fast Visual Reinforcement Learning for Sim-to-Real Robotics'
date: 2026-02-25 23:30:40+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.21203v1
aliases:
- /posts/20260226-arxiv_ai-squint-fast-visual-reinforcement-learning-for-sim--1/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:f128e36ece0ddaabc4134c53bbaa37e6dce66c8bfac9e6aca1644c6b2880d225
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 67
captured_at: '2026-07-18T04:16:57.484529Z'
source_capture_sha256: sha256:0c75a884916284babc72dfa64933829fbb0feb8879db1e2c8e4e1dc1c88ddea0
source_capture_chars_original: 1118
source_publication_excerpt_chars: 1118
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.21203v1](<https://arxiv.org/abs/2602.21203v1>)
- **作者**: Abdulaziz Almuzairee, Henrik I. Christensen
- **分类**: cs.RO
- **论文时间**: 2026-02-24T18:58:11Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.21203v1.pdf](<https://arxiv.org/pdf/2602.21203v1.pdf>)

## 来源摘要/节选

> Visual reinforcement learning is appealing for robotics but expensive -- off-policy methods are sample-efficient yet slow; on-policy methods parallelize well but waste samples. Recent work has shown that off-policy methods can train faster than on-policy methods in wall-clock time for state-based control. Extending this to vision remains challenging, where high-dimensional input images complicate training dynamics and introduce substantial storage and encoding overhead. To address these challenges, we introduce Squint, a visual Soft Actor Critic method that achieves faster wall-clock training than prior visual off-policy and on-policy methods. Squint achieves this via parallel simulation, a distributional critic, resolution squinting, layer normalization, a tuned update-to-data ratio, and an optimized implementation. We evaluate on the SO-101 Task Set, a new suite of eight manipulation tasks in ManiSkill3 with heavy domain randomization, and demonstrate sim-to-real transfer to a real SO-101 robot. We train policies for 15 minutes on a single RTX 3090 GPU, with most tasks converging in under 6 minutes.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
