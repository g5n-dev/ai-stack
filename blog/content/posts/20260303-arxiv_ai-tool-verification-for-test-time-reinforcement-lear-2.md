---
title: Tool Verification for Test-Time Reinforcement Learning
date: 2026-03-03 23:28:17+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2603.02203v1
aliases:
- /posts/20260304-arxiv_ai-tool-verification-for-test-time-reinforcement-lear-2/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:4332fc1e9130cc89b8c5ea29f9cae34bb644949f4061f71ac1499be71d592439
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 54
captured_at: '2026-07-18T04:26:38.668400Z'
source_capture_sha256: sha256:c6989196a9cc0b3a02287312f4015d845240aef369fe6d0c41493bf126eafcc8
source_capture_chars_original: 1069
source_publication_excerpt_chars: 1069
observation_id: obs_441bc26fc96462b58f8f44397566ffa31504e9b32f9a19a243294d1fb246bffd
revision_id: rev_eaabdf67da596dae18518589c38595007391f0e6112062a79ad77896e299b47d
event_id: evt_4634a2c9d2ec5b8a77e1bf2ceea1b83559f21a1f3d19d284e0efffe255d17261
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.02203v1](<https://arxiv.org/abs/2603.02203v1>)
- **作者**: Ruotong Liao, Nikolai Röhrich, Xiaohan Wang, Yuhui Zhang, Yasaman Samadzadeh, Volker Tresp, Serena Yeung-Levy
- **分类**: cs.AI
- **论文时间**: 2026-03-02T18:57:52Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.02203v1.pdf](<https://arxiv.org/pdf/2603.02203v1.pdf>)

## 来源摘要/节选

> Test-time reinforcement learning \(TTRL\) has emerged as a promising paradigm for self-evolving large reasoning models \(LRMs\), enabling online adaptation on unlabeled test inputs via self-induced rewards through majority voting. However, a spurious yet high-frequency unverified consensus can become a biased and reinforced reward signal, leading to incorrect mode collapse. We address this failure mode with T^3RL \(Tool-Verification for Test-Time Reinforcement Learning\), which introduces test-time tool verification into reward estimation. Concretely, a verifier uses an external tool as evidence \(e.g., from code execution\) to upweight verified rollouts in a verification-aware voting, producing more reliable pseudo-labels for training. Across various math difficulties \(MATH-500, AMC, and AIME 2024\) and diverse backbone types, T^3RL significantly improves over TTRL, with larger gains on harder problems. More broadly, T^3RL can be viewed as verified online data synthesis, highlighting test-time tool verification as a key mechanism for stabilizing self-evolution.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
