---
title: Dify 接入蓝耘 MaaS：从 0 搭建一个企业知识库问答助手
date: 2026-06-04 22:46:26+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- RAG
- 大语言模型
categories:
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
- RAG应用
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7647356541462626356
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:2eaaaa078c987ec3b1e52637451e94fc168e8bebbc73a4e015feb77f5002747b
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 32
captured_at: '2026-07-18T04:21:36.221496Z'
source_capture_sha256: sha256:76a66a8bdde3f85b8fcdeeb09d408bb154398403e0726a6d10322f7d59953367
source_capture_chars_original: 5471
source_publication_excerpt_chars: 791
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_39d45aec5148632f4c0bc23e7023c96f6b0562292303f696949a9c7a68e3dae4
revision_id: rev_58980e17305cb82d1352550c65a7fc488d153f4b9d9d7619dbdc31a3637d635e
event_id: evt_942e3bffa8cd08e2259d8dbaf2ae5c5278c206405727364f9db741d457a15ef5
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-06-04T14:46:26Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7647356541462626356](<https://juejin.cn/post/7647356541462626356>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 最近很多团队都在尝试把大模型接入到自己的业务里，但真正落地时会发现一个问题：直接和大模型聊天并不等于拥有一个可用的业务助手。
> 比如我们想让 AI 回答公司产品文档、接口说明、运维手册、售后 FAQ 里的问题，如果只是直接问通用大模型，它很可能并不知道这些内部资料。即使模型能回答，也可能出现信息过期、回答不稳定、甚至凭空补充内容的情况。
> 这类场景更适合用 RAG 知识库问答来解决：先把自己的文档上传到知识库，用户提问时先从知识库中检索相关内容，再把检索结果交给大模型生成回答。这样模型回答时就有了明确的上下文依据。
> 本文我会用 Dify 的「知识库 + 聊天机器人」模板，接入蓝耘 MaaS 模型服务，并在 LLM 节点中选择 GLM-5.1 作为知识库问答模型，从 0 搭建一个可以基于文档回答问题的企业知识库助手。
> @\[toc\]
> 一、为什么选择蓝耘 MaaS + Dify
> 在这个方案里，Dify 和蓝耘 MaaS 承担的角色并不一样。
> Dify 更像是 AI 应用搭建平台。它负责应用创建、知识库管理、工作流编排、节点调试、Prompt 配置和最终对话界面。通过 Dify，我们可以不用从零写后端，就完成一个知识库问答应用的基本链路。
> 蓝耘 MaaS 则提供大模型调用能力。在知识库问答流程中，模型主要负责理解用户问题、结合检索到的文档内容组织答案，并把结果返回给用户。
> 两者结合以后，整体链路可以理解为：
> 用户提问 -&gt; Dify 接收问题 -&gt; 知识库检索相关文档 -&gt; 蓝耘 MaaS 模型生成回答 -&gt; Dify 返回答案
> 这套组合的优势是比较清晰的：
> 不需要从零开发完整的 RAG 后端。
> Dify 可以可视化管理知识库和工作流。
> 蓝耘 MaaS 可以作为大模型底座接入到应用链路中。
> 适合快速验证企业文档助手、产品 FAQ 助手、智能客服、内部运维助手等场景。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
