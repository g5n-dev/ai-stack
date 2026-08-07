---
title: "Predicting Brain Morphometry with MT-GNN: Mesh Evolution in Continuous Time with Graph-Based Metric Tensor Embeddings"
date: 2026-08-07T08:17:57+08:00
draft: false
entry_kind: "auto"
tags: ["计算机视觉", "cs.CV", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:8905c70eb97b6d22b1aeca9ee0669dfa4e6b2a33c008bec52ab76140185d547d"
source_payload_sha256: "sha256:3657b146b53ee1472438c076ab122608140987b19e3f7661aad2384afd2d0847"
observation_id: obs_1c67781e720805d767e0ac1c07f8120fed7d597783462218a5fc5c99ad7a9afd
event_id: evt_d1fa7bb77c577b06de32c3535d9b8baba40d56b422aeaf986e6f43b0892fdc9a
revision_id: rev_a35e59cfb5d55865c808c8233cb5497d257d51994eb520cabd13feb862e33b95
source_published_at: 2026-08-05T17:53:33Z
first_seen_at: 2026-08-07T00:15:22.910460Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 117
interpretation_sha256: "sha256:1cf44da105e099b0779d6941e73dbfacdc2f9a4376ec804120a5ceb8495acd50"
description: "该研究提出一种基于图神经网络的连续时间皮层下结构表面演化预测模型，模型通过预测每个顶点的一阶基本形式（度量张量）并利用可微分刚体保持求解器将其恢复为完整表面，实现从少量先前扫描直接推断未来几何形态。"
external_url: http://arxiv.org/abs/2608.05132v1
parent_observation_id: null
last_seen_at: 2026-08-07T00:15:22.910460Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.05132v1](http://arxiv.org/abs/2608.05132v1)
- **发布域名**: arxiv.org
- **分类**: cs.CV
- **作者**: Hao Ding、Daniel Semchin、Paul M. Thompson 等

## 要点解读

### 这是什么  
该研究提出一种基于图神经网络的连续时间皮层下结构表面演化预测模型，模型通过预测每个顶点的一阶基本形式（度量张量）并利用可微分刚体保持求解器将其恢复为完整表面，实现从少量先前扫描直接推断未来几何形态。

### 用在哪里  
适用于需要依据先前影像随访预测脑结构形态变化的临床评估和试验设计环节，相关研究者和影像分析工程师可利用该模型进行快速形态学预测和进展监控。

### 可以推断的  
- 推测：图网络能够捕捉局部顶点之间的空间关联，从而在预测时保持拓扑一致性。  
- 推测：随预测时间跨度延长，误差范围可能出现扩大趋势。

## 来源摘要/节选

> Predicting how a subcortical structure's shape will evolve from a few prior scans could support prognosis and clinical-trial enrichment. Existing longitudinal mesh predictors either extrapolate shape trajectories via high-dimensional embeddings or regress vertex deformations directly. We instead predict the surface's intrinsic geometry in continuous time: a single per-structure graph network predicts the future per-vertex first fundamental form (metric tensor) for an arbitrary causal multiple-visit history and an arbitrary prediction horizon, conditioned on a Fourier encoding of the lead time. The predicted metric is decoded into a surface by a differentiable As-Rigid-As-Possible solver, and the model is trained end-to-end on the rigid-aligned vertex error. Training through the reconstruction keeps the decoded prediction a valid surface and consistently improves it. On 14 subcortical structures from the ADNI dataset, the proposed mesh evolution model (MT-GNN) predicts best among the evaluated methods at every horizon ($-2.29\%$ mean vertex error vs. the temporal mean, $p{=}6.1{\times}10^{-5}$, beating it on 14/14 structures), ahead of geodesic shape regression (DCM, $-0.19\%$) and a mesh transformer (TransforMesh, $-0.45\%$; $p{=}1.2{\times}10^{-4}$), with the lead widening as the horizon grows.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。