---
title: "Skill Self-Play: Pushing the Frontier of LLM Capability with Co-Evolving Skills"
date: 2026-07-28T03:07:34+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "cs.CL", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:12f1a9dae950c96554e67c27c3158692911b9f5b3edabcbae3868ced926d23b9"
source_payload_sha256: "sha256:9e39feebd0cb486dea0fab5f4672231c855747c893523e1df5b73eefc0d13277"
observation_id: obs_0f8bb094b1a337c9213094fbd560a44e9fbf5ffcf9d25c23cb4192f7b3e33903
event_id: evt_b38d5f9da3f253983d504fbafa4b16a30204db78d74978f7a9a77193c63d7237
revision_id: rev_d700e1218b84cbaf1e64f4e9404d5d486249881c24f3c6895eea40454ee7e5e5
source_published_at: 2026-07-24T17:59:22Z
first_seen_at: 2026-07-27T19:23:20Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 79
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2607.22529v1
parent_observation_id: null
last_seen_at: 2026-07-27T19:06:39.228405Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2607.22529v1](http://arxiv.org/abs/2607.22529v1)

## 来源摘要/节选

> LLM training is shifting from manual design and annotation to interaction-driven self-evolution. However, existing self-evolutionary methods face a fundamental dilemma between task diversity and verification reliability: environment-bound methods obtain precise feedback but confine learning to narrow domains, while open-ended self-generation broadens the task space but lacks reliable verification, allowing misleading rewards to pollute the training loop. We identify agent skills as a powerful middle ground to reconcile this tension: each skill ensures deep, verifiable execution in a specific scenario, while dynamic routing across skills maintains open-ended task variety. Leveraging this insight, we introduce Skill Self-Play (Skill-SP), a co-evolutionary framework comprising a proposer, a solver, and a dynamic skill controller. Orchestrated via a reinforcement learning loop, these components co-evolve in a continuous self-play loop: the proposer generates challenging tasks conditioned on dynamically sampled skills; the solver explores candidate solutions to push its capability boundaries; and the skill controller collects execution feedback to update and expand the skill library. This interactive co-evolution effectively bridges the gap between structured verification and open-ended exploration. Empirical evaluations on tool-use and reasoning benchmarks demonstrate that Skill-SP, serving as a robust evolution engine, consistently pushes the performance ceiling of competent backbones while catalyzing striking turnarounds for initially misaligned models. Our code is available at https://github.com/Qwen-Applications/skill-self-play.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。