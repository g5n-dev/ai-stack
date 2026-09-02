---
title: "Beyond Scores: Understanding LLM-as-a-Judge Mechanisms in Summarization Evaluation"
date: 2026-09-02T12:35:39+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "cs.CL", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:61d80502e11ea7e2c7017331cff3912f5d2dad28af1eb8a05b725cc490dc3c66"
source_payload_sha256: "sha256:3d1585875a68e37034280b3e5ba8118e553faceea1870bb0727931902d760786"
observation_id: obs_df2edf0951501d0bc70aa3c6f20411b29c3f5cba44defb37fcad70863edbe128
event_id: evt_a5573580a5ce4c26201209498549e6161331795257be1a8bd7401db5df6fd390
revision_id: rev_b5b850ae6521bfb2df30c8614c3eb3d308c999d117b57a48f8267252cf650ff4
source_published_at: 2026-09-01T17:59:49Z
first_seen_at: 2026-09-02T04:32:14.031983Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 82
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2609.01604v1
parent_observation_id: null
last_seen_at: 2026-09-02T04:32:14.031983Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.01604v1](http://arxiv.org/abs/2609.01604v1)
- **发布域名**: arxiv.org
- **分类**: cs.CL
- **作者**: Himil Vasava、Ming Jiang

## 来源摘要/节选

> LLM-based evaluators of natural language generation (NLG) quality are widely deployed as scoring tools and as automated training signals, yet the internal procedure by which they assign a rating remains poorly understood. We investigate this procedure mechanistically through an eight-attack perturbation taxonomy across the Readability and Adequacy dimensions of NLG quality, a generation pipeline that produces paired clean and corrupt summaries with controlled error intensity and explicit token-level modification maps, and a four-experiment battery of causal tracing, logit-lens vocabulary projection, and attention-head knockout applied to Themis (Llama-3-8B) and Prometheus (Mistral-7B). Both evaluators implement a structured, coherent evaluation pipeline operating in two stages: below layer 15, attention performs local error comparison and routes the result to the final input position; above it, the MLP cascade integrates the signal and writes the rating, with the decision crystallizing in the residual stream at a sharp late layer (L = 26 on Themis, L = 25 on Prometheus). Furthermore, a base-model control at the same scale (Llama-3-8B) reproduces the routing architecture and crystallization but not the stage separation, isolating the two mechanisms that fine-tuning specifically installs, suppression of below-L15 MLP contribution at the last position and a two-layer advance of the crystallization depth, indicating that fine-tuning sculpts an existing substrate rather than building the pipeline from scratch. We release the source code and data at https://github.com/himil-v/judge-mech

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。