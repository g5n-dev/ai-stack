---
title: "ESPO: Error-Structured Prompt Optimization via Diagnose, Diversify, and Stabilize"
date: 2026-09-05T02:26:17+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "自然语言处理", "Prompt 工程", "cs.CL", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:843038310e3282bae0d939a114befe3af97076dd442b2ac76f03e48674c762ec"
source_payload_sha256: "sha256:c1a6126fc55fe548371c9695acd7bb957d3565e469b27e893fd001c2bb9ce630"
observation_id: obs_9060a4ab2030050f8bc329ef82f6d86aad9d8ada98d1ba26fdf312a0d76afe70
event_id: evt_d7a038244c83e78a6d4fd966e42c0b6f18424648e9d73511ad2759c966887853
revision_id: rev_04f00b1b654a6e757ebc692de59fb9394498c8b29d24102fa88087a5b9cc35d6
source_published_at: 2026-09-03T17:59:37Z
first_seen_at: 2026-09-04T18:34:06Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 81
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2609.04197v1
parent_observation_id: null
last_seen_at: 2026-09-04T18:24:06.142073Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.04197v1](http://arxiv.org/abs/2609.04197v1)
- **发布域名**: arxiv.org
- **分类**: cs.CL
- **作者**: Lihao Liu、Peng Tang、Kunwar Yashraj Singh 等

## 来源摘要/节选

> Evolutionary prompt optimizers such as GEPA suffer from prompt bloat: each iteration appends rules and caveats, producing prompts up to 3$\times$ longer yet no more accurate. We trace this to three deficiencies - incomplete error observation, limited search diversity, and unreliable selection - and propose ESPO (Error-Structured Prompt Optimization), which decomposes prompt optimization into three phases: Diagnose clusters all training errors into structural patterns in one round; Propose generates candidates via four complementary strategies with independent biases; Select applies bootstrap stability selection. On seven public NLP benchmarks - Tweet, MMLU, GSM8K, HotpotQA, ScoNe, HoVer, and PUPA - ESPO improves average accuracy by $+$3.76 pp over the state-of-the-art (74.67% vs 70.91% for GEPA), matching or exceeding GEPA on every dataset while producing prompts 47% shorter (1,004 vs 1,878 chars) and faster at inference. Cross-model experiments across four additional student models (Gemma 3 12B, Mistral 14B, Qwen3 32B, Claude Haiku 4.5) show ESPO yields the best average accuracy on every model tested, with the largest gap on Qwen3 GSM8K (15.00% $\to$ 91.40%). A generalization bound (Appendix) grounds each phase in a corresponding term of the test-time gap, and the ablation confirms a key prediction: adding diversity without bootstrap selection actually hurts performance ($-$1.20%).

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。