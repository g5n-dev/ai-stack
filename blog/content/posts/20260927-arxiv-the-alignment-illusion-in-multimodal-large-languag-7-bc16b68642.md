---
title: "The Alignment Illusion in Multimodal Large Language Models"
date: 2026-09-27T16:11:58+08:00
draft: false
entry_kind: "auto"
tags: ["计算机视觉", "cs.CV", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:b21494c0a1f4f314acca1fdc9adc195f861d2476cf0e96af51a411fd6f6b197a"
source_payload_sha256: "sha256:01b51fe059c86f87232fd58c915e7356d29dad56d3191d862b4f0710e7533ef9"
observation_id: obs_bc16b686428a679f371d5f5ddf3ac4153a7e187114e084dcbca07762423301e4
event_id: evt_bd0f70cc0ae60fd024fea1c85d733e97eeded1c08fd3a5ca1da8743a440d33f4
revision_id: rev_b0ac7033eaa1ec1b1bf4aef249bcd3d92ab5231eb32148bcbd7ff9198d58432d
source_published_at: 2026-09-24T17:42:29Z
first_seen_at: 2026-09-27T08:23:13Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 58
interpretation_sha256: "sha256:56c87141562ab278f4ce55da305088110285c090543702ccb06f089ff4e1a746"
description: "该研究通过在视觉流中加入噪声来检验常见的层间视觉‑文本对齐指标是否真正反映跨模态内容交互，发现四种标准标量度量在噪声干扰下仍难以区分原始与受损表示，并将此现象称为对齐幻觉。"
external_url: http://arxiv.org/abs/2609.30210v1
parent_observation_id: null
last_seen_at: 2026-09-27T08:08:40.563014Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.30210v1](http://arxiv.org/abs/2609.30210v1)
- **发布域名**: arxiv.org
- **分类**: cs.CV
- **作者**: Hong-Han Wang、Yuntao Wang、Hu Ding

## 要点解读

### 这是什么
该研究通过在视觉流中加入噪声来检验常见的层间视觉‑文本对齐指标是否真正反映跨模态内容交互，发现四种标准标量度量在噪声干扰下仍难以区分原始与受损表示，并将此现象称为对齐幻觉。

### 用在哪里
适用于评估多模态语言模型内部视觉表征独立性以及在设计或调试对齐度量时判断相似度是否具备实际任务意义的研究者和工程师。

### 可以推断的
推测：在缺乏额外约束的情况下，仅凭标量对齐分数可能高估模型对视觉信息的真实利用程度。  
推测：若视觉流的内部几何结构与任务表现出现背离，模型可能更依赖语言路径的先验而非视觉特征。

## 来源摘要/节选

> Layer-wise visual-text similarity in Multimodal Large Language Models (MLLMs) is widely interpreted as evidence that the language model progressively integrates visual content into a shared representation space. This reading rests on the assumption that scalar alignment scores reflect content-level cross-modal interaction. To test this assumption, we apply controlled interventions to the visual stream. Across 13 MLLMs from five families spanning 0.5B to 72B parameters, replacing projector-output visual tokens with Gaussian noise sharply reduces task accuracy, yet four standard scalar measures (CKA, SVCCA, MIR, and the leading principal-angle cosine) fail to consistently separate the corrupted stream from the original. We call this failure the alignment illusion and trace it to the shared language-model pathway: anisotropic MLP down-projections pull visual and text tokens toward common output directions, producing weight-induced alignment. Because this component is essentially one-dimensional, we introduce the principal-angle gap (PA gap), defined as the difference between the top two principal-angle cosines, which separates weight-induced similarity from multi-directional visual structure. Under graded visual corruption, the PA gap tracks task accuracy more consistently than the scalar scores we consider; under a structured but irrelevant image, it further exposes regimes in which internal geometry and task accuracy come apart. Internal visual-text alignment in MLLMs is therefore best read as a geometric diagnostic of the visual stream inside the language model rather than a direct proxy for content-level cross-modal interaction, and is most informative when calibrated by controlled task evidence.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。