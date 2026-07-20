---
title: Rethinking the Trust Region in LLM Reinforcement Learning
date: 2026-02-05 23:03:18+08:00
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
external_url: https://arxiv.org/abs/2602.04879v1
aliases:
- /posts/20260206-arxiv_ai-rethinking-the-trust-region-in-llm-reinforcement-l-3/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:fddddee89b98a6a800df77f6054436f3295285b6154cee28089948f748e42394
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 57
captured_at: '2026-07-18T04:10:53.549487Z'
source_capture_sha256: sha256:319607a78c81d381505cbb4b8bece163b88ea6668372a921f41567d58397544f
source_capture_chars_original: 1330
source_publication_excerpt_chars: 1330
observation_id: obs_235a95e33139074bb45d4c6bdfa3ae010c955f2102c4700af6a0712d77fe4b74
revision_id: rev_216454a55f9e6ba327867a116107ca79cf0178eb171c53f66800b4f4cfa27b3b
event_id: evt_99947be3dbd83d751fe25748d8eefb804a92ca8ceb6f429b1684210074fbbc3e
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.04879v1](<https://arxiv.org/abs/2602.04879v1>)
- **作者**: Penghui Qi, Xiangxin Zhou, Zichen Liu, Tianyu Pang, Chao Du, Min Lin, Wee Sun Lee
- **分类**: cs.LG
- **论文时间**: 2026-02-04T18:59:04Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.04879v1.pdf](<https://arxiv.org/pdf/2602.04879v1.pdf>)

## 来源摘要/节选

> Reinforcement learning \(RL\) has become a cornerstone for fine-tuning Large Language Models \(LLMs\), with Proximal Policy Optimization \(PPO\) serving as the de facto standard algorithm. Despite its ubiquity, we argue that the core ratio clipping mechanism in PPO is structurally ill-suited for the large vocabularies inherent to LLMs. PPO constrains policy updates based on the probability ratio of sampled tokens, which serves as a noisy single-sample Monte Carlo estimate of the true policy divergence. This creates a sub-optimal learning dynamic: updates to low-probability tokens are aggressively over-penalized, while potentially catastrophic shifts in high-probability tokens are under-constrained, leading to training inefficiency and instability. To address this, we propose Divergence Proximal Policy Optimization \(DPPO\), which substitutes heuristic clipping with a more principled constraint based on a direct estimate of policy divergence \(e.g., Total Variation or KL\). To avoid huge memory footprint, we introduce the efficient Binary and Top-K approximations to capture the essential divergence with negligible overhead. Extensive empirical evaluations demonstrate that DPPO achieves superior training stability and efficiency compared to existing methods, offering a more robust foundation for RL-based LLM fine-tuning.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
