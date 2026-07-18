---
title: 使用 PyTorch 进行模型训练train
date: 2026-03-15 11:28:03+08:00
draft: false
entry_kind: auto
tags:
- 掘金
categories: []
scenarios: []
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7616818675262652450
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:46632c08f450566517a915fdf20d0f679f6b22924e3b410e939cc42a62662b83
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 22
captured_at: '2026-07-18T04:19:16.445512Z'
source_capture_sha256: sha256:17c963fb00f37ab7738810729f79e1505d3635f44c3fda3d0b9af409b2321161
source_capture_chars_original: 6000
source_publication_excerpt_chars: 625
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7616818675262652450](<https://juejin.cn/post/7616818675262652450>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 使用 PyTorch 进行模型训练
> 你可以观看下方视频或 YouTube 上的对应内容跟随学习。
> 引言
> 在之前的视频中，我们已经讨论并演示了：
> 使用
> torch.nn
> 模块的神经网络层和函数构建模型
> 自动梯度计算的原理（这是基于梯度的模型训练的核心）
> 使用 TensorBoard 可视化训练进度和其他过程
> 在本视频中，我们将为你新增一些实用工具：
> 熟悉
> Dataset
> 和
> DataLoader
> 抽象类，以及它们如何简化训练循环中的数据喂入流程
> 讲解特定的损失函数及其适用场景
> 学习 PyTorch 优化器（Optimizer）—— 它们能根据损失函数的计算结果调整模型权重
> 最后，将所有这些组件整合，完整演示 PyTorch 训练循环的运行过程
> Dataset 和 DataLoader
> Dataset
> 和
> DataLoader
> 类封装了从存储介质读取数据，并以批次形式提供给训练循环的全过程：
> Dataset
> 负责读取和处理
> 单个数据样本
> DataLoader
> 从
> Dataset
> 中抽取样本（自动抽取或通过自定义采样器）、组合成批次，并返回给训练循环使用。
> DataLoader
> 适用于所有类型的数据集，与数据类型无关
> 本教程中，我们将使用 TorchVision 提供的 Fashion-MNIST 数据集。通过
> torchvision.transforms.Normalize\(\)
> 实现图像数据的零均值化和归一化，并下载训练集和验证集。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
