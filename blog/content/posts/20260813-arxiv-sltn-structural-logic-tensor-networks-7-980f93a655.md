---
title: "sLTN: Structural Logic Tensor Networks"
date: 2026-08-13T06:05:42+08:00
draft: false
entry_kind: "auto"
tags: ["AI", "cs.AI", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:f1801d6c5b9684648de3ec28fc15b21e2ac486f1fcc1c6fbf6b8a2747fe0cc0c"
source_payload_sha256: "sha256:b6b9986aacaeabc2662fe18720fa26571d89acefc621b3b29cc57b019f905b6d"
observation_id: obs_980f93a6557c850396cffedfc48a65d1301d9584e6d326e8d6410459c5fb2b0d
event_id: evt_5ef39cbd8ef694d527b2122d6243a3eb4b59df50805247130bdd77ed06cdb55e
revision_id: rev_29cff31afa57966a893af7c33a8bba65f68cde472353aeebd9ef75a647c230b5
source_published_at: 2026-08-11T16:58:38Z
first_seen_at: 2026-08-12T22:14:51Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 38
interpretation_sha256: "sha256:efe8784afa5883eea75f490ddc0ec9e0bc8a5f77bba4fc1c8032e952488f9359"
description: "sLTN 把时间步、序列位置、图节点这类结构维度提升为语言的基本元素，使逻辑约束能够在带有组织信息的数据上直接表达，并保留了原有 LTN 的张量语义作为特例。"
external_url: http://arxiv.org/abs/2608.11136v1
parent_observation_id: null
last_seen_at: 2026-08-12T22:02:29.794088Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.11136v1](http://arxiv.org/abs/2608.11136v1)
- **发布域名**: arxiv.org
- **分类**: cs.AI
- **作者**: Davide Rinaldi、Luciano Serafini

## 要点解读

### 这是什么
sLTN 把时间步、序列位置、图节点这类结构维度提升为语言的基本元素，使逻辑约束能够在带有组织信息的数据上直接表达，并保留了原有 LTN 的张量语义作为特例。

### 用在哪里
适用于在神经符号框架中引入时序、顺序或关系约束的场景，如需要对结构化数据施加业务规则或在深度学习模型里整合逻辑推理的研究者和工程师。

### 可以推断的
推测：实现会提供声明式的签名与公式解析功能，便于在 PyTorch 项目中直接使用 sLTN 库添加自定义约束。  
推测：结构维度的显式量化和关联能力使 sLTN 更适合需要对数据内部结构进行保留和推理的任务，而非仅处理扁平样本的情形。

## 来源摘要/节选

> Logic Tensor Networks (LTN) provide a neurosymbolic framework in which first-order logic is interpreted through tensor operations, enabling logical constraints to be integrated with differentiable learning. However, the original formulation of LTN is primarily suited to data represented as flat collections of individuals, and does not explicitly capture structural organization such as temporal order, sequential position, or graph connectivity. We introduce sLTN, an extension of LTN that makes structural dimensions first-class elements of the language. Structural dimensions represent named tensor axes associated with domain-specific organization, such as time steps, sequence positions, or graph nodes. They can be quantified explicitly, related through structural relations, and used to express temporal, sequential, and relational constraints directly at the logical level. We formalize the syntax and fuzzy tensor semantics of sLTN and show that, in the absence of structural dimensions, the framework recovers the original LTN semantics as a special case. We further describe a PyTorch implementation based on a declarative signature, formula parsing, and tensorial interpretation. The framework is illustrated on representative temporal and sequential reasoning examples. This paper serves as a companion to the sltn library, available at https://github.com/logictensornetworks/sltn.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。