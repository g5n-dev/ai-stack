---
title: "Agogic: Performance-Timed Music Tokens for LLM-Native Text-to-Symbolic-Music Generation"
date: 2026-08-06T02:53:31+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "cs.SD", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:1897b04d58b15cc8e20b5f23a23431ff43c329b915d72d95474078140e70f9ca"
source_payload_sha256: "sha256:8593e4c0bd208f31fe3a9f52769a7e6bbb0920f7e059d43a3fe09fe9b08d1cc8"
observation_id: obs_835fc536357b976782fafec88b066df8b01901b7b1cf47866c33ec568021ccf7
event_id: evt_ef2b4c37c06c7656acbd2f2ebfc62b2a4baad4dabbecdeb1a5cfb8e675b9df1a
revision_id: rev_1d350a12310f264f132ef90e4d95b45430157b4220d1d00a8e0eb5af2b37013d
source_published_at: 2026-08-04T17:56:49Z
first_seen_at: 2026-08-05T18:50:22.576155Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 87
interpretation_sha256: "sha256:1ca09532a6288acb4f115794b3a00bbacb1ec3f9ffdd3c075979b0fd765f48ba"
description: "该研究通过固定模型、数据、算力和解码方式，系统比较七种不同的音乐标记化方案对生成质量的影响，并提出一种以演奏时序为核心的标记流，实验表明该标记化方式在保持分布一致性的前提下显著提升音符时值与力度的表达。"
external_url: http://arxiv.org/abs/2608.03999v1
parent_observation_id: null
last_seen_at: 2026-08-05T18:50:22.576155Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.03999v1](http://arxiv.org/abs/2608.03999v1)
- **发布域名**: arxiv.org
- **分类**: cs.SD
- **作者**: Junhao Chen、Mingjin Chen、Jingjia Mao 等

## 要点解读

### 这是什么  
该研究通过固定模型、数据、算力和解码方式，系统比较七种不同的音乐标记化方案对生成质量的影响，并提出一种以演奏时序为核心的标记流，实验表明该标记化方式在保持分布一致性的前提下显著提升音符时值与力度的表达。

### 用在哪里  
适用于从事文本转符号音乐、语言模型音乐生成的科研人员和工程师，尤其是需要选择或评估标记化方案的团队；也可为构建高质量音乐生成系统提供参考。

### 可以推断的  
推测：在相同训练条件下，标记化方案的选择对生成效果的影响可能大于单纯增大模型规模的收益。  
推测：通过在解码阶段加入轻量约束，可提升生成音乐对乐器种类和调性的一致性，且不增加分布偏离的风险。

## 来源摘要/节选

> Text-to-music language models begin with a choice usually made by default: how to tokenize music. Normally entangled with backbone, data, and recipe, its effect has never been measured in isolation. We fix pretrained Qwen3.5 (0.8B-27B), data, budget, and decoding, and swap only the representation across seven tokenizations, anchoring texture metrics to each representation's model-free ceiling. The ordering is clean and surprising: representation, not model size, is the binding variable for distributional fidelity. Scaling the backbone 34x barely moves Frechet Music Distance (FMD), whereas switching representation halves it. PMT, a performance-resolution stream we release (10 ms timing, per-note velocity, multi-track texture; 609 symbols), reaches FMD 159 at 0.8B against 272-286 for beat grids (1.7-1.8x lower, up to 2.8x elsewhere; non-overlapping bootstrap CIs), so a 0.8B performance-resolution model beats a 27B beat grid. It reappears on a 26M from-scratch backbone and a second performance-resolution tokenizer: a property of the class, not one lucky vocabulary. Nor is it a finer-lattice artifact: snapping PMT's onsets to the beat grids' resolution still leaves it 67-129 FMD ahead of both (n=500). The effect is distributional; whether it is audible is a separate question, left open by our probe, with a human study pre-registered. Native caption adherence is weak but separable: a lightweight decode-time constraint doubles instrument-F1 (.28 to .60) and Correct-Key (.16 to .35) at no distributional cost. We release the harness, 25+ checkpoints, two corpora (86.6k aligned across caption/MIDI/ABC/audio; 6.25M captioned, the largest for music), and an imprinting diagnostic: published text-to-MIDI systems reproduce their training distribution near-invariant to the caption (72% vs. 71% chord-time on disjoint domains). The field's next representation claim can now be measured, not asserted.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。