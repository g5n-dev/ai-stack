---
title: "Teaching Nemotron Greek: Mining a Corpus, Adapting Retrieval, and Grounding Generation for Modern Greek across Specialist Domains"
date: 2026-08-06T20:21:11+08:00
draft: false
entry_kind: "auto"
tags: ["RAG", "eess.AS", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:319def87a9589262fb0b29a53bed3dd3fc6c736b74d0752a652ff8c807ac71db"
source_payload_sha256: "sha256:3fa7844cf1326e7ed78eed016b42a61bbe320b1c945d746d4584f65434edbe0c"
observation_id: obs_33a3e040cf98081787ebeb1761caf548aefc32dec83ce4ddbfd8666576bba2b2
event_id: evt_abac9ffc33a0dd3e8cc060b1f515475f91f5cf0b4c03c9b2275e873c8241c41d
revision_id: rev_e8c40348b330b0ccc0478bb706311e5a36f0c567f9aa49bd7788fe9667039535
source_published_at: 2026-08-05T17:56:40Z
first_seen_at: 2026-08-06T12:29:34Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 129
interpretation_sha256: "sha256:56e35df17b9c28c7ec911b1ff647cdeb491b9579ab56ad8fd96e3f840a428f2b"
description: "该研究针对现代希腊语在检索增强生成（RAG）系统中的缺失，提出了一套从语料库挖掘、合成监督、检索模型训练、重排微调到阅读模型调优的完整适配方案，并发布了相应的评估基准。"
external_url: http://arxiv.org/abs/2608.05138v1
parent_observation_id: null
last_seen_at: 2026-08-07T00:00:00Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.05138v1](http://arxiv.org/abs/2608.05138v1)
- **发布域名**: arxiv.org
- **分类**: eess.AS
- **作者**: Ayoub Kirouane、Christos Petrocheilos

## 要点解读

### 这是什么
该研究针对现代希腊语在检索增强生成（RAG）系统中的缺失，提出了一套从语料库挖掘、合成监督、检索模型训练、重排微调到阅读模型调优的完整适配方案，并发布了相应的评估基准。

### 用在哪里
适用于需要在法律、能源、金融、医疗等专业领域处理希腊语文档的检索系统开发者，以及对多语言检索模型进行适配的研究人员。

### 可以推断的
推测：在其他资源稀缺的语言中，类似的语料库挖掘与合成监督流程可能有助于提升检索性能。  
推测：完整的检索与阅读模型微调在实际部署时可能需要较大的计算资源。

## 来源摘要/节选

> Modern Greek is absent from NVIDIA's Nemotron retrieval models and from major multilingual retrieval benchmarks, despite being important for retrieval-augmented generation (RAG) in legal, energy, financial, and medical applications. We present an end-to-end adaptation of the Nemotron retrieval stack for Modern Greek, including corpus mining, synthetic supervision, retrieval model training, reranker adaptation, reader fine-tuning, and a new benchmark called HERA. Our study shows that a parameter-free BM25 baseline outperforms several off-the-shelf multilingual dense retrieval models on specialist Greek corpora. After fine-tuning on 65,773 Greek retrieval pairs, a Nemotron 1B embedder improves nDCG@10 from 0.362 to 0.835 and substantially outperforms its unadapted counterpart. The learned language competence transfers to general-domain Greek, although the advantage over BM25 remains domain-dependent. We further adapt a cross-encoder reranker and demonstrate consistent improvements across specialist domains. Finally, we LoRA-tune a Nemotron 30B-A3B mixture-of-experts reader for grounded generation, increasing judged answer correctness from 29.4% to 66.9% while significantly improving faithfulness and citation quality. We also introduce HERA, the first large-scale Greek benchmark for retrieval-augmented generation, and release our adapted models and benchmark to support future research on Greek-language RAG systems.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。