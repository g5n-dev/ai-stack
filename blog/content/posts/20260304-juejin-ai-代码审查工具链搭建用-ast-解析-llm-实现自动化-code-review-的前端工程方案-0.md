---
title: AI 代码审查工具链搭建：用 AST 解析 + LLM 实现自动化 Code Review 的前端工程方案
date: 2026-03-04 10:32:30+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- 大语言模型
- TypeScript
categories:
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7613237473859256329
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:26ebad8f90971173797b5c8f307c34b475cb445fb6f480c22bdb5f53952db989
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 53
captured_at: '2026-07-18T04:18:33.113763Z'
source_capture_sha256: sha256:698d1b25d43c026a7ca0da57c9696475a3d695dd4a6cbb8aa80bc098a622d281
source_capture_chars_original: 5759
source_publication_excerpt_chars: 757
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7613237473859256329](<https://juejin.cn/post/7613237473859256329>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> AI 代码审查工具链搭建：用 AST 解析 + LLM 实现自动化 Code Review 的前端工程方案
> 团队到了 15 人以上，Code Review 就开始变味了。
> 不是没人 review，而是 review 变成了"LGTM 流水线"——打开 PR，滚动两屏，留一句 "looks good to me"，合并。真正的逻辑问题、潜在的性能隐患、不符合团队规范的写法，全靠运气。
> 人工 review 的瓶颈不是态度，是带宽。一个资深工程师一天能认真 review 多少个 PR？3 到 5 个，顶天了。剩下的要么排队，要么糊弄。
> 所以我们开始想：
> 能不能让机器先过一遍，把"明显有问题"的地方标出来，人再去看真正需要判断力的部分？
> 这就是这篇文章要聊的事——用 AST 解析做结构化分析，用 LLM 做语义级审查，把两者串成一条自动化 Code Review 工具链。
> 先搞清楚：人工 Review 到底哪里不行？
> 不是人不行，是人干了太多不该干的活。
> 一次典型的 Code Review，reviewer 的注意力大概分布在这几个层面：
> 层面
> 举例
> 能否自动化
> 格式规范
> 缩进、命名、import 顺序
> ESLint/Prettier 已解决
> 模式违规
> 组件里直接调 fetch、没用 hooks 封装
> AST 可以搞定
> 逻辑隐患
> useEffect 依赖缺失、竞态条件
> AST + 规则引擎可以搞定
> 业务语义
> 这个字段不该在这里改、这段逻辑和需求不符
> 需要 LLM
> 架构决策
> 该不该拆微服务、该不该用新方案
> 需要人
> ESLint 覆盖了第一层，但第二到第四层基本是裸奔状态。
> 我们要做的，就是把中间这三层自动化掉。
> 整体架构：两阶段流水线
> 核心思路一句话：
> AST 做确定性分析，LLM 做模糊判断
> 。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
