---
title: 'FedCova: Robust Federated Covariance Learning Against Noisy Labels'
date: 2026-03-05 02:41:37+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2603.04062v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:1c2fd141effba19380b9416eb05d67b818136430aa4d43b58011dd525f228708
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 66
captured_at: '2026-07-18T04:27:05.167132Z'
source_capture_sha256: sha256:2370dd8d7f2c7ac71077197bfa8f2b86a0e863607b55af07e46df1776c1ad8b7
source_capture_chars_original: 1440
source_publication_excerpt_chars: 1440
observation_id: obs_58810396870ab84d34a95eb676ef0e226e1209699e5aac899460ab4b5416dacf
revision_id: rev_7f5637e13a01fc75e01120014d9a8f77941f696427e62d45d3ae31c0544bafd2
event_id: evt_e90bb4815a74dadf0402c66acb3d14caf4c7326d9a3528ef59f8f650b595b751
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-03-05T03:42:24Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.04062v1](<https://arxiv.org/abs/2603.04062v1>)
- **作者**: Xiangyu Zhong, Xiaojun Yuan, Ying-Jun Angela Zhang
- **分类**: cs.LG
- **论文时间**: 2026-03-04T13:40:09Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.04062v1.pdf](<https://arxiv.org/pdf/2603.04062v1.pdf>)

## 来源摘要/节选

> Noisy labels in distributed datasets induce severe local overfitting and consequently compromise the global model in federated learning \(FL\). Most existing solutions rely on selecting clean devices or aligning with public clean datasets, rather than endowing the model itself with robustness. In this paper, we propose FedCova, a dependency-free federated covariance learning framework that eliminates such external reliances by enhancing the model's intrinsic robustness via a new perspective on feature covariances. Specifically, FedCova encodes data into a discriminative but resilient feature space to tolerate label noise. Built on mutual information maximization, we design a novel objective for federated lossy feature encoding that relies solely on class feature covariances with an error tolerance term. Leveraging feature subspaces characterized by covariances, we construct a subspace-augmented federated classifier. FedCova unifies three key processes through the covariance: \(1\) training the network for feature encoding, \(2\) constructing a classifier directly from the learned features, and \(3\) correcting noisy labels based on feature subspaces. We implement FedCova across both symmetric and asymmetric noisy settings under heterogeneous data distribution. Experimental results on CIFAR-10/100 and real-world noisy dataset Clothing1M demonstrate the superior robustness of FedCova compared with the state-of-the-art methods.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
