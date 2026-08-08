---
title: "Beyond Top-K: Replacing Black-Box Retrieval with Interpretable Agentic Operations"
date: 2026-08-08T06:58:07+08:00
draft: false
entry_kind: "auto"
tags: ["AI Agent", "cs.AI", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:2fc328e4d77ecf05202fc86ec78ed9496177b43b0a73c440912a2933688161b4"
source_payload_sha256: "sha256:f628fd3c522d458bb94c3b6efa9e8f73ff01c46b5d012914d42ccd7282b2ef25"
observation_id: obs_23d83db6b24f3aa19aa628edf7b58fb2f995dba02f96aedc051c1ee82d576308
event_id: evt_49af30a9fba06f7b4720dbfb0f4cf7b775a4155b91df2a123f44ae708731b05c
revision_id: rev_d550c9a4556531c748f2ee976950f8294c15d89248915bbc882b95f002ab2598
source_published_at: 2026-08-06T17:23:13Z
first_seen_at: 2026-08-07T23:07:06Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 81
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2608.06305v1
parent_observation_id: null
last_seen_at: 2026-08-08T00:00:00Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.06305v1](http://arxiv.org/abs/2608.06305v1)
- **发布域名**: arxiv.org
- **分类**: cs.AI
- **作者**: Sagar Tamang、Ayush Vyas、Tabarakul Hazarika

## 来源摘要/节选

> Retrieval-augmented generation over long documents is dominated by one design: chunk the text, embed the chunks, and surface the top-k nearest neighbours of the query. We argue that for an important class of documents -- financial statements, audit reports, regulatory returns -- this design is structurally unsound, and we make the argument measurable. On a 780-page government financial report, 86.8% of content lines are table rows, thousands of near-identical figures compete in one embedding space, and a figure inherits its unit from a header a median of 13 lines above it -- so a chunk boundary routinely separates a number from whether it is in lakh or crore, an error of two orders of magnitude. A table-aware chunker built as a steelman fixes the unit problem but leaves 27-30% of numeric chunks with no fiscal-year header at every chunk size we tried. We propose READ (Reliable Embedding-free Agentic Document-search), in which an agent reads the raw document through three deterministic operations -- normalized lexical search, structural navigation, and bounded span reads -- exposed over the Model Context Protocol, so a trajectory is a replayable audit trail, not an opaque similarity score. On 51 verified questions READ answers 58.8% against dense retrieval's 15.7% (p_Holm = 2 x 10^-5) -- or 35.3% tuned, which READ still leads by 23.5 points (p_Holm = 0.017). An agent given the same loop but a top-k tool reaches only 27.5%, locating the gain in the interface rather than in iteration. We also report what the evidence does not support: BM25 is statistically indistinguishable from READ, so our result separates embedding-based from embedding-free retrieval, not agentic from lexical search.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。