---
title: "VetClaw: An Edge-Cloud Multimodal Agentic System for Veterinary Disease Screening"
date: 2026-07-29T20:25:10+08:00
draft: false
entry_kind: "auto"
tags: ["AI Agent", "计算机视觉", "cs.CV", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:3b163d128f95c6f4f3eed31b5b6b0bbb3f34da75b4e8d93d1e5a66effdc7649f"
source_payload_sha256: "sha256:f5458048907c89552fc6ead3efe26ef8701acf6dbad360380092bbdc621ae171"
observation_id: obs_9a501e20b0b4f19a3d9b522c92a85dcdd49f491ee0c701413fcd985c147c83a0
event_id: evt_3301f0866c15ee46e1578c3f8d879832683bcfbfc42e7dcd10a45e9cd0e22327
revision_id: rev_63b6638b0e9f44a7eab7086c64c5e5de7f2c3f23ac7e8a439ffea2f9f82076ae
source_published_at: 2026-07-28T17:50:25Z
first_seen_at: 2026-07-29T12:41:00Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 81
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2607.26042v1
parent_observation_id: null
last_seen_at: 2026-07-29T12:23:49.127933Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2607.26042v1](http://arxiv.org/abs/2607.26042v1)

## 来源摘要/节选

> We present VetClaw, an edge-cloud multimodal agentic system for early veterinary disease screening. VetClaw uses a camera module as an edge sensing device and sends captured images, together with optional symptom descriptions, to a server-hosted vision-language model for zero-shot disease classification. The system separates agent interaction from workflow orchestration: OpenClaw provides scheduling, tool access, user interaction, and notification services on the edge device, while LangGraph manages the stateful screening workflow, including input validation, image transmission, model invocation, safety checks, conditional routing, failure handling, and structured logging. This design moves beyond static image classification by enabling the system to collect visual evidence, invoke external models, apply deterministic safety rules, and generate diagnostic-support alerts. Results show that image-only VLM prediction remains limited, whereas symptom-guided and multimodal inputs improve zero-shot classification performance. Thus, VetClaw transforms a static prediction model into a coordinated, safety-aware system that can use tools, manage workflows, handle failures, and escalate uncertain cases.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。