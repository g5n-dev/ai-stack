---
title: "First-Order Stationarity of Reverse Diffusions"
date: 2026-09-29T06:01:53+08:00
draft: false
entry_kind: "auto"
tags: ["生成式 AI", "stat.ML", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:b551a68f88c0d8ef1fc97f1e08da9387392fb2eba3b6d32f4f9513750c526658"
source_payload_sha256: "sha256:9880f5d399a1cccfcf2ad9b5769b3ecfbd1db9cce3fa72defc08ac16ab7d74ae"
observation_id: obs_f33da46175678f5e74ad8f64447beada25e10861ecc6641d99c72b40072d8402
event_id: evt_097a80d23cf5b3fd9564e3701841d125ee394a1273f2a94368c7e68447eddd8b
revision_id: rev_c030a009a3541d49d90baff6bf9b38668fc87c562c758ea1aa545a0d316afde6
source_published_at: 2026-09-25T17:57:43Z
first_seen_at: 2026-09-28T22:00:29.089212Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 46
interpretation_sha256: "sha256:1405c52b57a03348c0ef50d9269045878260e986db44db02275a6b53ec5afbf9"
description: "这篇论文把优化中的一阶平稳性概念迁移到扩散模型，给出基于随机微分方程的逆向扩散在强凸势条件下相对于 Fisher 散度的收缩性，并给出离散化后平均一阶平稳性界的理论结果。"
external_url: http://arxiv.org/abs/2609.31612v1
parent_observation_id: null
last_seen_at: 2026-09-28T22:00:29.089212Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.31612v1](http://arxiv.org/abs/2609.31612v1)
- **发布域名**: arxiv.org
- **分类**: stat.ML
- **作者**: Zhifeng Chen、Chenyang Jiang、Yazhen Wang

## 要点解读

### 这是什么
这篇论文把优化中的一阶平稳性概念迁移到扩散模型，给出基于随机微分方程的逆向扩散在强凸势条件下相对于 Fisher 散度的收缩性，并给出离散化后平均一阶平稳性界的理论结果。  

### 用在哪里
适用于研究扩散模型收敛性、设计新采样算法或进行理论分析的研究者，尤其在需要评估非凸分布采样质量时。  

### 可以推断的
推测：该理论不依赖特定模型结构，只要满足所给的强凸势条件即可使用。  
推测：在实际离散采样时，平均梯度范数的上界可作为收敛性的参考指标。

## 来源摘要/节选

> Recent literature has shown a strong connection between optimization and sampling. We develop the corresponding first-order theory for diffusion models. First, the SDE-based reverse-time flows of overdamped and underdamped Langevin diffusions contract relative Fisher divergences at explicit exponential rates whenever the stationary potential of the forward process is strongly convex---a condition on the noising process one chooses, not on the data. This is a unique advantage of SDE-based reverse diffusion, absent in the reverse process based on ODEs. Second, we incorporate discretization and establish averaged first-order stationarity bounds---the sampling analog of averaged gradient-norm guarantees in nonconvex optimization---for samplers of both overdamped and underdamped diffusion models. As in nonconvex optimization, the convexity-free certificate is local: it guarantees score consistency, not global mode weights.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。