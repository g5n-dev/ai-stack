---
title: "SpeakerMem-R1: Speaker-Centered Dual-Track Memory for Multi-Party Dialogue"
date: 2026-09-24T00:58:45+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "cs.CL", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:6c058f1950558a939d2b189b0c14ef433ea2ee70d49efd189e75e17bdca81dc8"
source_payload_sha256: "sha256:f28c0feea4eb87b2b3a7ab2a40aa323a9752762d3a4ad10a89c73675f92a7760"
observation_id: obs_1ef9cc7a7ec923797fc1bd29a3c2ab6a522a776263cef1f59259746ade101f06
event_id: evt_da7aa4ad280288b6f66b37a4ea5628e06663c9809b03dfff8ab11376599a0281
revision_id: rev_0db6870f20f5844082fd774612c5f09eb2d918499eca53852b18243af39e0057
source_published_at: 2026-09-22T17:56:12Z
first_seen_at: 2026-09-23T17:09:32Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 74
interpretation_sha256: "sha256:d19cea9ee30c30c3d62f918edb9886971fb1b7d994e041fdd80e991de5cf9deb"
description: "该文提出一种面向多方对话的双轨记忆框架，一轨保存说话者的原始语句，另一轨提取并维护人物级和群体级的状态信息，在查询时依据实体、事件和时间将两轨证据融合，以解决对话中角色归属和关系演化的难题。"
external_url: http://arxiv.org/abs/2609.26780v1
parent_observation_id: null
last_seen_at: 2026-09-23T16:56:53.208812Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.26780v1](http://arxiv.org/abs/2609.26780v1)
- **发布域名**: arxiv.org
- **分类**: cs.CL
- **作者**: Haobo Zheng、Tan Tang、Yan Chen 等

## 要点解读

### 这是什么
该文提出一种面向多方对话的双轨记忆框架，一轨保存说话者的原始语句，另一轨提取并维护人物级和群体级的状态信息，在查询时依据实体、事件和时间将两轨证据融合，以解决对话中角色归属和关系演化的难题。

### 用在哪里
适用于需要在长时间多人交互中持续追踪谁说了什么、如何影响彼此以及群体信息变化的对话系统，如社交机器人、协作工具或客服平台。对关注对话记忆、关系建模及多轮交互的研发人员和技术研究者具有参考价值。

### 可以推断的
推测：在多方对话场景中，清晰区分每条消息的说话者是保证记忆准确性的基础。  
推测：通过将原始文本与结构化状态分层管理，可以在更新记忆时避免因局部修改导致整体上下文丢失。

## 来源摘要/节选

> Long-term conversational memory in multi-party settings requires more than retrieving relevant content from long-term conversations: it must distinguish who said what, whom each statement concerns, how individuals perceive one another, what information is shared by the group, and how states change over time. Recent studies on multi-party dialogue benchmarks show that existing general-purpose LLM memory systems tend to lose person and group relations or struggle to integrate clues distributed across members, groups, and time. Together, these issues reveal two core bottlenecks: message attribution and relational understanding in multi-party dialogue, and state reconstruction from interleaved histories. To address both, we propose $\textbf{SpeakerMem-R1}$: its dual-track memory stores speaker-labeled verbatim messages and derived states organized into person-level and group-level views, then combines evidence from both tracks by entity, event, and time at query time. To reduce attribution and update errors during structured memory construction while enabling local deployment, we train Writer-R1 with SpeakerLevenshtein and speaker-conditioned GRPO. On GroupMemBench, SocialMemBench, and EverMemBench, SpeakerMem-R1 achieves binary accuracies of 47.9%, 69.2%, and 61.9%, respectively. On the publicly reported EverMemBench leaderboard from EverMind-AI, we achieves 62.33%, the best reported result among the latest state-of-the-art frameworks. It also achieves 70.85% on all 1,986 LoCoMo questions, which we use as a two-person long-term conversation boundary test. In a controlled evaluation of 305 questions, RL raises the SFT Writer's mean accuracy from 57.38% to 68.20%. We report both binary accuracy and token-F1, and ablations show that the verbatim and structured tracks, as well as person-level and group-level views, are complementary under the standardized evaluation interface.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。