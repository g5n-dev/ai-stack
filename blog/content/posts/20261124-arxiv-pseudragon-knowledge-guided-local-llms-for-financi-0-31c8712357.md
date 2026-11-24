---
title: "PseuDRAGON: Knowledge-Guided Local LLMs for Financial-Data Pseudonymization in Closed Networks"
date: 2026-11-24T14:01:40+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "cs.AI", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:d437eb382c71b97bb2a9dee9435cd0fe9e6f2b39af06837480c74a7af6b87c3e"
source_payload_sha256: "sha256:15d44537e440ca653c48947355391a15352a734f986446603cf6c7eb499de2b2"
observation_id: obs_31c8712357503aea746175d0f07151c2d3443821eee9f3ced99202b9e6a317de
event_id: evt_df3eeebeab20edb5a98db351b00c85b0ec6282d89ba82c625e5f2c16f8ba8a71
revision_id: rev_7f8ca30eee089d729f5659fd28b7f67423c6924f230c8b8f5ec40fbcab007a0f
source_published_at: 2026-11-23T09:24:48Z
first_seen_at: 2026-11-24T06:00:05.767968Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 94
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2611.30353v1
parent_observation_id: null
last_seen_at: 2026-11-24T06:00:05.767968Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2611.30353v1](http://arxiv.org/abs/2611.30353v1)
- **发布域名**: arxiv.org
- **分类**: cs.AI
- **作者**: Gwangui Hong、Seonho An、Seonkyu Lim 等

## 来源摘要/节选

> Staff pseudonymizing financial data in closed networks must interpret abbreviated column names, identify personal information, and choose processing methods. Local language models can assist, but may give different labels for the same input. PseuDRAGON keeps confirmed judgments and corrections outside a fixed model and reuses them through exact-name lookup and learned rules. For expert review, the workflow searches institutional policy, national privacy law, then international sources. Across 92 columns from one institution, rules increase reuse under the same approval checks from 75 to 83 labels without reuse errors when all training judgments are available. With 25% of the training judgments, withholding non-PII rules for unseen names eliminated the extra PII misses in replay at the cost of lower reuse. Revising or withdrawing approvals rebuilds derived rules, and tests on synthetic records verify that selected methods produce the specified outputs. In three paired runs, the history-first baseline cut automated identification time by 83.0% on average versus no reuse.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。