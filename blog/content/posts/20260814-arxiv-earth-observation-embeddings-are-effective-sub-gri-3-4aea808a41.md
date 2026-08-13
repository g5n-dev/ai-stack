---
title: "Earth observation embeddings are effective sub-grid descriptors for probabilistic weather downscaling"
date: 2026-08-14T05:05:58+08:00
draft: false
entry_kind: "auto"
tags: ["AI", "cs.LG", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:4517a0b4a262fb8774a15037fec53ca771b35ba6c174d2bcf587ca64c860f17d"
source_payload_sha256: "sha256:9e65838af18d2de6e1d30b4320dd8c562d19609e496cdb4b4274727dc1174f24"
observation_id: obs_4aea808a41606dbeecca6bd500e14d81c87a870ced4c674238cd5738dc13b5f3
event_id: evt_d33898123fe4b93e38877594b24cf22c924facc1bf1bc3eaac9651d845667812
revision_id: rev_3ced9f7809d5fe49509d449e613505109ba5fcb71498d4c3f828816198a0ca7f
source_published_at: 2026-08-12T17:10:42Z
first_seen_at: 2026-08-13T21:02:36.899281Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 101
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2608.12271v1
parent_observation_id: null
last_seen_at: 2026-08-13T21:02:36.899281Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.12271v1](http://arxiv.org/abs/2608.12271v1)
- **发布域名**: arxiv.org
- **分类**: cs.LG
- **作者**: Pedro Sousa、Will Tebbutt、Sadiq Jaffer 等

## 来源摘要/节选

> Global weather reanalyses and forecasts resolve the evolving atmospheric state on coarse grids, but site-specific applications require predictions at arbitrary locations where near-surface conditions also depend on unresolved terrain and land-surface properties. Existing probabilistic downscalers address this gap using hand-crafted topographic descriptors. We ask instead whether Earth observation foundation models can provide transferable sub-grid surface representations for probabilistic weather downscaling.
> We augment a convolutional conditional neural process that downscales coarse ERA5 reanalysis fields at ~25 km resolution with a learned local surface descriptor, obtained by compressing a patch of TESSERA embeddings at 10 m resolution. Although these embeddings summarise surface conditions over annual timescales, they improve downscaling of instantaneous 2 m temperature and 10 m wind speed by encoding persistent surface properties that capture a location's departure from the coarse-grid atmospheric state. Across five climatically diverse regions, the embedding improves point and probabilistic skill at stations held out in both space and time, overall improving CRPS skill by 11.5% for 2 m temperature and 6.2% for 10 m wind speed. We further analyse how its contribution differs by variable, finding that topography explains more of temperature's sub-grid structure, while TESSERA provides additional surface information for wind speed.
> These improvements persist when the coarse input is changed from ERA5 to forecasts from the Aurora AI forecasting model, and when predicting at newly deployed stations with no regional history. To our knowledge, this is the first evidence that long-timescale Earth-observation embeddings can support short-timescale weather downscaling where sub-grid departures are systematically structured by persistent surface properties.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。