---
title: "Diffusion LLMs as Targets and Adversaries: Mechanistic Safety Exploits"
date: 2026-08-11T06:00:12+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "生成式 AI", "Prompt 工程", "cs.LG", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:f45e45491d837b7fd6d19c773c7a5e2a072b474a5e8af295e218d047465bf316"
source_payload_sha256: "sha256:3293a4501f309390e22364fbdb6b5abe98f9a38e79604872a95fb41854a73084"
observation_id: obs_98e96cb8f162f963c62780272afb908451b048d21789b5c467f2f13e28bf0c6d
event_id: evt_35fd0c5f8223e3dd50d2061ce14486a0d679225c236ededc87c14315af07a01f
revision_id: rev_85d9a82fd3e20f8ccffdcfae7c71dfef78c596fe2d9a5c0380908f0d7f54aa5e
source_published_at: 2026-08-07T17:17:18Z
first_seen_at: 2026-08-10T21:57:59.773501Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 70
interpretation_sha256: "sha256:73e9aa2f2196882bcd7c3b21514a9a072872ed1df4871a73d86783d739f5024c"
description: "该研究把扩散式大型语言模型既当作攻击目标，又当作攻击者，探索其在安全对齐过程中的结构脆弱性，并提出一种仅依赖噪声空间引导的黑盒越狱框架。"
external_url: http://arxiv.org/abs/2608.07430v1
parent_observation_id: null
last_seen_at: 2026-08-10T21:57:59.773501Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.07430v1](http://arxiv.org/abs/2608.07430v1)
- **发布域名**: arxiv.org
- **分类**: cs.LG
- **作者**: Elena Dumitrescu、Gert Lek、Lydia Y. Chen 等

## 要点解读

### 这是什么
该研究把扩散式大型语言模型既当作攻击目标，又当作攻击者，探索其在安全对齐过程中的结构脆弱性，并提出一种仅依赖噪声空间引导的黑盒越狱框架。

### 用在哪里
适用于安全研究者评估扩散语言模型的安全性，以及模型开发者检测和加固安全机制时参考。

### 可以推断的
推测：扩散模型在并行去噪阶段引入的噪声分布可能为规避安全约束提供可操作的搜索空间。  
推测：公开此类结构漏洞后，模型提供方可能加快对安全神经元的审查和剪枝，以提升对齐鲁棒性。

## 来源摘要/节选

> Diffusion Large Language Models (DLLMs) replace autoregressive next-token prediction with iterative parallel denoising, yet their internal safety mechanisms remain poorly understood. In this work, we investigate DLLMs both as targets and as adversaries, exposing mechanistic vulnerabilities in diffusion-based alignment.
> We first show that safety alignment in DLLMs remains sparse and transferable across architectures. DLLMs initialized from autoregressive predecessors inherit the same mechanistic safety footprint as their source models, enabling transfer attacks via direct safety neuron mapping and pruning. Self-pruning increases attack success rates (ASR) from 2.6% to 73.8% on LLaDA and from 1.9% to 86.6% on Dream, while transfer pruning from Qwen2.5 increases ASR from 1.9% to 73.2% on Dream and from 7.0% to 86.3% on Fast-dLLM.
> Building on these findings, we introduce SN-Guided Diffusion, a fully offline black-box jailbreak framework that steers the diffusion process away from safety-triggering regions using a weighted safety neuron loss, which achieves near-perfect prompt separability (AUROC = 1.0 for benign-vs-jailbreak discrimination). Across multiple open and proprietary targets, our method achieves a transfer ASR of up to 77.1% on Llama-3-8B-Instruct, 86.9% on Qwen2.5-7B-Instruct, and 74.3% against Gemini-2.5-Flash-Lite, while requiring only 20 generation episodes per prompt. Compared to prior jailbreaking frameworks, our method achieves competitive transferability with orders-of-magnitude lower generation cost.
> Our codebase is available at https://github.com/ellyoana/sn-guided-diffusion.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。