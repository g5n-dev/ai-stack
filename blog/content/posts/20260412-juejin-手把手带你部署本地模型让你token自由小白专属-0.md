---
title: 手把手带你部署本地模型，让你Token自由（小白专属）
date: 2026-04-12 13:20:21+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- TypeScript
categories: []
scenarios: []
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7627535770001080347
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:0c5e21b6a8ca45fd080eba58415b7b9beea6bbad9e8f95545851e6e4f1c19659
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 27
captured_at: '2026-07-18T04:19:32.648182Z'
source_capture_sha256: sha256:ae1c4d9042ef3aa2cece85725590b8e940e36cd149e122e38e55d9ae8f76a04e
source_capture_chars_original: 1892
source_publication_excerpt_chars: 800
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7627535770001080347](<https://juejin.cn/post/7627535770001080347>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 本教程包括不同显卡配置可以安装哪种大模型的对照表、3步安装本地模型图文教程、本地模型使用进阶示例三大模块
> 本地部署模型在
> 内网开发
> 时，无需外网即可提供代码补全、日志分析等AI能力，避免敏感数据外泄；在
> 出差或网络不稳
> 时（如高铁、偏远现场），可离线运行，保障开发不中断。相比云端API，它规避了合规风险与计费成本，只需一台4GB显存的笔记本就能流畅运行Gemma-4B等小模型，实现“随时随地、安全可控”的智能辅助。
> 在一切开始前，一定要先安装
> QClaw
> 一、Gemma 4 本地安装速查表
> 全系列模型 × 显存对照表
> 显存 \(VRAM\)
> 代表显卡
> Gemma 1
> Gemma 2
> Gemma 3
> Gemma 4
> 2 GB
> 核显 / MX450
> ✅ 2B \(~1.5GB\)
> ✅ 2B \(~1.5GB\)
> ✅ 1B \(~1GB\)
> ✅ E2B \(~1.5GB\)
> 4 GB
> GTX 1650/1660
> ✅ 2B
> ⚠️ 7B\(紧凑\)
> ✅ 2B
> 9B\(勉强\)
> ✅ 1B
> 4B\(~3.5GB\)
> ✅ E2B
> E4B\(~3.5GB\)
> 6 GB
> RTX 2060
> ✅ 2B
> 7B\(~5.5GB\)
> ✅ 2B
> 9B\(~6.5GB\)
> ✅ 4B
> 12B\(紧凑\)
> ✅ E2B
> E4B
> 8 GB
> RTX 3060/4060
> ✅ 全部 Q4
> ✅ 9B\(~6.5GB\)
> ✅ 4B
> 12B\(~8GB\)
> ✅ E4B
> 26B MoE\(紧凑\)
> 12 GB
> RTX 3060 12G
> ✅ 全部 FP16
> ✅ 27B\(Q4\)
> ✅ 12B
> 27B\(紧凑\)
> ✅ 26B MoE
> 31B\(Q4\)
> 16 GB
> RTX 4080
> —
> ✅ 27B\(Q4\)
> ✅ 12B
> 27B\(紧凑\)
> ✅ 26B MoE
> 31B\(Q4\)
> 24 GB
> RTX 3090/4090
> —
> ✅ 27B\(FP16\)
> ✅ 27B\(FP16\)
> ✅ 31B\(FP16\)
> Gemma 4 输…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
