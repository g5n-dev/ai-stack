---
title: "UniMem: Complementary Episodic-to-Parametric Memory for Boundary-Agnostic Task Streams"
date: 2026-07-30T07:17:50+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "cs.CL", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:1309594a20ae6c5c90bb12a4cb95557b2e1fbd8f41e2a34f0bdc6c55fb57a14c"
source_payload_sha256: "sha256:fda623f326234d4c023be538e22192277b11c8b7fbbaf6934341a74dd455b68b"
observation_id: obs_891fc9aeca2690ca024ddc6dadd130804774156330db3a5383673272e631be05
event_id: evt_16b0eb59a7db5e6d4182cc3f8bf22f971e71f4923fa2b3da4f7e0551e0461f9c
revision_id: rev_e1e95e2367b94f589bdcb73a0e8da68bb66e494342071e584b8a2b664040c806
source_published_at: 2026-07-28T17:28:21Z
first_seen_at: 2026-07-29T23:16:54.043185Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 86
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2607.26017v1
parent_observation_id: null
last_seen_at: 2026-07-29T23:16:54.043185Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2607.26017v1](http://arxiv.org/abs/2607.26017v1)

## 来源摘要/节选

> Memory is essential for LLM agents to accumulate task experience and reuse task-specific execution strategies. However, real-world deployment over boundary-agnostic and evolving task streams exposes a fundamental stability-plasticity dilemma. External retrieval-based memory can rapidly absorb new evidence, but it often fails to internalize recurring execution patterns and incurs inference-time retrieval overhead. Parametric memory enables stable and efficient execution once learned, but typically relies on explicit task boundaries and fixed parameter budgets. Inspired by the human brain, which balances plasticity and stability through complementary episodic storage and gradual consolidation, we propose UniMem, a self-routing framework for autonomous memory management. UniMem uses learnable routing tokens as memory controllers, enabling adaptive coordination between complementary memory pathways: novel or sparse tasks are retained in an episodic buffer for retrieval-augmented execution, while recurring and reliable patterns are consolidated into expandable parametric memory. By decoupling task identification from task execution with routing tokens and parametric memory blocks, UniMem expands memory on demand without task labels during deployment or uncontrolled parameter growth. Experiments on long-horizon streaming task sequences show that UniMem consistently outperforms baselines while maintaining execution fidelity, achieving an average gain of 4.0 EM points across three backbone models.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。