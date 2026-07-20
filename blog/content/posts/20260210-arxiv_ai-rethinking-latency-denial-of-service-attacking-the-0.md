---
title: 'Rethinking Latency Denial-of-Service: Attacking the LLM Serving Framework,
  Not the Model'
date: 2026-02-10 03:34:40+08:00
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
external_url: https://arxiv.org/abs/2602.07878v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:6b997e1cc05454b0d42605fc706e918d6d043256fd73d118564d42df04cf6d3d
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 88
captured_at: '2026-07-18T04:14:28.443184Z'
source_capture_sha256: sha256:a330256127c10ddca11c57d87502e16f9953c10678c5e3209c0fb6e840331ae4
source_capture_chars_original: 1462
source_publication_excerpt_chars: 1462
observation_id: obs_c365cfddb04079b7f6b3dde4c529b9df59c0632e200175d990f4c5aa2d99ecac
revision_id: rev_2d4bc4b8f7e68b9b2c37a6a320f2e35372e92bce67110c31f476ffb08e4522ec
event_id: evt_898fecd99c68ca0896661ee2af4129c4fc802c695fb87e4a8025d402d9158835
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.07878v1](<https://arxiv.org/abs/2602.07878v1>)
- **作者**: Tianyi Wang, Huawei Fan, Yuanchao Shu, Peng Cheng, Cong Wang
- **分类**: cs.CR
- **论文时间**: 2026-02-08T09:05:54Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.07878v1.pdf](<https://arxiv.org/pdf/2602.07878v1.pdf>)

## 来源摘要/节选

> Large Language Models face an emerging and critical threat known as latency attacks. Because LLM inference is inherently expensive, even modest slowdowns can translate into substantial operating costs and severe availability risks. Recently, a growing body of research has focused on algorithmic complexity attacks by crafting inputs to trigger worst-case output lengths. However, we report a counter-intuitive finding that these algorithmic latency attacks are largely ineffective against modern LLM serving systems. We reveal that system-level optimization such as continuous batching provides a logical isolation to mitigate contagious latency impact on co-located users. To this end, in this paper, we shift the focus from the algorithm to the system layer, and introduce a new Fill and Squeeze attack strategy targeting the state transition of the scheduler. "Fill" first exhausts the global KV cache to induce Head-of-Line blocking, while "Squeeze" forces the system into repetitive preemption. By manipulating output lengths using methods from simple plain-text prompts to more complex prompt engineering, and leveraging side-channel probing of memory status, we demonstrate that the attack can be orchestrated in a black-box setting with much less cost. Extensive evaluations indicate by up to 20-280x average slowdown on Time to First Token and 1.5-4x average slowdown on Time Per Output Token compared to existing attacks with 30-40% lower attack cost.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
