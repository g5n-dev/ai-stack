---
title: WorkBuddy 上手实战：打造一个可用的本地 AI 工作台
date: 2026-06-25 23:42:10+08:00
draft: false
entry_kind: auto
tags:
- 掘金
categories: []
scenarios: []
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7655157905101062178
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:940d799f064d6f13b8f15a10ebd96e0e88f8a0fbf8f82f32566a6a0cd4208bc5
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 31
captured_at: '2026-07-18T04:21:46.270794Z'
source_capture_sha256: sha256:c0b1c621e42011b492133a62811dfefc545b25adb3d74693a4048eb45dcda253
source_capture_chars_original: 4158
source_publication_excerpt_chars: 727
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7655157905101062178](<https://juejin.cn/post/7655157905101062178>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> WorkBuddy 上手实战：打造一个可用的本地 AI 工作台
> 很多 AI 产品看上去都能聊天，但真正进到日常使用里，最常见的需求并不是闲聊，而是整理一段零散记录、起草一段通知、输出一份周报，或者把一个任务拆成清单。而WorkBuddy 更像一个本地工作台，而不是单一聊天框：它把任务输入、专家角色、技能扩展和自动化模板放在同一个界面里，适合把办公动作收拢到一处完成。
> 和只做对话的产品相比，WorkBuddy 的优势很明显：
> 任务入口更集中，不用在多个页面之间来回切换。
> 专家、技能、自动化是分层组织的，更贴近真实办公流程。
> 适合把总结、写作、清单、模板这些高频动作固定下来。
> 但 WorkBuddy 也有一个很现实的问题：它本身需要积分调用，工作量一大，积分消耗会很快，所以底层模型不能只看“能不能聊”，还要看吞吐、延迟和稳定性。
> 这次我把蓝耘 MaaS 接进 WorkBuddy，统一使用
> /maas/minimax/MiniMax-M2.5
> 作为模型调用，目标很直接：先把模型换对，再看工作台里的 Claw、专家中心、技能中心和自动化模板能不能真正用起来。
> @\[toc\]
> 一、整体方案
> 从首页看，WorkBuddy 的结构很清楚：左侧是任务和模块入口，中间是当前工作区，底部是对话输入区域。和普通聊天窗口相比，它更像一个可以分层组织任务的工作台。
> 这次实操的链路如下：
> WorkBuddy 首页 / 工作空间
> -&gt; 自定义模型配置
> -&gt; Claw 基础输入
> -&gt; 专家中心
> -&gt; 技能中心
> -&gt; 自动化模板
> 本次实操重点验证三件事：
> 模型是否能稳定接入。
> 工作台里的模块是否真的能承接办公任务。
> 输出结果是否足够直接拿去用。
> 二、准备工作
> 1.…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
