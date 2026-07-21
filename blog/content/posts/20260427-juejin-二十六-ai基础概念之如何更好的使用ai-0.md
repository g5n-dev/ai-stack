---
title: 二十六. AI基础概念之如何更好的使用AI
date: 2026-04-27 11:27:45+08:00
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
external_url: https://juejin.cn/post/7633205760817758251
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:5977c78836a6673d1bb54e151a74470e5ccbf010a289b546a8f400ff622f6b12
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 21
captured_at: '2026-07-18T04:19:42.494428Z'
source_capture_sha256: sha256:76d533a049a6339e68e7c1802bacd42de81dda5efd87d14193a0ae9c67323dbb
source_capture_chars_original: 5022
source_publication_excerpt_chars: 638
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_eaff8585fbd75aa4af29c73569e28c967ce5e190fdec601e19f11ec9785d08ea
revision_id: rev_cdd048c8983e71838b89cb00bfeb5cd22415273daef0be4b1c8f7bd13c74f711
event_id: evt_3dc22e030de275ac02b4b72f90b057d8de90c6824b48117395a48d03ec3b23a4
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-04-27T03:27:45Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7633205760817758251](<https://juejin.cn/post/7633205760817758251>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 一、这份分享的目标
> 这份内容主要是帮助大家建立一个可落地的基础认知，重点包括：
> AI 在实际工作中的使用方式
> Agent
> 、
> Skills
> 、
> Rules
> 、
> MCP
> 的区别
> 这些能力在 Everything Claude Code 里的协作方式
> 如何从“单次对话”转向“多智能体分工协作”
> 二、为什么要先理解这些概念
> 很多人第一次使用 AI 时，会把它理解成“一个什么都能回答的聊天工具”。
> 但如果要真正把 AI 用到工作流里，就会发现它其实由几类不同的能力组成：
> 有的负责执行任务
> 有的负责提供专门知识
> 有的负责限制行为边界
> 有的负责连接外部系统和数据
> 如果不先分清这些概念，就容易出现这些问题：
> 不知道什么任务该交给谁
> 以为 AI 会自动理解所有上下文
> 配置了很多内容，但整体效果还是不稳定
> 工具接了一堆，却没有形成清晰分工
> 三、从“问答式 AI”到“协作式 AI”
> 1. 问答式使用
> 最常见的方式，是把 AI 当成搜索引擎或者问答工具使用，比如：
> 问一个概念是什么
> 让它总结一段文字
> 让它翻译、润色、改写
> 让它快速给一个建议
> 这种方式的优点是简单直接，但缺点也明显：
> 多数是一次性回答
> 上下文容易丢失
> 不一定适合复杂任务
> 2. 协作式使用
> 当你开始让 AI 参与真实工作时，它就不再只是“回答问题”，而是开始“参与做事”。
> 例如：
> 帮你拆解需求
> 帮你整理资料
> 帮你生成初稿
> 帮你查找相关文件
> 帮你执行重复性操作
> 这时，AI 的角色会从“回答者”变成“协作者”。
> 3.…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
