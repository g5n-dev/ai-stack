---
title: CLI + MCP + Skill：2026年AI Agent开发的三大范式
date: 2026-06-11 15:09:22+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- MCP
- AI Agent
- 命令行工具
- 数据库
categories:
- AI 工程
- 数据
scenarios:
- AI/ML项目
- 命令行工具
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7650031039254953984
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:fbc9283bc104593d28059fe9121e01e63995c10d9cae28a66942c9e0d79fc90f
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 38
captured_at: '2026-07-18T04:21:39.820576Z'
source_capture_sha256: sha256:318d49a7beb9354e530d2a4e2e0bfc9abc2ac6e4ee5793aa8db7c84c6c70e734
source_capture_chars_original: 3926
source_publication_excerpt_chars: 642
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_490e927f59b01c5230cb99607a63eba6936cfb538ca7c24b530bdf8a183d64db
revision_id: rev_8bf3d3243044a96aa4a7432a98c605fc13d84f84c9cf9078e6d50c7d90816d3e
event_id: evt_f46b56237dc6e24a34ccc2710e112b0d9e16b4ce8861c7a96c522c1257af9c64
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-06-11T07:09:22Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7650031039254953984](<https://juejin.cn/post/7650031039254953984>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 当三大办公平台同一周开源CLI，一个时代正在转变
> 2026年4月，一个看似平常的消息在开发者圈子里悄然发酵：
> 钉钉、飞书、企业微信，同一周内相继开源了自己的CLI工具。
> 这并非巧合，而是一个清晰的信号——
> 软件正在从"为人设计界面"转向"为AI设计接口"
> 。
> 如果你是AI Agent开发者，或者正在思考如何让大模型真正"干活"，那么CLI、MCP、Skill这三个概念，将是你绕不开的技术图谱。本文不打算重复官方文档，而是从实践者的视角，
> 梳理这三种范式的设计哲学、适用场景，以及它们如何协同构建下一代AI Agent基础设施
> 。
> 一、CLI复兴：为什么古老的技术成了AI的最佳接口
> CLI（命令行界面）诞生于1960年代，比图形界面早了整整二十年。在AI Agent爆发的2026年，它意外地迎来了"第二春"。
> CLI vs GUI：AI的"母语"是什么？
> AI大模型处理信息的核心方式是
> 文本
> 。输入是文本，输出也是文本。CLI的输入输出同样是文本——这个本质上的亲和性，让CLI成为AI Agent天然的交互方式。
> 反观GUI操作，AI需要先截图 -&gt; 视觉识别 -&gt; 定位坐标 -&gt; 模拟点击 -&gt; 解析结果。一条
> git push
> 命令三秒钟完成的操作，用GUI方式需要至少五步，每一步都可能出错。
> 数据说话：
> 在同等任务复杂度下，AI通过CLI完成操作的
> 成功率比GUI高约40%
> ，平均耗时减少60%以上（来源：2026年AI Agent Benchmark报告）。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
