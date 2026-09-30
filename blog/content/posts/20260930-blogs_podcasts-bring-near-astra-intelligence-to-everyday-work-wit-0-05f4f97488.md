---
title: "Bring near-Astra intelligence to everyday work with GPT-6.1 Sol on Amazon Bedrock"
date: 2026-09-30T04:48:56+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "Amazon Bedrock", "Announcements", "Intermediate (200)", "博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:e4c068f2bc6fca82f005197a40542c83bcc72686ed7305e0da29058816ef5dab"
source_payload_sha256: "sha256:6e93ec54ef287519365595a158b3f33a0838e4591c6290873c2d78c52f346918"
observation_id: obs_05f4f9748885e1c59e65c4eac32533835fff3ea66ca004e45b09b1a9c9c85fe0
event_id: evt_6865ae8240aecc91b3326602e21a88b4aa6101d1169235f5ed0cf021e312288d
revision_id: rev_c838c84e05954e708b51f8826bfb353b03cb90c684481c1baada67a029630f00
source_published_at: 2026-09-29T19:34:14Z
first_seen_at: 2026-09-29T20:59:23Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 81
interpretation_sha256: "sha256:167634bca3672496176177a9a4948f6ae6a8fd9d45f7ba243cf5d2ead616a449"
description: "GPT-6.1 Sol 在 Amazon Bedrock 上正式发布，为 AI 代理的编码、计算机操作和专业工作流程带来更强的推理能力，同时在成本上优于前代版本。"
external_url: https://aws.amazon.com/blogs/machine-learning/bring-near-astra-intelligence-to-everyday-work-with-gpt-6-1-sol-on-amazon-bedrock
parent_observation_id: null
last_seen_at: 2026-09-30T00:00:00Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/bring-near-astra-intelligence-to-everyday-work-with-gpt-6-1-sol-on-amazon-bedrock](https://aws.amazon.com/blogs/machine-learning/bring-near-astra-intelligence-to-everyday-work-with-gpt-6-1-sol-on-amazon-bedrock)
- **发布域名**: aws.amazon.com

## 要点解读

### 这是什么

GPT-6.1 Sol 在 Amazon Bedrock 上正式发布，为 AI 代理的编码、计算机操作和专业工作流程带来更强的推理能力，同时在成本上优于前代版本。

### 用在哪里

适用于需要构建 AI 代理的企业开发者，尤其是涉及软件工程、多步骤文档处理和跨系统工作协调的场景。AWS 和 OpenAI 的合作使其面向使用 Amazon Bedrock 构建生产级 AI 应用的技术团队。

### 可以推断的

推测：该模型针对代理场景优化，推理能力的提升意味着代理在执行复杂任务时需要更少的交互次数，从而降低延迟和人工干预的频率。

推测：Amazon Bedrock 提供的基础设施保障，如硬件隔离和 VPC 端点，表明该服务主要面向对数据安全和合规有较高要求的企业客户。

## 来源摘要/节选

> GPT-6.1 Sol is now generally available on Amazon Bedrock, bringing stronger reasoning to coding, computer use, and professional workloads that run frequently.
>
> For an AI agent to complete a task, it may need to gather information, use tools, test different approaches, recover from errors, and verify its result. Every decision shapes what happens next. A wrong turn can add model interactions, tool calls, latency, and human intervention before the agent reaches a useful result.
>
> The economics of an AI agent take shape across the entire task. Token prices influence the cost of each interaction, while reasoning quality influences how many interactions the work requires and whether they lead to a successful outcome. The total cost of completing a task depends on both.
>
> Today, GPT-6.1 Sol is generally available on Amazon Bedrock, running on an inference engine built for performance, security, and reliability at scale. A major upgrade to GPT-6 Sol, it delivers strong performance on agentic coding, computer use, and professional work. According to OpenAI, it brings near-Astra intelligence to everyday workflows.
>
> Apply stronger reasoning across agentic work
>
> Navigate software engineering workflows more effectively
>
> Software engineering shows how reasoning quality affects an entire workflow. An agent may need to understand an unfamiliar repository, trace dependencies, determine where to make a change, and validate the implementation. According to OpenAI, GPT-6.1 Sol matches GPT-6 Astra on DeepSWE v1.1 at roughly one-fifth the cost per task. It also exceeds the best score from GPT-6 Sol by 6.4 percentage points while using a lower reasoning effort than that GPT-6 Sol result.
>
> Codex puts that reasoning to work across the full development cycle. You can configure Codex to use GPT-6.1 Sol on Amazon Bedrock for work spanning investigation, implementation, and testing. Codex works with repositories, local files, terminals, and development tools to write features, fix bugs, and run tests. You can access Codex through the desktop app, CLI, and supported IDEs. For AWS development, the Agent Toolkit for AWS connects Codex to AWS documentation, APIs, and services through a single terminal command.
>
> Turn information into action across documents and tools
>
> The same reasoning capabilities apply when agents must interpret complex documents, select the appropriate tools, and adapt as conditions change. According to OpenAI, GPT-6.1 Sol approaches GPT-6 Astra on complex document analysis and improves on GPT-6 Sol when completing multistep workflows across business tools.
>
> You can apply these capabilities through ready-to-use experiences or applications you build. In the desktop app, ChatGPT Work can gather information across files and applications and turn it into finished deliverables. Using supported Amazon Bedrock APIs, you can also build internal tools that synthesize documents, agents that coordinate work across systems, and customer-facing applications that evaluate multiple inputs.
>
> Recognize limitations and respect constraints
>
> Working effectively across tools also requires an agent to recognize when a tool has failed, an action is restricted, or information is missing. Communicating these limitations allows the application or user to intervene before the agent continues with incomplete information or takes an unintended action. According to OpenAI, GPT-6.1 Sol improves on GPT-6 Sol in challenging evaluations of transparency, user intent, and explicit restrictions.
>
> When building with supported Amazon Bedrock APIs, you can define the tools available to the model. You can also determine how your application responds when an action requires approval or cannot be completed. These application-level controls complement the model improvements by helping you keep people involved when a workflow reaches a consequential decision.
>
> Run GPT-6.1 Sol on Amazon Bedrock
>
> Amazon Bedrock provides the infrastructure and controls to run GPT-6.1 Sol in production. You can govern model access through AWS Identity and Access Management (IAM) policies and audit invocations through AWS CloudTrail. To help keep traffic within your network boundaries, you can use virtual private cloud (VPC) endpoints powered by AWS PrivateLink. Inference runs on hardware-isolated infrastructure with zero-operator access, so not even AWS operators can access your prompts and completions during inference.
>
> Your inference data isn’t used for model training, and using GPT-6.1 Sol doesn’t require you to opt into sharing your data with OpenAI. For automated abuse detection, classifier-flagged traffic is retained by AWS for up to 30 days and processed programmatically. You can request zero data retention through your AWS account team. See data retention for details.
>
> Get started
>
> GPT-6.1 Sol brings stronger reasoning to agentic work at a fraction of the cost per task, so your agents reach the right answer in fewer steps. You can get started with GPT-6.1 Sol in the Amazon Bedrock console or programmatically through supported Amazon Bedrock APIs. For information about supported AWS Regions, endpoints, APIs, features, inference profiles and pricing, see the Amazon Bedrock documentation.
>
> Interested in how Amazon Bedrock can support your team? Connect with us to start the conversation.
>
> About the authors
>
> Tanvi Girinath
>
> Tanvi is a Product Marketing Manager for Amazon Bedrock at Amazon Web Services (AWS), where she helps customers adopt and scale AI applications and agents with Amazon Bedrock.
>
> Chris Dickens
>
> Chris is a Member of Product Staff at OpenAI focused on the OpenAI APIs. His work includes collaboration with AWS on Amazon Bedrock to make OpenAI’s frontier models widely accessible to developers.
>
> Manish Rathaur
>
> Manish is a Senior Product Manager for Amazon Bedrock.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。