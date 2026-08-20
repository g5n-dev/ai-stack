---
title: "SPADE: Self-Play in Adaptive Synthetic Executable Environments"
date: 2026-08-21T07:42:06+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "cs.CL", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:73289b6ec2e2dccdf48dd7364bb5589e070338c26646b0b26e3f370a0a953c4a"
source_payload_sha256: "sha256:d020b20ac602cde0136e67a25288b8764dc8be704fa1dc2f632f8f9941345635"
observation_id: obs_dacc985195c52a763ca1a3c1857b6e6513f35ed01af99633bf42dd0396474168
event_id: evt_c482c7deec5011cf710b30b21fc2593322be47bf97578b039345f1f564a783b4
revision_id: rev_cfc3dacb5a63cf9d61ca9d254fbde6e4c94ab2a356ef87067a40cedc3dce6de5
source_published_at: 2026-08-19T17:58:56Z
first_seen_at: 2026-08-20T23:39:40.930668Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 62
interpretation_sha256: "sha256:df5517b89057eeb48142654460b7e493d55867ad9ce14dae8d629df235b76f02"
description: "该工作提出一种自博弈强化学习框架，让同一个大语言模型兼任“环境设计者”和“推理智能体”。环境以可执行代码形式生成，具备状态转移、奖励函数和验证逻辑，智能体在其上学习并通过对比有/无提示的收益差距来调整设计者，使其持续在“能力边缘”生成可行的任务。"
external_url: http://arxiv.org/abs/2608.19197v1
parent_observation_id: null
last_seen_at: 2026-08-20T23:39:40.930668Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.19197v1](http://arxiv.org/abs/2608.19197v1)
- **发布域名**: arxiv.org
- **分类**: cs.CL
- **作者**: Bo Liu、Simon Yu、Yiding Jiang 等

## 要点解读

### 这是什么
该工作提出一种自博弈强化学习框架，让同一个大语言模型兼任“环境设计者”和“推理智能体”。环境以可执行代码形式生成，具备状态转移、奖励函数和验证逻辑，智能体在其上学习并通过对比有/无提示的收益差距来调整设计者，使其持续在“能力边缘”生成可行的任务。

### 用在哪里
适用于需要让语言模型在多轮推理、代码执行、工具使用等复杂场景下自行提升的研究与实验。对希望在缺乏人工标注数据的情况下构建自适应训练循环的团队尤其有帮助。

### 可以推断的
推测：该方法在大规模实验时可能需要显著的计算资源，因为环境生成与策略学习同步进行。  
推测：通过让环境设计本身可学习，模型在面对新颖任务时或能更快适应，而不依赖预先收集的固定数据集。

## 来源摘要/节选

> Continuous self-improvement requires an ever-expanding pool of self-generated, diverse, adaptive goals. For language agents, existing training environment pools (hand-curated, statically synthesized, or frozen-verifier) keep the goal distribution fixed as the learner scales. We introduce SPADE (Self-Play in Adaptive Synthetic Executable Environments), a self-play RL framework in which a single LLM plays two roles: an Environment Designer that writes complete, long-horizon training environments as executable code with an OpenAI Gym-style reset()/step() interface, and a Reasoning Agent that learns to act in them. Each is a stateful, multi-turn environment (state transitions, reward functions, and verification code), so one interface spans reasoning problems and multi-step agentic tool use. The Reasoning Agent's regret is estimated using the gap between its reward with and without privileged hints; in optimizing this regret signal the Environment Designer learns to target environments at the edge of the agent's capabilities while keeping them feasible. Through extensive experimentation, we find several components critical to success: grounding the Environment Designer on documents sampled from a large pretraining corpus, and giving it an accumulated environment memory. Scaling to 30B-parameter models, SPADE improves over the strongest fixed-environment baseline by +5.3 on average across eight held-out math, science, code, and reasoning benchmarks, and lifts the tool-use setting by +5.7 on BFCL-v4 multi-turn and +13.9 on ACEBench-Agent; on the games setting, the margin over the strongest baseline grows with model scale. By making environment design itself a learnable component, SPADE takes a concrete step toward open-ended self-improvement.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。