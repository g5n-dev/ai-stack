---
title: 'CRoSS: A Continual Robotic Simulation Suite for Scalable Reinforcement Learning
  with High Task Diversity and Realistic Physics Simulation'
date: 2026-02-05 23:03:18+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
- AI Agent
categories:
- 论文
scenarios:
- AI/ML项目
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.04868v1
aliases:
- /posts/20260206-arxiv_ai-cross-a-continual-robotic-simulation-suite-for-sca-6/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:63d4000c67a66fc2610ecd25024ac26d3d9e70cb778048c47f20de579683484b
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 137
captured_at: '2026-07-18T04:10:49.793468Z'
source_capture_sha256: sha256:65b35589b8c0cb9ccc7bb8cf1cf194b44b51def49e2bbff9c841688b25cec730
source_capture_chars_original: 1601
source_publication_excerpt_chars: 1601
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.04868v1](<https://arxiv.org/abs/2602.04868v1>)
- **作者**: Yannick Denker, Alexander Gepperth
- **分类**: cs.LG
- **论文时间**: 2026-02-04T18:54:26Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.04868v1.pdf](<https://arxiv.org/pdf/2602.04868v1.pdf>)

## 来源摘要/节选

> Continual reinforcement learning \(CRL\) requires agents to learn from a sequence of tasks without forgetting previously acquired policies. In this work, we introduce a novel benchmark suite for CRL based on realistically simulated robots in the Gazebo simulator. Our Continual Robotic Simulation Suite \(CRoSS\) benchmarks rely on two robotic platforms: a two-wheeled differential-drive robot with lidar, camera and bumper sensor, and a robotic arm with seven joints. The former represent an agent in line-following and object-pushing scenarios, where variation of visual and structural parameters yields a large number of distinct tasks, whereas the latter is used in two goal-reaching scenarios with high-level cartesian hand position control \(modeled after the Continual World benchmark\), and low-level control based on joint angles. For the robotic arm benchmarks, we provide additional kinematics-only variants that bypass the need for physical simulation \(as long as no sensor readings are required\), and which can be run two orders of magnitude faster. CRoSS is designed to be easily extensible and enables controlled studies of continual reinforcement learning in robotic settings with high physical realism, and in particular allow the use of almost arbitrary simulated sensors. To ensure reproducibility and ease of use, we provide a containerized setup \(Apptainer\) that runs out-of-the-box, and report performances of standard RL algorithms, including Deep Q-Networks \(DQN\) and policy gradient methods. This highlights the suitability as a scalable and reproducible benchmark for CRL research.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
