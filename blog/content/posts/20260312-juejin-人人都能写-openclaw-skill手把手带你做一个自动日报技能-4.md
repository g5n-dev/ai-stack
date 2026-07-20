---
title: 人人都能写 OpenClaw Skill！手把手带你做一个自动日报技能
date: 2026-03-12 13:04:46+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- AI Agent
- Python
- 数据库
categories:
- AI 工程
- 数据
scenarios:
- AI/ML项目
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7615972610168176686
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:97a39e4f3228b3e71ace387f4b3a787ded48fe686d17cc80d880824a420b1760
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 35
captured_at: '2026-07-18T04:19:10.176264Z'
source_capture_sha256: sha256:01c4ecce0f8425fbd15da42691994d3a38bbaf2891e1aa0de7a2524d2731249e
source_capture_chars_original: 3299
source_publication_excerpt_chars: 731
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_7b6b7b6aac55f2c483b428dc8a256126543c19fca18d3dc79db9dadc0ee04063
revision_id: rev_a2f1111194b80614d3d5b3c0403ae25a5476b5655ba7a6eb773116d47c9d71ca
event_id: evt_0b418ddd66602ede3be350b1dd77557eff070926a19001903460edd01115543d
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-03-12T05:04:46Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7615972610168176686](<https://juejin.cn/post/7615972610168176686>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 人人都能写 OpenClaw Skill！手把手带你做一个自动日报技能
> 引子
> 我前几天在想一个问题：AI Agent 到底怎么才能"学会"新技能？
> 不是那种微调训练的学法，而是——我今天有个新需求，希望 Agent 明天就能处理，后天就能自动化。这种"即插即用"的能力扩展，有没有一种足够轻量的实现方式？
> 后来我在 OpenClaw 里找到了答案：
> Skill
> 。
> 它的做法简单到有点反直觉——写一个 Markdown 文件，描述清楚"你是谁、什么时候用、怎么做"，放到指定目录下，Agent 下次对话就能自动识别和执行。不需要编译，不需要注册，不需要重启。
> 这篇文章我会手把手带你写一个"每日技术日报"Skill，从目录结构到完整代码，再到调试上线。你会发现，门槛真的没有想象中那么高。
> Skill 是什么
> 在 OpenClaw 的架构里，Skill 是 AI Agent 的能力扩展单元。但它不是传统意义上的代码插件——它是一份
> Markdown 格式的操作手册
> 。
> 工作原理：
> Agent 启动时扫描所有 Skill 的
> name
> 和
> description
> （元数据层，常驻内存）
> 用户发来请求时，Agent 根据 description 判断该不该触发某个 Skill
> 触发后，Agent 才去读取 SKILL.md 的正文内容（指令层，按需加载）
> 按正文中的指令执行操作
> 这种三层加载的设计（元数据 → 正文 → 附属资源）是为了节省上下文窗口。毕竟 Agent 的上下文是有限资源，不能把所有 Skill 的内容都塞进去。
> 你可以把 Skill 理解为给 Agent 写的 SOP（标准操作程序）。写得好的 Skill，Agent 拿到就能干活。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
