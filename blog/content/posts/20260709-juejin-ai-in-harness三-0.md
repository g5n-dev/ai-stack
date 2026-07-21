---
title: AI in Harness（三）
date: 2026-07-09 12:24:38+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- AI Agent
- 大语言模型
- Java
categories:
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7660395288364597294
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:026fb6131f054686579b4bbaf0a71edf3b4203845339532fc2c4642bfc416510
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 16
captured_at: '2026-07-18T04:21:52.234901Z'
source_capture_sha256: sha256:62e227e4271f2d9762c759ca98763da105151f5aaae35fc1723f3695fa3b336b
source_capture_chars_original: 3624
source_publication_excerpt_chars: 750
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_2997c21a65bdf0d241d6a800fce67f3d33456ff48ae448ac14316a7350f7a27e
revision_id: rev_77ab64357c343ab925aceacc91ebfb80b270faaaf422ef7a39c1208ddacdffe6
event_id: evt_af7847c8f990dc6d2d4d938421c7632bfdc6366ca546648c38874a2c7d010a76
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-09T04:24:38Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7660395288364597294](<https://juejin.cn/post/7660395288364597294>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 多Agent 协同 - 需要一个团队
> 前面我们实现了 Subagent、Background Task，为什么还需要多 Agent 协同呢？
> 一句话区分
> Background Task
> = "把这个工具调用
> 派到后台跑,我等结果通知
> "
> Subagent
> = "派一个新 agent
> 干一件具体事,跑完销毁,我等摘要
> "
> Teammate
> = "派一个
> 长期协作的队友
> ,我们持续异步通信"
> 对比表
> 维度
> Background Task
> Subagent
> Teammate
> 被派的是什么
> 一个工具调用\(bash\)
> 一个全新 agent\(独立 LLM + messages\)
> 一个全新 agent
> 谁在执行
> 工具 executor
> 新一轮 LLM 调用
> 新一轮 LLM 调用
> 生命周期
> 短\(工具一次调用结束\)
> 短\(派一次跑完销毁\)
> 长\(教学版限 10 轮\)
> 同步 / 异步
> 异步\(daemon thread\)
> 同步
> \(父等子返回\)
> 异步\(daemon thread\)
> 父是否阻塞
> 不阻塞,立即拿 placeholder
> 阻塞
> ,等子 agent 结果
> 不阻塞,立即拿"已派出"
> 通信方式
> 单向 — 后台→父 \(
> &lt;task\_notification&gt;
> \)
> 单向 — 子→父\(只回 last text\)
> 双向
> —
> MessageBus
> 文件邮箱
> 能否多个并行
> 是
> 否\(父 spawn 时阻塞\)
> 是
> 能否互相通信
> 不能
> 不能
> 能
> \(teammate 之间能 send\)
> 典型用途
> 慢命令\(
> ./mvnw test
> \)
> "分析 X 模块,做完告诉我"
> "重构后端 — 多 agent 长期协作"
> 能调用工具
> 不能\(它
> 就是
> 工具\)
> 能\(白名单子集\)
> 能\(白名单 + send\_message\)
> 人多力量大。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
