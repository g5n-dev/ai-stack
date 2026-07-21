---
title: Incremental Neural Network Verification via Learned Conflicts
date: 2026-03-13 23:24:24+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2603.12232v1
aliases:
- /posts/20260314-arxiv_ai-incremental-neural-network-verification-via-learne-9/
- /posts/20260315-arxiv_ai-incremental-neural-network-verification-via-learne-9/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:0c7e3beebd6111511b2d38dc417af22f3bdc76dd2540f1190adaf0c3cd76b0c1
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 61
captured_at: '2026-07-18T04:28:07.966279Z'
source_capture_sha256: sha256:379e640ca6fd4d62b587ccca741f9c8d75c9a74dd29417827472ab28bfa1b2b6
source_capture_chars_original: 1578
source_publication_excerpt_chars: 1578
observation_id: obs_f89fe3d523fb0c8d048ca2a5259cc3d4d62fc42b37312c8ad8864e49a097bc24
revision_id: rev_7f6836855d97aa9bb893ce6f8062a55ff571e797841df92a231f93c756c48c96
event_id: evt_158e1932108b84b6cb1fd7801cb8bf89f06f2580f162e4bd89fe55e21b9e2385
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.12232v1](<https://arxiv.org/abs/2603.12232v1>)
- **作者**: Raya Elsaleh, Liam Davis, Haoze Wu, Guy Katz
- **分类**: cs.LO
- **论文时间**: 2026-03-12T17:52:12Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.12232v1.pdf](<https://arxiv.org/pdf/2603.12232v1.pdf>)

## 来源摘要/节选

> Neural network verification is often used as a core component within larger analysis procedures, which generate sequences of closely related verification queries over the same network. In existing neural network verifiers, each query is typically solved independently, and information learned during previous runs is discarded, leading to repeated exploration of the same infeasible regions of the search space. In this work, we aim to expedite verification by reducing this redundancy. We propose an incremental verification technique that reuses learned conflicts across related verification queries. The technique can be added on top of any branch-and-bound-based neural network verifier. During verification, the verifier records conflicts corresponding to learned infeasible combinations of activation phases, and retains them across runs. We formalize a refinement relation between verification queries and show that conflicts learned for a query remain valid under refinement, enabling sound conflict inheritance. Inherited conflicts are handled using a SAT solver to perform consistency checks and propagation, allowing infeasible subproblems to be detected and pruned early during search. We implement the proposed technique in the Marabou verifier and evaluate it on three verification tasks: local robustness radius determination, verification with input splitting, and minimal sufficient feature set extraction. Our experiments show that incremental conflict reuse reduces verification effort and yields speedups of up to $1.9\\times$ over a non-incremental baseline.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
