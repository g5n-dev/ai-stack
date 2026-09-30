---
title: "Imagine3D-LLM: Teaching MLLMs to Imagine 3D Scenes Before Answering"
date: 2026-09-30T14:44:52+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "计算机视觉", "cs.CV", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:ed21d7e6c34d91ee078fc9e2e595249672167af59685cf021a4c7641808cace6"
source_payload_sha256: "sha256:127ccb71a956154443fd08361c5dc87f106c4a370a639d62d22e117f002ef6dd"
observation_id: obs_6537f883b6a1ef4c2f49b56022e85633f1f4e08a91cf8d5ceddac8fde81f843f
event_id: evt_9f653a86b93890d0a8c624bebb92bf181a5623a3d7020a88e7180660cdba6262
revision_id: rev_0042f78adeb2059746df87a3cd99e27b9cd86623c67124862e420e141552f7e4
source_published_at: 2026-09-29T17:59:52Z
first_seen_at: 2026-09-30T06:55:35Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 67
interpretation_sha256: "sha256:96433ef00f45022792eb76f35f0dd8b07294d5e72da27900f2e9ef046f81c389"
description: "该工作提出一种多模态大语言模型，通过在学习阶段为每张图像加入可学习的汇总标记，将其解码为紧凑的三维高斯喷洒形式，并以此三维表示作为答案的生成条件，从而提升模型在多视角场景下的空间推理能力。"
external_url: http://arxiv.org/abs/2609.38177v1
parent_observation_id: null
last_seen_at: 2026-09-30T06:42:38.809034Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.38177v1](http://arxiv.org/abs/2609.38177v1)
- **发布域名**: arxiv.org
- **分类**: cs.CV
- **作者**: Jaewoo Jung、Hyeonseo Yu、Honggyu An 等

## 要点解读

### 这是什么  
该工作提出一种多模态大语言模型，通过在学习阶段为每张图像加入可学习的汇总标记，将其解码为紧凑的三维高斯喷洒形式，并以此三维表示作为答案的生成条件，从而提升模型在多视角场景下的空间推理能力。

### 用在哪里  
适用于需要从多张视角图像推断整体三维布局的任务，如视觉问答、机器人环境感知或增强现实的场景理解；也可供研究跨视角特征一致性和多模态语言模型空间推理的学者参考。

### 可以推断的  
推测：在训练中让模型同时完成 token 预测和三维表征重建，可能促使其内部图像特征在帧间形成更强的对应关系。  
推测：如果该方法在更多基准上表现稳健，未来有望与现有的三维重建流程结合，为语言模型提供更直观的场景结构信息。

## 来源摘要/节选

> Reasoning about the 3D world from multi-view images remains a fundamental challenge for Multimodal Large Language Models (MLLMs). While modern MLLMs handle single-image inputs effectively, they struggle to integrate evidence across viewpoints into a coherent 3D understanding. A growing body of work attempts to close this gap by injecting 3D awareness into MLLMs, either by boosting fine-grained pixel-level cross-view correspondence or by fusing features from 3D geometry foundation models, yet a substantial gap to human reasoning persists. In this work, we revisit human spatial reasoning, which suggests that rather than relying on fine-grained geometry cues, humans roughly identify common objects across views, infer the relative geometry between viewpoints, and assemble a coarse 3D layout of the scene. Inspired by this process, we introduce Imagine3D-LLM, an MLLM that learns to assemble a similar compact 3D representation of the scene and conditions its answer on this representation. Concretely, we append a small set of learnable summary tokens after the image tokens, decode them into a compact 3D Gaussian Splatting representation supervised by a photometric reconstruction loss, and train jointly with the standard next-token prediction objective. Notably, although only the summary tokens receive direct reconstruction supervision, this objective also induces stronger cross-frame correspondence within the LLM's underlying image features, suggesting that learning to reconstruct propagates 3D-aware signals throughout the model. As a result, Imagine3D-LLM consistently outperforms prior approaches across multiple spatial reasoning and 3D understanding benchmarks, suggesting that imagining the scene can be more effective than being told its pixel-wise geometry.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。