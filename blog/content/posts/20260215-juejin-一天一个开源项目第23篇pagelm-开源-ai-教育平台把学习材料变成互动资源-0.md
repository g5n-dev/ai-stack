---
title: 一天一个开源项目（第23篇）：PageLM - 开源 AI 教育平台，把学习材料变成互动资源
date: 2026-02-15 12:10:18+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- RAG
- 大语言模型
- TypeScript
- Docker
- 数据库
categories:
- 大模型
- 数据
scenarios:
- AI/ML项目
- 大语言模型
- RAG应用
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7606519452976873522
aliases:
- /posts/20260215-juejin-一天一个开源项目第23篇pagelm-开源-ai-教育平台把学习材料变成互动资源-1/
- /posts/20260215-juejin-一天一个开源项目第23篇pagelm-开源-ai-教育平台把学习材料变成互动资源-2/
- /posts/20260216-juejin-一天一个开源项目第23篇pagelm-开源-ai-教育平台把学习材料变成互动资源-2/
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:3adaeb27a690b3bd44f15c271d7e3c343c8eba07926ff84df6ef0d07a2a1e9aa
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 46
captured_at: '2026-07-18T04:17:19.700639Z'
source_capture_sha256: sha256:bc3cf06031981f532644a4581c412b98ad27caeb3b46d6a13af0c525bb9c837a
source_capture_chars_original: 4544
source_publication_excerpt_chars: 800
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7606519452976873522](<https://juejin.cn/post/7606519452976873522>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 引言
> "把教材和笔记交给 AI，得到测验、闪卡、康奈尔笔记和播客——一个平台搞定输入与输出。"
> 这是"一天一个开源项目"系列的第23篇文章。今天带你了解的项目是
> PageLM
> （
> GitHub
> ），由
> CaviraOSS
> 开源。
> Google 的 NotebookLM 把文档变成可对话、可生成音频的「个人 AI」，但不开源、依赖其生态。
> PageLM
> 定位为
> 社区驱动的 NotebookLM 风格教育平台
> ：上传 PDF、DOCX、Markdown、TXT 等学习材料，即可获得
> 情境对话、智能笔记、闪卡、测验、AI 播客
> ，以及语音转写、作业规划、模拟考试、辩论陪练、学习伴侣等能力。后端支持多 LLM（Gemini、GPT、Claude、Grok、Ollama、OpenRouter）与多 TTS（Edge TTS、ElevenLabs、Google TTS），前端为 Vite + React + Tailwind，可自托管、可扩展，适合学生、教师与研究者。
> 你将学到什么
> PageLM 的定位：开源、多模态的「学习材料 → 互动资源」平台
> 核心能力：情境对话、SmartNotes、闪卡、测验、AI 播客、语音转写、作业规划、ExamLab、辩论、学习伴侣
> 技术栈：Node.js/TypeScript、LangChain/LangGraph、Vite/React、JSON 或向量库存储
> 如何本地运行与 Docker 部署，以及环境与配置要点
> 与 NotebookLM 及同类教育/笔记工具的对比
> 前置知识
> 对 RAG（检索增强生成）、LLM API 有基本概念
> 会用 Node.js、npm/pnpm，了解前后端分离项目结构
> 若自建部署，需准备 LLM/TTS API Key 或本地 Ollama
> 项目背景
> 项目简介
> PageLM
> 是一款
> 开源、AI 驱动的教育平台
> ，将学习材料…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
