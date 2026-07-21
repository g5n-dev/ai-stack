---
title: 你的 nginx 在扼杀 AI 服务——为什么需要重新设计流量层
date: 2026-02-23 12:44:38+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- 大语言模型
- 数据库
categories:
- 大模型
- 数据
scenarios:
- AI/ML项目
- 大语言模型
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7609151073308196915
aliases:
- /posts/20260223-juejin-你的-nginx-在扼杀-ai-服务为什么需要重新设计流量层-3/
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:8259bdbe7f75a635c2002f0b29891240330481ab9a267c5f0747ac4c5f5bba78
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 32
captured_at: '2026-07-18T04:17:35.615252Z'
source_capture_sha256: sha256:22326b714a52947b707956d5c4c3723287458fa6c1b3d2986b58ec476b402e74
source_capture_chars_original: 1484
source_publication_excerpt_chars: 790
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_2b1d0397aa43e288de3f1e72fe5d2751db86163a2293d82765599eb8eea78e9a
revision_id: rev_b1b281f801a65bab2bf640e956c4823ad9a3709f636951bc88f36b672e72de61
event_id: evt_dddd8d372469c17a7170f7cc4b5e6f1e10543b3f21a03e803d9fc8d572f5dbe5
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-23T04:44:38Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7609151073308196915](<https://juejin.cn/post/7609151073308196915>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 四个数字，定义了这篇文章要讨论的问题：
> 3 秒
> ：用户能接受的最长等待时间，超过这个阈值流失率急剧上升。
> 47 秒
> ：一个 70B 模型在 A100 上完成一次完整推理的中位时间。
> 0.3 秒
> ：同一个模型输出第一个 token 的时间。
> $2.48
> ：一块 A100 GPU 每小时的按需定价。如果它在凌晨三点空转，这笔钱就消失了。
> 这四个数字的张力，就是 AI 基础设施最核心的工程问题：
> 用户要求即时响应，模型需要漫长思考，算力必须精确调度，而传统流量层对这一切一无所知。
> 目录
> 一个请求的生死：nginx 在做什么
> 第一个断层：响应不是一个包，是一条河流
> 第二个断层：后端可能还不存在
> 第三个断层：你永远不知道新模型有没有变傻
> 第四个断层：连接不是用完就扔的
> 第五个断层：推理失败的方式和 HTTP 500 不同
> 重新设计：AI 流量层需要什么
> A3S Gateway 怎么应对这五个断层
> 和现有方案的真实对比
> 实战：为 AI 后端配置完整代理
> 弹性扩缩容：数字背后的原理
> 1. 一个请求的生死：nginx 在做什么
> 让我们从最基础的问题开始：当一个请求进入 nginx 时，nginx 在做什么？
> 客户端  ──→  nginx  ──→  后端  ──→  nginx  ──→  客户端
> ↑                       ↑
>           收到完整响应             转发给客户端
> nginx 的核心模型是
> 代理缓冲（proxy buffering）
> 。它的默认行为是：
> 从上游接收完整的响应体
> 缓存到本地内存或临时文件
> 再把缓存的内容发给客户端
> 这个设计在 2004 年非常合理。HTTP 响应是静态文件、数据库查询结果、模板渲染输出——它们在生成时就已经完整，只是需要一个缓冲来应对客户端网络抖动。
> 但 LLM 的响应不是这样的。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
