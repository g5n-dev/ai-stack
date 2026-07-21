---
title: 'MARTI-MARS$^2$: Scaling Multi-Agent Self-Search via Reinforcement Learning
  for Code Generation'
date: 2026-02-10 03:34:40+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
- AI Agent
- 大语言模型
categories:
- 论文
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.07848v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:9a0ffc69a96673a165c27440f084581b45963cc28277cfac11556810dd363f72
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 94
captured_at: '2026-07-18T04:14:28.443184Z'
source_capture_sha256: sha256:cd068d05cf13e5d5f8ca43ae8c1fd6751624b0a2a2994d554587689c44b885c6
source_capture_chars_original: 1820
source_publication_excerpt_chars: 1820
observation_id: obs_84b2d613e6dba563ae104850129bebcc88793aa3414ce16e11e41f5b2938f7ff
revision_id: rev_2b67ad91e7194583a300cb5556475824d0cfde24870b64a1a184d42491d50517
event_id: evt_36d2563b3ca76dedb3a6deb34805047b7e9cce69e82569bbc0263fc42e691f3a
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-10T04:25:57Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.07848v1](<https://arxiv.org/abs/2602.07848v1>)
- **作者**: Shijie Wang, Pengfei Li, Yikun Fu, Kaifeng Liu, Fangyuan Li, Yang Liu, Xiaowei Sun, Zonglin Li, Siyao Zhao, Jian Zhao, Kai Tian, Dong Li, Junqi Gao, Yutong Zhang, Yiqun Chen, Yuqiang Li, Zoe Li, Weinan Zhang, Peng Ye, Shuyue Hu, Lei Bai, Bowen Zhou, Kaiyan Zhang, Biqing Qi
- **分类**: cs.LG
- **论文时间**: 2026-02-08T07:28:44Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.07848v1.pdf](<https://arxiv.org/pdf/2602.07848v1.pdf>)

## 来源摘要/节选

> While the complex reasoning capability of Large Language Models \(LLMs\) has attracted significant attention, single-agent systems often encounter inherent performance ceilings in complex tasks such as code generation. Multi-agent collaboration offers a promising avenue to transcend these boundaries. However, existing frameworks typically rely on prompt-based test-time interactions or multi-role configurations trained with homogeneous parameters, limiting error correction capabilities and strategic diversity. In this paper, we propose a Multi-Agent Reinforced Training and Inference Framework with Self-Search Scaling \(MARTI-MARS2\), which integrates policy learning with multi-agent tree search by formulating the multi-agent collaborative exploration process as a dynamic and learnable environment. By allowing agents to iteratively explore and refine within the environment, the framework facilitates evolution from parameter-sharing homogeneous multi-role training to heterogeneous multi-agent training, breaking through single-agent capability limits. We also introduce an efficient inference strategy MARTI-MARS2-T+ to fully exploit the scaling potential of multi-agent collaboration at test time. We conduct extensive experiments across varied model scales \(8B, 14B, and 32B\) on challenging code generation benchmarks. Utilizing two collaborating 32B models, MARTI-MARS2 achieves 77.7%, outperforming strong baselines like GPT-5.1. Furthermore, MARTI-MARS2 reveals a novel scaling law: shifting from single-agent to homogeneous multi-role and ultimately to heterogeneous multi-agent paradigms progressively yields higher RL performance ceilings, robust TTS capabilities, and greater policy diversity, suggesting that policy diversity is critical for scaling intelligence via multi-agent reinforcement learning.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
