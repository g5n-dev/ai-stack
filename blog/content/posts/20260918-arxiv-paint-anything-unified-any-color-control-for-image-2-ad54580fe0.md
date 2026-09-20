---
title: "Paint-Anything: Unified Any-Color Control for Image Generation and Editing"
date: 2026-09-18T22:34:39+08:00
draft: false
entry_kind: "auto"
tags: ["计算机视觉", "Prompt 工程", "cs.CV", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:74c506bd1b9b38a6902a75462baf45aedb78675c1ca5847bf622206f9fb86d00"
source_payload_sha256: "sha256:8b71c66f5abb9cb4859e88d0a30dcdaa4989fdb674d0427bed780890e2534943"
observation_id: obs_ad54580fe0ff774d14112aaa9e2262996d61872f75899f254334beafa6774742
event_id: evt_a666aee16fbc590c768480b4fc91803fa8c63cdc93d150e3f66b5006c4f5aae9
revision_id: rev_12dcbd9884970e956bc2dbe7c855c0cb735b185d47031a7851f2bbf922b5c360
source_published_at: 2026-09-17T17:59:30Z
first_seen_at: 2026-09-18T14:44:06Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 74
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2609.20816v1
parent_observation_id: null
last_seen_at: 2026-09-20T00:00:00Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.20816v1](http://arxiv.org/abs/2609.20816v1)
- **发布域名**: arxiv.org
- **分类**: cs.CV
- **作者**: Ji Xie、Dewei Zhou、Xinyu Huang 等

## 来源摘要/节选

> Professional design requires any-color control: the ability to specify an object's target color with any 24-bit hex value for image generation and editing. Prior work has explored color generation, editing, and colorization, but often relies on dedicated color representations or specialized inference procedures. Advances in large language models offer a simpler starting point: even compact models can associate hex values with color semantics. We present Paint-Anything, which learns a shared hex-prompt interface for generation and editing through object-level color supervision. We develop a data pipeline that constructs Paint-500K from real images through object grounding, perceptual color labeling, and editing-pair synthesis. Since shadows make real-image labels only approximate colors, we complement this supervision with pure-color anchors whose pixels exactly match their paired hex values. These anchors are used only at high-noise timesteps, leaving low-noise training to natural images. We further introduce Any Color Benchmark (ACBench), comprising ACBench-T2I and ACBench-Edit, to measure object-level hex color fidelity across both tasks. On FLUX.2-4B, Paint-Anything improves ACBench-T2I and ACBench-Edit scores by 85.3% and 28.3%, respectively, relative to the base model, with ablations supporting the training recipe. It also achieves the highest average CompColor score among the compared methods.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。