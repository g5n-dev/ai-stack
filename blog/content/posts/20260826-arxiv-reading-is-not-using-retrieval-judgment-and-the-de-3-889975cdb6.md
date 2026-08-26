---
title: "Reading Is Not Using: Retrieval, Judgment, and the Design of AI Financial Research Workflows"
date: 2026-08-26T18:53:41+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "cs.CL", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:8b0d73be5138ac45fc14279cc5cca8509d8f8e742ccabcec1508661d4f151a5c"
source_payload_sha256: "sha256:51366b7df312f9ddf241ab7286ba3415db749c10fb4f3ca39480404b2e13e3c7"
observation_id: obs_889975cdb69f3694905731f0695e1f3008a0ab63220c642ab7dfafd03ff803e3
event_id: evt_cde83480888f18bbab63a9ff8eb8f4e9fc2ca71f7a6e466a068abfa3373719cd
revision_id: rev_7a12527f8b55c29adede00130d438d69988a0580fa2d5640213da278d3cc29f9
source_published_at: 2026-08-25T17:31:25Z
first_seen_at: 2026-08-26T11:03:55Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 92
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2608.24842v1
parent_observation_id: null
last_seen_at: 2026-08-26T10:51:34.856490Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.24842v1](http://arxiv.org/abs/2608.24842v1)
- **发布域名**: arxiv.org
- **分类**: cs.CL
- **作者**: Miao Liu、Zhizhe Liu

## 来源摘要/节选

> Large language models (LLMs) are increasingly deployed as AI analysts to process financial disclosures and support AI-assisted investment decisions. Yet such systems are usually evaluated by what they can retrieve, not whether retrieved information affects their judgments. We identify a retrieval-integration gap in long-context financial analysis. Holding focal-firm information fixed and varying only unrelated context from 2,000 to 128,000 tokens, we find that a risk disclosure's influence on investment judgments falls to the experimental noise floor even as direct retrieval remains accurate. The pattern replicates across model families and judgment tasks and in experiments removing real disclosures from actual 10-K filings. More capable models postpone but do not eliminate the gap. Causal memory interventions show that compressed summaries and source-text lookup jointly transmit disclosures into judgments. Workflow architecture determines whether this transmission succeeds: chunk-and-summarize pipelines evict relevant information, whereas a targeted, structured restatement adjacent to the decision restores its influence. AI analyst performance is therefore jointly determined by model capability and workflow architecture. Retrieval-based evaluations can certify systems whose investment judgments ignore information they demonstrably retrieved.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。