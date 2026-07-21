---
title: 在职前端 Agent 配置分享
date: 2026-04-26 13:32:47+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- MCP
- AI Agent
- 命令行工具
categories:
- AI 工程
scenarios:
- AI/ML项目
- 命令行工具
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7632567246008270902
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:9a638dac7ee0b3b30d0beaa0feeca59211e48a2cbe17bc62965bdd2f9940db51
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 15
captured_at: '2026-07-18T04:19:41.786127Z'
source_capture_sha256: sha256:417dd4203601c1f158499eb486082a5dcd310d094deaa830922b791be538f069
source_capture_chars_original: 1980
source_publication_excerpt_chars: 645
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_94712ce43e6dfe15cb510e5381e4740ec175199e15cfe5f38cf0ffe7834aa5f7
revision_id: rev_8653f61e3542ece34c9c8a59830e08829b1537160e1ae4ee80f9bfe7e9ccd69e
event_id: evt_2a7b8d1ef18a2916ba37719aa18c6e4cf9cd690c3314c125f10e9e44f18483e4
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-04-26T05:32:47Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7632567246008270902](<https://juejin.cn/post/7632567246008270902>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 前言
> 去年花了半年时间对公司旧业务代码做了不少架构优化，今年开始陆续就要开始业务开发了。
> 不得不说在 AI 时代背景下，开发范式每天都在变化，prompt engineering -&gt; context engineering -&gt; agent engineering -&gt; harness engineering，一路狂飙，看似每天都有新东西要学习，到最后大多都是 FOMO。
> 然而在显而易见的不确定性面前，总有一些东西是固定不变的。今天我来分享在 AI 冲击下我的前端 Agent 开发配置，这些内容个人认为属于长期不变的地基。
> （本文以 Mac 为例）
> 基本工具
> 首先是两个配置工具：
> cc-switch
> skills.sh
> 前者用于接入不同 AI 供应商，例如业内熟知的 Claude、Codex、Gemini、OpenCode 等等；后者用来添加 skills，一些固定的工作流被总结为技能供模型识别和调用。
> CC Switch
> 安装
> 以 Homebrew（macOS）为例：
> brew tap farion1231/ccswitch
> brew install --cask cc-switch
> # 更新
> brew upgrade --cask cc-switch
> 其他平台也可以在
> Release
> 找到对应的安装包。
> 更新
> APP 的关于页可以检查更新、同时还兼具了本地环境检查：
> 我觉得特别好的一点就是还提供了一键安装的脚本：
> 以往我都是要去官方文档上找，这里一键复制更方便。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
