---
title: Physics Is All You Need? A Case Study in Physicist-Supervised AI Development
  of Scientific Software
date: 2026-05-29 21:23:58+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
- AI Agent
categories:
- 论文
scenarios:
- AI/ML项目
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2605.30353v1
aliases:
- /posts/20260530-arxiv_ai-physics-is-all-you-need-a-case-study-in-physicist--0/
- /posts/20260531-arxiv_ai-physics-is-all-you-need-a-case-study-in-physicist--0/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:14cad0cd3b542cddd549053084aedd2664010e38b018877fd7a48fa639ef46a0
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 99
captured_at: '2026-07-18T04:29:58.207159Z'
source_capture_sha256: sha256:a58ffb3970348734d5e97fd469b41ad62853dcde2e321535afb49938d5a4c738
source_capture_chars_original: 1833
source_publication_excerpt_chars: 1833
observation_id: obs_61988d1570e25e068734f3f6807f7bc111e9ec3d0d01a31c9bc92caa94ba7412
revision_id: rev_6d422d0b3789865693d1b741dec3b5243c56b2aae6af84bc83825e255a15045e
event_id: evt_80ece0195d506857de2087087c15598ef2167e03eec98c208286b6359a0ab4d0
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-05-29T16:35:21Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2605.30353v1](<https://arxiv.org/abs/2605.30353v1>)
- **作者**: Nhat-Minh Nguyen
- **分类**: cs.AI
- **论文时间**: 2026-05-28T17:59:59Z
- **论文 PDF**: [https://arxiv.org/pdf/2605.30353v1.pdf](<https://arxiv.org/pdf/2605.30353v1.pdf>)

## 来源摘要/节选

> Are AI agents tools, co-authors, or researchers? We present a quantified case study \($N=1$\): a physicist supervising an AI coding agent \(Claude Code, Sonnet and Opus models\) over 12 work days and 57 sessions to build CLAX-PT, a differentiable one-loop perturbation theory module in JAX. We documented and classified 15 supervision events by intervention level. The agent resolved ten autonomously by iterating against oracle tests. Two more by the physicist's domain knowledge. The three it could not -- all evaded oracle detection -- share a common property: the agent treated symptom reduction as root-cause resolution. It spent 33 of the 57 sessions adjusting coefficients within a code architecture that could not represent the target physics, and could not re-evaluate its CLASS-PT branch choice even when prompted to reconsider; only an injected physics concept \(anisotropic BAO damping\) triggered the redesign. Separately, the agent committed a calibrated correction that passed all oracle tests but corresponded to no quantity in the theory, predicting wrong values at any other cosmology. The fudge factor was caught and replaced within the same session. Three supervision practices proved critical for catching what oracle tests missed: testing at diverse parameter points beyond the fiducial calibration; shared changelogs that surfaced stalled exploration across sessions; and an explicit rule against unphysical numerical patches. In this case, supervision design, not model capability, determined whether the agent's output was trustworthy. Closing the gap would require agents that propose architectural alternatives rather than optimize within a given structure, and distinguish predictive adequacy from explanatory correctness -- capabilities not exhibited here, not obviously addressed by scaling alone. \[Abridged.\]

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
