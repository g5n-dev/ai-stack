---
title: 我把终端小说阅读器接上了 AI Agent：TRNovel 现在能用 skill 生成书源了
date: 2026-06-01 23:28:09+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- AI Agent
- Rust
- 命令行工具
- Docker
categories:
- AI 工程
scenarios:
- AI/ML项目
- 云原生/容器
- 命令行工具
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7646334161279680521
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:df4aedc4583824728df94f8f9e90976544ee2037f3d82baf8f31af2dfd1cfca7
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 46
captured_at: '2026-07-18T04:21:34.090584Z'
source_capture_sha256: sha256:7883a3c40583926155e105d4ea78665978ce6d4cdd07f5a95dce293f5bf04f3a
source_capture_chars_original: 5225
source_publication_excerpt_chars: 779
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7646334161279680521](<https://juejin.cn/post/7646334161279680521>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 一篇 TRNovel 的阶段性复盘，也是一篇安利文。
> 如果说上一篇文章是在介绍「我做了一个终端小说阅读器」，那这篇更像续集：当时 TRNovel 刚到 0.5.1，主打本地 TXT、网络书源、历史记录、主题设置，以及 npm / cargo / Release 安装；一年多后，它已经慢慢长成了一个本地优先、跨平台分发、支持听书、能让 AI 帮你生成书源的阅读工具箱。
> 前面几篇关于 TRNovel 的文章可以按时间顺序看：
> TRNovel：一个专为小说爱好者打造的终端阅读器
> ：0.5.1 时的首次开源介绍。
> TRNovel王者归来：让小说阅读"声"临其境的终端神器
> ：讲 ratatui-kit 声明式重构、文档和听书功能。
> 用 cargo-dist 接管 Rust CLI 的发布：以 TRNovel 为例
> ：讲 TRNovel 如何把发布链路收敛到 cargo-dist。
> 先说结论
> TRNovel 现在不只是一个「终端小说阅读器」。
> 它现在更像是下面这几件事的组合：
> 一个用 Rust + Ratatui 写的跨平台 TUI 阅读器；
> 一个本地优先的 TXT 小说阅读工具，支持章节识别、分卷、历史记录和主题；
> 一个网络小说书源引擎，使用结构化的
> trnovel-booksource/v2
> 配置描述站点规则；
> 一个带
> doctor
> 体检命令的书源验证器；
> 一个可以通过 Agent skill 自动生成书源的 AI 工作流；
> 一个支持 npm、Homebrew、Cargo、shell / PowerShell 一键脚本的 Rust CLI。
> 换句话说，TRNovel 这段时间的核心变化不是「又加了几个按钮」，而是开始回答一个更现实的问题：
> 在 AI Agent 已经能读网页、写代码、跑命令的时代，一个开源小说阅读器应该怎么跟上新的工作流？…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
