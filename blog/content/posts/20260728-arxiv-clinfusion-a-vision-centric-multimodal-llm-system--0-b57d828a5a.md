---
title: "ClinFusion: A Vision-Centric Multimodal LLM System for Holistic Medical Understanding"
date: 2026-07-28T11:40:08+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "计算机视觉", "cs.CV", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:e60e7eb7a3e3099085324aff035d038c1cb889601e8c86d0f854303d5f5e9e1e"
source_payload_sha256: "sha256:ead0e121038e742d2693a881ada362195f8715f4ded5287bb5243b3b43a88f71"
observation_id: obs_b57d828a5ad1224c768f8f2953aecf5e345fc9dd2bc7fc05163304aef6d9fba6
event_id: evt_d31126d7dadd4c55e04b2e1b0a3f0dc3f8eebd5fb7f75d028e85c1e6541b2c11
revision_id: rev_c23bd998cc31767ed150cdd79cc9c2e4d5253b28cfa0aa7256cf9a24aabfbb68
source_published_at: 2026-07-27T17:59:49Z
first_seen_at: 2026-07-28T03:55:33Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 85
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2607.24743v1
parent_observation_id: null
last_seen_at: 2026-07-29T00:00:00Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2607.24743v1](http://arxiv.org/abs/2607.24743v1)

## 来源摘要/节选

> Multimodal large language models (MLLMs) hold immense potential to revolutionize clinical practice, yet deploying them in the medical domain is fundamentally a vision-centric challenge: models must absorb knowledge from heterogeneous 2D and 3D medical images, and evaluation protocols must align with radiologists' clinical practice and provide an accurate, fine-grained and factualness-driven assessment. In this paper, we introduce ClinFusion, a vision-centric MLLM designed for holistic medical understanding that systematically addresses these limitations. We propose a compositional and cascaded vision encoder architecture featuring a Cascade Spatial-Aware Locality Fusion operator that unifies diverse 2D and native 3D medical image understanding within a fused encoder. We further introduce a vision-grounded evaluation framework, including MedIF-Bench for instruction-following assessment and a region-of-interest-grounded method for clinically aligned and factualness-driven report generation evaluation. We show that ClinFusion sets a new state-of-the-art across a comprehensive suite of 2D and 3D multimodal medical benchmarks---spanning visual question answering, report generation, and instruction following---as well as textual medical tasks, outperforming leading open-source medical MLLMs (\textit{e.g.}, Hulu-Med, Lingshu) on 20 out of 24 benchmarks and demonstrating multimodal capabilities better than powerful proprietary models such as GPT-5.2 and Gemini-3-Flash on 13 out of 16 benchmarks, and can be further augmented with agentic tool use for retrieval-augmented and tool-assisted clinical workflows. A blinded evaluation by board-certified radiologists confirms that ClinFusion produces the highest-ranked reports, and validates our RoI-grounded metric as achieving the strongest correlation with expert judgment among all automatic evaluation metrics examined.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。