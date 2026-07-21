---
title: Claude Code AI 子代理（Subagents）：何时用、怎么用完全指南
date: 2026-02-18 22:40:49+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- MCP
- AI Agent
- 大语言模型
- 数据库
categories:
- 大模型
- 数据
scenarios:
- AI/ML项目
- 大语言模型
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7606523741611950099
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:747bb05aae07f3979e87137704101c1f0c1ba1bc38376faaafed04504a35c761
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 41
captured_at: '2026-07-18T04:17:25.537620Z'
source_capture_sha256: sha256:9718f086e316a6a14dd941d6d276a3f59dc17882a2ef7225e6ddea89f066fd93
source_capture_chars_original: 5804
source_publication_excerpt_chars: 794
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_0e9ebd0a7c8ddc274b145963c42a3fe5f47ac7d7f56c2b437965304e7c66bd7d
revision_id: rev_3ec63fef5844bd6eab0f89ddaa33fdc145853ca857461d578c25d775a16b628e
event_id: evt_6d88734f3f8626955e3ca93fb5be972c5214bd0e0671e297008b73c4814d075c
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-18T14:40:49Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7606523741611950099](<https://juejin.cn/post/7606523741611950099>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> AI 子代理（Subagents）：何时用、怎么用完全指南
> 写在前面
> 本文已收录到
> AI编程一站式导航
> 。本文链接：\[03.3 AI 子代理使用完全指南\]\(
> code.ai80.vip/ai-tool-gui…
> AI 子代理使用完全指南\) 强烈推荐：AI编程巴士网站：
> 稳定纯净的ClaudeCode套餐供应
> ；
> 你的 Agent 花了 15 分钟探索，找到了你需要的东西，然后忘了你的请求。现在你在 400 行日志里滚来滚去，试图找出哪里出了问题。
> 你试过规则（Rules）。试过命令和技能（Commands and Skills）。它们有帮助，但没解决根本问题：
> 一个上下文窗口能装的东西有限，装太多就乱了。
> 解决方案是子代理（Subagents）。这里有一些关于子代理是什么、何时用、怎么优化的实战建议。
> 你可能会好奇：
> 子代理到底是什么？
> 跟技能（Skills）有什么区别？
> 什么时候该用子代理？
> 怎么定义和优化子代理？
> 有哪些常见坑？
> 什么是子代理
> 子代理是你定义的专家 Agent，主 Agent 可以生成它来做聚焦、隔离的工作，然后把结果报告回来。
> 就这么简单。干净的上下文是让主线程保持可读的关键，而工作本身可以很嘈杂。对于高级用户，子代理还提供了并行性、工具范围控制、混合模型的能力，把单个对话变成一个协作团队。
> 在 Builder 里，你可以通过在
> .builder/agents/
> 创建一个 Markdown 文件来定义子代理，包含名称、描述和工具列表。定义好后，你可以在聊天中按名称调用它，或者一次生成多个子代理来并行工作。
> 你可以在
> Builder 文档
> 里读到所有关于使用子代理的内容。
> 为什么子代理在实践中感觉很好
> 大多数
> Agent IDE
> 共享相同的工作流循环。你描述意图，Agent 探索，它改代码，然后你需要验证。
> 问题是探索和验证产生最多的输出。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
