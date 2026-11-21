---
title: "PlayCraft: Designing Engaging Games from Agent Play Experience"
date: 2026-11-21T09:32:07+08:00
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
first_seen_at: 2026-11-21T01:30:50.329324Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 62
interpretation_sha256: "sha256:6d4bb7109cdb1a5f4b7a8f0e9f119a3d4fb1e2e5cfb5ae382e0581240ce095b5"
description: "PlayCraft 是一种自动化游戏设计框架，通过视觉代理反复试玩并记录决策、进展与反思，再据此修改游戏，使玩家获得更有意义的练习机会，逐步提升能力。"
external_url: http://arxiv.org/abs/2611.26624v1
parent_observation_id: null
last_seen_at: 2026-11-21T01:30:50.329324Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2611.26624v1](http://arxiv.org/abs/2611.26624v1)
- **发布域名**: arxiv.org
- **分类**: cs.AI
- **作者**: Weihao Cheng

## 要点解读

### 这是什么
PlayCraft 是一种自动化游戏设计框架，通过视觉代理反复试玩并记录决策、进展与反思，再据此修改游戏，使玩家获得更有意义的练习机会，逐步提升能力。

### 用在哪里
它适用于需要提升游戏可玩性与“掌握感”的游戏设计和迭代场景，尤其适合希望减少人工试玩与调参工作的人。

### 可以推断的
- 推测：让玩家代理承担试玩和反馈角色，可能帮助设计者更快发现影响学习体验的游戏问题。
- 推测：以学习增益和学习斜率评估设计效果，有助于比较不同游戏版本是否更容易促成能力提升。

## 来源摘要/节选

> Recent AI agents can generate playable games, but these games are not necessarily engaging. Mastery is a key source of engagement, yet designing for it requires extensive human play and tuning. We propose PlayCraft, an automated framework that uses a vision-based agent to play games and draws on its detailed play experience to revise them for mastery. Starting from an initial game, PlayCraft alternates between playing and crafting. In the playing stage, a player agent watches the game screen, uses the controls, and pursues the game objective over repeated episodes while retaining memory. After each episode, it reports its progress, outcomes, decisions, and reflections. In the crafting stage, a crafter agent uses these reports to revise the game. It estimates player abilities, predicts performance at different proficiency levels, and compares those predictions with a target learning progression. It diagnoses the game and addresses the gaps by giving players meaningful opportunities to improve through better decisions and execution. We evaluate games in fresh runs with player agents across three intelligence settings, measuring learning gain and learning slope. Compared with the initial games, PlayCraft yields larger learning gains and steeper learning slopes in most games. It also outperforms the baselines on the macro-average of each metric at every intelligence setting.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。