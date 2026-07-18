---
title: 难以想象啊，我用 Codex 全 AI 一天做了个拼豆小程序
date: 2026-07-04 19:28:31+08:00
draft: false
entry_kind: auto
tags:
- 掘金
categories: []
scenarios: []
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7658510258419220490
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:60f625818f41117aaf71237adb9e0f97771e912b180f942d2b78c4d6580d9cc7
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 30
captured_at: '2026-07-18T04:21:50.413850Z'
source_capture_sha256: sha256:bac3d5499f49a7ace56ef691126d8e83efe3baf70a126033054cb3feaf29a50e
source_capture_chars_original: 2664
source_publication_excerpt_chars: 792
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7658510258419220490](<https://juejin.cn/post/7658510258419220490>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 我用 Codex 全 AI一天做了个WX拼豆小程序：上传照片，直接生成图纸和用色清单
> 最近我做了一个很小但很完整的微信小程序，叫
> 嘎嘎拼豆
> 。
> 它解决的问题也很直白：
> 你有一张喜欢的照片，想做成拼豆作品，但不想手动描图、不想自己数颜色、不想对着图片一点点猜色号。
> 那就把照片传上来。
> 小程序会把照片转成拼豆图纸，自动生成网格、色号、用色数量，还能下载图纸。
> 这篇不是单纯说这个小程序。
> 我是想把它当成一个小案例聊聊：一个看起来很“手工爱好者”的工具，背后其实有不少工程问题；而且这次我基本是用 Codex 全程 AI 协作做出来的。
> 它不是画图工具，而是从照片到材料清单的转换器
> 拼豆玩家真正需要的不是一张“像素化图片”。
> 而是一套能落地制作的东西：
> 图纸要能看。
> 格子要能数。
> 颜色要能买。
> 颗数要能算。
> 太碎的颜色要能合并。
> 做错的地方要能修。
> 所以我一开始就没有把它做成普通的图片滤镜，而是做成一条完整链路：
> 上传照片。
> 选择品牌色板。
> 选择图纸尺寸。
> 生成拼豆图纸。
> 查看用色统计。
> 手动修图。
> 导出清单和图纸。
> 这也是我觉得它有推广价值的地方：它不是让你“看一下效果”，而是尽量把一个手工作品从灵感推进到可制作。
> 第一件难事：图片要变成格子
> 用户看到的是一个上传按钮。
> 工程上第一步其实是把一张普通照片变成固定尺寸的网格。
> 比如截图里这张驴子的图纸，生成结果是
> 104 x 163
> ，总计
> 9237
> 颗，
> 38
> 色。
> 这里有几个取舍。
> 网格太小，图案会糊，细节没了。
> 网格太大，效果更像原图，但颗数会暴涨，玩家做起来会很累。
> 所以小程序里我放了 52、78、104 这样的尺寸选择，再加一个“生成偏好”，让用户在效果和制作成本之间做选择。
> 这件事跟很多 AI 应用很像。
> 不是模型越强越好，也不是参数越大越好。
> 真正重要的是让用户能控制成本：时间成本、材料成本、制作难度。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
