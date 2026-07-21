---
title: Risk-Aware World Model Predictive Control for Generalizable End-to-End Autonomous
  Driving
date: 2026-02-27 02:54:04+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.23259v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:47a626f8cf1dbaa34dc8a233a6eabdd7cf48ce8351523dbe2d0516011d82f29f
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 89
captured_at: '2026-07-18T04:30:40.966842Z'
source_capture_sha256: sha256:f6e9d12cdb4d2f8231f047995d56a0743511d5c285a791df0ba580c3e130ba25
source_capture_chars_original: 1842
source_publication_excerpt_chars: 1842
observation_id: obs_a91a61f98468989ca7a6d6aa02a924ef47861a2e3550375bc4ad9affffb04c22
revision_id: rev_61a8585115d3503f78cb6f9c92ab62b7cd2ae64cf2b47aacdd026e9cafb7d66b
event_id: evt_cf2d887e744ed85cba5b855d437fde247f1edb5b19a9a4398c0ec241442dce32
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-27T03:55:34Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.23259v1](<https://arxiv.org/abs/2602.23259v1>)
- **作者**: Jiangxin Sun, Feng Xue, Teng Long, Chang Liu, Jian-Fang Hu, Wei-Shi Zheng, Nicu Sebe
- **分类**: cs.CV
- **论文时间**: 2026-02-26T17:32:30Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.23259v1.pdf](<https://arxiv.org/pdf/2602.23259v1.pdf>)

## 来源摘要/节选

> With advances in imitation learning \(IL\) and large-scale driving datasets, end-to-end autonomous driving \(E2E-AD\) has made great progress recently. Currently, IL-based methods have become a mainstream paradigm: models rely on standard driving behaviors given by experts, and learn to minimize the discrepancy between their actions and expert actions. However, this objective of "only driving like the expert" suffers from limited generalization: when encountering rare or unseen long-tail scenarios outside the distribution of expert demonstrations, models tend to produce unsafe decisions in the absence of prior experience. This raises a fundamental question: Can an E2E-AD system make reliable decisions without any expert action supervision? Motivated by this, we propose a unified framework named Risk-aware World Model Predictive Control \(RaWMPC\) to address this generalization dilemma through robust control, without reliance on expert demonstrations. Practically, RaWMPC leverages a world model to predict the consequences of multiple candidate actions and selects low-risk actions through explicit risk evaluation. To endow the world model with the ability to predict the outcomes of risky driving behaviors, we design a risk-aware interaction strategy that systematically exposes the world model to hazardous behaviors, making catastrophic outcomes predictable and thus avoidable. Furthermore, to generate low-risk candidate actions at test time, we introduce a self-evaluation distillation method to distill riskavoidance capabilities from the well-trained world model into a generative action proposal network without any expert demonstration. Extensive experiments show that RaWMPC outperforms state-of-the-art methods in both in-distribution and out-of-distribution scenarios, while providing superior decision interpretability.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
