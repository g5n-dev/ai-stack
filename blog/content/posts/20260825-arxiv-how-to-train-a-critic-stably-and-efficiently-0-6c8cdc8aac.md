---
title: "How to Train a Critic Stably and Efficiently"
date: 2026-08-25T11:48:42+08:00
draft: false
entry_kind: "auto"
tags: ["Prompt 工程", "cs.LG", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:7ff76c0779beb21f87c00af30e6eac9a00f296d20ac91d0c9185d79c20c2f453"
source_payload_sha256: "sha256:7f1b1b83fc6413c764f3480270004e4c8db0d323e6150867456b0cb9074eaa53"
observation_id: obs_6c8cdc8aac26a2e89707a7b627656ef2c28306f48c70b1e8d7eb2b3a40ca9f31
event_id: evt_69bfa03023eb09188f9b245801794260b34a72463178ab5c14f1bfe79c1f1e17
revision_id: rev_13e25ea74ab477f47ec66f344e1da64f0df3234c543e10c4660cc11f246335f8
source_published_at: 2026-08-24T17:59:39Z
first_seen_at: 2026-08-25T04:10:27Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 44
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2608.23566v1
parent_observation_id: null
last_seen_at: 2026-08-25T03:46:13.922365Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.23566v1](http://arxiv.org/abs/2608.23566v1)
- **发布域名**: arxiv.org
- **分类**: cs.LG
- **作者**: Penghui Qi、Xiangxin Zhou、Wee Sun Lee

## 来源摘要/节选

> Group-based reinforcement learning methods such as GRPO for large language models avoid training a critic by sampling multiple responses for each prompt. A reliable critic could instead estimate token-level advantages from one response, but standard critic-based training recipes are often unstable. We study this instability and develop \textbf{Best-Practice Critic Optimization (BPCO)}, a recipe that combines DPPO, value predictions bounded to the reward range, Monte Carlo value targets, unnormalized policy advantages, and length-adaptive generalized advantage estimation. Because the critic is used only during training, BPCO can also condition it on reward-defining information, such as a reference answer or grading rubric, that is hidden from the policy. Controlled experiments isolate the effect of each design choice. Across mathematical reasoning tasks with models ranging from 1.5B parameters to 30B-A3B mixtures of experts, BPCO improves a strong critic-based baseline consistently, and matches or exceeds a group-based baseline while sampling one response per prompt. The same recipe also improves learning with rubric-based rewards. These results show that a carefully designed critic provides a reliable alternative to group-relative advantage estimation. Code is available at https://github.com/QPHutu/golden_critic

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。