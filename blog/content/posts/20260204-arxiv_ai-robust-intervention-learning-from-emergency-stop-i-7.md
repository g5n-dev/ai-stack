---
title: Robust Intervention Learning from Emergency Stop Interventions
date: 2026-02-04 23:12:07+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.03825v1
aliases:
- /posts/20260205-arxiv_ai-robust-intervention-learning-from-emergency-stop-i-7/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:f66ec2f656e5e6a7ec563c0c952b6173c709977a36fc811d6a5511daaed71220
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 62
captured_at: '2026-07-18T04:10:41.702374Z'
source_capture_sha256: sha256:9b43928d088785782471455e842ffd9accf79be9940b1f6ad2eaa402d0ddba23
source_capture_chars_original: 1539
source_publication_excerpt_chars: 1539
observation_id: obs_fd80d62d1f39b0a0fd4a5410b3662d0f455e1ebf2a3d139177d15fd8bc98cb57
revision_id: rev_b58edf3ac6aad65b7deddd4c4406fe4386f2854a2f226b7a8c9686724d8c58eb
event_id: evt_de51a8d253f59630da6b86009b22eae5e72c74c302ad971209cd5865f2208d67
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-04T05:02:40Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.03825v1](<https://arxiv.org/abs/2602.03825v1>)
- **作者**: Ethan Pronovost, Khimya Khetarpal, Siddhartha Srinivasa
- **分类**: cs.LG
- **论文时间**: 2026-02-03T18:33:21Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.03825v1.pdf](<https://arxiv.org/pdf/2602.03825v1.pdf>)

## 来源摘要/节选

> Human interventions are a common source of data in autonomous systems during testing. These interventions provide an important signal about where the current policy needs improvement, but are often noisy and incomplete. We define Robust Intervention Learning \(RIL\) as the problem of learning from intervention data while remaining robust to the quality and informativeness of the intervention signal. In the best case, interventions are precise and avoiding them is sufficient to solve the task, but in many realistic settings avoiding interventions is necessary but not sufficient for achieving good performance. We study robust intervention learning in the context of emergency stop interventions and propose Residual Intervention Fine-Tuning \(RIFT\), a residual fine-tuning algorithm that treats intervention feedback as an incomplete learning signal and explicitly combines it with a prior policy. By framing intervention learning as a fine-tuning problem, our approach leverages structure encoded in the prior policy to resolve ambiguity when intervention signals under-specify the task. We provide theoretical analysis characterizing conditions under which this formulation yields principled policy improvement, and identify regimes where intervention learning is expected to fail. Our experiments reveal that residual fine-tuning enables robust and consistent policy improvement across a range of intervention strategies and prior policy qualities, and highlight robust intervention learning as a promising direction for future work.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
