---
title: Efficient Reasoning on the Edge
date: 2026-03-18 08:22:04+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
- 大语言模型
categories:
- 论文
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2603.16867v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:9393de84ef8d59e60056bfa0bc1628f30f67427e15183e8c366e586f56c1d290
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 31
captured_at: '2026-07-18T04:28:45.482788Z'
source_capture_sha256: sha256:ac687206e2c63b3c9ef1d539841f97aa8d5c1dd6c7e923b583ed7c69baedc5f0
source_capture_chars_original: 1503
source_publication_excerpt_chars: 1503
observation_id: obs_ee66768575c0a1d00aadc80aee81bf939275ace67eb5d6c254eaaf9f659b31b5
revision_id: rev_1d252bac4297ff65e36b0f057c6b24a465346aaf80416331b44180285a87aae2
event_id: evt_367f2f3db54158cd03be0a90461b7db303e5eb3e566455afc4819967669c7814
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-03-18T04:20:43Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.16867v1](<https://arxiv.org/abs/2603.16867v1>)
- **作者**: Yelysei Bondarenko, Thomas Hehn, Rob Hesselink, Romain Lepert, Fabio Valerio Massoli, Evgeny Mironov, Leyla Mirvakhabova, Tribhuvanesh Orekondy, Spyridon Stasis, Andrey Kuzmin, Anna Kuzina, Markus Nagel, Ankita Nayak, Corrado Rainone, Ork de Rooij, Paul N Whatmough, Arash Behboodi, Babak Ehteshami Bejnordi
- **分类**: cs.LG
- **论文时间**: 2026-03-17T17:59:51Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.16867v1.pdf](<https://arxiv.org/pdf/2603.16867v1.pdf>)

## 来源摘要/节选

> Large language models \(LLMs\) with chain-of-thought reasoning achieve state-of-the-art performance across complex problem-solving tasks, but their verbose reasoning traces and large context requirements make them impractical for edge deployment. These challenges include high token generation costs, large KV-cache footprints, and inefficiencies when distilling reasoning capabilities into smaller models for mobile devices. Existing approaches often rely on distilling reasoning traces from larger models into smaller models, which are verbose and stylistically redundant, undesirable for on-device inference. In this work, we propose a lightweight approach to enable reasoning in small LLMs using LoRA adapters combined with supervised fine-tuning. We further introduce budget forcing via reinforcement learning on these adapters, significantly reducing response length with minimal accuracy loss. To address memory-bound decoding, we exploit parallel test-time scaling, improving accuracy at minor latency increase. Finally, we present a dynamic adapter-switching mechanism that activates reasoning only when needed and a KV-cache sharing strategy during prompt encoding, reducing time-to-first-token for on-device inference. Experiments on Qwen2.5-7B demonstrate that our method achieves efficient, accurate reasoning under strict resource constraints, making LLM reasoning practical for mobile scenarios. Videos demonstrating our solution running on mobile devices are available on our project page.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
