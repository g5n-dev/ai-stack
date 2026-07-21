---
title: 'BEVLM: Distilling Semantic Knowledge from LLMs into Bird''s-Eye View Representations'
date: 2026-03-09 21:48:42+08:00
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
external_url: https://arxiv.org/abs/2603.06576v1
aliases:
- /posts/20260310-arxiv_ai-bevlm-distilling-semantic-knowledge-from-llms-into-0/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:4511c17d8a027599bc7c51e80864043d88dd4fd8b9e71d756bcee4061043c99d
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 83
captured_at: '2026-07-18T04:27:20.159062Z'
source_capture_sha256: sha256:f26377d032a0562ea7b572017ff7cf505ce5487d346a77011b11d368b52a66ad
source_capture_chars_original: 1299
source_publication_excerpt_chars: 1299
observation_id: obs_a2743254ac19e0433e317b0acef0e2d7a99348dee5e6291ab88657f9bcde75d3
revision_id: rev_1f8d6d3b941344f9bc3f82986536ef528736e66172611089c59f52a3f6c2e698
event_id: evt_e146d037acd0644fecf0440a5352df56f791529fbead33e3f370d335679c4255
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-03-09T03:53:15Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.06576v1](<https://arxiv.org/abs/2603.06576v1>)
- **作者**: Thomas Monninger, Shaoyuan Xie, Qi Alfred Chen, Sihao Ding
- **分类**: cs.CV
- **论文时间**: 2026-03-06T18:59:55Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.06576v1.pdf](<https://arxiv.org/pdf/2603.06576v1.pdf>)

## 来源摘要/节选

> The integration of Large Language Models \(LLMs\) into autonomous driving has attracted growing interest for their strong reasoning and semantic understanding abilities, which are essential for handling complex decision-making and long-tail scenarios. However, existing methods typically feed LLMs with tokens from multi-view and multi-frame images independently, leading to redundant computation and limited spatial consistency. This separation in visual processing hinders accurate 3D spatial reasoning and fails to maintain geometric coherence across views. On the other hand, Bird's-Eye View \(BEV\) representations learned from geometrically annotated tasks \(e.g., object detection\) provide spatial structure but lack the semantic richness of foundation vision encoders. To bridge this gap, we propose BEVLM, a framework that connects a spatially consistent and semantically distilled BEV representation with LLMs. Through extensive experiments, we show that BEVLM enables LLMs to reason more effectively in cross-view driving scenes, improving accuracy by 46%, by leveraging BEV features as unified inputs. Furthermore, by distilling semantic knowledge from LLMs into BEV representations, BEVLM significantly improves closed-loop end-to-end driving performance by 29% in safety-critical scenarios.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
