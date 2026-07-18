---
title: 一条龙服务！Claude Code新功能goal详解
date: 2026-05-13 03:46:42+08:00
draft: false
entry_kind: auto
tags:
- 掘金
categories: []
scenarios: []
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7638983028574437419
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:fd0e3e4b29a9cf0230f74df097cde127fe471d7169ccfc536985095e02243022
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 26
captured_at: '2026-07-18T04:21:23.451725Z'
source_capture_sha256: sha256:a418d0d2c87a11e116675e40614720f528dfeddd9ed778f7657d57c87d3fd210
source_capture_chars_original: 2123
source_publication_excerpt_chars: 758
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7638983028574437419](<https://juejin.cn/post/7638983028574437419>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> Claude Code v2.1.139 出了一个新功能：
> /goal
> 。
> 很多 ai 都会有主动降智的行为，比如你给出一个大任务，它干完一轮就停了，你得手动说"继续"，它又干一轮又停了，你来来回回催好几趟，跟个猪一样，赶一下动一下。
> /goal
> 能解决这个问题。你设一个完成条件，Claude 每干完一轮，系统自动检查条件有没有满足。没满足就继续干，满足了就自动停。
> 下面我展开讲讲。
> 基本用法
> /goal 做一个移动端界面适配的检查，用webapp-testing这个skills。出现了适配性的bug就修复，直到满足 webapp-testing       
> 的检查标准。
> 设完之后 Claude 立刻开始干活，你会看到一个
> ◎ /goal active
> 的状态指示器，显示目标已经运行了多久。
> 每一轮结束后，系统会用一个小模型（默认 Haiku）评估条件是否满足，给出一个简短的 reason，这就是“
> 评估器
> ”。你可以在状态面板和对话记录里看到这个 reason，知道 Claude 在朝哪个方向努力。
> 最后成功完成了任务
> 官方在文档里给了几个/goal 适合场景的例子：
> 把一个模块迁移到新 API，直到所有调用点编译通过、测试全过
> 按照设计文档实现功能，直到所有验收标准满足
> 把一个大文件拆成聚焦的小模块，直到每个文件都在大小限制内
> 清理 issue 列表，直到队列为空
> 所以，有明确终态的、可验证的大任务，就可以用 /goal 。
> 和 /loop、Stop Hook 的区别
> Claude Code 里有三个"让 Claude 持续工作"的机制，我们引用一下官方文档的介绍
> 可以看到，
> /goal
> 是"跑到目标为止"，
> /loop
> 是"每隔多久跑一次"，Stop Hook 是"你自己定规则"。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
