---
title: 5 分钟用 Amazon Bedrock 搭一个 AI Agent：从零到能干活
date: 2026-03-10 21:20:59+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- MCP
- RAG
- AI Agent
- Python
- JavaScript
- Java
- 命令行工具
categories:
- AI 工程
scenarios:
- AI/ML项目
- RAG应用
- 命令行工具
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7615419563384274984
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:bdd560751f42cdbac32fec590f64e4462ca479087bf44da79f7fe3742b57b144
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 40
captured_at: '2026-07-18T04:18:47.510786Z'
source_capture_sha256: sha256:38069feacec28e7099c57d96d7dab08a19da659b25e15cbe069979211310da5d
source_capture_chars_original: 4052
source_publication_excerpt_chars: 713
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_16575f1465c948864c9423dedcf965093565f68807c0fcae161d4d85ee97acb9
revision_id: rev_9b15989b4b60be08f32ca7b3c6d4f0d262d21dfecd3de8d63506061309ef8de6
event_id: evt_79d29ab6f9c2868095e00e68bac9b3f86392baa4ff6f1e5e7fe49fe3035d2cd0
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-03-10T13:20:59Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7615419563384274984](<https://juejin.cn/post/7615419563384274984>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 5 分钟用 Amazon Bedrock 搭一个 AI Agent：从零到能干活
> 最近打开掘金，热榜一半都是 AI Agent 相关的内容——OpenClaw 拆解、MCP 协议、Function Call 实战... 概念已经讲了不少，但真正从零搭过一个完整 Agent 的人可能不多。
> 今天换个思路：
> 不装环境、不写框架、不管运维
> ，直接用 Amazon Bedrock 的 Agent 功能，5 分钟搭一个能理解用户意图、自动调 API 的 Agent。
> 本文所有步骤均已实际验证跑通
> ，不是对着文档猜的。
> 前置条件
> 一个 AWS 账号（
> 注册入口
> ，新用户有免费额度）
> 就这一个。不需要 GPU、不需要装 Python、不需要 Docker。
> 第 1 步：开通模型访问权限（1 分钟）
> 登录
> Amazon Bedrock 控制台
> 左侧菜单
> Model access（模型访问）
> →
> Manage model access
> 勾选你要用的模型，推荐：
> Claude Sonnet 4.6
> （综合能力强，支持中文）
> DeepSeek V3.2
> （性价比高）
> 点
> Save changes
> ，几秒钟就开通
> 💡 Bedrock 目前支持 100+ 基础模型，覆盖 Anthropic Claude 全系列、DeepSeek、Meta Llama 4、Qwen3、GLM 等主流模型。
> 注意
> ：部分模型需要使用 Inference Profile（跨区域推理配置）才能调用，控制台会自动处理这个，API 调用时需要用
> us.anthropic.claude-sonnet-4-6
> 这样的 Profile ID 而非裸模型 ID。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
