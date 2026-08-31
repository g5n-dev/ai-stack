---
title: "DARTS: Decoder-Aware Representation Tuning via Surgery for Model Merging"
date: 2026-09-01T04:08:21+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "cs.LG", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:246fe0316ada56e5fbb8178b5dedfe8c8049a6a241d0ac42bf325725a37cf526"
source_payload_sha256: "sha256:3a0d3313e9a4a292cb225dede03093e362658b313442e46eb4d4a5b636f054c7"
observation_id: obs_0dd17f7127bc523694bd30deee1b9390205bcac6cece57d66ff1f3b47c0510a8
event_id: evt_c0bb7d4aad5edc9e9f42502603f760ababd9ee02dc31cb0a5cad14bf8e2a5028
revision_id: rev_78d0315168160486b3b11f2b379e232e01988ddd2d0805094791955f45e557f1
source_published_at: 2026-08-28T17:22:47Z
first_seen_at: 2026-08-31T20:04:11.284101Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 72
interpretation_sha256: "sha256:b81feb6d1be6ec5b10250ae2703155dcf26f64c48a2a344a8daa0bdc932857af"
description: "该研究针对多任务大模型合并后出现的表示偏移问题，提出一种针对解码器模型的校准技术 DARTS。它通过在每个 token 位置引入可学习的加性偏置，并依据位置的熵值加权 L1 损失，实现对高决策关键位置的更强烈纠正。"
external_url: http://arxiv.org/abs/2608.28547v1
parent_observation_id: null
last_seen_at: 2026-08-31T20:04:11.284101Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.28547v1](http://arxiv.org/abs/2608.28547v1)
- **发布域名**: arxiv.org
- **分类**: cs.LG
- **作者**: Aaryan Ajay Sharma、Sai Nishanth Padala、Seganrasan Subramanian

## 要点解读

### 这是什么
该研究针对多任务大模型合并后出现的表示偏移问题，提出一种针对解码器模型的校准技术 DARTS。它通过在每个 token 位置引入可学习的加性偏置，并依据位置的熵值加权 L1 损失，实现对高决策关键位置的更强烈纠正。

### 用在哪里
适用于在无额外训练的情况下将多个针对不同任务的微调语言模型合并为统一模型的场景，尤其在需要保持代码生成、数学推理、指令跟随等多种能力的应用中。模型的参数量增加极小，适合资源受限的部署环境。

### 可以推断的
推测：该方法通过位置感知的校正，能够在不显著增加参数的情况下提升合并模型在关键生成步骤的质量。  
推测：由于强调高熵位置的误差修正，对于生成结果对局部决策高度依赖的任务，提升可能更为明显。

## 来源摘要/节选

> Model merging combines multiple task-specific fine-tuned LLMs into a single multi-task model without additional training. However, merged models are known to suffer from representation bias: systematic drift between the merged model's hidden states and those of each individual source model. Prior work (Yang et al., 2024a) study and mitigate this bias for encoder-based vision models using a lightweight correction module trained with L1 loss. However, such bias is not studied for decoder models due to their autoregressive nature. We analyze the problem of representation bias in decoder models, and show two challenges absent in encoders: (1) the causal attention mask causes bias to accumulate across token positions, requiring position-dependent correction; and (2) not all token positions are equally important, i.e., high-entropy (decision-critical) positions matter far more than low-entropy ones. To address these challenges, we propose Decoder-Aware Representation Tuning via Surgery (DARTS). DARTS employs a novel entropy-weighted L1 loss to upweight correction at high-entropy positions where errors most affect generation quality, and a per-position additive bias that captures position-dependent error without overparameterization. We perform extensive evaluation on three domains: code generation (HumanEval), mathematical reasoning (GSM8K), and instruction following (AlpacaEval) on Llama-2-7B models, and show DARTS achieves significant improvement over the standard surgery approach while adding negligible parameters ($0.1\%$ of total parameters).

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。