---
title: "Don't Drop the BATON: Long-Horizon Robot Manipulation via Agentic Subtask Exploration and Transition-aware Memory"
date: 2026-08-18T23:52:15+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "cs.RO", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:53af474ca18c561acae2681d3fbb1af332492fe208f7e7176b77fb867a1cdc30"
source_payload_sha256: "sha256:6a09301c3c5c9fce65f45b71bfca2ab337660ccf2391a2c9f2af278e3ff89834"
observation_id: obs_4e48d42ef4f7ad7e7397633a0ba02c443c66561a1e514dfcede3f11380eeb18b
event_id: evt_1eb5de7c81b4b42b22241861dc3870d05deaa271109720ab473254c6d85df791
revision_id: rev_0076901b5753af0d3fe241013db1ba9ced540657c2d47355d0432829d1384c91
source_published_at: 2026-08-17T17:59:57Z
first_seen_at: 2026-08-18T15:50:35.242369Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 113
interpretation_sha256: "sha256:cf55fc8f1f754886b3215b2eed561c05aeef355d37c9d6092ac4847965b838ab"
description: "这是一种针对长时域机器人操作任务的方法，通过将子任务作为探索的基本单元来降低计算成本，并引入转换感知的记忆机制来确保子任务之间的衔接正确。"
external_url: http://arxiv.org/abs/2608.16889v1
parent_observation_id: null
last_seen_at: 2026-08-18T15:50:35.242369Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.16889v1](http://arxiv.org/abs/2608.16889v1)
- **发布域名**: arxiv.org
- **分类**: cs.RO
- **作者**: Bingxin Xu、Yuzhang Shang、Emilio Ferrara

## 要点解读

### 这是什么
这是一种针对长时域机器人操作任务的方法，通过将子任务作为探索的基本单元来降低计算成本，并引入转换感知的记忆机制来确保子任务之间的衔接正确。

### 用在哪里
该方法适用于需要机器人执行多阶段连续操作的实际任务，尤其是涉及接触式技能组合的场景。相关领域的研究人员和技术开发者可以直接参考其思路。

### 可以推断的
推测：在长时域任务中，将复杂的完整任务分解为可独立验证的子任务是一种常见的工程实践，这种分解方式有助于定位和修复问题。

推测：引入转换感知的验证机制意味着系统需要具备场景理解能力，这在实际部署时可能对感知模块的性能有一定要求。

## 来源摘要/节选

> Long-horizon robot manipulation chains many contact-rich skills into one multi-stage task. Vision-language-action (VLA) models increasingly master the individual skills, yet the chain still fails: errors compound beyond the policy's ability to correct, and one subtask silently constrains the next. A promising recipe freezes the VLA and puts an LLM agent in charge: it plans in language, moves in free space with analytic primitives, invokes the VLA only for contact-rich segments, and writes adaptation into language memory. Applied to long horizons, it breaks twice. (1) Competence comes from whole-task exploration at test time, whose cost is multiplicative in stages: if one stage needs T episodes, a K-stage task needs about T^K, and a failure does not reveal which stage caused it. (2) It has no representation of transitions: the VLA primitive carries an exit but no entry condition, so a subtask can succeed in a form its successor cannot use. We present BATON. Against (1), BATON makes the subtask the unit of exploration: each is explored in the cheap short-horizon regime and its solution stored in memory; a long-horizon trajectory is then composed from these solutions rather than discovered whole. Cost becomes additive (T*K) and every failure is attributed to a single stage. Against (2), BATON equips exploration with a transition-aware memory. Within a subtask, a verifier agent governs the invocation transition: the VLA is called only after the wrist view confirms the scene is ready. Across subtasks, a handoff transition restores an entry state disturbed by the predecessor's residue, and a lookahead transition selects the strategy whose outcome the successor can inherit. No parameters are updated. On the long-horizon benchmark RoboMemArena, BATON improves task success by 11.6% and cumulative success by 14.9% over the SoTA.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。