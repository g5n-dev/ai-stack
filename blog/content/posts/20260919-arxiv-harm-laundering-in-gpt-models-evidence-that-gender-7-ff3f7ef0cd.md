---
title: "Harm Laundering in GPT Models: Evidence That Gender Discrimination Is Transformed Rather Than Reduced Across Safety-Trained Generations"
date: 2026-09-19T18:59:25+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "cs.CL", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:2165216f15c20dd882a44bf53496baa126c6aa5900ad2cce3a27375272a85c76"
source_payload_sha256: "sha256:b4f8fa9340160fbd1f75053eb2e42c8bd94b6e908c21ec9c177df1927ffc697a"
observation_id: obs_ff3f7ef0cd71957d42a56a37454f1ceaadcae39bb4a2a7e1285c59d40c440b29
event_id: evt_88354593e01fcc5e4263b5c8e8a9cb802d0651d2fa9b6c9d72e34181b94d10db
revision_id: rev_794f7ddbd6b6d4b5d02cca386aad9e8506a0efa6be06563be5cbdfc88f9c0bf8
source_published_at: 2026-09-17T17:49:28Z
first_seen_at: 2026-09-19T10:57:17.571650Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 135
interpretation_sha256: "sha256:ef25569c30ae18eeb4f0fa2c6573033a59046bb07d81fcbb00051110dd83b869"
description: "该研究指出，现有的安全评估依赖表层毒性指标，而模型实际上是将明显的歧视性内容转化为更隐蔽的形式，而非真正消除，这种现象被称为“危害洗白”。通过对 GPT 系列模型生成的性别导向文本进行大规模分析，揭示了不同代际模型在性别偏见表现上的转变。"
external_url: http://arxiv.org/abs/2609.20779v1
parent_observation_id: null
last_seen_at: 2026-09-19T10:57:17.571650Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.20779v1](http://arxiv.org/abs/2609.20779v1)
- **发布域名**: arxiv.org
- **分类**: cs.CL
- **作者**: Sarah Wyer、Sue Black、Noura Al Moubayed

## 要点解读

### 这是什么  
该研究指出，现有的安全评估依赖表层毒性指标，而模型实际上是将明显的歧视性内容转化为更隐蔽的形式，而非真正消除，这种现象被称为“危害洗白”。通过对 GPT 系列模型生成的性别导向文本进行大规模分析，揭示了不同代际模型在性别偏见表现上的转变。

### 用在哪里  
适用于 AI 安全研发团队、模型审计机构以及制定公平性监管政策的部门，帮助他们认识到仅凭表面毒性分数无法全面判断模型是否真正降低了危害。

### 可以推断的  
推测：表面毒性分数的下降可能掩盖了模型在更深层次上产生的性别偏见，需结合更细粒度的表征危害指标进行评估。  
推测：随着模型代际更新，开发者可能无意中将显性歧视内容转化为更隐蔽的表达，使得传统检测工具难以捕捉真实风险。

## 来源摘要/节选

> Safety evaluations for large language models rely on surface-form classifiers that report declining harm scores across model generations. We provide evidence that this methodology is systematically incomplete: explicit discriminatory content is transformed rather than removed. We call this \emph{harm laundering}. Analysing 450,000 gender-directed completions across 15 models spanning GPT-2 through to GPT-5 (OpenAI GPT lineage; three demographic conditions), we show that sexual violence clusters prevalent in GPT-2 women-directed output disappear by GPT-4, while men-directed completions gain positive representational territory (caregiving, emotional range, ally identity) that women-directed completions do not. The pattern is most visible at GPT-5: Topic~5 (1,997~documents) frames breast cancer as a men's rights debate, while zero equivalent clusters appear in women-directed output. Three independent classifiers score this content as non-toxic. Sentiment scores invert at GPT-4: early models demean women; later models over-correct. Topic diversity in women-directed completions falls 36\% relative to men at the GPT-4 alignment boundary (W/M~$= 0.58$, from $0.91$ at GPT-2). REGARD representational harm disparity correlates with release date ($ρ= +0.55$, $p = .034$) while Detoxify does not ($ρ= -0.23$, $p = .42$): toxicity scores fall as representational harm grows. We formalise harm laundering as a three-criteria test and provide a three-stage detection protocol applicable to any generative model. Within the OpenAI GPT lineage, toxicity score reduction is not a sufficient proxy for harm reduction.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。