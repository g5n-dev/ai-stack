---
title: "DSLE: A Learning Environment for Dark Souls Boss Encounters"
date: 2026-08-11T19:59:32+08:00
draft: false
entry_kind: "auto"
tags: ["AI Agent", "cs.AI", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:c714df40b053c913618b0a25bef244b9bc78ec174244ec542a7f98bc1926defc"
source_payload_sha256: "sha256:d140bbadf1bd62a050c88a0f01b07db83f79f7414743a303cfbf91200ab27731"
observation_id: obs_3a5d2e47a2b6f6fc00750424b0ef8c807e24294c67dc1fbdc03bc82731545345
event_id: evt_f765446c3d997a40a74bb37ea3ef9147d1580a989a39320e14cb5d9d647adb69
revision_id: rev_c72e6b47f92ad856b2be72b6be4078567ca9a278b8566f3f4fe00b806f0987f9
source_published_at: 2026-08-10T17:48:45Z
first_seen_at: 2026-08-11T11:56:28.545637Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 59
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2608.09902v1
parent_observation_id: null
last_seen_at: 2026-08-11T11:56:28.545637Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.09902v1](http://arxiv.org/abs/2608.09902v1)
- **发布域名**: arxiv.org
- **分类**: cs.AI
- **作者**: Derin Gezgin、Jim O'Connor、Tanner Goodwin 等

## 来源摘要/节选

> We introduce the Dark Souls Learning Environment (DSLE), a containerized platform that presents all 22 boss encounters of Dark Souls: Remastered as game-playing agent benchmarks through a Gymnasium-style interface. DSLE combines real-time combat, high-dimensional visual input, and sparse terminal rewards, with each environment step being a real action executed against the running game. To support controlled comparison, we define DSLE-5, a representative five-boss subset, spanning a melee fight, a spatially constrained arena, an environmental-hazard fight, a multi-target fight, and a fast final-boss fight, that we recommend as the starting suite for agents built on DSLE. On DSLE-5 we evaluate a random policy, an expert system, an evolutionary baseline, and PPO and DQN agents trained from visual input. The expert system and the evolutionary baseline each defeat the Asylum Demon, the game's tutorial boss (63% and 43% peak win rates), but none of the five methods defeats the other four DSLE-5 bosses; PPO and DQN show no measurable learning (at most 0.33% win rate on the tutorial boss, 0% elsewhere) within a budget that already costs tens of wall-clock hours per run. A broader study running the evolutionary baseline across all 22 encounters under advantaged all level-50 stats yields wins on only a handful of additional early-game bosses and leaves the rest unwon. The failure cases range from sub-10-second deaths in cramped, multi-target encounters to minute-long stalemates that inflict almost no damage, and we report them through survival time and damage dealt rather than win rate alone.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。