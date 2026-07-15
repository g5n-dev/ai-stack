---
title: "Watermark Forensics for Generative Models: An Informati"
date: 2026-07-15T23:05:07+08:00
draft: false
entry_kind: "auto"
tags: ["cs.CR", "arXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:cf3cf00c5341ab396fb6524b6aacb1cc3c10d8b7ddbb4af91fea4da9508df3ae"
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_is_truncated: false
source_support: 1.0
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2607.13003v1
---

# Watermark Forensics for Generative Models: An Informati

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