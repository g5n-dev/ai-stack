---
title: 🎉Token自由-Ollama部署本地大模型超详细操作指南
date: 2026-05-03 11:58:57+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- 大语言模型
- Python
- 命令行工具
categories:
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
- 命令行工具
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7634768133992759296
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:b6fce293129a1e32045b876d60d766f31b246ebbd899227f254671ed68a2b0ce
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 29
captured_at: '2026-07-18T04:19:47.083228Z'
source_capture_sha256: sha256:4b312e60d5e605da8902a5050b194525ca1cd6fa827520e9f60d52428c6d754d
source_capture_chars_original: 5498
source_publication_excerpt_chars: 689
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_4c7f2e51f4ffaf24992c4eafb35a9da75e3af25e1641b154b46153ebfecaeebd
revision_id: rev_7e70d8f0c2f4647c0fdf196c5cd60304b4b58eba7a17c943f9cb840f6075946d
event_id: evt_3fee26b84fd83bad5cb4efea8b2553f2c1f47ae45b8368b5933ea362ce498a0b
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-05-03T03:58:57Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7634768133992759296](<https://juejin.cn/post/7634768133992759296>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 一、Ollama 简介及下载
> 1、Ollama 简介
> Ollama是一个专为macOS设计的开源工具，让你能在自己的Mac上轻松运行各类大语言模型。它最大的特点是“极简”--无需复杂的Python环境配置，无需CUDA驱动，只要一条命令就能完成模型的下载、安装和运行。
> 核心优势：
> 极致简单：
> ollama run qwen3.5
> 一行命令即可对话，零学习成本
> 苹果专属优化：最新0.19版本全面整合苹果MLX框架，在M系列芯片上推理速度提升近一倍
> 完全本地运行：数据不上云，隐私安全有保障
> 开箱即用：内置丰富的模型库，通义千问、Llama、DeepSeek等主流模型一键下载
> 开发者友好：提供OpenAI兼容的API，可轻松集成到其他应用中
> 无论你是AI开发者还是普通用户，Ollama都能让你在本机体验顶级大模型的魅力。
> 2、Ollama 下载安装
> 下载安装方式：
> 访问官网：打开浏览器，进入 Ollama 官网（
> ollama.com/
> ）
> 下载版本：下载安装包（直接点击官网上对应系统 Download 按钮）
> 安装：打开下载的 .dmg 文件，将 Ollama 图标拖入 "Applications" 文件夹
> 首次启动：打开应用程序中的 Ollama，它会提示你安装命令行工具，按提示操作即可
> 验证方式：打开终端输入 ollama --version，如果显示 "ollama version is x.xx.x" 说明安装成功。
> 二、下载运行模型
> 1、运行 Ollama
> 在Ollama安装完成后， 一般会自动启动 Ollama 服务，而且会自动设置为开机自启动。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
