---
title: "One Frozen Simulator Is Not Enough: Simulator Collapse in Multi-Agent RL"
date: 2026-08-14T07:59:45+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "cs.CL", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:b847956497fbab358d390c64118cbe2ae8ee03daeb502f69badcb10b3a116a21"
source_payload_sha256: "sha256:784603ae315ee1575a31e407ffcd3b6f2fdda85c369a9947f8b2164d22e5fc7f"
observation_id: obs_d97729e3c0fc5f28143b6d79ff7f72ce03f2d3d18d5acb2b101d795854f36b02
event_id: evt_bb2bd0f39da8ceb8c18600f892ac96b237d44c53a50cb79a62618754defaf78a
revision_id: rev_16f62d77d7cf5e6a9945e34eba19408f71dbc920e860e92080ae3384343dbe08
source_published_at: 2026-08-12T16:55:50Z
first_seen_at: 2026-08-13T23:57:59.303467Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 72
interpretation_sha256: "sha256:9b85c8eafaa6c056021ff93009c6bb4b965debe9ed96b75bed0a509e05502d8e"
description: "这是一篇探讨多智能体强化学习中，单个语言模型模拟用户时出现的模式坍缩（simulator collapse）问题的研究，作者提出在推理时扩展采样多样性的方法，以及在训练时使用多模拟器协同训练的方法，以提升策略在不同环境下的迁移能力。"
external_url: http://arxiv.org/abs/2608.12253v1
parent_observation_id: null
last_seen_at: 2026-08-13T23:57:59.303467Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.12253v1](http://arxiv.org/abs/2608.12253v1)
- **发布域名**: arxiv.org
- **分类**: cs.CL
- **作者**: Simon Yu、Nicholas Tomlin、Marwa Abdulhai 等

## 要点解读

### 这是什么  
这是一篇探讨多智能体强化学习中，单个语言模型模拟用户时出现的模式坍缩（simulator collapse）问题的研究，作者提出在推理时扩展采样多样性的方法，以及在训练时使用多模拟器协同训练的方法，以提升策略在不同环境下的迁移能力。

### 用在哪里  
适用于人机对话系统的研发团队、需要训练多轮交互策略的研究者，以及关注强化学习泛化能力的工程师。

### 可以推断的  
推测：在训练环境缺乏多样性时，模型容易学习到针对单一模式的捷径，导致在实际部署时表现下降。  
推测：通过在训练阶段引入多个可调节的模拟器或采用多样化的响应抽样，可以缓解模式坍缩，提升策略的鲁棒性。

## 来源摘要/节选

> Multi-agent reinforcement learning for human-AI interaction typically relies on a single large language model to simulate user behavior. We show that this approach systematically fails to generalize, and trace the failure to simulator collapse: because the simulator LLM is mode-collapsed, an LLM policy trained against it overfits to narrow strategies that exploit the simulator's dominant mode, and such a policy transfers poorly to unseen simulators and real users. We formalize this collapse theoretically and propose two complementary solutions, one at inference time and one at training time. The inference-time solution, Verbalized Sampling, broadens the simulator's behavior by sampling from a verbalized response distribution, reducing mode collapse. The training-time solution, Co-Training, jointly optimizes the policy against a population of trainable simulators, preventing it from overfitting to any single simulator's mode. We validate both solutions on three multi-turn benchmarks: Persuasion for Good, $τ^2$-bench, and CooperBench. Verbalized Sampling improves held-out success by up to 9% over single-simulator RL, and Co-Training pushes gains further to 14%; the human study shows similar gain on real users. Both solutions preserve the policy diversity that collapses under single-simulator RL. To support further work in this direction, we release SCOPE, an open-source framework for Population Co-Training multi-agent RL. More broadly, our results suggest that the diversity of the training environment, not only the policy, is critical to the generalization of multi-turn RL to real-world deployment.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。