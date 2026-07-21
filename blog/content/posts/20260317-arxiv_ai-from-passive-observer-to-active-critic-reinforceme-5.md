---
title: 'From Passive Observer to Active Critic: Reinforcement Learning Elicits Process
  Reasoning for Robotic Manipulation'
date: 2026-03-17 20:30:33+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2603.15600v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:917535675d09da38a2b17109bb625f0b7918f058667821f858ddcf10d807807b
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 113
captured_at: '2026-07-18T04:28:30.264258Z'
source_capture_sha256: sha256:af7f07b9de2b79a9745433e4f757d23a9d062d54e834ab26f6b6544778dc7a6a
source_capture_chars_original: 1444
source_publication_excerpt_chars: 1444
observation_id: obs_2752fcb4de75e0e96b47bf6baa64e412aa309fd7938b252d88e0f6429b46e38f
revision_id: rev_80b70b0ea3713bf19cce9982be95d8df67be86d7c5e7730a8cb2bf77742b02d2
event_id: evt_6c0d5b3095ba976b830c5169f5e7bd494789bb02b5192c2eb0a92f0ada378041
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.15600v1](<https://arxiv.org/abs/2603.15600v1>)
- **作者**: Yibin Liu, Yaxing Lyu, Daqi Gao, Zhixuan Liang, Weiliang Tang, Shilong Mu, Xiaokang Yang, Yao Mu
- **分类**: cs.RO
- **论文时间**: 2026-03-16T17:53:28Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.15600v1.pdf](<https://arxiv.org/pdf/2603.15600v1.pdf>)

## 来源摘要/节选

> Accurate process supervision remains a critical challenge for long-horizon robotic manipulation. A primary bottleneck is that current video MLLMs, trained primarily under a Supervised Fine-Tuning \(SFT\) paradigm, function as passive "Observers" that recognize ongoing events rather than evaluating the current state relative to the final task goal. In this paper, we introduce PRIMO R1 \(Process Reasoning Induced Monitoring\), a 7B framework that transforms video MLLMs into active "Critics". We leverage outcome-based Reinforcement Learning to incentivize explicit Chain-of-Thought generation for progress estimation. Furthermore, our architecture constructs a structured temporal input by explicitly anchoring the video sequence between initial and current state images. Supported by the proposed PRIMO Dataset and Benchmark, extensive experiments across diverse in-domain environments and out-of-domain real-world humanoid scenarios demonstrate that PRIMO R1 achieves state-of-the-art performance. Quantitatively, our 7B model achieves a 50% reduction in the mean absolute error of specialized reasoning baselines, demonstrating significant relative accuracy improvements over 72B-scale general MLLMs. Furthermore, PRIMO R1 exhibits strong zero-shot generalization on difficult failure detection tasks. We establish state-of-the-art performance on RoboFail benchmark with 67.0% accuracy, surpassing closed-source models like OpenAI o1 by 6.0%.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
