---
title: "Contrastive Discovery: Open-Ended Scientific Discovery over Competing Explanations"
date: 2026-11-12T19:03:37+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "cs.AI", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:e40d1b3462a6fd33281f91d3538aac0c4f5e4a2467c90a40619918ce465954da"
source_payload_sha256: "sha256:2bcaa8a34c6a876452a2f00f4e8d3668dcc8d5db1b225b000b586d9100e2ec2d"
observation_id: obs_0ada6edaa8802c6af289894ab967fcf35b0a0535c053bc2fcc11ff5fc424d2a9
event_id: evt_8b8c2e498a2724f40dce556760995e3b489348c4cb21300d916064d4d0ecdf46
revision_id: rev_9f655d2daf261ce244b9e2a3d72ba262a292ca8451668710197b6cd1230a82be
source_published_at: 2026-11-10T18:58:43Z
first_seen_at: 2026-11-12T11:02:24.975910Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 82
interpretation_sha256: "sha256:ecc343c3a410d648a7f1f440618f5f2597ec90efaffb8ccc92c179a47962f374"
description: "这项研究提出“对比式发现”：让智能体同时评估一组相互排斥、覆盖完整备选方案的科学解释，并根据实验后各解释的信念变化判断问题是否解决。"
external_url: http://arxiv.org/abs/2611.14514v1
parent_observation_id: null
last_seen_at: 2026-11-12T11:02:24.975910Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2611.14514v1](http://arxiv.org/abs/2611.14514v1)
- **发布域名**: arxiv.org
- **分类**: cs.AI
- **作者**: Ziang Liu、James J. Kim、Yijia Dai 等

## 要点解读

### 这是什么
这项研究提出“对比式发现”：让智能体同时评估一组相互排斥、覆盖完整备选方案的科学解释，并根据实验后各解释的信念变化判断问题是否解决。

### 用在哪里
它适用于基于 LLM 智能体的开放式、数据驱动科学发现，可用于重新利用已有证据，或在相同实验预算下指导后续实验搜索。

### 可以推断的
- 推测：显式比较竞争解释，可能比单纯判断一个假设是否成立更适合需要确定替代方案的科研任务。
- 推测：若智能体常因当前假设被否定而停止，加入替代解释可能帮助其继续利用已有证据。

## 来源摘要/节选

> LLM agents are increasingly used for open-ended, data-driven scientific discovery, yet most of them evaluate hypotheses pointwise, testing an empirical claim $h$ only against its complement $\neg h$. When evidence rejects $h$, the agent learns that one explanation is unlikely but not which alternative the evidence supports. To recover that alternative, we introduce Contrastive Discovery, which replaces the single hypothesis with a contrast set, a scientific question paired with mutually exclusive and collectively exhaustive competing explanations. Each experiment is scored by how its evidence redistributes belief across the set, and the question is resolved when belief concentrates on one explanation. Because contrast sets change only the unit an agent proposes and scores, an existing agent can use them to re-evaluate evidence it has already collected or to guide its search. Across six domains, $89\%$ of the pointwise candidates with the largest belief shifts are rejections. On the same evidence, contrast sets resolve $73\%$ of these candidates to a specific alternative. When contrast sets guide search, the agent resolves $67\%$ more questions than pointwise surprisal under the same experiment budget. In a blinded study, $38$ human experts chose the same explanation on $78\%$ of resolved questions and on $82\%$ of questions where the pointwise agent rejected its hypothesis and stopped. Together, these results support explicit competing explanations as a way for discovery agents to resolve more scientific questions from the same evidence and validation budget.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。