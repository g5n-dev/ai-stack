---
title: 大模型“全家桶”：除了Transformer，还有这些“配料”值得品！
date: 2026-03-12 11:11:52+08:00
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
external_url: https://juejin.cn/post/7615972610167980078
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:a98fea57ccaa122c34fce430f5286ad1f8965db6efcbc53a48474872ae5b814d
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 35
captured_at: '2026-07-18T04:19:10.322247Z'
source_capture_sha256: sha256:f0332b1d82d9d3ca952eadd3413638da8a9b1fb05ba11bdad8e9d3771232df8a
source_capture_chars_original: 5025
source_publication_excerpt_chars: 741
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7615972610167980078](<https://juejin.cn/post/7615972610167980078>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 大模型“全家桶”：除了Transformer，还有这些“配料”值得品！
> 如果把大模型比作一道顶级料理，Transformer是主厨，但光有主厨可做不出满汉全席！今天带你看看LLaMA的“厨房秘笈”——那些让大模型更香、更高效、更聪明的“秘密配料”。
> 一、位置编码：给词语发“座位号”
> 1.1 为什么需要位置编码？
> 想象一下：Transformer是个“社交牛逼症”，能同时跟所有人聊天
> 但有个问题：它是个“脸盲”，分不清谁先来谁后到
> “猫追老鼠”和“老鼠追猫”对它来说是一样的！
> 1.2 LLaMA的绝招：RoPE（旋转位置编码）
> # 传统位置编码：给每个位置贴标签
> # 问题：标签是固定的，模型学不到相对位置
> # RoPE的魔法：让词向量“旋转”起来
> class
> 旋转座位表
> :
> def
> 安排座位
> \(
> self, 词语, 位置
> \):
> # 不是简单加个数字，而是让向量“转个角度”
> # 位置1：转30度
> # 位置2：转60度
> # 位置3：转90度
> # 这样模型就知道：“哦，你是第3个来的！”
> # 更妙的是：相对位置也能知道！
> # “猫”在位置1（30度），“老鼠”在位置3（90度）
> # 角度差60度 → 距离2个位置
> return
> 旋转后的向量
> # 效果：不管句子多长，都能准确定位
> # 就像GPS：不仅知道你在哪，还知道你和别人的距离
> 实际效果
> ：
> 输入：“我爱北京天安门”
> 传统方法：知道每个词的位置，但不知道“北京”和“天安门”挨着
> RoPE：知道“北京”和“天安门”是邻居，关系密切
> 二、归一化技术：给模型“减肥瘦身”
> 2.1 LayerNorm的“体重秤”
> 传统LayerNorm：每次都要计算均值和方差
> 就像每天称体重：要脱鞋、脱外套、空腹...
> 计算量大，还慢！…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
