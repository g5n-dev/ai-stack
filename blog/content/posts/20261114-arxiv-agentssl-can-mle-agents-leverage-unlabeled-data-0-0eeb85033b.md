---
title: "AgentSSL: Can MLE Agents Leverage Unlabeled Data?"
date: 2026-11-14T11:13:51+08:00
draft: false
entry_kind: "auto"
tags: ["AI Agent", "机器学习", "cs.AI", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:e8e058c5231c0d8d3a22164dec627bf3c586fa2858429a4ec3fd26341adc7fc7"
source_payload_sha256: "sha256:8e197bfedde48df693c64862791584d9557b468185271c558d7cb1cf1d370b70"
observation_id: obs_0eeb85033b17e767df2baf29952590b87a1d0a37fafcf55314bf3032800cc91f
event_id: evt_8fc1dac9dcdcbcb2f58e259523a7875f879e074e091d701c05f10125bcdf9001
revision_id: rev_0ae56e1f982e418f8ec1aa6bae494bf53d9d2efe333f158679d40ee341b12e91
source_published_at: 2026-11-12T18:59:06Z
first_seen_at: 2026-11-14T03:24:33Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 49
interpretation_sha256: "sha256:39f873177219c44274f2b508b643c549190359845d1fcbab2947e9f0de3edab1"
description: "AgentSSL 研究 MLE 智能体在标注数据有限、未标注数据丰富时，能否自动组合并改进半监督学习方案。实验显示其在多数设置中超过人工基线，但程序选择仍会造成明显性能下降，并配套提出 ProgramSelectBench 基准。"
external_url: http://arxiv.org/abs/2611.17323v1
parent_observation_id: null
last_seen_at: 2026-11-14T03:12:22.680622Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2611.17323v1](http://arxiv.org/abs/2611.17323v1)
- **发布域名**: arxiv.org
- **分类**: cs.AI
- **作者**: Ethan Lin、Akanksha Sarkar、Ziang Liu 等

## 要点解读

### 这是什么
AgentSSL 研究 MLE 智能体在标注数据有限、未标注数据丰富时，能否自动组合并改进半监督学习方案。实验显示其在多数设置中超过人工基线，但程序选择仍会造成明显性能下降，并配套提出 ProgramSelectBench 基准。

### 用在哪里
适合关注半监督学习、自动化机器学习流水线或智能体程序生成的读者，也可用于评估从多个候选方案中选择程序的难题。研究还覆盖了生态检测任务，检验方法向现实场景迁移的表现。

### 可以推断的
- 推测：若业务存在“标注昂贵但未标注数据充足”的约束，这类将半监督学习转化为程序搜索的思路值得进一步评估。
- 推测：仅依赖智能体反馈指标挑选程序可能放大误差，实际应用时需要更可靠的方案选择机制。

## 来源摘要/节选

> Applying machine learning systems to new domains introduces bottlenecks in both labeled data acquisition and manual pipeline engineering. While recent MLE agents show promise in automating pipeline design, they have been studied almost exclusively in fully supervised settings, leaving them untested in realistic regimes where labeled data is scarce but unlabeled data is abundant. In this work, we introduce Agentic Semi-Supervised Learning (AgentSSL), framing SSL as a program search problem and studying how agents navigate this space under limited supervision. We find that even under weak feedback and matched compute, agents can synthesize code that combines and adapts established SSL techniques, exceeding the strongest human-engineered baselines in 8 of 12 settings by up to +21.8%. However, our results identify program selection as a critical bottleneck in AgentSSL, where performance drops by as much as 47% when selecting based on the agent's feedback metric. To systematically study this bottleneck, we introduce ProgramSelectBench, a large-scale benchmark with a combined total of 16,977 agent-generated and human-engineered SSL programs, and evaluate both unsupervised and active program selection methods. We further evaluate AgentSSL on real-world ecology detection tasks, highlighting the opportunities and challenges of transferring agent-discovered strategies beyond controlled benchmarks.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。