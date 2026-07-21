---
title: Scaling Verification Can Be More Effective than Scaling Policy Learning for
  Vision-Language-Action Alignment
date: 2026-02-13 23:30:43+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.12281v1
aliases:
- /posts/20260214-arxiv_ai-scaling-verification-can-be-more-effective-than-sc-0/
- /posts/20260215-arxiv_ai-scaling-verification-can-be-more-effective-than-sc-0/
- /posts/20260216-arxiv_ai-scaling-verification-can-be-more-effective-than-sc-0/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:84819cd24854f2484373f1fe13a49c6640632727e5fd8c1248a9a21f569a83da
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 108
captured_at: '2026-07-18T04:15:22.283119Z'
source_capture_sha256: sha256:89caf2f7ba2b5c87f6ba8bd01a8f40553aa276f9e4114c6c7244287a2215e1a8
source_capture_chars_original: 1620
source_publication_excerpt_chars: 1620
observation_id: obs_45191be22d0a82229804ad0529149ce91de16a54cd3346e1451490286e11a73c
revision_id: rev_93e9e4a812be6f95fc44df5e7570ce1e17949447a17ac5b9cf276e439a98757b
event_id: evt_9739f11904692b30bb1d560d5a6e70ff6c6327fac9e170fb02d850467010c625
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-13T06:19:22Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.12281v1](<https://arxiv.org/abs/2602.12281v1>)
- **作者**: Jacky Kwok, Xilun Zhang, Mengdi Xu, Yuejiang Liu, Azalia Mirhoseini, Chelsea Finn, Marco Pavone
- **分类**: cs.RO
- **论文时间**: 2026-02-12T18:59:59Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.12281v1.pdf](<https://arxiv.org/pdf/2602.12281v1.pdf>)

## 来源摘要/节选

> The long-standing vision of general-purpose robots hinges on their ability to understand and act upon natural language instructions. Vision-Language-Action \(VLA\) models have made remarkable progress toward this goal, yet their generated actions can still misalign with the given instructions. In this paper, we investigate test-time verification as a means to shrink the "intention-action gap.'' We first characterize the test-time scaling law for embodied instruction following and demonstrate that jointly scaling the number of rephrased instructions and generated actions greatly increases test-time sample diversity, often recovering correct actions more efficiently than scaling each dimension independently. To capitalize on these scaling laws, we present CoVer, a contrastive verifier for vision-language-action alignment, and show that our architecture scales gracefully with additional computational resources and data. We then introduce "boot-time compute" and a hierarchical verification inference pipeline for VLAs. At deployment, our framework precomputes a diverse set of rephrased instructions from a Vision-Language-Model \(VLM\), repeatedly generates action candidates for each instruction, and then uses a verifier to select the optimal high-level prompt and low-level action chunks. Compared to scaling policy pre-training on the same data, our verification approach yields 22% gains in-distribution and 13% out-of-distribution on the SIMPLER benchmark, with a further 45% improvement in real-world experiments. On the PolaRiS benchmark, CoVer achieves 14% gains in task progress and 9% in success rate.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
