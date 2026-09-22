---
title: "GameHorizon Suite: Multi-Horizon Data and Evaluation in Gameplay"
date: 2026-09-22T17:58:49+08:00
draft: false
entry_kind: "auto"
tags: ["计算机视觉", "cs.CV", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:38050abaa47ec3ebac23abb891252b37b4f4a13f77c46fcf4f77684e68c501a7"
source_payload_sha256: "sha256:a86b93f10a34805590e0bf3b7adbee010ca001d0f5503f7a3b2d110e19af9977"
observation_id: obs_8608f274b3e702c75696f23c27a92308fc549cf4cd57309f3f11dd041739630b
event_id: evt_d5ac22170926d91b12fd5e5612cd213f5f41d00109f05d3791dd89647f35ffdf
revision_id: rev_6eb3db0be2785bd2f5baa7ae3d85cdfa38cfda866691d8c83f9db40d29285b22
source_published_at: 2026-09-21T17:59:33Z
first_seen_at: 2026-09-22T09:56:54.486583Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 64
interpretation_sha256: "sha256:f93ff6147791db78b7e775ae5b338f23bd2604f4e920a23a1c151d0b2013cc1a"
description: "它是一套针对视频游戏的多时间跨度数据和评测框架，包含自动化标注流程、大规模游戏录像与指令集合，以及可重复的离线与逐步在线评估模块。"
external_url: http://arxiv.org/abs/2609.25001v1
parent_observation_id: null
last_seen_at: 2026-09-22T09:56:54.486583Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.25001v1](http://arxiv.org/abs/2609.25001v1)
- **发布域名**: arxiv.org
- **分类**: cs.CV
- **作者**: Yiran Wang、Xingyilang Yin、Junfu Pu 等

## 要点解读

### 这是什么  
它是一套针对视频游戏的多时间跨度数据和评测框架，包含自动化标注流程、大规模游戏录像与指令集合，以及可重复的离线与逐步在线评估模块。  

### 用在哪里  
适合需要评估模型在游戏中跨时长任务表现的研究者，也适合想构建或对比多模型游戏AI基准的团队。  

### 可以推断的  
- 推测：离线评测通过大量标准化问题实现可重复的模型对比。  
- 推测：大规模录像库可能帮助模型学习不同游戏中的长期策略与动作映射。

## 来源摘要/节选

> Modern video games provide a measurable testbed for AI models, combining abilities of visual understanding, instruction decomposition, goal planning, and precise action control over multiple temporal horizons. Existing datasets and benchmarks, however, either cover a narrow range of games, lack language instructions, or rely on high-variance online rollouts. To address these challenges, we introduce GameHorizon, a unified data and evaluation suite that measures gameplay capabilities at different horizons for diverse model families. GameHorizon Suite consists of three components. First, GameHorizon-Annotator is a scalable and automated annotation pipeline for multi-horizon instructions. Second, utilizing the pipeline, we construct GameHorizon-Data, the first large-scale AAA gameplay dataset with temporally aligned videos, player actions, and multi-horizon instructions. It comprises 5,000 hours of recordings from 21 games, collected by 100 human expert players. Third, we build GameHorizon-Bench with reproducible offline and stepwise online testing. The offline track enables reproducible evaluation using thousands of standardized questions organized into three primary tasks and a series of diagnostic variants, while the online track tests whether offline scores reflect actual gameplay capabilities and localizes failures to specific steps within long-horizon gameplay. Based on our GameHorizon Suite, we evaluate 47 models through more than one million model invocations, revealing a meaningful hierarchy of task difficulty and pronounced differences in model capabilities. Our work can provide a standardized yardstick for evaluating gameplay capabilities across horizons and model families. We will release our dataset, annotator, and benchmark to facilitate future research.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。