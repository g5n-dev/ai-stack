---
title: 'DySCO: Dynamic Attention-Scaling Decoding for Long-Context LMs'
date: 2026-02-26 23:29:19+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.22175v1
aliases:
- /posts/20260227-arxiv_ai-dysco-dynamic-attention-scaling-decoding-for-long--8/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:a4c75639af769bac17e340734e7bf62fb8466b80e960c207818d2989ffe37307
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 62
captured_at: '2026-07-18T04:17:01.203007Z'
source_capture_sha256: sha256:74e4e41cc79a6637628a266b48f4b6ee660ee2ebf74b630558ff3bba8aa360fc
source_capture_chars_original: 1362
source_publication_excerpt_chars: 1362
observation_id: obs_23c167e382dd8506798ee82396c25a3e6df133d353eb32891df9639d3ec457f4
revision_id: rev_7c33e15c1fd99613d70b513e296c6360c85e3f3a7ad5b950004df0adb437f3b2
event_id: evt_1e8e7d739d92f984c9c13999454201f20ef59f6dde854ff513ebff821aec3009
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-26T06:26:37Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.22175v1](<https://arxiv.org/abs/2602.22175v1>)
- **作者**: Xi Ye, Wuwei Zhang, Fangcong Yin, Howard Yen, Danqi Chen
- **分类**: cs.CL
- **论文时间**: 2026-02-25T18:21:35Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.22175v1.pdf](<https://arxiv.org/pdf/2602.22175v1.pdf>)

## 来源摘要/节选

> Understanding and reasoning over long contexts is a crucial capability for language models \(LMs\). Although recent models support increasingly long context windows, their accuracy often deteriorates as input length grows. In practice, models often struggle to keep attention aligned with the most relevant context throughout decoding. In this work, we propose DySCO, a novel decoding algorithm for improving long-context reasoning. DySCO leverages retrieval heads--a subset of attention heads specialized for long-context retrieval--to identify task-relevant tokens at each decoding step and explicitly up-weight them. By doing so, DySCO dynamically adjusts attention during generation to better utilize relevant context. The method is training-free and can be applied directly to any off-the-shelf LMs. Across multiple instruction-tuned and reasoning models, DySCO consistently improves performance on challenging long-context reasoning benchmarks, yielding relative gains of up to 25% on MRCR and LongBenchV2 at 128K context length with modest additional compute. Further analysis highlights the importance of both dynamic attention rescaling and retrieval-head-guided selection for the effectiveness of the method, while providing interpretability insights into decoding-time attention behavior. Our code is available at https://github.com/princeton-pli/DySCO.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
