---
title: "Rethinking Heterogeneous System Disaggregation for Subquadratic Attention"
date: 2026-09-15T06:33:03+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "cs.AI", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:e05bdf104dcf30fd7a5d156306210369bdea1016f14e4823c3869f3c8c0ecea5"
source_payload_sha256: "sha256:852ce30b5a2489f7926c017abb69c697c20bcbacd1be306a72ba8418a0fcca83"
observation_id: obs_6855f5217cba444ae69107932d6bcf6bdde8b1f9bfb4ab4da481b1896141b182
event_id: evt_2912057886875f198a986e851eb2f4090815254ddf21a293b574bc67f0882562
revision_id: rev_e316a85beefa17cc3156fdeb60478f7252c5583e6110bf4c4a183f92dfdbd8bf
source_published_at: 2026-09-11T17:55:45Z
first_seen_at: 2026-09-14T22:30:32.389781Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 73
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2609.13134v1
parent_observation_id: null
last_seen_at: 2026-09-14T22:30:32.389781Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.13134v1](http://arxiv.org/abs/2609.13134v1)
- **发布域名**: arxiv.org
- **分类**: cs.AI
- **作者**: Arya Tschand、Yaosheng Fu、Vikram Sharma Mailthody 等

## 来源摘要/节选

> Frontier language models are more aggressively using subquadratic attention to reduce the memory footprint and compute requirements during inference while still delivering frontier accuracy. While existing systems make dense attention-centric disaggregated serving decisions, we show that disaggregating inference around the unique arithmetic intensity and memory footprint of subquadratic attention LLMs can achieve significant throughput and energy efficiency gains on emerging DRAM-based and SRAM-only heterogeneous systems.
> We introduce SQD (SubQuadratic Disaggregation), a fine-grained heterogeneous disaggregation scheme that splits decode by quadratic and subquadratic attention rather than by operator type, and that applies across subquadratic attention variants. For sparse attention LLMs, we disaggregate decode into top-k selection, which must index through the full KV, and top-k attention plus FFN, which have static memory footprints. For linear and sliding-window attention LLMs, we disaggregate decode into dense attention layers and subquadratic attention layers plus FFN. In an adjusted 8xB200 heterogeneous system proxy, we observe average tokens/J improvements of 53% on GLM 5.2, 31% on Nemotron 3 Ultra, and 56% on Gemma 4 31B over the strongest GPU-only baselines. In an analytical model of a Rubin plus LPX system with fixed power budgets, we observe 1.2x to 1.5x tighter achievable latencies and up to 3.6x higher throughput over the best baseline of attention-FFN disaggregation. Our experiments also reveal architectural insights on chip and interconnect provisioning for next-generation heterogeneous systems serving subquadratic attention.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。