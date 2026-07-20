---
title: 'Agency and Architectural Limits: Why Optimization-Based Systems Cannot Be
  Norm-Responsive'
date: 2026-02-27 02:54:04+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
- AI Agent
- 大语言模型
categories:
- 论文
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.23239v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:b6f1398f002c4eea651e939e495ed4c556488f87293434b7f45d3ae391536976
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 89
captured_at: '2026-07-18T04:30:37.182965Z'
source_capture_sha256: sha256:38dbb0261c64d5f09b5428b1e70b6c617cbb9b19442103d481cbf1b413a37410
source_capture_chars_original: 1914
source_publication_excerpt_chars: 1914
observation_id: obs_dca1bcbd72715e53f27b22622a30533346e17c6e7dc75df092eaec0eaa3a8f6d
revision_id: rev_8f075faceab69eb99309f0083a9d85f6b3d6686eb1b400cfb291dec87e8507ea
event_id: evt_9a86fb22dc65f8021c4e776d794d71458144b2fde8d39ec518dee4f7d39f4725
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.23239v1](<https://arxiv.org/abs/2602.23239v1>)
- **作者**: Radha Sarma
- **分类**: cs.AI
- **论文时间**: 2026-02-26T17:16:17Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.23239v1.pdf](<https://arxiv.org/pdf/2602.23239v1.pdf>)

## 来源摘要/节选

> AI systems are increasingly deployed in high-stakes contexts -- medical diagnosis, legal research, financial analysis -- under the assumption they can be governed by norms. This paper demonstrates that assumption is formally invalid for optimization-based systems, specifically Large Language Models trained via Reinforcement Learning from Human Feedback \(RLHF\). We establish that genuine agency requires two necessary and jointly sufficient architectural conditions: the capacity to maintain certain boundaries as non-negotiable constraints rather than tradeable weights \(Incommensurability\), and a non-inferential mechanism capable of suspending processing when those boundaries are threatened \(Apophatic Responsiveness\). These conditions apply across all normative domains. RLHF-based systems are constitutively incompatible with both conditions. The operations that make optimization powerful -- unifying all values on a scalar metric and always selecting the highest-scoring output -- are precisely the operations that preclude normative governance. This incompatibility is not a correctable training bug awaiting a technical fix; it is a formal constraint inherent to what optimization is. Consequently, documented failure modes - sycophancy, hallucination, and unfaithful reasoning - are not accidents but structural manifestations. Misaligned deployment triggers a second-order risk we term the Convergence Crisis: when humans are forced to verify AI outputs under metric pressure, they degrade from genuine agents into criteria-checking optimizers, eliminating the only component in the system capable of normative accountability. Beyond the incompatibility proof, the paper's primary positive contribution is a substrate-neutral architectural specification defining what any system -- biological, artificial, or institutional -- must satisfy to qualify as an agent rather than a sophisticated instrument.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
