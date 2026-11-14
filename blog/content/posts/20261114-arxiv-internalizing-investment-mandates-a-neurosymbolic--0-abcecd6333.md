---
title: "Internalizing Investment Mandates: A Neurosymbolic RL Approach to Portfolio Allocation"
date: 2026-11-14T06:38:15+08:00
draft: false
entry_kind: "auto"
tags: ["AI Agent", "cs.LG", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:1adaebdc068f133a64bc45c5196bacc789794c7a59581bef33d1d64b75a7e8e0"
source_payload_sha256: "sha256:5eaefd5e0de3fb50a9c5ac56d3d69a483ceb8fee2458047a7e4097dc06964ef8"
observation_id: obs_abcecd6333f5ed1bdbe0e7085d07e9646945ccac172ebdf75fc1cf1a93e35680
event_id: evt_3ef71bf30bbf1eb5c3cf423bddacd2d7b0c4cd80dae9f6ba8fd1f3ac680f837f
revision_id: rev_db2c6a9c60de79eb29267d29c985fff6337b7c151ef509cad54528f9aaf98752
source_published_at: 2026-11-12T18:59:37Z
first_seen_at: 2026-11-13T22:47:22Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 86
interpretation_sha256: "sha256:7224731e352dbd21e561a120ddbf410d3c7461a77dae7029c9da39e36d99d096"
description: "论文将可微分的符号逻辑监督引入连续资产配置，使智能体在学习过程中掌握投资政策声明的约束，而非在执行后补救违规。实验显示，在六条随市场状态变化的规则下，违规率明显低于无约束强化学习和奖励惩罚方法。"
external_url: http://arxiv.org/abs/2611.17329v1
parent_observation_id: null
last_seen_at: 2026-11-14T00:00:00Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2611.17329v1](http://arxiv.org/abs/2611.17329v1)
- **发布域名**: arxiv.org
- **分类**: cs.LG
- **作者**: Zeynep Yıldız、Satchit Chatterji、Ercan Atam 等

## 要点解读

### 这是什么
论文将可微分的符号逻辑监督引入连续资产配置，使智能体在学习过程中掌握投资政策声明的约束，而非在执行后补救违规。实验显示，在六条随市场状态变化的规则下，违规率明显低于无约束强化学习和奖励惩罚方法。

### 用在哪里
适用于机构投资者构建资产配置策略的场景，尤其适合需要根据市场状态调整配置、同时必须遵守投资授权规则的应用。

### 可以推断的
- 推测：相较于仅优化收益的强化学习方法，符号约束有望提升策略在真实部署中的规则可用性。
- 推测：将合规能力训练进策略本身，可能减少推理阶段额外拦截和修正的依赖。

## 来源摘要/节选

> Institutional portfolios operate under investment policy statements that specify asset allocation constraints, often conditioned on market regime information. Deep reinforcement learning has been shown to optimize financial performance but typically does not enforce rule compliance, making it unsuitable for real-world deployment. Existing neurosymbolic methods such as Probabilistic Logic Policy Gradient (PLPG) offer constraint-satisfying reinforcement learning (RL) via differentiable symbolic supervision but assume a finite, discrete action space. We present a PLPG-inspired continuous allocation method that estimates the probability that the policy's own executed action satisfies the investment mandate, using reparameterized Monte Carlo sampling, and adds it to the training objective. No post-hoc enforcement mechanism intercepts actions at inference time and compliance is learned by the agent. Audited directly on deterministic mean actions with no correction, the policy reduces violations of a six-rule regime-conditional mandate from 96-98% for unconstrained RL and 33.4% for a reward-penalty baseline to 4.8%, showing that a continuous-action neurosymbolic policy can substantially internalize a symbolic mandate.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。