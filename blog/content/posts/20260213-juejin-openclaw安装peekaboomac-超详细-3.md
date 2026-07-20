---
title: OpenClaw安装peekaboo（Mac-超详细）
date: 2026-02-13 11:27:57+08:00
draft: false
entry_kind: auto
tags:
- 掘金
categories: []
scenarios: []
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7605882792145649727
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:fbe57221ad399dcf083094654ac127eb92f0dffde3ca0adb3678925eaf36325b
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 27
captured_at: '2026-07-18T04:21:59.071411Z'
source_capture_sha256: sha256:78ca8ea107b8dada0e7945813be9c79cccfb2334300a9fe7618d8467f8d15dc9
source_capture_chars_original: 1804
source_publication_excerpt_chars: 651
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_53630e4a404b9b1993bdac1dacff283c4d3dad173200e9a75d7fe15fd3c67094
revision_id: rev_df358660bff4a21662b959a0b4824290f42d58737489f405b8154401eb213271
event_id: evt_124e5a0ef44ab812947eec7203119ecd2f773697b35b77d5ca6733c0d8d9e91d
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-13T03:27:57Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7605882792145649727](<https://juejin.cn/post/7605882792145649727>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 作者已在OpenClaw中成功使用peekaboo，本文记录一些踩过的坑。以下会介绍快速安装及使用peekaboo，其详细介绍及多种安装方式可移步
> www.aipuzi.cn/ai-news/pee…
> 1.peekaboo介绍
> 控制和读取你 Mac 上的界面：切应用、点按钮、打字、截屏 + 让 AI 读屏
> 2.peekaboo安装
> 使用homebrew安装：
> brew install steipete/tap/peekaboo
> 检查是否安装成功：
> peekaboo
> --version
> ​检查权限，显示Not Granted：
> peekaboo permissions
> ​
> 在Mac设置中给予需要使用peekaboo的应用权限：
> 设置-隐私与安全性-录屏与系统录音，点击+，例如可以新增“终端”；
> 设置-隐私与安全性-辅助功能，点击+，例如可以新增“终端”；
> ​
> ​
> 重启终端，再次输入peekaboo permissions，两者都显示Granted即成功：
> ​
> 此时即可使用peekaboo相关命令，例如：
> 捕获全屏并保存到桌面
> peekaboo image
> --mode
> screen
> --retina
> --path
> ~/Desktop/screen
> .png
> ​
> 3.坑1-OpenClaw中无法使用peekaboo
> ​
> 原因：虽然我们给了终端使用peekaboo的权限，但是我们的OpenClaw却没有这个权限，OpenClaw执行命令时打开的shell和我们系统的shell是隔离的。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
