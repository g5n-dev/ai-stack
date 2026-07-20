---
title: 阿里云PAI助力新一代Qwen3.5模型发布！
date: 2026-02-24 11:01:45+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- AI Agent
- Docker
categories:
- AI 工程
scenarios:
- AI/ML项目
- 云原生/容器
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7609985140800126976
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:c062ec5c7e58c17ddbd965185a654a58a841822ebe194cb596043f646faf2ba7
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 23
captured_at: '2026-07-18T04:17:38.692681Z'
source_capture_sha256: sha256:90a1d630027d3f2fcbcd43df9afdd512e80372749664d2561469bc7358d44306
source_capture_chars_original: 1988
source_publication_excerpt_chars: 774
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_134a92a9a3ab8eb49d313ae369ff7bff4271b6818b4eb56f8cb21dc28d585c1f
revision_id: rev_748818449af56b3c9fe70bd70df6ed7ebc2d8388176f068280c813e0a32fca4d
event_id: evt_2e2237ffd0c0b300454158051c686278bed98e19e0335c0aec9ea943fd5bb09a
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-24T03:01:45Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7609985140800126976](<https://juejin.cn/post/7609985140800126976>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 2月16日，Qwen3.5 正式发布，并推出 Qwen3.5 系列的第一款模型—— Qwen3.5-Plus 的开放权重版本！作为原生视觉-语言模型，Qwen3.5-Plus 在推理、编程、智能体能力与多模态理解等全方位基准评估中表现优异，助力开发者与企业显著提升生产力。
> Qwen3.5 采用创新的混合架构，将线性注意力（Gated Delta Networks）与稀疏混合专家（MoE）相结合，实现出色的推理效率：总参数量达 3970 亿，每次前向传播仅激活 170 亿参数，在保持能力的同时优化速度与成本。并将语言与方言支持从 119 种扩展至 201 种，为全球用户提供更广泛的可用性与更完善的支持。
> Qwen3.5-Plus 性能表现
> 随着大模型能力边界的持续拓展，训练与推理基础设施正面临前所未有的工程挑战：更大规模的训练数据、更复杂的多模态对齐，以及规模化 Agent 训练带来的计算与通信开销。
> 为支撑新一代 Qwen 模型在算法创新与工程落地间的高效协同，阿里云人工智能平台 PAI（Platform for AI）与 Qwen 团队深度共建，围绕异构计算资源调度、混合精度训练等核心环节系统性地升级了全链路训练基础设施。
> 异构训练框架 PAI-Maestro 支持原生多模态模型高效训练
> 为支持原生多模态模型的高效训练，Qwen3.5 在训练基础设施层面进行了系统性创新，引入了异构训练框架 PAI-Maestro。该框架针对多模态训练中视觉编码器等异构组件与语言模型主干网络在计算特性、内存需求和通信模式上的显著差异，设计了模块化解耦的并行策略：将视觉 Transformer、语言模型等不同模态组件的张量并行、流水线并行和数据并行策略进行独立配置与动态协同，避免了传统方案中"一刀切"并行策略导致的计算资源浪费和通信瓶颈。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
