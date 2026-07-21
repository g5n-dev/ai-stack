---
title: Discourse-Aware Dual-Track Streaming Response for Low-Latency Spoken Dialogue
  Systems
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
external_url: https://arxiv.org/abs/2602.23266v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:7416a4f6725b6434ea42ab43b2398bf2d0a21577c57c2f4463a8897b4e913fec
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 85
captured_at: '2026-07-18T04:30:40.966842Z'
source_capture_sha256: sha256:3db5d1a30a2f8d57a63f7494c26f9c4dd41713b0cb14a1142a0c2470066919ea
source_capture_chars_original: 1425
source_publication_excerpt_chars: 1425
observation_id: obs_6236fc4fc8f8127bca6f9addb51eb85566e07aeaa67d89fa846571247b630917
revision_id: rev_bd788b2aef3d0fa7d33d0be287dc2eefd7d8ae22cb01f50d55b93a1a0e30858f
event_id: evt_83f17c873e441a4c0ee09bc6b31647e48ae24112c0ec503ea3ce5dcb0d4023d6
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.23266v1](<https://arxiv.org/abs/2602.23266v1>)
- **作者**: Siyuan Liu, Jiahui Xu, Feng Jiang, Kuang Wang, Zefeng Zhao, Chu-Ren Huang, Jinghang Gu, Changqing Yin, Haizhou Li
- **分类**: cs.CL
- **论文时间**: 2026-02-26T17:39:56Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.23266v1.pdf](<https://arxiv.org/pdf/2602.23266v1.pdf>)

## 来源摘要/节选

> Achieving human-like responsiveness is a critical yet challenging goal for cascaded spoken dialogue systems. Conventional ASR-LLM-TTS pipelines follow a strictly sequential paradigm, requiring complete transcription and full reasoning before speech synthesis can begin, which results in high response latency. We propose the Discourse-Aware Dual-Track Streaming Response \(DDTSR\) framework, a low-latency architecture that enables listen-while-thinking and speak-while-thinking. DDTSR is built upon three key mechanisms: \(1\) connective-guided small-large model synergy, where an auxiliary small model generates minimal-committal discourse connectives while a large model performs knowledge-intensive reasoning in parallel; \(2\) streaming-based cross-modal collaboration, which dynamically overlaps ASR, LLM inference, and TTS to advance the earliest speakable moment; and \(3\) curriculum-learning-based discourse continuity enhancement, which maintains coherence and logical consistency between early responses and subsequent reasoning outputs. Experiments on two spoken dialogue benchmarks demonstrate that DDTSR reduces response latency by 19%-51% while preserving discourse quality. Further analysis shows that DDTSR functions as a plug-and-play module compatible with diverse LLM backbones, and remains robust across varying utterance lengths, indicating strong practicality and scalability for real-time spoken interaction.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
