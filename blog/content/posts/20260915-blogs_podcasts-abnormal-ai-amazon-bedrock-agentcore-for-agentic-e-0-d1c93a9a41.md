---
title: "Abnormal AI: Amazon Bedrock AgentCore for agentic email security at scale"
date: 2026-09-15T06:33:03+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "生成式 AI", "机器学习", "深度学习", "Prompt 工程", "Advanced (300)", "Amazon Bedrock AgentCore"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:6149c678d3bd63c22c84f249c73f2ffbd1754ac9b615b21bcfecf22d0ee59991"
source_payload_sha256: "sha256:e7635d5233420a3b1ad2408d835f39252c3a7b19d8376d401ac76e9da4766bee"
observation_id: obs_d1c93a9a4173c0b28918d3112f7fd3c28bf7b7db15700155a6cac479db0c87d4
event_id: evt_851eced6dd5333dd8cbd96920b1425348242118d4905288c994297525c5c829b
revision_id: rev_198f147d6834be1c6ed79cd90854db54a55ca1ba18337ce39037b0729471155d
source_published_at: 2026-09-14T21:22:45Z
first_seen_at: 2026-09-14T22:30:52.086645Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 73
interpretation_sha256: "sha256:123d5f4cd1f79a19525a0d028f46a5827d7e3d0388141d770e64840339dd964d"
description: "该内容介绍了一种将动态代码执行能力集成到 AI 代理中的方案，使代理能够执行计算、数据处理和验证等超出语义推理范围的任务，并展示了在邮件安全检测场景中的实际应用架构。"
external_url: https://aws.amazon.com/blogs/machine-learning/abnormal-ai-amazon-bedrock-agentcore-for-agentic-email-security-at-scale
parent_observation_id: null
last_seen_at: 2026-09-14T22:30:52.086645Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/abnormal-ai-amazon-bedrock-agentcore-for-agentic-email-security-at-scale](https://aws.amazon.com/blogs/machine-learning/abnormal-ai-amazon-bedrock-agentcore-for-agentic-email-security-at-scale)
- **发布域名**: aws.amazon.com

## 要点解读

### 这是什么
该内容介绍了一种将动态代码执行能力集成到 AI 代理中的方案，使代理能够执行计算、数据处理和验证等超出语义推理范围的任务，并展示了在邮件安全检测场景中的实际应用架构。

### 用在哪里
适用于需要构建多层检测流程的系统，尤其是在处理大量数据时需要将简单分类、机器学习分析和需要深度推理的复杂判断分阶段进行的场景。

### 可以推断的
推测：该方案的实现思路在需要实时处理大量数据的领域具有通用性，其他面临类似规模压力的安全产品可能也会采用类似的分层架构来平衡成本与检测深度。

推测：批量分析代理的存在表明，在实际部署中，不仅需要实时响应机制，还需要周期性地从历史数据中提取模式并反哺模型，这种人机协同的闭环设计可能会成为 AI 安全产品的常见模式。

## 来源摘要/节选

> AI agents now run in production at a scale of billions of operations a day, and a recurring architectural pattern has surfaced: agents need a compute scratch pad. Not only for coding tasks, but for data aggregation, analysis, verification, and any workflow where semantic reasoning alone isn’t enough.
>
> Abnormal AI, a behavioral security service that protects more than 25 percent of the Fortune 500, has deployed Amazon Bedrock AgentCore Code Interpreter, a capability of Amazon Bedrock AgentCore. Abnormal AI uses it for the agents that support its real-time inline email threat detection. These systems run in production today, processing billions of messages and executing agent-driven code at that same scale to detect and block threats inline, before they reach the inbox.
>
> This work is part of how Abnormal AI builds software. Today, 80 percent of their code changes are built using an agent in some way, and 40 percent are built end-to-end by a background agent (fully AI built, not AI assisted). Their use of AgentCore Code Interpreter for threat detection reflects the same AI-native approach applied to their production runtime.
>
> In this post, we share how Abnormal AI architected these systems, the design decisions behind their sandbox approach, and practical lessons for builders deploying Code Interpreter at scale.
>
> What is Amazon Bedrock AgentCore Code Interpreter?
>
> Amazon Bedrock AgentCore Code Interpreter provides a fully managed, serverless runtime for agents to execute code dynamically. Key characteristics include:
>
> Ephemeral MicroVM sessions: configurable time-to-live from 15 minutes (default) up to 8 hours for long-running tasks.
>
> Security: sessions run in secure sandboxes with full separation at the host operating system level, designed to help prevent inadvertent disclosure between sessions.
>
> Flexible networking: configurable for sandbox virtual private cloud (VPC) mode, or public internet access.
>
> File handling: up to 100 MB through the API directly, or connect to Amazon Simple Storage Service (Amazon S3) for larger datasets.
>
> Preloaded runtimes: Python and Node.js environments with common visualization, statistics, and data processing libraries.
>
> Built-in observability: logs sent to Amazon CloudWatch and AWS CloudTrail for monitoring.
>
> Critically, Code Interpreter is exposed as an API. This means it doesn’t dictate the agent’s workflow. Instead, it provides a box where the agent can run commands, upload files, and retrieve results. For teams with existing agent infrastructure, this plug-and-play design makes the integration straightforward.
>
> Figure 1: Amazon Bedrock AgentCore Code Interpreter architecture, where the agent invokes the Code Interpreter API to provision an ephemeral MicroVM sandbox session for code execution, file input and output, and result retrieval
>
> Why agents need a compute scratch pad
>
> Large language models (LLMs) excel at reasoning and semantic coherence, but many real-world operations don’t map to semantic reasoning:
>
> Basic math and counting: “How many phishing email did we detect in the past hour?” requires computation, not language generation.
>
> Data processing and visualization: transforming raw data into charts, PDFs, or structured reports.
>
> Code verification: running unit tests, linting, and integration tests to validate agent-generated outputs.
>
> By pairing a large language model with Code Interpreter, you enhance the agent’s capabilities beyond what reasoning alone can achieve.
>
> “Pretty much any agent, whether it’s writing code or not, needs a code interpreter sandbox that allows it to actually crunch data and come to answers.”
>
> — Shrivu Shankar, VP of AI Strategy, Abnormal AI
>
> Abnormal AI’s architecture: Three-tiered detection at billion-message scale
>
> Abnormal AI processes billions of email messages through a three-tiered detection architecture, as shown in Figure 2.
>
> Figure 2: Abnormal AI’s three-tiered email detection pipeline, with Tier 1 (heuristics, billions/day), Tier 2 (machine learning models, millions/day), and Tier 3 (inline agents with Code Interpreter, tens of thousands/day), where each tier handles progressively harder cases that the previous tier was unconfident about
>
> Tier 1 — high-volume lightweight classification (billions/day)
>
> Small models, heuristic rules, and lightweight classifiers (logistic regressions) handle the largest volume of traffic. At this scale, it’s both cost-prohibitive to run larger models and unnecessary. Most messages can be classified without deep analysis.
>
> Tier 2 — medium models for uncertain cases (millions/day)
>
> Messages that Tier 1 is unconfident about flow into deep learning and machine learning (ML) models that perform more behavioral signal analysis.
>
> Tier 3 — inline agents with Code Interpreter (tens of thousands/day)
>
> The hardest cases, which would typically require a human analyst to evaluate, are processed by inline agents. These agents receive the threat intelligence data and use a sandbox to analyze it, writing scripts dynamically. They then evaluate how it fits into the overall behavioral model and make a determination. Misclassifications are handled by a separate system that learns and improves the system. A variety of monitoring systems verify the live system.
>
> The analyst agent — batch intelligence
>
> Beyond the real-time classification pipeline shown in Figure 2, Abnormal deploys an analyst agent that operates in batch mode (Figure 3):
>
> Ingests misclassifications and tuning signals from its detection pipeline.
>
> Identifies patterns and trends across large message sets.
>
> Autonomously writes draft candidate heuristics for Tier 1, operating on Abnormal AI’s own detection-pipeline features and signals.
>
> Improved models for Tier 2.
>
> Runs on the scale of approximately 100 batch jobs per week.
>
> Figure 3: The analyst agent feedback loop, where the batch agent ingests misclassifications from the real-time pipeline, analyzes patterns using Code Interpreter sessions, and feeds improved heuristics and models back into Tier 1 and Tier 2
>
> These batch jobs can run for more than 30 minutes with Code Interpreter sessions maintained throughout. They can also span day-long operations where the agent uses Code Interpreter intermittently. For example, it runs a session, trains a model externally, then re-invokes Code Interpreter to process the result.
>
> Security: Zero-trust sandbox design
>
> Abnormal chose the sandbox (no egress) configuration for Code Interpreter driven by two considerations:
>
> Reproducibility – Because the sandbox has no external network access, nothing outside Abnormal AI’s control can influence the agent’s behavior during that session. The environment is designed to be fully deterministic.
>
> Data exfiltration prevention – threat intelligence data enters the sandbox for analysis. Even if the agent becomes malicious through prompt injection or stochastic behavior, it is designed to prevent the exfiltration of that data to the internet.
>
> Additional security practices:
>
> Controlled data ingestion: intentional about what types of data enter Code Interpreter and what write actions are permitted.
>
> Subprocessor alignment: Code Interpreter operates under the existing AWS subprocessor relationship and reduces compliance overhead.
>
> Network isolation layering: sandbox isolation on top of their existing network-isolated harness provides defense in depth.
>
> Lessons learned and best practices
>
> Several practices emerged from running Code Interpreter in production at Abnormal AI.
>
> 1. Give the agent what it wants
>
> Agents perform better with a lightweight, general harness rather than rigid step-by-step workflows. Provide high-level principles for solving a problem and let the agent use its intelligence to determine the approach.
>
> 2. Every agent needs a scratch pad
>
> Code Interpreter isn’t only for coding agents. Security agents analyzing email benefit from compute scratch pads for data aggregation, pattern analysis, and verification.
>
> 3. Use programmatic verifiers as guardrails
>
> Agents deliver higher quality outputs when they have programmatic verification tools. Unit tests, integration tests, and linting allow the agent to self-test within the sandbox before delivering final results.
>
> 4. Use file systems as recovery points for long-running tasks
>
> For operations exceeding the Code Interpreter session time (for example, model training), use the file system as a checkpoint. Run Code Interpreter for computation, persist state to files, perform long-running operations externally, then re-invoke Code Interpreter to process results. The analyst agent (Figure 3) uses this pattern for day-long model training operations.
>
> Conclusion
>
> Abnormal AI’s implementation demonstrates a key insight for production agent systems: Code Interpreter is not merely a coding tool. It’s fundamental infrastructure that agents use to reason computationally. By combining the managed, secure sandbox of AgentCore Code Interpreter with their own lightweight agent harness, Abnormal achieves:
>
> Zero-trust security posture through sandbox isolation helping prevent data exfiltration.
>
> Billion-message scale by reserving agent compute for the hardest cases (Figure 2).
>
> Whether you’re building security agents or a system where agents need to crunch data and verify their own outputs, the pattern is clear. Give your agents a scratch pad and trust their evaluations more than you trust their assertions.
>
> Next steps
>
> Get started with Amazon Bedrock AgentCore Code Interpreter.
>
> Explore AgentCore capabilities and other tools (Gateway, Memory, Runtime, Identity).
>
> Learn more about Abnormal AI at abnormalsecurity.com.
>
> Abnormal AI is an AWS customer. The views and opinions expressed in this post are those of the customer and don’t necessarily reflect the views of Amazon Web Services.
>
> About the authors
>
> Aswin Vasudevan
>
> Aswin is a Senior Solutions Architect for Security, ISV at AWS. He is a big fan of generative AI and serverless architecture and enjoys collaborating and working with customers to build solutions that drive business value.
>
> Felipe Lopez
>
> Felipe is a Principal AI/ML Specialist Solutions Architect at AWS. Prior to joining AWS, Felipe worked with GE Digital and SLB, where he focused on modeling and optimization products for industrial applications.
>
> Shrivu Shankar
>
> Shrivu is VP of AI Strategy at Abnormal AI, where he leads AI transformation and advances practical applications of agentic systems in cybersecurity and software development. A machine-learning engineer by background, he specializes in building AI-native workflows and multi-agent systems.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。