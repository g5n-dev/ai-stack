---
title: "Semifactual Credit-Augmented Policy Optimization"
date: 2026-10-01T21:14:33+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "Prompt 工程", "cs.LG", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:227ea2cee6ec4f57092b627a9be027378283e6eba7923a7aa127b1684c0e7e79"
source_payload_sha256: "sha256:6b99c1207a8b0be1c41aaea6700c72fa9d056c9716cc97498abc21b59799bc0d"
observation_id: obs_9f89f727056a732f64957c468a0d0c20022639851c976aa0545ad191899b664d
event_id: evt_35e5cb6e7372530653e7849c3bb5c368101aa39d36388e5376dcd17b7b63050e
revision_id: rev_3681cf59be1e8bf82515a9ac1ed9063bc1fc3ea65bf12d675a86d88807e42031
source_published_at: 2026-09-30T17:59:56Z
first_seen_at: 2026-10-01T13:11:41.761992Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 48
interpretation_sha256: "sha256:eb17d44ed43bce76f2ddc0e39e8a8b0af7370f0502c67f5ff35acf351332efd9"
description: "该研究针对大语言模型在强化学习训练中存在的预测敏感性问题，提出了一种改进的训练方法。该方法通过分析模型对半事实扰动的响应稳定性，在token级别调整信用分配，使训练过程能够区分关键推理步骤和可能依赖虚假特征的无效token。"
external_url: http://arxiv.org/abs/2609.40360v1
parent_observation_id: null
last_seen_at: 2026-10-01T13:11:41.761992Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.40360v1](http://arxiv.org/abs/2609.40360v1)
- **发布域名**: arxiv.org
- **分类**: cs.LG
- **作者**: Junshu Pan、Zhizhang Fu、Shulin Huang 等

## 要点解读

### 这是什么

该研究针对大语言模型在强化学习训练中存在的预测敏感性问题，提出了一种改进的训练方法。该方法通过分析模型对半事实扰动的响应稳定性，在token级别调整信用分配，使训练过程能够区分关键推理步骤和可能依赖虚假特征的无效token。

### 用在哪里

该研究适用于需要提升大语言模型数学推理和复杂推理能力的场景。对于从事模型训练优化、强化学习应用开发或推理能力增强的研究人员和技术团队具有参考价值，尤其适合关注模型泛化能力和训练稳定性的实践者。

### 可以推断的

推测：token级别的敏感性分析可能揭示模型在处理特定问题时存在的不合理依赖路径，有助于识别训练数据中的潜在偏置来源。

推测：该方法中关于稳定性的评估方式可能需要针对不同任务类型进行适配，因为任务特征差异会影响半事实干预的有效性。

## 来源摘要/节选

> Reinforcement learning with verifiable rewards (RLVR) has improved the reasoning capabilities of large language models (LLMs), yet their predictions remain sensitive to task-irrelevant prompt features. We investigate this sensitivity through semifactual prompt interventions that preserve the underlying problem and its answer. Our analysis reveals substantial variation in token-level sensitivity and shows that suppressing high-drift token candidates during decoding improves reasoning accuracy without updating model weights. These findings highlight a limitation of Group Relative Policy Optimization (GRPO), which assigns the same outcome-derived advantage to every response token and may reinforce potential spurious dependence alongside useful reasoning. Motivated by this observation, we introduce Semifactual Credit-Augmented Policy Optimization (SCAPO), a causally inspired variant of GRPO that incorporates semifactual stability into token-level credit assignment. SCAPO measures token probability drift for fixed responses under semifactual interventions and uses normalized stability scores to reduce advantages for relatively unstable tokens during early training, while granting no additional credit for stability alone. On Qwen3-4B-Base and Qwen3-1.7B-Base, SCAPO improves AIME 2024-2026 accuracy over GRPO by 5.63 and 4.17 percentage points, respectively. At both model scales, SCAPO achieves the best results on most evaluated mathematics benchmarks and all evaluated out-of-distribution benchmarks among the compared methods. These results suggest that semifactual stability provides an effective training signal for improving reasoning and generalization through finer-grained credit assignment in RLVR. The code is available at https://github.com/DtYXs/SCAPO.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。