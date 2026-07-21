---
title: "Watermark Forensics for Generative Models: An Information-Theoretic Perspective"
date: 2026-07-15T23:05:07+08:00
draft: false
entry_kind: "auto"
tags: ["cs.CR", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:cf3cf00c5341ab396fb6524b6aacb1cc3c10d8b7ddbb4af91fea4da9508df3ae"
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 79
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2607.13003v1
observation_id: obs_c71fbb3c8b150bc73be8468f2bc876e32f6d56b313df4ef3f7569fcae428b8f3
revision_id: rev_7f70342c89231cd80a8812f8535192bcef4e185450ec5e7fd86d886bc49dc05e
event_id: evt_3424a80cb002ab3416e7cb47a620c8278233b2ed8a4bf3df420e53646becf532
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-15T15:07:00Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2607.13003v1](http://arxiv.org/abs/2607.13003v1)

## 来源摘要/节选

> A watermark in a generative model's output is usually asked only whether a text is machine-made. The same mark can do more: attribute it to the user who produced it, extract a hidden payload, or localize the part that survives editing. These form a forensic ladder, and we ask what each rung costs in the sample length $n$.
> One object organizes the answers. Let $S$ be the secret the mark carries (a user's identity or payload), and let the information profile $ν(t)=I(S;X_t\mid X_{&lt;t})$ record how much the $t$-th token reveals about $S$ given the earlier ones. Its total mass pays for attribution and extraction; how that mass is spread pays for localization; and detection alone is paid for not by information but by presence, the distance from the marked to the unmarked distribution. The literature's two quality models, a mark subtle on every token and one that stamps a few tokens loudly, are two incomparable ways of capping this profile.
> Our main theorem settles the ladder's entropy column. For statistically distortion-free schemes, attributing a text to one of $N$ users costs $Θ(\log N/h)$ tokens over every stationary-ergodic source of entropy rate $h$, sharp to a $(1+o(1))$ factor: to our knowledge the first tight entropy-rate law for multi-user attribution (via exact alignment). The natural collision-counting analysis overcharges without bound; only a decoder thresholding each candidate by its own realized surprisal attains the rate while almost never implicating an innocent user. A matching converse makes the law two-sided, and extraction of an $\ell$-bit payload costs $Θ(\ell/h)$. Two gaps are real, not modeling artifacts: a $Θ(\log N)$-token window in which a text is provably machine-made yet unattributable, and a footprint-resolution uncertainty principle. Experiments on GPT-2, Pythia-410M, and Qwen2.5 recover the predicted constants.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。
