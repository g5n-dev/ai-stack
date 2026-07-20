---
title: AI双层代码治理：Monorepo × Harness Engineering
date: 2026-04-30 09:41:30+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- TypeScript
- 命令行工具
- 数据库
categories:
- 数据
scenarios:
- 命令行工具
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7634325990316605494
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:64cec478c3125eb4d05dbf5e01c4eeca987ac57d412b23c0fe8d7965903230d5
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 39
captured_at: '2026-07-18T04:19:45.240639Z'
source_capture_sha256: sha256:fb025ef3865f5d8428421679c9cafe62cb76bb5f3cb414c0841da216aff21a84
source_capture_chars_original: 3164
source_publication_excerpt_chars: 795
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_8b387800fe319de3293375d979dc34159148531ab63d20336fb01cddfbc342b5
revision_id: rev_88d5c15460909998244bc38a98cec9d1b3b089268ed07c0442b3e3ddbcae5065
event_id: evt_2bee0e59cf6688419d67d3d330006b7062b6d46057e77c7624b00611a412d726
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-04-30T01:41:30Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7634325990316605494](<https://juejin.cn/post/7634325990316605494>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 人设计系统，AI 在系统内可靠执行
> 2026年了，你每天打开
> IDE
> 的第一件事是什么？
> 我猜是跟 AI 打招呼。
> Cursor
> 、
> Claude Code
> 、
> Trae
> ……这些工具已经从"尝鲜玩具"变成了日常开发的一部分。据统计，超过 80% 的开发者每天都在用 AI 辅助编程。
> 但有一个现象值得注意：
> 模型越来越强，可开发效率的提升似乎并没有那么明显。
> 回想一下过去一周的工作：
> AI 帮你生成的代码，看着没问题，跑起来却报错
> 改了一个接口字段，漏掉了几个引用的地方
> 前后端类型不同步，到运行时才发现
> 团队里每个人用 AI 生成的代码，风格不太一样
> 这些问题的原因可能不在
> AI
> 本身。我在一个多
> Repo
> 项目里折腾过一段时间之后，逐渐有了一个感受：
> 项目结构的方式，会直接影响 AI 能发挥多大的作用。
> 这篇文章想分享的，是两套在实践中被验证有效的方案：
> Monorepo
> 和
> Harness Engineering
> 。它们分别从"结构"和"执行"两个层面，帮助 AI 更好地融入开发流程。
> 原文地址
> 墨渊书肆/AI双层代码治理：Monorepo × Harness Engineering
> 一、AI 在多 Repo 项目中遇到的常见问题
> 1.1 上下文不完整
> 假设你的项目是这样组织的：
> frontend-repo/
> # 前端（Git仓库A）
> admin-repo/
> # 管理后台（Git仓库C）
> backend-repo/
> # 后端（Git仓库B）
> 这在很多团队中是很常见的做法。
> 现在你在
> backend-repo
> 里，让 AI 帮你改一下 User 接口，加一个
> role
> 字段。AI 打开文件——它只能看到
> backend-repo
> 里的内容。前端的调用方式？不清楚。管理后台有没有用到？不相关。
> 于是 AI 改完了后端的
> DTO
> 。你去前端跑了一下——类型报错了。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
