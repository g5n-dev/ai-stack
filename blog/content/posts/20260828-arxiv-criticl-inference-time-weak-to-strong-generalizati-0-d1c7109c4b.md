---
title: "CritICL: Inference-Time Weak-to-Strong Generalization from Small Language Model Failure Modes"
date: 2026-08-28T13:28:33+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "cs.CL", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:2e20af74cb4952fd858c84095c1db963c393808637e8ed84b37ed4ee33aa19c3"
source_payload_sha256: "sha256:0e580e980c7b32c784779ed2b861e429fe08e5ebee2b620d03a9f4cc33585504"
observation_id: obs_d1c7109c4b997a2e3a61be68890091763be84ad89f6b3bf287eedb79e6c41253
event_id: evt_bf58e0d25dc9abf5237155b9cb03e67a0716a48ccc3afce5c9da7dbb0854594d
revision_id: rev_bb0cea723847dec363923fa119acd6490ba4e50413dfefe1a5f7b7fe013eae7d
source_published_at: 2026-08-27T17:59:30Z
first_seen_at: 2026-08-28T05:38:17Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 93
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2608.27455v1
parent_observation_id: null
last_seen_at: 2026-08-28T05:23:34.626108Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.27455v1](http://arxiv.org/abs/2608.27455v1)
- **发布域名**: arxiv.org
- **分类**: cs.CL
- **作者**: Yufan Wu、Yinghui He、Zhengyi Hu 等

## 来源摘要/节选

> Recent advances in inference-time scaling have significantly improved the reasoning performance of large language models (LLMs). However, these methods typically rely on repeated generation or external verification. To address this limitation, we introduce CritICL, a novel inference-time framework that improves reasoning while maintaining high efficiency. Our key insight is that LLM failure modes exhibit structured patterns across model scales within the same family. Instead of treating failures as undesirable outputs, CritICL leverages them as a source of guidance. Specifically, we utilize failure modes derived from weaker models and incorporate them into inference through critique-based in-context examples. We propose two variants: CritICL-dynamic, which adaptively predicts input-specific failure modes and retrieves critiques, and CritICL-static, which uses a global failure mode profile to provide stable guidance. Experimental results show that CritICL consistently outperforms standard in-context learning and achieves performance competitive with or superior to test-time scaling methods, while requiring significantly fewer generations and lower token cost. Code available at: https://github.com/umwyf/CRITICL

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。