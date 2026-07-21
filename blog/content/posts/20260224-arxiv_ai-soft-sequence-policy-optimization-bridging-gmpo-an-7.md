---
title: 'Soft Sequence Policy Optimization: Bridging GMPO and SAPO'
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
external_url: https://arxiv.org/abs/2602.19327v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:082c3d46a0d9620a8dab2d3fc7be05d11c3f9803199f6caa4fd5e9d4dd6cbeba
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 57
captured_at: '2026-07-18T04:16:46.350966Z'
source_capture_sha256: sha256:8cb6dcab466494ad243c9166a61eda861d3a4e46d97ae6eab9ed5ae87f9c7b2f
source_capture_chars_original: 1153
source_publication_excerpt_chars: 1153
observation_id: obs_100f18a66eeada8a06654d57b898722a7a8da6b0f226dafa0241cf6b6644779d
revision_id: rev_c6d75831b2413c0bc4215bd1f6cef3e76e4b7778cfb59a196fb73f9dc089bbfe
event_id: evt_f96b314b1018a1fc2ac9ef7a6fd1b962c45b213886dcf12c49dabce793aefa92
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.19327v1](<https://arxiv.org/abs/2602.19327v1>)
- **作者**: Svetlana Glazyrina, Maksim Kryzhanovskiy, Roman Ischenko
- **分类**: cs.LG
- **论文时间**: 2026-02-22T20:21:00Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.19327v1.pdf](<https://arxiv.org/pdf/2602.19327v1.pdf>)

## 来源摘要/节选

> A significant portion of recent research on Large Language Model \(LLM\) alignment focuses on developing new policy optimization methods based on Group Relative Policy Optimization \(GRPO\). Two prominent directions have emerged: \(i\) a shift toward sequence-level importance sampling weights that better align with the sequence-level rewards used in many tasks, and \(ii\) alternatives to PPO-style clipping that aim to avoid the associated loss of training signal and entropy collapse. Recent work, such as Soft Adaptive Policy Optimization \(SAPO\), reformulates the Scopic objective within the GRPO framework and achieves both sequence coherence and token adaptivity. Geometric-Mean Policy Optimization \(GMPO\) leverages token-wise ratio clipping within sequence importance sampling weights. Building on these ideas, this work proposes a new objective that promotes effective policy exploration while maintaining training stability. Specifically, we introduce Soft Sequence Policy Optimization, an off-policy reinforcement learning objective that incorporates soft gating functions over token-level probability ratios within sequence-level importance weights.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
