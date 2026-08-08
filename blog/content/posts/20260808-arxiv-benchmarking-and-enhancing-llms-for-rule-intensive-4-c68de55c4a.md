---
title: "Benchmarking and Enhancing LLMs for Rule-Intensive Review of National Standard Documents"
date: 2026-08-08T04:02:59+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "cs.CL", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:54b058cab76995900a38d8714a9382bd34c1e0cf88a78223990af285b5ba5205"
source_payload_sha256: "sha256:112ac53661159b1dfb868f1bad4ad13a3c0eb71bd4e7261a50c5b1dd7016a333"
observation_id: obs_c68de55c4a744bddb050dbb4528b3ff1f55cca3f89bda725d14e3cf786ff76a7
event_id: evt_0e85aa0582c60aa6c3a0a6ace8b26a23f10a6ad74767cc9a25803a504f0666e2
revision_id: rev_898f835f9e2820e55bd50bd43087bc9b99a68f173ee5f4a429369c180c7a6a76
source_published_at: 2026-08-06T17:27:23Z
first_seen_at: 2026-08-07T20:12:33Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 88
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2608.06312v1
parent_observation_id: null
last_seen_at: 2026-08-08T00:00:00Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.06312v1](http://arxiv.org/abs/2608.06312v1)
- **发布域名**: arxiv.org
- **分类**: cs.CL
- **作者**: Tao Wang、Qihao Yang、Rongjiao Liang 等

## 来源摘要/节选

> Large language models (LLMs) increasingly support complex professional tasks, yet their capabilities in rule-intensive document review remain insufficiently evaluated. National standard documents, such as China GB/T standards, offer a representative testbed: they are lengthy, highly structured, and governed by explicit rules for scope, terminology, normative wording, and cross-section consistency. Existing benchmarks focus on domain knowledge and question answering, largely overlooking intrinsic quality review for professional documents. Such reviews rely heavily on human experts, making them costly and difficult to scale. To bridge this gap, we introduce GB/T-Bench, the first benchmark for the structured review of national standard documents. Its GB/T Review Taxonomy is a hierarchical schema covering document structure, scope alignment, normative modality, terminology consistency, and normative references, with 25 diagnosable error types. A controllable counterexample generation mechanism combines deterministic rules and constrained LLM rewriting to process 488 documents into 7,306 traceable review error instances for evaluation. We also develop a diagnosis-oriented evaluation protocol requiring exact matches on error location, review dimension, and error type, plus document-level coverage metrics. We further propose GB/T-Reviewer, a multi-agent framework that converts review knowledge into specialized skills and coordinates global inspection, targeted diagnosis, rule scanning, and result verification. Experiments with 14 mainstream LLMs reveal a substantial human-LLM gap: the strongest model achieves only 0.3280 CMCS versus 0.6640 for experts. GB/T-Reviewer raises the best CMCS to 0.5094, showing the value of structured skill coordination for rule-intensive document review. This work paves the way for trustworthy AI in standardization and other high-stakes document domains.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。