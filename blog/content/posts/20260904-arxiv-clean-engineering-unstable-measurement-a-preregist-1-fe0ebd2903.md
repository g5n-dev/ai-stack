---
title: "Clean Engineering, Unstable Measurement: A Preregistered Reliability Failure of Black-Box LLM Observers on Shared Endpoints"
date: 2026-09-04T17:42:05+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "cs.AI", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:6e8e231873a76cd5b2a9a9657a3c312f8b7d3af6e1a64a02711ec1ebb93d1b2a"
source_payload_sha256: "sha256:c38b7aee356f0ea9b302b7362a5b6e850da4121f28789546acfeac6a7ad54355"
observation_id: obs_fe0ebd2903fea3b7c8f32572461976c98adbc43a6a88d1e003cd616a9daadedd
event_id: evt_bb3de3e88fd3f849bccfffaae0fe041d04590dcc06a247e00587c96676adaefb
revision_id: rev_5d30cab8d915c37da0a2ba28212a3ef0bd9e3583a22e775b6b6188831f324d0f
source_published_at: 2026-09-03T17:59:43Z
first_seen_at: 2026-09-04T09:56:31Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 123
interpretation_sha256: "sha256:b8ab5c4ac8619e13b118f5ff6d7441a673faf72d03152959f2a582460ce20070"
description: "本文通过预先注册的大规模实验，验证“黑盒语言模型评判器在共享端点上对同一请求会产生相同结果”这一假设，发现实际排名一致性远低于预设阈值，表明该评判器缺乏仪器般的稳定性。"
external_url: http://arxiv.org/abs/2609.04198v1
parent_observation_id: null
last_seen_at: 2026-09-04T09:38:45.884804Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.04198v1](http://arxiv.org/abs/2609.04198v1)
- **发布域名**: arxiv.org
- **分类**: cs.AI
- **作者**: Haoyaun Zhu、Jie Zhang

## 要点解读

### 这是什么  
本文通过预先注册的大规模实验，验证“黑盒语言模型评判器在共享端点上对同一请求会产生相同结果”这一假设，发现实际排名一致性远低于预设阈值，表明该评判器缺乏仪器般的稳定性。

### 用在哪里  
适用于依赖外部共享端点进行自动评分、排序或构建排行榜的场景，尤其适合研究者和工程师在设计语言模型评价流程时参考。

### 可以推断的  
推测：在实际应用中，若未对评判工具本身的重复性和噪声水平进行测量就直接用于决定训练数据或模型排名，可能导致系统性偏差。  
推测：未来的评估框架需要在实验设计阶段先对评判器进行可靠性检验，以确保后续结论的有效性。

## 来源摘要/节选

> Language-model judges now gate training data, score generations, and drive leaderboards. The judge is then a measurement instrument, resting on one rarely stated assumption: the same request, sent to the same model name, reads the same tomorrow. We audited that assumption in two preregistered campaigns with every threshold fixed in advance; neither got past validating its instrument. Across 52,988 audited request attempts, same-window repeat rankings agreed at Spearman 0.400 against a required 0.90, and byte-identical next-day replays agreed at 0.78 against a required 0.99, each time with the execution record at ceiling. Three mechanisms explain the gap: a label-to-meaning mapping that biased readouts as strongly as the signal; candidate gaps seven orders of magnitude below the instrument's own noise floor; and byte-identical inputs returning different rankings, a noise that exact-permutation readouts compound. Neither metric substitution nor sampling repaired it on the tested grid. Preregistered follow-ups bound the problem: waiting did not help on the days sampled (0.805 versus 0.800, replicated over five further days); switching providers did not help (four providers share the floor, medians 0.74 to 0.88, predicted by none of the metadata fields they expose); self-hosting on batch-invariant kernels helped only while the server was quiet; and on constructed errors with known gaps, the readout's separation tracks error type, not size. We distill the evidence into a three-level snapshot-identity ladder, eight design rules, and a reporting checklist; a pilot at roughly 2% of the study's call volume would have exposed both unreachable gates in advance. All results concern externally measured behaviour on shared serving infrastructure. On a shared endpoint, a model name is not a frozen instrument; a preregistered evaluation must measure its instrument before freezing any gate on it.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。