---
title: 还有人在问 Skills 是啥？感觉和 prompt 一样
date: 2026-03-15 15:23:22+08:00
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
external_url: https://juejin.cn/post/7617156058722009124
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:6877cdedf834ed6172df5c23c773e304842f1957d8341d54182f171e42c060b7
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 29
captured_at: '2026-07-18T04:19:16.837448Z'
source_capture_sha256: sha256:591c2cc32e38ec7370a57aa29fa5d2cf90f3f74c2c5007aee918770809cc978d
source_capture_chars_original: 4710
source_publication_excerpt_chars: 778
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_e4320d3de94c969578acd2954e8c37232e9fbe185fb7e780fb88eb8c26a94554
revision_id: rev_0f1f893b6da86bee3f43f9a5070f2ace594b63e34d5b6593516a4251fdbb6eef
event_id: evt_8417f6d14c067ef1f12b698e5215c71c53fb17e02a8daf68f91927eeb1737c9b
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-03-15T07:23:22Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7617156058722009124](<https://juejin.cn/post/7617156058722009124>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> Hi，大家好，我是三金～
> 最近有小伙伴问我，skills 怎么感觉和 prompt 一样？为啥又搞一个概念出来？
> 其实我和他一样，在第一次看到 skills 这个东西时，也以为它就是个进阶版的 prompt：能反复使用，减少上下文损耗。
> 但深入研究了一下发现，还是兔羊兔森破了。在很多场景里，大家想复用的根本就不是一句话要怎么写，而是一整套的做事方法。比如：
> 代码审查怎么审？
> 文档改写按什么口径改？
> 发布前要不要核对清单？
> 碰到某类任务需要先看哪些资料？
> 以及最终的交付产物应该是怎样的等等
> 这些才是更难稳定的部分，也是大家最想复用的重点！
> Skills 解决了什么问题？
> 在 skills 出现之前，我们通常使用自定义 command、自定义 Agent 来解决一些重复工作，但实际效果可能并不能如我们所愿的那样好。
> 造成这种结果的原因通常来说不是单点的。
> 有时候是描述没补全，有时候是输出格式跑偏；还有时候是模型只知道大方向，但漏掉了一个团队约定、一个检查步骤，或者一份本来需要参考的本地资料。
> 只靠聊天现场去补充这些东西，往往费力不讨好。Skill 要做的事情，恰好就是把这些会反复出现的指引、资料、约束提前给装到一个包里，让它每次开工都从更接近正确的位置起跑。
> 对于个人开发者或者独立开发者来收，最直接的收益就是少解释。A 社也明确提到过几类典型受众：
> 想让 Claude 稳定遵循特定工作流的开发者
> 会自动化重复任务的高级用户
> 希望统一 Claude 行为方式的团队。
> 以及想把集成能力和稳定流程放在一起用的 MCP connector builders
> 落到团队里 \*
> ，
> \*一个共享 Skill 可以带着同样的写作口径、审查标准、目录约定或者交付模板，哪怕被不同人反复调用，虽然不能保证结果会一模一样，但起跑线会更接近，这点是非常重要的！…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
