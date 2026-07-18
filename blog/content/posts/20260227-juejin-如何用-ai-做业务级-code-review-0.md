---
title: 如何用 AI 做业务级 Code Review
date: 2026-02-27 08:07:36+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- RAG
- 大语言模型
- 命令行工具
- 数据库
categories:
- 大模型
- 数据
scenarios:
- AI/ML项目
- 大语言模型
- RAG应用
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7611165150921621554
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:3762f3108fb1c5530c86121faaf0897a8593c8e59fbf78e77f96e2e5bd0d5ad8
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 23
captured_at: '2026-07-18T04:18:22.175993Z'
source_capture_sha256: sha256:19862c8ac6412a4ffb926bc78748b7f2421c27969d1cc867cd66f3208cb3dcee
source_capture_chars_original: 4012
source_publication_excerpt_chars: 738
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7611165150921621554](<https://juejin.cn/post/7611165150921621554>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> Code Review 遇到的挑战
> 对于核心的业务项目来说，Code Review \(代码评审\) 是必不可少的。但现实中的代码评审时常常被以下几件事所困扰：
> Diff 太多，看不过来开
> 类似的 Bug 出现过，复盘文档也有，然而新人不知道，老人记不清
> AI 不懂业务，不能给出实质性的建议
> 因此，我们希望打造一个
> 有记忆、懂业务、还看过你们线上事故的评审
> 的 AI 助手，让它帮我们守最后一道门。
> 核心链路：从 git push 开始
> 整个流程可以大致分为以下几步
> 触发机制
> “触发机制的选择” 其实是个产品问题：
> 什么时候介入，才不打扰人？
> 我们最后选的是 GitLab Webhook 的事件驱动模式。开发者无需安装插件，也无需在本地执行脚本，只需按照往常一样进行 push 代码即可。
> 接入成本极低：
> 在 GitLab 项目或组织级别的 Webhook 配置中，只需勾选
> Push events
> 和
> Merge request events
> ，并填入审核工具的统一回调地址。
> 多场景触发
> ：
> 代码驱动
> ：当发起目标为
> 主分支的 MR
> ，或已有的
> MR 分支发生增量提交
> 时，系统将即时开启审计。
> 工程管控
> ：深度集成公司构建平台，支持通过构建
> Hook 配置
> ，针对特定业务分支在构建环节手动或自动触发评审任务。
> Diff 的深度预处理与语义重塑
> 当 Webhook 触发后，审核工具接收到的是一段包含
> +
> 和
> -
> 符号的原始 Diff 文本。原始 Diff 文本包含大量冗余符号和非逻辑变更。如果直接投喂给模型，不仅消耗 Token，还会导致模型注意力分散。
> 我们设计了一套
> 预处理流水线
> ：
> 特征过滤
> ：自动剔除
> .lock
> 、
> .json
> 、样式及静态资源文件。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
