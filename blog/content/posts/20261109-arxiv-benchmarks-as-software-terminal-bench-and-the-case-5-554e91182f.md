---
title: "Benchmarks as Software: Terminal-Bench and the Case for Continuous Benchmarks"
date: 2026-11-09T08:53:27+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "cs.AI", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:a45dff20c61e6f1342401b1cab66d778a06620125218e8d96e920f3664689ff9"
source_payload_sha256: "sha256:be6a145c479de75a03c41ea08b00d58780e430cc3eac29c5bb1590831cce4c18"
observation_id: obs_554e91182f04f9cb418bf145542d289d389ae347adfd9a24d1840e1d67e62fa3
event_id: evt_268a9176bddcc441740e381c3ce10e121fbc6387dae6c8721dd94327fec0b5ec
revision_id: rev_9315af885eef9a666514975654d01fba9dee32713fc42064bc46496d02e3cd52
source_published_at: 2026-11-05T18:18:39Z
first_seen_at: 2026-11-09T00:52:32.750192Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 77
interpretation_sha256: "sha256:8732999da16871c9832a992b6ed5d8d9c90f8f079ec534b449ccbe5ac6f8925e"
description: "这项工作提出“持续验证”流程，通过社区反馈、任务产物、代理轨迹、自动检查和人工审核，持续维护智能体基准。研究对 Terminal-Bench 2.0 的审计发现约 30% 的任务存在问题，修复后形成 2.1 版；结果准确率提高超过 10 个百分点，榜单名次最多变化三位。"
external_url: http://arxiv.org/abs/2611.08417v1
parent_observation_id: null
last_seen_at: 2026-11-09T00:52:32.750192Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2611.08417v1](http://arxiv.org/abs/2611.08417v1)
- **发布域名**: arxiv.org
- **分类**: cs.AI
- **作者**: E. Kelly Buchanan、Crystal Zhou、Scott W. Linderman 等

## 要点解读

### 这是什么
这项工作提出“持续验证”流程，通过社区反馈、任务产物、代理轨迹、自动检查和人工审核，持续维护智能体基准。研究对 Terminal-Bench 2.0 的审计发现约 30% 的任务存在问题，修复后形成 2.1 版；结果准确率提高超过 10 个百分点，榜单名次最多变化三位。

### 用在哪里
适用于设计和维护面向编程智能体的评测基准，尤其适合需要判断模型真实能力、比较不同模型表现或制定稳定排行榜的团队。评估配置时，也应把时间等资源预算作为需要持续校验的测量条件。

### 可以推断的
- 推测：随着模型能力提升，固定不变的评测任务和验证器可能逐渐失真，基准维护应成为持续工作而非一次性发布流程。
- 推测：在比较智能体性能时，若资源预算不同，榜单结果可能反映测量条件差异，而不完全代表模型能力差异。

## 来源摘要/节选

> Coding agents are among the most economically consequential deployments of LLMs to date, making reliable evaluation increasingly important. Yet even benchmarks that are carefully validated at release can become stale. As models improve, they can discover valid solutions that existing verifiers reject, while changes to evaluation infrastructure can invalidate assumptions embedded in tasks and tests. We call the resulting accumulation of defects benchmark maintenance debt: a growing gap between benchmark scores and the capabilities they are intended to measure. We introduce a continuous-validation workflow for agentic benchmarks that combines community reports, task artifacts, agent traces, automated oracle checks, and human-gated repairs. We apply this workflow to Terminal-Bench 2.0, a benchmark that underwent extensive human and LM-assisted review and red-teaming before release. Our audit identifies issues in roughly 30% of the benchmark, and we release the resulting repairs as Terminal-Bench 2.1. These repairs change evaluation results: accuracy increased by over 10 percentage points and leaderboard positions move by up to three ranks, even as the overall ranking remains highly correlated (Spearman rho = 0.958).
> We evaluate how resource allocation shapes benchmark conclusions. We show that fixed wall-clock can materially change agent performance: For example, extending the time limit closes a 20pp harness gap on GPT 5.4 and shrinks a 30 pp gap on GPT 5.4 mini to 5 pp. Benchmark maintenance is therefore not only about repairing task artifacts: resource budgets are part of the measurement specification and must be validated alongside the tasks themselves.
> More broadly, benchmark maintenance debt is not just accumulated implementation bugs: our results show that as models improve, both evaluation assumptions and resource settings may need to be revalidated.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。