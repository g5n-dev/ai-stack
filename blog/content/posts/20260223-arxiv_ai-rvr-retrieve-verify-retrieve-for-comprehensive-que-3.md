---
title: 'RVR: Retrieve-Verify-Retrieve for Comprehensive Question Answering'
date: 2026-02-23 22:40:51+08:00
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
external_url: https://arxiv.org/abs/2602.18425v1
aliases:
- /posts/20260224-arxiv_ai-rvr-retrieve-verify-retrieve-for-comprehensive-que-3/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:63ccf50889b5eb5d939c241a197b2ff43fe7ea81ecf0bf9a76f9bfdbe0e447d9
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 66
captured_at: '2026-07-18T04:16:23.555947Z'
source_capture_sha256: sha256:dde835478edf94f85db7f3d636e6d6345c30f16575992e2154f9b92fcfb73750
source_capture_chars_original: 1133
source_publication_excerpt_chars: 1133
observation_id: obs_2b4647d9117e322dec52ee4cc15dd3a5c0f857c7560b8ba45a06da13e562e31f
revision_id: rev_8fc5633ea31caa0ea69c1fe2246173cbf03e81388c3ca34734b0f49a5569e5c5
event_id: evt_abaea009c685b361bb8c84a3d04be6a236cc2b5602f31b656c678db848e624ae
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-23T03:53:16Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.18425v1](<https://arxiv.org/abs/2602.18425v1>)
- **作者**: Deniz Qian, Hung-Ting Chen, Eunsol Choi
- **分类**: cs.CL
- **论文时间**: 2026-02-20T18:48:05Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.18425v1.pdf](<https://arxiv.org/pdf/2602.18425v1.pdf>)

## 来源摘要/节选

> Comprehensively retrieving diverse documents is crucial to address queries that admit a wide range of valid answers. We introduce retrieve-verify-retrieve \(RVR\), a multi-round retrieval framework designed to maximize answer coverage. Initially, a retriever takes the original query and returns a candidate document set, followed by a verifier that identifies a high-quality subset. For subsequent rounds, the query is augmented with previously verified documents to uncover answers that are not yet covered in previous rounds. RVR is effective even with off-the-shelf retrievers, and fine-tuning retrievers for our inference procedure brings further gains. Our method outperforms baselines, including agentic search approaches, achieving at least 10% relative and 3% absolute gain in complete recall percentage on a multi-answer retrieval dataset \(QAMPARI\). We also see consistent gains on two out-of-domain datasets \(QUEST and WebQuestionsSP\) across different base retrievers. Our work presents a promising iterative approach for comprehensive answer recall leveraging a verifier and adapting retrievers to a new inference scenario.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
