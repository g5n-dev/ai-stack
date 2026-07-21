---
title: Native Active Perception as Reasoning for Omni-Modal Understanding
date: 2026-06-18 22:25:14+08:00
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
external_url: https://arxiv.org/abs/2606.19341v1
aliases:
- /posts/20260619-arxiv_ai-native-active-perception-as-reasoning-for-omni-mod-0/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:eb005e3bdf723856af7e5b7c031c007ddfa5502b78e2c3f4b6b5310475537d39
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 66
captured_at: '2026-07-18T04:30:09.568344Z'
source_capture_sha256: sha256:e9afb472289311e4b101caf9fc89e3de076648a96c557d30fc641355782b4a1d
source_capture_chars_original: 1489
source_publication_excerpt_chars: 1489
observation_id: obs_94756c4c65579c940c07383f2968220fbaf24bf5f8627067fa66bcb03b3b0cb8
revision_id: rev_ca47f4141226bd22ccf373a7ee9d2344dfc2767f207c8cedd87e6c0147ec65f7
event_id: evt_08932c21378674bbeba17794015badede2963970b54941617d655b6a559581e4
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-06-18T10:03:24Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2606.19341v1](<https://arxiv.org/abs/2606.19341v1>)
- **作者**: Zhenghao Xing, Ruiyang Xu, Yuxuan Wang, Jinzheng He, Ziyang Ma, Qize Yang, Yunfei Chu, Jin Xu, Junyang Lin, Chi-Wing Fu, Pheng-Ann Heng
- **分类**: cs.CV
- **论文时间**: 2026-06-17T17:59:56Z
- **论文 PDF**: [https://arxiv.org/pdf/2606.19341v1.pdf](<https://arxiv.org/pdf/2606.19341v1.pdf>)

## 来源摘要/节选

> Passive models for long video understanding typically rely on a "watch-it-all" paradigm, processing frames uniformly regardless of query difficulty, causing computational cost to grow with video duration. Although interactive frameworks have emerged, they often rely on global pre-scanning, and their context cost still scales with video length. We propose OmniAgent, the first native omni-modal agent that formulates video understanding as a POMDP-based iterative Observation-Thought-Action cycle. OmniAgent executes on-demand actions to selectively distill audio-visual cues into a persistent textual memory, effectively decoupling reasoning complexity from raw video duration. To operationalize this, we introduce \(1\) Agentic Supervised Fine-Tuning to bootstrap native active perception via best-of-N trajectory synthesis with dual-stage quality control, and \(2\) Agentic Reinforcement Learning with TAURA \(Turn-aware Adaptive Uncertainty Rescaled Advantage\), which leverages turn-level entropy to steer credit assignment toward pivotal discovery turns. Crucially, OmniAgent exhibits positive test-time scaling, where performance improves as the number of reasoning turns increases, validating the efficacy of active perception. Empirical results across ten benchmarks \(e.g., VideoMME, LVBench\) demonstrate that OmniAgent achieves state-of-the-art performance among open-source models. Notably, on LVBench, our 7B agent outperforms the 10$\\times$ larger Qwen2.5-VL-72B \(50.5% vs. 47.3%\).

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
