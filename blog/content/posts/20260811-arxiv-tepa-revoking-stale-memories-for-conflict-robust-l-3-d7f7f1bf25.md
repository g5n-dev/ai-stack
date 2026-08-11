---
title: "TEPA: Revoking Stale Memories for Conflict-Robust Language Agents"
date: 2026-08-11T06:58:58+08:00
draft: false
entry_kind: "auto"
tags: ["AI Agent", "Prompt 工程", "cs.AI", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:10a28f6cce85472a25639eedff0fbef582e9cc8ac76710798eb4123772b037a1"
source_payload_sha256: "sha256:4417da3a0961f9df8d457db2dd143a43968c5dc647754f2c6abce05df22314b6"
observation_id: obs_d7f7f1bf25c4ce7662f3afc99979d783e616d05dc5fc63edc4d826cdef57e33d
event_id: evt_84a7914252ab19c1bf85bdf3bbf15ebe102cb17b5b60ebc40e303183d2aec159
revision_id: rev_2ced04cff83b8a560d23f1769cbe2bb147473776e94e87552b7568f927853437
source_published_at: 2026-08-07T17:16:33Z
first_seen_at: 2026-08-10T23:08:53Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 65
interpretation_sha256: "sha256:bd775b368e62e9dacd820a66b99638e5a446f58c1e0d25a07c53e98f79a972bd"
description: "这是一种针对语言代理的长期记忆系统，通过将记忆设为可撤销状态并在出现冲突新证据时自动清除失效记忆，来解决记忆污染问题。该机制以键控先例表示观察结果，并在同一键下新证据出现时撤销已有先例，以保持检索结果时效性。"
external_url: http://arxiv.org/abs/2608.07429v1
parent_observation_id: null
last_seen_at: 2026-08-10T22:56:33.983975Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.07429v1](http://arxiv.org/abs/2608.07429v1)
- **发布域名**: arxiv.org
- **分类**: cs.AI
- **作者**: Yan Zhou、Yue Ouyang、Kaiyang Zheng 等

## 要点解读

### 这是什么
这是一种针对语言代理的长期记忆系统，通过将记忆设为可撤销状态并在出现冲突新证据时自动清除失效记忆，来解决记忆污染问题。该机制以键控先例表示观察结果，并在同一键下新证据出现时撤销已有先例，以保持检索结果时效性。

### 用在哪里
可用于需要在信息快速变化环境中保持记忆一致的代理系统，例如处理文件、执行任务或响应用户偏好更新的场景。

### 可以推断的
推测：在多跳推理场景下，仅靠记忆层面的撤销可能不足以消除上下文选择错误，需要结合检索链路的改进。  
推测：将撤销机制与其他记忆管理策略（如分层缓存或版本控制）结合，可进一步提升系统在高动态环境中的鲁棒性。

## 来源摘要/节选

> Long-term memory enables language agents to reuse past facts, preferences, and task experience. Persistence also creates a central falsifiability problem: when the world changes, stale memories can remain retrievable and pollute the prompt. We characterize this failure mode as memory pollution: degradation caused by active memories that newer conflicting evidence has superseded. We introduce TEPA, a revocable evidence-memory mechanism that makes validity an explicit state of memory. TEPA represents observations as keyed precedents and revokes active precedents when fresh evidence contradicts them under the same key, allowing retrieval to draw from current evidence while preserving revoked history for audit. Across controlled hidden-regime drift, real file-backed executable drift, and preference-update streams, revocation prevents stale active memory from remaining in the retrieval set after reversal. In controlled drift over 50 seeds, append-only and last-write-wins memory fell below no memory during full reversal (append-only and last-write-wins both 0.210, no memory 0.309, TEPA 0.950), and the same pattern reproduced under real file execution (append-only 0.203, no memory 0.298, TEPA 0.950). On clean MemoryAgentBench SH-6k, TEPA matches a strong last-write-wins cache, confirming that current-key replacement is the decisive operation for single-hop fact consolidation. Boundary tests on multi-hop and very long-context MemoryAgentBench settings expose retrieval-chain and context-selection bottlenecks beyond fact-level validity tracking. Together, these results establish lifecycle revocation as a core memory operation for agents that must falsify, audit, and later re-promote evolving knowledge.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。