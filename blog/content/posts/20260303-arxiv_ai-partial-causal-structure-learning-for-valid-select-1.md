---
title: Partial Causal Structure Learning for Valid Selective Conformal Inference under
  Interventions
date: 2026-03-03 23:28:17+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2603.02204v1
aliases:
- /posts/20260304-arxiv_ai-partial-causal-structure-learning-for-valid-select-1/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:b9e2a41d0199516070b1d9b7280ae7665bd139d438b3e57bae4ccc7b2c07e694
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 93
captured_at: '2026-07-18T04:26:34.932328Z'
source_capture_sha256: sha256:b1fb470572b5c934ecbbd9f6ac3f73f01356c050e10f6759a29f85f3e4dd5f86
source_capture_chars_original: 1792
source_publication_excerpt_chars: 1792
observation_id: obs_0013f2fd66061a6d0dbbfad82eeebad30314a521306ad3274bd136de01fe25bd
revision_id: rev_67ed5356e5f7324f791d7d9452f84c6873f55e3d00fac01dc4a4795ea58720dd
event_id: evt_e2c1dd21b5fcba5ade95c71fafe19413804bf5bd29f2dacdb9877e73057d3500
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-03-03T06:15:49Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.02204v1](<https://arxiv.org/abs/2603.02204v1>)
- **作者**: Amir Asiaee, Kavey Aryan, James P. Long
- **分类**: cs.LG
- **论文时间**: 2026-03-02T18:58:22Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.02204v1.pdf](<https://arxiv.org/pdf/2603.02204v1.pdf>)

## 来源摘要/节选

> Selective conformal prediction can yield substantially tighter uncertainty sets when we can identify calibration examples that are exchangeable with the test example. In interventional settings, such as perturbation experiments in genomics, exchangeability often holds only within subsets of interventions that leave a target variable "unaffected" \(e.g., non-descendants of an intervened node in a causal graph\). We study the practical regime where this invariance structure is unknown and must be learned from data. Our contributions are: \(i\) a contamination-robust conformal coverage theorem that quantifies how misclassification of "unaffected" calibration examples degrades coverage via an explicit function $g\(δ,n\)$ of the contamination fraction and calibration set size, providing a finite-sample lower bound that holds for arbitrary contaminating distributions; \(ii\) a task-driven partial causal learning formulation that estimates only the binary descendant indicators $Z\_\{a,i\}=\\mathbf\{1\}\\\{i\\in\\mathrm\{desc\}\(a\)\\\}$ needed for selective calibration, rather than the full causal graph; and \(iii\) algorithms for descendant discovery via perturbation intersection patterns \(differentially affected variable set intersections across interventions\), and for approximate distance-to-intervention estimation via local invariant causal prediction. We provide recovery conditions under which contamination is controlled. Experiments on synthetic linear structural equation models \(SEMs\) validate the bound: under controlled contamination up to $δ=0.30$, the corrected procedure maintains $\\ge 0.95$ coverage while uncorrected selective CP degrades to $0.867$. A proof-of-concept on Replogle K562 CRISPR interference \(CRISPRi\) perturbation data demonstrates applicability to real genomic screens.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
