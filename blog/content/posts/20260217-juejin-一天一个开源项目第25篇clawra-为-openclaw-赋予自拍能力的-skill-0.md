---
title: 一天一个开源项目（第25篇）：Clawra - 为 OpenClaw 赋予「自拍」能力的 Skill
date: 2026-02-17 03:10:02+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- 大语言模型
- 命令行工具
categories:
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
- 命令行工具
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7606589625742639154
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:6ac93628ea2af0a8f3496e48f6102f9836cc9c68ab4758b894fe9d76078732e3
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 50
captured_at: '2026-07-18T04:17:23.374858Z'
source_capture_sha256: sha256:761c082cfb7b05c558408728888cb650f4c92c742b43318061c94ae7df92f0ea
source_capture_chars_original: 5026
source_publication_excerpt_chars: 490
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_89cb620961e4f629accd0890ac3310de14dca160f3fb5478de3f44ae39f87cb9
revision_id: rev_1e6a97929e54cfb5bd8e88b907fc7a2778f2fe3fd52f8f6dd95cc80b9da449a4
event_id: evt_9b4c4b3deae2d13c6339d9f59c2e39ac5cb6c411cdf5576e82a10ff75127eb95
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-16T19:10:02Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7606589625742639154](<https://juejin.cn/post/7606589625742639154>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 引言
> "让 AI 助手不仅能聊，还能按一句「发张自拍」生成并发送一张符合人设的图片。"
> 这是"一天一个开源项目"系列的第25篇文章。今天带你了解的项目是
> Clawra
> （
> GitHub
> ），由
> SumeLabs
> 开源。来剖析下号称电子女友的开项目项目，到底有哪些功能。
> OpenClaw 通过 Telegram、Discord、WhatsApp 等渠道与你对话，但默认能力以文本为主。若希望助手具备「形象」、能响应「发张自拍」「你现在在干嘛？发张图」这类请求，就需要
> 图像生成 + 与渠道发图
> 的能力。
> Clawra
> 是一个
> OpenClaw Skill
> ：基于
> fal.ai
> 调用
> xAI Grok Imagine
> ，用一张固定参考图（reference image）保持形象一致，按用户描述生成「自拍」并通过 OpenClaw Gateway 在对应平台发送。一条
> npx clawra@latest
> 即可完成检查、获取 fal.ai Key、安装 Skill、配置与 SOUL.md 注入，让助手支持 Mirror（全身/穿搭）与 Direct（近景/场景）两种自拍模式。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
