---
title: "How Mobileye transformed support operations using Amazon Bedrock AgentCore"
date: 2026-08-06T06:23:59+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "生成式 AI", "Amazon Bedrock", "Amazon Bedrock AgentCore", "AWS Lambda", "AWS Secrets Manager", "Customer Solutions"]
categories: []
source: "blogs_podcasts"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:a48e74e44e6004516c7d20c6b8a56f1a9295042fe66bb301274bcb477881a53b"
source_payload_sha256: "sha256:b436c322c9c2016ccdbb4efbc1df0904fa9ce4ccd874a46f87478039461196ac"
observation_id: obs_db756ec4d6e59ca936da7aa8eca44d5d6459a0ef221677a8ea82662f0ffa317c
event_id: evt_1e28557a77c211bae90a2fbe49036ecc84ef2c559978f2329dce637941e053c2
revision_id: rev_2153862914958c1b68cc12c581b6922ebaa4a65d9f0f68503427e259bf596825
source_published_at: 2026-08-05T18:09:03Z
first_seen_at: 2026-08-05T22:20:33.126599Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 74
description: "当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。"
external_url: https://aws.amazon.com/blogs/machine-learning/how-mobileye-transformed-support-operations-using-amazon-bedrock-agentcore
parent_observation_id: null
last_seen_at: 2026-08-05T22:20:33.126599Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/how-mobileye-transformed-support-operations-using-amazon-bedrock-agentcore](https://aws.amazon.com/blogs/machine-learning/how-mobileye-transformed-support-operations-using-amazon-bedrock-agentcore)
- **发布域名**: aws.amazon.com

## 来源摘要/节选

> What if deploying production-grade AI agents required zero infrastructure management, came with enterprise observability built-in, and worked easily with your existing on-premises systems?
>
> Mobileye, the autonomous driving pioneer with more than 230 million EyeQ system-on-chips deployed across roughly 1,200 vehicle models worldwide, saw an opportunity to free skilled engineers from routine internal ticket status inquiries.
>
> Mobileye’s Data Collection Processing pipeline ingests thousands of drive-recording sessions daily, generating a constant stream of status inquiries from engineers and data teams. Each inquiry previously required manual steps across multiple systems – identifying sessions, cross-referencing visualization tools, validating outputs, and reviewing logs – before composing a response. Using Amazon Bedrock AgentCore, Mobileye deployed an AI Support Agent that cut response times by 90% and exceeded 95% accuracy targets, with zero infrastructure overhead. The results were so compelling that Mobileye transformed AgentCore into a self-service platform for teams across the company to deploy their own AI agents.
>
> In this post, we’ll explore how Mobileye deployed an AI support agentic solution on Amazon Bedrock AgentCore – from the support bottleneck that sparked the idea, through the proof of concept that validated it, to the hybrid architecture that bridges on-premises systems with AWS cloud services. This approach is relevant for enterprises struggling to scale AI Agents while maintaining enterprise grade governance and security standards.
>
> From manual bottleneck to AI-powered support
>
> As Mobileye’s Data Collection pipeline scaled, 66% of support tickets became routine status inquiries requiring engineers to manually navigate 15 clicks across multiple backend systems. This time-consuming process diverted skilled engineers from complex issues while internal users faced longer wait times.
>
> Traditional automation approaches – scripting, static workflows, and rule-based decision trees – proved inadequate. While these could handle predictable queries, they lacked the contextual understanding needed to interpret the variability of real-world support requests. The team chose to build an AI agent capable of understanding context and adapting to diverse inquiry patterns.
>
> Validating the approach: Proof of concept
>
> Before full production rollout, Mobileye’s team conducted a proof of concept targeting 95% accuracy in ticket classification with sub-2-minute response times.
>
> The agent uses Anthropic Claude foundation models, accessed through Mobileye’s internal LLM Gateway that provides governed, quota-managed access to foundation models on Amazon Bedrock. The critical enabler was the Model Context Protocol (MCP), which gave the agent real-time access to the drive-data processing platform’s APIs -allowing it to query session status, retrieve processing logs, and pull diagnostic information during inference.
>
> This meant the agent went far beyond simple ticket classification, becoming an intelligent investigator capable of handling inquiries that were previously resolved through time-consuming manual effort.  When users inquired about drive-recording sessions, the agent could determine current state and respond with answers: confirming completed sessions with access details, surfacing specific errors with debugging recommendations and log links for failures, or guiding users through submission processes for missing requests – all in under two minutes with no human intervention.
>
> Evaluating the options
>
> After successfully proving the concept with their AI agent, Mobileye needed to take it to production. This transition required a solution that could meet enterprise-grade requirements while maintaining the flexibility they had demonstrated in their proof of concept. After careful evaluation, they chose to deploy their AI Agent on Amazon Bedrock AgentCore, a fully managed platform to build, connect and optimize AI agents at scale with any framework or model. The decision came down to five key factors:
>
> Serverless infrastructure ready for enterprise workloads
>
> Accelerated time-to-resolution for support inquiries
>
> Comprehensive built-in observability
>
> Support for multiple agentic frameworks
>
> Hybrid architecture support that could integrate easily with their existing on-premises ticketing system
>
> This last point was particularly important. Mobileye’s internal ticketing system operated on-premises and was inaccessible from AWS, so any solution would need to bridge that divide without compromising security or compliance.
>
> The production architecture: Bridging two worlds
>
> Following the successful proof of concept, Mobileye moved to production with a sophisticated hybrid architecture featuring clearly defined component roles across two environments.
>
> On-premises components
>
> The following table describes the on-premises components that handle local ticketing operations and bridge to cloud-based AI processing.
>
> Component
>
> Role
>
> Local Orchestrator
>
> Handles ticketing operations locally, extracting new tickets and posting completed responses back into the ticketing system.
>
> Internal ticketing system
>
> The on-premises ticket management system serves as both the source of support tickets and the destination for AI-generated responses. Its inaccessibility from AWS was the primary driver behind the hybrid design.
>
> AWS cloud components
>
> The following table describes the AWS cloud components that provide serverless compute, security, and observability infrastructure for the AI agent.
>
> Component
>
> Role
>
> AgentCore Runtime
>
> Mobileye runs their AI Support Agent on AgentCore’s serverless runtime, eliminating all infrastructure management. The team deploys and iterates without provisioning servers, benefits from automatic scaling to handle spikes in support volume and maintains full flexibility to use any agentic framework. A single API call invokes the agent – keeping integration with their existing systems straightforward.
>
> AgentCore Observability
>
> Mobileye’s engineering team uses built-in observability to trace every agent interaction end-to-end — from the initial request, through MCP tool calls to backend systems, to the final response. Detailed logs and tracebacks surface exactly how the agent reasoned, what data it retrieved, and where errors occur, dramatically reducing debugging time and accelerating iteration cycles.
>
> AWS Secrets Manager
>
> Mobileye uses Secrets Manager to enable faceless, secure authentication for their GenAI platform. Teams invoking AI agents never handle credentials directly – secrets required to interact with agents and backend systems are stored, rotated, and retrieved programmatically, enforcing enterprise security standards without adding friction for end users.
>
> Mobileye service
>
> The following table describes Mobileye’s own services that provide data connectivity and governed model access for the agent.
>
> Component
>
> Role
>
> Data Pipeline Model Context Protocol (MCP)
>
> The Data Pipeline MCP server enables real-time querying of live production data during inference including driving session warming statuses, request progress, and processing errors – allowing the agent to deliver context-aware responses on the fly.
>
> AI LLM Gateway
>
> Mobileye’s governed, quota-managed access to foundation models on Amazon Bedrock and other LLM providers
>
> How it all works together
>
> The automated workflow follows a streamlined four-step process:
>
> The Local Orchestrator extracts new tickets and sends them to the AI Support Agent running on AgentCore Runtime.
>
> The AI Support Agent processes each ticket end-to-end – categorizing the inquiry, querying live production systems via the MCP Server for real-time session data, and accessing Claude through the AI LLM Gateway – to generate a fully formatted response with links, recommendations, and actionable next steps.
>
> The Local Orchestrator receives the completed response and posts it back to the Internal Ticketing System with appropriate comments and labels.
>
> AgentCore Observability captures agent activity – session metrics, latency, token usage, and traces – for continuous monitoring and debugging
>
> Measurable results that speak for themselves
>
> The production deployment of Mobileye’s AI Support Agent on AgentCore delivered results that consistently met or surpassed initial targets.
>
> Overall success rate: 98% (surpassing the original 95% target)
>
> Response time: Reduced from hours to ~1 minute (90% improvement)
>
> Support volume automated: 66% of total ticket volume
>
> Monthly throughput: 100+ tickets processed
>
> Strategic benefits
>
> Support engineers are freed to focus on complex work – and the team didn’t have to build the infrastructure themselves, because AgentCore provides it out of the box.
>
> “Amazon Bedrock AgentCore enabled us to build a production-grade AI agent that delivers measurable business value while maintaining the security and operational standards our enterprise requires. The AI Support Agent has transformed our support operations, saving our engineers hundreds of hours previously spent on routine ticket lookups, and freed them to focus on what they do best.” — Shay Margalit, Principal Engineer, Mobileye
>
> Scaling the vision: From single agent to enterprise platform
>
> With the AI Support Agent delivering results in production, Mobileye faced a new challenge: most developers across the organization lacked the AWS credentials or infrastructure access to deploy agents on AgentCore independently. To address this, the Mobileye Cloud Infra team built an internal agent deployment platform.
>
> This internal managed service enables Mobileye developers to deploy production-grade AI agents without AWS expertise or cloud credentials. The process follows these steps:
>
> Teams provide their agent code
>
> Teams specify needed AgentCore capabilities – Memory, Browser Tool, Code Interpreter, Observability, Gateway.
>
> The Cloud Infra team provisions all infrastructure: AWS IAM Roles, Amazon S3 storage, Amazon CloudWatch monitoring, and Amazon Cognito authentication.
>
> Developers receive a pre-configured bedrock_agentcore.yaml file that integrates directly into their project.
>
> Deployment is a single command: agentcore deploy.
>
> The provisioned infrastructure aligns with Mobileye’s standards for security, cost governance, and operational excellence. CloudWatch Alarms on code exceptions help verify issues surface immediately.
>
> What began as a single proof-of-concept has evolved into an enterprise-wide platform where teams can deploy secure, monitored, cost-tracked agents in minutes rather than weeks.
>
> The path from manual processes to intelligent automation is shorter than you think, and the results, as Mobileye has shown, can be extraordinary.
>
> About the authors
>
> Shay Margalit
>
> Shay Margalit is a Principal Engineer at Mobileye, where he leads the development of AI-powered solutions for the company’s data infrastructure.
>
> Max Rabin
>
> Max Rabin is a Principal Engineer in Cloud Ops at Mobileye, responsible for architecting and operating production cloud environments at scale.
>
> Adi Jabkowsky
>
> Adi Jabkowsky is a Senior AI Specialist at Amazon Web Services, helping customers identify and implement high-impact generative AI use cases.
>
> Adir Gozlan
>
> Adir Gozlan is a Senior AI/ML Specialist Technical Account Manager at Amazon Web Services, focused on helping customers operationalize AI workloads at enterprise scale.
>
> Liat Tzur
>
> Liat Tzur is a Principal Technical Account Manager at Amazon Web Services and an AI enthusiast who partners with enterprise customers to accelerate their cloud and AI journeys.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。