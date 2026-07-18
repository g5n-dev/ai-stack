---
title: 🌟 LangChain 30 天保姆级教程 · Day 23｜Agent 进阶实战！Function Calling + 自动 Tool 注册，打造会“动
date: 2026-04-19 13:14:52+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- AI Agent
- 大语言模型
- 数据库
categories:
- 大模型
- 数据
scenarios:
- AI/ML项目
- 大语言模型
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7629718939094155306
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:b4aa5609311d651b8b7d951a8930e13499ecf79b9d7c65489d3c2fc9eb8cfb02
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 77
captured_at: '2026-07-18T04:19:36.949624Z'
source_capture_sha256: sha256:e1ea79b69b0c3cbdfbc8464f74b2cc21289681f2ea2fcb5e0a8f1a84e2323c03
source_capture_chars_original: 3765
source_publication_excerpt_chars: 778
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7629718939094155306](<https://juejin.cn/post/7629718939094155306>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 系列目标
> ：30 天从 LangChain 入门到企业级部署
> 今日任务
> ：理解 ReAct Agent 原理 → 实现自定义 Tool → 构建“查订单 + 发通知”自动化工作流！
> 🤖 一、为什么需要 Function Calling？
> 普通聊天机器人只能“说”，但企业需要 AI 能“做”：
> “帮我查订单 1001 的状态”
> “如果已发货，发邮件通知客户”
> “顺便查下今天北京天气”
> 传统 Chain 的局限
> ：
> ❌ 固定流程，无法动态决策
> ❌ 不能组合多个外部服务
> 解决方案
> ：
> ✅
> Agent + Tools
> —— 让 LLM
> 自主规划
> 、
> 调用工具
> 、
> 整合结果
> ！
> 💡 今天，我们就用 LangChain 的
> ReAct Agent
> +
> 自定义 Tool
> ，打造一个会“思考+行动”的 AI 助手！
> 🧠 二、Agent 核心原理：ReAct 框架
> ReAct =
> Reasoning（推理） + Acting（行动）
> 工作流程：
> 用户提问 → Agent 分析是否需要工具
> 若需要 → 选择合适 Tool + 生成参数
> 调用 Tool → 获取结果
> 基于结果生成最终回答（可多轮）
> 🔑 关键：LLM 必须支持
> Function Calling
> （结构化输出）
> ✅
> Qwen 通过 Ollama 支持 Function Calling
> （需
> ollama&gt;=0.1.34
> ）
> 🛠️ 三、动手实践 1：定义自定义 Tool
> 假设我们有两个内部服务：
> Tool 1：查询订单状态（模拟）
> # day23\_agent\_tools.py
> from
> langchain\_core.tools
> import
> tool
> @tool
> def
> get\_order\_status
> \(
> order\_id:
> str
> \) -&gt;
> str
> :
> """根据订单ID查询物流状态。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
