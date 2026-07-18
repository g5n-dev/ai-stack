---
title: 大模型根本不是“学会了”，它只是会“看例子”：一文讲透 In-context Learning（ICL）
date: 2026-04-20 15:16:13+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- 机器学习
- 自然语言处理
categories:
- AI 工程
scenarios:
- AI/ML项目
- 自然语言处理
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7630730075692449855
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:e71bde138201eb00eb3763dfb29e0b0b34471929015f1c200c9f1d28b4de0754
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 52
captured_at: '2026-07-18T04:19:37.684260Z'
source_capture_sha256: sha256:7925a4811f66de88a2e0e5fe8d16586468187c698c5742f04a48c8eeeb69c12e
source_capture_chars_original: 4156
source_publication_excerpt_chars: 766
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7630730075692449855](<https://juejin.cn/post/7630730075692449855>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 大家好，我是舒一笑不秃头，喜欢分享和写作，
> 更多精彩内容
> ～
> 大家第一次接触大模型时，往往会有一种错觉：
> “这模型怎么这么聪明？我给它举两个例子，它居然就会做了。”
> 比如你对模型说：
> 北京 -&gt; China
> 东京 -&gt; Japan
> 巴黎 -&gt; ?
> 它立刻回答：
> France
> 很多人会觉得：
> 哇，它是不是刚刚被我‘训练’了？
> 其实不是。
> 这背后对应的是大模型里一个非常重要的能力：
> In-context Learning，简称 ICL
> 。
> 翻译成中文，就是：
> 上下文学习
> 。
> 今天这篇文章，我尽量不用论文腔，带你真正搞懂：
> ICL 到底是什么
> 它和传统训练有什么区别
> 为什么 few-shot prompt 这么有效
> 为什么说它是大模型时代最重要的能力之一
> 一、什么是 ICL？一句话先讲明白
> ICL 的核心思想非常简单：
> 不给模型重新训练，只在输入里放几个示例，模型就能“照着例子”完成新任务。
> 注意这句话里最关键的两个点：
> 不重新训练
> 只靠上下文中的示例
> 也就是说，模型不是通过梯度下降学会任务的，
> 而是通过你给它的例子，
> 临时理解当前任务该怎么做
> 。
> 你可以把它理解成一种：
> “现场看题、现场悟规则”的能力。
> 二、很多人真正没懂的点：ICL 不是训练
> 这是初学者最容易混淆的地方。
> 我们平时说“机器学习”，默认是这种流程：
> 准备大量数据
> 标注数据
> 训练模型
> 更新参数
> 模型学会任务
> 比如你想让模型做“情感分类”，传统做法就是喂给它几万条：
> “这个产品太好用了” -&gt; 正面
> “物流慢得离谱” -&gt; 负面
> 训练很多轮以后，它参数变了，能力也变了。
> 这叫
> 监督学习/微调
> 。
> 但 ICL 完全不是这样。
> 在 ICL 里，你只是把示例写进 prompt：
> 句子：这个电影太无聊了
> 情感：负面
>
> 句子：这家餐厅真的很不错
> 情感：正面…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
