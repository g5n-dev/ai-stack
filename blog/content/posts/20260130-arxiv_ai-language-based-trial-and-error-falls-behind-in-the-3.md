---
title: Language-based Trial and Error Falls Behind in the Era of Experience
date: 2026-01-30 03:54:32+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
- AI Agent
- 大语言模型
categories:
- 论文
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2601.21754v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:7d4195ed2fe48128935acb74a59f63209139edf6600aa1580e8d46c0ba282794
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 68
captured_at: '2026-07-18T04:09:52.752345Z'
source_capture_sha256: sha256:5e54f620aecc78f0b0e3b67d32ba4ae8a21ed0e8384bdf1e0dda97c6853c01c3
source_capture_chars_original: 1242
source_publication_excerpt_chars: 1242
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2601.21754v1](<https://arxiv.org/abs/2601.21754v1>)
- **作者**: Haoyu Wang, Guozheng Ma, Shugang Cui, Yilun Kong, Haotian Luo, Li Shen, Mengya Gao, Yichao Wu, Xiaogang Wang, Dacheng Tao
- **分类**: cs.AI
- **论文时间**: 2026-01-29T14:08:41Z
- **论文 PDF**: [https://arxiv.org/pdf/2601.21754v1.pdf](<https://arxiv.org/pdf/2601.21754v1.pdf>)

## 来源摘要/节选

> While Large Language Models \(LLMs\) excel in language-based agentic tasks, their applicability to unseen, nonlinguistic environments \(e.g., symbolic or spatial tasks\) remains limited. Previous work attributes this performance gap to the mismatch between the pretraining distribution and the testing distribution. In this work, we demonstrate the primary bottleneck is the prohibitive cost of exploration: mastering these tasks requires extensive trial-and-error, which is computationally unsustainable for parameter-heavy LLMs operating in a high dimensional semantic space. To address this, we propose SCOUT \(Sub-Scale Collaboration On Unseen Tasks\), a novel framework that decouples exploration from exploitation. We employ lightweight "scouts" \(e.g., small MLPs\) to probe environmental dynamics at a speed and scale far exceeding LLMs. The collected trajectories are utilized to bootstrap the LLM via Supervised Fine-Tuning \(SFT\), followed by multi-turn Reinforcement Learning \(RL\) to activate its latent world knowledge. Empirically, SCOUT enables a Qwen2.5-3B-Instruct model to achieve an average score of 0.86, significantly outperforming proprietary models, including Gemini-2.5-Pro \(0.60\), while saving about 60% GPU hours consumption.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
