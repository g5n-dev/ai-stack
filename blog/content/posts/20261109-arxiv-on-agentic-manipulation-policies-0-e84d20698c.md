---
title: "On Agentic Manipulation Policies"
date: 2026-11-09T15:59:24+08:00
draft: false
entry_kind: "auto"
tags: ["AI Agent", "cs.RO", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:0f1e148e730f5685903abdc2445bb2e1bba86ee8b430bf31dbb9cef1336842db"
source_payload_sha256: "sha256:932f5ce7fcfd3fb3b4536c174cc3496687c987bfc136bbc68dd30b33fe9d9d68"
observation_id: obs_e84d20698cc7a671e7a864639f81f91bee039005171bf8245447f998da81dbf3
event_id: evt_faf58236b331ffac5ab0cdc2acb63d4c41855c34dd9ed6b2677daf422a32e373
revision_id: rev_4aa55a372c5ba5088a603bfb91339093d155c1e26904d280cd97dec2b3550538
source_published_at: 2026-11-06T18:59:34Z
first_seen_at: 2026-11-09T07:57:40.464126Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 32
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2611.09892v1
parent_observation_id: null
last_seen_at: 2026-11-09T07:57:40.464126Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2611.09892v1](http://arxiv.org/abs/2611.09892v1)
- **发布域名**: arxiv.org
- **分类**: cs.RO
- **作者**: Chen Chen、Omid Bagherieh、Naveen Nikamanth Appiah Balaji 等

## 来源摘要/节选

> Recent work on robot manipulation has focused on specialist policies trained on demonstrations. We show that generalist AI models can control manipulators more reliably than specialist policies such as vision-language-action models (VLAs) and world-action models (WAMs). We systematically analyze agentic manipulation policies (AMPs), in which a generalist AI model commands the manipulator directly, adapting its actions as the task unfolds. We present AMP1, a reference harness that runs unchanged across single-arm, bimanual, and mobile manipulation. AMP1 achieves state-of-the-art results on the RoboLab-120 and CaP-Gym benchmarks, with no demonstrations or task-specific training. On RoboLab-120, AMP1 reaches an 85.6\% success rate zero-shot, compared to 49.2\% and 42.9\% for leading VLA and WAM policies. The agent succeeds zero-shot in 104 of 108 real-world trials spanning twelve tasks and three robot instances, reducing failure rates by 20x and 15x relative to strong VLA and WAM baselines. The basic harness supplies no grasping, pushing, or placing skills; the agent develops its own strategies, such as searching for hidden objects, using objects as tools, and calibrating its cameras. With the addition of a persistent memory store, the agent can also learn from experience: an augmented harness with a memory representation that is carried across episodes lowers the failure rate on RoboDojo bimanual manipulation tasks by 4.6x relative to zero-shot deployment. Our analysis suggests that AMPs are substantially more general and robust than specialist manipulation policies, providing a promising foundation for robot manipulation.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。