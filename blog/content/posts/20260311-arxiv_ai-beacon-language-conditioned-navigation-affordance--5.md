---
title: 'BEACON: Language-Conditioned Navigation Affordance Prediction under Occlusion'
date: 2026-03-11 22:41:14+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2603.09961v1
aliases:
- /posts/20260312-arxiv_ai-beacon-language-conditioned-navigation-affordance--5/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:05259e2ee249f84ec31e3d8379252508d679a68e0aa8342f84812a27cc2c2e03
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 77
captured_at: '2026-07-18T04:27:42.897478Z'
source_capture_sha256: sha256:3e4a76e33824e2d4b387983670e01f1039ab8675140c97cb1612d5587fe9699f
source_capture_chars_original: 1312
source_publication_excerpt_chars: 1312
observation_id: obs_7e03815ba515a1f8fb43ea54c514a59caef3721149d63830809725a774c1bcde
revision_id: rev_12cc1dfeed41a62e6e0c31c571b1cc96c2158d53ce20e4f5249fae89e9054689
event_id: evt_70a252381ffc2be4eed9bc13d42a9d420b460eebb39206293773a0cd1488a726
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-03-11T04:17:05Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.09961v1](<https://arxiv.org/abs/2603.09961v1>)
- **作者**: Xinyu Gao, Gang Chen, Javier Alonso-Mora
- **分类**: cs.RO
- **论文时间**: 2026-03-10T17:56:16Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.09961v1.pdf](<https://arxiv.org/pdf/2603.09961v1.pdf>)

## 来源摘要/节选

> Language-conditioned local navigation requires a robot to infer a nearby traversable target location from its current observation and an open-vocabulary, relational instruction. Existing vision-language spatial grounding methods usually rely on vision-language models \(VLMs\) to reason in image space, producing 2D predictions tied to visible pixels. As a result, they struggle to infer target locations in occluded regions, typically caused by furniture or moving humans. To address this issue, we propose BEACON, which predicts an ego-centric Bird's-Eye View \(BEV\) affordance heatmap over a bounded local region including occluded areas. Given an instruction and surround-view RGB-D observations from four directions around the robot, BEACON predicts the BEV heatmap by injecting spatial cues into a VLM and fusing the VLM's output with depth-derived BEV features. Using an occlusion-aware dataset built in the Habitat simulator, we conduct detailed experimental analysis to validate both our BEV space formulation and the design choices of each module. Our method improves the accuracy averaged across geodesic thresholds by 22.74 percentage points over the state-of-the-art image-space baseline on the validation subset with occluded target locations. Our project page is: https://xin-yu-gao.github.io/beacon.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
