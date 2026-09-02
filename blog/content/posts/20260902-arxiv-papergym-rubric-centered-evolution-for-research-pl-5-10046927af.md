---
title: "PaperGym: Rubric-Centered Evolution for Research-Plan Generation"
date: 2026-09-02T08:15:55+08:00
draft: false
entry_kind: "auto"
tags: ["AI", "cs.CL", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:4db47888a7b2c96bed9d557450bbc38ee666d1600049d621ab3ad00a7a639fbf"
source_payload_sha256: "sha256:7b55dad3eeed7549fc7a42938b2906a5c4237b713a46ca18ab9f345ff9a24fdb"
observation_id: obs_10046927af255ec023acf3becd03eca64345e659ccbd71bbf20397d9546aded9
event_id: evt_e63f00c02e3f66bb9bd2f70a4e194a4d0decfbaeb956b805d400fbcc1f35b92e
revision_id: rev_7205c0551a6d29d02d1a4537fa2cc1f4d491763d22184ca3503cbb66311ae011
source_published_at: 2026-08-31T17:31:18Z
first_seen_at: 2026-09-02T00:13:34.127341Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 64
interpretation_sha256: "sha256:a2d35ffbd58ed43a21f38f801befc370f09a7cb4eea266704b105a3a292ff3b2"
description: "PaperGym 将单篇科研论文转化为完整的训练环境，分别从论文的目标、背景、方法、实验中抽取研究计划的问题与评估标准，为强化学习生成研究计划提供可验证的奖励。"
external_url: http://arxiv.org/abs/2608.31119v1
parent_observation_id: null
last_seen_at: 2026-09-02T00:13:34.127341Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.31119v1](http://arxiv.org/abs/2608.31119v1)
- **发布域名**: arxiv.org
- **分类**: cs.CL
- **作者**: Yuhan Wang、Zhengxi Lu、Yuchen Yan 等

## 要点解读

### 这是什么
PaperGym 将单篇科研论文转化为完整的训练环境，分别从论文的目标、背景、方法、实验中抽取研究计划的问题与评估标准，为强化学习生成研究计划提供可验证的奖励。

### 用在哪里
在需要自动生成或评估科研思路的 AI 系统研发中，可使用该框架进行模型训练、奖励设计以及基准对比。

### 可以推断的
推测：把 rubric 同时用作上下文信息和奖励信号，有助于提升训练信号的可信度，减少因改写而产生的虚假奖励。  
推测：随着可用训练语料的规模扩大，模型在科研计划生成任务上的表现可能进一步提升。

## 来源摘要/节选

> Research planning is the decisive capability of AI scientists. Yet a research plan admits no verifiable answer, so reinforcement learning lacks the environment it requires: tasks paired with a critic. Rubrics extracted from scientific papers can supply the critic. Existing pipelines, however, draw the question and the criteria from the same content, so the reward can be earned by paraphrase. The rubric is further compressed into a single scalar per rollout. We introduce PaperGym, a unified framework that turns each research paper into a complete training environment. PaperGym exploits the structure of a paper: the question is synthesized from the research goal and background, while the criteria are derived from the method and experiments. The criteria span methodological innovation and experimental design, and criterion leakage falls to 3.7%, versus 11.90% to 34.10% in existing datasets. Training uses the rubric twice: first as privileged context for OPSD's self-teacher, then as the reward for GRPO. Across Qwen3-1.7B/4B/8B, this schedule outperforms supervised fine-tuning, either stage alone, and the reverse ordering, improving five-benchmark averages by +5.6, +5.0, and +4.8 points. With the recipe held fixed, models trained on PaperGym-20k win 58.1% of three-way comparisons, against 28.2% for RubricHub Science. The trained Qwen3-8B reaches 73.48 on ResearchQA, above the far larger Kimi K2.6. We release the pipeline, the 20,000-instance corpus PaperGym-20k, and the benchmarks PaperGym-Innov and PaperGym-Design.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。