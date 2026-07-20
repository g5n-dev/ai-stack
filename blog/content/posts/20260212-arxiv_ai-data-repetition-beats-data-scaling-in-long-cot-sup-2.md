---
title: Data Repetition Beats Data Scaling in Long-CoT Supervised Fine-Tuning
date: 2026-02-12 23:40:07+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
- 大语言模型
- 机器学习
categories:
- 论文
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.11149v1
aliases:
- /posts/20260213-arxiv_ai-data-repetition-beats-data-scaling-in-long-cot-sup-2/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:f28db93774b5cadf50c5dfe3c1589839f5ab236b78d7249db25746e898b8cefd
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 69
captured_at: '2026-07-18T04:14:55.115056Z'
source_capture_sha256: sha256:2b08f757b9ea93f6d8ab0761f381b1e44acb905e1e3e1c77e11f276519f1a2a2
source_capture_chars_original: 1210
source_publication_excerpt_chars: 1210
observation_id: obs_d18149596760f4057a552679005bf0df9778068361f431561de085f94c40a1e7
revision_id: rev_59247064b1b2c7321bc08e2ee80b6161327ee52e734d9aaad3c6a8efbe4f36b3
event_id: evt_ceb3ac2598b46a89196c5e1fd7aa03c995ebba741886b55c992e929328be37f7
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.11149v1](<https://arxiv.org/abs/2602.11149v1>)
- **作者**: Dawid J. Kopiczko, Sagar Vaze, Tijmen Blankevoort, Yuki M. Asano
- **分类**: cs.CL
- **论文时间**: 2026-02-11T18:58:54Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.11149v1.pdf](<https://arxiv.org/pdf/2602.11149v1.pdf>)

## 来源摘要/节选

> Supervised fine-tuning \(SFT\) on chain-of-thought data is an essential post-training step for reasoning language models. Standard machine learning intuition suggests that training with more unique training samples yields better generalization. Counterintuitively, we show that SFT benefits from repetition: under a fixed update budget, training for more epochs on smaller datasets outperforms single-epoch training on larger datasets. On AIME'24/25 and GPQA benchmarks, Olmo3-7B trained for 128 epochs on 400 samples outperforms the equivalent 1 epoch on 51200 samples by 12-26 percentage points, with no additional catastrophic forgetting. We find that training token accuracy reliably signals when repetition has saturated; improvements from additional epochs plateau at full memorization, a pattern consistent across all settings. These findings provide a practical approach for reasoning SFT, where scaling epochs with token accuracy as a stopping criterion can replace expensive undirected data scaling. We pose the repetition advantage, where full memorization coincides with improved generalization, as a new open problem for the community in understanding the training dynamics of large language models.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
