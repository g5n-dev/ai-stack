---
title: "BrowserForge: Scaling Web Episode via Parallel Browser Sandboxes"
date: 2026-08-26T16:01:27+08:00
draft: false
entry_kind: "auto"
tags: ["AI Agent", "cs.CL", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:b0258d90fe296ed9ce65d113ffb51bd04b53470d8dbd6112578455b2c427564d"
source_payload_sha256: "sha256:0d2180e9b1b0c3ae20e32b0b597dc209e363551aaa5031c98504ef08314979a6"
observation_id: obs_5b0f6af26ec4c9eec41e835a69517315307fe06a7c20c81d32e5ea1364796426
event_id: evt_1d68843ff3beb03bf718cc7e5401a424a7865cad328efa71fb41d2f2c415a352
revision_id: rev_d46add5042bb295a84a8b91ae550da2e71b42fef96e8993c74a0eb738da5e30c
source_published_at: 2026-08-25T17:35:42Z
first_seen_at: 2026-08-26T17:00:02.558076Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 64
interpretation_sha256: "sha256:8d6f81ff42df1f735187cad5a10ecbad8b87ee8de718e0449712e005b83c6eab"
description: "该工作提出一种框架，利用并行浏览器沙箱在开放网络中批量生成网页交互轨迹，以获取大量多样化的训练数据。"
external_url: http://arxiv.org/abs/2608.24848v1
parent_observation_id: null
last_seen_at: 2026-08-26T07:59:10.941790Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.24848v1](http://arxiv.org/abs/2608.24848v1)
- **发布域名**: arxiv.org
- **分类**: cs.CL
- **作者**: Fei Tang、Huawen Shen、Zhiqiong Lu 等

## 要点解读

### 这是什么
该工作提出一种框架，利用并行浏览器沙箱在开放网络中批量生成网页交互轨迹，以获取大量多样化的训练数据。

### 用在哪里
适用于需要训练基于视觉的网页代理、且对交互轨迹的规模和质量有较高要求的研究项目或工程团队。

### 可以推断的
推测：该框架生成的数据规模大幅提升后，代理在未见网站上的成功率可能会得到显著改善。  
推测：在实际部署时，需要调度大量并发浏览器实例，对计算资源和任务调度系统提出较高要求。

## 来源摘要/节选

> Web agents that act from rendered pixels avoid the fragility and heavy token cost of reading a page's HTML or accessibility tree, but training them depends on large amounts of high-quality interaction trajectories, and how to produce such data at scale remains an open problem. Public datasets typically contain only a few thousand trajectories drawn from a fixed and narrow set of websites, and even recent automated synthesis pipelines stay bound to predefined site lists or tutorial sources, so the number of distinct websites the agent ever sees barely grows. We present BrowserForge, a framework that generates web interaction data at scale by driving many browser sandboxes in parallel over the open web. BrowserForge couples three components: an open-web sourcing stage that exposes the agent to hundreds of thousands of real, openly reachable websites; a sandbox cluster manager that schedules hundreds of concurrent browsers with high utilization; and a Proposer-Solver dual-agent loop that turns a raw page into an executable task and then collects a verified trajectory for it. A rule-plus-model cleaning pipeline removes failed runs and rewrites the surviving reasoning into a single unified chain-of-thought style. Page structure such as the accessibility tree is used only as a synthesis-time signal; the agent we train and release acts purely from the screenshot. The resulting corpus contains 203,238 trajectories, each collected from a distinct website, larger and more diverse than prior trajectory datasets. Fine-tuning a compact multimodal model on this corpus raises its success rate on the live Online-Mind2Web from 25.66% to 33.33% and consistently improves step accuracy on the static Multimodal-Mind2Web, with the gain growing as the corpus scales. Controlled analyses further confirm that open-web sourcing and broad website coverage are key contributors to the observed improvement.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。