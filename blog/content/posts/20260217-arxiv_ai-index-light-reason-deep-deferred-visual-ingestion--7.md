---
title: 'Index Light, Reason Deep: Deferred Visual Ingestion for Visual-Dense Document
  Question Answering'
date: 2026-02-17 03:10:02+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.14162v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:6b07e43faca3edfb92a4f62541d016bec78e646fbdf534ad63ff569bcc2b46a0
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 96
captured_at: '2026-07-18T04:15:37.655804Z'
source_capture_sha256: sha256:2b738fb21e47249719f3b33f45ea3938b301ebbf5ad0b1e97bc9d4b9ab1ffdd6
source_capture_chars_original: 1627
source_publication_excerpt_chars: 1627
observation_id: obs_0610d6e00be17b0381589da746157a73d4e7727e8c31d2b098da567b2b3c4ef9
revision_id: rev_bcc807f015459048fc0d36341a95f74f869bf130ceb16d812645c7525e909f78
event_id: evt_7b51bec33fe18a8c0a3da22226eb4adaee8bc5d2d6af3a93302672753a9d5001
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.14162v1](<https://arxiv.org/abs/2602.14162v1>)
- **作者**: Tao Xu
- **分类**: cs.CL
- **论文时间**: 2026-02-15T14:23:50Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.14162v1.pdf](<https://arxiv.org/pdf/2602.14162v1.pdf>)

## 来源摘要/节选

> Existing multimodal document question answering methods universally adopt a supply-side ingestion strategy: running a Vision-Language Model \(VLM\) on every page during indexing to generate comprehensive descriptions, then answering questions through text retrieval. However, this "pre-ingestion" approach is costly \(a 113-page engineering drawing package requires approximately 80,000 VLM tokens\), end-to-end unreliable \(VLM outputs may fail to be correctly retrieved due to format mismatches in the retrieval infrastructure\), and irrecoverable once it fails. This paper proposes the Deferred Visual Ingestion \(DVI\) framework, adopting a demand-side ingestion strategy: the indexing phase performs only lightweight metadata extraction, deferring visual understanding to the moment users pose specific questions. DVI's core principle is "Index for locating, not understanding"--achieving page localization through structured metadata indexes and BM25 full-text search, then sending original images along with specific questions to a VLM for targeted analysis. Experiments on two real industrial engineering drawings \(113 pages + 7 pages\) demonstrate that DVI achieves comparable overall accuracy at zero ingestion VLM cost \(46.7% vs. 48.9%\), an effectiveness rate of 50% on visually necessary queries \(vs. 0% for pre-ingestion\), and 100% page localization \(98% search space compression\). DVI also supports interactive refinement and progressive caching, transforming the "QA accuracy" problem into a "page localization" problem--once the correct drawing page is found, obtaining the answer becomes a matter of interaction rounds.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
