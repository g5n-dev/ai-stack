---
title: "Desktop-Delta Bench: Do Computer-Use Models Understand Desktop GUI Transitions?"
date: 2026-07-29T23:33:58+08:00
draft: false
entry_kind: "auto"
tags: ["AI Agent", "cs.AI", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:99aa955e5c51904a3c656a6610e9e8c8bb2e22ba5cd0021b9b7d79a964e04cf1"
source_payload_sha256: "sha256:352c892a52692301e14125e126a52508feb39ef7cd034d7cb0c48a27fb54b8ac"
observation_id: obs_17ff776a83fbbcc21e3a554e4bb7cc0e87fe860b17efd3cd3e13caa9b17941b5
event_id: evt_bfc09705d117513f1a3aa7f3a19db4e6d1e18dc6f0b3a4a3ef3a2eb1409148bf
revision_id: rev_9163f646d442d5a68a621bed6eee95625ef94746694161f0935775fd36db4e28
source_published_at: 2026-07-28T17:49:51Z
first_seen_at: 2026-07-29T15:33:00.969009Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 79
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2607.26041v1
parent_observation_id: null
last_seen_at: 2026-07-29T15:33:00.969009Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2607.26041v1](http://arxiv.org/abs/2607.26041v1)

## 来源摘要/节选

> Computer-use agents (CUAs) increasingly act through desktop GUIs to complete long-horizon tasks. Current benchmarks primarily measure end-task success or single-frame grounding. Neither isolates whether a model can reconstruct the causal, task-relevant transition produced by an action- crucial for rejecting stale observations, verifying progress, and recovering from failure. This is difficult because inference, remote input, app rendering, and screenshot capture are asynchronous: the next observation may be delayed, occluded, transient, or unrelated, then misread as progress and carried into subsequent planning. We introduce Desktop-Delta Bench (DDB), an offline step-level benchmark with 2,013 human-verified instances from novel, multi-app Linux trajectories across ~15 applications and 50 task domains. DDB trajectories targets 3 failure dimensions- state verification, source tracking, and context-aware control- through 2 complementary tasks: 463 3-frame temporal-ordering instances, including 105 with a cross-trajectory decoy, and 1,550 before-after pairs labeled from 5 actions + its payload. We evaluate 8 closed and open-source model families across 32 ordering and 16 single-action settings, observing consistent gaps. Ordering remains unsaturated: best non-decoy and decoy exact-match rates are 65.1% and 65.7%. Task context improves decoy identification by 6.9 percentage points but reduces non-decoy exact match by 2.2 points; error analysis reveals systematic copying of the presented A-B-C order. Single-action results show that inferring the action family is harder than locating it: click F1 is 0.96 vs, 0.76 for drag, while recognized drags are generally localized well. DDB, thus, complements end-to-end benchmarks by filling the missing diagnostic layer between GUI grounding and final task success, enabling targeted improvements to desktop CUA verification, reliability, and recovery.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。