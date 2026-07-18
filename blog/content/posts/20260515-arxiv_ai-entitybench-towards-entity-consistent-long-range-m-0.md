---
title: 'EntityBench: Towards Entity-Consistent Long-Range Multi-Shot Video Generation'
date: 2026-05-15 23:06:43+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2605.15199v1
aliases:
- /posts/20260516-arxiv_ai-entitybench-towards-entity-consistent-long-range-m-0/
- /posts/20260517-arxiv_ai-entitybench-towards-entity-consistent-long-range-m-0/
- /posts/20260518-arxiv_ai-entitybench-towards-entity-consistent-long-range-m-0/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:68c628eb6b9e8b6c40b0ed0d9d8e2121aaadc31764633b2314853a305f991bdc
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 77
captured_at: '2026-07-18T04:29:39.576255Z'
source_capture_sha256: sha256:8e0deca56bb967be052c2fd2e2908ad90e73c20618dcee458f58ba7904a15525
source_capture_chars_original: 1491
source_publication_excerpt_chars: 1491
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2605.15199v1](<https://arxiv.org/abs/2605.15199v1>)
- **作者**: Ruozhen He, Meng Wei, Ziyan Yang, Vicente Ordonez
- **分类**: cs.CV
- **论文时间**: 2026-05-14T17:59:55Z
- **论文 PDF**: [https://arxiv.org/pdf/2605.15199v1.pdf](<https://arxiv.org/pdf/2605.15199v1.pdf>)

## 来源摘要/节选

> Multi-shot video generation extends single-shot generation to coherent visual narratives, yet maintaining consistent characters, objects, and locations across shots remains a challenge over long sequences. Existing evaluations typically use independently generated prompt sets with limited entity coverage and simple consistency metrics, making standardized comparison difficult. We introduce EntityBench, a benchmark of 140 episodes \(2,491 shots\) derived from real narrative media, with explicit per-shot entity schedules tracking characters, objects, and locations simultaneously across easy / medium / hard tiers of up to 50 shots, 13 cross-shot characters, 8 cross-shot locations, 22 cross-shot objects, and recurrence gaps spanning up to 48 shots. It is paired with a three-pillar evaluation suite that disentangles intra-shot quality, prompt-following alignment, and cross-shot consistency, with a fidelity gate that admits only accurate entity appearances into cross-shot scoring. As a baseline, we propose EntityMem, a memory-augmented generation system that stores verified per-entity visual references in a persistent memory bank before generation begins. Experiments show that cross-shot entity consistency degrades sharply with recurrence distance in existing methods, and that explicit per-entity memory yields the highest character fidelity \(Cohen's d = +2.33\) and presence among methods evaluated. Code and data are available at https://github.com/Catherine-R-He/EntityBench/.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
