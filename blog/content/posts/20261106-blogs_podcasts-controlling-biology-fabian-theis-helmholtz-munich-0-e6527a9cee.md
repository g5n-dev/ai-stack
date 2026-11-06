---
title: "Controlling Biology - Fabian Theis, Helmholtz Munich"
date: 2026-11-06T23:02:42+08:00
draft: false
entry_kind: "auto"
tags: ["深度学习", "博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:18427a7677787c6725620681c519d4324ace24b284a3687276cde846ac792e7f"
source_payload_sha256: "sha256:a2788a458706eb2e1b8551161552ad5df2327d19a5adbd18d8156654fbfdec2d"
observation_id: obs_e6527a9cee2850cb16fb4bf4c2a03a608877d83a95400d1f4cdcf1196d7f18e2
event_id: evt_e5f56911428699db261e3f57c8bd1ffee2a04d18811592294311f0c54906510d
revision_id: rev_8a68fcb39a983992a1d1e5b0cdf8695338269e5911262da715b09476ea310341
source_published_at: 2026-11-06T14:48:24Z
first_seen_at: 2026-11-06T15:01:40.859086Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 52
interpretation_sha256: "sha256:fb47b2085d3ac57e93141b5fb1eb65f0b1b66256b1ef800b977e290cd97db283"
description: "本文介绍 Fabian Theis 对“虚拟细胞”及其未来发展方向的看法，重点讨论 Biohub 的大规模数据收集、多模态生物数据建模，以及虚拟细胞模型在扰动预测上面临的评测难题。"
external_url: https://latent.space/p/controlling_biology_-_fabian_theis_helmholtz_munich_1
parent_observation_id: null
last_seen_at: 2026-11-06T15:01:40.859086Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://latent.space/p/controlling_biology_-_fabian_theis_helmholtz_munich_1](https://latent.space/p/controlling_biology_-_fabian_theis_helmholtz_munich_1)
- **发布域名**: latent.space

## 要点解读

### 这是什么
本文介绍 Fabian Theis 对“虚拟细胞”及其未来发展方向的看法，重点讨论 Biohub 的大规模数据收集、多模态生物数据建模，以及虚拟细胞模型在扰动预测上面临的评测难题。

### 用在哪里
适用于关注 AI 与生物医学交叉、计算生物学、精准医学的读者，可帮助理解多尺度、多模态数据与实验闭环在该领域的意义。

### 可以推断的
- 推测：虚拟细胞研究的核心挑战，可能正从单一任务的扰动预测转向跨尺度、时序和多模态数据的联合建模。
- 推测：高质量成像、实验室自动化与数据基础设施的成熟，可能成为推进复杂生物模型的重要条件。

## 来源摘要/节选

> Fabian Theis has been one of the key players in the various iterations of the Virtual Cell concept and initiatives. It is not hyperbole at all to say that his lab has been pushing the frontier of algorithms to understand multi-scale, multi-modal (”multiomics”), time-varying biological data.
>
> Indeed, he has shaped the large scale vision and data collection through his leadership at Helmholtz, various startups and probably at Biohub itself.
>
> Much of the recent attention in AI x Bio has been on protein and molecular design. AlphaFold, ESM and BioHub, Chai, Leash, Isomporphic, Boltz, Genesis, Octant, Baker Lab, and many many more. After a lot of initial excitement, Virtual Cell projects have received less attention, due in no small part to questions about the effectiveness of large-scale models in solving even basic Virtual Cell problems.
>
> A $1.8B bet
>
> The Biohub announcement a few weeks ago got a lot of press for the (really) big numbers: $1.8B of commitments[1] from Biohub, NIH, DOE, Google and Meta. The discussion cites new imaging and measurement capabilities, generating large data sets and making the data available for training AI.
>
> https://x.com/biohub/status/2107819946034266562
>
> But why are these organizations doubling down on these big bets now? They have been in the works for years now, what is going on that makes now the moment to push?
>
> New measurement capabilities and scale infrastructure, are now coming online that make Biohub’s push likely lead to big impact on science. DOE and NIH are developing lab-in-the-loop automation capabilities at scale. Google is scaling and broadening its connectomics capabilities ( episode coming soon!). Biohub itself has worked with various labs to develop and improve imaging platforms like laser phase plate microscopy, light sheet microscopy and advanced post-processing for regular microscopes that reveal deep phenotypic data. These technologies are quickly maturing, and will likely play a big part in the Biohub initiative.
>
> Virtual cells struggle
>
> This kind of multi-scale, multi-modal data looks a lot like the data Fabian has made a career out modeling. On the other hand Virtual Cell modeling has run into problems that have dampened excitement about systems biology.
>
> The 2025 Arc Virtual Cell Challenge shined a light on the problem: a slew of papers pointed out that constant baselines (not even linear!) often beat sophisticated models for “Perturbation Prediction”. If you change the inputs or programming of a cell (via gene editing, drugs or other environmental factors), how will the cell change it’s “state”. The disappointing finding is that many models fail to beat even the most basic basic baselines 🤦‍♂️.
>
> The situation is not actually so bad:
>
> https://www.nature.com/articles/s41587-026-03307-w
>
> This excellent paper show that many existing evaluation metrics are poorly calibrated: they can reward an uninformative mean prediction because most genes barely change. With better-calibrated metrics, deep learning models can outperform the mean baseline.
>
> The problem is the problem
>
> Nonetheless, Fabian Theis believes that perturbation prediction under the existing data sets just isn’t a hard enough problem to warrant complex algorithms. Instead we should be focused on exactly the problems that Biohub just announce an $1.8B data collection effort around: using large, high precision, multi-scale, co-registered biological data to predict the evolution of molecules → cells → niches → tissues → organs → organisms, and how all these scales effect one another.
>
> This is a happy situation: at this very moment, AI is enabling us to tackle dramatically larger problems, and this problem is very, very big. We lack understanding of the “scale interfaces” between these different different “domains of applicability,” and we lack the data. The Biohub initiative aims to solve the data problem. Fabian Theis has been working on the algorithms to model these larger problems for years.
>
> https://youtu.be/DLKg78H1wSI
>
> How do the other cells near me change my state? What happens to a distribution of cells from a perturbation? How do I perturb a cell to get it into the state I want?
>
> These are increasingly complex questions that are building towards a lab-in-the-loop and large scale experimentation, and (actually) require increasingly complex models.
>
> Models drive precision medicine
>
> Fabian’s labs and initiatives have been also investing heavily: the Computational Health Center at Helmholtz combines AI, molecular data, medical imaging, genomics, and clinical data to develop predictive and mechanistic models for precision medicine. The Institute of Computational Biology develops statistical and dynamical models integrating biological information from single-cell time series through population-scale omics data.
>
> Given his drivers seat at the frontier, we were so excited for the opportunity to get an hour of his time to understand how Fabian Theis is thinking about Virtual Cells when the concept of what is difficult is changing so quickly.
>
> We also discussed:
>
> The business of Virtual Cells
>
> The Bitter Lesson in biology - our perennial topic
>
> Training the next generation of Computation Biologists
>
> Closing the lab-in-the-loop
>
> https://youtu.be/3nAV2s4GYbs
>
> [1] NIH money is prior investments

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。