---
title: "Reflection-aware Generative Novel View Synthesis"
date: 2026-09-09T05:53:53+08:00
draft: false
entry_kind: "auto"
tags: ["生成式 AI", "计算机视觉", "cs.CV", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:4b0348b782005aefc042cad66b9bc484c288004fc4c1bed319c3eca305277ce9"
source_payload_sha256: "sha256:1c1fd0d284d770bee4cf7b89809cf1cd52916368af6483912fb371e3dc4574ca"
observation_id: obs_32d3a0d7cd23c3de900ae1dab7714e9dacf6b7d2c28d1df9fd82716f52db269d
event_id: evt_9edf6a65c4cd9fe76a5b2ad0c783e88fc82bfe621939c9eff7e756f9b626a128
revision_id: rev_2ff3b8c09232dfc2af81da9a1056e88638728cf5bc31e955afbe71713b8288c7
source_published_at: 2026-09-04T17:33:45Z
first_seen_at: 2026-09-08T22:04:05Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 48
interpretation_sha256: "sha256:56e32293e8b9ca85fa044bea8564cf46baa5be9f46da48ad4b9c5fd539eea3c4"
description: "该方法是一种无需额外训练的生成式新视角合成技术，专门用于包含镜面的场景。它把镜中像视作两幅互补视角，估计镜面并映射相机位姿形成虚拟视角，随后通过两个阶段的生成步骤——镜门控注意力和反射注入——在多视角扩散模型中显式利用反射关系，实现反射一致且场景连贯的新视角。"
external_url: http://arxiv.org/abs/2609.05382v1
parent_observation_id: null
last_seen_at: 2026-09-09T00:00:00Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.05382v1](http://arxiv.org/abs/2609.05382v1)
- **发布域名**: arxiv.org
- **分类**: cs.CV
- **作者**: GeonU Kim、Shin Dong-Yeon、Tae-Hyun Oh

## 要点解读

### 这是什么
该方法是一种无需额外训练的生成式新视角合成技术，专门用于包含镜面的场景。它把镜中像视作两幅互补视角，估计镜面并映射相机位姿形成虚拟视角，随后通过两个阶段的生成步骤——镜门控注意力和反射注入——在多视角扩散模型中显式利用反射关系，实现反射一致且场景连贯的新视角。

### 用在哪里
适用于需要在真实或合成场景中通过镜面获取隐藏结构的应用，例如室内建模、虚拟现实内容生成或增强现实中的场景补全。研究者或开发者若使用多视角扩散模型进行场景重建，而现有模型对镜面处理不足，可考虑采用该方法进行改进。

### 可以推断的
推测：该方法在需要保持反射细节的高质量渲染时，可能比未考虑镜面的方案更具优势。  
推测：由于不依赖额外微调，它在资源受限或快速原型开发环境中更容易部署。

## 来源摘要/节选

> We propose Ref-GeNVS, a training-free, reflection-aware method for generative novel view synthesis (NVS) in mirror scenes. Existing multi-view diffusion models often fail to recognize the mirror in the scene and cannot exploit reflected content for scene generation. To fix this issue without additional training, our key idea is to treat a mirror image as two complementary views. From input images, we estimate the mirror plane and reflect camera poses to form virtual views. Based on this virtual view setup, we propose a two-stage generation method consisting of Mirror-gated attention and Reflection injection, which enables reflection-consistent NVS by explicitly leveraging reflection relationships in a multi-view diffusion model. Ref-GeNVS inherits the strong generalizability of the multi-view diffusion backbone, while it does not require finetuning. On synthetic and real scenes including mirrors, Ref-GeNVS outperforms recent generative NVS methods by generating reflection-consistent and contextually coherent novel views, revealing scene structure visible only through mirrors. Project page: https://kim-geonu.github.io/Ref-GeNVS/

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。