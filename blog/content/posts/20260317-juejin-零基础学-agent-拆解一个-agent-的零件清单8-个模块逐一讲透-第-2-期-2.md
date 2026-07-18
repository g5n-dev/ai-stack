---
title: 零基础学 Agent ：拆解一个 Agent 的「零件清单」——8 个模块逐一讲透 第 2 期
date: 2026-03-17 12:14:38+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- RAG
- AI Agent
categories:
- AI 工程
scenarios:
- AI/ML项目
- RAG应用
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7618055361979039759
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:11d07553b768cb48632caffc5cbce4354d023a861f350e22b1f2dc522d1401cc
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 47
captured_at: '2026-07-18T04:19:22.160208Z'
source_capture_sha256: sha256:f9c7ba83a80a4a011c4b97dc5cd11f1e6ec48bd98f3b899ec12ad508e48bdc34
source_capture_chars_original: 4856
source_publication_excerpt_chars: 782
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7618055361979039759](<https://juejin.cn/post/7618055361979039759>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 大家好，我是AI淇橦学。
> 上一期我们搞清楚了 Agent 到底是什么：AI 大脑 + 工具 + 自主规划，能真正帮你做事，而不是只告诉你怎么做。
> 但光知道定义还不够。
> 如果你想
> 自己做一个 Agent
> ，或者
> 评估一个 Agent 好不好用
> ，就必须知道它内部由哪些部分组成——哪些是必须有的，哪些可以以后再加，缺了哪个会出什么问题。
> 这一期就来干这件事：把一个完整的 Agent 拆成 8 个核心模块，用「办公 Agent」这个案例贯穿全文，逐一讲透。
> 先看全貌：8 个模块是什么
> 一个完整的 Agent，通常由这 8 个部分组成：
> 目标
> （Goal）- 它到底要完成什么
> 模型
> （Model）- 用哪个 AI 大脑
> 工具
> （Tools）- 能调用哪些外部能力
> 记忆
> （Memory）- 能记住什么
> 规划
> （Planning）- 会不会自己拆解步骤
> 执行
> （Execution）- 能不能真正采取行动
> 反馈
> （Feedback）- 会根据结果调整吗
> 约束
> （Constraints）- 有哪些边界和限制
> 接下来一个一个拆解，每个模块我都会说清楚：
> 是什么、负责什么、具体怎么做、如果没有会怎样
> 。
> 模块一：目标（Goal）- 它到底要完成什么
> 目标是 Agent 的起点，也是终点。它定义了「任务成功」的标准。
> 目标不清楚，Agent 就不知道什么时候算「做完了」。
> 它可能做了一半就停下来，也可能做完之后还在继续做，或者做了一件你根本没想要它做的事。
> 在办公 Agent 里，目标的具体描述是：
> 输入
> ：一份合同模板 + 客户信息
> 输出
> ：把客户信息填入模板对应字段，另存为新文件
> 完成标准
> ：所有标注为「待填写」的字段都已被处理，原始模板未被修改，新文件成功保存
> 注意「完成标准」这一条——模糊的目标只说「填写合同」，清晰的目标还要说清楚「怎么算填好了」。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
