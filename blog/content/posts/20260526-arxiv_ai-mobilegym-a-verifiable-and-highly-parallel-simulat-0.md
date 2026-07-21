---
title: 'MobileGym: A Verifiable and Highly Parallel Simulation Platform for Mobile
  GUI Agent Research'
date: 2026-05-26 18:44:28+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
- AI Agent
categories:
- 论文
scenarios:
- AI/ML项目
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2605.26114v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:90d847e1c8c8ad82ae4d05da9f5ccd0a128e7eb156298aacd75350ec69a90d55
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 93
captured_at: '2026-07-18T04:29:43.284780Z'
source_capture_sha256: sha256:145c7012fb15a85b203924ecd559c8b20d18b51bf79805a6751fec75d6f68dec
source_capture_chars_original: 1385
source_publication_excerpt_chars: 1385
observation_id: obs_1f01bf8081c728c708d7a3bd61b1d4895f194a10d103f47b0ed86cc9561080ff
revision_id: rev_0a1e680c5808b591bf7b05331fde472c8c0913ee08e0e6c2edaef3483053e31c
event_id: evt_bf4790afcd23f7f20fe5e146855df35914483c587a48f140e26bc7fc231beab0
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2605.26114v1](<https://arxiv.org/abs/2605.26114v1>)
- **作者**: Dingbang Wu, Rui Hao, Haiyang Wang, Shuzhe Wu, Han Xiao, Zhenghong Li, Bojiang Zhou, Zheng Ju, Zichen Liu, Lue Fan, Zhaoxiang Zhang
- **分类**: cs.AI
- **论文时间**: 2026-05-25T17:59:49Z
- **论文 PDF**: [https://arxiv.org/pdf/2605.26114v1.pdf](<https://arxiv.org/pdf/2605.26114v1.pdf>)

## 来源摘要/节选

> We present MobileGym, a browser-hosted, lightweight, fully controllable environment for everyday mobile use, targeting interaction fidelity without replicating proprietary backends. It enables two capabilities previously out of reach for everyday apps: verifiable outcome signals through deterministic state-based judging over structured JSON state, and scalable online RL through low-cost parallel rollouts. The full environment state is captured, configured, forked, and compared as structured JSON, and a single server can host hundreds of parallel instances, with about 400 MB memory per instance and about 3 s cold start. A layered state model and a declarative task-definition framework keep state programmability and task creation practical at scale, and a single programmatic judging mechanism delivers both deterministic evaluation verdicts and dense RL rewards. The accompanying MobileGym-Bench provides 416 parameterized task templates, including 256 test and 160 train templates, over 28 apps, with deterministic judges and a structured AnswerSheet protocol that avoids free-text matching failures. In a Sim-to-Real case study, GRPO on Qwen3-VL-4B-Instruct gains +12.8 percentage points on the 256-task test set, and on a 59-task real-device signal subset, real-device execution retains 95.1% of the simulation-side training gain. Project page: https://mobilegym.github.io.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
