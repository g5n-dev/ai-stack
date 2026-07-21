---
title: 'CUDA Agent: Large-Scale Agentic RL for High-Performance CUDA Kernel Generation'
date: 2026-03-02 23:25:37+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
- AI Agent
- 大语言模型
- 深度学习
categories:
- 论文
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.24286v1
aliases:
- /posts/20260303-arxiv_ai-cuda-agent-large-scale-agentic-rl-for-high-perform-3/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:8fe1f1dadf935fd02f3ccd965dad5896cb469094c24d7d9db1bbbcc689922411
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 78
captured_at: '2026-07-18T04:26:08.408518Z'
source_capture_sha256: sha256:8bbcc11a44ba0174a7f1ad332ddcda6986bfa2f72ef65e532624f02aedc70e17
source_capture_chars_original: 1290
source_publication_excerpt_chars: 1290
observation_id: obs_572c567c49c57cc792e57affeb6abe06dd10aefa097d0c21555b358d4bc70480
revision_id: rev_ea0182ea7dd4b8044886ad769eea225c5e5feb445dde574c467a2d57a840bd89
event_id: evt_894005c1f0e20ceb42e9a2944afb95d60746a41c7aa50296e88fffb37443ebf3
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-03-02T06:24:05Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.24286v1](<https://arxiv.org/abs/2602.24286v1>)
- **作者**: Weinan Dai, Hanlin Wu, Qiying Yu, Huan-ang Gao, Jiahao Li, Chengquan Jiang, Weiqiang Lou, Yufan Song, Hongli Yu, Jiaze Chen, Wei-Ying Ma, Ya-Qin Zhang, Jingjing Liu, Mingxuan Wang, Xin Liu, Hao Zhou
- **分类**: cs.LG
- **论文时间**: 2026-02-27T18:58:05Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.24286v1.pdf](<https://arxiv.org/pdf/2602.24286v1.pdf>)

## 来源摘要/节选

> GPU kernel optimization is fundamental to modern deep learning but remains a highly specialized task requiring deep hardware expertise. Despite strong performance in general programming, large language models \(LLMs\) remain uncompetitive with compiler-based systems such as torch.compile for CUDA kernel generation. Existing CUDA code generation approaches either rely on training-free refinement or fine-tune models within fixed multi-turn execution-feedback loops, but both paradigms fail to fundamentally improve the model's intrinsic CUDA optimization ability, resulting in limited performance gains. We present CUDA Agent, a large-scale agentic reinforcement learning system that develops CUDA kernel expertise through three components: a scalable data synthesis pipeline, a skill-augmented CUDA development environment with automated verification and profiling to provide reliable reward signals, and reinforcement learning algorithmic techniques enabling stable training. CUDA Agent achieves state-of-the-art results on KernelBench, delivering 100\\%, 100\\%, and 92\\% faster rate over torch.compile on KernelBench Level-1, Level-2, and Level-3 splits, outperforming the strongest proprietary models such as Claude Opus 4.5 and Gemini 3 Pro by about 40\\% on the hardest Level-3 setting.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
