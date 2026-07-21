---
title: 'SCOPE: Scene-Contextualized Incremental Few-Shot 3D Segmentation'
date: 2026-03-09 21:48:42+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2603.06572v1
aliases:
- /posts/20260310-arxiv_ai-scope-scene-contextualized-incremental-few-shot-3d-2/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:0858437efd13ca589b0dd32080c1fa402775c8c3b7acc5fb99019f4169ba4c28
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 64
captured_at: '2026-07-18T04:27:20.159062Z'
source_capture_sha256: sha256:96a9db8b2997514f083ffdea3627c4f9a7f1588ec5ba001f3e0f90af0de28338
source_capture_chars_original: 1252
source_publication_excerpt_chars: 1252
observation_id: obs_6fd24e45f712c49e1de878ed28ec07933ad445c1437d0fb718f7f6aa95e3cb6b
revision_id: rev_540b659828b5d72f3920ea84dd6014247f9c339eae324dd1dc5b3402acb3e6e8
event_id: evt_ceb479b9cc0e0bfd7b023db1fd31406a99b9a76d61a4e1dcf1edff850e88367f
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-03-09T06:26:14Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.06572v1](<https://arxiv.org/abs/2603.06572v1>)
- **作者**: Vishal Thengane, Zhaochong An, Tianjin Huang, Son Lam Phung, Abdesselam Bouzerdoum, Lu Yin, Na Zhao, Xiatian Zhu
- **分类**: cs.CV
- **论文时间**: 2026-03-06T18:59:36Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.06572v1.pdf](<https://arxiv.org/pdf/2603.06572v1.pdf>)

## 来源摘要/节选

> Incremental Few-Shot \(IFS\) segmentation aims to learn new categories over time from only a few annotations. Although widely studied in 2D, it remains underexplored for 3D point clouds. Existing methods suffer from catastrophic forgetting or fail to learn discriminative prototypes under sparse supervision, and often overlook a key cue: novel categories frequently appear as unlabelled background in base-training scenes. We introduce SCOPE \(Scene-COntextualised Prototype Enrichment\), a plug-and-play background-guided prototype enrichment framework that integrates with any prototype-based 3D segmentation method. After base training, a class-agnostic segmentation model extracts high-confidence pseudo-instances from background regions to build a prototype pool. When novel classes arrive with few labelled samples, relevant background prototypes are retrieved and fused with few-shot prototypes to form enriched representations without retraining the backbone or adding parameters. Experiments on ScanNet and S3DIS show that SCOPE achieves SOTA performance, improving novel-class IoU by up to 6.98% and 3.61%, and mean IoU by 2.25% and 1.70%, respectively, while maintaining low forgetting. Code is available https://github.com/Surrey-UP-Lab/SCOPE.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
