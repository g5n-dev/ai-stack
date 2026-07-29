---
title: "CHARM: A Multimodal Graph Foundation Model with Hierarchical Context Modeling for Zero-Shot Transfer"
date: 2026-07-30T06:16:28+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "cs.AI", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:b956f37d335722eabe35b760120779ed882791708e78c179bdede3d688c06200"
source_payload_sha256: "sha256:8a7267cd5afc897e121e21e52df7c7a360293e4c450890c642fa95fd343437de"
observation_id: obs_1f6bfb8771e601287d2dcaed404d234ab535fc4d5f696335ce5de9faad3c9c4b
event_id: evt_fef27d1237edb0939766fae7b487cad5423f0e2df21b5de09a5bd9d0323915ec
revision_id: rev_36182db6c2a94be5f3a3fcc96ba61037623d726589bd9411d9b7f5eaf26ad2f9
source_published_at: 2026-07-28T17:35:26Z
first_seen_at: 2026-07-29T22:38:52Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 100
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2607.26023v1
parent_observation_id: null
last_seen_at: 2026-07-29T22:15:36.455418Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2607.26023v1](http://arxiv.org/abs/2607.26023v1)

## 来源摘要/节选

> Graph foundation models (GFMs) have emerged as a promising paradigm for transferring knowledge across graph domains and tasks. Real-world graphs associate nodes with text, images, and other modalities, making multimodal graphs essential for representing complex entities and relations. Moreover, collecting labels and adapting models for every new graph domain is costly and often infeasible, motivating zero-shot transfer. Unfortunately, zero-shot transfer on multimodal graphs remains underexplored. Existing GNN-based graph foundation models typically require downstream adaptation, whereas LLM-based graph methods mainly address unimodal graphs or tasks within a single domain. This setting presents two key challenges. First, models must generalize knowledge from individual modalities while capturing transferable cross-modal relations. Second, without target-domain fine-tuning, node representations remain entangled with domain-specific structures and modality-specific characteristics, obscuring shared concepts in unseen domains. To address these challenges, we propose CHARM, a multimodal graph foundation model with hierarchical context modeling for zero-shot transfer. CHARM replaces isolated raw nodes with hierarchical graph contexts that capture multimodal semantics and cross-modal relations. These contexts map domain-specific node patterns to shared high-level concepts, reducing reliance on target-domain supervision or adaptation. A modality-aware graph context encoder integrates multimodal information with graph structure and converts the resulting representations into graph tokens for a large language model . Experiments show consistent improvements on zero-shot multimodal graph tasks.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。