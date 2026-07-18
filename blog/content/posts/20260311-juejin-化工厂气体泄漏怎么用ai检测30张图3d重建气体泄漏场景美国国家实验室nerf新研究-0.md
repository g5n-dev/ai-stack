---
title: 化工厂气体泄漏怎么用AI检测？30张图3D重建气体泄漏场景——美国国家实验室NeRF新研究
date: 2026-03-11 03:01:56+08:00
draft: false
entry_kind: auto
tags:
- 掘金
categories: []
scenarios: []
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7615484384252624911
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:97fddf6364564270dac255112d9d404831c0e49f66872b90fe143b18a11714fa
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 45
captured_at: '2026-07-18T04:18:51.793004Z'
source_capture_sha256: sha256:a77b82ee791ca848c288d8fc3051be03c411ef2312bb4dc59d1e6801d27cce94
source_capture_chars_original: 2879
source_publication_excerpt_chars: 788
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7615484384252624911](<https://juejin.cn/post/7615484384252624911>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 气体泄漏是化工安全的重大隐患，但传统方法只能从单张红外图像逐帧分析。犹他州立大学联合洛斯阿拉莫斯国家实验室，尝试用NeRF把多张红外高光谱图像融合成3D场景，然后从任意新角度检测气体。结果：30张训练图像就能达到AUC 0.821。
> 数据
> ：DIRSIG合成LWIR HSI，128通道（7.8-13.4µm），SF6气体，231张图像
> 核心指标（30张训练图像）
> ：PSNR 39.6dB，气体检测AUC 0.821，检出率55.7%，误报率0.3%
> 一个真实的安全痛点
> 化工厂、炼油厂、天然气管道——这些设施最怕什么？气体泄漏。
> 很多有毒有害气体肉眼看不到、鼻子闻不到，等发现时往往已经酿成事故。怎么在泄漏早期就发现它？
> 目前的主流方法是用
> 长波红外高光谱相机
> 。原理很直观：很多气体在红外波段有独特的"吸收指纹"——特定波长的光穿过气体时会被吸收，形成一个可被检测的光谱特征。通过分析图像中每个像素的光谱，就能判断哪些地方可能有气体。
> 但这个方法有一个根本局限：
> 每次只能从一个角度看一张图。
> 你站在A点拍了一张，能看到气体羽流的正面；但它的侧面长什么样？它在空间中占多大体积？它飘向了哪个方向？——这些问题，一张2D图像回答不了。
> 如果能把从不同角度拍的多张红外图像，融合成一个3D场景，是不是就能从任意角度去理解气体泄漏了？
> 犹他州立大学和洛斯阿拉莫斯国家实验室（美国从事国家安全科研的顶级机构之一）刚发表的一篇论文，做的就是这件事。
> 用NeRF"看见"红外光中的气体
> NeRF（Neural Radiance Fields，神经辐射场）是近年来3D重建领域最热门的技术之一。简单说，它能从一组不同角度的照片中，学习出一个3D场景的隐式表示，然后从任意新角度渲染出逼真的图像。
> 但标准NeRF有两个前提：输入是RGB三通道图像，且场景中的物体对所有颜色都"可见"。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
