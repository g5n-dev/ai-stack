---
title: "$π\\mathbf{R}^2$: Reactive Real-time Flow Policies"
date: 2026-07-29T11:41:31+08:00
draft: false
entry_kind: "auto"
tags: ["生成式 AI", "cs.RO", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:7da543a71b1662c5eb39cc9fffed38571fdfb1d764e8a70c012121cadbd3c057"
source_payload_sha256: "sha256:fe331ecc1f47d6ffd82684ff58fbf7521732c907a1af4f263a450aeef579aac0"
observation_id: obs_7e5f82b8d38001147abde3031acf65b44c4a8516f50791a7563cbb894447c8ed
event_id: evt_b56a6b01e856750098279deec3a79e9ea90708c70230a6385cd3826fd6af29a4
revision_id: rev_f86704d488657d9d15d0c7cc844ffa74a77064029cafddc4341dd63d514ae422
source_published_at: 2026-07-28T17:59:31Z
first_seen_at: 2026-07-29T03:40:05.819393Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 49
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2607.26055v1
parent_observation_id: null
last_seen_at: 2026-07-29T03:40:05.819393Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2607.26055v1](http://arxiv.org/abs/2607.26055v1)

## 来源摘要/节选

> Generalist manipulation policies increasingly take the form of action-chunking flow policies built on large pretrained backbones. Such chunks run open-loop, so the policy cannot react to sensory input arriving mid-execution, sacrificing \emph{reactivity}. Replanning more often would restore it, but the perception-to-action pipeline (a large backbone plus multiple denoising steps) is too slow: this \emph{latency} forbids frequent replanning and leaves committed actions stale, making such policies ill-suited for dynamic, closed-loop control. We present $π\mathbf{R}^2$, which makes these policies reactive and real-time while retaining large backbones, expressive multi-modal policies, and multi-action prediction. Built on the per-position noise schedule of diffusion forcing, $π\mathbf{R}^2$ contributes two ideas. First, it splits conditioning into a fast channel (proprioception, fresh every tick) and an asynchronously updated slow channel (vision-language features), so the policy reacts to proprioception within a chunk while tolerating stale vision. Second, a latency-adaptive flow schedule treats in-flight actions as inpainting conditioning and emits actions in one denoising step per call, letting one trained model adapt to varying hardware latency. Requiring minimal modification to existing architectures, $π\mathbf{R}^2$ can be finetuned from a pretrained policy: applied to GR00T-N1.7 on a real xArm6+XHand platform, it replans closed-loop roughly $4\times$ faster than the base policy (~$25$Hz on an A5000 GPU), acting on a fresh observation every $40$ms. Across simulation and real-world manipulation tasks, $π\mathbf{R}^2$ improves the success rate by up to $23\%$ in simulation and $30\%$ in the real world over the strongest baseline. Project page: https://pi-r2-flow.github.io/

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。