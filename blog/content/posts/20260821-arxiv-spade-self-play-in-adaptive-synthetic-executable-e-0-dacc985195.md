---
title: "SPADE: Self-Play in Adaptive Synthetic Executable Environments"
date: 2026-08-21T06:47:22+08:00
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
first_seen_at: 2026-08-20T22:45:01.181160Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 62
interpretation_sha256: "sha256:3004ed3f14e06d7614108df17103e03aa1a93d59feafa56b27241ee03158e881"
description: "SPADE 是一种自博弈强化学习框架，让同一个大语言模型同时扮演**环境设计者**和**推理智能体**两个角色。设计者以代码形式生成具有状态转移、奖励函数和验证逻辑的可执行训练环境，推理智能体在其中学习解决长时程任务，并通过比较有无特权提示的奖励差距来驱动设计者不断生成难度适中且可行的环境。"
external_url: http://arxiv.org/abs/2608.19197v1
parent_observation_id: null
last_seen_at: 2026-08-20T22:45:01.181160Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.19197v1](http://arxiv.org/abs/2608.19197v1)
- **发布域名**: arxiv.org
- **分类**: cs.CL
- **作者**: Bo Liu、Simon Yu、Yiding Jiang 等

## 要点解读

### 这是什么  
SPADE 是一种自博弈强化学习框架，让同一个大语言模型同时扮演**环境设计者**和**推理智能体**两个角色。设计者以代码形式生成具有状态转移、奖励函数和验证逻辑的可执行训练环境，推理智能体在其中学习解决长时程任务，并通过比较有无特权提示的奖励差距来驱动设计者不断生成难度适中且可行的环境。

### 用在哪里  
- 需要为语言智能体构建**多样化、可自动扩展的训练任务**时，如数学推理、代码执行、工具调用等多步骤场景。  
- 适用于研究**自驱动、开放域学习**以及想要把环境构建本身纳入可学习组件的团队。

### 可以推断的  
推测：让语言模型自行生成训练环境，可以在缺乏人工设计资源的情况下持续提升任务多样性和难度。  
推测：在模型规模增大时，设计者的能力提升可能会进一步缩小与固定环境基线的表现差距。

## 来源摘要/节选

> Continuous self-improvement requires an ever-expanding pool of self-generated, diverse, adaptive goals. For language agents, existing training environment pools (hand-curated, statically synthesized, or frozen-verifier) keep the goal distribution fixed as the learner scales. We introduce SPADE (Self-Play in Adaptive Synthetic Executable Environments), a self-play RL framework in which a single LLM plays two roles: an Environment Designer that writes complete, long-horizon training environments as executable code with an OpenAI Gym-style reset()/step() interface, and a Reasoning Agent that learns to act in them. Each is a stateful, multi-turn environment (state transitions, reward functions, and verification code), so one interface spans reasoning problems and multi-step agentic tool use. The Reasoning Agent's regret is estimated using the gap between its reward with and without privileged hints; in optimizing this regret signal the Environment Designer learns to target environments at the edge of the agent's capabilities while keeping them feasible. Through extensive experimentation, we find several components critical to success: grounding the Environment Designer on documents sampled from a large pretraining corpus, and giving it an accumulated environment memory. Scaling to 30B-parameter models, SPADE improves over the strongest fixed-environment baseline by +5.3 on average across eight held-out math, science, code, and reasoning benchmarks, and lifts the tool-use setting by +5.7 on BFCL-v4 multi-turn and +13.9 on ACEBench-Agent; on the games setting, the margin over the strongest baseline grows with model scale. By making environment design itself a learnable component, SPADE takes a concrete step toward open-ended self-improvement.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。