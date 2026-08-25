---
title: "Provably adaptive sampling with uniform and remasking discrete diffusion models"
date: 2026-08-25T17:53:20+08:00
draft: false
entry_kind: "auto"
tags: ["生成式 AI", "cs.LG", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:6c15471a86fe5e849661938d7a7933887619890aba74a7a82e299ffa0af54211"
source_payload_sha256: "sha256:70ccead56780ac139fba9f3e87364d4495f8df1e16144228ed0878b387cd0a58"
observation_id: obs_f9180ff81d88965a92e1af61e9632ea7ac55e04d18250f53d87aca8d7f820a48
event_id: evt_2c21d3f08febc1dd1e8efe7871499dbe29e07a58ccf65ad05c652205eef57ebf
revision_id: rev_11d98d7573361a84f157e8a164fb4e28be0980ffeb823e4ffdc715d3583b9630
source_published_at: 2026-08-24T17:54:51Z
first_seen_at: 2026-08-25T10:03:15Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 79
interpretation_sha256: "sha256:4b1a1488e9390b9d5d4162fa231236b5335dda9e89a2e4b14c4c370de85fa6f0"
description: "本文研究离散扩散模型中的采样方法，针对均匀和再掩码前向过程提出一种基于留一去噪器的一阶采样器，并证明其采样复杂度由目标分布的内部依赖结构（双总相关）决定，而不是直接取决于环境维度。"
external_url: http://arxiv.org/abs/2608.23554v1
parent_observation_id: null
last_seen_at: 2026-08-25T09:51:11.965141Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.23554v1](http://arxiv.org/abs/2608.23554v1)
- **发布域名**: arxiv.org
- **分类**: cs.LG
- **作者**: Daniil Dmitriev、Zhihan Huang、Yuting Wei

## 要点解读

### 这是什么  
本文研究离散扩散模型中的采样方法，针对均匀和再掩码前向过程提出一种基于留一去噪器的一阶采样器，并证明其采样复杂度由目标分布的内部依赖结构（双总相关）决定，而不是直接取决于环境维度。

### 用在哪里  
适合从事离散数据（如文本、代码、分子结构等）生成模型研发的工程师，以及关注在高维离散空间中提升采样效率的理论研究者。

### 可以推断的  
- 推测：当目标分布的依赖关系较弱（双总相关较小）时，采样所需的离散化步骤可能更少，从而加快生成速度。  
- 推测：在维度较高的离散空间里，这类采样器相比传统 τ‑leaping 采样器更不易受维度线性增长的影响，可能更具可扩展性。

## 来源摘要/节选

> Discrete diffusion models offer a promising alternative to autoregressive generation by enabling parallel updates, but their sampling efficiency can depend strongly on the choice of the forward process and the sampler. For the uniform forward process, existing lower bounds for the standard $τ$-leaping sampler scale linearly with the ambient dimension $d$, raising the question of whether this dependence is intrinsic to the forward process. We answer this question in the negative. We consider a first-order sampler based on the leave-one-out denoiser for uniform and remasking processes whose coordinate updates can be performed in parallel. In both cases, the sampler can correct denoising mistakes during the sampling process, which becomes necessary when many coordinates are updated together. Our main result establishes an adaptive sampling guarantee: up to logarithmic factors, $N = O(\mathrm{DTC}(X_0) / \varepsilon)$ discretization steps suffice to achieve sampling error $O(\varepsilon_{\mathrm{score&#125;&#125;+\varepsilon)$, where $\varepsilon_{\mathrm{score&#125;&#125;$ is the error in score estimation. Thus, the sampling complexity is governed by the intrinsic dependence structure of the target distribution, as measured by its dual total correlation $\mathrm{DTC}(X_0)$, rather than directly by the ambient dimension $d$. Our analysis proceeds through a Bayes-optimal auxiliary sampler that separates discretization error from score-estimation error. We also derive an exact information-theoretic representation of the discretization error in terms of the mutual information between different coordinates of the forward process at different times. This representation applies to general forward processes and, in the uniform and remasking cases, can be controlled by $\mathrm{DTC}(X_0)$. Numerical experiments on structured synthetic distributions illustrate the predicted dimension-adaptive behavior.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。