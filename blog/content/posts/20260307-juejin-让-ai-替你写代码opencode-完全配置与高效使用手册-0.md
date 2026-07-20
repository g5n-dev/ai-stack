---
title: 让 AI 替你写代码：OpenCode 完全配置与高效使用手册
date: 2026-03-07 02:49:40+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- AI Agent
categories:
- AI 工程
scenarios:
- AI/ML项目
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7613785351649329167
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:f6b1d855dda92efadb2f3fa2d35c72925f0c66381416e6ab7188e92c1b5700f9
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 31
captured_at: '2026-07-18T04:18:40.863434Z'
source_capture_sha256: sha256:e453832310cff7ddb0db93bd1d44d42fbaff7d4a5e45cf50e16e0cf51754e5be
source_capture_chars_original: 4299
source_publication_excerpt_chars: 800
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_b622437d5d903eff76b522f2d2dc37aae3faa42ba93120aa66124079f5fe7bee
revision_id: rev_328db2b1ffa13f6286646516a8d73695a826d4615ec84f96752c01f5a5687255
event_id: evt_3440d4ce6a2ecfec3db1bbe32703cd8f21b84f9f4281a46d96ea524d903760a4
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-03-06T18:49:40Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7613785351649329167](<https://juejin.cn/post/7613785351649329167>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 前言
> 相信大家对
> Cursor
> 、
> Trae
> 、
> Github Copilot
> 、
> 通义灵码
> 等 AI 辅助编程工具已经很熟悉了，今天主要想聊一款不止是补全代码的工具 ——
> OpenCode
> 。
> 简介
> OpenCode 是一个开源的 AI 编程代理（AI coding agent），支持在终端（Terminal）、桌面应用和主流 IDE（如 VS Code）中与 AI 交互完成代码相关任务。
> OpenCode 可以帮助我们理解代码库、编写新功能、重构代码、修复 Bug 等，大幅提升开发效率。
> OpenCode 支持 75+ 家模型提供商，内置 GLM-4.7、MiniMax M2.1 等免费模型，可对接 OpenAI、Anthropic、Google 等商业模型，也能配置本地模型（如 Llama 3），按需适配轻量脚本、复杂架构等不同场景。
> 安装
> 安装 OpenCode 最简单的方式是通过安装脚本。
> curl -fsSL https://opencode.ai/install | bash
> 或者通过命令安装
> Node.js
> npm install -g opencode-ai
> 在 macOS 和 Linux 上使用 Homebrew
> brew install anomalyco/tap/opencode
> 配置
> 运行
> /connect
> 命令
> /connect
> 输入你的 API 秘钥
> ┌ API key
> │
> └ enter
> opencode.json
> 加载
> 加载优先级：
> 远程配置 \(.well-known/opencode\)
>   → 全局配置 \(~/.config/opencode/opencode.json\)
>     → 环境变量 \(OPENCODE\_CONFIG\)
>       → 项目配置 \(./opencode.json\)
> 最小配置：
> \{
>   "model": "ant…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
