---
title: "KGCaRe: Explainable Complex Conditional Question Answering using Automatic Knowledge Graph Construction and Context Retrieval with LLMs"
date: 2026-08-11T10:30:11+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "RAG", "Prompt 工程", "cs.CL", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:22e239eef7cc3fb9e985dba396066fac441fe612aca65341114c2fef80688ac6"
source_payload_sha256: "sha256:a7c478a4aa8fb240e013f115689a9fbaeb51f797759379dc354224833b3b5530"
observation_id: obs_3bacb09b1e0b9b22a9cd860fc47aea3c46e6e58b1e8cf382270c037db1707269
event_id: evt_859a924a3dd3aa57c1fee5bbf98c995fb05a6d9566b30259515d2ca40f4cba81
revision_id: rev_d4ccbd80866e30f223f07fa6237ab9d700de270e3a2b6db88785d84f073d6b01
source_published_at: 2026-08-10T16:05:58Z
first_seen_at: 2026-08-11T02:27:23.258651Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 135
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2608.09779v1
parent_observation_id: null
last_seen_at: 2026-08-11T02:27:23.258651Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.09779v1](http://arxiv.org/abs/2608.09779v1)
- **发布域名**: arxiv.org
- **分类**: cs.CL
- **作者**: Ghanshyam Verma、Simanta Sarkar、Devishree Pillai 等

## 来源摘要/节选

> Answering complex conditional questions using Large Language Models (LLMs) and Retrieval-Augmented Generation (RAG) remains a challenge, particularly in domain-specific contexts where general-purpose LLMs and RAG tend to underperform. We hypothesize that augmenting RAG with unstructured and structured knowledge, extracted from both documents and knowledge graphs (KGs), can improve reasoning and answer accuracy for such tasks.
> To test this, we propose KGCaRe, a hybrid approach that combines neural retrieval with symbolic reasoning over LLM-generated KGs. KGCaRe constructs a KG from documents using a multi-prompt extraction strategy and stores it in a graph database. Simultaneously, the documents are embedded into a vector store to enable neural retrieval. KGCaRe performs innovative iterative graph traversal guided by the LLM to extract relevant triples, prune irrelevant information, and uses additional clue entities to traverse the graph again if the initial traversal does not provide satisfactory context to generate the answer. The relevant triples extracted from the KG in path form, along with semantically retrieved text passages, are then fed into custom KGCaRe prompts to generate answers to the complex conditional questions with explanations.
> We evaluate KGCaRe on two complex conditional QA datasets. Our results on these datasets show that KGCaRe consistently outperforms existing baselines, including Vanilla LLM, Code Prompt, Text Prompt, Think-on-Graph, Vanilla RAG, and HybridContextQA, across multiple LLMs such as Mistral, Mixtral, GPT-3.5, and GPT-4o. We publicly release the software pipeline that we developed to implement the proposed KGCaRe approach.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。