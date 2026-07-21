---
title: 'V2M-Zero: Zero-Pair Time-Aligned Video-to-Music Generation'
date: 2026-03-12 21:14:37+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2603.11042v1
aliases:
- /posts/20260313-arxiv_ai-v2m-zero-zero-pair-time-aligned-video-to-music-gen-3/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:d1f0d5a8ef70611763499d006d4a5e20bdff510f03034ef8f09721fd9db7d470
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 58
captured_at: '2026-07-18T04:28:03.257131Z'
source_capture_sha256: sha256:9837f4b9a69ef19700c42352af9b0b38d9e3d86c2203dfdfa06fe5253e336535
source_capture_chars_original: 1575
source_publication_excerpt_chars: 1575
observation_id: obs_f304b2f28854b019456aa71f23b0fe800c088c865cc524146269ab0a87688988
revision_id: rev_dae9d2cf8f94f52dd0c3f3efdb307b98a859a65f077218a7c0f920b92afd37af
event_id: evt_8e64c73798ca6e8bbe7f1d3cf5285ed9bec7f8f53966a7638671e0352184771a
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-03-12T04:13:20Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.11042v1](<https://arxiv.org/abs/2603.11042v1>)
- **作者**: Yan-Bo Lin, Jonah Casebeer, Long Mai, Aniruddha Mahapatra, Gedas Bertasius, Nicholas J. Bryan
- **分类**: cs.CV
- **论文时间**: 2026-03-11T17:59:40Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.11042v1.pdf](<https://arxiv.org/pdf/2603.11042v1.pdf>)

## 来源摘要/节选

> Generating music that temporally aligns with video events is challenging for existing text-to-music models, which lack fine-grained temporal control. We introduce V2M-Zero, a zero-pair video-to-music generation approach that outputs time-aligned music for video. Our method is motivated by a key observation: temporal synchronization requires matching when and how much change occurs, not what changes. While musical and visual events differ semantically, they exhibit shared temporal structure that can be captured independently within each modality. We capture this structure through event curves computed from intra-modal similarity using pretrained music and video encoders. By measuring temporal change within each modality independently, these curves provide comparable representations across modalities. This enables a simple training strategy: fine-tune a text-to-music model on music-event curves, then substitute video-event curves at inference without cross-modal training or paired data. Across OES-Pub, MovieGenBench-Music, and AIST++, V2M-Zero achieves substantial gains over paired-data baselines: 5-21% higher audio quality, 13-15% better semantic alignment, 21-52% improved temporal synchronization, and 28% higher beat alignment on dance videos. We find similar results via a large crowd-source subjective listening test. Overall, our results validate that temporal alignment through within-modality features, rather than paired cross-modal supervision, is effective for video-to-music generation. Results are available at https://genjib.github.io/v2m\_zero/

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
