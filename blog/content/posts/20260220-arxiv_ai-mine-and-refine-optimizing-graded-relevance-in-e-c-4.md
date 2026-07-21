---
title: 'Mine and Refine: Optimizing Graded Relevance in E-commerce Search Retrieval'
date: 2026-02-20 22:59:37+08:00
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
external_url: https://arxiv.org/abs/2602.17654v1
aliases:
- /posts/20260221-arxiv_ai-mine-and-refine-optimizing-graded-relevance-in-e-c-4/
- /posts/20260222-arxiv_ai-mine-and-refine-optimizing-graded-relevance-in-e-c-4/
- /posts/20260223-arxiv_ai-mine-and-refine-optimizing-graded-relevance-in-e-c-4/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:19c8942b3ba1f5060fac01a78e1ed2e03c16e66992ddb03f7f700986671dfca7
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 75
captured_at: '2026-07-18T04:16:19.911759Z'
source_capture_sha256: sha256:dd1c4df98627b4da8ab04b3f471f1dcf5dea660ab33dc293e75296d202597ec6
source_capture_chars_original: 1533
source_publication_excerpt_chars: 1533
observation_id: obs_c7d80c1cc982837c5ae8a0c5552ccd05c83f54b5b060caaeae276995222c318c
revision_id: rev_6986c2dd5aa0ae4ca17988fd5413b9af272585681aa1940ea6889f5701cbb466
event_id: evt_80077e9bdebbc567188ba84225952476f05157c3f31fa33d813e2373d4b887fa
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-20T03:54:51Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.17654v1](<https://arxiv.org/abs/2602.17654v1>)
- **作者**: Jiaqi Xi, Raghav Saboo, Luming Chen, Martin Wang, Sudeep Das
- **分类**: cs.IR
- **论文时间**: 2026-02-19T18:56:36Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.17654v1.pdf](<https://arxiv.org/pdf/2602.17654v1.pdf>)

## 来源摘要/节选

> We propose a two-stage "Mine and Refine" contrastive training framework for semantic text embeddings to enhance multi-category e-commerce search retrieval. Large scale e-commerce search demands embeddings that generalize to long tail, noisy queries while adhering to scalable supervision compatible with product and policy constraints. A practical challenge is that relevance is often graded: users accept substitutes or complements beyond exact matches, and production systems benefit from clear separation of similarity scores across these relevance strata for stable hybrid blending and thresholding. To obtain scalable policy consistent supervision, we fine-tune a lightweight LLM on human annotations under a three-level relevance guideline and further reduce residual noise via engagement driven auditing. In Stage 1, we train a multilingual Siamese two-tower retriever with a label aware supervised contrastive objective that shapes a robust global semantic space. In Stage 2, we mine hard samples via ANN and re-annotate them with the policy aligned LLM, and introduce a multi-class extension of circle loss that explicitly sharpens similarity boundaries between relevance levels, to further refine and enrich the embedding space. Robustness is additionally improved through additive spelling augmentation and synthetic query generation. Extensive offline evaluations and production A/B tests show that our framework improves retrieval relevance and delivers statistically significant gains in engagement and business impact.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
