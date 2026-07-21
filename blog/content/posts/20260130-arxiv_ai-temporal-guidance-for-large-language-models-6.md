---
title: Temporal Guidance for Large Language Models
date: 2026-01-30 03:54:32+08:00
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
external_url: https://arxiv.org/abs/2601.21744v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:97e41bb90b111f2a3c8404eeea537ef21cf6c22ce1a9a8e9f1e0ea4b68025444
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 43
captured_at: '2026-07-18T04:10:00.628947Z'
source_capture_sha256: sha256:f1f6089d7393e0e418dbdc8095de995f3aa040874366128345b547f79ad38d6c
source_capture_chars_original: 1086
source_publication_excerpt_chars: 1086
observation_id: obs_d909a0733a0cef7fddc3a47049640fd066d196981c8c7f02920f7fedc671f8ec
revision_id: rev_d8bb15c171650e02f2acc64afc7a027b4516d0a5a34a5b48291e2b7e69658ad3
event_id: evt_7e87a3e231863ed3f1f46320a0aaf4b7bcef1625b2a55cafefad84c69b6e58bf
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-01-30T03:58:50Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2601.21744v1](<https://arxiv.org/abs/2601.21744v1>)
- **作者**: Hong-Kai Zheng, Piji Li
- **分类**: cs.CL
- **论文时间**: 2026-01-29T14:01:00Z
- **论文 PDF**: [https://arxiv.org/pdf/2601.21744v1.pdf](<https://arxiv.org/pdf/2601.21744v1.pdf>)

## 来源摘要/节选

> Contrastive Decoding \(CD\) enhances the generation quality of large language models \(LLMs\) but incurs significant additional computational overhead due to the need for an auxiliary model. Existing internal self-contrastive decoding methods, such as Decoding by Contrasting Layers \(DoLa\), focus on discrepancies across different layers, which are notably unstable on small-scale models. In this work, based on the observation that LLMs exhibit local preferences, we propose a novel contrastive guidance strategy along the temporal dimension, namely Temporal Guidance \(TeGu\). Our method ingeniously leverages Multi-Token Prediction \(MTP\) to construct weaker amateur predictions for model self-contrast. To standardize the implementation of this mechanism, we further introduce a lightweight Conditional MTP Projector \(cMTPP\), which avoids maintaining multiple independent networks as required by other MTP modules. Across various model series and benchmarks, TeGu achieves significant performance improvements while maintaining low additional memory consumption and computational overhead.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
