---
title: "Constructing Dynamic Master Logic Models as Knowledge Graphs for Complex System Diagnostics Using Retrieval-Augmented Large Language Models"
date: 2026-08-13T14:47:22+08:00
draft: false
entry_kind: "auto"
tags: ["AI", "cs.AI", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:c2bf8cc70299157450613b34464b704c6f7fc1dc6168fe9b61b7ac43de24b9b9"
source_payload_sha256: "sha256:a486f6c51bc7995fa988f20dad48fbcee3e4af9fdf5e8668324fec1c57fcc62c"
observation_id: obs_31ac698c56e20b53a57364f4c84ab6909013b48df116aca01d9a1842de7ac3dd
event_id: evt_ef56f5f52d0e62e0bbbe9dad67285ec09a7c9e9c2ba463132b733ecb493f2824
revision_id: rev_672f8490c522ec6e142e2efa5c25bea21f29aa37a524a00d0d1de525c429143f
source_published_at: 2026-08-12T17:50:39Z
first_seen_at: 2026-08-13T06:56:27Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 139
interpretation_sha256: "sha256:2c320f02dbae9665524be138cd5f2bcd71d7b91027b28a8392af99584f60b65c"
description: "本研究提出利用检索增强生成和大语言模型，将系统描述自动构建为以知识图谱呈现的动态主逻辑模型，以支持复杂系统的诊断与可靠性分析。"
external_url: http://arxiv.org/abs/2608.12304v1
parent_observation_id: null
last_seen_at: 2026-08-13T06:45:03.684470Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.12304v1](http://arxiv.org/abs/2608.12304v1)
- **发布域名**: arxiv.org
- **分类**: cs.AI
- **作者**: Saman Marandi、Yu-Shu Hu、Mohammad Modarres

## 要点解读

### 这是什么  
本研究提出利用检索增强生成和大语言模型，将系统描述自动构建为以知识图谱呈现的动态主逻辑模型，以支持复杂系统的诊断与可靠性分析。  

### 用在哪里  
适用于需要在大量技术文档中快速提取功能依赖、进行故障诊断和安全评估的工程团队或研究者，尤其在核电站等复杂装置的可靠性分析中有潜在价值。  

### 可以推断的  
推测：自动化构建能够降低对专家解读的依赖，从而缩短大型系统模型的开发周期。  
推测：通过显式保留功能依赖和逻辑关系，知识图谱可以在故障传播路径分析中帮助识别潜在的级联风险。

## 来源摘要/节选

> Dynamic Master Logic (DML) provides a hierarchical framework for representing system behavior by linking functional objectives to underlying structural elements. However, DML construction typically relies on expert interpretation of technical documentation, limiting scalability for complex systems. This study presents a framework for automated construction of DML models from system descriptions and their representation as Knowledge Graphs (KG-DML), using Retrieval-Augmented Generation and Large Language Models as enabling tools. Building on prior work with small-scale systems, the framework extends automated KG-DML construction and evaluation to substantially larger and more complex systems. Model construction proceeds across the DML hierarchy using targeted retrieval while preserving functional dependencies and explicit logical relationships. The resulting KG-DML supports diagnostic reasoning, safety assessment, upward failure propagation, and downward dependency tracing. A multi-level validation methodology evaluates layer-specific precision and recall, logical gate consistency, and overall structural integrity. Application to the Low-Pressure Coolant Injection system of a decommissioned Boiling Water Reactor demonstrates consistent reconstruction across repeated runs. The results show that automated KG-DML construction can transform technical documentation into executable functional models for diagnostic and reliability analysis.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。