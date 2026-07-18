---
title: 'EndoCoT: Scaling Endogenous Chain-of-Thought Reasoning in Diffusion Models'
date: 2026-03-13 23:24:24+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
- 大语言模型
categories:
- 论文
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2603.12252v1
aliases:
- /posts/20260314-arxiv_ai-endocot-scaling-endogenous-chain-of-thought-reason-2/
- /posts/20260315-arxiv_ai-endocot-scaling-endogenous-chain-of-thought-reason-2/
- /posts/20260316-arxiv_ai-endocot-scaling-endogenous-chain-of-thought-reason-2/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:768f46578aa85f0db5d7656287e2b8ea9ea1f54deaf35b7c3e8642ecc5a150a6
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 74
captured_at: '2026-07-18T04:28:07.966279Z'
source_capture_sha256: sha256:1eca422defaa54ad8269257f6df3f57432b62b34de1ad3523b03141d56962fc7
source_capture_chars_original: 1532
source_publication_excerpt_chars: 1532
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.12252v1](<https://arxiv.org/abs/2603.12252v1>)
- **作者**: Xuanlang Dai, Yujie Zhou, Long Xing, Jiazi Bu, Xilin Wei, Yuhong Liu, Beichen Zhang, Kai Chen, Yuhang Zang
- **分类**: cs.CV
- **论文时间**: 2026-03-12T17:58:48Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.12252v1.pdf](<https://arxiv.org/pdf/2603.12252v1.pdf>)

## 来源摘要/节选

> Recently, Multimodal Large Language Models \(MLLMs\) have been widely integrated into diffusion frameworks primarily as text encoders to tackle complex tasks such as spatial reasoning. However, this paradigm suffers from two critical limitations: \(i\) MLLMs text encoder exhibits insufficient reasoning depth. Single-step encoding fails to activate the Chain-of-Thought process, which is essential for MLLMs to provide accurate guidance for complex tasks. \(ii\) The guidance remains invariant during the decoding process. Invariant guidance during decoding prevents DiT from progressively decomposing complex instructions into actionable denoising steps, even with correct MLLM encodings. To this end, we propose Endogenous Chain-of-Thought \(EndoCoT\), a novel framework that first activates MLLMs' reasoning potential by iteratively refining latent thought states through an iterative thought guidance module, and then bridges these states to the DiT's denoising process. Second, a terminal thought grounding module is applied to ensure the reasoning trajectory remains grounded in textual supervision by aligning the final state with ground-truth answers. With these two components, the MLLM text encoder delivers meticulously reasoned guidance, enabling the DiT to execute it progressively and ultimately solve complex tasks in a step-by-step manner. Extensive evaluations across diverse benchmarks \(e.g., Maze, TSP, VSP, and Sudoku\) achieve an average accuracy of 92.1%, outperforming the strongest baseline by 8.3 percentage points.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
