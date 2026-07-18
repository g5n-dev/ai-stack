---
title: 测试与调试：怎么验证你的 AI Agent 真的能用
date: 2026-03-09 10:32:53+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- RAG
- AI Agent
- 数据库
categories:
- AI 工程
- 数据
scenarios:
- AI/ML项目
- RAG应用
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7615014502552518694
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:619038de08717195525a556b58b3e1de9e0485023c19fbe6d609a9f314ca77fd
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 26
captured_at: '2026-07-18T04:18:44.953154Z'
source_capture_sha256: sha256:0fb65b39dd3c9e03a5bfde2c2ea1300e2f7a1db7fe3a03b99d6dfc65207dff05
source_capture_chars_original: 6000
source_publication_excerpt_chars: 800
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7615014502552518694](<https://juejin.cn/post/7615014502552518694>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 传统 API 返回固定 JSON，写个断言就能测。Agent 的输出是非确定性的自然语言或半结构化数据 — 同样的输入，跑两次可能得到不同的结果。这让测试变成了一门"艺术"。
> 本章从实战出发，教你如何系统性地验证 Agent 的可用性，快速定位问题根因。
> 5.1 Agent 测试的核心难题
> 先说清楚为什么 Agent 测试和传统后端测试不一样：
> 对比维度
> 传统 API
> Agent
> 输出确定性
> 同输入 → 同输出
> 同输入 → 不同输出
> 验证方式
> 精确断言 \(
> assert.equal
> \)
> 模式匹配 + 人工审查
> 失败模式
> 报错 / 返回错误码
> 输出"看起来对但实际不对"
> 调试信号
> 堆栈跟踪、日志
> Prompt 语义、模型行为
> 耗时
> 毫秒级
> 秒 ~ 分钟级
> 成本
> 几乎免费
> 每次调用都花钱
> 这意味着你不能简单地用 Jest 写一堆
> expect\(result\).toBe\(expected\)
> 就完事。你需要
> 分层测试策略
> 。
> 5.2 分层测试策略
> 第一层：输入输出格式验证（必须自动化）
> 不管模型生成什么内容，
> 格式必须正确
> 。这是可以精确断言的部分。
> // 验证生成的测试用例格式是否正确
> function
> validateTestCaseFormat
> \(
> testCase:
> any
> \):
> boolean
> \{
> // 必须有这些字段
> const
> requiredFields = \[
> 'title'
> ,
> 'steps'
> ,
> 'expectedResult'
> ,
> 'priority'
> \]
> for
> \(
> const
> field
> of
> requiredFields\) \{
> if
> \(!testCase\[field\]\) \{
> console
> .
> error
> \(
> \`缺少必要字段:
> $\{field\}
> \`
> \)
> return
> false
> \}
>   \}
> // priority 必须是合法枚举值
> const
> val…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
