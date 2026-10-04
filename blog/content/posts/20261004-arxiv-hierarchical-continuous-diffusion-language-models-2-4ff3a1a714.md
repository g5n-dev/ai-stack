---
title: "Hierarchical Continuous Diffusion Language Models"
date: 2026-10-04T03:59:29+08:00
draft: false
entry_kind: "auto"
tags: ["生成式 AI", "cs.CL", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:b121992b9e206b44e7f2f4a60c50a1f48a299091ce8b5f2d0ca77469f31a3a21"
source_payload_sha256: "sha256:a93daca79ba3fd307b2fa95b9a7d7eec69d312326790d48161a69fcc88b53768"
observation_id: obs_4ff3a1a7148d7bc20958e8f62dd251b0fd6ff123b75624063f07cba760c50fab
event_id: evt_b267f2fe50f2009eefe15e29c49ee78650868b711d975b66381e4ab9f567631f
revision_id: rev_2d1577039604502cdfffc650bd13703bffa565952ce9512363c957624f72b607
source_published_at: 2026-10-01T17:59:39Z
first_seen_at: 2026-10-03T20:11:20Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 49
interpretation_sha256: "sha256:b59f11fd8a5cb18c8e24564ade6bb02a11d884eb99169b83f85f284aee26055b"
description: "该工作提出一种层次化连续扩散语言模型，通过在单一去噪过程中耦合离散 token 生成与连续潜在轨迹，使每个 token 的生成都受到全局潜在状态的约束。"
external_url: http://arxiv.org/abs/2610.02193v1
parent_observation_id: null
last_seen_at: 2026-10-04T00:00:00Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2610.02193v1](http://arxiv.org/abs/2610.02193v1)
- **发布域名**: arxiv.org
- **分类**: cs.CL
- **作者**: Hui Ren、Zihan Li、Chang Liu 等

## 要点解读

### 这是什么
该工作提出一种层次化连续扩散语言模型，通过在单一去噪过程中耦合离散 token 生成与连续潜在轨迹，使每个 token 的生成都受到全局潜在状态的约束。

### 用在哪里
适用于需要在生成时满足全局约束的任务，如结构化推理（Sudoku）、数学规划（Countdown）以及一般语言建模（LM1B）。

### 可以推断的
推测：在需要严格约束的生成场景（如逻辑推理或代码生成）中，该方法可能比仅使用离散或连续扩散的模型更具优势。  
推测：由于每一步都要从潜在状态读取 token 并反馈，模型的训练与推理开销可能会高于仅使用单一扩散机制的方案。

## 来源摘要/节选

> Discrete diffusion language models offer a compelling alternative to autoregressive generation for tasks demanding bidirectional reasoning and global constraint satisfaction. Yet they share a structural bottleneck: when decoding in parallel, each token is sampled independently from its marginal, severing the statistical dependencies among the tokens decoded together. Continuous diffusion language models avoid this by denoising a shared continuous state, but their denoiser sees only that state, so nothing ties it to a valid token configuration until it is finally decoded. To address this, we propose Hierarchical Continuous Diffusion Language Models (HC-DLM), which couple discrete token generation with a continuous latent trajectory in a single, principled denoising process, whose training objective is derived from a variational bound on the token likelihood. In contrast to recent methods that attach continuous context to a self-contained discrete chain, HC-DLM makes the latent the only persistent generative state: tokens are read out from it at every step and feed back as a scaffold for the next latent update. On structured reasoning (Sudoku), mathematical planning (Countdown) and language modeling (LM1B), HC-DLM improves over discrete and continuous diffusion baselines at matched model size, in puzzle accuracy on Sudoku and Countdown and in generative perplexity on LM1B. Project page: https://hc-dlm.github.io/.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。