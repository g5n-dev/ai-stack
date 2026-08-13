---
title: "Two-stage Odd Residual Flows for Mean-Preserving Probabilistic Time Series Forecasting"
date: 2026-08-13T07:58:59+08:00
draft: false
entry_kind: "auto"
tags: ["生成式 AI", "cs.LG", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:0c6ba262188f32d6e815f08575dade0bb36e5f2adeb8192d9b92e61d9828b70f"
source_payload_sha256: "sha256:c7596be62458ee9e1f8e26235635f404437a7f0ab13deaf21d99189b8c22ef90"
observation_id: obs_1880d8bbd8bb88c8101307eab6e5be68b247af597932f9d8eea6f068307ee4f4
event_id: evt_c5a791c94a3c340e6b0f3c07d992a51106ec2b7526e7148c031e6b0efeea938f
revision_id: rev_7b3183882632c02f42b309098c482233d80b981d1110f47176c5acd107f49166
source_published_at: 2026-08-11T16:22:47Z
first_seen_at: 2026-08-12T23:57:29.367159Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 86
interpretation_sha256: "sha256:5ab521d91d142fafbbe3e533f68157687de6580f4b8c6919c951196cd1351ed8"
description: "该框架将均值预测与不确定性估计分两个阶段实现：先用一个确定性模型给出准确的均值，再利用仅含奇函数的受限归一化流学习围绕该均值的残差分布，从而保证均值保持且无需采样。"
external_url: http://arxiv.org/abs/2608.11114v1
parent_observation_id: null
last_seen_at: 2026-08-12T23:57:29.367159Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.11114v1](http://arxiv.org/abs/2608.11114v1)
- **发布域名**: arxiv.org
- **分类**: cs.LG
- **作者**: Kiran Madhusudhanan、Christian Klötergens、Lars Schmidt-Thieme 等

## 要点解读

### 这是什么  
该框架将均值预测与不确定性估计分两个阶段实现：先用一个确定性模型给出准确的均值，再利用仅含奇函数的受限归一化流学习围绕该均值的残差分布，从而保证均值保持且无需采样。  

### 用在哪里  
适用于对风险敏感、需要在长期预测中同时提供可靠点估计和概率分布的应用，例如金融风险评估、能源负荷预测等场景。  

### 可以推断的  
推测：在需要兼顾预测精度和概率质量的时序任务中，这种分离式设计可能比端到端联合训练更具灵活性。  
推测：采用仅含奇函数的归一化流可以在不增加采样开销的前提下实现均值保持，有助于降低计算成本。

## 来源摘要/节选

> Probabilistic forecasting plays an essential role in risk-sensitive decision-making, particularly in long-horizon settings. However, existing approaches often face a fundamental trade-off between distributional flexibility and accurate mean prediction. Traditional parametric methods, such as Mean Variance Estimation (MVE), can suffer from degraded point accuracy when trained under joint Negative Log-Likelihood (NLL) objectives, while modern-flexible generative models, including Normalizing Flows and Diffusion Models, typically rely on costly Monte Carlo sampling and may yield suboptimal mean estimates. To address this limitation, we propose Two-stage Odd Residual Flows (TORF), a framework that decouples mean forecasting from uncertainty estimation. In the first stage, a pre-trained deterministic model is used to produce an accurate mean prediction. In the second stage, a Restricted Normalizing Flow, with strictly odd functions learns flexible residual distributions around the point forecast, guaranteeing mean preservation from the first stage without sampling. Experiments show that TORF achieves state-of-the-art deterministic accuracy (NMAE) while providing strong density estimation performance (CRPS) on short and long-horizon forecasting.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。