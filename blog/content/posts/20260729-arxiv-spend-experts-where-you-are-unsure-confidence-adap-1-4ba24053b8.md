---
title: "Spend Experts Where You Are Unsure: Confidence-Adaptive Routing for Mixture-of-Experts LoRA"
date: 2026-07-29T17:53:19+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "cs.LG", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:d274b9087b7b798dd8a35d1436d75854b2227526cca863c01100728e1b5a7e06"
source_payload_sha256: "sha256:836d7fd682cb16b2580fde607b3b38c88a09c1db489a4066c739a788c8b07f47"
observation_id: obs_4ba24053b8572ab4990901970c4fa9b3feb4976ee82a93838a4df00e51119b84
event_id: evt_c132f3398fd95999b7bb51b465f85af8f1841c6e767f0de3df3db21bfa228ed9
revision_id: rev_3fb46f6077ebe1953ae45d45531b8bf8c66413085f8f97eb2f6a73647ac8a5dd
source_published_at: 2026-07-28T17:59:16Z
first_seen_at: 2026-07-29T10:10:08Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 91
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2607.26052v1
parent_observation_id: null
last_seen_at: 2026-07-29T09:52:02.112168Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2607.26052v1](http://arxiv.org/abs/2607.26052v1)

## 来源摘要/节选

> Mixture-of-Experts (MoE) variants of Low-Rank Adaptation (LoRA) route every token to a fixed number of experts $k$. Tokens differ in how uncertain the model is about them, so a single k over-spends on easy tokens and under-serves hard ones. We observe that the router's output distribution is already a per-token uncertainty signal: peaked mass indicates confidence, while a flat distribution indicates ambiguity. We introduce CARE (Confidence-Adaptive Routing of Experts), which admits experts in a nucleus fashion. Experts are activated in decreasing router weight until their cumulative mass reaches a threshold, with a small extension when the admitted experts disagree. A budget thermostat calibrates the threshold so that the average number of active experts matches any target. CARE is a drop-in, single-forward-pass rule with no extra parameters. Across eight commonsense benchmarks on LLaMA-3.1-8B and Qwen2.5-7B, as well as math, code, and knowledge tasks, CARE improves over fixed top-k MoE-LoRA at matched compute and matches the fixed-k=4 baseline while activating fewer experts. The same confidence and disagreement signals also improve out-of-distribution detection over MSP, entropy, and multi-pass proxies. We support the design with nucleus fidelity, budget optimality, and an epistemic reading of disagreement, and we release code.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。