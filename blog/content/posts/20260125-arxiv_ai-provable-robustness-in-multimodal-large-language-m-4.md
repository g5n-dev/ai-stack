---
title: Provable Robustness in Multimodal Large Language Models via Feature Space Smoothing
date: 2026-01-25 12:39:55+08:00
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
external_url: https://arxiv.org/abs/2601.16200v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:a824932e1b7f398d96cd716b2362365a3d3d86f417b768f7075664e1bbbdbed2
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 83
captured_at: '2026-07-18T04:08:56.487166Z'
source_capture_sha256: sha256:c29c234cb12a5046c71ab557f162dc04993c84356f9af82ce58933aad99bf4aa
source_capture_chars_original: 1463
source_publication_excerpt_chars: 1463
observation_id: obs_a6d054fab2def3d1485fed2f3905c788a82c24b82c00e0fee4a128f3ce0f88d5
revision_id: rev_bdab09f0c2e4f49f1845d77037908c0a993a87314d4037d4b6263574564cb2b9
event_id: evt_a054a7c142f7dce8593a8b4a0dd4caae372fd927cf63cab21779b90cb6daaea5
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-01-25T12:41:54Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2601.16200v1](<https://arxiv.org/abs/2601.16200v1>)
- **作者**: Song Xia, Meiwen Ding, Chenqi Kong, Wenhan Yang, Xudong Jiang
- **分类**: cs.LG
- **论文时间**: 2026-01-22T18:52:21Z
- **论文 PDF**: [https://arxiv.org/pdf/2601.16200v1.pdf](<https://arxiv.org/pdf/2601.16200v1.pdf>)

## 来源摘要/节选

> Multimodal large language models \(MLLMs\) exhibit strong capabilities across diverse applications, yet remain vulnerable to adversarial perturbations that distort their feature representations and induce erroneous predictions. To address this vulnerability, we propose the Feature-space Smoothing \(FS\) and theoretically prove that FS offers certified robustness on the feature representations of MLLMs. Specifically, FS transforms any feature encoder into a smoothed variant that is guaranteed to maintain a certified lower bound on the feature cosine similarity between clean and adversarial representations under $\\ell\_2$-bounded attacks. Moreover, we indicate that the value of this Feature Cosine Similarity Bound \(FCSB\) derived from FS can be improved by enlarging the defined Gaussian robustness score on the vanilla encoder. Building upon this, we introduce the Purifier and Smoothness Mapper \(PSM\), a plug-and-play module that improves the Gaussian robustness score of MLLMs and thus enhances their certified robustness under FS, without requiring any retraining on MLLMs. We demonstrate that the FS with PSM not only provides a strong theoretical robustness guarantee but also exhibits superior empirical performance compared to adversarial training. Extensive experiments across diverse MLLMs and downstream tasks indicate the effectiveness of the FS-PSM, reducing the Attack Success Rate \(ASR\) of various white-box attacks from nearly 90\\% to about 1\\%.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
