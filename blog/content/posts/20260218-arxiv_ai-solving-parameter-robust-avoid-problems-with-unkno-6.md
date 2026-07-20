---
title: Solving Parameter-Robust Avoid Problems with Unknown Feasibility using Reinforcement
  Learning
date: 2026-02-18 21:10:38+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.15817v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:eb4425ffaab3ec6bb6ae1d1f291a4dac7617d709cc7e131a68693a26d24b86ff
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 93
captured_at: '2026-07-18T04:15:52.664467Z'
source_capture_sha256: sha256:288e8ff7d0f4840723127b82dcd107735bc277fa4127781185686854d07a7965
source_capture_chars_original: 1239
source_publication_excerpt_chars: 1239
observation_id: obs_aa71fa3aed66159e77718fa5565c3029e23c2540c999ce3b33c843cf56294d10
revision_id: rev_edde4fb950955fbaf66229ade5e4ac559bf281f16d80a9d8c87d542ac0337b49
event_id: evt_4301679b1afb5daee41e5337e49d00a4cc1076d7ebd46feef9d1db7c211f4afd
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.15817v1](<https://arxiv.org/abs/2602.15817v1>)
- **作者**: Oswin So, Eric Yang Yu, Songyuan Zhang, Matthew Cleaveland, Mitchell Black, Chuchu Fan
- **分类**: cs.LG
- **论文时间**: 2026-02-17T18:53:31Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.15817v1.pdf](<https://arxiv.org/pdf/2602.15817v1.pdf>)

## 来源摘要/节选

> Recent advances in deep reinforcement learning \(RL\) have achieved strong results on high-dimensional control tasks, but applying RL to reachability problems raises a fundamental mismatch: reachability seeks to maximize the set of states from which a system remains safe indefinitely, while RL optimizes expected returns over a user-specified distribution. This mismatch can result in policies that perform poorly on low-probability states that are still within the safe set. A natural alternative is to frame the problem as a robust optimization over a set of initial conditions that specify the initial state, dynamics and safe set, but whether this problem has a solution depends on the feasibility of the specified set, which is unknown a priori. We propose Feasibility-Guided Exploration \(FGE\), a method that simultaneously identifies a subset of feasible initial conditions under which a safe policy exists, and learns a policy to solve the reachability problem over this set of initial conditions. Empirical results demonstrate that FGE learns policies with over 50% more coverage than the best existing method for challenging initial conditions across tasks in the MuJoCo simulator and the Kinetix simulator with pixel observations.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
