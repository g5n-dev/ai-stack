---
title: 'MEG-XL: Data-Efficient Brain-to-Text via Long-Context Pre-Training'
date: 2026-02-03 23:08:59+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.02494v1
aliases:
- /posts/20260204-arxiv_ai-meg-xl-data-efficient-brain-to-text-via-long-conte-1/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:4fff94fb32c3adcbf2f89f86106ce8ef35797a72184db14d80e2c9931d128b36
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 66
captured_at: '2026-07-18T04:10:26.671991Z'
source_capture_sha256: sha256:db47c59227d7ce788f856de9d7d9dce9b512b380fc0f498b49abcd4528d4f077
source_capture_chars_original: 1105
source_publication_excerpt_chars: 1105
observation_id: obs_52603399ba22baaf623dffb6362bdf1850f1b9a77d17da4010b622adf5a4447a
revision_id: rev_12460bbe3a7d597e18f2f20189d6869e3590b0d473ef37e3fc4f29e4f487bdc4
event_id: evt_51ecced2fc0db59343f37a2aafffe174c5f981b37a845f55b954047cd0eb8a77
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-03T05:27:06Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.02494v1](<https://arxiv.org/abs/2602.02494v1>)
- **作者**: Dulhan Jayalath, Oiwi Parker Jones
- **分类**: cs.LG
- **论文时间**: 2026-02-02T18:59:50Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.02494v1.pdf](<https://arxiv.org/pdf/2602.02494v1.pdf>)

## 来源摘要/节选

> Clinical brain-to-text interfaces are designed for paralysed patients who cannot provide extensive training recordings. Pre-training improves data-efficient generalisation by learning statistical priors across subjects, but these priors critically depend on context. While natural speech might unfold gradually over minutes, most methods pre-train with only a few seconds of context. Thus, we propose MEG-XL, a model pre-trained with 2.5 minutes of MEG context per sample, 5-300x longer than prior work, and equivalent to 191k tokens, capturing extended neural context. Fine-tuning on the task of word decoding from brain data, MEG-XL matches supervised performance with a fraction of the data \(e.g. 1hr vs 50hrs\) and outperforms brain foundation models. We find that models pre-trained with longer contexts learn representations that transfer better to word decoding. Our results indicate that long-context pre-training helps exploit extended neural context that other methods unnecessarily discard. Code, model weights, and instructions are available at https://github.com/neural-processing-lab/MEG-XL .

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
