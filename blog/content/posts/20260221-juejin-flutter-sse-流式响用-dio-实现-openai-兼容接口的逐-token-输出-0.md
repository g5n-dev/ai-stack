---
title: Flutter SSE 流式响用 Dio 实现 OpenAI 兼容接口的逐 Token 输出
date: 2026-02-21 02:41:10+08:00
draft: false
entry_kind: auto
tags:
- 掘金
categories: []
scenarios: []
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7607332124487958591
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:d682d25a514350f5e024e9bf1f1d65e28d1a32c938b896e0f9894c9cba88ff2b
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 46
captured_at: '2026-07-18T04:17:31.488636Z'
source_capture_sha256: sha256:fd3f992e868790f7db075722de56c8a8602a710945572be4c746dc511a37cb51
source_capture_chars_original: 5151
source_publication_excerpt_chars: 713
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7607332124487958591](<https://juejin.cn/post/7607332124487958591>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> SSE 流式响应用 Dio 实现 OpenAI 兼容接口的逐 Token 输出（可直接复用）
> 在做 AI 提示词优化器 时，“等 10 秒一次性返回大段文本”的体验通常很差。
> 更好的体验是：
> 模型一边生成，你的 UI 一边展示
> （像打字机逐字出现）
> 用户能更快确认方向，必要时可以提前取消
> 这通常依赖
> SSE（Server-Sent Events）流式响应
> 。
> 本项目（PromptOptimizer）已经实现了一个
> 可复用的、OpenAI 兼容的 SSE 解析方案
> ：
> 网络层：
> dio
> +
> ResponseType.stream
> 协议层：解析
> data:
> 行，识别结束符
> \[DONE\]
> 业务层：把“逐 token 的片段”包装成
> Stream&lt;String&gt;
> 状态层（MVI）：Riverpod
> StateNotifier
> 订阅 stream，拼接到
> optimizedPrompt
> 本文会用“原理 + 实践 + 踩坑”的方式，带你从 0 到 1 搭出来。
> 1. 环境与版本（可复现）
> Flutter
> ：项目约定 Flutter 3.10+
> Dart SDK
> ：
> pubspec.yaml
> 中为
> sdk: ^3.10.3
> 网络库
> ：
> dio
> （见
> pubspec.yaml
> ）
> 运行命令（Windows / PowerShell）：
> flutter pub get
>
> dart run build\_runner build --delete-conflicting-outputs
>
> flutter run -d windows
> 2. SSE 是什么？一句话理解
> SSE 是一种“服务器主动推送”的 HTTP 响应形式。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
