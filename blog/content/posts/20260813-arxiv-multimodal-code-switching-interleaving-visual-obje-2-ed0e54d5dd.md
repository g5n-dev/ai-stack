---
title: "MultiModal Code-Switching: Interleaving Visual Objects into Language for Explicit Object-Level Alignment"
date: 2026-08-13T02:09:30+08:00
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
first_seen_at: 2026-08-12T18:19:10Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 104
interpretation_sha256: "sha256:8e64477619d5e5e5d38104615e1c928ee3119d15b7c4ec58049aeb7281a08ace"
description: "提出一种多模态代码切换的预训练方法，通过把语言中的实体替换为对应的视觉对象，实现对象级别的显式监督，提升视觉‑语言局部对齐。"
external_url: http://arxiv.org/abs/2608.11167v1
parent_observation_id: null
last_seen_at: 2026-08-12T18:07:07.293801Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.11167v1](http://arxiv.org/abs/2608.11167v1)
- **发布域名**: arxiv.org
- **分类**: cs.CV
- **作者**: Changhao Xiang、Shangyu Xing、Zhen Wu 等

## 要点解读

### 这是什么  
提出一种多模态代码切换的预训练方法，通过把语言中的实体替换为对应的视觉对象，实现对象级别的显式监督，提升视觉‑语言局部对齐。

### 用在哪里  
适用于多模态大模型的预训练阶段，帮助模型在需要细粒度对象定位的任务（如指向表达、视觉问答）中更好地学习视觉‑语言对应关系。

### 可以推断的  
推测：该方法通过局部对应减轻全局表示的歧义，相同数据规模下可能获得更稳健的对象识别能力。  
推测：对象级别的监督有广泛适用性，从小型到大型的多模态网络均可受益，提升视觉定位和感知表现。

## 来源摘要/节选

> Existing Multimodal Large Language Models (MLLMs) predominantly rely on image-text pairs for modality alignment pretraining, mapping global image representations to long textual descriptions. However, this image-level alignment suffers from referential ambiguity: models struggle to infer the correspondences between multiple visual objects and textual entities from the global representation, leading to data inefficiency and suboptimal semantic grounding. To address this, we propose MultiModal Code-Switching (MMCS), a novel pretraining paradigm that provides explicit object-level supervision. Inspired by the linguistic phenomenon of code-switching, MMCS interleaves vision and language by replacing textual entities with their corresponding visual objects, enforcing local vision-language grounding. We further develop a scalable data synthesis pipeline to generate a pretraining dataset of 773K samples with accurate object-entity correspondences. Experiments show that MMCS is highly data-efficient: with only 50K samples, it matches or surpasses models trained on 600K image-text pairs. Furthermore, MMCS consistently improves visual grounding and perception capabilities across varying model scales.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。