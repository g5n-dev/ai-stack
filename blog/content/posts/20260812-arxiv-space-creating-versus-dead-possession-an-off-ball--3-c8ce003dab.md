---
title: "Space-Creating versus Dead Possession: An Off-Ball Possession-Quality Index for Broadcast Football"
date: 2026-08-12T00:15:31+08:00
draft: false
entry_kind: "auto"
tags: ["计算机视觉", "cs.CV", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:b794ca9815d6db8c63b5a5ef1bf80c28668a2a3997a2782109f1916c51850403"
source_payload_sha256: "sha256:8b29512377848c88ebaaf48156c15b548b5861fd76c02fe0c8a670a10913b464"
observation_id: obs_c8ce003dabf06f7af132bc804287c88ed970f5a6008102645f27b805e6576a8a
event_id: evt_bb576f4b0c1fc6312edab3719ab5b9975e27957ed2c1336e3b2e403ce95b395e
revision_id: rev_b86c7579673fa870e67df6e09c30225aca6d600cec0dbfa4423fb065a183eded
source_published_at: 2026-08-10T17:39:05Z
first_seen_at: 2026-08-11T16:12:46.918040Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 98
interpretation_sha256: "sha256:5fad65df3c7e1991ce6281be656182cf3b46b7f525e65e3b65df1b2b8211a10a"
description: "提出一种两层评估框架：先在事件层面识别低威胁持球序列（垃圾持球），随后利用视频投影得到空间创造指数，区分产生空间与无效持球。"
external_url: http://arxiv.org/abs/2608.09887v1
parent_observation_id: null
last_seen_at: 2026-08-11T16:12:46.918040Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.09887v1](http://arxiv.org/abs/2608.09887v1)
- **发布域名**: arxiv.org
- **分类**: cs.CV
- **作者**: Seongjin Choi

## 要点解读

### 这是什么  
提出一种两层评估框架：先在事件层面识别低威胁持球序列（垃圾持球），随后利用视频投影得到空间创造指数，区分产生空间与无效持球。

### 用在哪里  
适用于赛后战术分析、球队表现评估以及教练在进攻策略调整中参考，可帮助区分持球率高但未制造威胁的情况。

### 可以推断的  
推测：若球队大量出现垃圾持球标记，可能意味着其进攻方式偏向保守或缺乏有效空间渗透。  
推测：该方法需要视频坐标映射，成本较高，难以在实时转播中直接应用。

## 来源摘要/节选

> Ball possession is the most-cited and most-misleading number in football: 60% recycled in one's own half is not 60% spent pinning the opponent back. Existing event-based possession-value frameworks (expected threat, VAEP, on-ball value) price on-ball actions but ignore the off-ball question a sterile possession poses: did holding the ball create space, or was the circulation dead? We answer this in two layers. First, an event-side junk-possession index prices each possession sequence by its peak threat gain under an expected-threat grid and -- after reconstructing the live scoreline to exclude lead-protecting circulation -- flags low-threat sequences in tied-or-losing states. On the 2026 FIFA World Cup (103 matches, 206 team-matches) the flag correlates negatively with points (r=-0.37) and xG difference (r=-0.51, partly index-coupled). It is not a repackaging of on-ball value: with team offensive VAEP and field tilt held fixed, the junk flag stays strongly negatively associated with points (p&lt;0.0001, also match-clustered) while VAEP is not significant -- in this same-match (descriptive) regression it adds information beyond this on-ball action-value model. Second, for a flagged window we resolve whether it was spatially dead or space-creating by projecting broadcast video to pitch coordinates and measuring a Space-Creation Index (SCI): a net pitch-control change capturing whether the possession seized space or pushed the opponent's block back. Across 31 of 35 flagged windows from nine World Cup matches (a purposive sample), 74% are spatially non-space-creating, 19% weak progression, and 6% space-creating windows the event flag alone would score as failure -- including a side with 73% of the ball that exited on penalties (two non-creating windows). The two layers separate space-creating-but-unconverted from sterile possession, a distinction event-only on-ball value cannot make.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。