---
title: 'KNIGHT: Knowledge Graph-Driven Multiple-Choice Question Generation with Adaptive
  Hardness Calibration'
date: 2026-02-24 23:13:49+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
- RAG
- 大语言模型
categories:
- 论文
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
- RAG应用
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.20135v1
aliases:
- /posts/20260225-arxiv_ai-knight-knowledge-graph-driven-multiple-choice-ques-7/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:97ed661b8414f409bcaa0c1fa70eba829f18b600b0c724e1d6f1ed668be6e8d2
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 101
captured_at: '2026-07-18T04:16:34.952314Z'
source_capture_sha256: sha256:8198b83d1f82b6fd70bf6e67fb133bc44dcac45770b222beb8eba28ccf937f3e
source_capture_chars_original: 1460
source_publication_excerpt_chars: 1460
observation_id: obs_f0fcd97368f2889742b7ba8cf79a37bcee0e7e3053850e0b208ec66c74590cb3
revision_id: rev_adb0e2dcabe03ec45347c347baedb55fc3eaaa8f00bd5511cf2273b5a01f1f35
event_id: evt_9b00ef8f9d5077c62b7a4a64b9157d2a2e9c6b3b70e0bb185463344304efa1fe
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.20135v1](<https://arxiv.org/abs/2602.20135v1>)
- **作者**: Mohammad Amanlou, Erfan Shafiee Moghaddam, Yasaman Amou Jafari, Mahdi Noori, Farhan Farsi, Behnam Bahrak
- **分类**: cs.CL
- **论文时间**: 2026-02-23T18:46:27Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.20135v1.pdf](<https://arxiv.org/pdf/2602.20135v1.pdf>)

## 来源摘要/节选

> With the rise of large language models \(LLMs\), they have become instrumental in applications such as Retrieval-Augmented Generation \(RAG\). Yet evaluating these systems remains bottlenecked by the time and cost of building specialized assessment datasets. We introduce KNIGHT, an LLM-based, knowledge-graph-driven framework for generating multiple-choice question \(MCQ\) datasets from external sources. KNIGHT constructs a topic-specific knowledge graph, a structured and parsimonious summary of entities and relations, that can be reused to generate instructor-controlled difficulty levels, including multi-hop questions, without repeatedly re-feeding the full source text. This knowledge graph acts as a compressed, reusable state, making question generation a cheap read over the graph. We instantiate KNIGHT on Wikipedia/Wikidata while keeping the framework domain- and ontology-agnostic. As a case study, KNIGHT produces six MCQ datasets in History, Biology, and Mathematics. We evaluate quality on five criteria: fluency, unambiguity \(single correct answer\), topic relevance, option uniqueness, and answerability given the provided sources \(as a proxy for hallucination\). Results show that KNIGHT enables token- and cost-efficient generation from a reusable graph representation, achieves high quality across these criteria, and yields model rankings aligned with MMLU-style benchmarks, while supporting topic-specific and difficulty-controlled evaluation.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
