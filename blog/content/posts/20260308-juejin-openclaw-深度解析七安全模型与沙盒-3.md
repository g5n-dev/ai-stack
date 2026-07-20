---
title: OpenClaw 深度解析（七）：安全模型与沙盒
date: 2026-03-08 23:19:33+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- AI Agent
- 命令行工具
- Docker
categories:
- AI 工程
scenarios:
- AI/ML项目
- 云原生/容器
- 命令行工具
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7614388350333861897
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:ef75905ae16c6f95d7d3aec7655af5ea0a47789e13fc92090d9a341af13a0f68
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 24
captured_at: '2026-07-18T04:18:42.195703Z'
source_capture_sha256: sha256:8ccb631e2f1688730c5a6865eca8a376cb288f5453848945867100545d832ebc
source_capture_chars_original: 6000
source_publication_excerpt_chars: 707
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_bb8ba5da6f9f78110f18894caabc09efd3fba15207ca5ea95ebfa853df69362e
revision_id: rev_ded56a0b8aaefdd9bb40783e9bf1f62d3087837e4d8af88d642703bda0980b31
event_id: evt_128c882d5bb636cf0d7b9279856fbf0b78fa7265582fe73fb854bc79bfe54933
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-03-08T15:19:33Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7614388350333861897](<https://juejin.cn/post/7614388350333861897>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 场景：把 AI 助手部署在共享服务器上
> 前六篇从 Gateway、通道、Agent、插件、模型到 Canvas，一路分析了 OpenClaw 的核心能力。现在，假设你打算把它部署在一台多人共用的 Linux 服务器上——同事小李的账号也在这台机器上，你们共用同一个 Docker 环境。
> 这立刻暴露了一系列问题：
> 认证
> ：HTTP 端口绑定到
> 0.0.0.0
> ，没有 token，小李的脚本能直接调用
> /tools/invoke
> 执行命令？
> 工具过度暴露
> ：
> sessions\_spawn
> 工具暴露在 HTTP 接口上，意味着任何人都能远程派生 Agent，相当于 RCE 入口。
> Shell 逃逸
> ：Agent 执行
> exec
> 工具时直接在宿主机跑，一个
> rm -rf /
> 就是灾难。
> API Key 泄漏
> ：
> openclaw.yml
> 里写着明文的 Anthropic API Key，
> cat
> 一下就能看到。
> 提示注入
> ：把外部邮件内容喂给 AI 处理，邮件正文里夹带
> ignore all previous instructions
> 就能劫持行为。
> 这五个问题分别对应 OpenClaw 安全模型的五个层次：
> Gateway 认证
> 、
> 工具策略
> 、
> 沙盒隔离
> 、
> 密钥管理
> 、
> 外部内容防护
> 。再加上贯穿所有层次的
> 安全审计
> 框架，构成完整的信任边界设计。
> 一、Gateway 认证：信任边界的第一道门
> 问题：谁可以连接 Gateway？
> Gateway 提供 HTTP/WebSocket 接口——任何能访问该端口的进程都能发请求。在非 loopback 绑定时，这意味着同一局域网甚至公网上的所有人。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
