---
title: Endogenous Resistance to Activation Steering in Language Models
date: 2026-02-09 23:42:37+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
- 大语言模型
categories:
- 论文
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.06941v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:0f178d977ce0b1c0fa9c04e24b4c26aade0c58d618fdda0275d38641e1812a7b
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 63
captured_at: '2026-07-18T04:11:23.963527Z'
source_capture_sha256: sha256:22406359a99ede1a9b5ee4158911e4e45b93e6f139a72a38ec51e4868eae2c4e
source_capture_chars_original: 1425
source_publication_excerpt_chars: 1425
observation_id: obs_3b49183eee78aa3d70078b6e222dfb6a763b667c141757ef91851a7a91f72e40
revision_id: rev_cc9d03636a549cb1416957278df446cb1d33ddd02d90156c01d3b8f92cddbbcc
event_id: evt_7eaa3741ef7968bd7c238c5582a55346225557afd5b96b49d8a1b2f6a8f30c6d
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.06941v1](<https://arxiv.org/abs/2602.06941v1>)
- **作者**: Alex McKenzie, Keenan Pepper, Stijn Servaes, Martin Leitgab, Murat Cubuktepe, Mike Vaiana, Diogo de Lucena, Judd Rosenblatt, Michael S. A. Graziano
- **分类**: cs.LG
- **论文时间**: 2026-02-06T18:41:12Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.06941v1.pdf](<https://arxiv.org/pdf/2602.06941v1.pdf>)

## 来源摘要/节选

> Large language models can resist task-misaligned activation steering during inference, sometimes recovering mid-generation to produce improved responses even when steering remains active. We term this Endogenous Steering Resistance \(ESR\). Using sparse autoencoder \(SAE\) latents to steer model activations, we find that Llama-3.3-70B shows substantial ESR, while smaller models from the Llama-3 and Gemma-2 families exhibit the phenomenon less frequently. We identify 26 SAE latents that activate differentially during off-topic content and are causally linked to ESR in Llama-3.3-70B. Zero-ablating these latents reduces the multi-attempt rate by 25%, providing causal evidence for dedicated internal consistency-checking circuits. We demonstrate that ESR can be deliberately enhanced through both prompting and training: meta-prompts instructing the model to self-monitor increase the multi-attempt rate by 4x for Llama-3.3-70B, and fine-tuning on self-correction examples successfully induces ESR-like behavior in smaller models. These findings have dual implications: ESR could protect against adversarial manipulation but might also interfere with beneficial safety interventions that rely on activation steering. Understanding and controlling these resistance mechanisms is important for developing transparent and controllable AI systems. Code is available at github.com/agencyenterprise/endogenous-steering-resistance.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
