---
title: 一天一个开源项目（第42篇）：OpenFang - 用 Rust 构建的 Agent 操作系统，16 层安全与 7 个自主 Hands
date: 2026-03-06 14:24:36+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- MCP
- AI Agent
- 大语言模型
- Python
- Rust
- TypeScript
- JavaScript
categories:
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7613971395927834651
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:391a124345896afd285f5da644219db8d58f3bcbaf9a6fac4c028fcfaf348e30
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 67
captured_at: '2026-07-18T04:18:38.481970Z'
source_capture_sha256: sha256:2e405fb8a9fcdd06c4bb1eb005d04129e15676806d6ed66e5d2eba3e176bac6f
source_capture_chars_original: 6000
source_publication_excerpt_chars: 800
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_e85a49cb1758571e05f5f3960a98797800de2b6c12f8c4142682f91fc9458333
revision_id: rev_528cfb94df7e4d6944f845f78f98dcb86bd44c1f8146605252392a64ed95673a
event_id: evt_c6c76c739fdf01d6c691f426a9ca1c39bcaaff42127591bef84f6417f2441d45
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-03-06T06:24:36Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7613971395927834651](<https://juejin.cn/post/7613971395927834651>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 引言
> "The Agent Operating System — not a chatbot framework, not a Python wrapper around an LLM, not a 'multi-agent orchestrator.'"
> 这是「一天一个开源项目」系列的第 42 篇文章。今天介绍的项目是
> OpenFang
> （
> GitHub
> ）。
> 传统 Agent 框架需要你输入指令才工作。
> OpenFang
> 是 RightNow-AI 用
> Rust
> 从零构建的
> 开源 Agent 操作系统
> ：运行
> 自主 Agent
> ，按计划、24/7 工作，构建知识图谱、监控目标、生成线索、管理社交媒体、向仪表盘报告结果。整个系统编译为
> 单一约 32MB 二进制
> ，一次安装、一条命令，Agent 即可运行。内置
> 7 个 Hands
> （自主能力包）、
> 16 层安全系统
> 、
> 40 个通道适配器
> 、
> 27 个 LLM 提供商
> ，冷启动 小于200ms，空闲内存约 40MB。
> 为什么值得看？
> 🦀
> Rust 构建
> ：137K LOC，14 crates，1,767+ 测试，零 clippy 警告
> 🤖
> 自主 Hands
> ：7 个内置 Hands（Clip、Lead、Collector、Predictor、Researcher、Twitter、Browser），无需提示即可按计划工作
> 🔒
> 16 层安全
> ：WASM 双计量沙箱、Merkle 审计链、信息流污点追踪、Ed25519 签名等
> 🌐
> 40 通道适配器
> ：Telegram、Discord、Slack、WhatsApp、Signal、Matrix、Email、Teams、LINE、Mastodon 等
> 🚀
> 性能优异
> ：冷启动 小于200ms，空闲内存 40MB，安装大小 32MB
> 📊
> OpenAI 兼容 API
> ：140+ REST…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
