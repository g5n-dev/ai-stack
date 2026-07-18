---
title: 如何把小米 MiMo 接入 CodeBuddy，打造私有 Agent
date: 2026-07-05 12:33:40+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- AI Agent
- Python
- TypeScript
- 命令行工具
categories:
- AI 工程
scenarios:
- AI/ML项目
- 命令行工具
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7658622701872103459
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:cb9cba6920c52958207a8b67dcdab59a6cccb6e307d5900fd0a7407af7b787aa
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 34
captured_at: '2026-07-18T04:21:50.444930Z'
source_capture_sha256: sha256:b9dc245afd58602c2aa6a67dcd181351d98f2d1c77b86938fb9a0905fc8c02b9
source_capture_chars_original: 3354
source_publication_excerpt_chars: 751
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7658622701872103459](<https://juejin.cn/post/7658622701872103459>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 把小米 MiMo 接入 VSCode：用 CodeBuddy 打造你的专属 AI 编程 Agent
> 关键词：VSCode, CodeBuddy, 小米 MiMo, 自定义模型, Agent, OpenAI 兼容, AI 编程
> 前言
> 最近拿到了小米 MiMo 的 API Key，本想直接在 VSCode 里写代码，却发现市面上的教程大多停留在“用 Python 调 API”的阶段，离真正的 IDE 集成还有距离。
> 我也尝试过直接修改 CodeBuddy 的
> Enterprise Endpoint
> ，结果发现那是腾讯云企业版的专属通道，根本无法指向第三方模型。
> 直到我翻到了腾讯云官方的这篇教程：
> 《自定义大模型配置》
> ，才找到了正解：通过修改
> models.json
> 文件，配合 Agent 的
> .md
> 配置文件，实现真正的“模型自由”。
> 本文将手把手教你如何将小米 MiMo 接入 CodeBuddy，并赋予它文件读写、命令行执行等“超能力”。
> 原理解析：为什么不能直接改 Endpoint？
> 在 CodeBuddy 的设置界面中，有一个
> Codingcopilot: Enterprise Endpoint
> 选项。很多人的第一反应是修改这里。
> 这是一个误区。
> •   Enterprise Endpoint：仅供腾讯云企业客户连接内部私有化部署的模型网关，不接受外部 OpenAI 格式的 API Key。
> •   正确的架构：CodeBuddy 采用了“配置驱动”的设计：
> ◦
> \`models.json\`
> ：充当“模型注册表”，负责定义有哪些模型（API 地址、Key、参数）。
>
> ◦
> \`\*.md\`
> \(Agent 文件\)：充当“行为说明书”，负责定义怎么用模型（人设、工具权限、执行模式）。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
