---
title: 'DanceOPD: On-Policy Generative Field Distillation'
date: 2026-06-26 22:27:03+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2606.27377v1
aliases:
- /posts/20260627-arxiv_ai-danceopd-on-policy-generative-field-distillation-0/
- /posts/20260628-arxiv_ai-danceopd-on-policy-generative-field-distillation-0/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:3d22377f903153f15550a335544bf0ccabf9b3b97ddf18ffc3ebc740e5b7704a
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 49
captured_at: '2026-07-18T04:30:14.398876Z'
source_capture_sha256: sha256:21773796b567fe65380cb1db0194d06caf53c01b438ab099dd8a24b611af3941
source_capture_chars_original: 1334
source_publication_excerpt_chars: 1334
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2606.27377v1](<https://arxiv.org/abs/2606.27377v1>)
- **作者**: Wei Zhou, Xiongwei Zhu, Zelin Xu, Bo Dong, Lixue Gong, Yongyuan Liang, Meng Chu, Leigang Qu, Lingdong Kong, Wei Liu, Tat-Seng Chua
- **分类**: cs.CV
- **论文时间**: 2026-06-25T17:59:58Z
- **论文 PDF**: [https://arxiv.org/pdf/2606.27377v1.pdf](<https://arxiv.org/pdf/2606.27377v1.pdf>)

## 来源摘要/节选

> Modern image generation demands a single model that unifies diverse capabilities, including text-to-image \(T2I\), local editing, and global editing. However, these capabilities are rarely naturally aligned and often conflict. For instance, editing tends to degrade T2I performance, while global and local editing interfere with each other. Consequently, effectively composing these capabilities has become a central challenge for image generation model training. To tackle this, we introduce DanceOPD, an on-policy generative field distillation framework for flow-matching models that routes each sample to one capability field, queries one low-noise student-induced state, and trains with a simple velocity MSE objective. With each capability source defined as a velocity field over the shared flow state space, the student learns from fields queried on its own rollout states to compose expert capabilities. This formulation also absorbs operator-defined fields such as classifier-free guidance. Comprehensive experiments on T2I, editing, realism-field absorption, and CFG absorption show that our approach improves multi-capability composition, strengthening target capabilities while preserving anchor generation quality. We believe this work establishes a practical route for generative field distillation in flow-matching models.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
