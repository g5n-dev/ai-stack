---
title: Claude Code 使用技巧：把“聪明实习生”变成你的王牌搭档
date: 2026-03-16 08:20:51+08:00
draft: false
entry_kind: auto
tags:
- 掘金
categories: []
scenarios: []
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7617454306796699689
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:47f687ef3b72fb90a8fb22d91caaa1f92a99590d79e3fea097b827b4de4845e2
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 33
captured_at: '2026-07-18T04:19:19.183043Z'
source_capture_sha256: sha256:fbc569ad037807aefcf8f66b878a1aae017270b1bb8d3248ea7a37a445f87744
source_capture_chars_original: 3368
source_publication_excerpt_chars: 737
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7617454306796699689](<https://juejin.cn/post/7617454306796699689>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 前言：AI浪潮下，大家一定用过Claude Code吧，在我看来，Claude Code不仅是一个“会写点代码的聊天机器人”，更是一个结对编程伙伴。用得好，它能显著提升个人效率，也能在团队里形成统一的工程规范。接下来，本文将介绍我在项目中关于Claude Code的使用技巧。
> 一、先统一一个心智：把 Claude Code 当“快速实习生”
> 1. 不要把 Claude 当“答案机”
> 更好的定位是：
> 一个非常能干、记忆力变态好、但需要你给清晰任务的实习生
> 。
> 这会直接影响你怎么写指令、怎么验收结果：
> 不指望“随便一问就给完美答案”
> 而是像带实习生一样：给目标、给边界、给上下文，让它帮你干具体活
> 2. 你负责“要什么”，它负责“怎么做”
> 你负责
> ：
> 业务目标（要实现什么功能/解决什么问题）
> 约束条件（架构分层、不跨层调用、安全要求等）
> 风格与规范（命名规则、日志规范、DTO 字段类型等）
> 它负责
> ：
> 找文件、读代码、分析依赖
> 设计实现方案（plan 模式下给出计划）
> 修改代码、跑测试、写提交信息草稿
> 3. 一定要配合 Git 使用
> 大改动前
> ：先自己
> git commit
> 一次，保证有可回滚的基线
> Claude 改完一轮
> ：自己再用
> git diff
> 快速扫一遍
> 不满意的改动
> ：直接
> git checkout
> 回滚这次修改，然后重写更清晰的指令让它再来
> 二、三步完成“从 0 到能干活”的配置
> 1. 安装 + 验证：两个关键点
> 强调两个
> 别踩坑
> 的地方：
> Node 版本必须 ≥ 18
> node --version
> # 确认版本号，推荐 18+ 或 20+
> 安装完成要立刻自检
> npm install -g @anthropic-ai/claude-code…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
