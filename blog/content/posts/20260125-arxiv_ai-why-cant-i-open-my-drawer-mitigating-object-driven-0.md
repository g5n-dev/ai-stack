---
title: Why Can't I Open My Drawer? Mitigating Object-Driven Shortcuts in Zero-Shot
  Compositional Action Recognition
date: 2026-01-25 12:39:55+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2601.16211v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:0b2c2d22e3c85facd560ced147c6983288f087f5c91846d6abb744661222a20b
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 108
captured_at: '2026-07-18T04:08:56.487166Z'
source_capture_sha256: sha256:24c67193026684e56d18e1162723d2e60abe8cf4bf5a7c74edf16495f4ab8192
source_capture_chars_original: 1551
source_publication_excerpt_chars: 1551
observation_id: obs_ee31aff56d824d5b51c4632961f933596619fe5cf284bf751091294cd63d8c1b
revision_id: rev_b5764239d77d8b9967379e0768305fd4a8029b1b5d465a8bc8b553e75aebb553
event_id: evt_b67f8f50a2d0f138515e7e9feb7302103304ab4dde54ab65e6f3ff314227e16d
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-01-25T12:41:54Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2601.16211v1](<https://arxiv.org/abs/2601.16211v1>)
- **作者**: Geo Ahn, Inwoong Lee, Taeoh Kim, Minho Shim, Dongyoon Wee, Jinwoo Choi
- **分类**: cs.CV
- **论文时间**: 2026-01-22T18:59:13Z
- **论文 PDF**: [https://arxiv.org/pdf/2601.16211v1.pdf](<https://arxiv.org/pdf/2601.16211v1.pdf>)

## 来源摘要/节选

> We study Compositional Video Understanding \(CVU\), where models must recognize verbs and objects and compose them to generalize to unseen combinations. We find that existing Zero-Shot Compositional Action Recognition \(ZS-CAR\) models fail primarily due to an overlooked failure mode: object-driven verb shortcuts. Through systematic analysis, we show that this behavior arises from two intertwined factors: severe sparsity and skewness of compositional supervision, and the asymmetric learning difficulty between verbs and objects. As training progresses, the existing ZS-CAR model increasingly ignores visual evidence and overfits to co-occurrence statistics. Consequently, the existing model does not gain the benefit of compositional recognition in unseen verb-object compositions. To address this, we propose RCORE, a simple and effective framework that enforces temporally grounded verb learning. RCORE introduces \(i\) a composition-aware augmentation that diversifies verb-object combinations without corrupting motion cues, and \(ii\) a temporal order regularization loss that penalizes shortcut behaviors by explicitly modeling temporal structure. Across two benchmarks, Sth-com and our newly constructed EK100-com, RCORE significantly improves unseen composition accuracy, reduces reliance on co-occurrence bias, and achieves consistently positive compositional gaps. Our findings reveal object-driven shortcuts as a critical limiting factor in ZS-CAR and demonstrate that addressing them is essential for robust compositional video understanding.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
