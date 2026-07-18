---
title: 大模型行为塑造：SFT 与 LoRA 深度解析
date: 2026-02-15 12:10:18+08:00
draft: false
entry_kind: auto
tags:
- 掘金
categories: []
scenarios: []
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7606183276774129727
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:06bde4d2250058ad2f253e009f591e699d4aa20c76ff6847d682d0561fe26fe0
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 23
captured_at: '2026-07-18T04:17:20.050125Z'
source_capture_sha256: sha256:592c7277045c90757c60fdc78985cd43dedc0698113066ee4208222f34693676
source_capture_chars_original: 2237
source_publication_excerpt_chars: 799
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7606183276774129727](<https://juejin.cn/post/7606183276774129727>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 如果说\*\*预训练（Pre-train）\*\*是让模型在图书馆里读万卷书，那么
> SFT（有监督微调）
> 就是教模型如何通过考试、如何与人沟通，而
> LoRA
> 则是完成这一过程最经济高效的“手术刀”。
> 一、 SFT \(Supervised Fine-Tuning\)：从“接龙”到“对话”
> 1.1 核心定义
> SFT 是在
> 高质量、人工编写
> 的指令数据集上，对基座模型（Base Model）进行的微调。
> 输入模式
> ：
> Instruction \(指令\) + Input \(上下文\) -&gt; Output \(标准答案\)
> 目标
> ：修正模型的输出行为，使其从“无目的的文本补全”转变为“遵循指令的对话助手”。
> 1.2 训练逻辑：Teacher Forcing
> SFT 的训练流程与预训练相似，但在工程实现上有两个关键差异点：
> 精准目标
> ：通过最小化模型输出与标准答案之间的
> 交叉熵损失
> 。
> 损失掩码 \(Loss Masking\)
> ：仅针对 Answer 部分计算梯度，不对 Prompt 部分算 Loss。
> 二、 LoRA \(Low-Rank Adaptation\)：参数的“补丁”艺术
> 2.1 核心原理
> LoRA 认为模型在微调时的参数变化具有“低秩性”。它不在原始矩阵
> W
> W
> W
> 上动刀，而是在旁边并联两个小矩阵
> A
> A
> A
> 和
> B
> B
> B
> ：
> 计算公式
> ：
> O
> u
> t
> p
> u
> t
> =
> \(
> W
> f
> r
> o
> z
> e
> n
> ×
> x
> \)
> +
> \(
> B
> ×
> A
> ×
> x
> \)
> ⋅
> α
> r
> Output = \(W\_\{frozen\} \\times x\) + \(B \\times A \\times x\) \\cdot \\frac\{\\alpha\}\{r\}
> O
> u
> tp
> u
> t
> =
> \(
> W
> f
> roze
> n
> ​
> ×
> x
> \)
> +
> \(
> B
> ×
> A
> ×
> x
> \)
> ⋅
> r
> α
> ​
> 矩阵 A \(降维\)
> ：将高维信号压缩到极小的维度
> r
> r
> r
> 。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
