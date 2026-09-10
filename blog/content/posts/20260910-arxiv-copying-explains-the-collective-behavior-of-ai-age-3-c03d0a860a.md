---
title: "Copying explains the collective behavior of AI agents in the wild"
date: 2026-09-10T05:44:48+08:00
draft: false
entry_kind: "auto"
tags: ["AI Agent", "cs.MA", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:7bdab92cb571c4ae547452f4aa275fe83d2cd00ff6c5a0bf4b44c93335557366"
source_payload_sha256: "sha256:8ea6306cb1b04b9f4c40d6f96ee63438ee542ac2cb29298ce4055c6a5e7063c5"
observation_id: obs_c03d0a860a609f6071c68df99b9cc2f2878b5f96641d1a1243e5806cb9237abb
event_id: evt_939573c6019e133c0a320af9b60c02d03f019cbd0f3e9d5fa81cf1a711f63238
revision_id: rev_099043872430d9a3dcdf9bbce625842fd88dea831694a4be6350c4be6aa8c5de
source_published_at: 2026-09-08T17:59:20Z
first_seen_at: 2026-09-09T21:55:39Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 65
interpretation_sha256: "sha256:3bb226bcf8232db7aea1ff762a263c9a60a3a1813a61e1eee09feec9fb303a3b"
description: "该研究通过公开的编辑日志分析了大量 AI 代理在共享百科页面上进行写入的行为，发现代理几乎完全依赖环境中已出现的内容来选择写入位置、自己名称以及消息措辞。"
external_url: http://arxiv.org/abs/2609.09150v1
parent_observation_id: null
last_seen_at: 2026-09-10T00:00:00Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.09150v1](http://arxiv.org/abs/2609.09150v1)
- **发布域名**: arxiv.org
- **分类**: cs.MA
- **作者**: Giordano De Marzo、Nicola Alboré、David Garcia

## 要点解读

### 这是什么  
该研究通过公开的编辑日志分析了大量 AI 代理在共享百科页面上进行写入的行为，发现代理几乎完全依赖环境中已出现的内容来选择写入位置、自己名称以及消息措辞。  

### 用在哪里  
适用于研究人工代理群体行为、研究多代理系统的协作机制，或为平台设计者提供对代理行为模式的参考。  

### 可以推断的  
推测：基于复制规则的代理对先行出现的内容产生强烈依赖，后续加入的代理很少自行改变已有惯例。  
推测：在实时环境中调整内容呈现顺序或引入变化，可能会显著改变代理的集体分布特征。

## 来源摘要/节选

> In June 2026, thousands of AI agents found that a small public wiki would accept edits from inside their sandboxes, and started using it to help one another pass a timed test. Each agent lived for about an hour and remembered nothing afterwards. Nobody asked them to cooperate, and the wiki had not been built for them. The complete record of what they wrote is public, and it is unusually informative, because it preserves not only what each agent wrote but what that agent could see before writing. We use it to follow the three decisions an agent had to make on arrival: where to write, what to call itself, and how to word its message. One rule governs all three. An agent takes an option with a probability close to the share of that option in what it can see, and the share that matters is the one on the page in front of it, then the one in the stream of recent edits, and only weakly anything older. Three minimal copying models, one per decision and with a single free parameter each, reproduce the heavy-tailed distribution of how many agents met on a page, the frequency of the pieces from which the agents built their names, and the patchwork of pages that are internally consistent and different from one another. Copying whatever the environment happens to show is enough to produce most of the collective structure of this population. It is also what makes such a population easy to steer, since whoever writes first, or writes while the others are quiet, sets the convention for everyone who comes later.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。