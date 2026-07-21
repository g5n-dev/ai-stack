---
title: Mode Seeking meets Mean Seeking for Fast Long Video Generation
date: 2026-03-02 23:25:37+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.24289v1
aliases:
- /posts/20260303-arxiv_ai-mode-seeking-meets-mean-seeking-for-fast-long-vide-0/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:f0cbeae975d961374a8d10ab25cdd20f3f1a2d23f39df4d68240d73a2504f27f
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 62
captured_at: '2026-07-18T04:26:12.126510Z'
source_capture_sha256: sha256:aa4af8ef8a5c6a3a540950998eb5c7c76a42309f9a6b045162585e1a12013d55
source_capture_chars_original: 1234
source_publication_excerpt_chars: 1234
observation_id: obs_ee749a97d8dcbeb948100865021be1390a9333a17002ffb9d6e96b8b11c11653
revision_id: rev_0d1be9769c56760bd16e0ca374820aa5ebca5a7e101d77d674c99ee8c4ddd77a
event_id: evt_4e6252fafa090f2ca9cc54a0f57b9f6f19b1aa25925a30a08f8f3659e12874c9
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-03-02T06:24:05Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.24289v1](<https://arxiv.org/abs/2602.24289v1>)
- **作者**: Shengqu Cai, Weili Nie, Chao Liu, Julius Berner, Lvmin Zhang, Nanye Ma, Hansheng Chen, Maneesh Agrawala, Leonidas Guibas, Gordon Wetzstein, Arash Vahdat
- **分类**: cs.CV
- **论文时间**: 2026-02-27T18:59:02Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.24289v1.pdf](<https://arxiv.org/pdf/2602.24289v1.pdf>)

## 来源摘要/节选

> Scaling video generation from seconds to minutes faces a critical bottleneck: while short-video data is abundant and high-fidelity, coherent long-form data is scarce and limited to narrow domains. To address this, we propose a training paradigm where Mode Seeking meets Mean Seeking, decoupling local fidelity from long-term coherence based on a unified representation via a Decoupled Diffusion Transformer. Our approach utilizes a global Flow Matching head trained via supervised learning on long videos to capture narrative structure, while simultaneously employing a local Distribution Matching head that aligns sliding windows to a frozen short-video teacher via a mode-seeking reverse-KL divergence. This strategy enables the synthesis of minute-scale videos that learns long-range coherence and motions from limited long videos via supervised flow matching, while inheriting local realism by aligning every sliding-window segment of the student to a frozen short-video teacher, resulting in a few-step fast long video generator. Evaluations show that our method effectively closes the fidelity-horizon gap by jointly improving local sharpness, motion and long-range consistency. Project website: https://primecai.github.io/mmm/.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
