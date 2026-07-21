---
title: 'MemSkill: Learning and Evolving Memory Skills for Self-Evolving Agents'
date: 2026-02-03 23:08:59+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
- AI Agent
- 大语言模型
categories:
- 论文
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.02474v1
aliases:
- /posts/20260204-arxiv_ai-memskill-learning-and-evolving-memory-skills-for-s-9/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:64da401af37a39b48595ac21493276ec5200c4cfd6b877db5f4842795a41034f
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 70
captured_at: '2026-07-18T04:10:30.388786Z'
source_capture_sha256: sha256:a40ae1bfc91c0425926db11e9070ac06c800c15af9f8f186a26ce8a109ccb2ca
source_capture_chars_original: 1428
source_publication_excerpt_chars: 1428
observation_id: obs_55d9428146d01416227ae0fdabd427cf1ab8a03bbfc111c0f3a0902761e52e5c
revision_id: rev_3552a2194fbe7e0387ea57149113f89be8e69838f6950e43f6e92eb4113ab588
event_id: evt_449abc77a350bdd7e18c83602f9369174155d06409a1ed1989e767370d5d7a46
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-03T05:27:06Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.02474v1](<https://arxiv.org/abs/2602.02474v1>)
- **作者**: Haozhen Zhang, Quanyu Long, Jianzhu Bao, Tao Feng, Weizhi Zhang, Haodong Yue, Wenya Wang
- **分类**: cs.CL
- **论文时间**: 2026-02-02T18:53:28Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.02474v1.pdf](<https://arxiv.org/pdf/2602.02474v1.pdf>)

## 来源摘要/节选

> Most Large Language Model \(LLM\) agent memory systems rely on a small set of static, hand-designed operations for extracting memory. These fixed procedures hard-code human priors about what to store and how to revise memory, making them rigid under diverse interaction patterns and inefficient on long histories. To this end, we present \\textbf\{MemSkill\}, which reframes these operations as learnable and evolvable memory skills, structured and reusable routines for extracting, consolidating, and pruning information from interaction traces. Inspired by the design philosophy of agent skills, MemSkill employs a \\emph\{controller\} that learns to select a small set of relevant skills, paired with an LLM-based \\emph\{executor\} that produces skill-guided memories. Beyond learning skill selection, MemSkill introduces a \\emph\{designer\} that periodically reviews hard cases where selected skills yield incorrect or incomplete memories, and evolves the skill set by proposing refinements and new skills. Together, MemSkill forms a closed-loop procedure that improves both the skill-selection policy and the skill set itself. Experiments on LoCoMo, LongMemEval, HotpotQA, and ALFWorld demonstrate that MemSkill improves task performance over strong baselines and generalizes well across settings. Further analyses shed light on how skills evolve, offering insights toward more adaptive, self-evolving memory management for LLM agents.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
