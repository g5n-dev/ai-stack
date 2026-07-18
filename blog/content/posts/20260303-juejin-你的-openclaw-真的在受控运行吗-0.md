---
title: 你的 OpenClaw 真的在受控运行吗？
date: 2026-03-03 11:19:12+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- AI Agent
categories:
- AI 工程
scenarios:
- AI/ML项目
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7612868336570286118
aliases:
- /posts/20260304-juejin-你的-openclaw-真的在受控运行吗-1/
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:2c680e19fc381e827fc86d4ad355304c663003dd4c41c77665d4e5b066e9b64f
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 21
captured_at: '2026-07-18T04:18:30.951822Z'
source_capture_sha256: sha256:1dbfe7c62af4db8febddad58981a5d30df31cf81f0f8d34daa39e9d58b134ba9
source_capture_chars_original: 6000
source_publication_excerpt_chars: 567
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7612868336570286118](<https://juejin.cn/post/7612868336570286118>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 作者：徐可甲
> 基于 OpenClaw（
> github.com/openclaw/op…
> ）与阿里云日志服务（SLS），将日志与 OpenTelemetry 遥测汇入 SLS，搭建 AI Agent 可观测体系，实现行为审计、运维观测、实时告警与安全审计闭环。
> 为什么必须回答：“Agent 真的在受控运行吗？”
> “
> 受控
> ”至少包含四件事：
> 谁
> 在触发调用、
> 花了多少钱
> 、
> 做了哪些操作
> （尤其是高危工具）、
> 行为是否可追溯
> 、
> 可审计
> 。回答不了这些问题，就不能说 Agent 在受控运行。
> 本文围绕“如何用阿里云 SLS 回答上述问题”展开：Session 日志回答“做了什么、花了多少”；应用日志回答“系统哪里异常”；OTEL 指标与链路回答“当前状态与耗时”。多条数据 Pipeline 协同，才能对“Agent 真的在受控运行吗？”给出有据可查的答案。
> 1.1 AI Agent 的安全风险面
> AI Agent 与传统后端服务有一个本质差异：Agent 的行为是非确定的。同样的用户输入，模型可能产生完全不同的工具调用序列。这意味着你无法像审计 REST API 那样，通过代码审查预判所有行为路径。
> 若不做可观测，你无法回答“谁在调你的模型、花了多少钱、有没有被注入恶意指令”——也就无法声称 Agent 在受控运行。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
