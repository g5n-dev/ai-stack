---
title: AI 编程工程化：Command——给你的 AI 员工编一套操作手册
date: 2026-03-13 21:28:07+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- MCP
- AI Agent
- 数据库
categories:
- AI 工程
- 数据
scenarios:
- AI/ML项目
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7616377118177591311
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:b212a0c76e3e9d8173f98256ceb8f6474c8384a7a9b0fedd8e6df26ff9a9c006
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 34
captured_at: '2026-07-18T04:19:12.822044Z'
source_capture_sha256: sha256:006d0a7234ef066aef6d7635a92d3b9316fe37444d61719264da205ab6cd16af
source_capture_chars_original: 4898
source_publication_excerpt_chars: 756
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_f1bae608b3400d2d08011233574aa3ee83dfc8253bd201a36bdc7752da77298a
revision_id: rev_06ce98c3f50e9441e04d55cf3ec13924f2e58a039d282529662cf993ba6af11a
event_id: evt_69d65d51108c82c3f3e95ebcbe173fba56a0c7dad54e93a9e9a111aee2e258b7
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-03-13T13:28:07Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7616377118177591311](<https://juejin.cn/post/7616377118177591311>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 上一篇我们讲了
> Rule——给你的 AI 员工立规矩
> 。
> 规矩立完了，下一步是什么？
> 是把常用的操作标准化。
> 公司有了规章制度，还需要什么？
> 操作手册
> 。遇到这种情况走哪个流程，遇到那种情况怎么处理，写清楚，不用每次口头交代。
> 这就是 Command。
> 先说一个让我烦透了的事
> 我之前让 Claude Code 帮我生成 commit message，都要输一段差不多的话：
> 根据当前代码变更，生成一条 commit message。
> 要求：
> - 使用约定式提交格式（feat/fix/refactor/docs/chore）
> - 描述用中文
> - 不超过 50 个字
> 每次，同样的要求，重复输入。
> 用了几天之后，我开始想：这件事能不能只做一次？
> 可以。这就是 Command。
> 什么是 Command
> 说白了，Command 就是把一段 Prompt 存成文件，用
> /命令名
> 来触发。
> 你创建一个
> .md
> 文件，把要说的话写进去，以后不用再重复输入。直接输
> /命令名
> ，Claude Code 就会用那段内容作为 Prompt 执行。
> 文件名就是命令名。
> 建一个
> .claude/commands/commit.md
> ，以后就输
> /commit
> 触发。建一个
> review.md
> ，就输
> /review
> 。
> 就这样。
> 你可以把它理解成给 AI 员工的标准化操作手册——遇到标准场景，按流程走，不需要每次口头交代。
> Command 分两层
> 和 Rule 一样，Command 也有两个层级：
> 个人全局命令
> 路径：
> ~/.claude/commands/
> 放在这里的 Commands，在你电脑上所有项目都能用。
> 适合放个人习惯性操作，比如你个人的 commit 风格、你喜欢的代码审查标准。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
