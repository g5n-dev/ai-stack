---
title: AI 视觉连载3：RGB与通道
date: 2026-02-11 20:41:49+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- 深度学习
- 计算机视觉
categories:
- AI 工程
scenarios:
- AI/ML项目
- 计算机视觉
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7605206033267540003
aliases:
- /posts/20260212-juejin-ai-视觉连载3rgb与通道-0/
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:68a12684e0cc0fe42f9b84dd4f704c364573a0691e16a18815ea9c7146cfc777
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 15
captured_at: '2026-07-18T04:17:11.685116Z'
source_capture_sha256: sha256:614f68d4d2e77b511a0c3590c478d28138ed5bac947b45786b60a209e8a7d644
source_capture_chars_original: 1957
source_publication_excerpt_chars: 766
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_df42e7944d9916ca9cc9be5dc3aa9f8571151e8122dfcea25a63dd5dcb40360a
revision_id: rev_baf02b870790166bcc1d8174a25c8a397bff1f3ab09c62d1b070d4534bc3bdf1
event_id: evt_ba80468cb2294f6244f1cde799abe0c367b7788b9ce21bfcc756dca971f85fcd
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-11T12:41:49Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7605206033267540003](<https://juejin.cn/post/7605206033267540003>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 在
> 2、灰度与色彩
> 的最后，给出了一个由彩色图片转成灰度图的示例，并且通过
> color\_image.mode
> 获取了图片的格式：彩色图片获取到的格式为 RGBA，灰度图为 L。
> 这一节再介绍一下 RGB 图片以及通道的概念。
> 通道这个概念，在
> 深度学习
> 中很重要，并且极为重要。
> 举个例子——
> 在很多时候，对AI神经网络中的一些算法做工程化实现，或者做性能优化，除了关注算法本身之外，还会关注数据存储格式。
> 一般在 pytorch 中（一个AI模型框架），数据的存储格式 NCHW, C指代的就是通道\(channel\)， 如此一来，对于需要在通道维度做归一化（如 reduce）的算法，是很不友好的。
> 因为数据在通道维度不连续，导致取到完整的通道维度信息要跨越很大的地址范围，CPU 或其他 xPU 对于这类的数据寻址性能都是很差的，至少要比连续寻址差。
> 此时就需要对通道维度做其他的变换。
> 以上举了在实际 AI 算法开发中会遇到的一类问题：通道维度数据在存储器中摆放不连续导致某些算法运算性能不好，这里暂时了解即可，无需深究，涉及到的内容会在专栏后面有详述。
> 本节的目的只有一个：只需要了解通道这个概念是什么就行了。
> 先看下 RGB 图像
> 你可能知道，色彩通常由红色（Red，R）、绿色（Green, G）、蓝色（Blue, B）三种基本颜色组成，这种颜色表示方式被称为彩色 RGB 模型。
> 在这个模型中，每个像素的颜色由这三种基本颜色组合而成。
> 因此，一个图像在二维平面上看似只有一个像素，实际是由三个不同颜色（不同通道）的像素混合组成。
> 这里的 R/G/B 三种颜色，就认为是彩色图片的三个通道，如下图所示。
> （一张彩色RGB图片按照通道维度（C）堆叠）
> 来调一下颜色
> 通过调整红、绿、蓝三个通道的值，你可以混合出各种颜色。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
