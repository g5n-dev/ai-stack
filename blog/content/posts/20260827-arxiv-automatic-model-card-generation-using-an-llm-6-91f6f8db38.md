---
title: "Automatic Model Card Generation Using an LLM"
date: 2026-08-27T07:34:36+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "机器学习", "cs.SE", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:7332f7851cdb9654dd35b64081de0cdc508d65ba1044d9a5b1bfe5ce6c965804"
source_payload_sha256: "sha256:b16abef69b6eb49d403e5b7fbd35fa660222a54e8a7b7b8197182330cd5cd7dc"
observation_id: obs_91f6f8db38e5377e6b68d916237d2746a4a35b6c5687647b4a3b1078a26cad70
event_id: evt_d7bd73635aee553485a2b16bf086dd76b4fb9ace8112dc92613906b6110507f4
revision_id: rev_85f4f5fd449fee6d6f85005bdc2dbd33f1e51b76c83401683b624dd29f79db85
source_published_at: 2026-08-25T16:49:37Z
first_seen_at: 2026-08-26T23:31:44.228567Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 44
interpretation_sha256: "sha256:4645704c9c63681e83ef9073a18a26b7d18a5eaae5368d38fdd6f0462f880429"
description: "该研究提出两种基于语言模型的方案：一种将已有的模型卡片重新组织为统一模板，另一种直接从模型仓库数据生成新的模型卡片，旨在提升模型文档的结构一致性和可获取性。"
external_url: http://arxiv.org/abs/2608.24807v1
parent_observation_id: null
last_seen_at: 2026-08-26T23:31:44.228567Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.24807v1](http://arxiv.org/abs/2608.24807v1)
- **发布域名**: arxiv.org
- **分类**: cs.SE
- **作者**: Tajkia Rahman Toma、Balreet Grewal、Cor-Paul Bezemer

## 要点解读

### 这是什么  
该研究提出两种基于语言模型的方案：一种将已有的模型卡片重新组织为统一模板，另一种直接从模型仓库数据生成新的模型卡片，旨在提升模型文档的结构一致性和可获取性。

### 用在哪里  
适用于需要批量管理或快速生成模型文档的团队、平台或开发者，尤其在模型数量庞大、手动撰写卡片成本高的情况下可发挥作用。

### 可以推断的  
- 推测：当模型仓库中包含较为完整的技术说明或关联论文时，自动生成的质量会更佳。  
- 推测：该技术有潜力集成到模型托管服务中，实现自动化的文档流水线，从而降低人工维护文档的成本。

## 来源摘要/节选

> Model cards are structured documents that summarize key information about machine learning models to improve transparency, usability, and accountability. However, they often lack a consistent structure, and many models provide no model cards, making comparison and interpretation difficult. This paper presents two contributions. First, we propose MCTidy, an LLM-based approach that reorganizes existing model cards into a standardized template to improve clarity and comparability. Second, we introduce MCGenie, an LLM-based system that generates model cards directly from model repository data. We apply MCTidy to 48 Hugging Face model cards and evaluate information retention, section alignment, hallucination, and stability. Our findings show high information retention with minimal textual loss, accurate section assignment, rare hallucinations primarily in descriptive sections, and strong stability across runs. We assess MCGenie by generating model cards for the same 48 models and assessing semantic similarity, factual correctness, and sensitivity to input resources. The generated model cards achieved high semantic similarity (mean around 0.9); over half were fully correct, and most remaining errors were minor. Generation quality depended strongly on the availability of supporting resources, particularly associated papers. Overall, our findings demonstrate the potential of LLM-based methods to enable scalable, standardized model card documentation.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。