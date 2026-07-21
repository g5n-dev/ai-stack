---
title: 'Why Adam Works Better with $β_1 = β_2$: The Missing Gradient Scale Invariance
  Principle'
date: 2026-01-30 03:54:32+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2601.21739v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:c69913c5b027de93bcd50dac3a6c7517ac656b9cc6d1c8d9a3dc16b3ebb142e4
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 87
captured_at: '2026-07-18T04:10:00.628947Z'
source_capture_sha256: sha256:1bf0be66291a3c4e19b34cc2b06218e58ee3bac680584aa7108d619064bdb563
source_capture_chars_original: 1184
source_publication_excerpt_chars: 1184
observation_id: obs_e7550136ebfd902a745f7de3b5f4ad30326cd9d25bc61bfead5ef5ad67d21b54
revision_id: rev_21dc98be7d73e77ee78a69b7c31069e0a93bdd57473765bb54bf6a0b986bca5d
event_id: evt_381151c6cf47a1c0bc8b53820b27d17ab36a90b3bd939c55eaf48a06e45daeea
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-01-29T19:54:32Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2601.21739v1](<https://arxiv.org/abs/2601.21739v1>)
- **作者**: Alberto Fernández-Hernández, Cristian Pérez-Corral, Jose I. Mestre, Manuel F. Dolz, Enrique S. Quintana-Ortí
- **分类**: cs.LG
- **论文时间**: 2026-01-29T13:56:11Z
- **论文 PDF**: [https://arxiv.org/pdf/2601.21739v1.pdf](<https://arxiv.org/pdf/2601.21739v1.pdf>)

## 来源摘要/节选

> Adam has been at the core of large-scale training for almost a decade, yet a simple empirical fact remains unaccounted for: both validation scores and the qualitative behaviour of the training runs improve when the momentum parameters satisfy $β\_\{1\}=β\_\{2\}$. Some recent studies have reported this pattern, but there is still no explanation for why this choice helps. We show that this choice is closely tied to a structural property that we refer to as \\textit\{gradient scale invariance\}. We formalize this notion and prove that Adam becomes gradient scale invariant of first order if and only if $β\_\{1\}=β\_\{2\}$. This perspective places the balanced regime of Adam in direct alignment with the design principles underlying several recent optimizers that explicitly enforce scale-robust updates. The theory is supported by experiments across vision and language tasks, and across different architectural families, in which rescaling the gradient has a markedly smoother effect on the update when $β\_\{1\}=β\_\{2\}$. Overall, our results offer a coherent explanation for an open question in the behavior of Adam and provide a simple principle that helps guide the design of future optimizers.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
