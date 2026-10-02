---
title: "Reconstruct, Practice, Go Real: Guided Self-Improvement for Embodied Agents"
date: 2026-10-02T23:51:49+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "Prompt 工程", "cs.RO", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:4978eae66d579bf87437f494b9ca44245975a4e21a361a63ed1f9184abc02e50"
source_payload_sha256: "sha256:c18cccfdcf5b3736b7879815d3177ecf81304f9218965fb7380a0305130beb29"
observation_id: obs_e2a630667d4124a4e7a04cb1d71cc7c64e00f04b0351aeef7e26af3776772bb7
event_id: evt_b6773f3d18f7608bf93b91bd352d07785d5686288e191ece54553a971d077d62
revision_id: rev_932946ed74b70675a24883b149c1013e92290d5a346b06fa343a711cd78782b8
source_published_at: 2026-10-01T17:59:50Z
first_seen_at: 2026-10-02T15:48:29.164280Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 75
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2610.02204v1
parent_observation_id: null
last_seen_at: 2026-10-02T15:48:29.164280Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2610.02204v1](http://arxiv.org/abs/2610.02204v1)
- **发布域名**: arxiv.org
- **分类**: cs.RO
- **作者**: Yen-Jen Wang、Haozhe Jiang、Shuying Deng 等

## 来源摘要/节选

> Building reliable robot capabilities across diverse tasks requires substantial human effort to develop and maintain skills, design rewards, and integrate perception with control. We present Reconstruct, Practice, Go Real (RPG), a framework for autonomous improvement of robot execution systems without updating model weights. RPG identifies manipulation capabilities in an offline dataset and constructs related practice tasks in simulation. During practice, RPG uses execution feedback, privileged simulator state, and available dataset videos to diagnose failures. It develops new reusable symbolic skills, refines existing skills, and revises the system prompt based on these diagnoses. Cross-task evaluation tests individual candidate changes and merged revisions before they are retained for reuse. At test time, a multimodal LLM uses the resulting system prompt and skill library to coordinate perception and robot control. On held-out initializations of 22 manipulation tasks, RPG improves task success from 28.6% after the first practice round to 95.0% after 15 rounds, outperforming all evaluated baselines, including ASPIRE (75.5%) and CaP-Agent0 powered by GPT-6 Astra Pro (60.0%). After a common calibration and hardware-adaptation procedure, the frozen system succeeds in all 30 physical trials, with ten trials on each of three tasks. Project Website: https://rpg-robot.github.io/

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。