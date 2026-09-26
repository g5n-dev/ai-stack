---
title: "RAPID: Robot Agentic Programming from Demonstrations"
date: 2026-09-26T09:36:52+08:00
draft: false
entry_kind: "auto"
tags: ["AI Agent", "cs.RO", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:5cf60fdb3cc00accc54f4d746e9016ae9deaaba6564d384566b1a75d71d3f784"
source_payload_sha256: "sha256:f36d88b72424bcf6b84880743e77fc7443a98b61cd5e4850c046307665f7cf8c"
observation_id: obs_17bc28fb539ceee0c6fb9aef75bc6bb4a80a167bd33a43644bd5b3fc969247fb
event_id: evt_9a92eb7619e5f5ca54028815fefd80fc376f7e2ddbc0118b6c438aaf744d0c95
revision_id: rev_1aca6001124d80fb430f1dbfe3d3cfbfa39e540a7f11e7116862e559c22ca76b
source_published_at: 2026-09-24T17:58:21Z
first_seen_at: 2026-09-26T01:32:57.032334Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 52
interpretation_sha256: "sha256:797898d6dda988d750ef4f68a75f5b4d39a302e1dd6b9618fa6a40809ec056be"
description: "RAPID 是一种仅凭一次视觉示范即可自动生成、验证并改进机器人任务程序的方法，通过迭代式的代码优化循环把示范转化为可执行的策略。"
external_url: http://arxiv.org/abs/2609.30249v1
parent_observation_id: null
last_seen_at: 2026-09-26T01:32:57.032334Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.30249v1](http://arxiv.org/abs/2609.30249v1)
- **发布域名**: arxiv.org
- **分类**: cs.RO
- **作者**: Yuyao Liu、Jiayuan Mao、David Hsu 等

## 要点解读

### 这是什么
RAPID 是一种仅凭一次视觉示范即可自动生成、验证并改进机器人任务程序的方法，通过迭代式的代码优化循环把示范转化为可执行的策略。

### 用在哪里
适用于需要快速为机器人编程的研究或工业场景，尤其是接触丰富、难以抓取的物体操作任务。也能帮助不熟悉代码的研发人员把演示快速转换为可复用的机器人策略。

### 可以推断的
推测：该技术把动作抽象为轨迹优化问题，在运行时依据现场几何关系自动适配，从而在相似任务间具备一定通用性。  
推测：若代码生成与验证环节运行效率足够高，RAPID 有望在真实机器人上实现即时部署，显著降低人工调参的时间成本。

## 来源摘要/节选

> Coding agents have demonstrated enormous success in solving complex programming problems. To leverage their potential for robot systems, this work introduces Robot Agentic Programming from Demonstrations (RAPID), which automatically generates, verifies, and refines robot programs, given a single visual human demonstration. The iterative agentic loop of code refinement requires several key ingredients: (i) a testable task specification, (ii) action primitives for robot execution, and (iii) an interactive environment for program execution and verification. RAPID infers all three from the demonstration automatically. To make the resulting program reusable beyond the demonstration setting, RAPID uses an object-centric relational program representation that focuses on the underlying structure of the demonstrated strategy rather than the specific motion per se: it expresses the action primitives as trajectory-optimization programs that realize object-level motion effects, while composing them through relational constraints that capture scene-specific geometry at run time. We evaluated RAPID in simulation on eight challenging contact-rich nonprehensile manipulation tasks as well as general prehensile manipulation tasks in the LIBERO-Pro benchmark. We also successfully deployed it on a real Franka arm and evaluated on all eight nonprehensile tasks. In all experiments, RAPID demonstrated strong performance, with generalization over object pose, shape, material, and environment. Website: https://yuyaoliu.me/projects/rapid.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。