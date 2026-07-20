---
title: AI内容工厂2.0：我把OpenClaw换成ArkClaw，接管了整个飞书
date: 2026-03-13 07:36:37+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- MCP
- AI Agent
categories:
- AI 工程
scenarios:
- AI/ML项目
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7616265766074220554
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:b5ff4eacded6a1c4c7ce9e0b358ead60753eaecb752e9bea5252f1787c225aae
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 37
captured_at: '2026-07-18T04:19:13.142855Z'
source_capture_sha256: sha256:f9fb4da6edde332189dc2f10766f1aeb8e979c802c6aa6a17250cd08127e1c9a
source_capture_chars_original: 3673
source_publication_excerpt_chars: 780
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_798ae424dcdf8adbcf5cbde9dfeb447c1441e4ebfdd642340a35aea319ea3993
revision_id: rev_e35c045d816154fe0ac51f62ddfb4f5c3cdc0ba64bcdcc5a9f2744d376b6dd3a
event_id: evt_af8535c8616fcdb2b9488c3bd4be02092efe6e70acab8265442e8e77e16fe36a
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-03-12T23:36:37Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7616265766074220554](<https://juejin.cn/post/7616265766074220554>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 之前写过一篇：用 OpenClaw + Obsidian 搭建内容工厂，写出了百万阅读的爆文。
> 那篇文章有人复刻成功。但也有人用了一段时间后发现：灵感还是在积压，选题还是不知道选哪个，写完的文章还是找不到。
> 我自己用下来也发现了根本问题——Obsidian 不适合流动。手机刷到好内容，根本不可能随手存进去。而且 OpenClaw 虽然能读 Obsidian，但往里面写很危险，双向链接一断就全坏了。
> 所以只能单向读，AI 帮不了你管理。内容的整理负担还是全在自己身上。
> 那是 1.0。
> 今天来说 2.0——换掉 Obsidian，用飞书做底座：
> 刷到好内容，直接转给 OpenClaw，它帮你存进灵感库、打标签、拆选题。想写东西了，问它推荐，它从灵感库里给你选题。你选定一个，它建档、出大纲、生成初稿、创建云文档，链接自动回填到表格里。你去改稿，改完一句话告诉它定稿了，它帮你归档进知识库。
> 也就是说，你负责扔素材和做决定，其他全部交给 AI。
> 工欲善其事，必先利其器
> 不过先说工具。
> 1.0 文章发出来之后，问我最多的问题不是怎么用，是怎么装。OpenClaw 的安装对普通人来说门槛不低，Windows 上尤其折腾。
> 2.0 版本我直接换了一个开箱即用的方案：火山引擎的 ArkClaw
> 订阅 Coding Plan 首月 9.9 元，ArkClaw 直接就能用，不需要自己部署任何东西，Web 端打开就是。
> Coding Plan 本来是给开发者设计的 AI 编程订阅服务，但拿来跑 ArkClaw 这种智能 Agent 同样是绝配——token 额度大，按月订阅不用每天盯着用量，也不会因为 Agent 跑任务太多被限速。
> 入口链接：
> v2ig.cn/cRm03IcFyUU…
> 但真正让我决定用它的，不是省了安装这步。
> 是因为它和飞书是同一套生态。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
