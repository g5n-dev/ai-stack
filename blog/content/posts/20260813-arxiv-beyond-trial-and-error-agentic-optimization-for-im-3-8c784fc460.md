---
title: "Beyond Trial-and-Error: Agentic Optimization for Image-to-Video Adherence"
date: 2026-08-13T18:23:55+08:00
draft: false
entry_kind: "auto"
tags: ["计算机视觉", "Prompt 工程", "cs.CV", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:d6d89c8b7dfbf78043389876b4c12c0baf0c3592ae4fb717a6b955cee3a53fd6"
source_payload_sha256: "sha256:321adf572d27fb5c9742857df1b55498b0ac3dba687ae4d1640f61162cf84ac0"
observation_id: obs_8c784fc460bd8a95c54bfa6488b8de829df3bbc40b55501f73178487e09a2c28
event_id: evt_f830a033d8e1034062afa03cd369b5289d08f4a832e2ce0ffda5b725768a47a4
revision_id: rev_289a8a210e3c9cb6906549cd53baf8b792e836e84b85714f0e14c1c114f11ac2
source_published_at: 2026-08-12T17:35:16Z
first_seen_at: 2026-08-13T10:21:44.489829Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 73
interpretation_sha256: "sha256:1991010b81d65dd753cde89b33025e6b48290ce8e317e9a35de3ceacac65fd2d"
description: "这是一种将文字驱动的视频生成过程转化为闭环优化的方法，先利用多模态大模型迭代改进输入提示，再通过贝叶斯搜索协同优化随机种子与生成尺度，并配合语义一致性与伪影检测的评价指标实现目标导向的产出。"
external_url: http://arxiv.org/abs/2608.12290v1
parent_observation_id: null
last_seen_at: 2026-08-13T10:21:44.489829Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.12290v1](http://arxiv.org/abs/2608.12290v1)
- **发布域名**: arxiv.org
- **分类**: cs.CV
- **作者**: Aman Tyagi、Hemanth Boinpally、Jonathan Chen 等

## 要点解读

### 这是什么
这是一种将文字驱动的视频生成过程转化为闭环优化的方法，先利用多模态大模型迭代改进输入提示，再通过贝叶斯搜索协同优化随机种子与生成尺度，并配合语义一致性与伪影检测的评价指标实现目标导向的产出。

### 用在哪里
适用于需要高可控性和可重复产出的内容创作团队，尤其是使用黑盒图像转视频模型的制作流程，帮助减少人工试错的成本。

### 可以推断的
- 推测：该方法在需要批量生成且对细节一致性要求严格的场景（如广告、产品展示）中具有显著价值。  
- 推测：框架的模块化设计可能使其能够适配其他类型的生成任务，如文本到图像或音频合成。

## 来源摘要/节选

> Modern black-box Image-to-Video (I2V) models offer powerful capabilities in automated content creation, yet their lack of fine-grained control and reliability presents significant challenges in professional workflows. Their inherent stochasticity causes minor variations in textual prompts or hyperparameters to yield drastically different outputs often necessitating inefficient, brute-force trial-and-error processes. To address these limitations, we introduce the ``Agentic Self-Improvement" framework, which reframes video synthesis into a closed-loop, goal-directed optimization. Our framework systematically navigates the generation parameter space using a novel two-stage approach. In the first stage, an iterative prompt optimization loop uses a multimodal Large Language Model (mLLM) to refine the input prompt. This refinement implements two automated evaluations: Davidsonian Scene Graph (DSG) queries ensure semantic adherence, and Common Mistake Questions (CMQ) for artifact detection. At the second stage, we use Bayesian optimization to efficiently co-optimize stochastic seeds and CFG scales. This search is guided by a suite of quality metrics, including the novel Video-Text Adherence (VTA) score derived from the DSG and CMQ evaluations. Our framework significantly outperforms unguided search methods: in human preference studies, videos generated via our agentic approach were strongly preferred over baseline outputs, achieving win rates up to 69\%. This work provides a practical and extensible methodology for enhancing the predictability and control of state-of-the-art video generation models, moving the field beyond speculative curiosities toward reliable, production-ready tools.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。