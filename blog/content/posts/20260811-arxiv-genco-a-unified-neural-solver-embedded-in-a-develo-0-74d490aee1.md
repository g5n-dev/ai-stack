---
title: "GENCO - A Unified Neural Solver Embedded in a Development Framework for Steady-State Grid Analysis"
date: 2026-08-11T19:08:50+08:00
draft: false
entry_kind: "auto"
tags: ["AI", "cs.AI", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:0b1e250aa1fffc3ade97b80e95b1c6bcf4aceaec00c32c88fc94061ac5dd9c8f"
source_payload_sha256: "sha256:c254ff336d283873d59c5e2269eb44dff679ad26ead45f8e44559eaca550180a"
observation_id: obs_74d490aee13326f96b16d2b0f2f45b17b6854d7d99fcbee147609b2fb438660a
event_id: evt_1c5ee54380a54a53967f95372f14865fbf9fe31bb6d19860583d21c6b1510e66
revision_id: rev_557fb2c56d4587f9c35e44a3b59db1125fc1994155797269dab3197a5285fd72
source_published_at: 2026-08-10T17:57:49Z
first_seen_at: 2026-08-11T11:18:10Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 98
interpretation_sha256: "sha256:d3e9045b1ec10fbfc376e33727a3541e04ea1d3dc093848dd9bfba87a650dd55"
description: "GENCO 是一种统一的神经网络求解器，兼顾潮流、最优潮流和状态估计三大任务，配合开源 GridFM 框架提供标准化数据和低代码训练，并在实验中实现约30倍于传统牛顿法的加速以及约85倍于 IPOPT 的加速。"
external_url: http://arxiv.org/abs/2608.09921v1
parent_observation_id: null
last_seen_at: 2026-08-11T11:04:40.335444Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.09921v1](http://arxiv.org/abs/2608.09921v1)
- **发布域名**: arxiv.org
- **分类**: cs.AI
- **作者**: Alban Puech、Matteo Mazzonelli、Tamara R. Govindasamy 等

## 要点解读

### 这是什么
GENCO 是一种统一的神经网络求解器，兼顾潮流、最优潮流和状态估计三大任务，配合开源 GridFM 框架提供标准化数据和低代码训练，并在实验中实现约30倍于传统牛顿法的加速以及约85倍于 IPOPT 的加速。

### 用在哪里
适用于大规模输电网的快速仿真、实时优化和基准评估，适合电力系统研发工程师、算法研究者以及希望低代码构建神经求解器的团队。

### 可以推断的
推测：统一模型架构可能在不同拓扑上复用，降低针对单一任务重新设计模型的门槛。  
推测：随着开源数据集和框架的发布，社区或将快速开展神经求解器的改进与标准化基准研究。

## 来源摘要/节选

> Foundation models are transforming business workflows and boosting productivity, yet they remain largely absent from engineering domains such as power system analysis, where strict physical consistency must be enforced.
> We present GENCO (GEometric Neural Corrective Optimizer), a unified neural solver for steady-state transmission grid analysis that handles power flow (PF), optimal power flow (OPF), and state estimation (SE) within a single architecture and shared network representation. To support advances in neural power system solvers, we introduce the open-source GridFM Development Framework, which standardizes synthetic data generation and training in a low-code environment. We also release large-scale datasets with millions of PF and OPF scenarios across diverse grid topologies to support reproducible benchmarking.
> We evaluate GENCO on the PFDelta and OPFData benchmarks against state-of-the-art neural solvers and classical solvers, including Newton-Raphson and IPOPT, as well as on real-world Hydro-Québec SCADA data. For large-scale PF, GENCO recovers the full AC operating state, including voltage magnitudes and reactive power that DC-PF cannot provide, while matching DC-PF-level active power-balance residuals. It achieves up to 30x speedups over Newton-Raphson at only 2x the runtime of DC-PF. For OPF, it achieves up to 85x speedups over IPOPT while improving feasibility, optimality, and runtime over DC-OPF. For SE, GENCO is more robust than classical weighted least squares to noisy measurements and network parameter errors, and always returns a high-quality estimate even when weighted least squares fails to converge.
> Together, the unified architecture and development framework provide a new approach to large-scale steady-state grid analysis, lowering the barrier to entry for power system engineers and marking a step toward Grid Foundation Models.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。