---
title: 用 AI 搞定用户系统：Superpowers 工程化开发教程
date: 2026-04-06 15:11:52+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- Python
- Docker
- 数据库
categories:
- 数据
scenarios:
- 云原生/容器
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7625060523634163775
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:35788c392e027ae6ab1486a69ebeab35c199625550095faab549534af41275dc
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 31
captured_at: '2026-07-18T04:19:28.772864Z'
source_capture_sha256: sha256:c3aef7b56479d8bef923904fc3f6522fcf8362cb0cd15f0f9d65833e2b282dc5
source_capture_chars_original: 5766
source_publication_excerpt_chars: 716
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7625060523634163775](<https://juejin.cn/post/7625060523634163775>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 🧠 如果你最近在关注 AI Coding，大概率已经刷到过 Superpowers 和 ui-ux-pro-max。
> 前者试图把“想到哪写到哪”的 AI 编程，拉回到更像工程交付的节奏里；后者则想解决另一个老问题：AI 能把页面写出来，但不一定写得像一个成熟产品。
> 这篇文章不准备再用“工具很强、流程很酷、装上就起飞”那种方式来介绍它们。
> 我更想做的，是把几个真正重要的问题讲清楚：这两个 Skill 分别解决什么问题、官方文档里到底怎么安装和工作的，以及如果把它们放进一个真实项目里，具体应该怎样用。
> 为了把过程讲具体，后文用一个
> RBAC 用户权限系统
> 作为案例来串起整条链路。本文讨论的是
> 单租户后台管理系统
> 里的 RBAC，不展开 ABAC、行级权限、组织继承、多租户隔离这类更复杂的话题。
> 这是最终完成初版的多租户 RBAC 系统项目，仓库地址为
> github.com/Cookieboty/…
> 。感兴趣的同学可以 Star 支持一下。需要注意的是，这个项目虽然是按下文流程 VB 出来的，但过程中也做了不少 bug 处理；另外，受 AI 幻觉影响，部分分支出现过偏差，因此做了一些调整，但整体流程基本可控。
> 一、Superpowers 与 ui-ux-pro-max 的定位
> 1.1 Superpowers：面向工程流程的 AI 开发工作流
> 很多 AI 编程体验之所以让人又爱又烦，本质上不是模型不会写代码，而是它太容易
> 过早进入实现阶段
> 。你刚抛出一个需求，它就开始生成文件；你话还没说完，它已经默认做了三层扩展。
> Superpowers 的核心思路，正是把这种“先写再说”的节奏，改造成一套更接近工程实践的工作流。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
