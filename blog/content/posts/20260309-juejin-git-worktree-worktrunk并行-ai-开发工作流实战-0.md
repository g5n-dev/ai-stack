---
title: Git Worktree / Worktrunk：并行 AI 开发工作流实战
date: 2026-03-09 21:48:42+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- AI Agent
- Rust
- 命令行工具
- 数据库
categories:
- AI 工程
- 数据
scenarios:
- AI/ML项目
- 命令行工具
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7615074040147394570
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:af54e5a1a209a2d79abb99cad58d0ae949f93b581468fe849ea41811911978c1
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 38
captured_at: '2026-07-18T04:18:44.080468Z'
source_capture_sha256: sha256:2acc2bf36f7104ca981bf95c133f607b4b3a72643c390e97913e9fee80b571a2
source_capture_chars_original: 6000
source_publication_excerpt_chars: 769
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7615074040147394570](<https://juejin.cn/post/7615074040147394570>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 最近在日常开发中尝试了用 Git Worktree \(Worktrunk\) 配合 Claude Code 进行并行开发，体验下来效果非常好。这篇文章就来分享一下这套工作流的搭建和使用经验，希望能对大家有点帮助~
> 欢迎大家点个 star：
> Github
> 以及下载我的独立 app：
>  iColors
> 一、为什么需要 Git Worktree
> 先说一个日常开发中很常见的场景：你正在开发一个新功能，突然来了一个紧急 bug 需要修复。通常你要么
> git stash
> ，要么
> git commit
> 一个半成品，切换分支去修 bug，改完再切回来。
> 这个过程不仅繁琐，而且一旦涉及到 AI 辅助开发（比如 Claude Code），问题就更大了——每个 Claude 会话的上下文会因为切换分支而断掉。
> Git Worktree 就是为了解决这个问题的。简单来说，它允许一个 Git 仓库拥有
> 多个工作目录
> ，每个目录检出不同的分支：
> my
> -project/
> # 主仓库，develop 分支
> my
> -project.feature-A/
> # worktree，feature-A 分支
> my
> -project.feature-B/
> # worktree，feature-B 分支
> my
> -project.bugfix/
> # worktree，bugfix 分支
> 核心优势：
> 不需要多次克隆仓库
> ，所有 worktree 共享同一个
> .git
> 数据库
> 多个分支同时活跃
> ，互不干扰
> 磁盘空间省得多
> ，不像 clone 那样每次都复制整个 git 历史
> 二、Worktree vs Clone：到底省了什么
> 可能有同学会问：我直接 clone 多份不也行吗？
> 当然可以，不过在回答这个问题之前，我们先看看一个 Git 仓库到底包含了哪些东西。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
