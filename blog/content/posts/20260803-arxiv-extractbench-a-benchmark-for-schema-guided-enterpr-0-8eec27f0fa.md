---
title: "ExtractBench: A Benchmark for Schema-Guided Enterprise Document Extraction"
date: 2026-08-03T23:17:13+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "cs.AI", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:d50b66500247a873017bb7856f500fec590bf8dc1b26a3481cbee487309bea06"
source_payload_sha256: "sha256:c2cf16320ebc57f2ac23080013cade42be9d8c9aa4faf3101d2971238408ddff"
observation_id: obs_8eec27f0fabdee08b466df478818c884bd4927a69d74f9d3d380fa294b70bc66
event_id: evt_c02871e5ba83f612edbf4c3ce290cb62421ecb84363647cc077e65df6f05aadc
revision_id: rev_419c901a57f8188483ef4a065caae36210a57727712a90ba176f31dfdfec1115
source_published_at: 2026-07-31T17:55:58Z
first_seen_at: 2026-08-03T15:15:07.203309Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 74
interpretation_sha256: "sha256:da1ceca5695e0725277f5fd0701a383395b4e6c2d8d9666a5776fedd19a0bb2c"
description: "这是一个针对企业文档的模式引导提取任务的基准测试，用于评估系统在值准确性、记录完整性、溯源可信度以及运行成本等多个维度的表现。"
external_url: http://arxiv.org/abs/2607.29677v1
parent_observation_id: null
last_seen_at: 2026-08-03T15:15:07.203309Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2607.29677v1](http://arxiv.org/abs/2607.29677v1)
- **发布域名**: arxiv.org
- **分类**: cs.AI
- **作者**: Boyang Zhang、Adrian Lyjak、Eli Stewart 等

## 要点解读

### 这是什么
这是一个针对企业文档的模式引导提取任务的基准测试，用于评估系统在值准确性、记录完整性、溯源可信度以及运行成本等多个维度的表现。

### 用在哪里
适合企业在搭建自动文档处理流程时对比不同模型的实际效果，也适合研究人员检验新方法在大规模真实文档上的性能。

### 可以推断的
推测：在实际业务中，处理页数较多的文档时，系统可能出现信息截断或遗漏记录的情况。  
推测：企业在选择提取方案时，除了关注准确率外，运行成本也会成为重要考量因素。

## 来源摘要/节选

> Enterprise workflows increasingly rely on agents for \emph{schema-guided extraction}: given a document and a user-defined schema, the agent faithfully follows the schema to produce the correct output with source evidence as grounding metadata. We present ExtractBench, a benchmark for schema-guided extraction and, to our knowledge, the first to score value accuracy, record completeness at scale, grounding, and measured cost together. The evaluation system contains 4,869 pages across 370 enterprise documents, 8 business domains, and 67 document types, with clear tags differentiating their challenge scenarios. The scalable schema and ground-truth curation pipeline combines independent-system agreement for real documents, known values for synthetic lists, and human verification for forms. We report order-insensitive value F1 for value accuracy, plus two grounding metrics for source traceability: word- and page-level F1. Commercial VLMs perform well on short documents but often truncate record lists on long ones, while coding agents retain higher accuracy at much higher cost. LlamaExtract Agentic Plus ranks first on all three metrics, with accuracy comparable to coding agents at a fraction of the cost. Dataset and evaluation code are available on \href{https://huggingface.co/datasets/llamaindex/ExtractBench}{HuggingFace} and \href{https://github.com/run-llama/ExtractBench}{GitHub}.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。