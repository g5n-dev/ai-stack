---
title: "RedEvoAgent: Automatic Red-Teaming Agent with Experience-Driven Skill Evolution"
date: 2026-08-29T22:30:38+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "cs.CR", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:e59b2d8f8dcbc480df0efb08151f3a1a0448c11d83c34f6e3d7ce9115468bfce"
source_payload_sha256: "sha256:2f025db19eec4360d2cede887268a6ee985a103992bb85db0c269bfc5f4de529"
observation_id: obs_104986103cb850f2cb1a7a0a7c829a42e4be2878fcd09c89643f1a7e21d2bb37
event_id: evt_ef82e60dda787d5e1d7d703b1d6c3060b11913cd63b1693978a8ffcca04d1596
revision_id: rev_e3bf4609b16029c339b493283dfe69664f256752cfac37b01cd819ebe524c93d
source_published_at: 2026-08-27T17:55:33Z
first_seen_at: 2026-08-29T14:28:31.368419Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 79
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2608.27439v1
parent_observation_id: null
last_seen_at: 2026-08-29T14:28:31.368419Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.27439v1](http://arxiv.org/abs/2608.27439v1)
- **发布域名**: arxiv.org
- **分类**: cs.CR
- **作者**: Junjie Zhang、Hui Liu、Kecheng Chen 等

## 来源摘要/节选

> LLM-based agents are increasingly deployed in product-level execution harnesses, where jailbreaks can trigger harmful tool use and persistent state changes, creating greater risks than unsafe text generation alone. Existing automatic red-teaming methods often rely on fixed attacks, while recent agentic attackers coordinate multiple jailbreak tools and show stronger potential through trajectory-based retrieval. However, such retrieval can reuse misleading experiences due to retrieval bias and unclear tool credit, and full trajectories add context overhead while reducing interpretability. We propose RedEvoAgent, a black-box red-teaming agent that distills cross-case attack trajectories into a concise, human-readable attack skill. The attack skill adaptively evolves through tool-effectiveness profiling and Deciding-Tool Attribution for skill updates, and a validation ratchet that retains only updates improving validation performance. Experiments on multiple benchmarks, target models, and target execution harnesses show that RedEvoAgent outperforms fixed and agentic baselines, improves tool efficiency, and transfers across attacker models and target execution harnesses.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。