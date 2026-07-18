---
title: AI 编程工程化：Skill——给你的 AI 员工装上技能包
date: 2026-03-14 23:04:01+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- 命令行工具
categories: []
scenarios:
- 命令行工具
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7616660062761549858
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:9ecb9ff61db1ec4246d3f1c917ce56585d9dfbbc3be3bc9c33487fec7ec4f39f
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 30
captured_at: '2026-07-18T04:19:14.028568Z'
source_capture_sha256: sha256:91d6e4d0b7b6f2c82530406e95367b5287ae6ea2087d5ae615b37804a9b509f0
source_capture_chars_original: 3984
source_publication_excerpt_chars: 798
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7616660062761549858](<https://juejin.cn/post/7616660062761549858>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 上一篇我们讲了 Command——把自己的重复操作封装成一键命令。
> Command 解决的是「你的流程」。
> 但还有另一个问题：
> 你可能不知道这件事该怎么做
> 。
> 先说一件让我有点尴尬的事
> 有一次，一个项目着急上线，我让 Claude Code 帮我做了一遍安全 review。
> 它给出的结论是：「代码整体符合安全规范，未发现明显漏洞。」
> 我觉得挺好，就这样上线了。
> 后来装了一个专门做安全审查的 Skill，同样的代码跑了一遍。
> 它找出来 3 个问题：一处 JWT 没有校验 expiration，一处接口缺少频率限制，一处敏感字段在日志里被打印出来了。
> 都是我平时不太关注、但真的会出事的点。
> 我后来才想明白：问题根本不在 AI。
> 我说的是「帮我做安全 review」。但我自己不懂安全审查的标准框架。AI 拿到这个 Prompt，只能按「通用理解」走。
> 那个 Skill 不一样。它是真正做过安全工程的人写的，把自己的检查清单和判断框架全部写进去了。
> 你的水平决定了你的 Prompt 上限。
> 装一个 Skill，就是装上了别人的经验上限。
> 什么是 Skill
> 说白了，Skill 是一个打包好的 Prompt 工作流，通常放在一个叫
> SKILL.md
> 的文件里。
> 和 Command 一样，也是 Markdown 文件。但它不只是「一段 Prompt」，而是一套
> 完整的工作流描述
> ——触发条件、执行步骤、质量标准、异常处理，全都写进去了。
> 更关键的是：
> Skill 可以被社区分发和安装
> 。
> 别人打磨好的工作流，你装上，直接用。
> 你可以把它理解成给 AI 员工的
> 专业技能包
> 。
> Rule 告诉 AI 规矩，Command 告诉 AI 你的操作流程，Skill 让 AI 具备一项专业能力——哪怕那个领域你自己也不是专家。
> Skill 和 Command 有什么区别
> 这是被问最多的问题。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
