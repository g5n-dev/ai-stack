---
title: 'ProxyFL: A Proxy-Guided Framework for Federated Semi-Supervised Learning'
date: 2026-02-25 02:57:16+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.21078v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:559fd8ac6429f3dddb5598525a08ca82bb476be9c32f4cea6b185684c75bab1d
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 72
captured_at: '2026-07-18T04:16:49.996029Z'
source_capture_sha256: sha256:9529dfac6726a2a8d25c25a587a29cbdd1f768ea52da0b62270e2bef5be3d3b6
source_capture_chars_original: 1525
source_publication_excerpt_chars: 1525
observation_id: obs_4bc39471741f510f662887da16d42363a15426cf04d40b5791443108ecd7225f
revision_id: rev_9f3f7caf239df057c699bfb1138ba0d3d65714e23bf9759299db491c1323ec8c
event_id: evt_941c1e9589cafd5b5fa05941a7091124f90298f64d81cd1c12a087869b5d0b52
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-25T03:56:57Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.21078v1](<https://arxiv.org/abs/2602.21078v1>)
- **作者**: Duowen Chen, Yan Wang
- **分类**: cs.LG
- **论文时间**: 2026-02-24T16:41:16Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.21078v1.pdf](<https://arxiv.org/pdf/2602.21078v1.pdf>)

## 来源摘要/节选

> Federated Semi-Supervised Learning \(FSSL\) aims to collaboratively train a global model across clients by leveraging partially-annotated local data in a privacy-preserving manner. In FSSL, data heterogeneity is a challenging issue, which exists both across clients and within clients. External heterogeneity refers to the data distribution discrepancy across different clients, while internal heterogeneity represents the mismatch between labeled and unlabeled data within clients. Most FSSL methods typically design fixed or dynamic parameter aggregation strategies to collect client knowledge on the server \(external\) and / or filter out low-confidence unlabeled samples to reduce mistakes in local client \(internal\). But, the former is hard to precisely fit the ideal global distribution via direct weights, and the latter results in fewer data participation into FL training. To this end, we propose a proxy-guided framework called ProxyFL that focuses on simultaneously mitigating external and internal heterogeneity via a unified proxy. I.e., we consider the learnable weights of classifier as proxy to simulate the category distribution both locally and globally. For external, we explicitly optimize global proxy against outliers instead of direct weights; for internal, we re-include the discarded samples into training by a positive-negative proxy pool to mitigate the impact of potentially-incorrect pseudo-labels. Insight experiments &amp; theoretical analysis show our significant performance and convergence in FSSL.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
