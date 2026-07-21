---
title: 别再直接 `json.loads` 了！AI 返回的 JSON 坑位指南
date: 2026-04-12 11:13:50+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- Python
- TypeScript
categories: []
scenarios: []
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7627283724289294371
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:931199b67c9790cbd41908ab03cdc309a23ab13536fb9f4ccb52bab7678847f8
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 36
captured_at: '2026-07-18T04:19:32.356358Z'
source_capture_sha256: sha256:be8c616e420d5063f89a203f6a612db4165202055923e1b83e7cd739ed2ca396
source_capture_chars_original: 2027
source_publication_excerpt_chars: 732
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_f1e6f23354513793aebdf11620bb2361a8d61130b5e3fee01dd67505f1a32052
revision_id: rev_71dcc5b7ce43f9730ca045c25bf7f5a14be75ce3037d08be91c564239372d4a0
event_id: evt_60451d343124c116204f3de1ebc591167c662bdc97aaec2c2a6d76fef91380bb
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-04-12T03:13:50Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7627283724289294371](<https://juejin.cn/post/7627283724289294371>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 01. 成就感背后的“生产事故”
> 当你第一次成功让模型返回一个完美的 JSON 结构时，那种“代码终于受控”的成就感溢于言表。但如果你直接在代码里写下
> print\(data\['title'\]\)
> ，那么恭喜你，你已经为未来的生产事故埋下了伏笔。
> 在 AI 工程中，有一个残酷的现实：
> 模型返回 JSON，并不代表程序可以无条件信任它。
> 02. 模型会给 JSON 挖哪些坑？
> 即便你用了最强的 GPT-4 或 Claude 3，模型依然会偶尔“掉链子”。常见的异常场景包括：
> 1. 结构性“幻觉”
> 你要求返回一个数组，模型可能因为上下文太长，返回了一个被截断的字符串，或者干脆在 JSON 前后加了句“这是你要的结果：”。
> 后果
> ：
> json.loads\(\)
> 直接抛出
> ValueError
> 或
> JSONDecodeError
> 。
> 2. 字段“失踪案”
> 模型可能会漏掉你认为“必填”的字段，或者自作聪明地修改了键名（比如把
> user\_name
> 改成了
> username
> ）。
> 后果
> ：程序访问时触发
> KeyError
> 。
> 3. 类型“变色龙”
> 最典型的例子：你期待
> tags
> 是一个数组
> \["A", "B"\]
> ，模型却返回了逗号分隔的字符串
> "A, B"
> 。
> 后果
> ：下游的
> .map\(\)
> 或
> foreach
> 逻辑直接崩溃。
> 03. 核心观念：AI 输出是“不可信输入”
> 在传统工程中，我们对用户提交的表单、第三方接口的返回都会进行严格的校验。
> AI 输出本质上也是一种“外部输入”
> ，而且是比第三方接口更不稳定、更不可控的输入。
> 优秀的 AI 工程师不相信“概率”，只相信“防御”。
> 04. 实战：如何优雅地“接住”模型输出？
> 不要只写
> json.loads
> 。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
