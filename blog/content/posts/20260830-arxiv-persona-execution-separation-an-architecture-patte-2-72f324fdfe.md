---
title: "Persona-Execution Separation: An Architecture Pattern for Evolving LLM Agents under Execution Audit"
date: 2026-08-30T05:46:31+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "cs.SE", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:b9ae52718625d19e9ceb70f6bf98cd483a935890176a867a44eab8adfcdcfbba"
source_payload_sha256: "sha256:a45e08a5915b85f69bb9ed3efd25869f8ce619b3d4ce0f030b934e8f2eb25209"
observation_id: obs_72f324fdfe93557cb3f515d896515f8b4dd89cd89918462645cf9cfa4631d412
event_id: evt_637495a5a2c9fa4ce4a76f199fb07d61af7f791fc130d151695d2a66467e0b2c
revision_id: rev_01dd9b51ea102de1b0dd9c155de4917f5acaadcb81ead26c45c5324c2a4c23b1
source_published_at: 2026-08-27T17:50:07Z
first_seen_at: 2026-08-29T21:56:32Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 99
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2608.27427v1
parent_observation_id: null
last_seen_at: 2026-08-30T00:00:00Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.27427v1](http://arxiv.org/abs/2608.27427v1)
- **发布域名**: arxiv.org
- **分类**: cs.SE
- **作者**: Yisen Xi

## 来源摘要/节选

> Large language model (LLM) agents in governed organizations must let the persona (instructions, tone, self-presentation) evolve freely, while keeping execution (stateful, audited work) traceable. A single trust domain does not satisfy both cheaply. We present Persona-Execution Separation (PES): persona and execution reside in different trust domains, connected by a governed contract bridge. The persona is singly-homed and may drift; execution is faceless and audited. Status summaries may return; data bodies remain in the restrictive domain except a graded data-loss-prevention (DLP) exception; identity stays continuous. An approval matrix, DLP, and audit enforce the crossing. PES follows from three goals---free drift, execution traceability, and decoupling. Under LLM representational indistinguishability, any single-domain mechanism that meets all three must re-introduce typed change objects, an external gate, and a stable audit anchor: PES rebuilt at higher coupling cost. A development/pilot case in a regulated digital-employee platform records five decisions over one month, each with a rejected alternative. A mechanism check on the shipped implementation found no execution-side re-validation under persona perturbation (five model configurations) and no persona fingerprint on hard-asserted fields. A probe of a recovered pre-separation build found the governed execution path decoupled from the persona by omission, not by construction; a later wiring change could reverse that isolation, which PES makes an audited architectural rule. The pattern applies when multi-user deployment, execution audit, and expected persona churn hold jointly.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。