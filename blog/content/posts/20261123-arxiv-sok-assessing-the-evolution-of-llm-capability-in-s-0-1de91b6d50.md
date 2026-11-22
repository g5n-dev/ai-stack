---
title: "SoK: Assessing the Evolution of LLM Capability in Software Vulnerability Research"
date: 2026-11-23T03:37:34+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "cs.CR", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:8916bc0a7bc65e76f2102599c9b131c6dd4f2fb05a4b303252cb1ea8bddcdcda"
source_payload_sha256: "sha256:4e34505f1ecf84b690cc75ebe641ab13a9be78a7961c67497345fba6f3dba914"
observation_id: obs_1de91b6d50876f2b92d1483c6fd69ee54a89e4a41e5b90bc3e28d8f075e53e4b
event_id: evt_514431738fce807281077253ffd789775b76716846400492bea2867c8007a6ce
revision_id: rev_a39d843d448b27bff372f990214befc523580470b2d4712728557361169b9ef4
source_published_at: 2026-11-19T18:54:19Z
first_seen_at: 2026-11-22T19:36:12.074967Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 81
interpretation_sha256: "sha256:bc20b0aa0c8df8ad2972a9531535b1808f330f0c7d22e7e223ce255978562b5f"
description: "这是一项系统化梳理研究，用类似自动驾驶级别的自主性框架评估大模型在真实软件漏洞发现、验证和修补中的能力，并按正确性、可用性与证据强度对相关主张分级。研究还分析十年来的公开漏洞记录、公告与利用数据，并评估文献中提出的缓解措施。"
external_url: http://arxiv.org/abs/2611.26601v1
parent_observation_id: null
last_seen_at: 2026-11-22T19:36:12.074967Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2611.26601v1](http://arxiv.org/abs/2611.26601v1)
- **发布域名**: arxiv.org
- **分类**: cs.CR
- **作者**: Amine Lbath、Manan Suri、Aurelien Delaitre 等

## 要点解读

### 这是什么
这是一项系统化梳理研究，用类似自动驾驶级别的自主性框架评估大模型在真实软件漏洞发现、验证和修补中的能力，并按正确性、可用性与证据强度对相关主张分级。研究还分析十年来的公开漏洞记录、公告与利用数据，并评估文献中提出的缓解措施。

### 用在哪里
该框架适用于研究者和厂商比较不同模型与智能体的漏洞研究能力、辨别证据质量，并为不同利益相关方选择缓解方案提供参考。

### 可以推断的
- 推测：统一的自主性分级与证据标准，有助于减少不同来源之间能力声明难以直接比较的问题。
- 推测：若漏洞披露到攻击的间隔暂未明显缩短，自动化发现能力的提升未必会立即转化为更快的攻击响应。

## 来源摘要/节选

> LLM-based agents are becoming increasingly capable at discovering, validating and patching vulnerabilities in real software, and vendors and researchers report that this is already changing how vulnerabilities are found and fixed. These claims, however, are scattered across papers, vendor reports and disclosures and are rarely comparable. We introduce a framework that rates these capabilities on an autonomy scale modeled on the levels of driving automation, and qualifies each claim by its correctness, its availability and the strength of its evidence. We use this framework to systematize the published evidence on LLM capability in vulnerability research. We find that agents discovered, validated, and patched vulnerabilities in real-world software without human intervention before the restricted frontier models of 2026, and that open-weight models subsequently attained comparable autonomy for discovery and validation. We then measure the consequences of evolving LLM security capabilities in a decade of public vulnerability records, advisories and exploitation data. In 2026 the number of disclosed vulnerabilities more than doubled, with an increasing share rated critical or high, and severe bugs that had survived a decade or more in widely used code were reported several times more often than before. Yet the time between the stages of a vulnerability's life, from report to fix and from disclosure to attack, has not shifted noticeably so far. We grade the mitigations proposed in the literature with an explicit rubric and draw guidance for each group of stakeholders from the best-supported ones.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。