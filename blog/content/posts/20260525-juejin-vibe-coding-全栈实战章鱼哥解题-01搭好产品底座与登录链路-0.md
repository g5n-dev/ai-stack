---
title: Vibe Coding 全栈实战：章鱼哥解题 01｜搭好产品底座与登录链路
date: 2026-05-25 12:52:51+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- RAG
- AI Agent
- Python
- Docker
categories:
- AI 工程
scenarios:
- AI/ML项目
- RAG应用
- 云原生/容器
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7643636893746675753
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:e15e14656b387f29260d98148612a121357722cc7e52d5502c77735902e4a668
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 37
captured_at: '2026-07-18T04:21:29.807932Z'
source_capture_sha256: sha256:3a80595d5f61b5258d3583a47c13573da488a7020fb1c9286d7589e08db1a655
source_capture_chars_original: 4002
source_publication_excerpt_chars: 743
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7643636893746675753](<https://juejin.cn/post/7643636893746675753>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> Vibe Coding 全栈实战：章鱼哥解题 01｜搭好产品底座与登录链路
> 一、故事背景：为什么要做这个系列
> 平均每天消耗约 4-5 亿 token——这是我现在用 AI 写代码的日常。从"让 AI 写个函数"到"让 AI 搭一个页面"，我越来越依赖
> Vibe Coding
> 这种开发方式：用自然语言描述意图，由 AI 生成实现代码，我来负责审查、决策和组装。
> 但用着用着，我开始好奇一个更大的问题：
> Vibe Coding 到底能不能支撑一个完整项目？
> 不只是写一个函数、一个组件、一个页面，而是从 0 到 1 做一个真实的全栈产品：有需求分析，有技术选型，有登录，有前后端，有本地开发环境，也有线上部署。AI 能不能一路参与？哪些地方它能直接搞定，哪些地方还是需要人来判断、兜底和收口？
> 所以我决定拿一个真实项目做实验：
> 探索 Vibe Coding 从 0 到 1 实现全栈项目的完整过程。
> OctoTutor（章鱼哥解题）就是这个实验对象。它的目标是做一个面向高中数学学习场景的 AI 解题助手：用户可以输入题目，系统不是直接给出答案，而是解释思路、拆解步骤、指出易错点，最终像一个耐心的数学助教一样陪学生把题做明白。
> 二、产品要做什么：先把目标分清楚
> OctoTutor 不是一开始就直接进入开发的。我先和 AI 做了一轮需求对齐，把一个问题说清楚：
> 这个产品到底要帮学生完成什么任务？
> 2.1 长期产品目标
> 现在回头看，最开始写的“基于固定高中数学教材的启发式问答助手”有点太像技术方案。它里面已经包含了“固定教材”“启发式”这些实现策略，但还没有先把用户问题讲清楚。
> 我更愿意把章鱼哥解题的长期目标改成一句更直白的话：
> 做一个陪学生把高中数学题想明白的 AI 学习助手。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
