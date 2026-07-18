---
title: 'SceneCritic: A Symbolic Evaluator for 3D Indoor Scene Synthesis'
date: 2026-04-15 23:20:33+08:00
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
external_url: https://arxiv.org/abs/2604.13035v1
aliases:
- /posts/20260416-arxiv_ai-scenecritic-a-symbolic-evaluator-for-3d-indoor-sce-0/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:09ecc37a4d61eddc784ebe617a891fa67aa8fef6f5e1ca8d321fdfb63a95a797
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 63
captured_at: '2026-07-18T04:29:12.103286Z'
source_capture_sha256: sha256:d8533a7654fb0f5ff409247204902b668a21291dcbe0cd8e9ac9936075d675db
source_capture_chars_original: 1664
source_publication_excerpt_chars: 1664
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2604.13035v1](<https://arxiv.org/abs/2604.13035v1>)
- **作者**: Kathakoli Sengupta, Kai Ao, Paola Cascante-Bonilla
- **分类**: cs.CV
- **论文时间**: 2026-04-14T17:59:26Z
- **论文 PDF**: [https://arxiv.org/pdf/2604.13035v1.pdf](<https://arxiv.org/pdf/2604.13035v1.pdf>)

## 来源摘要/节选

> Large Language Models \(LLMs\) and Vision-Language Models \(VLMs\) increasingly generate indoor scenes through intermediate structures such as layouts and scene graphs, yet evaluation still relies on LLM or VLM judges that score rendered views, making judgments sensitive to viewpoint, prompt phrasing, and hallucination. When the evaluator is unstable, it becomes difficult to determine whether a model has produced a spatially plausible scene or whether the output score reflects the choice of viewpoint, rendering, or prompt. We introduce SceneCritic, a symbolic evaluator for floor-plan-level layouts. SceneCritic's constraints are grounded in SceneOnto, a structured spatial ontology we construct by aggregating indoor scene priors from 3D-FRONT, ScanNet, and Visual Genome. SceneOnto traverses this ontology to jointly verify semantic, orientation, and geometric coherence across object relationships, providing object-level and relationship-level assessments that identify specific violations and successful placements. Furthermore, we pair SceneCritic with an iterative refinement test bed that probes how models build and revise spatial structure under different critic modalities: a rule-based critic using collision constraints as feedback, an LLM critic operating on the layout as text, and a VLM critic operating on rendered observations. Through extensive experiments, we show that \(a\) SceneCritic aligns substantially better with human judgments than VLM-based evaluators, \(b\) text-only LLMs can outperform VLMs on semantic layout quality, and \(c\) image-based VLM refinement is the most effective critic modality for semantic and orientation correction.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
