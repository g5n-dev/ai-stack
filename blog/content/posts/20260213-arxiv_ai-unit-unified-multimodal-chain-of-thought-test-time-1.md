---
title: 'UniT: Unified Multimodal Chain-of-Thought Test-time Scaling'
date: 2026-02-13 23:30:43+08:00
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
external_url: https://arxiv.org/abs/2602.12279v1
aliases:
- /posts/20260214-arxiv_ai-unit-unified-multimodal-chain-of-thought-test-time-1/
- /posts/20260215-arxiv_ai-unit-unified-multimodal-chain-of-thought-test-time-1/
- /posts/20260216-arxiv_ai-unit-unified-multimodal-chain-of-thought-test-time-1/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:13809d4cfe009a34ea6a680987251c0e56999791a6f8e2d185b575813662a4c8
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 59
captured_at: '2026-07-18T04:15:26.440768Z'
source_capture_sha256: sha256:dd3adb61f5086b77508b69f814b8ed6a459ab837cc51f2158271b2a30856e250
source_capture_chars_original: 1537
source_publication_excerpt_chars: 1537
observation_id: obs_6b96321be25ea4f1baa9df7bfcc8acbf00cdb6a201d05b2d774c9b8925990b1e
revision_id: rev_c40d074ec38b95ca1da92181de588f7c2ce7948510bf698cb36eccc1cc5ffb75
event_id: evt_b609018c71f3e73e56c9e0b1ecb90630af33d5082071301358ee780f2cb10cb7
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-13T06:19:22Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.12279v1](<https://arxiv.org/abs/2602.12279v1>)
- **作者**: Leon Liangyu Chen, Haoyu Ma, Zhipeng Fan, Ziqi Huang, Animesh Sinha, Xiaoliang Dai, Jialiang Wang, Zecheng He, Jianwei Yang, Chunyuan Li, Junzhe Sun, Chu Wang, Serena Yeung-Levy, Felix Juefei-Xu
- **分类**: cs.CV
- **论文时间**: 2026-02-12T18:59:49Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.12279v1.pdf](<https://arxiv.org/pdf/2602.12279v1.pdf>)

## 来源摘要/节选

> Unified models can handle both multimodal understanding and generation within a single architecture, yet they typically operate in a single pass without iteratively refining their outputs. Many multimodal tasks, especially those involving complex spatial compositions, multiple interacting objects, or evolving instructions, require decomposing instructions, verifying intermediate results, and making iterative corrections. While test-time scaling \(TTS\) has demonstrated that allocating additional inference compute for iterative reasoning substantially improves language model performance, extending this paradigm to unified multimodal models remains an open challenge. We introduce UniT, a framework for multimodal chain-of-thought test-time scaling that enables a single unified model to reason, verify, and refine across multiple rounds. UniT combines agentic data synthesis, unified model training, and flexible test-time inference to elicit cognitive behaviors including verification, subgoal decomposition, and content memory. Our key findings are: \(1\) unified models trained on short reasoning trajectories generalize to longer inference chains at test time; \(2\) sequential chain-of-thought reasoning provides a more scalable and compute-efficient TTS strategy than parallel sampling; \(3\) training on generation and editing trajectories improves out-of-distribution visual reasoning. These results establish multimodal test-time scaling as an effective paradigm for advancing both generation and understanding in unified models.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
