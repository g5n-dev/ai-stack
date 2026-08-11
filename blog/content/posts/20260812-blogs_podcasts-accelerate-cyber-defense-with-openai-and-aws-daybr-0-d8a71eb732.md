---
title: "Accelerate cyber defense with OpenAI and AWS: Daybreak Red & Daybreak Blue now available to eligible customers on Amazon Bedrock"
date: 2026-08-12T06:05:52+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "Amazon Bedrock", "Announcements", "Foundational (100)", "博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:f379197af210d85bef12db376d644a38aa7a32162a596e94ed0a1bbff9e8800d"
source_payload_sha256: "sha256:857876251c9bca7c1ab12d8f9898a66d3a0e7fca1562a2f8e14f1b58384fa985"
observation_id: obs_d8a71eb7325669ff71f036f17a2104d7d6ed908ffc98b61d89e7f22fa21eef07
event_id: evt_a35f33d3f46811f24bd467f35f0046dc863bc0c97415e37d2843dce36a3f30c0
revision_id: rev_ce67b7f3bda599338fd8c78025aa463b99a4c847849f1598408bf6d87fb80a32
source_published_at: 2026-08-11T21:38:06Z
first_seen_at: 2026-08-11T22:15:13Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 128
interpretation_sha256: "sha256:1c172dce43d929e31ddf52b906cc8713d0cf7fa0640db0290731e0c3b7ba47c3"
description: "这是 AWS 与 OpenAI 在 Amazon Bedrock 上线专门用于网络防御的 AI 模型。Daybreak Red 提供攻击性安全研究能力，Daybreak Blue 侧重防御性安全任务，两者都旨在帮助安全团队更快完成漏洞发现、验证和修复流程。"
external_url: https://aws.amazon.com/blogs/machine-learning/accelerate-cyber-defense-with-openai-and-aws-daybreak-red-daybreak-blue-now-available-to-eligible-customers-on-amazon-bedrock
parent_observation_id: null
last_seen_at: 2026-08-11T22:04:20.232839Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/accelerate-cyber-defense-with-openai-and-aws-daybreak-red-daybreak-blue-now-available-to-eligible-customers-on-amazon-bedrock](https://aws.amazon.com/blogs/machine-learning/accelerate-cyber-defense-with-openai-and-aws-daybreak-red-daybreak-blue-now-available-to-eligible-customers-on-amazon-bedrock)
- **发布域名**: aws.amazon.com

## 要点解读

### 这是什么
这是 AWS 与 OpenAI 在 Amazon Bedrock 上线专门用于网络防御的 AI 模型。Daybreak Red 提供攻击性安全研究能力，Daybreak Blue 侧重防御性安全任务，两者都旨在帮助安全团队更快完成漏洞发现、验证和修复流程。

### 用在哪里
适合需要在云环境中处理敏感代码和漏洞数据的网络安全团队。这些模型在 AWS 基础设施上运行，强调数据安全和合规性，适用于进行源代码分析、漏洞挖掘和事件响应的专业安全人员。

### 可以推断的
推测：这类工具主要面向具有专门安全团队的企业组织，因为模型提供受限的访问机制和身份验证流程，不适合个人或小型团队随意使用。
推测：随着 AI 技术在网络安全领域的应用加速，防御者与攻击者在工具层面的竞争将更加激烈，企业需要通过可信云平台获取这些能力以保持优势。

## 来源摘要/节选

> Cyber defenders have never had more capability at their fingertips, and they have never needed it more. Frontier models can now reason across an entire code base, trace a vulnerability to its root cause, and propose a fix in minutes. Those same capabilities are available to adversaries. This is why the window between a vulnerability being disclosed and being exploited keeps shrinking. Defenders are expected to keep pace across sprawling, unfamiliar code bases, validate which findings matter, and ship patches that hold. They must do all of this while keeping sensitive code and vulnerability data inside an environment they control and can audit. The challenge is no longer surfacing potential issues but confirming which ones are real, fixing them, and doing it before the window closes.
>
> AWS has always operated on the principle that security is built in from the start. The same is true for AI: customers run workloads on Amazon Bedrock, from inference to fully autonomous agents, under the same infrastructure, controls, and governance they rely on across AWS. Today, AWS and OpenAI are extending that foundation to cyber defense. Daybreak Red and Daybreak Blue from OpenAI are now available on Amazon Bedrock to eligible customers. Daybreak Red provides access to GPT-5.6 Cyber, a purpose-trained cybersecurity model. Daybreak Blue provides access to GPT-5.6 Sol with safeguards calibrated for defensive cybersecurity work. Both are part of Daybreak, the cyber defense initiative from OpenAI that gives defenders governed access to frontier AI, including agentic tooling, application red teaming, and services that help defenders move from findings to tested fixes.
>
> “AWS and OpenAI share a belief that defenders should have the advantage. This partnership brings Daybreak Red and Daybreak Blue from OpenAI to Amazon Bedrock. AWS security teams are using both models today to analyze source code, discover vulnerabilities, and conduct red-team research. On Bedrock, that work runs under the same infrastructure controls AWS applies to every other critical workload. As these models continue to advance, so will what defenders can do with them on Amazon Bedrock.”
>
> — John Sheehan, Vice President, AWS Security
>
> Specialized models for advanced, authorized cyber security work
>
> The path from vulnerability discovery to remediation is long: confirming exploitability, tracing how the vulnerable component is reachable, developing a fix that addresses root cause without introducing regressions, validating it holds under realistic conditions, and shipping a patch within the disclosure window. Defenders need models that can accelerate every step. But cybersecurity is inherently dual use. A request to reproduce a vulnerability or reverse engineer an exploit chain looks identical regardless of intent, and general-purpose models resolve that ambiguity by declining the request. Daybreak Red and Daybreak Blue resolve it through context: who is using the model, where the work occurs, and what safeguards govern that access.
>
> Daybreak Blue is the right starting point for most security teams. It supports vulnerability discovery, detection engineering, and incident response. Daybreak Red is designed for advanced tasks like vulnerability research, exploit reproduction, and mitigation development. For these tasks, a lower refusal threshold (the point at which the model declines a request) matched by stronger identity verification, monitoring, and access controls improves the speed and depth of an investigation.
>
> According to OpenAI, security researchers used GPT-5.6 Cyber through Daybreak Red to identify two previously unknown vulnerabilities in V8, the JavaScript engine used by Chrome, which when chained together could enable memory corruption and a heap sandbox escape. The initial vulnerability was fixed and released as CVE-2026-15903, one of only four successful zero-day entries to V8 CTF in 2026.
>
> Run it on the foundation you already trust
>
> A cyber security workload feeds the model your most sensitive inputs: proprietary source code, unpatched vulnerability details, and live telemetry from production systems. Before any of that runs through a model, you need certainty about where it goes and who can see it.
>
> Both models run on the Amazon Bedrock next-generation inference engine built for high performance, security, and reliability. Zero-operator access (ZOA) is enforced at the chip, so even AWS operators cannot access your prompts and completions during inference. Everything is encrypted in transit and at rest with customer-managed AWS Key Management Service (AWS KMS) keys. Access is governed by your AWS Identity and Access Management (IAM) policies, logged in AWS CloudTrail, and routed through virtual private cloud (VPC) endpoints. You can set data perimeter policies at the organization level to prevent exfiltration across account and network boundaries.
>
> Your inference data is not used for model training, and neither model requires you to opt into sharing your data with OpenAI. For automated abuse detection, classifier-flagged traffic is retained by AWS for up to 30 days and processed programmatically. Customers may request zero data retention through their AWS account team. See data retention for details.
>
> Get started
>
> Daybreak Red: GPT-5.6 Cyber and Daybreak Blue: GPT-5.6 Sol are now available to eligible customers on Amazon Bedrock in the following AWS Region: US East (N. Virginia). Access to the models requires enrollment in Trusted Access for Cyber from OpenAI. To enroll, contact OpenAI or reach out to your AWS account team for guidance on eligibility. Once approved, work with your account team to request access on AWS. To learn more, see the documentation.
>
> To explore the full GPT-5.6 family on Amazon Bedrock, see Get started with OpenAI GPT-5.6 Sol, Terra, and Luna on Amazon Bedrock.
>
> Interested in how Amazon Bedrock can support your team? Connect with us to start the conversation.
>
> About the authors
>
> Tanvi Girinath
>
> Tanvi is a Product Marketing Manager for Amazon Bedrock at Amazon Web Services (AWS), where she helps customers adopt and scale AI applications and agents with Amazon Bedrock.
>
> Saurabh Trikande
>
> Saurabh is Senior Product Manager for Amazon Bedrock at Amazon Web Services (AWS). He leads efforts to make inference with frontier models from leading providers performant, secure, and cost-efficient for customers at any scale.
>
> Chris Dickens
>
> Chris is a Member of Product Staff at OpenAI focused on the OpenAI APIs. His work includes collaboration with AWS on Amazon Bedrock to make OpenAI’s frontier models widely accessible to developers.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。