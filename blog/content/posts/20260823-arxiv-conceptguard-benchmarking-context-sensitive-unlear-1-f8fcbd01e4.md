---
title: "ConceptGuard: Benchmarking Context-Sensitive Unlearning in Large Language Models"
date: 2026-08-23T16:51:07+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "cs.CL", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:0b3b76516c23aa294ca57ca014f5fbeec0acfd15f63302061a74addf030c1c57"
source_payload_sha256: "sha256:15c340717657d159247e5081c50d8de915198d1414e9ed9f953f7d34d9bf851e"
observation_id: obs_f8fcbd01e4613e069a34623d41a4e7dfc5ec1c276c78d220d5a4eaaf440d129c
event_id: evt_c2a2603aa24b4789372e1b347b8a59cd395dab43b58df6110b8f40db6852fc4d
revision_id: rev_5a44a6c4a6ce653d41897f8e0c9bc565cddb332f8a8cbbf91605721b92ddbecb
source_published_at: 2026-08-20T17:59:57Z
first_seen_at: 2026-08-23T08:48:19.606856Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 80
interpretation_sha256: "sha256:bac53a0fd418c83e9a2e27c18541f919c71ecaf17a210b5437cc8a5ea832613a"
description: "ConceptGuard 通过构建概念层面的忘‑记互补集合，对大语言模型的上下文敏感去学习能力进行评估。"
external_url: http://arxiv.org/abs/2608.20338v1
parent_observation_id: null
last_seen_at: 2026-08-23T08:48:19.606856Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.20338v1](http://arxiv.org/abs/2608.20338v1)
- **发布域名**: arxiv.org
- **分类**: cs.CL
- **作者**: Sahil Kale、Ian Harris

## 要点解读

### 这是什么
ConceptGuard 通过构建概念层面的忘‑记互补集合，对大语言模型的上下文敏感去学习能力进行评估。

### 用在哪里
适用于研发去学习方法的研究者，以及需要在实际部署中验证模型能否在保留有用知识的同时抑制有害使用的安全工程师。

### 可以推断的
推测：该基准需要系统地准备涵盖有害和良性情境的概念级测试样本。  
推测：现有去学习技术在实现高度上下文分离方面可能仍有不足，需进一步提升对双用途概念的控制能力。

## 来源摘要/节选

> Large Language Models (LLMs) increasingly require selective removal of harmful or sensitive knowledge, called unlearning, yet existing methods and benchmarks fail to evaluate this capability completely. Current approaches rely on disjoint forget and retain sets composed of independent facts, and measure success using simple and direct factual recall. This framing fails to capture a key requirement of unlearning, namely the ability to eliminate harmful behaviors while preserving benign and beneficial knowledge. We argue that effective unlearning must operate at the level of concepts, ensuring complete removal of unsafe applications while maintaining their correct and useful usage, thereby achieving conceptually meaningful and complete unlearning. To better evaluate unlearning techniques from such a practical viewpoint, we introduce the notion of dual-use concepts: concepts that can be used in both harmful and benign contexts. Building on these concepts, we construct a benchmark called ConceptGuard where forget and retain sets are explicitly complementary in concept usage. Our benchmark uniquely enables unlearning to be explored and gauged at the level of concepts, instead of sparse facts, and evaluation is intent-sensitive with the goal of maximizing contextual separation to promote safer behavior. We demonstrate that current unlearning techniques perform poorly under this setting, showing weak contextual separation alongside poor performance in ROUGE and concept-level metrics. Our results reveal strong forgetting-utility trade-offs, limited gains in contextual sensitivity, and poor consistency in concept-level control across methods, and provide ideas for unlearning approaches that better align with real-world safety requirements. Our dataset is publicly available.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。