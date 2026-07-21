---
title: Claude Code 构建完全指南：十大核心功能深度解析
date: 2026-02-25 15:56:41+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- MCP
- AI Agent
- 命令行工具
- 数据库
categories:
- AI 工程
- 数据
scenarios:
- AI/ML项目
- 命令行工具
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7610377938862669834
aliases:
- /posts/20260225-juejin-claude-code-构建完全指南十大核心功能深度解析-4/
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:3e43d1a222b685cb8bebd60f1cc564d17c7894c534db0e2bac32873ed4a8d86d
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 29
captured_at: '2026-07-18T04:17:40.959168Z'
source_capture_sha256: sha256:e9cb9f73c6a7eae1dd9a7f1edb6d016647dcd4772c071ddc1481a80bd59cf23e
source_capture_chars_original: 6000
source_publication_excerpt_chars: 800
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_1fd50e308d95abc80b9dc0b43bfd90a21a8865db35302f47c44d9930ff946153
revision_id: rev_35e3e2e8654168f261b07be8428b51460642c45faac77947b056bc1806d40718
event_id: evt_bff5f0989b959758a103e298c0990a69e2aec72d7b69cdb8772aa0f9a1cbebab
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-25T07:56:41Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7610377938862669834](<https://juejin.cn/post/7610377938862669834>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 一、创建自定义子代理（Subagents）
> 1. 是什么
> 子代理是运行在独立上下文窗口中的专用 AI 助手。每个子代理拥有自己的系统提示、工具访问权限和权限设置。当 Claude 遇到与某个子代理描述匹配的任务时，会自动将任务委派给该子代理，子代理独立工作并返回结果。Claude Code 内置了 Explore（只读代码搜索，使用 Haiku 模型）、Plan（计划模式研究代理）和 general-purpose（全工具通用代理）等子代理，用户也可以创建自定义子代理。
> 2. 怎么用
> 创建子代理最简单的方式是在 Claude Code 中运行
> /agents
> 命令，进入交互式界面选择"Create new agent"，然后选择作用域（用户级或项目级），输入描述后由 Claude 自动生成配置。也可以手动创建 Markdown 文件，放在
> .claude/agents/
> （项目级）或
> ~/.claude/agents/
> （用户级）目录中：
> ---
> name:
> code-reviewer
> description:
> Reviews
> code
> for
> quality
> and
> best
> practices
> tools:
> Read,
> Glob,
> Grep
> model:
> sonnet
> ---
> You
> are
> a
> code
> reviewer.
> Analyze
> the
> code
> and
> provide
> actionable
> feedback.
> 还可以通过 CLI 标志以 JSON 传递临时子代理：
> claude --agents
> '\{ "code-reviewer": \{ "description": "Expert code reviewer.", "prompt": "Focus on code quality and security.", "tools": \["Read","Gr…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
