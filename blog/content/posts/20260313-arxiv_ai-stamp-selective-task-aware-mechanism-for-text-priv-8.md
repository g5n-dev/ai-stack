---
title: 'STAMP: Selective Task-Aware Mechanism for Text Privacy'
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
external_url: https://arxiv.org/abs/2603.12237v1
aliases:
- /posts/20260314-arxiv_ai-stamp-selective-task-aware-mechanism-for-text-priv-8/
- /posts/20260315-arxiv_ai-stamp-selective-task-aware-mechanism-for-text-priv-8/
- /posts/20260316-arxiv_ai-stamp-selective-task-aware-mechanism-for-text-priv-8/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:24e1212b6c45800a0dbf996518cf3cdd460a98d2738a1d463cfcd12a92bd4e7f
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 54
captured_at: '2026-07-18T04:28:15.328315Z'
source_capture_sha256: sha256:a3fb16525d0c52a7c1672b25bb17b32eefdce7f8f8383bafcbf9b3be1f42dbec
source_capture_chars_original: 1303
source_publication_excerpt_chars: 1303
observation_id: obs_c6f94dcc41f3e5b0f14a65f3d46201b7b6884520dcaee6066cf6531f701288b1
revision_id: rev_35382cdd80aef6725ea48a61dd58c2bbb8cd1810f6b743c77ff99be0ca9f8b0d
event_id: evt_e6f23c2a941957c024c6016b7ea7319e517b9344ad0eb918dcb73752f95c1dc7
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.12237v1](<https://arxiv.org/abs/2603.12237v1>)
- **作者**: Fengwei Tian, Payel Bhattacharjee, Heidi Hanson, Geoffrey D. Rubin, Joseph Y. Lo, Ravi Tandon
- **分类**: cs.LG
- **论文时间**: 2026-03-12T17:55:07Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.12237v1.pdf](<https://arxiv.org/pdf/2603.12237v1.pdf>)

## 来源摘要/节选

> We present STAMP \(Selective Task-Aware Mechanism for Text Privacy\), a new framework for task-aware text privatization that achieves an improved privacy-utility trade-off. STAMP selectively allocates privacy budgets across tokens by jointly considering \(i\) each token's importance to the downstream task \(as measured via a task- or query-specific representation\), and \(ii\) its privacy sensitivity \(e.g., names, dates, identifiers\). This token-level partitioning enables fine-grained, group-wise control over the level of noise applied to different parts of the input, balancing privacy protection with task relevance. To privatize individual token embeddings, we introduce the polar mechanism, which perturbs only the direction of embeddings on the unit sphere while preserving their magnitude. Decoding is performed via cosine nearest-neighbor search, aligning the perturbation geometry with the decoding geometry. Unlike isotropic noise mechanisms, the polar mechanism maintains semantic neighborhoods in the embedding space and better preserves downstream utility. Experimental evaluations on SQuAD, Yelp, and AG News datasets demonstrate that STAMP, when combined with the normalized polar mechanism, consistently achieves superior privacy-utility trade-offs across varying per-token privacy budgets.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
