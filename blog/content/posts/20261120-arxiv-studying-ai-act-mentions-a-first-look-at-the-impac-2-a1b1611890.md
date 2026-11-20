---
title: "Studying AI Act Mentions: A first look at the impact of the European Union's AI regulation on Hugging Face"
date: 2026-11-20T11:13:52+08:00
draft: false
entry_kind: "auto"
tags: ["AI", "cs.AI", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:5d0c55f2823f2a6c3460eb4826d571c4859ea33945d4f5f60a6ac2a4f18a7afa"
source_payload_sha256: "sha256:7e235a1aac55f5999929066aa46f03a2756d0f9259e50fae70900092ae4c478b"
observation_id: obs_a1b161189031d4b9cff10c3964311447b49a7f4e13e30748da05f9b15047ced4
event_id: evt_26c7c448e15f84ff7a71b8e2f0f2161f5e15054b005e05e99bdb1baa6b065d9e
revision_id: rev_a963072a353dcf6783d800d634f581db8845a6cdba281de70d555534e6b558c4
source_published_at: 2026-11-19T12:57:53Z
first_seen_at: 2026-11-20T03:11:56.286339Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 106
interpretation_sha256: "sha256:b91649afa5b65bdc29ce1e39bce9ac2fd1226c3697466584d11a5a91098ddc99"
description: "这项研究考察欧盟《人工智能法案》在 Hugging Face 社区中的实际提及与回应，分析了超过五百万条记录，并人工标注其中一千五百余条相关内容。研究发现，显式提及仍然较少，多数内容集中于责任归属、违规报告与合规材料更新。"
external_url: http://arxiv.org/abs/2611.26050v1
parent_observation_id: null
last_seen_at: 2026-11-20T03:11:56.286339Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2611.26050v1](http://arxiv.org/abs/2611.26050v1)
- **发布域名**: arxiv.org
- **分类**: cs.AI
- **作者**: Anamaria Mojica-Hanke、Tessi Aigbovbiosa-Igbinovia、Steffen Herbold

## 要点解读

### 这是什么
这项研究考察欧盟《人工智能法案》在 Hugging Face 社区中的实际提及与回应，分析了超过五百万条记录，并人工标注其中一千五百余条相关内容。研究发现，显式提及仍然较少，多数内容集中于责任归属、违规报告与合规材料更新。

### 用在哪里
适合用于评估开源模型与公共平台如何落实欧盟 AI 监管义务，以及设计平台合规提示、文档模板和自动检查机制。研究结果也可帮助合规人员理解开发者常用的声明方式及其不足。

### 可以推断的
- 推测：把责任声明转化为自动检查和标准化文档，可能比单纯要求作者作出声明更便于执行合规要求。
- 推测：若缺少平台辅助与清晰的范围指引，开发者的合规实践可能继续偏向形式化声明，而非具体实施措施。

## 来源摘要/节选

> The European Union's Artificial Intelligence Act (AI Act) entered into force in August 2024, and its obligations apply in stages. Obligations for providers of general-purpose AI models have applied since August 2025, and transparency rules since August 2026. These obligations affect developers who share and deploy models and applications on public platforms such as Hugging Face (HF), the largest platform for distributing AI artifacts. However, little is known about how practitioners respond to the regulation in practice. To address this gap, we conducted an empirical study of explicit references to the AI Act on HF. We collected over five million records, including repository cards, discussions, and commits from Models, Datasets, and Spaces, and identified over 1,500 records that explicitly mention the Act. Two coders manually labeled these records using a primarily closed coding approach, and we analyzed the resulting categories per source. We find that explicit references to the AI Act remain rare across all repository types. Repository cards mainly contain claims of compliance and responsibility, like ensuring compliance or assigning responsibility to downstream users, and some claim that the Act does not apply because the model is not a general-purpose AI model. Discussions are used to report alleged violations of the Act, while commits mainly update artifacts that support compliance. Overall, compliance statements focus on who is responsible rather than how compliance is achieved. We believe that this calls for direct platform support, e.g., automated checks and documentation templates, as well as clearer guidance on the scope of the AI Act.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。