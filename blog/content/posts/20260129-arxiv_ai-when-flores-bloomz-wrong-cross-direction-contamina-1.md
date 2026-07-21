---
title: 'When Flores Bloomz Wrong: Cross-Direction Contamination in Machine Translation
  Evaluation'
date: 2026-01-29 22:59:16+08:00
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
external_url: https://arxiv.org/abs/2601.20858v1
aliases:
- /posts/20260130-arxiv_ai-when-flores-bloomz-wrong-cross-direction-contamina-1/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:46190a9a210ac05b1ba4aed10fd40447f5c335819cd2f628889d81dac7bf2059
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 89
captured_at: '2026-07-18T04:09:34.038253Z'
source_capture_sha256: sha256:6134eb73c7e1ae9139a47ff7c023a5050229f086ff13f6edea2284fd45b22d29
source_capture_chars_original: 966
source_publication_excerpt_chars: 966
observation_id: obs_b30b6189e700a4588c0da55e8520c3439a691c90909e1bc3d70436a8ddaf6385
revision_id: rev_ac6a05bb09fd1f51bc54038a9a030da54f38f5a735509878cdf0680c11a9cbf8
event_id: evt_816ce426baba0cbe04e7879e98a8741bc4165bcda6d984380d31bf1d7218181a
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-01-29T05:04:04Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2601.20858v1](<https://arxiv.org/abs/2601.20858v1>)
- **作者**: David Tan, Pinzhen Chen, Josef van Genabith, Koel Dutta Chowdhury
- **分类**: cs.CL
- **论文时间**: 2026-01-28T18:56:21Z
- **论文 PDF**: [https://arxiv.org/pdf/2601.20858v1.pdf](<https://arxiv.org/pdf/2601.20858v1.pdf>)

## 来源摘要/节选

> Large language models \(LLMs\) can be benchmark-contaminated, resulting in inflated scores that mask memorization as generalization, and in multilingual settings, this memorization can even transfer to "uncontaminated" languages. Using the FLORES-200 translation benchmark as a diagnostic, we study two 7-8B instruction-tuned multilingual LLMs: Bloomz, which was trained on FLORES, and Llama as an uncontaminated control. We confirm Bloomz's FLORES contamination and demonstrate that machine translation contamination can be cross-directional, artificially boosting performance in unseen translation directions due to target-side memorization. Further analysis shows that recall of memorized references often persists despite various source-side perturbation efforts like paraphrasing and named entity replacement. However, replacing named entities leads to a consistent decrease in BLEU, suggesting an effective probing method for memorization in contaminated models.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
