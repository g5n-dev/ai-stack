---
title: "Energy-Structured Latent World Models with Neural Time Fields for Physically Constistent Open-World Motion Planning"
date: 2026-08-12T03:22:40+08:00
draft: false
entry_kind: "auto"
tags: ["AI", "cs.RO", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:b1e1ec7fabd186b9ead973305001a35f4fccf596b87315f653ec6d3d81130262"
source_payload_sha256: "sha256:f9c13f8f11f21eb69f3552f231e1946510c8ee10473dbab59756c51cdcb99830"
observation_id: obs_78bbdc6c6f93f80022ad37005726413b50d34043cf603373bbdcf5bcb0d48d68
event_id: evt_3ceb9ad02ec3560867a1b50d1a1c520854d55561240e922511fe1866ab9b0242
revision_id: rev_641dcd871d3fd49419544d2dc40822947425187a5229c097775c94134c74402c
source_published_at: 2026-08-10T17:31:18Z
first_seen_at: 2026-08-11T19:32:21Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 115
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2608.09876v1
parent_observation_id: null
last_seen_at: 2026-08-11T19:19:36.404747Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.09876v1](http://arxiv.org/abs/2608.09876v1)
- **发布域名**: arxiv.org
- **分类**: cs.RO
- **作者**: Yapeng Liu、Yuanzhao Zhai、Bo Ding 等

## 来源摘要/节选

> Physically consistent motion planning remains a fundamental challenge in embodied AI, as generated trajectories must strictly conform to real-world execution dynamics. While latent world models offer a promising approach by predicting these dynamics, existing methods learn unconstrained future representations where absorbed physics remains implicit. Therefore, they fail to form reusable physical knowledge, which compromises reliability in unpredictable open-world navigation. To address this, we propose a novel Energy-Structured Latent World Model (ELWM). Our key idea is to structure the ELWM latent state to explicitly carry energy and momentum, ensuring strictly causal transitions via dissipation and control ports. Trained on multimodal RGB-D and inertial interaction histories, our model guarantees physically consistent predictions. We further implement this for motion planning by constructing Physics-Conditioned Neural Time Fields (PC-NTF), a key technical cornerstone that integrates ELWM into an arrival time field via the Eikonal equation to yield a physically-informed navigation policy. Across held-out scenes, our evaluation reveals significant improvements. Compared to generic latent models, PC-NTF reduces 0.8-s motion-prediction NRMSE from 0.36 to 0.29. Against Active Neural Time Fields, it improves navigation success from 81.3% to 89.7% and SPL from 0.64 to 0.73, while cutting the physical collision rate from 12.1% to 5.8% and the Eikonal residual from 0.083 to 0.031. Beyond these targeted gains, our results demonstrate that embedding explicit physical structures into latent spaces intrinsically bridges the gap between predictive world models and safe, dynamically feasible motion planning.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。