---
title: Tide Commander — 一个用3D战场管理多个AI编程Agent的可视化工具（Claude Code + Codex）
date: 2026-02-17 03:10:02+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- AI Agent
- 命令行工具
- Docker
- 数据库
categories:
- AI 工程
- 数据
scenarios:
- AI/ML项目
- 云原生/容器
- 命令行工具
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7606793134374666303
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:e35e9e8e4c92dd216c9f7293befad1176cf4b86cb3fe1d9f1e5df38903a942e8
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 64
captured_at: '2026-07-18T04:17:23.277903Z'
source_capture_sha256: sha256:23c324ba345808ce2b3a78d95f9f64bd5eb1d3b71a664a2d1ed039f970e7002e
source_capture_chars_original: 1606
source_publication_excerpt_chars: 730
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7606793134374666303](<https://juejin.cn/post/7606793134374666303>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> Tide Commander — 一个用3D战场管理多个AI编程Agent的可视化工具（Claude Code + Codex）
> 如果你同时运行多个Claude Code或Codex终端，你一定懂这种痛苦：标签页到处都是，上下文丢失，完成的任务被淹没。我开发了Tide Commander来解决这个问题。
> 它是一个可视化的多Agent编排工具。你的AI Agent以3D角色出现在战场上，点击选择，输入命令，实时观看它们工作。看起来像游戏，但内部是一个完整的开发者工具。
> bunx tide-commander
> 需要 Node.js 18+，Linux 或 Mac，PATH 中有 Claude Code 或 Codex CLI。
> 解决什么问题
> AI编程Agent并行工作效果最好——一个跑测试，一个写功能，一个修Bug。但同时管理五个终端是一团乱。哪个有认证模块的上下文？测试Agent完成了吗？
> Tide Commander把所有东西放在一个可视化界面里，包含文件差异对比、Git集成的文件浏览器和实时流式输出。很多场景下，IDE变得几乎不必要了。
> 核心概念
> Boss Agent
> — 拥有下属Agent的上下文，把任务分配给最合适的Agent，汇总工作进度。跟一个Boss对话，不用在终端之间切换。
> Supervisor（监督者）
> — 上帝视角观察者。Agent完成任务时自动生成摘要。你不会错过任何完成的任务。
> Group Areas（区域）
> — 在战场上画区域来按项目组织Agent。分配文件夹可启用文件浏览器。
> Classes（职业）
> — 类似游戏里的职业系统：每个职业有3D模型、指令（类似claude.md）和技能。支持上传自定义GLB模型。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
