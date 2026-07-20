---
title: 手写 AI 编程 Agent 的命令执行工具：我被 child_process 坑出来的实战经验
date: 2026-07-14 22:32:28+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- AI Agent
categories:
- AI 工程
scenarios:
- AI/ML项目
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7662273240988057615
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:f83661ef367d1ffbff1a371047a69c92157a768e9990ac1fc82bbc40ce32c858
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 48
captured_at: '2026-07-18T04:21:54.670268Z'
source_capture_sha256: sha256:9bc6cbf0317632048064dc1df5c3ed62d857e64800dddd2fa8522d407839845d
source_capture_chars_original: 4677
source_publication_excerpt_chars: 735
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_837c5329bc2c11dbe2b6bda2621d5c83ee7e0fda50913a7e2f12048f6d4d6cfc
revision_id: rev_7c8fdcf5fc201f8994dc1c2c11057171dd4eebe92d9bda712a5f742351031f57
event_id: evt_59b0081ac8044428968727a5b30c1ea089733f9847ba959b2146b52b58d485e5
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-14T14:32:28Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7662273240988057615](<https://juejin.cn/post/7662273240988057615>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 前阵子折腾 AI 编程 Agent 的 Demo，想实现个很简单的效果：跟大模型说一句「用 vite 建一个 React 的 todo 项目」，它就能自动把命令跑完、项目建好。本来以为很简单，不就是调用 Node 的 child\_process 跑个命令么，结果前前后后卡了我两天。要么命令悄无声息没反应，要么直接报找不到命令，Windows 和 Mac 上表现还不一样。踩完一圈坑我才发现，这个看起来最基础的 API，细节里全是门道。今天就顺着我当时踩坑的思路，把 child\_process 写命令执行工具的完整过程捋一遍，省得你们再走弯路。
> 先说说为啥 Agent 非得用 child\_process
> 我最开始其实也疑惑过，直接在 Node 里调命令不行吗，为啥非要整个子进程出来？后来想明白了，Node 本身是单线程跑 JS 的，主进程要处理大模型调用、对话逻辑、状态管理这些事，总不能卡着等一条命令执行完吧？而且 bash 命令本质就是系统级的独立进程，跟 Node 进程本来就不是一回事，硬塞到主线程里反而会把整个 Agent 堵死。
> 你可以这么理解：Agent 主进程就像办公室里的项目经理，只管做决策、调度任务；跑命令这种外勤杂活，交给专门的同事（子进程）去干。同事出去跑任务的时候，项目经理该干嘛干嘛，不会被卡住，同事干完了通过专属通道（IPC 进程间通信）回传结果就行。
> 像 Cursor、Trae 这类 AI 编程工具，底层的命令执行能力本质都是这么实现的。大模型输出要执行的指令，Agent 封装一层调用 child\_process 开子进程跑命令，跑完把结果返回给大模型，再继续下一步操作。整个自动化的基础，就是这个看起来不起眼的子进程工具。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
