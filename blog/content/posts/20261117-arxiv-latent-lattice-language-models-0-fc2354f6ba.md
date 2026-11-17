---
title: "Latent Lattice Language Models"
date: 2026-11-17T21:23:27+08:00
draft: false
entry_kind: "auto"
tags: ["AI", "cs.LG", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:4dd084e2386a9bf2d9834b6626fd5b7920871d59762ff18f8a6cbe832aa0be30"
source_payload_sha256: "sha256:25c260831bca048555f935f459001e9469aa3fce1d861f68a266e7235439dd1b"
observation_id: obs_fc2354f6bafffb995691208c7ec027fe80c78eaebcca5dd1ca9faed4a9a97fe2
event_id: evt_17b7b456c5b135316b9cd08365bb74028038589bfcf45c5d779bc18caa4d1a9b
revision_id: rev_e0cf1ba794c7b6b43d333b973dc72124250ee8f40a898e6a77b16720b0ae5840
source_published_at: 2026-11-16T18:59:38Z
first_seen_at: 2026-11-17T13:31:48Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 30
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2611.21608v1
parent_observation_id: null
last_seen_at: 2026-11-17T13:22:09.340207Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2611.21608v1](http://arxiv.org/abs/2611.21608v1)
- **发布域名**: arxiv.org
- **分类**: cs.LG
- **作者**: Shivam Duggal、Zongze Wu、William T. Freeman 等

## 来源摘要/节选

> Language models typically increase per-token computation through deeper or looped layers and latent reasoning steps, while richer residual connections improve information flow across layers. We instead increase computational capacity: the number of active computational states a model maintains. We introduce the Lattice of Latents, a set of per-layer horizontal latent streams that run recurrently along time, alongside the vertical residual stream that flows through depth. Like hyper-connections, mHC, and attention or value residuals, the Lattice enhances the residual stream, but rather than adding or rerouting residual pathways through depth, it provides companion computational states that persist across tokens. Unlike hybrid Transformer-SSM architectures, whose recurrent states primarily serve as internal memory for sequence mixing, these latents directly condition the vertical stream's attention, KV-cache writes, MLP computation, and decoding. On Transformers trained on 20B FineWeb-Edu tokens, a 406M-parameter Lattice model lowers validation perplexity from 15.41 to 14.40 over a parameter-matched Transformer. These gains extend across architectural variants. The Lattice composes with prior residual-stream enhancements: with hyper-connections and input residuals, it lowers validation perplexity from 15.41 (base Transformer) and 14.22 (Transformer with the same enhancements) to 13.61. On Gated DeltaNet, Mamba-2, Triadic GDN, and GDN-Mamba-2 hybrids, it improves perplexity at every tested native state size, with Lattice-GDN and Lattice-Triadic-GDN variants outperforming pure baselines with 4x larger native states. These results identify persistent per-layer state as a complementary axis for scaling language-model computation.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。