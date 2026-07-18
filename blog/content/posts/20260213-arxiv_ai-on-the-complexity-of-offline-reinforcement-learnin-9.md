---
title: On the Complexity of Offline Reinforcement Learning with $Q^\star$-Approximation
  and Partial Coverage
date: 2026-02-13 03:01:31+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.12107v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:79cb68cdedfe57b3f07767f0467520faeac85c24b8509d0f6aa0e5131090a376
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 101
captured_at: '2026-07-18T04:15:22.283119Z'
source_capture_sha256: sha256:6b091773693edde4dff0abedb19e1d1909dc79970b4a32cadc9fcd51c5c2426e
source_capture_chars_original: 1886
source_publication_excerpt_chars: 1886
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.12107v1](<https://arxiv.org/abs/2602.12107v1>)
- **作者**: Haolin Liu, Braham Snyder, Chen-Yu Wei
- **分类**: cs.LG
- **论文时间**: 2026-02-12T15:59:42Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.12107v1.pdf](<https://arxiv.org/pdf/2602.12107v1.pdf>)

## 来源摘要/节选

> We study offline reinforcement learning under $Q^\\star$-approximation and partial coverage, a setting that motivates practical algorithms such as Conservative $Q$-Learning \(CQL; Kumar et al., 2020\) but has received limited theoretical attention. Our work is inspired by the following open question: "Are $Q^\\star$-realizability and Bellman completeness sufficient for sample-efficient offline RL under partial coverage?" We answer in the negative by establishing an information-theoretic lower bound. Going substantially beyond this, we introduce a general framework that characterizes the intrinsic complexity of a given $Q^\\star$ function class, inspired by model-free decision-estimation coefficients \(DEC\) for online RL \(Foster et al., 2023b; Liu et al., 2025b\). This complexity recovers and improves the quantities underlying the guarantees of Chen and Jiang \(2022\) and Uehara et al. \(2023\), and extends to broader settings. Our decision-estimation decomposition can be combined with a wide range of $Q^\\star$ estimation procedures, modularizing and generalizing existing approaches. Beyond the general framework, we make further contributions: By developing a novel second-order performance difference lemma, we obtain the first $ε^\{-2\}$ sample complexity under partial coverage for soft $Q$-learning, improving the $ε^\{-4\}$ bound of Uehara et al. \(2023\). We remove Chen and Jiang's \(2022\) need for additional online interaction when the value gap of $Q^\\star$ is unknown. We also give the first characterization of offline learnability for general low-Bellman-rank MDPs without Bellman completeness \(Jiang et al., 2017; Du et al., 2021; Jin et al., 2021\), a canonical setting in online RL that remains unexplored in offline RL except for special cases. Finally, we provide the first analysis for CQL under $Q^\\star$-realizability and Bellman completeness beyond the tabular case.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
