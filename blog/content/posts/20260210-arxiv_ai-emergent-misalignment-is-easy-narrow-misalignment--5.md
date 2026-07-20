---
title: Emergent Misalignment is Easy, Narrow Misalignment is Hard
date: 2026-02-10 03:34:40+08:00
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
external_url: https://arxiv.org/abs/2602.07852v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:d73c821cf59962c275c5f9592e78332e8142f623d81bdc0f7bd9e9450a028e26
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 58
captured_at: '2026-07-18T04:14:24.737190Z'
source_capture_sha256: sha256:a5276c3c04d7252c747f360b66bb42ee281ef24ea736e239266a4d0bd2f9b95f
source_capture_chars_original: 1381
source_publication_excerpt_chars: 1381
observation_id: obs_959b0cc0fec3930334c35bc09ec48ace4f479318d56b5ec8b6de1221c4fb1cc0
revision_id: rev_f55d074b694ececbc0bd91020beab7308d60a9c4445c6d4e659e16320953d9a3
event_id: evt_6d6ad679c1dd665091a98ef7f888e6f16899adafe44862937ff6908ec417128a
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.07852v1](<https://arxiv.org/abs/2602.07852v1>)
- **作者**: Anna Soligo, Edward Turner, Senthooran Rajamanoharan, Neel Nanda
- **分类**: cs.AI
- **论文时间**: 2026-02-08T07:50:04Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.07852v1.pdf](<https://arxiv.org/pdf/2602.07852v1.pdf>)

## 来源摘要/节选

> Finetuning large language models on narrowly harmful datasets can cause them to become emergently misaligned, giving stereotypically \`evil' responses across diverse unrelated settings. Concerningly, a pre-registered survey of experts failed to predict this result, highlighting our poor understanding of the inductive biases governing learning and generalisation in LLMs. We use emergent misalignment \(EM\) as a case study to investigate these inductive biases and find that models can just learn the narrow dataset task, but that the general solution appears to be more stable and more efficient. To establish this, we build on the result that different EM finetunes converge to the same linear representation of general misalignment, which can be used to mediate misaligned behaviour. We find a linear representation of the narrow solution also exists, and can be learned by introducing a KL divergence loss. Comparing these representations reveals that general misalignment achieves lower loss, is more robust to perturbations, and is more influential in the pre-training distribution. This work isolates a concrete representation of general misalignment for monitoring and mitigation. More broadly, it offers a detailed case study and preliminary metrics for investigating how inductive biases shape generalisation in LLMs. We open-source all code, datasets and model finetunes.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
