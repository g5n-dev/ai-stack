---
title: Adaptive Block-Scaled Data Types
date: 2026-03-31 11:59:35+08:00
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
external_url: https://arxiv.org/abs/2603.28765v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:61c7a0e2099801b4f2353b4c9350dcde251510bd9d829e7bdc6cbf21e8301612
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 32
captured_at: '2026-07-18T04:29:04.624314Z'
source_capture_sha256: sha256:3a70a3190b6c597e8fbbbc9abc2806816c6eb97aac7e9ff4306bae2edbd1571e
source_capture_chars_original: 1442
source_publication_excerpt_chars: 1442
observation_id: obs_6adfd16cc130d90fc04b5f97302d9ed0add9472badd02896226a5efd3ceda2fd
revision_id: rev_dfaf2d69d8eaf77cce28588b428b5745f7e495cc6bee22e70738d918ee4ca5c3
event_id: evt_ca6524b184962644f772e6968c426779a4d591341f4949a614503b896ee9d5d8
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-03-31T12:33:27Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.28765v1](<https://arxiv.org/abs/2603.28765v1>)
- **作者**: Jack Cook, Hyemin S. Lee, Kathryn Le, Junxian Guo, Giovanni Traverso, Anantha P. Chandrakasan, Song Han
- **分类**: cs.CL
- **论文时间**: 2026-03-30T17:59:33Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.28765v1.pdf](<https://arxiv.org/pdf/2603.28765v1.pdf>)

## 来源摘要/节选

> NVFP4 has grown increasingly popular as a 4-bit format for quantizing large language models due to its hardware support and its ability to retain useful information with relatively few bits per parameter. However, the format is not without limitations: recent work has shown that NVFP4 suffers from its error distribution, resulting in large amounts of quantization error on near-maximal values in each group of 16 values. In this work, we leverage this insight to design new Adaptive Block-Scaled Data Types that can adapt to the distribution of their input values. For four-bit quantization, our proposed IF4 \(Int/Float 4\) data type selects between FP4 and INT4 representations for each group of 16 values, which are then scaled by an E4M3 scale factor as is done with NVFP4. The selected data type is denoted using the scale factor's sign bit, which is currently unused in NVFP4, and we apply the same insight to design formats for other bit-widths, including IF3 and IF6. When used to quantize language models, we find that IF4 outperforms existing 4-bit block-scaled formats, achieving lower loss during quantized training and achieving higher accuracy on many tasks in post-training quantization. We additionally design and evaluate an IF4 Multiply-Accumulate \(MAC\) unit to demonstrate that IF4 can be implemented efficiently in next-generation hardware accelerators. Our code is available at https://github.com/mit-han-lab/fouroversix.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
