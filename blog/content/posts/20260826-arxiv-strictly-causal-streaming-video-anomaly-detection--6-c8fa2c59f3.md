---
title: "Strictly Causal Streaming Video Anomaly Detection with a Theoretically-Grounded State-Space Core"
date: 2026-08-26T23:56:06+08:00
draft: false
entry_kind: "auto"
tags: ["AI", "cs.AI", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:953e5feef6cb2489bc5e331401c9debf2d5001ed0da33cf103ede167aae4e182"
source_payload_sha256: "sha256:cee00785e3706adc282b1fba3a5a70313ddb9e2b1cede26448168fc462be908c"
observation_id: obs_c8fa2c59f3b3c01999b322ea765cf475b38a8f356dffaa88c1a7490560badd54
event_id: evt_580baae8513af98e14a39b51562a720f136dbc3a7135133b6a9e9ace62dbee88
revision_id: rev_c758faaf30cc9bb6c86e045e83442b229ce97ee1f1c068c88cc35e4d2cd7096b
source_published_at: 2026-08-25T16:52:32Z
first_seen_at: 2026-08-26T15:53:04.084294Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 96
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2608.24810v1
parent_observation_id: null
last_seen_at: 2026-08-26T15:53:04.084294Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.24810v1](http://arxiv.org/abs/2608.24810v1)
- **发布域名**: arxiv.org
- **分类**: cs.AI
- **作者**: Yogesh Kumar

## 来源摘要/节选

> Recent work has applied Mamba style state space models (SSMs) to video anomaly detection, yet existing approaches still rely on buffering clips or windows internally, lack a theoretical account of how temporal memory relates to detection latency, and benchmark efficiency only through GPU throughput rather than the edge hardware these methods are intended to target. We introduce a strictly causal streaming anomaly detector whose fixed size state is updated in O(1) time and memory per incoming frame, with no lookahead and no clip buffering. Its temporal core is a diagonal linear state space recurrence with an input and state dependent decay gate, trained self supervised through causal next embedding prediction on a frozen visual backbone. We derive a closed form relationship between the recurrence decay spectrum and both detection delay and the shortest anomaly it can reliably capture, then validate empirically on UCSD Ped2 and CUHK Avenue. The settling delay bound predicted from the learned base decay (57 to 59 frames) sits far above the measured detection delay (1.6 and 18.4 frames), showing that the event boundary gate, not the base decay, governs responsiveness. We further report end to end latency and throughput measured directly on Apple M3 Pro hardware, 0.74 ms and 0.77 ms per frame (over 1300 FPS), rather than simulated GPU numbers. With an untuned initial configuration the method reaches 67.9 percent and 70.2 percent frame level AUC on Ped2 and Avenue, trailing prior non causal SSM baselines in accuracy. Ablations over decay rate, state size, and gating reveal that the gate contribution is dataset size dependent, hurting accuracy on the smaller Ped2 training set but helping on the larger Avenue one. Closing this accuracy gap and extending evaluation to a third, larger benchmark are immediate next steps.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。