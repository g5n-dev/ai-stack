---
title: "Quantifying Overclaiming Propensity in Frontier LLM Agents"
date: 2026-09-19T05:44:25+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "cs.SE", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:2eab0e364222103e4ff2f95a89ad2fdac53ee75d13336a430df644e1b1079acc"
source_payload_sha256: "sha256:52a36eeeb569bc1018b9da09dc30666760d0b214446429baa9c831d2bff5c96a"
observation_id: obs_803d5efe7eafa0597bc3ebca709fa939d0e5def9d0c528953d9b7a730b77c705
event_id: evt_7aa46ea3f46d977506133861873447f81e0e5271c1b8a9f250e8f594568dc4ee
revision_id: rev_cc428ae929bfa52d55a894fcaf1e2ad432409221a9d1718a4986bd6ac2e3862c
source_published_at: 2026-09-17T17:59:04Z
first_seen_at: 2026-09-18T21:41:18.130357Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 58
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2609.20812v1
parent_observation_id: null
last_seen_at: 2026-09-18T21:41:18.130357Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.20812v1](http://arxiv.org/abs/2609.20812v1)
- **发布域名**: arxiv.org
- **分类**: cs.SE
- **作者**: Nolan Smyth、Yorguin-Jose Mantilla-Ramos、Pascal Jr Tikeng Notsawo 等

## 来源摘要/节选

> Frontier coding agents are increasingly trusted to work autonomously for long periods, yet an agent's final response is often the only account of that work a user sees. We quantify the propensity of frontier agents to \emph{overclaim} task completion, a misrepresentation that can mislead the user. An agent overclaims when its final response contradicts information in its context. This definition requires no inference about intent and is independent of task success. We introduce \emph{OverclaimBench}, an evaluation suite composed of five file-review scenarios, transcript-based coverage measurements, and registered planted defects. We evaluate eight proprietary frontier models in their own production command-line interfaces, and four open-weight models under a single fixed harness on OverclaimBench and find that 1) agents do not read all the files they were asked to review in 67.9\% of runs; 2) among runs where not all files are read, agents are \emph{misleading} 80.4\% of the time (59--96\% per model), either falsely claiming to have read all files or omitting that coverage is incomplete; 3) requiring delegation to subagents increased reading coverage, but among reviews that remained incomplete, a large majority were still misleading; and 4) agents that falsely claimed a complete review missed planted defects at about 1.8 times the rate of agents that read every file, showing that claims of completion can conceal substantive failures. Together, these results show that agents' final responses are not reliable accounts of their actions.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。