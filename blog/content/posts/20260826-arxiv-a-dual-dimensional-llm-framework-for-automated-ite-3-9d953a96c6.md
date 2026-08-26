---
title: "A Dual-Dimensional LLM Framework for Automated Item Incidental Content Similarity Analysis in Large-Scale Assessments"
date: 2026-08-26T19:47:03+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "cs.AI", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:304fa7ab8992a97f607f6b9444140b26c8346aabc08e86690929c93b05469513"
source_payload_sha256: "sha256:ae0b0e80aad8dfa7f1c91a564c9a8a225ff94e064a07601880c9de60dbb418a6"
observation_id: obs_9d953a96c693237e0bb29d569fb102b046cf99993f9b6a978209e8a1134cc2ad
event_id: evt_f71a3ffd1e5d454666018a9030fad1b38e41f272a7fe18ee27af1d6e5f4a5a0c
revision_id: rev_c195bd8b5859e6b96741f72dcaf38150fd2706baa1342eb43b693280960ebc64
source_published_at: 2026-08-25T17:07:16Z
first_seen_at: 2026-08-26T11:44:32.749052Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 117
interpretation_sha256: "sha256:cb9ee58aa2078418ae940bbb6af2a6cfbc6ea738e65eb81250a8b85910d25890"
description: "这是一项研究，提出基于大型语言模型的双维度框架，用于自动评估测试项目中因表述或情境而产生的附带内容相似度，旨在解决传统文本相似度指标难以捕捉细微结构和语义冗余的问题。"
external_url: http://arxiv.org/abs/2608.24825v1
parent_observation_id: null
last_seen_at: 2026-08-26T11:44:32.749052Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.24825v1](http://arxiv.org/abs/2608.24825v1)
- **发布域名**: arxiv.org
- **分类**: cs.AI
- **作者**: Jing Huang、Jihong Zhang、Hua-Hua Chang

## 要点解读

### 这是什么
这是一项研究，提出基于大型语言模型的双维度框架，用于自动评估测试项目中因表述或情境而产生的附带内容相似度，旨在解决传统文本相似度指标难以捕捉细微结构和语义冗余的问题。

### 用在哪里
适用于大型题库管理、测评机构的项目审查以及计算机自适应测试系统中的题目挑选和防重复策略，尤其在需要保证测评公平性和测量精度的场景中具有实际价值。

### 可以推断的
推测：该框架在实际应用时可能需要针对不同学科或语言特点进行适配，以确保结构化分解的准确性。  
推测：在自适应测试中加入相似度约束时，需要在题目多样性跟测量效率之间做出权衡，以免出现效率显著下降的情况。

## 来源摘要/节选

> The rapid expansion of large-scale assessments and the growing adoption of automatic item generation have intensified concerns about incidental content redundancy, where construct-irrelevant elements such as wording or contextual framing become unintentionally repetitive across items. Traditional similarity metrics like BLEU or cosine similarity, often fail to capture the nuanced structural and semantic layers that drive perceived redundancy simultaneously. This study proposes a dual-dimensional framework for Automated Item Similarity Analysis (AISA) powered by Large Language Models (LLMs), operationalizing similarity through Structured Decomposition and Semantic Relatedness. Psychometric validation indicates that LLM-derived metrics align more closely with indicators of construct-irrelevant local dependence and yield more coherent item parameter groupings than traditional text-based measures. The framework is further evaluated through its application in Computerized Adaptive Testing (CAT). Simulations reveal that incorporating LLM-based similarity constraints into item selection improves estimation stability and reduces bias with minimal efficiency trade-offs, outperforming constraints based on conventional metrics. These findings highlight the potential of LLM-powered AISA to support scalable bank curation, content-aware test assembly, and experience-sensitive adaptive testing across diverse assessment contexts.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。