---
title: "WikiSkill: Compiling Agent Experience into Persistent Knowledge for Skill Evolution"
date: 2026-08-29T02:43:35+08:00
draft: false
entry_kind: "auto"
tags: ["AI Agent", "cs.AI", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:ee0c56eea342cebf0d9b8f8aec486061b38a895442bcd75e27dbd8afb989f895"
source_payload_sha256: "sha256:b7bb2e18a38fd631cba56e75dcbe28d724739e8f9f0310d1881473d21bb631bf"
observation_id: obs_4497f852104fcbb6c7ea3052e0793c4718a9e56f4be83c0d777cb847e9e4ef14
event_id: evt_497ac8aab67be06f3733f6d9ce11e30e1daba13694210a06efe218fce87863f0
revision_id: rev_7bc700a71c9f6f0a81904d21bcdc11110e54f97d344a720db88c94c01f41a30c
source_published_at: 2026-08-27T17:59:11Z
first_seen_at: 2026-08-28T18:54:26Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 83
interpretation_sha256: "sha256:89ecfe44a49ed29d3a6982637745bd83faac2cdcd3bed72ebe9628322ec1f99b"
description: "WikiSkill 把代理的原始执行经验、已积累的知识和可执行技能分层管理，并通过一个持久化的 Wiki 持续把经验写入其中，使后续技能更新能够直接在前人成果上构建，从而实现技能的逐步演化与复用。"
external_url: http://arxiv.org/abs/2608.27454v1
parent_observation_id: null
last_seen_at: 2026-08-29T00:00:00Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.27454v1](http://arxiv.org/abs/2608.27454v1)
- **发布域名**: arxiv.org
- **分类**: cs.AI
- **作者**: Liyan Tang、Cyrus Rashtchian、Chun-Sung Ferng 等

## 要点解读

### 这是什么
WikiSkill 把代理的原始执行经验、已积累的知识和可执行技能分层管理，并通过一个持久化的 Wiki 持续把经验写入其中，使后续技能更新能够直接在前人成果上构建，从而实现技能的逐步演化与复用。

### 用在哪里
适用于需要让 AI 代理在持续交互中不断提升技能的场景，如自动化工作流、智能客服和持续学习系统。关注技能可迁移性和复用效率的研究者或工程师可参考该框架的设计思路。

### 可以推断的
推测：持久化的知识库能够避免重复探索，使新技能在已有经验上快速收敛。  
推测：技能跨模型共享后，组织内部的多代理可以共同基于同一 Wiki 进化，提高整体系统的协作效率。

## 来源摘要/节选

> Agent skills package specialized knowledge and workflows into reusable resources that extend AI agent capabilities. Recent work automatically discovers such skills from agent experience, which enables agents to progressively adapt through interaction. However, the insights that guide skill development typically remain scattered across optimization histories, limiting their systematic reuse across iterations. We introduce WikiSkill, a framework that co-evolves agent skills with a persistent knowledge base (wiki). At a high level, WikiSkill separates raw execution experience, accumulated knowledge, and executable skills, while continuously consolidating experience into the wiki, which subsequent skill updates can build on. Across diverse benchmarks and models, WikiSkill consistently outperforms state-of-the-art skill-evolution methods and improves over no-skill baselines in most model-benchmark settings. We find that skill evolution complements model scaling: larger models generally benefit more from evolved skills, while smaller models with skills can outperform substantially larger models without them. We also find that evolved skills transfer effectively across models and model families, and skills evolved by other models can outperform self-evolved skills. Finally, our ablation studies confirm that persistent knowledge accumulation in the wiki is critical for effective skill evolution. These results demonstrate the benefits of systematically accumulating and refining agent experience for developing reusable and transferable skills.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。