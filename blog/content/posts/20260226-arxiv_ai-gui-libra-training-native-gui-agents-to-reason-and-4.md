---
title: 'GUI-Libra: Training Native GUI Agents to Reason and Act with Action-aware
  Supervision and Partially Verifiable RL'
date: 2026-02-26 23:29:19+08:00
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
external_url: https://arxiv.org/abs/2602.22190v1
aliases:
- /posts/20260227-arxiv_ai-gui-libra-training-native-gui-agents-to-reason-and-4/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:520b97795710a1ce92193694253249e5d8b5f777263dd64974434840af7b45c8
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 113
captured_at: '2026-07-18T04:17:05.285632Z'
source_capture_sha256: sha256:66298bdcd085f8921ad43cfdc9c2d4af7cdfd3ce5c900d77b49701956343b314
source_capture_chars_original: 1867
source_publication_excerpt_chars: 1867
observation_id: obs_dccec55f3e043a112cee93bf1d1855412cbebdc348b664830c8697a0129fd239
revision_id: rev_0657cb8910acf32ac3d3660483485981e31c721d211dccda749fdc8810bc2977
event_id: evt_f1590aacbc3e56472ea0a60c92759fc69dfd36933532ae4aea5ebc30a7378a21
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-26T06:26:37Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.22190v1](<https://arxiv.org/abs/2602.22190v1>)
- **作者**: Rui Yang, Qianhui Wu, Zhaoyang Wang, Hanyang Chen, Ke Yang, Hao Cheng, Huaxiu Yao, Baoling Peng, Huan Zhang, Jianfeng Gao, Tong Zhang
- **分类**: cs.LG
- **论文时间**: 2026-02-25T18:34:57Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.22190v1.pdf](<https://arxiv.org/pdf/2602.22190v1.pdf>)

## 来源摘要/节选

> Open-source native GUI agents still lag behind closed-source systems on long-horizon navigation tasks. This gap stems from two limitations: a shortage of high-quality, action-aligned reasoning data, and the direct adoption of generic post-training pipelines that overlook the unique challenges of GUI agents. We identify two fundamental issues in these pipelines: \(i\) standard SFT with CoT reasoning often hurts grounding, and \(ii\) step-wise RLVR-tyle training faces partial verifiability, where multiple actions can be correct but only a single demonstrated action is used for verification. This makes offline step-wise metrics weak predictors of online task success. In this work, we present GUI-Libra, a tailored training recipe that addresses these challenges. First, to mitigate the scarcity of action-aligned reasoning data, we introduce a data construction and filtering pipeline and release a curated 81K GUI reasoning dataset. Second, to reconcile reasoning with grounding, we propose action-aware SFT that mixes reasoning-then-action and direct-action data and reweights tokens to emphasize action and grounding. Third, to stabilize RL under partial verifiability, we identify the overlooked importance of KL regularization in RLVR and show that a KL trust region is critical for improving offline-to-online predictability; we further introduce success-adaptive scaling to downweight unreliable negative gradients. Across diverse web and mobile benchmarks, GUI-Libra consistently improves both step-wise accuracy and end-to-end task completion. Our results suggest that carefully designed post-training and data curation can unlock significantly stronger task-solving capabilities without costly online data collection. We release our dataset, code, and models to facilitate further research on data-efficient post-training for reasoning-capable GUI agents.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
