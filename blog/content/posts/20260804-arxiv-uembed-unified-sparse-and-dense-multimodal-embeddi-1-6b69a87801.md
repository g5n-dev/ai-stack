---
title: "UEmbed: Unified Sparse and Dense Multimodal Embeddings"
date: 2026-08-04T23:37:23+08:00
draft: false
entry_kind: "auto"
tags: ["计算机视觉", "cs.CV", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:5797b576090a05c58a51d877ccde5c4d09f89bcdcaa0097dfb215459712f5bfd"
source_payload_sha256: "sha256:af86647a2587df1860848a3db43c811ed29f63c9d1405472efc953ac83466f71"
observation_id: obs_6b69a87801ae94526d29e586a46d4d158cb527e03f611246a49056c1169239b5
event_id: evt_befc6448454842e331353732e5c7f2b1e294f82809e6424508edc41ef9583f3e
revision_id: rev_69ec9e4d6dd55be9206c87cc8f295d7c2816cc9dd3c80d345018609942b0682a
source_published_at: 2026-08-03T17:54:11Z
first_seen_at: 2026-08-04T15:46:26Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 54
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2608.02583v1
parent_observation_id: null
last_seen_at: 2026-08-04T15:35:07.571691Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.02583v1](http://arxiv.org/abs/2608.02583v1)
- **发布域名**: arxiv.org
- **分类**: cs.CV
- **作者**: Tingyu Song、Mingxin Li、Yanzhao Zhang 等

## 来源摘要/节选

> Sparse retrieval underpins modern search systems, from web search to retrieval-augmented generation. Existing work has introduced Learned Sparse Retrieval (LSR) to push beyond exact lexical matching toward richer semantics. Yet LSR has so far remained tied to encoder-style bidirectional architectures, and its extension to multimodal settings still relies heavily on auxiliary cross-modal modules. To address these limitations, we introduce UEmbed (Unified Embedding), a decoder-only multimodal embedding model that produces both sparse lexical and dense representations in one causal forward pass. UEmbed appends N learnable special tokens to the input and partitions the vocabulary into N disjoint subsets. Each token's causal hidden state predicts sparse weights over its assigned subset, and the N subsets are concatenated into the full sparse vector. Trained on public data, we release UEmbed at 2B, 4B, and 9B scales. UEmbed-9B reaches 71.8 (dense) and 71.0 (sparse) on MMEB-v2, outperforming multimodal embedding models trained on publicly available data (e.g., RzenEmbed). On BEIR, UEmbed also remains competitive with strong dense and sparse baselines. Furthermore, we demonstrate the practical utility of UEmbed across three dimensions: effectiveness, efficiency, and agentic applications. Overall, UEmbed offers a new paradigm: it unifies dense and sparse embeddings in one model, while further extending sparse retrieval to unify text and multimodal inputs.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。