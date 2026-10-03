---
title: "TACO: Ternary Absolute-max Column-wise One-sparse Optimizer for LLM Fine-Tuning"
date: 2026-10-04T01:18:56+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "cs.LG", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:8e6cbe1c98ba2ca6a1745e005a4b012f0eb748a5308ed58fed60dcaa21f84973"
source_payload_sha256: "sha256:71e23aa895e8bdf4656f1c0baeb37b396653d75f096a8a5844c3f8bc0416875c"
observation_id: obs_faf8ced7f9e1c6e3a24dd93ff0d219d0a9b5f369fc12ee0e45f4903f91953db3
event_id: evt_ebb2004e39723070501de68a06ac19fd3be8ebadf4c9f1f72f661a0ba2f6fb57
revision_id: rev_c8c074644358c2d708a2f1a837d81da332cf5b96d2f68c3c2e5e2a762787cebf
source_published_at: 2026-10-01T17:59:42Z
first_seen_at: 2026-10-03T17:30:11Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 79
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2610.02199v1
parent_observation_id: null
last_seen_at: 2026-10-03T17:16:37.294471Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2610.02199v1](http://arxiv.org/abs/2610.02199v1)
- **发布域名**: arxiv.org
- **分类**: cs.LG
- **作者**: Jichao Jiang、Cristian McGee、El Houcine Bergou 等

## 来源摘要/节选

> Full-parameter fine-tuning of large language models (LLMs) incurs substantial optimizer state memory overhead, limiting the model sizes that fit on modern GPUs. Existing approaches either compress optimizer state, abandon first-order gradients, or change the update geometry while retaining dense state. The recently introduced Muon optimizer reduces optimizer memory through matrix-valued updates. Still, its geometry differs from AdamW and can lead to performance degradation when fine-tuning AdamW-pretrained models. To reduce optimizer memory without sacrificing accuracy or computational efficiency in LLM fine-tuning, we propose Ternary Absolute-max Column-wise One-sparse optimizer, or TACO, which follows Muon's operator-norm steepest-descent view but takes the geometric route further. TACO computes the exact steepest-descent direction under a dimension-normalized $1\to1$ operator norm by selecting the sign of the largest magnitude entry in each column of two-dimensional weight matrices. This retains first-order gradients while making optimizer state memory nearly negligible. Our practical TACO optimizer maintains only a small set of low precision gradient components per column, reducing persistent optimizer state by $174\times$ relative to AdamW8bit (from 27.7 GB to 0.16 GB) and peak training memory by $2.9\times$ (from 80.6 GB to 27.5 GB) on OPT-13B, while achieving comparable accuracy and runtime. TACO further enables full-parameter fine-tuning of 30-32B-parameter models on a single 80 GB H100 GPU across multiple model families and tasks.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。