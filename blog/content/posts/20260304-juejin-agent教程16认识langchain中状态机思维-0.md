---
title: Agent教程16：认识LangChain(中)，状态机思维
date: 2026-03-04 01:39:34+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- Python
- 数据库
categories:
- 数据
scenarios: []
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7613032876864258088
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:3e8628ebf7b5bc8cc0fdbeee346488a60442c1f979f58a5d5aebb63d611bf527
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 30
captured_at: '2026-07-18T04:18:33.064246Z'
source_capture_sha256: sha256:3f07362fecbb638f1f791d30c197b9907ad9b47745cd48461bd1d752f1763ed5
source_capture_chars_original: 3582
source_publication_excerpt_chars: 743
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7613032876864258088](<https://juejin.cn/post/7613032876864258088>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 上一节我们列举了LangGraph的基本节点类型，但是只是知道，并不知道怎么组装和使用，先列举下来，后面讲如何组装：
> Node：一个函数（LLM调用、工具、判断）。
> Edge：跳转规则（普通边 + 条件边）。
> State：共享状态（情绪、记忆、亲密度等），支持Reducer自动合并。
> Checkpoint：自动持久化（内存/SQLite/Postgres），支持崩溃恢复 + 时间旅行调试。
> Interrupt：原生Human-in-the-loop（用户中途纠正、审批、回滚）。
> 一、状态机思维
> 在 LangChain 早期版本（包括 LCEL）中，绝大多数工作流本质上是
> 有向无环图（DAG）
> 或简单的线性流水线（Pipeline）。数据像流水一样从 A 流到 B 再流到 C，但很难 “回头”。
> LangGraph 最核心的突破就是它是支持环的有向图，相比于LangChain古早的链式版本极大的增强了灵活性。
> 假设，我们现在有这样一个业务，理想状态下希望LLM依次执行：
> 调用工具查询数据
> 格式化数据
> 打印结果
> 对，这就是早期的链式思维，一旦LLM因为其随机性出错，整个流程就会轰然倒塌。
> 因此，事实证明，链式操作救不了Agent开发。
> 一种更稳健，更方便影对随机性的设计哲学被LangGraph选中：状态机。
> 状态：可以理解为一组能被所有节点读取和更新的变量。
> 对状态的使用通常遵循这样的规则：
> 在Node中更新状态
> 在选择连线时读取状态
> 以上图为例，如果格式化失败，那么state='fail'，而在选择连线时，因为 state == 'fail'，因此进入了格式化自循环的连线。
> 在正式生产中，我们还可以加入
> fail\_count
> 这样的状态，来保证自循环的上限次数。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
