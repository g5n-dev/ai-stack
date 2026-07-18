---
title: OpenClaw 架构解析：一个生产级 AI Agent 是如何设计的
date: 2026-03-07 10:58:39+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- AI Agent
- Python
- Rust
- TypeScript
- 数据库
categories:
- AI 工程
- 数据
scenarios:
- AI/ML项目
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7613970761351888896
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:ccf402fafddac542c4cff67b6f34997a1adc65e54b1ac7706c2407fd56af6b12
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 35
captured_at: '2026-07-18T04:18:40.655986Z'
source_capture_sha256: sha256:9ee052fbc5d14179bf8d320845d8b7654247d610c851dcaf01e681808e61b5ec
source_capture_chars_original: 4208
source_publication_excerpt_chars: 765
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7613970761351888896](<https://juejin.cn/post/7613970761351888896>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> OpenClaw / MiniClaw / Anthropic SDK / Vercel AI SDK / pi-ai / parallel-code / Git Worktree
> 目录
> OpenClaw 架构与服务分层
> Claude Agent 内部决策流程
> 工具调用的完整生命周期
> Anthropic SDK：Tool 传入与背后逻辑
> Vercel AI SDK：自动化 Loop
> 三方 SDK 横向对比
> parallel-code 多 Agent 并行架构
> Git Worktree 完整解析
> 用 pi-ai 复现 parallel-code
> 1. OpenClaw 架构与服务分层
> 定位
> OpenClaw 是一个网关（Gateway），一个坐在 AI 模型和外部世界中间的单体运行时，不是框架。
> 五层服务
> 第一层：渠道适配层（Channel Adapter）
> 把 Discord、Telegram 等不同平台的输入转成统一消息格式，顺便提取附件。一个 Agent 挂多个渠道靠的就是这层。
> 第二层：网关服务器（Gateway Server）
> 流量总入口。Session Router 判断消息属于哪个会话，然后交给 Lane Queue（车道队列）做并发管理，避免多个对话同时跑的时候请求撞车或上下文串了。
> 第三层：Agent Runner（智能体运行器）
> 管模型选择、API Key 轮换冷却、提示词拼装和上下文窗口。
> 第四层：Agent Runtime / Agentic Loop
> 跑完整的 AI 循环：从会话历史和记忆里拼上下文 → 调模型 → 执行工具（浏览器自动化、文件操作、Canvas、定时任务等）→ 把更新后的状态存下来。
> 就是模型说"我要调工具"，系统执行，结果塞回去，模型再想，再调，直到搞定为止。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
