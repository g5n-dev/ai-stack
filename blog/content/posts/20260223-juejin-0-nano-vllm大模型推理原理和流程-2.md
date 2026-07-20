---
title: nano-vllm(1)：大模型推理原理和流程
date: 2026-02-23 15:36:57+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- 大语言模型
- Python
categories:
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7609925885416767497
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:618e5a92db7e514f1c01aba8237d7a7bd856bdabf0d64cadf1705210b273874c
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 23
captured_at: '2026-07-18T04:17:35.532546Z'
source_capture_sha256: sha256:f35a510ec681d7f3c46aff274799f3e290aeac0518531cff0f219317d716c33f
source_capture_chars_original: 6000
source_publication_excerpt_chars: 775
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_dcd3cf4ccfcae34dd167d29337619f9c63a6df0bc5f2a3e4103f7e7c25311318
revision_id: rev_38e07cc623c151d64254627e47a0053590688f02ad33261058263f94e882befa
event_id: evt_b2bc5ed6ca8c0e2e4697220bfd760dc9545a7892eac46b96902072bdd89cdc71
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-23T07:36:57Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7609925885416767497](<https://juejin.cn/post/7609925885416767497>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 0. 简介
> LLM：就是大语言模型，指参数量较大且具有较强生成能力的语言模型。
> vLLM：功能完备的生产级大语言模型推理引擎。
> nano-vllm：是vLLM的极简教学版实现，代码只有1200行左右。
> 作为算法和infra小白，希望通过nano-vllm的学习，学习了解大模型infra的相关知识。
> 1. 大模型推理过程
> 大语言模型的推理过程基本如上所示，大致分为四个阶段：
> 输入阶段：
> 用户输入一段文本，系统将这段文字分解为Token，每个Token可以映射到一个整数ID，一串Token就变成了模型可以处理的整数ID序列。
> 预填充阶段：
> 对整段输入做第一次完整的计算，生成首个输出Token。经过embedding，位置编码，attention，MLP，softmax等layer的处理，得到最终模型输出的logits。这个logits就是个概率分布，一般而言选取概率最大的预测token，当然这和设置的temperature有关。
> 自回归解码阶段：
> 每一次推理过程都是选取下一个token，然后拼接到已有序列的组成新的序列，作为下一次推理的输入，直到达到最大token限制或者生成特殊的 &lt;eos&gt; 结束符号。
> 输出阶段：
> 将模型输出的token ID转换为文字，返回给用户。当然，可以在第3步的解码阶段，每生成一个Token就进行一次
> 输出阶段
> ，以实现流式输出的效果，让用户可以直观感受模型的推理进展。
> 1.1 相关耗时指标
> 1.1.1 TTFT \(Time To First Token\)
> TTFT其实就是
> 大模型说话前的思考时间
> 。模型进行
> 一次完整的、并行的前向传播
> 。它需要为提示词中的
> 每一个token
> 计算其隐藏状态，并尤其关键的是，需要为
> 每一个token
> 计算并缓存其Key和Value向量，即初始化
> KV Cache
> 。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
