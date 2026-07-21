---
title: 具身智能开源生态：小米机器人VLA模型如何推动物理AI产业化？
date: 2026-02-15 12:10:18+08:00
draft: false
entry_kind: auto
tags:
- 掘金
categories: []
scenarios: []
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7606324035640918016
aliases:
- /posts/20260215-juejin-具身智能开源生态小米机器人vla模型如何推动物理ai产业化-2/
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:3fb13526f76b31346208c1d1d00fff8c11cd56551a8d087ec411970e1f7bd3ff
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 31
captured_at: '2026-07-18T04:17:19.767987Z'
source_capture_sha256: sha256:74df89de4aba4132ceb486e10dfec21b510b94751bf1fd660322377af4a2c811
source_capture_chars_original: 1953
source_publication_excerpt_chars: 764
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_ebc55d40e857486f6413b2d2ff1e9c7342dd40f82281e5172407c890e1aa991e
revision_id: rev_436accd8570b9e9f6640e6d14e85f924a72faab841818d26fcb4118d9e356650
event_id: evt_98b886150c329a842373dd3cd96e0f3026bca72a1826c75d64cda57a58f8c9ac
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-15T04:10:18Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7606324035640918016](<https://juejin.cn/post/7606324035640918016>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 2026年2月12日，小米开源首代机器人VLA大模型Xiaomi-Robotics-0，以47亿参数、80ms延迟、消费级显卡实时执行的性能，刷新三大基准测试全项SOTA。这不仅是技术突破，更是具身智能产业化的重要拐点。
> 一、技术背景：从虚拟到物理的智能演进
> 具身智能（Embodied AI）让AI算法“走出屏幕”，在物理世界中实现感知-决策-执行闭环。与传统AI仅处理虚拟信息不同，具身智能要求模型理解三维空间、处理柔性物体、应对环境突变，并生成连续平滑的动作轨迹。
> 发展三阶段
> ：
> 早期探索
> ：强化学习主导，任务专用，泛化弱
> 视觉‑语言融合
> ：VLM兴起，理解自然语言指令，但动作生成依赖离散token，延迟高
> 统一范式
> ：VLA模型实现多模态感知与连续动作生成的统一
> 开源生态价值
> ：
> 降低门槛
> ：中小团队无需从零构建，聚焦应用创新
> 加速迭代
> ：全球开发者共同优化，避免大厂垄断
> 标准化推动
> ：促进产业链协同，缩短产品化周期
> 二、模型解析：大脑+小脑协同与三重创新
> Xiaomi-Robotics-0采用MoT混合架构，通过三项核心技术实现突破。
> 1. 双脑协同架构
> 视觉语言大脑
> ：多模态VLM底座，解析模糊指令，结合RGB‑D图像构建空间语义
> 动作执行小脑
> ：16层扩散变换器，通过流匹配直接生成连续动作向量
> 松耦合设计
> ：KV Cache复用，实现80ms延迟、30Hz实时控制
> 2. 两阶段预训练
> 第一阶段
> ：Action Proposal机制对齐视觉与动作空间，混合数据避免遗忘
> 第二阶段
> ：冻结VLM，专注训练DiT，流匹配压缩推理步数至五步
> 3. Λ形注意力掩码
> 紧邻前缀
> ：回看历史动作，保证衔接平滑
> 远离前缀
> ：强制聚焦当前视觉反馈，实时修正轨迹
> 三重创新让机器人同时实现“连贯性”与“反应敏捷性”。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
