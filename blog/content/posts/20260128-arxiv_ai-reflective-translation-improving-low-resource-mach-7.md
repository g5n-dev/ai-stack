---
title: 'Reflective Translation: Improving Low-Resource Machine Translation via Structured
  Self-Reflection'
date: 2026-01-28 07:28:04+08:00
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
external_url: https://arxiv.org/abs/2601.19871v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:938b3f735a3d38761434d9c5ebc2dce93b3c86671e04e57df9b9751fe436e555
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 97
captured_at: '2026-07-18T04:09:22.840879Z'
source_capture_sha256: sha256:b7ed569e71cbc964e971c5a5e4e4ea7f2a53435a1653134b816dbae6d7886794
source_capture_chars_original: 1370
source_publication_excerpt_chars: 1370
observation_id: obs_038827cc7f22324e83dc7decff246811c1588b3fd7ab06862e3f428c9b28e1e3
revision_id: rev_72b7a70b4add3f9c48480c40ad9da116b32ad7e5d53bbcaf2d1fc505badaa452
event_id: evt_d94276b3f6dfc0f84a5e23a593696515162d1df7145040e397338f8451a3359c
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-01-28T07:34:45Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2601.19871v1](<https://arxiv.org/abs/2601.19871v1>)
- **作者**: Nicholas Cheng
- **分类**: cs.CL
- **论文时间**: 2026-01-27T18:37:09Z
- **论文 PDF**: [https://arxiv.org/pdf/2601.19871v1.pdf](<https://arxiv.org/pdf/2601.19871v1.pdf>)

## 来源摘要/节选

> Low-resource languages such as isiZulu and isiXhosa face persistent challenges in machine translation due to limited parallel data and linguistic resources. Recent advances in large language models suggest that self-reflection, prompting a model to critique and revise its own outputs, can improve reasoning quality and factual consistency. Building on this idea, this paper introduces Reflective Translation, a prompt-based framework in which a model generates an initial translation, produces a structured self-critique, and then uses this reflection to generate a refined translation. The approach is evaluated on English-isiZulu and English-isiXhosa translation using OPUS-100 and NTREX-African, across multiple prompting strategies and confidence thresholds. Results show consistent improvements in both BLEU and COMET scores between first- and second-pass translations, with average gains of up to +0.22 BLEU and +0.18 COMET. Statistical significance testing using paired nonparametric tests confirms that these improvements are robust. The proposed method is model-agnostic, requires no fine-tuning, and introduces a reflection-augmented dataset that can support future supervised or analysis-driven work. These findings demonstrate that structured self-reflection is a practical and effective mechanism for improving translation quality in low-resource settings.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
