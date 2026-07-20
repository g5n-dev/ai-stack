---
title: 'VAUQ: Vision-Aware Uncertainty Quantification for LVLM Self-Evaluation'
date: 2026-02-25 02:57:16+08:00
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
external_url: https://arxiv.org/abs/2602.21054v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:a784194e6cf21bad4907e9659adcb2096a7b2ebcbfceb217b3907065a80ce129
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 70
captured_at: '2026-07-18T04:17:01.203007Z'
source_capture_sha256: sha256:5c374117ab44867b7fccd9cbd876de834064fbf866f1c028353e6665d7174b48
source_capture_chars_original: 1068
source_publication_excerpt_chars: 1068
observation_id: obs_b3aa860bef2b88b1914c141bbd3680fb785152f741ed6f7f8569729eb515ad56
revision_id: rev_e05cfa1c4a1cb4a41bc5effa32e84d9664209fb641ec6293dd8ea1691031e5ac
event_id: evt_7cd23bbaffd8f74b156e1df230510b9b37141e23309aa41f72bcfff82f6efeaf
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.21054v1](<https://arxiv.org/abs/2602.21054v1>)
- **作者**: Seongheon Park, Changdae Oh, Hyeong Kyu Choi, Xuefeng Du, Sharon Li
- **分类**: cs.CV
- **论文时间**: 2026-02-24T16:11:14Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.21054v1.pdf](<https://arxiv.org/pdf/2602.21054v1.pdf>)

## 来源摘要/节选

> Large Vision-Language Models \(LVLMs\) frequently hallucinate, limiting their safe deployment in real-world applications. Existing LLM self-evaluation methods rely on a model's ability to estimate the correctness of its own outputs, which can improve deployment reliability; however, they depend heavily on language priors and are therefore ill-suited for evaluating vision-conditioned predictions. We propose VAUQ, a vision-aware uncertainty quantification framework for LVLM self-evaluation that explicitly measures how strongly a model's output depends on visual evidence. VAUQ introduces the Image-Information Score \(IS\), which captures the reduction in predictive uncertainty attributable to visual input, and an unsupervised core-region masking strategy that amplifies the influence of salient regions. Combining predictive entropy with this core-masked IS yields a training-free scoring function that reliably reflects answer correctness. Comprehensive experiments show that VAUQ consistently outperforms existing self-evaluation methods across multiple datasets.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
