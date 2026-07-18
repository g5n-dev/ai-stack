---
title: Spring AI 多模型对话 Demo 实战：OpenAI/Ollama 一套接口、Redis 会话记忆、SSE 流式输出、AOP 日志打点
date: 2026-02-17 15:40:46+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- Java
- 数据库
categories:
- 数据
scenarios: []
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7606793134375534655
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:f47574623c036ed8cb0f2e28e18577f2391614fce00829f082cbe89c821d51bd
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 71
captured_at: '2026-07-18T04:17:23.133971Z'
source_capture_sha256: sha256:b7186c05d5ca6271a94fe32758a6a4ffa4248fb5f5e36575b8ff59d41504c2e5
source_capture_chars_original: 6000
source_publication_excerpt_chars: 800
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7606793134375534655](<https://juejin.cn/post/7606793134375534655>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 这是一套可直接复用的 Spring AI Demo：同一套 API 同时支持
> OpenAI
> 与
> Ollama
> ，按
> provider
> 路由模型，支持
> model
> 运行时覆盖；会话上下文通过
> Redis 持久化 ChatMemory
> 进行多轮对话；同时提供同步与
> SSE 流式
> 接口；并用
> AOP
> 统一记录耗时、token 使用与异常。
> 下面按项目现有代码结构，把关键实现串起来讲清楚（复制即可跑）。
> 依赖与版本：Spring Boot 3.5.x + Spring AI 1.1.2 + JDK17
> 项目用 BOM 锁定 Spring AI 版本，避免依赖漂移：
> &lt;!-- pom.xml --&gt;
> &lt;
> parent
> &gt;
> &lt;
> groupId
> &gt;
> org.springframework.boot
> &lt;/
> groupId
> &gt;
> &lt;
> artifactId
> &gt;
> spring-boot-starter-parent
> &lt;/
> artifactId
> &gt;
> &lt;
> version
> &gt;
> 3.5.8
> &lt;/
> version
> &gt;
> &lt;
> relativePath
> /&gt;
> &lt;/
> parent
> &gt;
> &lt;
> properties
> &gt;
> &lt;
> java.version
> &gt;
> 17
> &lt;/
> java.version
> &gt;
> &lt;
> spring-ai.version
> &gt;
> 1.1.2
> &lt;/
> spring-ai.version
> &gt;
> &lt;/
> properties
> &gt;
> &lt;
> dependencyManagement
> &gt;
> &lt;
> dependencies
> &gt;
> &lt;
> dependency
> &gt;
> &lt;
> groupId
> &gt;
> org.springframework.ai
> &lt;/
> groupId
> &gt;
> &lt;
> artifactId
> &gt;
> spring-ai-bom
> &lt;/
> artifactId
> &gt;
> &lt;
> version
> &gt;
> $\{spring-ai.version\}
> &lt;/
> version
> &gt;
> &lt;
> ty…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
