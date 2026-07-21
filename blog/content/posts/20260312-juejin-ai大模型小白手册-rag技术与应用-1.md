---
title: AI大模型小白手册 | RAG技术与应用
date: 2026-03-12 14:57:45+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- RAG
- Python
- 数据库
categories:
- AI 工程
- 数据
scenarios:
- AI/ML项目
- RAG应用
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7616193410694397986
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:40f4e40019c2b74febc1d34a10f158950dfe80d1b297fa51aef527119c5383c4
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 20
captured_at: '2026-07-18T04:19:09.585915Z'
source_capture_sha256: sha256:806a6755dbc3032b70c3d71f1dc46f15fed3e82e1e07fdfafbbdb1ab97a8d38b
source_capture_chars_original: 2854
source_publication_excerpt_chars: 786
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_44f068f9a540fa0b78de3dc08f57a670c6274f32131f6c2616f207bf5f6dc0c5
revision_id: rev_aab26e231fcbd01b4f00d262bc154cf5c66b0602583cc62ca478770c72fe661a
event_id: evt_c60ccdcb34e88a5dfbdec3cadafb2cba427eb9b1fd447ebbb148bb060cbf6521
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-03-12T06:57:45Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7616193410694397986](<https://juejin.cn/post/7616193410694397986>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 前言
> 你有没有遇到过这样的尴尬？
> 问AI：“怎么申请信用卡？”
> 它答：“信用卡是银行发行的支付工具……”
> ——它根本没回答问题！
> 为什么？因为它“记性有限”，训练数据到2023年就停了，而银行新规早改了。
> RAG（检索增强生成）就是解决这个问题的“桥梁”，它让AI能“边查资料边答题”，把知识库变成它的“第二大脑”。
> 大模型系列系列目录（持续更新）：
> AI大模型小白手册｜基础原理篇
> AI大模型小白手册 | API调用的魔法指南
> AI大模型小白手册｜如何像工程师一样写Prompt
> AI大模型小白手册｜Embedding 与向量数据库
> 一、大模型应用开发的三种模式：Prompt、RAG、微调
> 想象一下，你有一个超级聪明但“记性有限”的助手（大模型）。你想让它帮你做事，有三种方式：
> 1.
> Prompt 工程（提示词工程）
> 怎么做
> ：直接告诉它问题，比如“写一篇关于春天的作文”。
> 优点
> ：简单、快速、零成本。
> 缺点
> ：它只能靠“训练时学过的知识”回答。如果你问公司内部制度？它不知道！还会“瞎编”——这叫
> 幻觉（Hallucination）
> 2.
> RAG（检索增强生成）
> 怎么做
> ：先给它一本“参考书”（你的私有文档），它查完再回答。
> 优点
> ：能回答专业、私有、最新问题，
> 不瞎编
> ，成本低。
> 适用场景
> ：企业知识库、客服问答、医疗/法律咨询等。
> 3.
> 微调（Fine-tuning）
> 怎么做
> ：用你的数据重新训练模型的一部分。
> 优点
> ：模型真正“学会”你的领域知识。
> 缺点
> ：贵、慢、需要大量数据和算力。
> 对大多数企业和个人开发者来说，
> RAG 是性价比最高、最实用的选择
> ！
> 二、RAG 是什么？核心原理与流程
> RAG =
> Retrieval-Augmented Generation
> （检索增强生成）
> 简单说：
> 让大模型“边查资料边答题”
> ，就像考试允许带课本！…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
