---
title: "IBIB: A Protocol for Measuring Enterprise AI Systems by Serving Route, Not Model Identifier"
date: 2026-09-11T02:31:08+08:00
draft: false
entry_kind: "auto"
tags: ["AI", "cs.CL", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:63c5bd02bdb34e75871e4badd1b600771f75169189048ceb389fd4c6ea76f0b2"
source_payload_sha256: "sha256:a8178ce84a944caf1b164a597f798bd295cbeab8e5bdecec78dce5723da3eecf"
observation_id: obs_65e171594791d971a728677b2d50e74b0bde3567e66df63826af68397447c85c
event_id: evt_4f55576aa517dfe9fd5de0341484671a86a002d5a32dea3fd3b89f07bfd01fae
revision_id: rev_84f0c60d47828d29b08a4f54c137d7c254a1ab322681fdc2fbe3c7c287076d56
source_published_at: 2026-09-09T17:31:29Z
first_seen_at: 2026-09-10T18:27:43.891499Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 91
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2609.10494v1
parent_observation_id: null
last_seen_at: 2026-09-10T18:27:43.891499Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.10494v1](http://arxiv.org/abs/2609.10494v1)
- **发布域名**: arxiv.org
- **分类**: cs.CL
- **作者**: Blake Stenstrom、Charangan Vasantharajan、Brian Sathianathan

## 来源摘要/节选

> Enterprises deploy systems, not checkpoints. Usable capability depends jointly on weights, serving route, precision, output contract, and harness, yet all 18 audited benchmarks score advertised model identifiers. We treat this as measurement error and give a protocol that makes it reportable. It has three parts. A gold-blind capability-binding preflight verifies that a route can execute the evaluation contract before any task reaches it; a reliability-inclusive first-pass scoring rule keeps failure in the score while keeping unsupported capability out; and adjudication is structurally score-blind. We call the protocol IB2 and release its algorithms, classification tables, request contract, and manifest schemas. Its reference instantiation, 128 locked tasks and 987 assertions over document, spreadsheet, chart, tool and database work, stays sealed: the procedure is the artifact, not the corpus. Across eleven systems, four results. Capability availability is measurable: two complete single-route runs on identical weights later failed distinct predicates of the finalized binding gate, while a third passed that gate before a fresh run. The advertised identifier exposed neither limit. Discrimination is not uniform: four of seven suites saturate under a six-system band, with the spread almost entirely from governed database work and multi-tab joins, so we report interval-backed resolution groups, not ranks; two of the nominal five-label output's four cuts fail multiplicity adjustment. Serving-arm choice moved one declared revision and precision from 77.38 to 82.54, paired interval [0.11,10.60], though the arms differ in access mode, harness generation, and the serving tool-call parser, and harness generation is a property of our evaluator, not any endpoint. Excluding failed responses from denominators changes the point ordering, so reliability inclusion changes a conclusion, not its wording.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。