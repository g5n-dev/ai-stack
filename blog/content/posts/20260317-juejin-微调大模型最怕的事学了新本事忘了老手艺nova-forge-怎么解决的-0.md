---
title: 微调大模型最怕的事：学了新本事，忘了老手艺。Nova Forge 怎么解决的
date: 2026-03-17 01:17:58+08:00
draft: false
entry_kind: auto
tags:
- 掘金
categories: []
scenarios: []
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7617728986828947483
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:87b7133df354038392410e573e532373b3f671bdfab32a04ed77dac32785236b
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 38
captured_at: '2026-07-18T04:19:22.457104Z'
source_capture_sha256: sha256:957cd6a86f58a0304242157b097d00ee99b95bbe072efbe91dc27d9ca81da6e4
source_capture_chars_original: 1487
source_publication_excerpt_chars: 495
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7617728986828947483](<https://juejin.cn/post/7617728986828947483>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 做过 SFT 的人都有体会：微调前模型啥都会一点，微调后某个领域变强了，但写文章、做推理、聊天的能力明显变菜了。
> 这叫灾难性遗忘。学了新东西，把老东西覆盖了。
> 最近用 Amazon Nova Forge 试了一下它的数据混合方案，效果不错——
> 领域分类准确率上去了，MMLU 分数几乎没掉
> 。
> 任务背景
> 客户评论分类，1420 个细分类别，四级标签体系，14000+ 训练样本。典型的企业级分类任务。
> 基础模型 zero-shot 不够准（类别太细），普通 SFT 之后分类好了但通用能力废了。
> Nova Forge 做了什么
> 核心思路：
> 微调时不只用你的领域数据，自动混入 Nova 的精选通用数据
> 。
> 你提供领域训练集，Nova Forge 自动：
> 从 Nova 训练语料中选互补子集
> 动态调整混合比例
> 联合优化领域损失和通用损失
> 不需要你手动找通用数据、试混合比例。
> 效果
> 指标
> 基础模型
> 普通SFT
> Nova Forge
> VOC分类
> 低
> 高
> 高
> MMLU通用
> 正常
> 明显下降
> 基本持平
> 关键：
> 领域能力和通用能力不再是二选一
> 。
> 代码长什么样
> import
> boto3, json…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
