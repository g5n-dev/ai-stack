---
title: 大模型 ai coding 比较
date: 2026-02-19 09:39:31+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- 大语言模型
- Java
categories:
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7607105207069065242
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:d9988c9d00930035252ac788d462cd23bbeb626131685b1221b5f942174aa535
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 16
captured_at: '2026-07-18T04:17:28.920355Z'
source_capture_sha256: sha256:1b920b461f94ae12fdec89703c81b8e3f6788d272faa147b5c4662eed9b3d83f
source_capture_chars_original: 6000
source_publication_excerpt_chars: 799
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7607105207069065242](<https://juejin.cn/post/7607105207069065242>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 序
> 我主要用途是 ai coding，从各种渠道获取到了很多 不同的大模型排序
> 最多的是 opus 4.6 &gt; k2.5 &gt; glm5 &gt; sonnet4.5 &gt; m2.5
> 但是我 希望从自身实践的角度 进行测试，我把所有的平台都办了月卡
> 我在这个基础上 添加了deepseek v3
> 结论
> 确实opus 4.6 更适合 ai coding
> glm5 可能是真的因为 资源不够，感觉降智，速度也慢，前两天 他们 发通知，寻求资源，目前可能不推荐
> 调研
> 我从
> 📊 评审维度明细：
> 1. 代码生成能力（权重40%）
> 测试目标 ：模型独立完成指定功能代码的能力
> 测评数据集：HumanEval 经典编程题（抽样10题）
> 核心指标： Pass@1 （一次生成代码直接通过所有测试用例的比例）
> 评分逻辑：题目完全通过得10分，失败得0分
> 实测结果：DeepSeek 10/10（100%通过），Kimi 2/10（20%通过）
> 2. Debug修复能力（权重35%）
> 测试目标 ：模型排查和修复代码问题的能力
> 测评数据集：DebugBench 真实bug场景（抽样9题）
> 覆盖Bug类型：语法错误、逻辑错误、性能优化三类
> 核心指标：Bug修复通过率
> 评分逻辑：成功修复得10分，修复失败/引入新问题得0分
> 实测结果：DeepSeek 9/9（100%通过），Kimi 7/9（77.8%通过）
> 3. 代码重构/项目理解能力（权重25%）
> 测试目标 ：模型对复杂项目的理解和工程化能力
> 测评题目：手工设计的企业级真实场景（10题）
> 覆盖题型：
> 读懂代码意图
> 函数拆分重构
> 接口改造升级
> 单元测试生成
> 跨文件依赖问题排查
> 评分维度：每道题从\*\*正确性\(40%\)、可读性\(30%\)、完整性\(30%\)\*\*三个角度综合打分（满分10分）
> 实测结果：DeepSeek 平均9.2/10，Kimi 平均9.0/10
> 4.…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
