---
title: "AVA-Encoder: Towards Agent-Native Video Representation Learning"
date: 2026-08-13T10:48:37+08:00
draft: false
entry_kind: "auto"
tags: ["AI Agent", "计算机视觉", "Prompt 工程", "cs.CV", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:5f12e2f4cd0d7d1eb70da993038690c3c0acd1639e185001150ddc02b02e49dc"
source_payload_sha256: "sha256:509c8132976c914ebdddfb0fb763c19b15e429b80218fa2e36fdc4fe70e16a63"
observation_id: obs_be22f6b56997c6350f914eb52fabe1751af2cad1a221f973d8d649af5a55f207
event_id: evt_4aa18c2e7f2864633b6e4cb5ee32e1efed27d66303430eece15779efeaea3e30
revision_id: rev_bdd471a8195ab9ffdd0a13420eb0be88d4eadcc45d4719440e96714ead455954
source_published_at: 2026-08-12T17:58:02Z
first_seen_at: 2026-08-13T17:12:00.783245Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 63
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2608.12313v1
parent_observation_id: null
last_seen_at: 2026-08-13T02:46:36.401928Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.12313v1](http://arxiv.org/abs/2608.12313v1)
- **发布域名**: arxiv.org
- **分类**: cs.CV
- **作者**: Chuyue Li、Jinpeng Yu、Haozhe Wang 等

## 来源摘要/节选

> Creative agents still lack an effective way to learn from high-quality human films, limiting their ability to produce cinematic-grade videos. A key challenge is the absence of a structured video representation that is both faithful to film content and directly usable for agentic reasoning and manipulation. To address the challenge, we propose the Agentic Video Auto-Encoder (AVA-Encoder), a framework for learning agent-native video representations via agentic auto-encoding.
> AVA-Encoder transforms a video into a knowledge graph (KG) representation and then reconstructs it back into video. Its hierarchy and state nodes store structured text, while a linked asset layer holds generated images, audio, and video. Typed edges preserve the relations between these text descriptions and assets in a form that agents can easily understand, query, and edit. The video reconstruction differences drive a textual-gradient optimization framework, which expresses evaluation feedback as natural-language update directions for Data-Independent Encoding Policy Pseudo-Training in the outer loop and optional Data-Dependent KG Representation Refinement in the test-time inner loop.
> Extensive experiments show that AVA-Encoder improves by 20.7 percentage points over the strongest external baseline. In the controlled policy-only setting, its pseudo-trained shot-level Agentic Video Encoder policy also outperforms a carefully human-tuned policy while using 74.3% fewer system-prompt tokens. We release the complete AVA-Encoder framework, a reliable agentic video reconstruction benchmark, and the first dataset of high-quality film KG representations.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。