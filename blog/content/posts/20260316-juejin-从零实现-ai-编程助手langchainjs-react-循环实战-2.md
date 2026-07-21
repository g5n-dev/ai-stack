---
title: 从零实现 AI 编程助手：LangChain.js + ReAct 循环实战
date: 2026-03-16 08:20:51+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- 数据库
categories:
- 数据
scenarios: []
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7617410783702777899
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:f40a9dc959db4270802e8d00a5eb502189616653999b9243e96b4a3520c6870b
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 38
captured_at: '2026-07-18T04:19:19.559816Z'
source_capture_sha256: sha256:d4d76dba698be4261ef69fa9abec9b3b32183bfd0267d765879356e4bc982c29
source_capture_chars_original: 3431
source_publication_excerpt_chars: 721
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_a230950c41b102bdbd11601c9d3de0eeaa77bdf9f1eef14f5ab86a709d134a73
revision_id: rev_6845979dfcfb5c2f534dd2605031c6da2c8e7163e1640101e1fe13e896adedc2
event_id: evt_24ebe0db50936c8d1dc308a41f04fe97a73a13380421a3b842f02ce964b894e0
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-03-16T00:20:51Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7617410783702777899](<https://juejin.cn/post/7617410783702777899>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> Claude Code 凭借精准的代码理解、生成与调试能力，成为开发者高效编码的利器。但是核心本质还是大模型结合工具调用，实现
> 代码场景化智能交互
> —— 而这一能力，我们完全可以基于 LangChain.js 复刻实现。
> 在此之前我们已系统掌握 LangChain.js 的核心基础：从豆包大模型的接入、invoke/stream 的调用，到 Messages 消息体系的运用，再到自定义 Tool 的开发与工具调用闭环的实现，为打造专属代码助手筑牢了技术根基。
> 如果你还不了解这些，可以查看这两篇文章：
> # LangChain.js 快速上手指南：模型接入、流式输出打造基础
> # LangChain.js 快速上手指南:Tool的使用，给大模型安上了双手
> 本文将基于 LangChain.js 整合大模型能力与自定义工具链，手把手打造一个
> 简易版 Claude Code
> 。我们将本地文件读写与代码落地读写，自定义执行命令工具的全流程能力，让大模型真正成为能写、能存、能解析的专属代码助手。
> 一、核心能力拆解
> Claude Code 的强大之处在于它能
> 理解代码上下文
> 并
> 执行具体操作
> 。我们将核心能力抽象为三个基础工具，对应代码中的三大模块：
> 工具
> 功能定位
> 技术实现
> read\_file
> 代码理解与分析
> fs.readFile
> 读取项目文件
> write\_file
> 代码生成与落地
> fs.writeFile
> + 自动目录创建
> execute\_command
> 环境交互与验证
> child\_process.spawn
> 支持前后台
> 这三个工具构成了
> 代码助手的最小能力闭环
> ：
> 读
> （感知上下文）→
> 写
> （生成代码）→
> 执行
> （验证运行）。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
