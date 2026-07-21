---
title: 一天一个开源项目（第48篇）：Agent-Reach - 给 AI Agent 装上互联网能力，零 API 费用支持 Twitter、Reddit、YouTub
date: 2026-03-12 13:04:46+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- MCP
- AI Agent
- 大语言模型
- Python
- 命令行工具
categories:
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
- 命令行工具
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7616234147671048242
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:b029b2cce90942629d0e40dcb5d12a6b6ff45fda692a3198fce483b962596975
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 80
captured_at: '2026-07-18T04:19:10.203622Z'
source_capture_sha256: sha256:ebfca076a6e4cf18f9427bab2a76fbfc2c1caf87174c47249e53a3caab067316
source_capture_chars_original: 6000
source_publication_excerpt_chars: 800
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_b978fe0651c11e29f5f2c6948bc6a0b3f4718b123e2fff79cdccf2420d7c45e6
revision_id: rev_20e15ccceda3abbee3d4ef4d24e96b381436d1d582dd46a33326ff66c16119c6
event_id: evt_e96d73915b645c9be2488dc6fcacae21e0d4a086181b1fa3910d93e188f06a5a
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-03-12T05:04:46Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7616234147671048242](<https://juejin.cn/post/7616234147671048242>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 引言
> "Give your AI agent eyes to see the entire internet."
> 这是「一天一个开源项目」系列的第 48 篇文章。今天介绍的项目是
> Agent-Reach
> （
> GitHub
> ）。
> AI Agent 能帮你写代码、改文档、管项目，但让它去网上找点东西就抓瞎了：YouTube 视频看不了、Twitter 搜不了（API 要付费）、Reddit 403 被封、小红书打不开、B站连不上……
> Agent-Reach
> 是一个
> 脚手架工具
> ，给 AI Agent 一键装上互联网能力：支持
> Twitter、Reddit、YouTube、GitHub、B站、小红书、抖音、LinkedIn、微信公众号、微博、RSS
> 等平台，
> 零 API 费用
> ，
> 一键安装
> ，兼容
> Claude Code、OpenClaw、Cursor、Windsurf
> 等所有能跑命令行的 Agent。
> 为什么值得看？
> 🚀
> 一键安装
> ：复制一句话给 Agent，自动完成所有配置
> 💰
> 零 API 费用
> ：所有工具开源免费，不依赖付费 API
> 🔌
> 可插拔架构
> ：每个渠道独立，不满意可替换
> 🤖
> 兼容所有 Agent
> ：Claude Code、OpenClaw、Cursor、Windsurf 等
> 🔒
> 隐私安全
> ：Cookie 只存本地，不上传不外传，代码完全开源
> 🩺
> 自带诊断
> ：
> agent-reach doctor
> 一条命令检测所有渠道状态
> 🔄
> 持续更新
> ：追踪各平台变化，平台封了自动修复
> 你将学到什么
> Agent-Reach 的定位与「脚手架」设计理念
> 支持的平台和上游工具选型（xreach、yt-dlp、Jina Reader、Exa 等）
> 一键安装流程和配置机制
> 可插拔架构：如何替换上游工具
> 安全机制：Cookie 管理、隐私保护
> 与同类工具（LangChain Tools、C…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
