---
title: "WorldCup Arena: Prospective, Leakage-Free Evaluation of Frontier LLMs on a Live Tournament"
date: 2026-08-05T17:50:46+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "cs.CL", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:79e276e866c4914612d11437f9e89a525099f383d4178731f9d08e888718dd77"
source_payload_sha256: "sha256:bcc2f2732ea50c8940ff7aec6d8ce0b2f6cc784aa9bb1d821f551a924176623f"
observation_id: obs_399723c4f15a073fa9f60a86e93a2232fed924cebf42616e39647893cf339b0e
event_id: evt_cfb4a26716754407193d824ca10621ac0e6ff979809ecc85511f9e1804f646cf
revision_id: rev_67c335c4ecbabc13a85e7b70cba6f68f25e0fc7f6e7d587a71820e22d764a458
source_published_at: 2026-08-04T17:59:55Z
first_seen_at: 2026-08-05T09:49:00.835524Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 90
interpretation_sha256: "sha256:b26360c3e3077443e4f83ee9b5617729c7521fd7af485f2f1d076a1d3b8273b7"
description: "在2026年世界杯的赛期（39 天）里，六款具备扩展思考和服务器端搜索功能的前沿大语言模型在每场比赛开球前填写七市场预测卡，涵盖104场小组赛、12支小组冠军以及赛前全赛预测。提问时答案尚未出现，评估因此实现了无泄漏的前瞻性，冻结档案保留了4 494条已评分预测。"
external_url: http://arxiv.org/abs/2608.04008v1
parent_observation_id: null
last_seen_at: 2026-08-05T09:49:00.835524Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.04008v1](http://arxiv.org/abs/2608.04008v1)
- **发布域名**: arxiv.org
- **分类**: cs.CL
- **作者**: Zhenran Wang、Zhonghan Bian、Jinsong Li 等

## 要点解读

### 这是什么  
在2026年世界杯的赛期（39 天）里，六款具备扩展思考和服务器端搜索功能的前沿大语言模型在每场比赛开球前填写七市场预测卡，涵盖104场小组赛、12支小组冠军以及赛前全赛预测。提问时答案尚未出现，评估因此实现了无泄漏的前瞻性，冻结档案保留了4 494条已评分预测。  

### 用在哪里  
适用于需要验证大模型在真实、尚未发生事件上的预测能力的研究场景，特别是体育比赛、金融走势或舆论热点等前瞻预测任务；也可以作为构建和发布类似公开基准的参考。  

### 可以推断的  
推测：在实时预测任务中，模型通常倾向于押注人气最高的选项，导致对平局或低概率结果的预测偏少。  
推测：若在此类任务中加入投票机制，可能难以显著提升整体准确率，因为模型的错误模式高度相似。

## 来源摘要/节选

> Benchmarks that measure the forecasting ability of large language models are almost always retrospective: the event has happened, the answer is somewhere on the Web, and the evaluation must defend itself against memorisation. We report the opposite design. Over the 39 days of the 2026 FIFA World Cup, six frontier LLMs -- all with extended thinking and native server-side web search -- were asked before every kickoff, one match at a time, to fill in a seven-market prediction card for all 104 matches, plus 12 group winners and a pre-tournament outright pool; no answer existed when the question was asked, so the evaluation is leakage-free by construction rather than by filtering, and the frozen archive holds 4,494 scored predictions. What the tournament establishes is a set of behaviours the six systems share. On match outcome they average 63.9%, level with backing the bookmaker's favourite -- which is in fact what they usually do. They agree with one another far more often than they are right, so a majority vote adds nothing. They under-commit to draws and to goals, and crowd their scoreline picks onto a single prototypical result. Accuracy tracks how lopsided a fixture is rather than how much is known about it: it collapses in the closest ties, where the dossiers are richest, while questions about the tournament as a whole are answered well. On this task the current generation of frontier systems is not sharply differentiated: the standings hold up at the top and the bottom across the run and churn in the middle, and the margins stay narrow throughout. The briefing dossiers, fixtures and official results are released as a benchmark, together with the scoring code.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。