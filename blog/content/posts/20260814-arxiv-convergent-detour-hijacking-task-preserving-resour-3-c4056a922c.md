---
title: "Convergent Detour Hijacking: Task-Preserving Resource Amplification in Skill-Based LLM Agents"
date: 2026-08-14T03:22:33+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "cs.CR", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:3f984a3c003e1dde6370ed6c271fc5d2aa89bca7fab16004daa18ece3a5a4f4b"
source_payload_sha256: "sha256:2c348434f9f4690cc8262902d5d0219bcd43e3fddc706234353a30df639eca51"
observation_id: obs_c4056a922c5f9cee58e2570eb6ad171a6d7a09f35192a435d2e04ba25b734bd8
event_id: evt_54f9d48fbf046c72e4086e5c2cff1e7a44e682250e5c234b210719e4ded7e8e9
revision_id: rev_7479619df486b0a3afc596775eb6e0b0cec1c315af5a802b880f122fe907ddfd
source_published_at: 2026-08-12T17:12:49Z
first_seen_at: 2026-08-13T19:32:16Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 93
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2608.12273v1
parent_observation_id: null
last_seen_at: 2026-08-13T19:19:22.457706Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.12273v1](http://arxiv.org/abs/2608.12273v1)
- **发布域名**: arxiv.org
- **分类**: cs.CR
- **作者**: Junliang Liu、Ruoyu Li、Wenxin Tang 等

## 来源摘要/节选

> LLM agents increasingly rely on third-party skills, using natural-language descriptions for selection and instruction bodies for planning. This progressive-disclosure design exposes two sequential control points to untrusted publishers: a static skill may steer an otherwise correct task onto an unnecessarily costly trajectory. Prior work studies selection manipulation, malicious skill instructions, and tool-chain resource amplification largely separately, leaving their end-to-end composition unclear. We introduce Convergent Detour Hijacking (CDH), a text-only, runtime-independent attack that couples these stages. Under shared semantic cover, a description establishes relevance during selection, while an aligned body reuses that rationale to fabricate plausible dependencies during planning. CDH attracts an attacker-controlled coordinator alongside legitimate skills, recruits unnecessary benign skills into a bounded detour, and then re-enters the original route to preserve task completion. We evaluate it across multiple LLM backends and 491 held-out tasks under single-task and multi-turn conditions. On DeepSeek-V4-Pro, the matched coordinator is selected in 80.02% of tasks; among coordinator-hit runs that complete tasks, token consumption and end-to-end execution time increase by 66.91% and 92.45%, respectively, while aggregate task completion remains comparable. Thus, correct outcomes do not guarantee trajectory integrity or cost safety.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。