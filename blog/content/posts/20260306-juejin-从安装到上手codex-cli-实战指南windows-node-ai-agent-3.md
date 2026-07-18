---
title: 从安装到上手：Codex CLI 实战指南（Windows + Node + AI Agent）
date: 2026-03-06 03:24:52+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- AI Agent
- 命令行工具
categories:
- AI 工程
scenarios:
- AI/ML项目
- 命令行工具
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7613658235174387727
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:25b1712ea52085680468fa01217f7ce63196c30ca951b51719c98fd17c22b598
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 48
captured_at: '2026-07-18T04:18:38.562968Z'
source_capture_sha256: sha256:49e29a3bb1dfb60fdafe1462ca1bc80cbda1676ff8b76b64ea593debfdd7ec13
source_capture_chars_original: 2168
source_publication_excerpt_chars: 782
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7613658235174387727](<https://juejin.cn/post/7613658235174387727>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 大家好，我是G探险者！
> 随着 AI 编程工具的兴起，越来越多开发者开始使用
> OpenAI Codex CLI
> 。
> 它是一种可以在终端运行的 AI 编程助手，可以读取项目代码、修改文件、执行命令，甚至帮你自动写测试和修 Bug。\(\[Aiberm\]\[1\]\)
> 相比传统聊天式 AI，Codex CLI 更像一个
> 本地 AI Agent
> ，可以直接参与工程开发流程。
> 本文记录一次完整的实践过程：
> 从安装 Codex CLI → 配置环境 → 解决常见坑 → 第一次使用。
> 一、什么是 Codex CLI
> Codex CLI 是 OpenAI 推出的
> 命令行 AI 编程助手
> ，主要特点：
> 在终端运行
> 能读取当前项目代码
> 可以修改文件
> 可以执行命令（如测试、构建）
> 支持自动化代码任务
> 例如你可以直接输入：
> codex
> 然后说：
> 为这个 service 写单元测试
> 它就会：
> 阅读代码
> 生成 test
> 运行测试
> 修复失败
> 二、安装 Codex CLI
> Codex CLI 依赖
> Node.js
> ，因此第一步需要安装 Node。
> 1 安装 Node.js
> 去官网下载 LTS 版本：
> 👉
> nodejs.org
> 安装完成后验证：
> node -v
> npm -v
> 如果显示版本号说明安装成功。\(\[Codexc\]\[2\]\)
> 2 安装 Codex CLI
> 使用 npm 全局安装：
> npm install -g @openai/codex
> 安装完成后验证：
> codex --version
> 如果能输出版本号说明安装成功。\(\[Codexc\]\[2\]\)
> 三、Codex CLI 的两种登录方式
> Codex CLI 有两种认证方式：
> 方式一：ChatGPT 账号登录
> 直接运行：
> codex
> 选择：
> Login
> with
> ChatGPT
> 需要 ChatGPT Plus / Team 等订阅。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
