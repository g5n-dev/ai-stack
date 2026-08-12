---
title: "MultiModal Code-Switching: Interleaving Visual Objects into Language for Explicit Object-Level Alignment"
date: 2026-08-13T01:14:51+08:00
draft: false
entry_kind: "auto"
tags: ["计算机视觉", "cs.CV", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:dfb4d1d359c0cdea84bc789e56bfdc38b42c153fa8d9fa15458195024f7e0e4e"
source_payload_sha256: "sha256:6e53f60bd13264825135c9c3b6cc598e66d35930c9a62eb3555d782918cf1411"
observation_id: obs_ed0e54d5dd1c5f65874e06766234368f4087620552a3fdad7c58b47d7b238ecf
event_id: evt_73e02d859952ca60bdb48a2ef83fb383a721214d5a4941ced053684254e2d567
revision_id: rev_23a7375b870f7dd2c477246ca15fdcda7152afbc6d49719a71077df14a30b63b
source_published_at: 2026-08-11T17:28:52Z
first_seen_at: 2026-08-12T17:11:57.824739Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 104
interpretation_sha256: "sha256:ea01e91738ea0d3a68c7fad7362fe99eb284ac281c7a560843b4311e81818ef7"
description: "本文提出一种新的预训练范式——多模态代码切换（MMCS），通过在文本中直接嵌入对应的视觉对象来实现细粒度的对象级对齐，从而改善模型对视觉与语言之间对应关系的感知。"
external_url: http://arxiv.org/abs/2608.11167v1
parent_observation_id: null
last_seen_at: 2026-08-12T17:11:57.824739Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.11167v1](http://arxiv.org/abs/2608.11167v1)
- **发布域名**: arxiv.org
- **分类**: cs.CV
- **作者**: Changhao Xiang、Shangyu Xing、Zhen Wu 等

## 要点解读

### 这是什么
本文提出一种新的预训练范式——多模态代码切换（MMCS），通过在文本中直接嵌入对应的视觉对象来实现细粒度的对象级对齐，从而改善模型对视觉与语言之间对应关系的感知。

### 用在哪里
适用于需要精准定位视觉对象的多模态任务，如视觉问答、图像描述、目标检测等。研究人员和开发者可利用该方法提升模型在细粒度视觉理解上的表现。

### 可以推断的
- 推测：由于采用对象级的显式监督，模型在需要将语言描述映射到具体视觉区域的任务中可能表现更好。  
- 推测：该方法有望降低对大规模人工标注的依赖，尤其在资源受限的环境中更具吸引力。

## 来源摘要/节选

> Existing Multimodal Large Language Models (MLLMs) predominantly rely on image-text pairs for modality alignment pretraining, mapping global image representations to long textual descriptions. However, this image-level alignment suffers from referential ambiguity: models struggle to infer the correspondences between multiple visual objects and textual entities from the global representation, leading to data inefficiency and suboptimal semantic grounding. To address this, we propose MultiModal Code-Switching (MMCS), a novel pretraining paradigm that provides explicit object-level supervision. Inspired by the linguistic phenomenon of code-switching, MMCS interleaves vision and language by replacing textual entities with their corresponding visual objects, enforcing local vision-language grounding. We further develop a scalable data synthesis pipeline to generate a pretraining dataset of 773K samples with accurate object-entity correspondences. Experiments show that MMCS is highly data-efficient: with only 50K samples, it matches or surpasses models trained on 600K image-text pairs. Furthermore, MMCS consistently improves visual grounding and perception capabilities across varying model scales.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。