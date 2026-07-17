---
title: "Online Neural Space Time Memory for Dynamic Novel View Synthesis"
date: 2026-07-17T23:42:15+08:00
draft: false
entry_kind: "auto"
tags: ["cs.CV", "arXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:c5713a12bcf244469ddc98e60b566de2404681dd89c39a8abf516d3e8b8a3ac9"
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 64
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2607.15271v1
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2607.15271v1](http://arxiv.org/abs/2607.15271v1)

## 来源摘要/节选

> Online novel view synthesis from multi-view streaming videos faces a fundamental trade-off: maintaining a persistent, long-horizon memory to reconstruct temporarily occluded regions while operating under strict real-time constraints. While Test-Time Training (TTT) offers a powerful memory mechanism, standard models mandate gradient-based memory updates at every frame to adapt to the changing motion in dynamic scenes. The computational cost of heavy memory updates precludes real-time application and can lead to instability over long contexts. Given that memory updates are more demanding than memory application and video content is largely redundant, we propose to decouple the frequencies of these two processes. Our approach performs periodic memory updates while applying the memory on a per-frame basis, using cross-view attention to manage deformations between the prior memory state and the current frame. To lock in the historical context, we introduce two critical mechanisms: an auxiliary Memory Loss that forces persistent internalization of the scene, and a Memory Caching strategy that regularizes active weights against catastrophic drift. Our method demonstrates real-time, state-of-the-art performance on scenes with dynamic human motion as well as minute-scale online memorization.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。