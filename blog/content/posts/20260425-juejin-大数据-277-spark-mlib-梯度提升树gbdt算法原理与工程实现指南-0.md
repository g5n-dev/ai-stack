---
title: 大数据-277 Spark MLib-梯度提升树（GBDT）算法原理与工程实现指南
date: 2026-04-25 03:02:05+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- 深度学习
categories:
- AI 工程
scenarios:
- AI/ML项目
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7632183161372164122
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:47339668ced68d755abd4bbe06b3162e56aca6fcd8bc9b18ab39868623029f42
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 41
captured_at: '2026-07-18T04:19:41.505914Z'
source_capture_sha256: sha256:0059857e08e076acde95b1420930b2cfbe2f141cb22d2baef8f90de4327750d4
source_capture_chars_original: 2754
source_publication_excerpt_chars: 685
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_04010e74878eb7165685c3e17bef96628755f5f08991289394f2210787b0cb2d
revision_id: rev_00c630e4ea16949298c2eec719b8c455aac81dee622de5f8a85416ccbdad0242
event_id: evt_084b72ffdeee1dd3ff37bc26b4e359ef1680544746a91e9a19eec0d38591de5c
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-04-24T19:02:05Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7632183161372164122](<https://juejin.cn/post/7632183161372164122>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> TL;DR
> 场景
> ：结构化表格数据的分类与回归问题，需要捕捉特征间复杂非线性关系
> 结论
> ：GBDT通过梯度下降逐步拟合残差，将多棵弱决策树累加为强学习器，是Kaggle等竞赛的常胜方案
> 产出
> ：掌握GBDT核心思想、XGBoost/LightGBM/CatBoost实现差异，能快速选择合适框架
> 版本矩阵
> 框架
> 版本
> 发布时间
> 核心特性
> XGBoost
> 2.0+
> 2023
> 二阶近似、稀疏感知、Block直方图、L1/L2正则
> LightGBM
> 4.0+
> 2023
> GOSS行采样、EFB特征捆绑、叶子优先生长
> CatBoost
> 5.0+
> 2024
> 有序目标编码、对称树、文本特征支持
> Gradient Boosting
> 梯度提升树（Gradient Boosting）是提升树（Boosting Tree）的一种改进算法，所以在讲梯度提升树之前先来说一下提升树。
> 先来例子理解：假如有个人30岁，我们首先用20岁去拟合，发现损失有10岁，这时我们用6岁去拟合剩下的损失，发现差距还有4岁，第三轮我们用3岁拟合剩下的差距，差距就只有一岁了。
> 如果我们迭代轮数还没有完，可以继续迭代下面，每一轮迭代，拟合的岁数误差都会减小，最后将每次拟合的岁数加起来便是模型输出的结果
> 提升树算法：
> 初始化 f0（x）= 0
> 对 m = 1,2...M，计算残差 rmi = yi - fm - 1\(x\) , i = 1,2...N
> 拟合残差 rmi 学习一个回归树，得到 hm\(x\)
> 更新 fx\(m\) = fm - 1 + hm\(x\)
> 得到回归问题提升树：
> 上面伪代码中的残差是什么？…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
