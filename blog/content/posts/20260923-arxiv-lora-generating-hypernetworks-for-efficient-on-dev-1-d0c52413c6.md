---
title: "LoRA-generating hypernetworks for efficient on-device LLM generative personalization"
date: 2026-09-23T08:34:04+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "cs.LG", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:7b5c7edab2bbd80c51bfe0f263dc6e9603fb8a3b22e7768c7fd53f5722918f8f"
source_payload_sha256: "sha256:4ad754cb380571f2aab99d8da037659483075d1bf843ef0af2c5517b08db7354"
observation_id: obs_d0c52413c6c78a4e3a9a4edfc2ab44feaf6fb942b414ade04be688dccdf864a8
event_id: evt_721aee7b06456b16cf2fc99a7452c7fe4e09d12144eb74d3824384dde02c09ff
revision_id: rev_4519f0a4e84d74d0134f14bbb968bf15273209382d6d9a9c1e5f60ec6380f9ca
source_published_at: 2026-09-21T17:55:48Z
first_seen_at: 2026-09-23T00:32:18.512608Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 84
interpretation_sha256: "sha256:0c1cc70071e34edd2561023bc4e2119d1157f385383f7d4664ec2da7dc775115"
description: "该工作提出一种在移动端为大型语言模型生成低秩适配（LoRA）的超网络方法，利用用户上下文直接合成个性化适配器，兼具推理时仅需前向传播和模型权重更新的优势。"
external_url: http://arxiv.org/abs/2609.24979v1
parent_observation_id: null
last_seen_at: 2026-09-23T00:32:18.512608Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.24979v1](http://arxiv.org/abs/2609.24979v1)
- **发布域名**: arxiv.org
- **分类**: cs.LG
- **作者**: Sean Augenstein、Li Ding、Jihwan Lee 等

## 要点解读

### 这是什么
该工作提出一种在移动端为大型语言模型生成低秩适配（LoRA）的超网络方法，利用用户上下文直接合成个性化适配器，兼具推理时仅需前向传播和模型权重更新的优势。  

### 用在哪里
适用于在手机等资源受限设备上提供定制化对话或文本生成的服务场景，对隐私要求高、希望减少云端依赖的开发者与研究者会感兴趣。  

### 可以推断的
推测：超网络在部署前需要在大规模用户上下文数据上进行离线训练，这一步的计算成本可能较大。  
推测：由于适配器在本地生成，若模型或语言能力需要更新，可能要重新训练或微调超网络本身。

## 来源摘要/节选

> On-device large language models (`LLMs'), e.g. running on mobile phones, are ripe for improvement via personalization. The limited compute resources of mobile devices impose limits on model scale and thus model quality, making any realizable quality gains highly impactful. At the same time, their personal nature (i.e., the close coupling to a particular user) means that a given on-device LLM tends to be used in similar, predictable patterns over the course of time. This paper presents a novel method for personalizing on-device LLMs. It trains a hypernetwork to map a user's context tokens to a low-rank adaptation (`LoRA') well-suited to that user. Once the trained common artifacts are deployed to users' devices, each user uses the hypernetwork to synthesize (entirely on device) a personalized LoRA. This approach blends the benefits while avoiding the drawbacks of two existing approaches to LLM customization: in-context learning (`ICL') and parameter-efficient fine-tuning (`PEFT'). Like ICL (and unlike PEFT), the on-device phase of our approach is computationally feasible, requiring only forward passes through neural networks. Like PEFT (and unlike ICL), our approach modifies the `target' base LLM via weights (the LoRA), avoiding negative consequences (e.g. increased latency) associated with extending the input sequence. Our approach is particularly well-suited to the mobile device regime. Apart from the on-device compute and latency benefits mentioned, it also requires minimal additional storage, as internally its architecture partly leverages the same LLM weights as belong to the target LLM to be personalized. We demonstrate the benefits of LoRA-generating hypernetworks on several representative personalization datasets, comparing against baselines like ICL and PEFT. Of note, our personalization experiments focus on more challenging and less studied long-form text generation tasks.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。