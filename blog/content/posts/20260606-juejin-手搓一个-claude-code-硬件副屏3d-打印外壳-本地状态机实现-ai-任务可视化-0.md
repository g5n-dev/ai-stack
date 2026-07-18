---
title: 我给 Claude Code 装了一个红绿灯，AI 干活还是摸鱼，一眼看穿
date: 2026-06-06 21:23:29+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- AI Agent
categories:
- AI 工程
scenarios:
- AI/ML项目
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7648054502554779698
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:3f893faeabfa656ef976c5fb87f1aa576b910b86e8b6dadff710777c7270d9a1
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 37
captured_at: '2026-07-18T04:21:37.030149Z'
source_capture_sha256: sha256:fac4c86f9b5f4a66302c683ec33bd8d2130286f23a781ce8107f84a7a1456e14
source_capture_chars_original: 3167
source_publication_excerpt_chars: 691
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7648054502554779698](<https://juejin.cn/post/7648054502554779698>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 用\*\* Claude Code\*\* 跑长任务时，我遇到过最窒息的一幕：把复杂任务丢给它，转身去处理其他事情。过一会想起来回来，要么卡在了等待界面，要么已经空闲了很久，小东西真会偷懒。
> 有朋友说系统通知能解决？前提是你坐在电脑前、且没有淹没在其他任务里。这是一个你根本意识不到的盲区——直到你发现时间被偷走了。所以我要
> 给 Claude Code 装了一个 Mini 红绿灯副屏，监视 AI 牛马干活
> 。
> 一、灵光乍现
> 核心技术主要考虑几个：
> 用 3D 打印外壳 + HDMI 小屏 + 本地状态服务
> ，通过红绿灯，把 Claude Code 的运行状态实时映射到桌面上。至于为什么要用小屏，主要是为了好玩。
> 🔴 红灯 —— AI 正在全速运行，CPU/Token 消耗中；
> 🟡 黄灯 —— AI 等待用户确认，任务卡在半路，这是最容易被遗漏的状态；
> 🟢 绿灯 —— AI 处于空闲，任务已完成或尚未开始。
> 无法上传视频，效果可以关注微信视频号：
> 涛哥玩3D
> 。
> 整个方案成本可控、复现门槛不高，下面按
> 硬件组装 → 软件状态机实现 → 前端展示
> 的顺序展开。
> 二、硬件准备
> 1、Mini 显示器外壳
> 外壳不需要自己建模，直接用开源方案。拓竹 MakerWorld 上搜索 "Mocintosh 摸鱼小副屏"，作者提供了两款尺寸：
> 尺寸
> 分辨率
> 打印时长
> 耗材重量
> 2.8-inch（推荐）
> 640×480
> 约 4.4h
> 161g
> 3.54-inch
> 960×640
> 约 4.8h
> 179g
> 个人推荐 2.8 寸款
> ，打印耗时更短，且 640×480 分辨率对静态状态展示完全够用。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
