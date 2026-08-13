---
title: "DreamFly: Causal Memory and Receding-Horizon Diffusion Planning for Aerial Vision-Language Navigation"
date: 2026-08-13T13:04:46+08:00
draft: false
entry_kind: "auto"
tags: ["AI Agent", "生成式 AI", "计算机视觉", "cs.CV", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:eadcd16fe63bab959cc19ccb3fa7b446248de326de3597cf9871926f5a345be7"
source_payload_sha256: "sha256:30765a29b95fca1df38661bcde3785c219b8c24c7ada1331e06806413f60eff7"
observation_id: obs_66cc1d289d60cd914b899897cd96a5af945ab357f32a30037f46fdc1e4abe8fe
event_id: evt_515fb603d1b83099bc52ad231418a7eef110a67b084f23d38dfd8bfc3b66db25
revision_id: rev_7132f58aa9f119456d4f5515ee66c3a19c3e46427feab662e006654fa9af7ff7
source_published_at: 2026-08-12T17:54:33Z
first_seen_at: 2026-08-13T17:12:00.783417Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 101
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2608.12308v1
parent_observation_id: null
last_seen_at: 2026-08-13T05:03:26.593223Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.12308v1](http://arxiv.org/abs/2608.12308v1)
- **发布域名**: arxiv.org
- **分类**: cs.CV
- **作者**: Yan Deng、Fei Xu

## 来源摘要/节选

> Aerial vision-language navigation (VLN) requires an embodied agent to integrate visual evidence over time, plan future actions, and determine when it has reached a navigation goal under partial observability. Although recent VLA models offer a promising perception-to-action paradigm, adapting them to aerial navigation remains challenging due to limited historical context, short planning horizons, and unreliable implicit termination. To address these challenges, we propose DreamFly, a diffusion-based aerial VLN framework built on Dream-VLA. DreamFly introduces a causally aligned historical memory that augments the current visual representation using only observations preceding the current decision step, enabling temporal reasoning without future information leakage. We further formulate navigation as receding-horizon diffusion planning, where the policy predicts a $K$-step action chunk but executes only the first action before replanning. This plan-$K$, execute-one strategy uses future actions as auxiliary planning targets while preserving closed-loop visual feedback. Finally, LiteStop estimates the stop probability directly from action logits at the initial all-mask state, decoupling explicit termination from action generation. Experiments on the OpenFly benchmark demonstrate consistent improvements in seen and unseen environments. DreamFly achieves 32.04%/29.46% SR and 28.22%/23.54% SPL on the test-seen/test-unseen splits, respectively, outperforming all compared methods on both metrics while attaining the lowest navigation error. These results demonstrate the effectiveness of jointly modeling historical context, future action structure, and explicit termination for aerial VLN.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。