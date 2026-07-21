---
title: 'Visual-ERM: Reward Modeling for Visual Equivalence'
date: 2026-03-16 23:16:09+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2603.13224v1
aliases:
- /posts/20260317-arxiv_ai-visual-erm-reward-modeling-for-visual-equivalence-2/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:aeaa5eb07600a09d790a184a02846df80d31303225458f34ce2345de46577847
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 50
captured_at: '2026-07-18T04:28:19.053555Z'
source_capture_sha256: sha256:96be94274d500f78589b0d389666b58914f421e06a4c2fdf7a0cb6a30739fd57
source_capture_chars_original: 1441
source_publication_excerpt_chars: 1441
observation_id: obs_6285bb907840ea998ffc409dd2ba06537403ad323c2c7a1a19e6ff52f21ea450
revision_id: rev_eb9fd0713d2d00bdc5ef1774ce35c66c741b48d87580f9ce4ad8c38571ad87cf
event_id: evt_5496d799c6dc593e3fea1f6b1b2020e34116a4d2ca5a6e94569bed1eadd25e15
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.13224v1](<https://arxiv.org/abs/2603.13224v1>)
- **作者**: Ziyu Liu, Shengyuan Ding, Xinyu Fang, Xuanlang Dai, Penghui Yang, Jianze Liang, Jiaqi Wang, Kai Chen, Dahua Lin, Yuhang Zang
- **分类**: cs.CV
- **论文时间**: 2026-03-13T17:58:14Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.13224v1.pdf](<https://arxiv.org/pdf/2603.13224v1.pdf>)

## 来源摘要/节选

> Vision-to-code tasks require models to reconstruct structured visual inputs, such as charts, tables, and SVGs, into executable or structured representations with high visual fidelity. While recent Large Vision Language Models \(LVLMs\) achieve strong results via supervised fine-tuning, reinforcement learning remains challenging due to misaligned reward signals. Existing rewards either rely on textual rules or coarse visual embedding similarity, both of which fail to capture fine-grained visual discrepancies and are vulnerable to reward hacking. We propose Visual Equivalence Reward Model \(Visual-ERM\), a multimodal generative reward model that provides fine-grained, interpretable, and task-agnostic feedback to evaluate vision-to-code quality directly in the rendered visual space. Integrated into RL, Visual-ERM improves Qwen3-VL-8B-Instruct by +8.4 on chart-to-code and yields consistent gains on table and SVG parsing \(+2.7, +4.1 on average\), and further strengthens test-time scaling via reflection and revision. We also introduce VisualCritic-RewardBench \(VC-RewardBench\), a benchmark for judging fine-grained image-to-image discrepancies on structured visual data, where Visual-ERM at 8B decisively outperforms Qwen3-VL-235B-Instruct and approaches leading closed-source models. Our results suggest that fine-grained visual reward supervision is both necessary and sufficient for vision-to-code RL, regardless of task specificity.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
