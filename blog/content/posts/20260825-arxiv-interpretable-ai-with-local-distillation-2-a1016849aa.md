---
title: "Interpretable AI with Local Distillation"
date: 2026-08-25T23:06:06+08:00
draft: false
entry_kind: "auto"
tags: ["AI", "stat.ME", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:eaef954f645e617f84b240e7ee74369167af74fd0aea63a822e9ae6493d56501"
source_payload_sha256: "sha256:68a24a4fb82adade7d699946a96a06a5bf222493127a9b15ab08e8e6cbc67399"
observation_id: obs_a1016849aab4bd687dc77ba25f57273f9b42e4da6fac71b47933ddd46e06c565
event_id: evt_66f347e9a7a8a3d5df03a4fb4481ecf78101b81adafd7628423f5962543c52ad
revision_id: rev_6996ee69bdd2e422c2151707bef41d5779a1f3bfb726ccfde35f9dbce650101b
source_published_at: 2026-08-24T17:43:07Z
first_seen_at: 2026-08-25T15:04:41.902984Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 40
interpretation_sha256: "sha256:6dc0082b000e357bc12e2bc3f4df1700ca75a6cc00d1e59d02dc947d043d406d"
description: "该研究提出一种“局部蒸馏”框架，让黑箱教师模型在每个查询点指导一个正则化线性学生模型学习局部可解释的近似，并通过加入少量高斯随机化来评估特征选择的稳定性，从而在保持预测精度的同时提供稀疏的线性解释。"
external_url: http://arxiv.org/abs/2608.23538v1
parent_observation_id: null
last_seen_at: 2026-08-25T15:04:41.902984Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.23538v1](http://arxiv.org/abs/2608.23538v1)
- **发布域名**: arxiv.org
- **分类**: stat.ME
- **作者**: Erin Craig、Yiling Huang、Snigdha Panigrahi

## 要点解读

### 这是什么  
该研究提出一种“局部蒸馏”框架，让黑箱教师模型在每个查询点指导一个正则化线性学生模型学习局部可解释的近似，并通过加入少量高斯随机化来评估特征选择的稳定性，从而在保持预测精度的同时提供稀疏的线性解释。

### 用在哪里  
适用于需要对高风险决策提供透明解释的场景，例如医疗诊断或金融风险评估；模型开发者或分析师若想在保持预测能力的同时获得每个样本的特征重要性，可采用此方法。

### 可以推断的  
推测：该方法在高维特征空间中更为实用，因为高维数据往往难以用全局线性模型捕捉局部差异。  
推测：在实际部署时，随机化步骤会增加计算开销，需要在解释需求和实时响应之间进行权衡。

## 来源摘要/节选

> Modern AI models such as tabular foundation models and gradient-boosted ensembles can outpredict classical methods, but provide little basis for reasoning about their predictions. High-stakes decisions call for models that are both accurate and interpretable as built. Local linear modeling offers a path forward: a smooth regression function is locally well approximated by a linear one, allowing a linear fit near each query point to achieve high accuracy without sacrificing transparency. The challenges lie in learning what is "local" and developing statistical tools for interpretation.
> Here, we propose local distillation, in which a black-box "teacher" guides a regularized linear "student" model at each query point. The teacher (1) defines locality by upweighting training observations with similar predicted outcomes, and (2) anchors the fit with its prediction at the query point, included as a pseudo-observation whose weight is estimated from the data. For interpretation, we add a small amount of Gaussian randomization to the local objective and use refits to assess stability: selection frequencies identify reliable features at a query point, and clustering the randomized fits identifies stable subgroups across the data. Under the lasso penalty, we prove that this randomization yields feature-selection probabilities that are stable under small perturbations of the training responses.
> Across 17 benchmark datasets, local distillation nearly matches its AI teacher's accuracy while producing a sparse linear model at each test point. In a high-dimensional cancer gene expression example, the framework identifies patient subgroups whose local models use different genes; this heterogeneity is invisible to a global linear model, and difficult to surface in a black-box model.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。