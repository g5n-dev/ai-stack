---
title: 'Olaf-World: Orienting Latent Actions for Video World Modeling'
date: 2026-02-11 22:09:57+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.10104v1
aliases:
- /posts/20260212-arxiv_ai-olaf-world-orienting-latent-actions-for-video-worl-1/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:e2d6d08d00bded68cb90b347ed9a4e8b40e02be5f26ff1f94369f7360741447a
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 61
captured_at: '2026-07-18T04:14:39.893621Z'
source_capture_sha256: sha256:3f774729da1ef0ef7f3388b3316573e93177969a8f22bf9d918fe4e659e71216
source_capture_chars_original: 1138
source_publication_excerpt_chars: 1138
observation_id: obs_5d7fa716bc5be4e6ba23501193d02524b8d05667d83cbc6e8cea49855aaf205f
revision_id: rev_16896a17836ab003e2c205ee168d957d7ae779af928cede92d00ccf3045ba417
event_id: evt_c971f3b58e41ba019457a84c05e0cbcd41db0b872ce62457cd5bc68fdb383e0f
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-11T06:29:26Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.10104v1](<https://arxiv.org/abs/2602.10104v1>)
- **作者**: Yuxin Jiang, Yuchao Gu, Ivor W. Tsang, Mike Zheng Shou
- **分类**: cs.CV
- **论文时间**: 2026-02-10T18:58:41Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.10104v1.pdf](<https://arxiv.org/pdf/2602.10104v1.pdf>)

## 来源摘要/节选

> Scaling action-controllable world models is limited by the scarcity of action labels. While latent action learning promises to extract control interfaces from unlabeled video, learned latents often fail to transfer across contexts: they entangle scene-specific cues and lack a shared coordinate system. This occurs because standard objectives operate only within each clip, providing no mechanism to align action semantics across contexts. Our key insight is that although actions are unobserved, their semantic effects are observable and can serve as a shared reference. We introduce Seq$Δ$-REPA, a sequence-level control-effect alignment objective that anchors integrated latent action to temporal feature differences from a frozen, self-supervised video encoder. Building on this, we present Olaf-World, a pipeline that pretrains action-conditioned video world models from large-scale passive video. Extensive experiments demonstrate that our method learns a more structured latent action space, leading to stronger zero-shot action transfer and more data-efficient adaptation to new control interfaces than state-of-the-art baselines.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
