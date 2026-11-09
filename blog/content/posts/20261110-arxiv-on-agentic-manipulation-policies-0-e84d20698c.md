---
title: "On Agentic Manipulation Policies"
date: 2026-11-10T02:48:25+08:00
draft: false
entry_kind: "auto"
tags: ["AI Agent", "cs.RO", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:0f1e148e730f5685903abdc2445bb2e1bba86ee8b430bf31dbb9cef1336842db"
source_payload_sha256: "sha256:932f5ce7fcfd3fb3b4536c174cc3496687c987bfc136bbc68dd30b33fe9d9d68"
observation_id: obs_e84d20698cc7a671e7a864639f81f91bee039005171bf8245447f998da81dbf3
event_id: evt_faf58236b331ffac5ab0cdc2acb63d4c41855c34dd9ed6b2677daf422a32e373
revision_id: rev_4aa55a372c5ba5088a603bfb91339093d155c1e26904d280cd97dec2b3550538
source_published_at: 2026-11-06T18:59:34Z
first_seen_at: 2026-11-09T18:46:46.127493Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 32
interpretation_sha256: "sha256:b898967ab91abd6ef2c601cb0291238bffddbcf00d948cf0ccf710c74ab0ac4b"
description: "这项研究提出智能体式操作策略（AMPs）：由通用 AI 模型直接操控机械臂，并根据任务进展动态调整动作。作者设计了可跨单臂、双臂和移动操作运行的 AMP1，在多项仿真基准及真实机器人测试中优于专家示范训练的策略。"
external_url: http://arxiv.org/abs/2611.09892v1
parent_observation_id: null
last_seen_at: 2026-11-09T18:46:46.127493Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2611.09892v1](http://arxiv.org/abs/2611.09892v1)
- **发布域名**: arxiv.org
- **分类**: cs.RO
- **作者**: Chen Chen、Omid Bagherieh、Naveen Nikamanth Appiah Balaji 等

## 要点解读

### 这是什么
这项研究提出智能体式操作策略（AMPs）：由通用 AI 模型直接操控机械臂，并根据任务进展动态调整动作。作者设计了可跨单臂、双臂和移动操作运行的 AMP1，在多项仿真基准及真实机器人测试中优于专家示范训练的策略。

### 用在哪里
它适用于需要零样本泛化、跨机器人形态部署，或希望机器人自主形成抓取、推物、放置等策略的机器人操作任务。研究还表明，为智能体加入跨回合记忆，可进一步改善双臂操作中的可靠性。

### 可以推断的
- 推测：统一的 AMP1 运行框架可能降低为不同机械臂和任务重复开发专用策略的成本。
- 推测：持久记忆与跨回合经验结合，可能比完全零样本部署更适合持续执行、逐步改进的任务。

## 来源摘要/节选

> Recent work on robot manipulation has focused on specialist policies trained on demonstrations. We show that generalist AI models can control manipulators more reliably than specialist policies such as vision-language-action models (VLAs) and world-action models (WAMs). We systematically analyze agentic manipulation policies (AMPs), in which a generalist AI model commands the manipulator directly, adapting its actions as the task unfolds. We present AMP1, a reference harness that runs unchanged across single-arm, bimanual, and mobile manipulation. AMP1 achieves state-of-the-art results on the RoboLab-120 and CaP-Gym benchmarks, with no demonstrations or task-specific training. On RoboLab-120, AMP1 reaches an 85.6\% success rate zero-shot, compared to 49.2\% and 42.9\% for leading VLA and WAM policies. The agent succeeds zero-shot in 104 of 108 real-world trials spanning twelve tasks and three robot instances, reducing failure rates by 20x and 15x relative to strong VLA and WAM baselines. The basic harness supplies no grasping, pushing, or placing skills; the agent develops its own strategies, such as searching for hidden objects, using objects as tools, and calibrating its cameras. With the addition of a persistent memory store, the agent can also learn from experience: an augmented harness with a memory representation that is carried across episodes lowers the failure rate on RoboDojo bimanual manipulation tasks by 4.6x relative to zero-shot deployment. Our analysis suggests that AMPs are substantially more general and robust than specialist manipulation policies, providing a promising foundation for robot manipulation.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。