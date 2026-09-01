---
title: "OntoAligner-Ensemble: Voting-Based Fusion across Heterogeneous Ontology Alignment Techniques"
date: 2026-09-01T22:56:40+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "cs.AI", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:e3ae38f7c0cd97874960db692fa5693bfd2464840aeecf3a2d600b175e176a54"
source_payload_sha256: "sha256:e2845af34b97079225ea570035f51591ab32faae18458e312ec9708c3a517311"
observation_id: obs_f0ce4747db968efb6971a1654040dc95d5e03c4b61ccbb302394b598a4561567
event_id: evt_215cba148d1874ba738e4fd5d925df23cf5204fcb6682a7b5f8171cc30ccfe64
revision_id: rev_071969c90342c71438849c8648bbb2debbd24110515f757c0b377dfa56d4d540
source_published_at: 2026-08-31T17:44:25Z
first_seen_at: 2026-09-01T15:06:55Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 92
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2608.31137v1
parent_observation_id: null
last_seen_at: 2026-09-01T14:53:09.314998Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.31137v1](http://arxiv.org/abs/2608.31137v1)
- **发布域名**: arxiv.org
- **分类**: cs.AI
- **作者**: Hamed Babaei Giglou、Sören Auer、Peio Popov 等

## 来源摘要/节选

> Ontology alignment (OA) has evolved through several methodological paradigms, ranging from lexical and structural aligners to knowledge graph embedding (KGE) models and, more recently, Large Language Model (LLM)-based approaches. Although modern OA frameworks provide unified ecosystems for deploying these heterogeneous aligners, mechanisms for systematically reconciling their complementary and sometimes conflicting predictions remain relatively underexplored. We present OntoAligner-Ensemble, a modular and aligner-agnostic framework that combines candidate correspondences through a configurable two-stage process comprising voting-based fusion strategies followed by post-fusion selection policies. The framework supports any aligner implemented within OntoAligner that produces candidate correspondences, enabling diverse alignment paradigms to be integrated through a unified decision process. To demonstrate its effectiveness, we instantiate the framework using representative lightweight string-aligner, KGE-based, and Retrieval-Augmented Generation aligners powered by both open-weight and API-based LLMs. We evaluate individual aligners and ensemble configurations across eight benchmark tasks from five OAEI tracks spanning biomedical to beyond-equivalence. The results show that ensemble fusion consistently improves the balance between precision and recall and frequently outperforms standalone aligners across diverse domains. Furthermore, our analysis reveals that ensemble composition directly affects the precision-recall trade-off: heterogeneous cross-paradigm ensembles generally improve precision, whereas homogeneous LLM ensembles more often achieve higher overall F1-scores. These findings demonstrate that systematic ensemble learning offers a robust and reproducible strategy for OA while providing practical guidance for selecting ensemble compositions under different alignment scenarios.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。