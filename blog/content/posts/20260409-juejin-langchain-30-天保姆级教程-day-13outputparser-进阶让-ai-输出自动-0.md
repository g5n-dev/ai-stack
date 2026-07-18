---
title: 🌟 LangChain 30 天保姆级教程 · Day 13｜OutputParser 进阶！让 AI 输出自动转为结构化对象，并支持自动重试！
date: 2026-04-09 07:52:04+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- AI Agent
- 大语言模型
- Python
categories:
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7626391049497624591
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:b909c170aa82af3d2b22601f97e74cdfdffabdf3ada3bff73e2d89b4d7b2ccb3
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 72
captured_at: '2026-07-18T04:19:31.011453Z'
source_capture_sha256: sha256:9b0fdcd3d2717a78582f852a3c7ae80b051babebf35ff86495abb9bd14c46bed
source_capture_chars_original: 3984
source_publication_excerpt_chars: 800
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7626391049497624591](<https://juejin.cn/post/7626391049497624591>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 系列目标
> ：30 天从 LangChain 入门到企业级部署
> 今日任务
> ：掌握
> PydanticOutputParser
> +
> RetryOutputParser
> → 构建高可靠结构化输出链 → 让 Agent 返回标准 JSON 对象！
> 🎯 一、为什么需要“带重试的结构化输出”？
> 在 Day 6 中，我们用
> PydanticOutputParser
> 让 AI 输出合法 JSON。
> 但现实是：
> 即使加了格式指令，大模型偶尔仍会“跑偏”
> ：
> 多了 Markdown 代码块（\`\`\`json）
> 字段名拼错（"user\_name" 写成 "username"）
> 返回一段解释文字而非纯 JSON
> 如果直接解析，程序会崩溃 ❌。
> 解决方案
> ：
> ✅
> RetryOutputParser
> +
> PydanticOutputParser
> = 自动重试 + 自动修复
> LangChain 会在解析失败时，
> 自动把错误信息反馈给 LLM，让它重新生成
> ，直到成功或达到最大重试次数。
> 🧱 二、核心组件介绍
> 表格
> 组件
> 作用
> PydanticOutputParser
> 定义期望结构 + 生成格式指令 + 解析输出
> RetryOutputParser
> 包装 parser，支持自动重试
> RunnableParallel
> /
> LCEL
> 将 parser 集成到 Chain 或 Agent 中
> 💡 今天我们将构建一个“用户意图识别器”，要求 AI 从自然语言中提取：
> class
> UserIntent
> \(
> BaseModel
> \):
>     action:
> Literal
> \[
> "order"
> ,
> "refund"
> ,
> "inquiry"
> \]
>     product:
> str
> confidence:
> float
> # 0.0 ~ 1.0
> 🛠️ 三、动手实践：构建带自动重试的结构化输出链
> 步骤 1：定义 Pydantic 模…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
