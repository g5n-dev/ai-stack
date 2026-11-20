---
title: "PlayCraft: Designing Engaging Games from Agent Play Experience"
date: 2026-11-21T04:15:17+08:00
draft: false
entry_kind: "auto"
tags: ["AI Agent", "cs.AI", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:d09b917e666691e3052f3998b811239bebab88aa3e9570265db74611dd77d7af"
source_payload_sha256: "sha256:54dbf70d2bce557bbefb2f9e5ac7bd39b60b9f66471f908e0a5e52adfa089431"
observation_id: obs_1d08b2a6b57ac2c64f5ff9e43ec87a437cffe348358a1a887b28c2291fe526e7
event_id: evt_2e110265f53205f0b1c2e470211877b9d201a15103f2d21fc2bc489e149fae78
revision_id: rev_72de2a0b03f82ed38bfce437ec71380095deaa9504c7435dc6fc69b92f236265
source_published_at: 2026-11-19T18:59:34Z
first_seen_at: 2026-11-20T20:13:50.060865Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 62
interpretation_sha256: "sha256:ed26f2f0bd41d6364da9e6f3efb82634c93989951b66be43b1d4b38ec5df785a"
description: "PlayCraft 是一个自动化游戏改进框架：视觉型玩家智能体通过反复游玩收集过程信息，创作智能体据此调整游戏，以增强玩家的学习收益与掌握体验。"
external_url: http://arxiv.org/abs/2611.26624v1
parent_observation_id: null
last_seen_at: 2026-11-20T20:13:50.060865Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2611.26624v1](http://arxiv.org/abs/2611.26624v1)
- **发布域名**: arxiv.org
- **分类**: cs.AI
- **作者**: Weihao Cheng

## 要点解读

### 这是什么
PlayCraft 是一个自动化游戏改进框架：视觉型玩家智能体通过反复游玩收集过程信息，创作智能体据此调整游戏，以增强玩家的学习收益与掌握体验。

### 用在哪里
它适用于改进 AI 生成的游戏，尤其适合游戏设计者和智能体开发者，在测试阶段利用玩家智能体自动评估并迭代游戏。

### 可以推断的
- 推测：该方法可能减少人工试玩与反复调优的工作，但实际效果仍取决于具体实现。
- 推测：以智能体体验作为反馈，可能提高游戏改进过程的可量化程度，但与真人玩家感受是否一致仍需验证。

## 来源摘要/节选

> Recent AI agents can generate playable games, but these games are not necessarily engaging. Mastery is a key source of engagement, yet designing for it requires extensive human play and tuning. We propose PlayCraft, an automated framework that uses a vision-based agent to play games and draws on its detailed play experience to revise them for mastery. Starting from an initial game, PlayCraft alternates between playing and crafting. In the playing stage, a player agent watches the game screen, uses the controls, and pursues the game objective over repeated episodes while retaining memory. After each episode, it reports its progress, outcomes, decisions, and reflections. In the crafting stage, a crafter agent uses these reports to revise the game. It estimates player abilities, predicts performance at different proficiency levels, and compares those predictions with a target learning progression. It diagnoses the game and addresses the gaps by giving players meaningful opportunities to improve through better decisions and execution. We evaluate games in fresh runs with player agents across three intelligence settings, measuring learning gain and learning slope. Compared with the initial games, PlayCraft yields larger learning gains and steeper learning slopes in most games. It also outperforms the baselines on the macro-average of each metric at every intelligence setting.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。