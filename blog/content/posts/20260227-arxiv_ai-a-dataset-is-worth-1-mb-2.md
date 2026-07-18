---
title: A Dataset is Worth 1 MB
date: 2026-02-27 23:20:57+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
- AI Agent
categories:
- 论文
scenarios:
- AI/ML项目
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.23358v1
aliases:
- /posts/20260228-arxiv_ai-a-dataset-is-worth-1-mb-2/
- /posts/20260301-arxiv_ai-a-dataset-is-worth-1-mb-2/
- /posts/20260302-arxiv_ai-a-dataset-is-worth-1-mb-2/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:5edd71390dda66adba7b9bdf36ea96bee1ecbf92eff5455cc3b11fff1c946cbd
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 23
captured_at: '2026-07-18T04:30:37.182965Z'
source_capture_sha256: sha256:e192454d3a53974dbdd87372ac06b4f3344b8d6f429282e7161077baff934a4e
source_capture_chars_original: 1388
source_publication_excerpt_chars: 1388
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.23358v1](<https://arxiv.org/abs/2602.23358v1>)
- **作者**: Elad Kimchi Shoshani, Leeyam Gabay, Yedid Hoshen
- **分类**: cs.LG
- **论文时间**: 2026-02-26T18:59:03Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.23358v1.pdf](<https://arxiv.org/pdf/2602.23358v1.pdf>)

## 来源摘要/节选

> A dataset server must often distribute the same large payload to many clients, incurring massive communication costs. Since clients frequently operate on diverse hardware and software frameworks, transmitting a pre-trained model is often infeasible; instead, agents require raw data to train their own task-specific models locally. While dataset distillation attempts to compress training signals, current methods struggle to scale to high-resolution data and rarely achieve sufficiently small files. In this paper, we propose Pseudo-Labels as Data \(PLADA\), a method that completely eliminates pixel transmission. We assume agents are preloaded with a large, generic, unlabeled reference dataset \(e.g., ImageNet-1K, ImageNet-21K\) and communicate a new task by transmitting only the class labels for specific images. To address the distribution mismatch between the reference and target datasets, we introduce a pruning mechanism that filters the reference dataset to retain only the labels of the most semantically relevant images for the target task. This selection process simultaneously maximizes training efficiency and minimizes transmission payload. Experiments on 10 diverse datasets demonstrate that our approach can transfer task knowledge with a payload of less than 1 MB while retaining high classification accuracy, offering a promising solution for efficient dataset serving.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
