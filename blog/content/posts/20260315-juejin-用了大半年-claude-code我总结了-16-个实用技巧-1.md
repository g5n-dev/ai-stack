---
title: 用了大半年 Claude Code，我总结了 16 个实用技巧
date: 2026-03-15 01:07:53+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- MCP
- AI Agent
- TypeScript
- 命令行工具
categories:
- AI 工程
scenarios:
- AI/ML项目
- 命令行工具
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7616666752521732096
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:5fb132540b2165e6ab9e77ac76ca65d5ee7872f4bdf6c284d81d9aebda012285
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 31
captured_at: '2026-07-18T04:19:16.657476Z'
source_capture_sha256: sha256:c0c2b21d96bd1bb234bc9d2078cc667a04685e6eda493bcbc31d7bf2daa2e898
source_capture_chars_original: 5287
source_publication_excerpt_chars: 696
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_e1bbb14ea7c243fc5212b471905207e6d15ec3871dd1a86edf99f6b441e17518
revision_id: rev_cec8e57aa457ee51464a92518a604716f293505fcd6c036fff7bfb87664e369c
event_id: evt_e9dda7bca1f5ac513e80c72ca441d9cf4fe8e739bb4e0f76388cce645217f3aa
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-03-14T17:07:53Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7616666752521732096](<https://juejin.cn/post/7616666752521732096>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 前言
> Hi～大家好呀。
> 我是清汤饺子，一个用 Claude Code 写了半年代码的普通前端工程师。
> 说实话，一开始我也用不太好，就觉得它跟其他 AI 编程工具差不多嘛，问问题、写代码，能有啥区别。
> 后来踩坑踩多了才发现，原来以前跟 AI 对话的方式，简直就是在浪费它的能力。
> 这篇文章呢，不是什么高大上的理论，就是我一路走过来总结的 16 个小技巧。都很实用，看完就能用～
> 对 Cursor 感兴趣的话也欢迎关注另外 2 篇专门介绍 Cursor 的文章：
> 一篇是
> 《Cursor 独有的 12 个技巧：这些是 Claude Code 没有的》
> ，专门讲了那些因为 Cursor 是编辑器才能做到的事——Plan Mode、Debug Mode、内置浏览器、Parallel Agents、Hooks、Bugbot 这些，Claude Code 里是没有的，感兴趣的可以去看看。
> 另一篇是
> 《用 Cursor 半年了，效率还是没提升？是因为你没用对这 7 个功能》
> ，讲了 Rules 怎么配、Plan Mode 怎么用、MCP 怎么接、TDD 工作流、@Branch 上下文管理，那些内容这里不重复了。
> 下面正式介绍 Claude Code 的 16 个实用技巧。
> 第一部分：提示技巧
> 1. 给 Claude 验证方式（最高杠杆）
> 不知道你们有没有遇到过这种情况：AI 给你写了一段代码，看起来是对的，结果一跑，全是 bug。
> 其实这不是 AI 的问题啦～是你没有告诉它什么算"对"。
> # ❌ 模糊
> "实现一个验证邮箱的函数"
> # ✅ 带验证
> "编写 validateEmail 函数。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
