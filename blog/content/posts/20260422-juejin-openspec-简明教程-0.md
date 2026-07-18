---
title: OpenSpec 简明教程
date: 2026-04-22 13:49:58+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- AI Agent
- 命令行工具
categories:
- AI 工程
scenarios:
- AI/ML项目
- 命令行工具
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7631425034263593014
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:13a81f29cd14e5f745ee40e5dde917530064d5189a05232471ccbe93a2339ebf
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 13
captured_at: '2026-07-18T04:19:39.522154Z'
source_capture_sha256: sha256:d7d25ee6960d7f5add438b408eba6c88cc0bdfa6c5b192a1b47945dbd3102419
source_capture_chars_original: 1630
source_publication_excerpt_chars: 780
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7631425034263593014](<https://juejin.cn/post/7631425034263593014>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 1. 是什么
> OpenSpec 是一个
> 规范驱动开发
> 工具，专为 AI 编码助手设计。核心理念很简单：
> 写代码前，先让人类和 AI 对“要做什么”达成一致
> 。
> 它解决的是“凭感觉聊天”式开发的痛点——需求散落在聊天记录里，AI 容易遗漏需求或偏离预期。OpenSpec 通过轻量级的规范流程，把模糊提示变成可审查、可落地的工程计划。
> 核心结构：
> openspec/
> ├── specs/
> # 已实现的功能（真相之源）
> └── changes/
> # 待实现的提案
> └──
> \[变更名\]
> /
>         ├── proposal.md
> # 为什么要做、做什么
> ├── design.md
> # 技术方案
> ├── tasks.md
> # 实施清单
> └── specs/
> # 规范增量（补丁）
> 2. 快速上手
> 环境要求：
> Node.js 20.19.0 或更高版本
> 安装与初始化：
> # 全局安装
> npm install -g openspec-cn/openspec
> # 进入项目目录
> cd
> your-project
> # 初始化
> openspec init
> 初始化会创建
> openspec/
> 目录结构，并根据你的 AI 工具配置对应的斜杠命令。
> 3. 核心工作流
> OpenSpec 采用四步工作流，全程通过斜杠命令与 AI 交互：
> 命令
> 阶段
> 功能
> /opsx:new
> 规划
> 创建新变更，生成首个工件模板
> /opsx:ff
> 规划
> “快进”——一次性生成所有规划文档
> /opsx:apply
> 实施
> 按任务清单实现代码
> /opsx:archive
> 收尾
> 归档已完成变更，更新主规范
> 实操示例
> （以“添加深色模式”为例）：
> # 1. 创建变更
> /opsx:new add-dark-mode
> → 创建 openspec/changes/add-dark-mode/
> # 2.…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
