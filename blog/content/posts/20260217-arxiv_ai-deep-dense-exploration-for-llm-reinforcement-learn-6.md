---
title: Deep Dense Exploration for LLM Reinforcement Learning via Pivot-Driven Resampling
date: 2026-02-17 03:10:02+08:00
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
external_url: https://arxiv.org/abs/2602.14169v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:be6f18d208ce366ae77e0900abb5278ea58dd9d6528fb1c4b5c76160f4f5725c
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 81
captured_at: '2026-07-18T04:15:33.978565Z'
source_capture_sha256: sha256:d84a0d2a409169a9b3398ba1cec5b6849b60070973b41c83c946dba02a279833
source_capture_chars_original: 1345
source_publication_excerpt_chars: 1345
observation_id: obs_2426f8fa4a9d69d5512cc56eb0b849270e03018809762f720c037fb322d92e35
revision_id: rev_bc1a0529a9b23a5e3471b6df06c8256db44e62a53060702eaf03db4991d74593
event_id: evt_13b67cd6cd0ceb4ab34aa0391b44ab91ded2fbdfaec6b20036ed5b873711fbd9
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.14169v1](<https://arxiv.org/abs/2602.14169v1>)
- **作者**: Yiran Guo, Zhongjian Qiao, Yingqi Xie, Jie Liu, Dan Ye, Ruiqing Zhang, Shuang Qiu, Lijie Xu
- **分类**: cs.LG
- **论文时间**: 2026-02-15T14:44:15Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.14169v1.pdf](<https://arxiv.org/pdf/2602.14169v1.pdf>)

## 来源摘要/节选

> Effective exploration is a key challenge in reinforcement learning for large language models: discovering high-quality trajectories within a limited sampling budget from the vast natural language sequence space. Existing methods face notable limitations: GRPO samples exclusively from the root, saturating high-probability trajectories while leaving deep, error-prone states under-explored. Tree-based methods blindly disperse budgets across trivial or unrecoverable states, causing sampling dilution that fails to uncover rare correct suffixes and destabilizes local baselines. To address this, we propose Deep Dense Exploration \(DDE\), a strategy that focuses exploration on $\\textit\{pivots\}$-deep, recoverable states within unsuccessful trajectories. We instantiate DDE with DEEP-GRPO, which introduces three key innovations: \(1\) a lightweight data-driven utility function that automatically balances recoverability and depth bias to identify pivot states; \(2\) local dense resampling at each pivot to increase the probability of discovering correct subsequent trajectories; and \(3\) a dual-stream optimization objective that decouples global policy learning from local corrective updates. Experiments on mathematical reasoning benchmarks demonstrate that our method consistently outperforms GRPO, tree-based methods, and other strong baselines.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
