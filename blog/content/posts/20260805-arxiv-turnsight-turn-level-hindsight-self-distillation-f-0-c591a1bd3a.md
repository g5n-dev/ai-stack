---
title: "TurnSight: Turn-Level Hindsight Self-Distillation for Tool-Integrated Reasoning"
date: 2026-08-05T20:17:48+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "cs.CL", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:81ae0fc55e49202a7e961014615ffc47e0a845b7101215c4d5c6c1ceeed7ec83"
source_payload_sha256: "sha256:d44e14f1d5e198293fa33ad887416927d76433cb12c23624a3f402cef4f685cf"
observation_id: obs_c591a1bd3ab58eddc135c7c17daf506870b24da6d3454e4ef030a33f4fd569b8
event_id: evt_7f5ba052ea6026a9f21a7f7f2de61575e2ea8df2be6d2474da25a0448a375a88
revision_id: rev_75950f0be0c32d12876f79ec9dc6de41519ecacf79aa0cdffa7bb86b9fa0c769
source_published_at: 2026-08-04T17:59:21Z
first_seen_at: 2026-08-05T12:27:10Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 79
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2608.04007v1
parent_observation_id: null
last_seen_at: 2026-08-05T12:16:02.146934Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.04007v1](http://arxiv.org/abs/2608.04007v1)
- **发布域名**: arxiv.org
- **分类**: cs.CL
- **作者**: Changle Qu、Sunhao Dai、Hengyi Cai 等

## 来源摘要/节选

> Tool-Integrated Reasoning (TIR) enables LLMs to solve complex tasks through iterative tool interactions. However, existing reinforcement learning methods often rely on trajectory-level supervision, limiting fine-grained credit assignment in long-horizon TIR scenarios. On-policy self-distillation offers denser signals through teacher branches with privileged context, but existing approaches typically derive such context from ground-truth answers or retrieved skills, which may not reflect the states actually visited by the agent. Moreover, token-level supervision fails to capture the turn-level structure of tool interactions. To address this, we propose TurnSight, a turn-level hindsight self-distillation framework that derives supervision directly from execution-conditioned hindsight. It then constructs multiple hindsight views with different lookahead horizons and selects reliable supervision through cross-horizon directional agreement. Finally, the selected hindsight signal is normalized across sibling rollouts and used to adaptively modulate RL advantages while preserving their original optimization direction. Extensive experiments on three benchmarks demonstrate the effectiveness of TurnSight. Our codes are available at https://github.com/quchangle1/TurnSight.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。