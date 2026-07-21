---
title: 'Tuning Just Enough: Lightweight Backdoor Attacks on Multi-Encoder Diffusion
  Models'
date: 2026-03-05 02:41:37+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2603.04064v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:e7c82e1b617966f8096226b4e7c36110bd41369bc7709e0ebd584fdd8127fe84
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 82
captured_at: '2026-07-18T04:27:08.846828Z'
source_capture_sha256: sha256:4eafdd27d551b751855082e622862d34d94c6a0a5b8093508c4b522db698503a
source_capture_chars_original: 1442
source_publication_excerpt_chars: 1442
observation_id: obs_ed6f0d22ade75886ea0a583f90bd614d002f27f8e06024e8df8917e0f0c9e6f3
revision_id: rev_655dbcdbc932354d4b591afe49fbf5499186dcc371a661ac48c69a956377548a
event_id: evt_6d148bb2f3da6f2bccd779fdf42e7cdbb8528765bd4d6c4613ade0b01d43e115
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-03-05T03:42:24Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.04064v1](<https://arxiv.org/abs/2603.04064v1>)
- **作者**: Ziyuan Chen, Yujin Jeong, Tobias Braun, Anna Rohrbach
- **分类**: cs.LG
- **论文时间**: 2026-03-04T13:41:20Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.04064v1.pdf](<https://arxiv.org/pdf/2603.04064v1.pdf>)

## 来源摘要/节选

> As text-to-image diffusion models become increasingly deployed in real-world applications, concerns about backdoor attacks have gained significant attention. Prior work on text-based backdoor attacks has largely focused on diffusion models conditioned on a single lightweight text encoder. However, more recent diffusion models that incorporate multiple large-scale text encoders remain underexplored in this context. Given the substantially increased number of trainable parameters introduced by multiple text encoders, an important question is whether backdoor attacks can remain both efficient and effective in such settings. In this work, we study Stable Diffusion 3, which uses three distinct text encoders and has not yet been systematically analyzed for text-encoder-based backdoor vulnerabilities. To understand the role of text encoders in backdoor attacks, we define four categories of attack targets and identify the minimal sets of encoders required to achieve effective performance for each attack objective. Based on this, we further propose Multi-Encoder Lightweight aTtacks \(MELT\), which trains only low-rank adapters while keeping the pretrained text encoder weight frozen. We demonstrate that tuning fewer than 0.2% of the total encoder parameters is sufficient for successful backdoor attacks on Stable Diffusion 3, revealing previously underexplored vulnerabilities in practical attack scenarios in multi-encoder settings.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
