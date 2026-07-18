---
title: AI Agent 框架探秘：拆解 OpenHands（7）--- Agent
date: 2026-02-23 15:36:57+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- AI Agent
- 大语言模型
- 机器学习
- Docker
categories:
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
- 云原生/容器
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7608953699230105640
aliases:
- /posts/20260224-juejin-ai-agent-框架探秘拆解-openhands7-agent-4/
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:274c2bbd7a69f3267ac2d3b9bad567a5e877427e16410798148e1fc536d74fc1
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 38
captured_at: '2026-07-18T04:17:36.121026Z'
source_capture_sha256: sha256:3584447de88d4ec67355806f13a15648ee9b4bdd95ddb013880f2678c797f572
source_capture_chars_original: 2409
source_publication_excerpt_chars: 721
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7608953699230105640](<https://juejin.cn/post/7608953699230105640>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> AI Agent 框架探秘：拆解 OpenHands（7）--- Agent
> 0x00 摘要
> 0x01 状态管理
> 1.1 设计要点
> 1.2 State类
> 0x02 Agent系统
> 2.1 基类
> 2.2 Agent 类型
> 0x03 State
> 3.1 特色
> 3.2 State 定义
> 3.3 生命周期
> 3.4 联系
> 3.5 持久化和恢复
> 3.6 小结
> 0x04 大模型适配层（LLM Adapter）
> 4.1 LLM
> 4.2 LLMRegistry
> 0xFF 参考
> 0x00 摘要
> An LLM agent runs tools in a loop to achieve a goal.
> 智能体（Agent）是一种能够感知和理解环境，并使用工具来实现目标的应用程序。LLM能够动态指导自己的过程和工具使用，保持对任务完成方式的控制。Agent的设计旨在更灵活地处理某些任务，其决策由模型决定，而非预定义的规则。
> 借助 CodeAct 的 LLM 智能体，OpenHands 通过交互式的多轮流程，展现出显著的优势：
> 智能体能够接收新的观察数据，并据此优化先前的行动方案。这类似于人类在任务执行中，依据新信息灵活调整策略的过程。
> 依托记忆与反馈机制，智能体可随时间提升自身性能。它能将过往经验铭记于心，并在后续任务中加以运用，不断进步，恰似一名持续学习成长的学生。
> 此外，智能体还能胜任复杂的流程任务，涵盖模型训练、数据可视化以及自动化决策等。这表明 CodeAct 不仅能处理基础任务，更能驾驭高级且复杂的作业，例如训练机器学习模型、绘制图表以及实施自动决策等。
> 因为本系列借鉴的文章过多，可能在参考文献中有遗漏的文章，如果有，还请大家指出。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
