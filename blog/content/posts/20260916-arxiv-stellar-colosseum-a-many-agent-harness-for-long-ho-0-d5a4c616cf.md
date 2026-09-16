---
title: "Stellar Colosseum: A Many-Agent Harness for Long-Horizon Research in Mathematics and Theoretical Computer Science"
date: 2026-09-16T08:20:58+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "cs.AI", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:241442616f158e54fa0b3a25e2af5e6adc20ca111e95392ec942c450e32b7ab7"
source_payload_sha256: "sha256:d43f5f0a6644e81c082709c3f88e4687faf8e55ac43ce2df66040c50866b88eb"
observation_id: obs_d5a4c616cf6c1a0c78b61b1ddf9d732351b543d23c4d5d47026463f836877388
event_id: evt_0a01abccb3eb04617af9082e0c53667b11d589ad0c96b9b594db15a39b6df996
revision_id: rev_fcd81a8f17c8251197155321a92ef0a65b51f3fe2be820c16a4f24266bf2a09a
source_published_at: 2026-09-14T17:58:55Z
first_seen_at: 2026-09-16T00:19:06.798593Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 113
interpretation_sha256: "sha256:104515187e044521ad46a2be9b3bc5af13a30d374dca1c06ee9fd9d52fb8ed96"
description: "这是一个用于数学和理论计算机科学领域的研究框架，旨在通过多智能体协作处理需要多步决策的复杂证明问题。框架采用并行生成候选方案、用针对性攻击进行验证、并通过树聚合方式整合不同方案。"
external_url: http://arxiv.org/abs/2609.15983v1
parent_observation_id: null
last_seen_at: 2026-09-16T00:19:06.798593Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.15983v1](http://arxiv.org/abs/2609.15983v1)
- **发布域名**: arxiv.org
- **分类**: cs.AI
- **作者**: Honghao Lin、David P. Woodruff、Yuan Deng 等

## 要点解读

### 这是什么
这是一个用于数学和理论计算机科学领域的研究框架，旨在通过多智能体协作处理需要多步决策的复杂证明问题。框架采用并行生成候选方案、用针对性攻击进行验证、并通过树聚合方式整合不同方案。

### 用在哪里
适用于需要解决开放性数学猜想或理论计算机科学难题的场景。对于正在进行高级数学研究或开发自动定理证明系统的研究团队具有参考价值。

### 可以推断的
- 推测：该框架的运行需要较高的计算资源，因为涉及并行生成多个候选方案并进行交叉验证。
- 推测：这种多智能体协作方式可能为自动化数学推理提供新的解决思路，尤其是在需要探索多条证明路径的复杂问题中。

## 来源摘要/节选

> Language models can produce plausible short proofs, but may still be unreliable on long-horizon research problems, where progress depends on a sequence of uncertain and interdependent decisions. We introduce Stellar Colosseum, a model-agnostic harness for allocating inference across research in mathematics and theoretical computer science. Colosseum explores alternative strategies before proof construction, uses a readiness gate to decide when a route is mature enough to decompose, represents the proof plan as interdependent section-level subproblems, and routes verifier findings back to the affected part of the argument. Across these stages, it generates candidates in parallel, attacks them with targeted falsification, and combines candidates and their critiques into a single research artifact through overlapping random-sample tree aggregation. The Colosseum workflow has also been integrated into Google Antigravity's Teamwork framework as the Long Proof pattern.
> We demonstrate the capabilities of Colosseum through open-ended research and evaluations on theorem-proving and competitive programming benchmarks. Using Colosseum with Gemini 3.1 Pro, we obtain several new results that address open problems arising from papers published at top venues such as FOCS and JMLR. On TCS-Bench, a benchmark of research-level theorem-proving tasks drawn from papers published at FOCS, STOC, and SODA, Colosseum achieves 71.0% accuracy using Gemini 3.1 Pro and Gemini 3.7 Flash. In a separate Codeforces evaluation using Gemini 3.1 Pro, the proof-oriented pipeline with execution feedback solves 218 of 222 problems.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。