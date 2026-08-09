---
title: "Does FLAIR super-resolution erase or hallucinate small white-matter lesions?"
date: 2026-08-08T05:00:55+08:00
draft: false
entry_kind: "auto"
tags: ["计算机视觉", "cs.CV", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:52ee111475d7d06a0daf8dedc883e34ad5a9d57cf665b8b5478034983cc859a8"
source_payload_sha256: "sha256:38d72a9e9cb0a7e47f99c2315f3064724cad3ead2452077a363c69df178decf6"
observation_id: obs_7611c224c88462815709bb99d5fde8b54adc3a1c8d2b58bba0a8122443e34847
event_id: evt_c8fc0d5b47bb04e7bef976cc377816e388b443b3441e9ba9e106450dce1ec362
revision_id: rev_2d793ef62c5849ae1378748036d6736d5d578d74ed8b412aced125048982eb38
source_published_at: 2026-08-06T17:26:01Z
first_seen_at: 2026-08-07T21:10:11Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 76
interpretation_sha256: "sha256:c489b791d535ce42bf12a32f359daff7d7e71180c220340093cef45c2cc2bc49"
description: "该研究评估在厚层FLAIR影像上使用超分辨率重建是否会导致小量白质高信号区被遗漏或误判，并通过对比不同插值与自监督模型对病灶检测的影响。"
external_url: http://arxiv.org/abs/2608.06311v1
parent_observation_id: null
last_seen_at: 2026-08-09T00:00:00Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.06311v1](http://arxiv.org/abs/2608.06311v1)
- **发布域名**: arxiv.org
- **分类**: cs.CV
- **作者**: Zahra Khodakarami、Yue Li、Pulkit Khandelwal 等

## 要点解读

### 这是什么
该研究评估在厚层FLAIR影像上使用超分辨率重建是否会导致小量白质高信号区被遗漏或误判，并通过对比不同插值与自监督模型对病灶检测的影响。

### 用在哪里
适用于神经影像预处理流水线、影像分割算法评估或临床影像质量改进的科研与技术人员，尤其在需要从低分辨率临床扫描恢复细节时参考。

### 可以推断的
推测：随着原始扫描层厚增大，超分辨率导致小病灶信号被抹除的风险可能升高，实际应用时需关注切片厚度的选择。  
推测：在保持细粒度结构方面，单对比自监督模型可能优于基于多对比的隐式神经表示，这一特性或可在缺乏配对高分辨率数据的场景中提升分割鲁棒性。

## 来源摘要/节选

> White matter hyperintensities (WMH), bright regions on Fluid-attenuated Inversion Recovery (FLAIR) scans are associated with cerebrovascular pathology and neurodegeneration. FLAIR is usually acquired with thick slices in clinical settings, giving it poor through-plane resolution. Super-resolution (SR) is a widely used method for recovering an isotropic volume from an anisotropic scan. Yet whether applying it prior to WMH segmentation preserves lesion content remains unknown: a model may erase small real lesions or hallucinate absent ones. We used 1-mm isotropic high-resolution (HR) FLAIR scans from 29 individuals in the ADNI cohort, each manually segmented for WMH by an expert. Then, we degraded each to simulated 3 and 5 mm through-plane acquisitions. Multi-contrast implicit neural representation (INR), a single-contrast self-supervised model (ECLARE), and cubic interpolation were used to upsample them onto the HR grid. WMH segmentation from a simulated thick slice and the original HR FLAIR set the floor and ceiling, respectively, for the per-lesion analysis. Of four WMH segmentation methods (WMH-SynthSeg, segcsvd, MARS-WMH, TrUE-Net), we ran the analysis under the most sensitive one to small lesions on HR (MARS-WMH) with the evaluation metrics of detection sensitivity, erasure rate (HR-detected lesions lost after reconstruction), and hallucination rate (predicted components absent from both the manual and HR segmentation). The dominant effect of SR was erasure of small real lesions, not hallucination, and it increased with slice thickness, though every reconstruction still improved lesion detection over the raw thick slice. ECLARE recovered small lesion signal best at both thicknesses, while the INR was no better than cubic interpolation.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。