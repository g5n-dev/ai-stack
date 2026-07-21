---
title: Smooth Gate Functions for Soft Advantage Policy Optimization
date: 2026-02-24 03:30:14+08:00
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
external_url: https://arxiv.org/abs/2602.19345v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:cc7af8e21a02f9ec145e7f673d2ebb465491f311001c05265f7b6cf466147759
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 60
captured_at: '2026-07-18T04:16:46.350966Z'
source_capture_sha256: sha256:ba073061cc9a6c0ddaf41e6b2b3b81cc90b8d2fc3c7c85df990ef439b4f17c78
source_capture_chars_original: 985
source_publication_excerpt_chars: 985
observation_id: obs_eb312e080498bb51d559c35cc2bf40c95586ffb57f51f1696108b0483e96437d
revision_id: rev_0808a76bbed5289fd6a38332e9f89d4ddead4b27a47bf19f7c8d3dec12411756
event_id: evt_550efed66a1c5173a91d898a820586d386232df65289cb40bd63e0f5ac456fd0
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.19345v1](<https://arxiv.org/abs/2602.19345v1>)
- **作者**: Egor Denisov, Svetlana Glazyrina, Maksim Kryzhanovskiy, Roman Ischenko
- **分类**: cs.LG
- **论文时间**: 2026-02-22T21:19:26Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.19345v1.pdf](<https://arxiv.org/pdf/2602.19345v1.pdf>)

## 来源摘要/节选

> Group Relative Policy Optimization \(GRPO\) has significantly advanced the training of large language models and enhanced their reasoning capabilities, while it remains susceptible to instability due to the use of hard clipping. Soft Adaptive Policy Optimization \(SAPO\) addresses this limitation by replacing clipping with a smooth sigmoid-based gate function, which leads to more stable updates. We have decided to push this theory further and investigate the impact of different gate functions on both training stability and final model performance. We formalize the key properties that admissible gates should satisfy and identify several families of such functions for empirical evaluation. This paper presents an analysis of our findings based on experiments conducted with the Qwen2.5-7B-Instruct model on mathematical reasoning tasks. These results provide practical guidance for designing smoother and more robust policy optimization objectives for large language model training.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
