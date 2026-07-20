---
title: 用 ASCII 草图 + AI 快速生成前端代码
date: 2026-02-17 03:10:02+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- 大语言模型
categories:
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7606548472222695466
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:f1344a468d17abd712dad780b3ba2006cd38b9d923e33b9d2176e83ed29087ea
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 24
captured_at: '2026-07-18T04:17:23.746708Z'
source_capture_sha256: sha256:50fafb5062bae7a4e1582bf4aae434c57e247ff064be4dba7340106c15b95001
source_capture_chars_original: 3872
source_publication_excerpt_chars: 664
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_276a9e7141ed18913ff26ed52ab0d98f67b142be3dce0cd84f795428fa85e73c
revision_id: rev_0e7a91cf4d80406de5da4fdde4a25ced376b6995c5103c2fd3bc594c82de1c0f
event_id: evt_edbac8028e58ad40933810fb1df1f85b287fc4ba61175f9143c6208f7400b435
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-16T19:10:02Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7606548472222695466](<https://juejin.cn/post/7606548472222695466>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 引言
> 从想法到代码，中间往往要经历画原型、出设计稿等环节。
> 用 ASCII 草图，可以跳过大量原型绘制、结构拆解和手动搭骨架的中间步骤。
> 这种表达方式其实一直存在，但真正让它进入工程流程的，是 AI 的能力提升。大语言模型对结构化文本具有很强的解析能力，能够识别文本中的层级、对齐关系与空间划分，并将这些结构信息稳定地映射为组件树和页面布局。
> 因此，ASCII 不再只是沟通草稿，而成为一种可执行的结构描述。
> 什么是 "ASCII 草图"
> 提到 ASCII，很多人的第一反应可能是那个年代久远的“字符画”。没错，ASCII 草图就是用字符来构建页面布局。
> 在 AI 时代，这种看似简陋的草图，其实蕴含着巨大的能量。大语言模型（LLM）对
> 结构化文本
> 的理解能力极强。相比于模糊的自然语言描述（“我要一个左边宽右边窄的布局”），ASCII 草图提供了一种
> 所见即所得的结构化 Prompt
> 。
> 简单来说，ASCII 草图充当了
> 视觉蓝图
> 的角色，AI 根据这个结构生成代码。
> 为什么要让 AI 先生成 ASCII 草图 ？
> 你可能会想：直接让 AI 生成代码不就行了吗？为什么要中间多这一步？
> 这就涉及到一个
> 沟通精度
> 的问题。
> 直接描述布局的问题
> 用自然语言描述布局，很容易产生歧义。比如你说"左边放导航，右边放内容"，AI 可能会理解成左右各占 50%，而你想要的是导航 200px 宽度。你说"卡片要突出一点"，AI 理解的"突出"可能是加阴影，而你想要的是加大字号。
> 这些细节上的偏差，会导致生成出来的代码需要反复调整。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
