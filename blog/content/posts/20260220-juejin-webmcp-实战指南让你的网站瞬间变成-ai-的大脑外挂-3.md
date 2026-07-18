---
title: WebMCP 实战指南：让你的网站瞬间变成 AI 的“大脑外挂”
date: 2026-02-20 09:01:37+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- MCP
- AI Agent
- JavaScript
- 数据库
categories:
- AI 工程
- 数据
scenarios:
- AI/ML项目
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7607097714301042698
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:4a0200d7d9c3a68d45267a6d4c75aa511dc33956d7f5270cee30dbfad787cf95
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 32
captured_at: '2026-07-18T04:17:30.746657Z'
source_capture_sha256: sha256:a5699406118c0b6527f3ee06b2fa2e59ec331cef1bf5ba80ff87dfdd273ebc65
source_capture_chars_original: 2783
source_publication_excerpt_chars: 644
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7607097714301042698](<https://juejin.cn/post/7607097714301042698>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 一、 AI 终于不用“瞎猜”你的网页了
> 我们可以把 WebMCP 想象成一种\*\*“翻译官协议”\*\*：
> 以前的 AI（视觉模拟派）
> ：就像一个老外在看一份全中文的报纸，他得先拍照，再识别文字，最后猜哪里是按钮。一旦你把按钮从左边挪到右边，他就找不到了。
> WebMCP（接口直连派）
> ：你的网站现在给 AI 提供了一个\*\*“操作说明书”\*\*。AI 进门后不用看页面长什么样，直接问：“那个‘查询余额’的功能在哪？” 你的网站直接通过 WebMCP 告诉它：“在这里，发个 JSON 给我，我就告诉你结果。”
> 一句话总结：WebMCP 让网页从“给人看的界面”变成了“给 AI 调用的函数”。
> 二、 核心能力：WebMCP 的“两把斧”
> 在实际开发中，WebMCP 提供了两种接入方式：
> 宣告式（适合简单动作）
> ：在 HTML 里加个属性，就像给按钮贴个“AI 可读”的标签。
> 命令式（适合高级逻辑）
> ：用 JavaScript 编写具体的执行函数，适合处理复杂计算。
> 三、 实战：WebMCP 的具体使用方法
> 目前，你可以在
> Chrome Canary \(v145+\)
> 中通过以下步骤实现一个“AI 自动分析监控日志”的功能。
> 1. 开启实验室开关
> 在浏览器地址栏输入：
> chrome://flags/#enable-webmcp
> ，将其设置为
> Enabled
> 并重启。
> 2. 定义“说明书” \(mcp-config.json\)
> 在你的网站根目录放置一个配置文件，告诉 AI 你有哪些能力。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
