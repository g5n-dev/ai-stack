---
title: "Financial Numerical Prediction and Allocation as Token Generation"
date: 2026-08-12T02:09:57+08:00
draft: false
entry_kind: "auto"
tags: ["计算机视觉", "cs.CV", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:57db26bb3368ad0d83574f9c18a1a702522ae8aaaf260e1d8c13741b178e7ab6"
source_payload_sha256: "sha256:d44f7d2cde48d0742729769955f905e3846cd2cb53d1c002c96c6fc103ebe598"
observation_id: obs_fe7cfdf3035729b35bf27dd9f7ac7d7dc2c0c1c3c3dfa10215945780df5fabff
event_id: evt_61cd30525ed0e9cb846eeef099e166f32049329fe0600c39dddf74075ec29c85
revision_id: rev_211c227b95bbbf653caa10c1e06b42cb6a2f88788af824ac2c19ba5b9e7fb3ca
source_published_at: 2026-08-10T17:33:10Z
first_seen_at: 2026-08-11T18:20:19Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 65
interpretation_sha256: "sha256:9783b37e115f452bed4630ce12b53539bea5af9590cb6597f9920e4f75963c59"
description: "该研究把因果语言模型的 token 生成能力直接用于股票收益率预测和 ETF 动态配置，构建了一套统一的无头部接口，实现从预测到仓位生成的全流程。"
external_url: http://arxiv.org/abs/2608.09880v1
parent_observation_id: null
last_seen_at: 2026-08-11T18:06:26.934442Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.09880v1](http://arxiv.org/abs/2608.09880v1)
- **发布域名**: arxiv.org
- **分类**: cs.CV
- **作者**: Xu Ouyang、Moontae Lee

## 要点解读

### 这是什么  
该研究把因果语言模型的 token 生成能力直接用于股票收益率预测和 ETF 动态配置，构建了一套统一的无头部接口，实现从预测到仓位生成的全流程。

### 用在哪里  
适用于需要把预测结果直接转化为投资权重的量化研究场景，尤其是探索语言模型在金融决策中端到端应用的从业者和学者。

### 可以推断的  
- 推测：在需要对预测和配置进行联合优化的任务中，端到端的 token 生成方式可能比传统多阶段管道更具灵活性。  
- 推测：实现过程可能需要在生成阶段加入约束机制，以满足实际交易的仓位限制和风险控制要求。

## 来源摘要/节选

> Financial prediction typically relies on task-specific regression, ranking, or policy heads, separating the language model from the numerical object ultimately evaluated. We investigate whether a causal language model can instead represent forecasts and decisions directly through constrained token generation. FinATOM introduces a unified, head-free interface for three-step stock-return forecasting and dynamic five-ETF allocation. The forecasting model autoregressively emits volatility-standardized return tokens and is trained with ordinal and ranking supervision followed by a one-epoch token-level policy stage. The allocation model generates normalized long-only weights; supervised fine-tuning imitates a causal mean--variance anchor, and DAPO-augmented GRPO optimizes realized 21-day Sharpe subject to anchor consistency. In 2023--2025 ETF tests, the allocation policy improves pooled gross Sharpe from 1.428 to 1.529 and net Sharpe under a 5-bp transaction-cost model from 1.394 to 1.494. The multimodal allocation input attains the highest three-period mean Sharpe of 1.540, with its clearest advantage in 2025. On FinTexTS, the SFT and policy strategies achieve 73.52\%/2.68 and 73.72\%/2.69 cumulative-return/Sharpe, respectively. These results support the feasibility of direct language-model token generation for financial numerical prediction and decision-making, while motivating broader tests across assets, regimes, and random seeds.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。