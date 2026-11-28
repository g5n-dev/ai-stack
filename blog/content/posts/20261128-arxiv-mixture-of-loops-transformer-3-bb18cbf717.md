---
title: "Mixture-of-Loops Transformer"
date: 2026-11-28T18:24:56+08:00
draft: false
entry_kind: "auto"
tags: ["AI", "cs.LG", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:55e3a98c6576bcd1ff746d4b94e838a8fdb3dca7c46c284256a41a071cb1e473"
source_payload_sha256: "sha256:33fce63b4814ee01c1fb70d28bc639713dfd118452601c95b9b035f94160b792"
observation_id: obs_bb18cbf717771ba45551aa076885ee39cc9a1b8d500cc976a3b44ead01439638
event_id: evt_480b0ab179f4de6ed969ba2efb42e6d49f0e307bfef11bf69bba9550eeec3023
revision_id: rev_28dfd8cfc16f255930cb96f29db9d78b57edf80b088ba2207dcd4d2f8bbee620
source_published_at: 2026-11-25T18:58:53Z
first_seen_at: 2026-11-28T10:23:41.440318Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 28
interpretation_sha256: "sha256:48ea261b67e6a5c022efb2436189c757c6a7aab2aeb1f943f7a8946e825f1e3b"
description: "Mixture-of-Loops Transformer（MoLT）重新设计循环 Transformer 中相邻循环之间的信息传递方式，以键值作为跨深度、跨循环选择的记忆。其 U-MoLT 变体将记忆构建与预测读取分离，在保持模型质量的同时减少不必要的解码遍历。"
external_url: http://arxiv.org/abs/2611.34923v1
parent_observation_id: null
last_seen_at: 2026-11-28T10:23:41.440318Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2611.34923v1](http://arxiv.org/abs/2611.34923v1)
- **发布域名**: arxiv.org
- **分类**: cs.LG
- **作者**: Lianghui Zhu、Shijie Wang、Xinggang Wang 等

## 要点解读

### 这是什么
Mixture-of-Loops Transformer（MoLT）重新设计循环 Transformer 中相邻循环之间的信息传递方式，以键值作为跨深度、跨循环选择的记忆。其 U-MoLT 变体将记忆构建与预测读取分离，在保持模型质量的同时减少不必要的解码遍历。

### 用在哪里
它适用于语言模型预训练、继续预训练及推理部署，尤其适合需要在表达能力与计算效率之间取舍的场景。文中在 OLMo3、Qwen3.5-0.8B-Base 等模型上进行了训练与延迟评估。

### 可以推断的
- 推测：以键值记忆替代更密集的循环间依赖，可能为可扩展训练和高效推理提供一种结构化方案。
- 推测：U-MoLT 兼顾验证损失、困惑度、任务准确率与推理延迟，说明该方法更偏向综合效率优化，而非只追求单一指标。

## 来源摘要/节选

> Looped Transformers boost expressivity by reusing shared layers across loops, yet at the cost of efficiency. Pushing their expressivity-efficiency frontier requires rethinking the core mechanism connecting adjacent loops: What should be passed as a Transformer loops? We introduce Mixture-of-Loops Transformer (MoLT), whose Mixture-of-Loops Attention (MoLA) uses keys and values (KV) as memory for selective reuse across depths and loops. Under loop residual, MoLT-R retains the residual stream and reads local KV across loops for expressivity. Under loop KV, MoLT-KV instead restarts from embeddings and reads current-loop local KV with preceding-loop memory KV at earlier positions for efficiency. MoLT-KV eliminates same-position cross-loop dependence and, paired with loop forcing for parallel training, unlocks single-traversal Mixture-of-Loops (MoL) decoding beyond the training loop horizon. To balance efficiency and quality, we introduce U-shaped MoLT (U-MoLT), which separates memory construction from prediction readout and skips unused decoder traversals without changing predictions. In 400B-token pretraining, U-MoLT outperforms OLMo3 across 700M/1.5B dense and 3B MoE models, achieving 1.7x validation cross-entropy (CE) token efficiency at 700M while improving 3B MoE 10-domain perplexity by 0.75 and 10-task accuracy by 2.1 percentage points. In 100B-token continued pretraining of Qwen3.5-0.8B-Base, our U-MoLT adaptation lowers CE on all 11 domains over the matched baseline with 1.4x mean token efficiency. At inference, U-MoLT with MoL-Hybrid-2 matches non-looped OLMo3 latency at 996.6 vs. 1,000.6 ms on S-size (~113M) models. Code is available at https://github.com/hustvl/MoLT

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。