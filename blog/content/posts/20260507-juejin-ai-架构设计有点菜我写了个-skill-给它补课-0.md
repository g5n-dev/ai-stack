---
title: AI 架构设计有点菜，我写了个 Skill 给它补课
date: 2026-05-07 00:14:25+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- AI Agent
- 大语言模型
- 命令行工具
- 数据库
categories:
- 大模型
- 数据
scenarios:
- AI/ML项目
- 大语言模型
- 命令行工具
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7636667427520102452
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:a010afaafb29fc28af79672dcfd71014aaac549d43d275088804b5553a22e3e2
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 26
captured_at: '2026-07-18T04:19:49.500177Z'
source_capture_sha256: sha256:45ce6b1b5003a414dca7803003fb19de1d838b2f3db24790f6e145f45cf37880
source_capture_chars_original: 6000
source_publication_excerpt_chars: 755
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_f9cd6bcf79043cee02ac5baf380ed2b70020182a0891902ab5952050eb12e895
revision_id: rev_61dbddbb277dc5a199d68731d48bf345325d6d0e50e50f4d4ef9a120628b3c8a
event_id: evt_843f7c1edb5bfe683bae2610a772e28ba478695a04eeaaf2157ff59b4fac0d76
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-05-06T16:14:25Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7636667427520102452](<https://juejin.cn/post/7636667427520102452>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 我最近越来越强烈地感觉到一件事：AI 写代码已经挺能打了，速度很快，补函数、改组件、写测试都能帮上很多忙。
> 但一到架构设计，情况就不一样了。很多时候，AI 能把代码写出来，却不太能决定系统应该怎么拆、边界应该放在哪里、哪些抽象现在值得做，哪些应该先忍住。最后架构还是得人自己定。
> 那人怎么定？一个很常见的做法，就是去调研别人已经做过的项目：看看成熟仓库怎么组织模块、怎么处理主流程、怎么把复杂度收起来。本来我以为这件事也可以交给 AI，让它帮我分析一下参考项目的架构。结果经常发现，AI 分析别人项目的能力也不太行，经常读到最后只剩目录结构、函数调用关系和一些泛泛的模块说明。
> 它很像一个刚入职、很努力、但还没学会抓重点的同事。
> 你把一个项目丢给它，它会认真读 README，扫目录，列模块，画几个箭头。说得都对，但你读完总觉得少了点什么。
> 少的不是"信息"，而是"判断"。
> 比如你真正想知道的是：
> 这个项目为什么这么拆模块？
> 哪条主流程最能暴露作者的设计意图？
> 哪些抽象值得我偷师，哪些只是历史包袱？
> 如果要把这种设计迁移到自己的项目，该复制什么，千万别复制什么？
> 但普通提示词下的 AI，经常给你一份"目录树豪华版"。看上去很充实，脑子里还是没有架构。
> 于是我写了一个项目：
> Arch Insight
> 。它是一个 Agent Skill，目标不是让 AI "总结代码"，而是让 AI 把源码仓库转成
> 设计判断
> 。
> 更准确地说，它试图教 AI 一件事：
> 读代码不是把文件读完，而是找到系统真正站在什么设计选择上。
> 目前我已经开源，放在
> GitHub
> 上，欢迎stars。
> 安装命令
> npx arch-insight install-release
> 并且花了3个小时做了个
> 官网
> 展示\(前端已经死的很安详\)。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
