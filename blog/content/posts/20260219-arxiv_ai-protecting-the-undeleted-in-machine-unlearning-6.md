---
title: Protecting the Undeleted in Machine Unlearning
date: 2026-02-19 22:55:31+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.16697v1
aliases:
- /posts/20260220-arxiv_ai-protecting-the-undeleted-in-machine-unlearning-6/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:361ff5de8ae72a55ff37819030b33dc863560e20ef6279c70fe4aef4dfb14670
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 46
captured_at: '2026-07-18T04:16:04.060671Z'
source_capture_sha256: sha256:05d78d08400636cf2b4ee69752f65529c48c83cedc9c413a993986668f9cfcf4
source_capture_chars_original: 1146
source_publication_excerpt_chars: 1146
observation_id: obs_4d6c0eb2250a72bcc7b272b818f4991d91466bcdeaa5440f1e6f5dff69518694
revision_id: rev_45fe1eb984050ae60456eb44e34053d817f3b5e497681fb792c1acd95a4b25dc
event_id: evt_8e5fb3e2230a0783019ba0c136c3ab6f8f3e71e427e082e2d799f68ab64f804c
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.16697v1](<https://arxiv.org/abs/2602.16697v1>)
- **作者**: Aloni Cohen, Refael Kohen, Kobbi Nissim, Uri Stemmer
- **分类**: cs.LG
- **论文时间**: 2026-02-18T18:44:21Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.16697v1.pdf](<https://arxiv.org/pdf/2602.16697v1.pdf>)

## 来源摘要/节选

> Machine unlearning aims to remove specific data points from a trained model, often striving to emulate "perfect retraining", i.e., producing the model that would have been obtained had the deleted data never been included. We demonstrate that this approach, and security definitions that enable it, carry significant privacy risks for the remaining \(undeleted\) data points. We present a reconstruction attack showing that for certain tasks, which can be computed securely without deletions, a mechanism adhering to perfect retraining allows an adversary controlling merely $ω\(1\)$ data points to reconstruct almost the entire dataset merely by issuing deletion requests. We survey existing definitions for machine unlearning, showing they are either susceptible to such attacks or too restrictive to support basic functionalities like exact summation. To address this problem, we propose a new security definition that specifically safeguards undeleted data against leakage caused by the deletion of other points. We show that our definition permits several essential functionalities, such as bulletin boards, summations, and statistical learning.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
