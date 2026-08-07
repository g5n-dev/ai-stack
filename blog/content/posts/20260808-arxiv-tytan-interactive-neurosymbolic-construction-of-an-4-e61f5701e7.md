---
title: "Tytan: Interactive Neurosymbolic Construction of Analytic Semantic Schemas from Relational Data"
date: 2026-08-08T02:04:47+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "cs.DB", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:8a4389ae6dcd460dedaab8bb31c93bde106b955cd0c49aad1f76cec92e4bb671"
source_payload_sha256: "sha256:aee071742ae11bbf5c8dbb56b434bc2b0ec3ef213e21809bed7d1b44f1611bf8"
observation_id: obs_e61f5701e74d34f01b8ebdeeacf6f076ffdfb0f8ee4d21a34d78b3a9a7abfbe8
event_id: evt_caa4f7327eb1a196f87144061035bc7b5b1657dddb1c7133ca249eea9d442c11
revision_id: rev_f4bf5a8c047ab41a26ad35bbd6e320e7db9a0c1e60e6c176e4e50cd4412aa6f9
source_published_at: 2026-08-06T17:40:26Z
first_seen_at: 2026-08-07T18:02:11.331496Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 95
interpretation_sha256: "sha256:1d6ba4fbd8850726ea79e019067c931db426faefb86786fac2a5379c7cb29084"
description: "TYTAN是一种自动从关系数据库构建分析型语义模式的系统，结合数据库的符号分析和基于LLM的语义推断，并在信息不足以确定时向用户提出自然语言问题以明确角色和命名。"
external_url: http://arxiv.org/abs/2608.06331v1
parent_observation_id: null
last_seen_at: 2026-08-07T18:02:11.331496Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.06331v1](http://arxiv.org/abs/2608.06331v1)
- **发布域名**: arxiv.org
- **分类**: cs.DB
- **作者**: Donna Hooshmand、Shubham Shahi、Cameron Barrie 等

## 要点解读

### 这是什么
TYTAN是一种自动从关系数据库构建分析型语义模式的系统，结合数据库的符号分析和基于LLM的语义推断，并在信息不足以确定时向用户提出自然语言问题以明确角色和命名。

### 用在哪里
适用于需要快速为数据添加语义层、支持自然语言查询或自动报表生成的分析平台，帮助非技术用户降低对专家手工编写模式的依赖。

### 可以推断的
推测：该系统在实际使用中可能需要处理多种结构的关系库，并且对表的主键、聚合特征等有一定识别能力。  
推测：当用户提供的描述信息有限时，系统可能更依赖交互式提问来补充语义推断的不足。

## 来源摘要/节选

> From natural-language query interfaces to automated report generation, data analysis tools need a description of the data: the real-world entities it contains, which columns function as measures or identifiers, and how tables connect into units of analysis. Today, this semantic layer is usually written by hand. This is a knowledge-acquisition bottleneck that limits the scalability of analytic systems, keeps non-technical users dependent on experts, and is itself error-prone. We present TYTAN, a system for automatically constructing an analytic semantic schema from a relational database and, when available, a short user-provided description. TYTAN combines symbolic analysis of the database with LLM-based semantic inference for entity proposal, role assignment, and naming. When the evidence leaves a decision ambiguous, TYTAN asks the user a targeted natural-language question. We evaluate TYTAN on eight databases spanning real-world and benchmark domains along the three axes that define a schema's functional utility: (i) coverage, are all important entities and features captured?; (ii) retrieval correctness, do the schema's instructions actually reach the data; and (iii) characterization accuracy, are semantic types correct? Across the seven reference domains, TYTAN reaches every entity, attribute, and aggregable feature of the expert-corrected reference schemas (100% coverage). Additionally, 100% of its retrieval instructions execute correctly (1,678 of 1,678 self-generated claims), and semantic roles agree with the reference on 92-100% of matched attributes. Checking the underlying data showed the small disagreement is in the reference, not in TYTAN. On a held-out blind test (a live, ten-table database with no declared keys), TYTAN recovers the full entity structure with verified keys and satisfies 100% of the satisfiable expectations of five independent blind annotators.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。