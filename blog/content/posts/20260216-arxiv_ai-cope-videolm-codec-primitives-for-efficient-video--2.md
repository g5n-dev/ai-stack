---
title: 'CoPE-VideoLM: Codec Primitives For Efficient Video Language Models'
date: 2026-02-16 23:54:05+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.13191v1
aliases:
- /posts/20260217-arxiv_ai-cope-videolm-codec-primitives-for-efficient-video--2/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:083d2f462a494bdb58f82fbc216feab0e91757eb2e6ded6192e4eca45addb487
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 66
captured_at: '2026-07-18T04:15:26.440768Z'
source_capture_sha256: sha256:a32159780b9276e8d60a2d1afd1fff38294b5bf6315cb0931784134ead9e3400
source_capture_chars_original: 1276
source_publication_excerpt_chars: 1276
observation_id: obs_0cd49d99ae81fa4ed393b9f30539ca97ee9820699e20d9b0d3eb73cdade16fff
revision_id: rev_6a9a6e04d5dfab04f34a0374cedc3938abaf10681e3370f6043537b6ea3c22a2
event_id: evt_d122dfe77a45f624ddfeb24a032f49c01c09f4bd46be6ccf576a37e970393977
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-16T03:51:58Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.13191v1](<https://arxiv.org/abs/2602.13191v1>)
- **作者**: Sayan Deb Sarkar, Rémi Pautrat, Ondrej Miksik, Marc Pollefeys, Iro Armeni, Mahdi Rad, Mihai Dusmanu
- **分类**: cs.CV
- **论文时间**: 2026-02-13T18:57:31Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.13191v1.pdf](<https://arxiv.org/pdf/2602.13191v1.pdf>)

## 来源摘要/节选

> Video Language Models \(VideoLMs\) empower AI systems to understand temporal dynamics in videos. To fit to the maximum context window constraint, current methods use keyframe sampling which can miss both macro-level events and micro-level details due to the sparse temporal coverage. Furthermore, processing full images and their tokens for each frame incurs substantial computational overhead. To address these limitations, we propose to leverage video codec primitives \(specifically motion vectors and residuals\) which natively encode video redundancy and sparsity without requiring expensive full-image encoding for most frames. To this end, we introduce lightweight transformer-based encoders that aggregate codec primitives and align their representations with image encoder embeddings through a pre-training strategy that accelerates convergence during end-to-end fine-tuning. Our approach reduces the time-to-first-token by up to $86\\%$ and token usage by up to $93\\%$ compared to standard VideoLMs. Moreover, by varying the keyframe and codec primitive densities we are able to maintain or exceed performance on $14$ diverse video understanding benchmarks spanning general question answering, temporal reasoning, long-form understanding, and spatial scene understanding.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
