---
title: 'Introspective Coupling: Self-Explanation Training Tracks Behavioral Change
  Despite Fixed Supervision'
date: 2026-07-01 21:59:10+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2606.32038v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:6441d43dd27ce1b3b3f7e02d15a9425734bfd361ccfd7a7b40f60675e434bd74
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 100
captured_at: '2026-07-18T04:30:14.398876Z'
source_capture_sha256: sha256:ac0ebb49c387908406721723ff3ad612dec83883add1ba0ce518293e951273fc
source_capture_chars_original: 1333
source_publication_excerpt_chars: 1333
observation_id: obs_84759a74be1fd00e9b3f95d8081e01b14401d85250ff999ca79ff0efc385850b
revision_id: rev_3c2358953764f3c26edd2897677272823523a60d812e2252d536da829aad4e8a
event_id: evt_f12f50d293f2222f89a314b63ab289e48caf67a0b98df2c0036581ca4519713a
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-01T09:30:04Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2606.32038v1](<https://arxiv.org/abs/2606.32038v1>)
- **作者**: Zifan Carl Guo, Laura Ruis, Jacob Andreas, Belinda Z. Li
- **分类**: cs.CL
- **论文时间**: 2026-06-30T17:59:32Z
- **论文 PDF**: [https://arxiv.org/pdf/2606.32038v1.pdf](<https://arxiv.org/pdf/2606.32038v1.pdf>)

## 来源摘要/节选

> When does training language models \(LMs\) to generate explanations of their predictions yield faithful introspection, rather than superficial imitation? We study LMs trained to explain which features of their inputs influenced their behavior, using models' counterfactual behavior on modified inputs as supervision. Surprisingly, we find that LMs trained on fixed counterfactual explanations derived from earlier checkpoints of themselves, or even from behaviorally similar models in different families, frequently produce explanations more faithful to their own current behaviors than to those of their training targets. This "introspective" coupling between LM explanations and behaviors occurs when training explanations remain sufficiently correlated with current behaviors over the course of training, even as behaviors themselves shift. We also show that introspective coupling tracks behavior shifts: when explanation training is provided concurrently with other post-training objectives, explanations track those shifts without requiring updated supervision. This phenomenon appears in multiple tasks, including sycophancy and refusal, and is robust to label noise. Overall, our results show that even fixed datasets of counterfactual explanations can provide scalable and generalizable post-training signal for introspection.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
