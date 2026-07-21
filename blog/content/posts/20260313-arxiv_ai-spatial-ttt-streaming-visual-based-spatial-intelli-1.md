---
title: 'Spatial-TTT: Streaming Visual-based Spatial Intelligence with Test-Time Training'
date: 2026-03-13 23:24:24+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2603.12255v1
aliases:
- /posts/20260314-arxiv_ai-spatial-ttt-streaming-visual-based-spatial-intelli-1/
- /posts/20260315-arxiv_ai-spatial-ttt-streaming-visual-based-spatial-intelli-1/
- /posts/20260316-arxiv_ai-spatial-ttt-streaming-visual-based-spatial-intelli-1/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:8c2a5cc484b01f5bb7509a06c054d1f77d6905d6233ac7fdd4338f16beda568b
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 80
captured_at: '2026-07-18T04:28:15.328315Z'
source_capture_sha256: sha256:afc6b31aa0960dfa4ae6201c50b0c53c45769f469e6d1edc073b3d0349f5f3ef
source_capture_chars_original: 1449
source_publication_excerpt_chars: 1449
observation_id: obs_ae8ba86eed83b1859ed1e3e02710654780b95d9b7b1f68957d9b15b300c11da7
revision_id: rev_1eea764f5f9472969e65d7f1a2631db677385dcd51dcc1c54036985052269382
event_id: evt_9212ecce01998758a098c8ceb15a0b558f546e5eab4fb7541e2d9ff749a7ed4a
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-03-13T04:23:00Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.12255v1](<https://arxiv.org/abs/2603.12255v1>)
- **作者**: Fangfu Liu, Diankun Wu, Jiawei Chi, Yimo Cai, Yi-Hsin Hung, Xumin Yu, Hao Li, Han Hu, Yongming Rao, Yueqi Duan
- **分类**: cs.CV
- **论文时间**: 2026-03-12T17:58:58Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.12255v1.pdf](<https://arxiv.org/pdf/2603.12255v1.pdf>)

## 来源摘要/节选

> Humans perceive and understand real-world spaces through a stream of visual observations. Therefore, the ability to streamingly maintain and update spatial evidence from potentially unbounded video streams is essential for spatial intelligence. The core challenge is not simply longer context windows but how spatial information is selected, organized, and retained over time. In this paper, we propose Spatial-TTT towards streaming visual-based spatial intelligence with test-time training \(TTT\), which adapts a subset of parameters \(fast weights\) to capture and organize spatial evidence over long-horizon scene videos. Specifically, we design a hybrid architecture and adopt large-chunk updates parallel with sliding-window attention for efficient spatial video processing. To further promote spatial awareness, we introduce a spatial-predictive mechanism applied to TTT layers with 3D spatiotemporal convolution, which encourages the model to capture geometric correspondence and temporal continuity across frames. Beyond architecture design, we construct a dataset with dense 3D spatial descriptions, which guides the model to update its fast weights to memorize and organize global 3D spatial signals in a structured manner. Extensive experiments demonstrate that Spatial-TTT improves long-horizon spatial understanding and achieves state-of-the-art performance on video spatial benchmarks. Project page: https://liuff19.github.io/Spatial-TTT.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
