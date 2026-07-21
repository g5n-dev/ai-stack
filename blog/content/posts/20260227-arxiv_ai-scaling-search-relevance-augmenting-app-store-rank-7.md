---
title: 'Scaling Search Relevance: Augmenting App Store Ranking with LLM-Generated
  Judgments'
date: 2026-02-27 02:54:04+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
- 大语言模型
categories:
- 论文
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.23234v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:22138b73c391fa2c81b89223766b473931afca1d480474a08272e3f20418f23c
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 83
captured_at: '2026-07-18T04:30:44.821176Z'
source_capture_sha256: sha256:a332b77652b559898d079f81fc39bce1de145903848ff04b705d75b0ca19ded3
source_capture_chars_original: 1399
source_publication_excerpt_chars: 1399
observation_id: obs_a1b0fc40c3a744ba776a975ed0ea79ccb1b5a2930f685020ab36f165ffca1ef0
revision_id: rev_6f10e29997e7daa636e46ef4ae28013dcc7a28a5a23fb2c85f59d98e45033b8b
event_id: evt_9a8182155a88aca8abd380c651856617b9de6cff8c033a2f0d5c5d639ef9978a
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-27T03:55:34Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.23234v1](<https://arxiv.org/abs/2602.23234v1>)
- **作者**: Evangelia Christakopoulou, Vivekkumar Patel, Hemanth Velaga, Sandip Gaikwad
- **分类**: cs.IR
- **论文时间**: 2026-02-26T17:11:26Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.23234v1.pdf](<https://arxiv.org/pdf/2602.23234v1.pdf>)

## 来源摘要/节选

> Large-scale commercial search systems optimize for relevance to drive successful sessions that help users find what they are looking for. To maximize relevance, we leverage two complementary objectives: behavioral relevance \(results users tend to click or download\) and textual relevance \(a result's semantic fit to the query\). A persistent challenge is the scarcity of expert-provided textual relevance labels relative to abundant behavioral relevance labels. We first address this by systematically evaluating LLM configurations, finding that a specialized, fine-tuned model significantly outperforms a much larger pre-trained one in providing highly relevant labels. Using this optimal model as a force multiplier, we generate millions of textual relevance labels to overcome the data scarcity. We show that augmenting our production ranker with these textual relevance labels leads to a significant outward shift of the Pareto frontier: offline NDCG improves for behavioral relevance while simultaneously increasing for textual relevance. These offline gains were validated by a worldwide A/B test on the App Store ranker, which demonstrated a statistically significant +0.24% increase in conversion rate, with the most substantial performance gains occurring in tail queries, where the new textual relevance labels provide a robust signal in the absence of reliable behavioral relevance labels.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
