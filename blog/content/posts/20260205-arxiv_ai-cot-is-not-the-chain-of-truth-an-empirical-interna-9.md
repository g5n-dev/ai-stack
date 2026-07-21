---
title: 'CoT is Not the Chain of Truth: An Empirical Internal Analysis of Reasoning
  LLMs for Fake News Generation'
date: 2026-02-05 23:03:18+08:00
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
external_url: https://arxiv.org/abs/2602.04856v1
aliases:
- /posts/20260206-arxiv_ai-cot-is-not-the-chain-of-truth-an-empirical-interna-9/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:acc612f87f6ab8d3715e2efc78cf51e697cd93c7ea3b94441da0f2deb49bccfc
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 104
captured_at: '2026-07-18T04:10:49.793468Z'
source_capture_sha256: sha256:8971f025b32a13f3e662c629d9a1e53af76f1d90f15db7bf1ebf9618e5a66f98
source_capture_chars_original: 1346
source_publication_excerpt_chars: 1346
observation_id: obs_62cac9073d3a7d3ccbb00b60ecd1eec23fcfe33e9ddf6585d95d2820f99294ae
revision_id: rev_85c44ba8505f3726463be9c8bb6fe9cd6e8687d6de2be19ef5e7377406560dae
event_id: evt_d5f229043d9f1430756dafb825dbc3cb706811f67f349e338be5f36f23374c01
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-05T04:21:21Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.04856v1](<https://arxiv.org/abs/2602.04856v1>)
- **作者**: Zhao Tong, Chunlin Gong, Yiping Zhang, Qiang Liu, Xingcheng Xu, Shu Wu, Haichao Shi, Xiao-Yu Zhang
- **分类**: cs.CL
- **论文时间**: 2026-02-04T18:43:10Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.04856v1.pdf](<https://arxiv.org/pdf/2602.04856v1.pdf>)

## 来源摘要/节选

> From generating headlines to fabricating news, the Large Language Models \(LLMs\) are typically assessed by their final outputs, under the safety assumption that a refusal response signifies safe reasoning throughout the entire process. Challenging this assumption, our study reveals that during fake news generation, even when a model rejects a harmful request, its Chain-of-Thought \(CoT\) reasoning may still internally contain and propagate unsafe narratives. To analyze this phenomenon, we introduce a unified safety-analysis framework that systematically deconstructs CoT generation across model layers and evaluates the role of individual attention heads through Jacobian-based spectral metrics. Within this framework, we introduce three interpretable measures: stability, geometry, and energy to quantify how specific attention heads respond or embed deceptive reasoning patterns. Extensive experiments on multiple reasoning-oriented LLMs show that the generation risk rise significantly when the thinking mode is activated, where the critical routing decisions concentrated in only a few contiguous mid-depth layers. By precisely identifying the attention heads responsible for this divergence, our work challenges the assumption that refusal implies safety and provides a new understanding perspective for mitigating latent reasoning risks.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
