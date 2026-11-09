---
title: "Data-driven discovery of intrinsic Lie point symmetries of differential equation systems"
date: 2026-11-09T00:44:29+08:00
draft: false
entry_kind: "auto"
tags: ["机器学习", "cs.LG", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:6b70b73a1628ead9a6c426df7da0914a684ca2dec57bfdd0a69e7c26d5d0577d"
source_payload_sha256: "sha256:43676bc19390afa9c63b04b1d0252b7eff39f398055be8fa1411730e77dcf36b"
observation_id: obs_42dfe44cf66a474fac25eca73aea9d3ad1e9644e81be5f908cc85bfd3fcd6283
event_id: evt_06ecfd74e8f0764da156d99781e805543fd979599d74426a3b344c2cc2a6355d
revision_id: rev_6b048c2d84b1c72b1a47cfd5205e83bb00dc3f26b4dd6f38706b1e80f431b096
source_published_at: 2026-11-05T18:19:28Z
first_seen_at: 2026-11-08T16:52:39Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 88
interpretation_sha256: "sha256:c06b6b71230d681826557513cab70f005ea6fa0466f93da1160eb408381df3d7"
description: "这项研究把从微分方程数据中发现连续李点对称性的过程转化为算子问题，在采样的射影空间数据上识别有效生成元，并排除冗余、解相关及几何平凡方向。方法不需要先写出符号确定方程或系统的闭式表示。"
external_url: http://arxiv.org/abs/2611.08421v1
parent_observation_id: null
last_seen_at: 2026-11-09T00:00:00Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2611.08421v1](http://arxiv.org/abs/2611.08421v1)
- **发布域名**: arxiv.org
- **分类**: cs.LG
- **作者**: Ilker Gurcan、Kadir Ustun、Ramazan Gokberk Cinbis

## 要点解读

### 这是什么
这项研究把从微分方程数据中发现连续李点对称性的过程转化为算子问题，在采样的射影空间数据上识别有效生成元，并排除冗余、解相关及几何平凡方向。方法不需要先写出符号确定方程或系统的闭式表示。

### 用在哪里
它适用于仅有精确或近似微分系统数据、需要挖掘其几何结构的研究场景，可用于模型降维与科学机器学习。对微分方程、几何分析和数据驱动建模的研究者有参考价值。

### 可以推断的
- 推测：若数据中的内在对称代数在字典扩展后趋于稳定，所得生成元更可能具有可靠的物理或几何意义。
- 推测：该方法可能降低发现隐藏对称性的门槛，尤其适合缺少显式方程形式但拥有局部微分数据的系统。

## 来源摘要/节选

> Discovering continuous symmetries directly from differential-equation data can reveal geometric structure for model reduction and scientific machine learning without symbolic determining equations or a closed-form representation of the governing system. We formulate intrinsic Lie point-symmetry discovery as an operator-theoretic problem on sampled jet-space data. Admissible generators are identified from a sampled determining operator and separated from redundant, solution-dependent, and geometrically trivial directions. The framework combines prolongation, sequential subspace restrictions, and a fixed nonlinear dictionary linear in trainable coefficients. A rank-stabilization preflight test diagnoses systems whose represented intrinsic symmetry algebra does not stabilize under dictionary refinement. On a controlled differential-equation benchmark with an analytically known 11-dimensional represented intrinsic symmetry algebra, the method recovers the complete represented generator set, reproduces its Lie-bracket structure to numerical precision, and approximates a known generator beyond the training domain. Here we show that explicit intrinsic continuous-symmetry generators can be recovered from data obtained from exact or approximate differential systems.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。