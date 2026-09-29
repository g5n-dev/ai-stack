---
title: "Telescopic Language Models"
date: 2026-09-29T23:53:46+08:00
draft: false
entry_kind: "auto"
tags: ["AI", "cs.CL", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:8991b14bb3f28aa3692228a075ada45b687b5ba3ba1b56604ef0046c7b359a63"
source_payload_sha256: "sha256:4999c6699940e5cbba540905c4d7e0c486fbe08de542d26bb78d12999704e913"
observation_id: obs_03cb481dafd25953aa0705b4bceeadd701433c62532f3cdd9493d98aea21c64d
event_id: evt_c5aa1c5612eebf32d854ccafd0cf6b7b7526f797a8a1a620d2ac7aaacdeb3a79
revision_id: rev_f22b79012eae7cdf33de811df32088f3703a18b5f01d725ba33c0597bb76bea0
source_published_at: 2026-09-28T17:59:53Z
first_seen_at: 2026-09-29T15:50:53.659399Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 26
interpretation_sha256: "sha256:02d8f06328bf51573986386a1996d2b7b0ca528b91bfe70907b8ec69c92323fc"
description: "该工作提出一种可伸缩的语言模型，通过在每次训练迭代中同时使用随机截断的容量前缀和完整容量的前向‑后向通道，使同一模型在任意层数前缀下都保持有效的语言建模能力。"
external_url: http://arxiv.org/abs/2609.35769v1
parent_observation_id: null
last_seen_at: 2026-09-29T15:50:53.659399Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.35769v1](http://arxiv.org/abs/2609.35769v1)
- **发布域名**: arxiv.org
- **分类**: cs.CL
- **作者**: Zhilin Guo、Boqiao Zhang、Hakan Aktas 等

## 要点解读

### 这是什么
该工作提出一种可伸缩的语言模型，通过在每次训练迭代中同时使用随机截断的容量前缀和完整容量的前向‑后向通道，使同一模型在任意层数前缀下都保持有效的语言建模能力。

### 用在哪里
适用于需要在不同计算预算下部署同一模型的场景，例如在延迟敏感或资源受限的环境中动态选择模型深度，从而避免为每个预算单独训练或压缩模型。

### 可以推断的
推测：在推理阶段可以根据实际算力或响应时间要求自由选择模型层数，帮助在质量与成本之间实现更平滑的权衡。  
推测：如果在训练时仅监督少量固定退出点，模型在其他深度的性能可能会显著下降，说明训练目标的覆盖面对整体表现至关重要。

## 来源摘要/节选

> One deployed language model must often serve many compute budgets, yet serving each budget still means a separate training or compression run per point. We train a Telescopic Language Model (TLM) to be that continuum: a nested-capacity Transformer supervised by stochastic prefix supervision with a full anchor. At every step, one randomly truncated prefix of the capacity axis is trained against the full next-token target, alongside one full-capacity pass, so the trained artifact is a valid language model at every depth. Two forward-backward passes per step, no architectural change, nothing extra at inference. Fixed-exit suites such as Matryoshka Language Model Suites (MLMS) occupy one point in this design space, and the point has a cost: supervising only a few fixed exits leaves the nested model at chance level everywhere else (perplexity 10^2-10^5 in our baselines). On a 200M proxy suite (20B FineWeb-Edu tokens, identical data stream for all methods), a single TLM run is a valid language model at every one of its twenty layer prefixes, in perplexity and on perplexity-sensitive downstream tasks, reducing the area under the quality-budget curve by 43-44% relative to the fixed-exit suites while matching them at full capacity, at ~12% lower GPU cost per run. The prefix sampling density is a dial: concentrating it on a few depths recovers fixed-exit quality there at the price of the continuum, so the operating points become a training-time choice rather than an architectural one. These results indicate that the training objective, not the nesting itself, is what makes a model elastic.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。