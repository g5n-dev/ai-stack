---
title: Statistical Query Lower Bounds for Smoothed Agnostic Learning
date: 2026-02-25 23:30:40+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.21191v1
aliases:
- /posts/20260226-arxiv_ai-statistical-query-lower-bounds-for-smoothed-agnost-7/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:c31f21eeb75045b3ac5d1812327530c13a8c04acd1bd9a7683b31ac63def2a8a
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 61
captured_at: '2026-07-18T04:16:57.484529Z'
source_capture_sha256: sha256:80a55db05926fe06e0717a3bc7aff2b7a8aea296856fa748904bd6d411eea3e6
source_capture_chars_original: 1567
source_publication_excerpt_chars: 1567
observation_id: obs_fdb601ad67bba6b4781be3446251e68743de4bfe05b17bb47d4541ede6c18a31
revision_id: rev_3dcfcb1ba5cb5fd272cf819a8733fc9ac5f94db16319f879ba4e1bbc9d5c1ba2
event_id: evt_3a9a3c7a0ce382f4570b47eb932daf9f32e3cc4036119965a4856c9474a02a5b
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-25T06:28:27Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.21191v1](<https://arxiv.org/abs/2602.21191v1>)
- **作者**: Ilias Diakonikolas, Daniel M. Kane
- **分类**: cs.LG
- **论文时间**: 2026-02-24T18:46:46Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.21191v1.pdf](<https://arxiv.org/pdf/2602.21191v1.pdf>)

## 来源摘要/节选

> We study the complexity of smoothed agnostic learning, recently introduced by~\\cite\{CKKMS24\}, in which the learner competes with the best classifier in a target class under slight Gaussian perturbations of the inputs. Specifically, we focus on the prototypical task of agnostically learning halfspaces under subgaussian distributions in the smoothed model. The best known upper bound for this problem relies on $L\_1$-polynomial regression and has complexity $d^\{\\tilde\{O\}\(1/σ^2\) \\log\(1/ε\)\}$, where $σ$ is the smoothing parameter and $ε$ is the excess error. Our main result is a Statistical Query \(SQ\) lower bound providing formal evidence that this upper bound is close to best possible. In more detail, we show that \(even for Gaussian marginals\) any SQ algorithm for smoothed agnostic learning of halfspaces requires complexity $d^\{Ω\(1/σ^\{2\}+\\log\(1/ε\)\)\}$. This is the first non-trivial lower bound on the complexity of this task and nearly matches the known upper bound. Roughly speaking, we show that applying $L\_1$-polynomial regression to a smoothed version of the function is essentially best possible. Our techniques involve finding a moment-matching hard distribution by way of linear programming duality. This dual program corresponds exactly to finding a low-degree approximating polynomial to the smoothed version of the target function \(which turns out to be the same condition required for the $L\_1$-polynomial regression to work\). Our explicit SQ lower bound then comes from proving lower bounds on this approximation degree for the class of halfspaces.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
