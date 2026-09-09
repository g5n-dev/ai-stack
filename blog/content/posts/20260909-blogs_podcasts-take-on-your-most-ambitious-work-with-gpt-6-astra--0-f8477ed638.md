---
title: "Take on your most ambitious work with GPT-6 Astra on Amazon Bedrock"
date: 2026-09-09T08:16:31+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "Prompt 工程", "Amazon Bedrock", "Announcements", "Intermediate (200)", "博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:9e419421247a1f2e7f5fea79dce1db0486171d4b12dad7f963feb067bd6104d3"
source_payload_sha256: "sha256:58d1c639275cf4bd9ffce05666d21eb007bf908978aca7c5953d63c823b5371b"
observation_id: obs_f8477ed638254f5fc90bb06823acb01d7c31da33d170e27e4bdd2ac5657da958
event_id: evt_d3a6c04149056805f9393883e8f82262633942d4c9bdefa18adf040002ecf6b1
revision_id: rev_e8a807050570f31c543443757341d454e58b6610b7171d93bbe5fbb3417c83fc
source_published_at: 2026-09-08T22:06:58Z
first_seen_at: 2026-09-09T00:26:53Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 67
description: "当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。"
external_url: https://aws.amazon.com/blogs/machine-learning/take-on-your-most-ambitious-work-with-gpt-6-astra-on-amazon-bedrock
parent_observation_id: null
last_seen_at: 2026-09-09T00:14:24.811841Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/take-on-your-most-ambitious-work-with-gpt-6-astra-on-amazon-bedrock](https://aws.amazon.com/blogs/machine-learning/take-on-your-most-ambitious-work-with-gpt-6-astra-on-amazon-bedrock)
- **发布域名**: aws.amazon.com

## 来源摘要/节选

> GPT-6 Astra from OpenAI brings greater depth and judgment to your most demanding tasks and runs on the Amazon Bedrock inference engine built for high performance, security, and scale.
>
> Organizations are already running AI agents that write code, analyze data, and automate complex workflows at production scale on Amazon Bedrock. GPT-6 Astra raises the potential of what those agents can deliver. It applies deeper reasoning and sharper judgment to complex business decisions, works across software and files, and produces professional-quality output aligned with organizational voice, templates, and standards.
>
> Today, GPT-6 Astra, the latest and most capable OpenAI model, is generally available on Amazon Bedrock. You can call the model directly through the Amazon Bedrock APIs or configure ChatGPT Work and Codex to use GPT-6 Astra on Amazon Bedrock. As part of this launch, OpenAI is also introducing new enterprise plugins for ChatGPT Work that extend Astra’s browser-use capabilities across common business applications. The Amazon Bedrock inference engine delivers the scalability and reliability required for production. Established AWS controls help you secure workloads, govern access, and audit model invocation activity.
>
> Greater depth for complex decisions
>
> GPT-6 Astra brings greater depth to work that requires you to reconcile competing inputs, trace dependencies, and determine what to prioritize. When performing financial analysis, it can help you reconcile conflicting data sources and identify discrepancies that could change a recommendation. During contract review, it can review hundreds of pages within a context window of up to 1 million input tokens and identify provisions that carry the greatest risk. Across a codebase, it can investigate problems across a large codebase, reason through dependencies, and carry a fix from diagnosis through testing. GPT-6 Astra also advances computer and browser use, allowing it to work across applications and continue workflows directly through software interfaces when an API or connector is unavailable.
>
> For workflows that reuse the same context across requests, such as recurring document review, codebase analysis, or agents grounded in company standards, GPT-6 Astra supports both implicit and explicit prompt caching. With explicit caching, you can set cache breakpoints to control which context is cached. Reusing that context in subsequent requests helps reduce repeated processing, cost, and latency.
>
> Layered security and governance for production AI
>
> Model-level safeguards work alongside the security and governance controls of Amazon Bedrock. OpenAI evaluated GPT-6 Astra through its Preparedness Framework, which assesses model capabilities across safety-relevant domains and applies progressively stronger safeguards as those capabilities advance. It’s the first OpenAI model to reach the Critical classification for cybersecurity capability. At this level, automated safeguards monitor misuse in real time and can pause or stop activity that exceeds defined boundaries, and work within the Amazon Bedrock service boundary. These safeguards complement AWS security controls when GPT-6 Astra works across code, software, and tools.
>
> Amazon Bedrock protects your inference data and governs access at every model invocation. Zero-operator access is enforced at the chip, so even AWS operators can’t access your prompts and completions during inference. Data is encrypted in transit and at rest. Access is governed by your AWS Identity and Access Management (IAM) policies, and every invocation is logged in AWS CloudTrail. You can route traffic through virtual private cloud (VPC) endpoints using AWS PrivateLink and establish data perimeter policies at the organization level to help prevent data exfiltration across account and network boundaries.
>
> Your inference data isn’t used for model training, and using GPT-6 Astra doesn’t require you to opt into sharing your data with OpenAI. For automated abuse detection, classifier-flagged traffic is retained by AWS for up to 30 days and processed programmatically. You can request zero data retention through your AWS account team. See data retention for details.
>
> Build, code, and work with Astra
>
> You can use GPT-6 Astra for inference, knowledge work, and software development.
>
> Integrate Astra into your applications
>
> You can integrate GPT-6 Astra directly into your applications using supported Amazon Bedrock APIs. Use it to power autonomous agents that handle complex, multistep workflows, build internal tools that analyze and synthesize documents at scale, or create customer-facing applications that require judgment across competing inputs.
>
> Turn complex tasks into finished deliverables
>
> ChatGPT Work is a productivity agent for turning complex business tasks into finished deliverables. With GPT-6 Astra, it can gather information across applications and files, use the web, and produce spreadsheets, slides, documents, and sites. You can control which applications and websites the agent can access, manage file uploads and downloads, and require confirmation before specific actions. You can also follow its progress, change direction, and approve important steps, keeping people in control throughout the workflow.
>
> ChatGPT Work is available through the ChatGPT desktop app for Mac and Windows. New enterprise plugins introduced alongside this release extend browser-use capabilities across business intelligence tools, Workday, Navan, and Avalara for tasks across data analytics, operations, and finance. These plugins work through your existing user account and within the permissions your administrators establish, so they do not grant Astra additional access.
>
> Build, test, and ship code faster
>
> Codex is a software engineering agent that works with local files, repositories, terminals, developer tools, and development environments to write features, fix bugs, run tests, and open pull requests. When you configure Codex to use GPT-6 Astra on Amazon Bedrock, it applies Astra’s reasoning and computer-use capabilities to tasks spanning investigation, implementation, and testing.
>
> You can access Codex through the ChatGPT desktop app, CLI, VS Code, JetBrains IDEs, and Xcode. For AWS development, the Agent Toolkit for AWS connects Codex to AWS documentation, APIs, and service capabilities with a single terminal command, so your agent can help you develop, deploy, and manage applications more efficiently.
>
> Get started
>
> You can get started in the Amazon Bedrock console or programmatically through supported Amazon Bedrock APIs. For information about supported AWS Regions, endpoints, APIs, features, inference profiles and pricing, see the Amazon Bedrock documentation.
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

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。