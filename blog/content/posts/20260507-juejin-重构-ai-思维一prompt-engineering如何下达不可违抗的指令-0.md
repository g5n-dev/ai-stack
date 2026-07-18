---
title: 重构 AI 思维（一）：Prompt Engineering，如何下达不可违抗的指令？
date: 2026-05-07 23:28:57+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- Java
- 数据库
categories:
- 数据
scenarios: []
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7637027340086624290
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:90a76fc83c7f49b56ae0d2042b27a842cf0322ec5614a0db3e45933909ff4758
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 43
captured_at: '2026-07-18T04:19:49.401499Z'
source_capture_sha256: sha256:5a283f76db5be42982b4f26f1dcdbffceb66dcfdd42b68d52b2c257e121df524
source_capture_chars_original: 1908
source_publication_excerpt_chars: 782
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7637027340086624290](<https://juejin.cn/post/7637027340086624290>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 嘿，兄弟们好，我是
> 飞哥
> 。
> 前阵子我发了那篇上岸感悟，很多兄弟私信我：“飞哥，你老说现在要靠 AI 铲子吃饭，可我发现这 AI 经常‘不听话’，给的回答不是太虚就是格式乱掉，这铲子不好使啊。”
> 确实，很多兄弟还把 AI 当成\*\*“搜索引擎”
> 在用——随手甩个问题，等着它给标准答案。但对于咱们要搞生产级应用的 Java 佬来说，你得把它当成一个
> “初级开发”
> 或者
> “外包伙计”\*\*。
> 这，就是
> Prompt Engineering（提示词工程）
> 。它是咱们重构 AI 思维的第一步：
> 把“聊天”变成“下达指令”。
> 1. 别把 Prompt 当作玄学，它其实是“声明式编程”
> 很多所谓的“提示词专家”把 Prompt 搞得很神秘。但在飞哥看来，Prompt Engineering 本质上是
> 声明式编程
> 。
> 以前写 Java 代码，我们是命令式：第一步干啥，第二步干啥。
> 现在写 Prompt，我们是告诉 AI：
> “我有一个什么场景，你要扮演什么角色，按照什么逻辑，最后给我吐出什么格式的结果。”
> 如果你发现 AI 给你的回复不稳，通常是因为你的“指令”写得太随意，让 AI 产生了\*\*“逻辑漂移”\*\*。
> 2. 飞哥的“完美指令”模版：把 AI 关进笼子里
> 想要 AI 给出不可违抗的指令，你不能指望它的悟性，你得靠
> 结构化
> 。分享一个飞哥在项目中复用的 Prompt 框架：
> 核心要素表
> 模块
> 说明
> 例子（票务系统场景）
> Role \(角色\)
> 给 AI 定位，划定知识边界。
> 你是资深 Java 架构师，精通 Spring Cloud Alibaba 和高性能并发处理。
> Context \(背景\)
> 告诉它现在的处境，避免它瞎猜。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
