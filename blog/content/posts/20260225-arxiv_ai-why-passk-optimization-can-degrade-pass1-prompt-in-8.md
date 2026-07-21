---
title: 'Why Pass@k Optimization Can Degrade Pass@1: Prompt Interference in LLM Post-training'
date: 2026-02-25 23:30:40+08:00
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
external_url: https://arxiv.org/abs/2602.21189v1
aliases:
- /posts/20260226-arxiv_ai-why-passk-optimization-can-degrade-pass1-prompt-in-8/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:10bf531d3205e1745d8a9c3d6b88accdeeb5cfdd7c75a44dedb7dc5d671826ca
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 84
captured_at: '2026-07-18T04:17:01.203007Z'
source_capture_sha256: sha256:967dfee400388e16a54916e015b8054b2d0a82fe9f3a41aa4d152763fee02e84
source_capture_chars_original: 1309
source_publication_excerpt_chars: 1309
observation_id: obs_0b717423e44a437b2083c8d808b9637e0cbbc83b9deb388dc063c1f740b0a0be
revision_id: rev_9896cce97bfa63d6cc51cae67e1040c2ced145b7a7a4b1cb38d0d3731707950e
event_id: evt_33ce0c8662682afdb926a89abc596168d1b9b97498bf04aa0cc8d7e521cf6477
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-25T06:28:27Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.21189v1](<https://arxiv.org/abs/2602.21189v1>)
- **作者**: Anas Barakat, Souradip Chakraborty, Khushbu Pahwa, Amrit Singh Bedi
- **分类**: cs.LG
- **论文时间**: 2026-02-24T18:43:08Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.21189v1.pdf](<https://arxiv.org/pdf/2602.21189v1.pdf>)

## 来源摘要/节选

> Pass@k is a widely used performance metric for verifiable large language model tasks, including mathematical reasoning, code generation, and short-answer reasoning. It defines success if any of $k$ independently sampled solutions passes a verifier. This multi-sample inference metric has motivated inference-aware fine-tuning methods that directly optimize pass@$k$. However, prior work reports a recurring trade-off: pass@k improves while pass@1 degrades under such methods. This trade-off is practically important because pass@1 often remains a hard operational constraint due to latency and cost budgets, imperfect verifier coverage, and the need for a reliable single-shot fallback. We study the origin of this trade-off and provide a theoretical characterization of when pass@k policy optimization can reduce pass@1 through gradient conflict induced by prompt interference. We show that pass@$k$ policy gradients can conflict with pass@1 gradients because pass@$k$ optimization implicitly reweights prompts toward low-success prompts; when these prompts are what we term negatively interfering, their upweighting can rotate the pass@k update direction away from the pass@1 direction. We illustrate our theoretical findings with large language model experiments on verifiable mathematical reasoning tasks.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
