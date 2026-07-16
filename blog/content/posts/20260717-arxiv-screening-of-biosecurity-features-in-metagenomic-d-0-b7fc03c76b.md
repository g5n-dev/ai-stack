---
title: "Screening of Biosecurity Features in Metagenomic Data with Evo 2 Probes"
date: 2026-07-17T04:15:17+08:00
draft: false
entry_kind: "auto"
tags: ["q-bio.GN", "arXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:fab2a475bb54d51f0ed05098fa16306e81cae43203bfffb565057220719c01a3"
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 71
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2607.14070v1
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2607.14070v1](http://arxiv.org/abs/2607.14070v1)

## 来源摘要/节选

> Genomic foundation models such as Evo 2 learn rich sequence representations, but their value for biosecurity screening is largely unexplored. We ask how much biosecurity-relevant signal is linearly accessible in these representations by training minimal linear and attention probes on frozen Evo 2 layer-26 activations, without fine-tuning the underlying model. Across held-out metagenomic test sets, the probes detect antimicrobial resistance (AMR) with strong discrimination: a linear probe reaches a region-level ROC-AUC of 0.888 (mean-pool), rising to 0.977 with a single-head attention probe. The probes resolve finer-grained AMR drug-class subcategories and separate them from unrelated functional genes, providing additional evidence that the learned signal is not explained solely by generic functional-gene status. Bacterial virulence is also decodable, though more weakly (region-level ROC-AUC 0.833). The AMR probe retains comparable ranking performance on simulated short reads without retraining, enabling evaluation before assembly in settings where assembly is computationally costly or unreliable. It achieves a read-level ROC-AUC of 0.898 (mean-pool), comparable to the mean-pooled full-region result. Within SynGenome, AMR-associated prompt labels are only weakly recoverable from Evo 1.5-generated sequences; these prompt-derived labels do not establish the function of the generated response sequences. A complementary sparse-autoencoder analysis recovers interpretable resistance-associated features but proves less consistent than the supervised probes. Together, these results position lightweight embedding-based probes as a fast, inexpensive first-pass detection layer for metagenomic biosurveillance and map both strengths and current limits of the approach. This work was conducted as part of the AIxBio Hackathon 2026 hosted by BlueDot Impact, Apart Research, and Cambridge Biosecurity Hub.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。