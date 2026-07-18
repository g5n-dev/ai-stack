---
title: Ollama 入门指南：本地大模型实践
date: 2026-03-02 02:56:17+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- 大语言模型
- JavaScript
- 命令行工具
categories:
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
- 命令行工具
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7611832090888208424
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:9586006721136cc58b70971c3e291df10d0988b93bb1ec6eb47fd9dc2213ba4f
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 19
captured_at: '2026-07-18T04:18:28.436611Z'
source_capture_sha256: sha256:e49319c4fc0c7ebe563b11e6391eaec7a866986601f5cff0c11df524beadc97f
source_capture_chars_original: 1084
source_publication_excerpt_chars: 751
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7611832090888208424](<https://juejin.cn/post/7611832090888208424>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> Ollama 是一个让你能在自己电脑上轻松运行开源大模型（LLM）的工具。对于开发者来说，它就像一个本地的“模型服务器”，能帮你快速搭建和测试需要 AI 能力的应用，而无需依赖外部云服务。本指南将带你快速上手 Ollama，了解它的核心概念，并提供可以直接运行的代码示例。
> 快速入门：安装与运行
> Ollama 的安装非常直接，支持主流操作系统。
> 步骤 1：安装
> Ollama
> 从
> Ollama 官网
> 下载安装包手动安装，或者在终端中运行官方安装脚本。
> 安装完成后，Ollama 会在后台作为一个服务运行。在 macOS 上，你会在菜单栏看到一个小图标；在 Windows 上，它会出现在系统托盘。
> 步骤 2：下载并运行一个模型
> 接下来，我们下载一个模型并与之交互。可以从
> 官网
> 查找模型，这里以
> qwen3:8b
> 为例
> 打开终端
> \(Terminal / PowerShell\)。
> 运行以下命令来下载并启动模型
> ：
> ollama run qwen3:8b
> 这条命令会做两件事：
> 如果本地没有
> qwen3:8b
> 模型，它会自动从 Ollama 的模型库中下载（第一次运行会比较慢）。
> 下载完成后，它会直接进入一个交互式的对话界面。
> 你会看到类似下面的输出，表示你可以开始对话了：
> &gt;
> &gt;&gt; Send a message \(/?
> for
> help
> \)
> 关于模型大小的说明
> 你可能注意到了
> qwen3:8b
> 中的
> 8b
> ，它代表模型的规模。
> 4b
> /
> 8b
> /
> 14b
> ：这些数字表示模型的参数量（Billion，十亿）。例如，
> 8b
> 就是 80 亿参数。
> 参数量越大
> ：通常意味着模型“知道”的更多，回答质量更高，逻辑推理能力更强。
> 参数量越小
> ：运行速度更快，对电脑配置（特别是显存和内存）的要求也越低。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
