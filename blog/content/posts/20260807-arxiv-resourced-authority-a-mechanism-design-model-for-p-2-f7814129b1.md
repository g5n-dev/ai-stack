---
title: "Resourced Authority A Mechanism-Design Model for Participatory Governance of Deployed AI Agents"
date: 2026-08-07T19:58:46+08:00
draft: false
entry_kind: "auto"
tags: ["AI Agent", "cs.GT", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:469c2b316c9bafcd89773613402f337ef4d19e10c7071592d4a782e83740d82b"
source_payload_sha256: "sha256:28e59a12b4578756d9f10355bd1df1259fd69ec97468c4ffe6174ea89c68cee3"
observation_id: obs_f7814129b1f66f282b4466dc2c9466c598930efd4b6227b5d103847c05e780a1
event_id: evt_7cba3c4f616aa926e9b88b5ff30a689658a1b792cfa393883977716e50d97408
revision_id: rev_790f3f743ef2c50383232227ff440272f5461346bdd841383effaeac00477a62
source_published_at: 2026-08-06T17:53:24Z
first_seen_at: 2026-08-07T11:56:57.158616Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 95
interpretation_sha256: "sha256:56f12f9a3d7ea81a26524ab6fa1cb960bb81eefcb0be3b8d1d51368b0e8d2a90"
description: "该模型把对已部署 AI 主体的治理抽象为一种机制设计，利用计算资源的分配实现自我执行的授权，并以硬件签名的计算许可证形式兑现决策。"
external_url: http://arxiv.org/abs/2608.06353v1
parent_observation_id: null
last_seen_at: 2026-08-07T11:56:57.158616Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.06353v1](http://arxiv.org/abs/2608.06353v1)
- **发布域名**: arxiv.org
- **分类**: cs.GT
- **作者**: Praphul Chandra、Sujit Gujar、Ganesh Ghalme

## 要点解读

### 这是什么
该模型把对已部署 AI 主体的治理抽象为一种机制设计，利用计算资源的分配实现自我执行的授权，并以硬件签名的计算许可证形式兑现决策。

### 用在哪里
适用于希望在部署阶段引入持续人类监督的 AI 系统，尤其是公共平台或合规层的治理框架；对机制设计、AI 安全与治理研究具有参考价值。

### 可以推断的
推测：该模型目前以理论建模为主，尚未进行大规模实证验证。  
推测：防止被治理主体操纵治理选民是核心难题，说明方案对策略性行为较为敏感，需要额外的防御手段。

## 来源摘要/节选

> We give a formal mechanism design model for the continuous participatory governance of a deployed AI agent. The mechanism is built on the principle that governance should control an AI agent through resource allocation so as to make authorization self enforcing via compute budgets. The mechanism seeks to establish the Safe AI paradigm that compute is an effective governance lever. We situate our work as a compliance or commons overlay on a deployer. One governance period is an extensive form game in which verified human stakeholders arrive sequentially and contribute, on a provision or a rejection market, in a governance currency that is deliberately distinct from the agents compute. A funding aggregator turns raw contributions into breadth weighted effective supports - a two threshold gate with hysteresis converts net support into a binary authorization that, through a coupling map bounded by an exogenously certified safety ceiling, releases a metered compute budget - realized in hardware as a signed compute license so that the decision is self-enforcing. We characterize the class of agents the mechanism can govern and isolate manipulation of the governing electorate by the governed agent as the central open problem. We also introduce several challenges addressing manipulation of governing electorate by the governed agents.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。