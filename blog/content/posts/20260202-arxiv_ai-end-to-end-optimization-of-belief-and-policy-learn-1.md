---
title: End-to-end Optimization of Belief and Policy Learning in Shared Autonomy Paradigms
date: 2026-02-02 19:22:59+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2601.23285v1
aliases:
- /posts/20260203-arxiv_ai-end-to-end-optimization-of-belief-and-policy-learn-1/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:2b0cefe6bef78a26712fa07908a38bea5d0d34b7c7ff557b57b395621652d74d
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 82
captured_at: '2026-07-18T04:10:04.354932Z'
source_capture_sha256: sha256:f434bf6080d85b797aedcea5914d375cf207ca301ceb8937963a84d755635626
source_capture_chars_original: 1900
source_publication_excerpt_chars: 1900
observation_id: obs_59a6073351e7d53a25f66d5c294a6430a400f11e3dd511aff1bf062a3338ea7d
revision_id: rev_c96c1dcbd50f13f84568869652ae1f24a89c0546c0783fa4e102e31068aa7f6d
event_id: evt_e7f76daf797917531424241a220adb74178c98ac4866aeeb6cc37ed1c007c17a
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-02T05:34:45Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2601.23285v1](<https://arxiv.org/abs/2601.23285v1>)
- **作者**: MH Farhadi, Ali Rabiee, Sima Ghafoori, Anna Cetera, Andrew Fisher, Reza Abiri
- **分类**: cs.RO
- **论文时间**: 2026-01-30T18:59:16Z
- **论文 PDF**: [https://arxiv.org/pdf/2601.23285v1.pdf](<https://arxiv.org/pdf/2601.23285v1.pdf>)

## 来源摘要/节选

> Shared autonomy systems require principled methods for inferring user intent and determining appropriate assistance levels. This is a central challenge in human-robot interaction, where systems must be successful while being mindful of user agency. Previous approaches relied on static blending ratios or separated goal inference from assistance arbitration, leading to suboptimal performance in unstructured environments. We introduce BRACE \(Bayesian Reinforcement Assistance with Context Encoding\), a novel framework that fine-tunes Bayesian intent inference and context-adaptive assistance through an architecture enabling end-to-end gradient flow between intent inference and assistance arbitration. Our pipeline conditions collaborative control policies on environmental context and complete goal probability distributions. We provide analysis showing \(1\) optimal assistance levels should decrease with goal uncertainty and increase with environmental constraint severity, and \(2\) integrating belief information into policy learning yields a quadratic expected regret advantage over sequential approaches. We validated our algorithm against SOTA methods \(IDA, DQN\) using a three-part evaluation progressively isolating distinct challenges of end-effector control: \(1\) core human-interaction dynamics in a 2D human-in-the-loop cursor task, \(2\) non-linear dynamics of a robotic arm, and \(3\) integrated manipulation under goal ambiguity and environmental constraints. We demonstrate improvements over SOTA, achieving 6.3% higher success rates and 41% increased path efficiency, and 36.3% success rate and 87% path efficiency improvement over unassisted control. Our results confirmed that integrated optimization is most beneficial in complex, goal-ambiguous scenarios, and is generalizable across robotic domains requiring goal-directed assistance, advancing the SOTA for adaptive shared autonomy.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
