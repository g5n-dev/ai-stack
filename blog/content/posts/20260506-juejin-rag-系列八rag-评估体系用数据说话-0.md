---
title: RAG 系列（八）：RAG 评估体系——用数据说话
date: 2026-05-06 22:15:44+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- RAG
- 大语言模型
- 自然语言处理
- Python
- Java
- 数据库
categories:
- 大模型
- 数据
scenarios:
- AI/ML项目
- 大语言模型
- RAG应用
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7636615193972523054
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:0538a3a1538451117c0b9ebc2aace8a8dc1b91f52025e3a653d182a71e6b2eaa
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 25
captured_at: '2026-07-18T04:19:48.834138Z'
source_capture_sha256: sha256:76cb858ba2d87a93b1838c1ad3fb8b6b36bb89f18e7d85e781afb0c1abccd79b
source_capture_chars_original: 6000
source_publication_excerpt_chars: 776
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_fecd1744f21f5b685532550a6898752755f4c3d6ba616dfe50842ea747343819
revision_id: rev_c6987b6c73b3f85b3eeb700bc1fcc5499275a7868eab00a830c8328ac469c907
event_id: evt_c0722dd9d9013d10e02c615277a12fa7a089170d9ccff96f67d27dd2c2e59b5e
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-05-06T14:15:44Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7636615193972523054](<https://juejin.cn/post/7636615193972523054>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 为什么"感觉不错"不是标准？
> 前面七篇文章，我们搭起了一整套 RAG 流程：分块、Embedding、向量库、检索策略。系统跑起来了，你问它几个问题，回答看起来"还不错"。
> 但问题接踵而至：
> 迭代后真的变好了吗？
> 你换了 Embedding 模型、调了 chunk\_size、加了 MMR，但回答质量真的提升了吗？还是只是"感觉"变好了？
> 问题出在哪里？
> 某个问题回答得很差，是
> 检索阶段
> 没召回相关文档，还是
> 生成阶段
> 模型在胡说八道？
> 怎么向老板汇报？
> "我觉得我们的 RAG 系统挺好的"——这句话在数据驱动的团队里毫无说服力。
> RAG 系统的评估，不能靠感觉，必须靠数据。
> 本文会带你从零开始，用
> RAGAS
> 框架建立一套可量化的 RAG 评估体系，让你清楚地知道系统好不好、哪里差、怎么改。
> RAGAS 是什么？
> RAGAS（Retrieval-Augmented Generation Assessment）是专为 RAG 系统设计的开源评估框架。它的核心思想很朴素：
> 用 LLM 作为裁判，自动判断 RAG 系统的输出质量
> 。
> 为什么用 LLM 当裁判？因为传统的 NLP 评估指标（如 BLEU、ROUGE）只适合做翻译或摘要任务，它们通过字符串匹配来判断相似度，完全无法理解语义。而 RAG 的评估需要理解"这个答案是否基于上下文"、"这个回答有没有答非所问"——这正是 LLM 擅长的。
> RAGAS 提出了
> 4 个核心指标
> ，覆盖了 RAG 系统的两个关键阶段（检索 + 生成）：
> 四个核心指标详解
> 1. Faithfulness（忠实度）
> 问题：答案有没有在胡说八道？
> Faithfulness 衡量生成答案是否
> 忠实于检索到的上下文
> 。如果模型在回答中加入了上下文里没有的信息，就是"幻觉"，Faithfulness 就会低。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
