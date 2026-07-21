---
title: Diffusion-Pretrained Dense and Contextual Embeddings
date: 2026-02-12 23:40:07+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.11151v1
aliases:
- /posts/20260213-arxiv_ai-diffusion-pretrained-dense-and-contextual-embeddin-0/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:745c14555a08c86d759443d6078de5f616e284967044fbb82437e2bdbf48b59f
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 52
captured_at: '2026-07-18T04:14:55.115056Z'
source_capture_sha256: sha256:797dbff46b321a09a988f74da8ce6cab1016ec7b56bc2d3799575f313b1f467e
source_capture_chars_original: 1209
source_publication_excerpt_chars: 1209
observation_id: obs_b15662235dda040e933b248ec6262d88227fc11ad4050fef617ed13166786a78
revision_id: rev_a646f70bc24ac8335dd61a8922d5a5be6dccb64ae4e4920772ee8b7961c25ca3
event_id: evt_568189ac7cbd8617447309678ff7a342631ecbb4116f250ff926252300c74dc2
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-12T06:23:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.11151v1](<https://arxiv.org/abs/2602.11151v1>)
- **作者**: Sedigheh Eslami, Maksim Gaiduk, Markus Krimmel, Louis Milliken, Bo Wang, Denis Bykov
- **分类**: cs.LG
- **论文时间**: 2026-02-11T18:59:08Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.11151v1.pdf](<https://arxiv.org/pdf/2602.11151v1.pdf>)

## 来源摘要/节选

> In this report, we introduce pplx-embed, a family of multilingual embedding models that employ multi-stage contrastive learning on a diffusion-pretrained language model backbone for web-scale retrieval. By leveraging bidirectional attention through diffusion-based pretraining, our models capture comprehensive bidirectional context within passages, enabling the use of mean pooling and a late chunking strategy to better preserve global context across long documents. We release two model types: pplx-embed-v1 for standard retrieval, and pplx-embed-context-v1 for contextualized embeddings that incorporate global document context into passage representations. pplx-embed-v1 achieves competitive performance on the MTEB\(Multilingual, v2\), MTEB\(Code\), MIRACL, BERGEN, and ToolRet retrieval benchmarks, while pplx-embed-context-v1 sets new records on the ConTEB benchmark. Beyond public benchmarks, pplx-embed-v1 demonstrates strong performance on our internal evaluation suite, which focuses on real-world, large-scale search scenarios over tens of millions of documents. These results validate the models' effectiveness in production environments where retrieval quality and efficiency are critical at scale.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
