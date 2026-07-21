---
title: 'HyCOP: Hybrid Composition Operators for Interpretable Learning of PDEs'
date: 2026-05-04 18:26:23+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2605.00820v1
aliases:
- /posts/20260505-arxiv_ai-hycop-hybrid-composition-operators-for-interpretab-0/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:ace871d80599ac9a5307a7293a629fe06766b52d172efc4f3e6f14196f47597a
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 70
captured_at: '2026-07-18T04:29:27.867360Z'
source_capture_sha256: sha256:9b939dff6562d122bacd81b6016f4c630f75d4fdb569a9e3dcb1949549f1eccb
source_capture_chars_original: 948
source_publication_excerpt_chars: 948
observation_id: obs_ed5c58bff321ef2729d21c202cf3b50323d5b7666ec84adb239cb0e43d074700
revision_id: rev_b0a0d10956a13827a2d01d0680d87d9c8def470f5aa13ffe645af1d006283ac0
event_id: evt_4b15271816e48cd9dffc1e2abce62144d738821bb0286d1764929327121012a4
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-05-04T03:55:08Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2605.00820v1](<https://arxiv.org/abs/2605.00820v1>)
- **作者**: Jinpai Zhao, Nishant Panda, Yen Ting Lin, Eirik Valseth, Diane Oyen, Clint Dawson
- **分类**: cs.CE
- **论文时间**: 2026-05-01T17:57:48Z
- **论文 PDF**: [https://arxiv.org/pdf/2605.00820v1.pdf](<https://arxiv.org/pdf/2605.00820v1.pdf>)

## 来源摘要/节选

> We introduce HyCOP, a modular framework that learns parametric PDE solution operators by composing simple modules \(advection, diffusion, learned closures, boundary handling\) in a query-conditioned way. Rather than learning a monolithic map, HyCOP learns a policy over short programs - which module to apply and for how long - conditioned on regime features and state statistics. Modules may be numerical sub-solvers or learned components, enabling hybrid surrogates evaluated at arbitrary query times without autoregressive rollout. Across diverse PDE benchmarks, HyCOP produces interpretable programs, delivers order-of-magnitude OOD improvements over monolithic neural operators, and supports modular transfer through dictionary updates \(e.g., boundary swaps, residual enrichment\). Our theory characterizes expressivity and gives an error decomposition that separates composition error from module error and doubles as a process-level diagnostic.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
