---
title: "Cropland PAtteRNS: Parallel Dimensional Attention Networks and Attention to Dataset Disparity for Crop Segmentation in Satellite Imagery Time Series Data"
date: 2026-10-01T03:22:34+08:00
draft: false
entry_kind: "auto"
tags: ["计算机视觉", "cs.CV", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:5448ced8122b27f4ae33010d2136016a5636a0379f721dfa73d9a1b4ac8a274f"
source_payload_sha256: "sha256:6434b67ad149d5b178bb5745054369addff5b70ec728ab0d7056b464953a2a74"
observation_id: obs_1e7b8ed0db01330cc5dadf0752d5e8284a3956b7b08b8a5ce03a4db033271aa6
event_id: evt_5ea36429e49b0c80f2e6183e3f842b0caa59dd4252b2c14c0213eb749b3d84e9
revision_id: rev_3864f025536a2e5291f55e7ca09f4308dff0392248af8962bdb48442461ba7b6
source_published_at: 2026-09-29T17:59:29Z
first_seen_at: 2026-09-30T19:19:12.701519Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 153
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2609.38165v1
parent_observation_id: null
last_seen_at: 2026-09-30T19:19:12.701519Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.38165v1](http://arxiv.org/abs/2609.38165v1)
- **发布域名**: arxiv.org
- **分类**: cs.CV
- **作者**: Joseph Metcalfe、Sara Sharifzadeh、Fabio Caraffini

## 来源摘要/节选

> The landscape of satellite imagery time series datasets and boundary-pushing architectures for cropland segmentation has never been richer. However, in this gold rush, important truths are being missed on both fronts, as a drive for the most novel concepts or the largest datasets pushes finer details to the side. In this paper, we present our hybrid transformer-convolutional model, Cropland Parallel Attention and Refinement Network for Segmentation (PAtteRNS), the first model to use self-attention mechanisms separately for each of the temporal, spectral, and spatial aspects of Sentinel-2 multispectral SITS data. To achieve fully-factorised attention in our proposed model, we introduce a novel parallel transformer architecture which significantly reduces the computational complexity of triple-factorised self-attention. We validate our architecture with an in-depth ablation study, and analyse the performance of our model against state-of-the-art crop segmentation models on multiple tile-size variants of the popular PASTIS and MTLCC datasets. Our findings show our model to outperform all others in the task of crop class segmentation, verified across multiple important segmentation metrics, with especially strong performance against compared models seen in the often under-reported parcel delineation quality, for which we use the Boundary IoU metric. We also find that flawed class groupings within datasets can have a significant negative impact on model performance, and report that alternate tile-size variants of crop segmentation datasets produce results incomparable to one-another, invalidating fair comparison between model performance when trained on different tile-sizes. Based on these findings, we suggest further work is required to standardise best practices when constructing SITS crop segmentation datasets, and to enable future dynamic-tile-sizing for ideal model performance.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。