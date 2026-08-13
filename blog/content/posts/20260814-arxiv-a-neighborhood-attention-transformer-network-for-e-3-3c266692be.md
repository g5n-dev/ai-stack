---
title: "A Neighborhood Attention Transformer Network for Enhanced 3D Segmentation of the Left Anterior Descending Artery"
date: 2026-08-14T01:14:39+08:00
draft: false
entry_kind: "auto"
tags: ["计算机视觉", "cs.CV", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:4985349e83e1449915c94aace2d4cd757e72a7ef218b24cb4a05dd875ca756ff"
source_payload_sha256: "sha256:7c9b6916320531c61c62ae781b861353164b9f24c79864973f39f99c6e42b11b"
observation_id: obs_3c266692beb948b42a8bca267cd9c3b950422e3243a5581e9888c15622f19405
event_id: evt_1bb2227c59ae33b4f4f5080eba814378353af214047679ac7c2eede6b63ffe05
revision_id: rev_d15da2cecfba1f8aec500b2a8e072c4a918fda0411c42d36095ce6f5e4098318
source_published_at: 2026-08-12T17:13:59Z
first_seen_at: 2026-08-13T17:12:00.785124Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 112
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2608.12274v1
parent_observation_id: null
last_seen_at: 2026-08-13T17:12:00.785124Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.12274v1](http://arxiv.org/abs/2608.12274v1)
- **发布域名**: arxiv.org
- **分类**: cs.CV
- **作者**: Rafi Ibn Sultan、Chengyin Li、Yiannos Demetriou 等

## 来源摘要/节选

> Background: Accurate segmentation of the Left Anterior Descending (LAD) artery in 3D free-breathing, non-contrast CT is critical for cardiac dose sparing in thoracic radiotherapy. The LAD is extremely small, has poor soft-tissue contrast, and varies substantially across patients; even manual contours show limited inter-observer agreement, underscoring the ambiguity of the vessel boundaries. Purpose: To develop a transformer-based framework that improves LAD delineation in low-contrast, imbalanced CT through local-global context modeling and uncertainty-guided optimization. Methods: We propose NA-UNETR, a 3D transformer-based segmentation model whose Neighborhood Attention (NA) and Dilated NA (DiNA) blocks jointly capture fine structural detail and long-range context. Given the scarcity of annotated LAD data, the model is pretrained on 1,000 CTA volumes of general coronary anatomy and fine-tuned with LoRA-based parameter-efficient adaptation on 20 free-breathing institutional CT scans. A composite Dice-Focal and Hausdorff loss, dynamically balanced via homoscedastic uncertainty, improves overlap and boundary accuracy. Results: NA-UNETR reached 45.64% Dice, 38.16 mm HD95, and 10.01 mm ASD, improving Dice by 3.10 percentage points over nnU-Net and reducing HD95 by 2.96 mm relative to Swin UNETR, with the strongest boundary accuracy among all models and improved centerline stability. On ImageCAS it achieved 79.49% Dice, 8.89 mm HD95, and 1.02 mm ASD. Ablations confirmed that residual blocks, variable kernels, and uncertainty-weighted loss each contributed. Conclusions: NA-UNETR balances local precision and global context for thin, low-contrast LAD structures, offering a computationally efficient framework for substructure-level cardiac segmentation in radiotherapy planning.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。