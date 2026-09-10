---
title: "ICYMI: What landed for AI builders in August 2026"
date: 2026-09-10T17:46:39+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "Prompt 工程", "Amazon Bedrock", "Amazon Bedrock AgentCore", "Announcements", "Intermediate (200)", "博客与播客"]
categories: []
source: "blogs_podcasts"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:aa6699733bcf8bbfc135add461538b3e949803cfa15e5aa6745c87401a94b414"
source_payload_sha256: "sha256:904680f8b65aae276ce6e6f3791216b7763fa205fa919d44bf24c007b617dab9"
observation_id: obs_b9d5f24ad37b2183f9b52e4de309f62eeaef1b2845bab909a44ae7005cf58a51
event_id: evt_8037c311b637e4e1baaad4b08e9e2a7317a58d974fe95a0e4f67e5377f43264c
revision_id: rev_ada186ac271feebe58f05760de6b4347422320ba9e10bfec1d00806e08040919
source_published_at: 2026-09-09T20:01:03Z
first_seen_at: 2026-09-10T09:43:58.513654Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 49
description: "当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。"
external_url: https://aws.amazon.com/blogs/machine-learning/icymi-what-landed-for-ai-builders-in-august-2026
parent_observation_id: null
last_seen_at: 2026-09-10T09:43:58.513654Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/icymi-what-landed-for-ai-builders-in-august-2026](https://aws.amazon.com/blogs/machine-learning/icymi-what-landed-for-ai-builders-in-august-2026)
- **发布域名**: aws.amazon.com

## 来源摘要/节选

> A recap of the biggest Amazon Bedrock, AgentCore, and Strands updates from August 2026.
>
> At AWS, we have long focused on making foundational technologies accessible and providing the infrastructure needed to put them to work. Amazon Bedrock, used by more than 225,000 active customers, including over 80% of Fortune 100 companies, embodies that commitment by providing access to leading models and a broad set of tools to build and scale AI, with the security, reliability, performance, and cost efficiency customers need in production. As agentic applications expand, Amazon Bedrock extends this foundation with AgentCore, which lets you build, connect, and optimize agents using any framework and model. AWS also released the Strands Agent Harness SDK as open source, giving you the flexibility to create agents and deploy them wherever you choose. Together, they help you turn model intelligence into production agents without limiting how those agents are built or where they run.
>
> As models become more capable, organizations can ask a more ambitious question: how much meaningful work can AI take on from start to finish? Across industries, agents are moving into workflows that require them to reason over enterprise information, remain productive over longer time horizons, and act across digital and physical systems. As the scope of that work expands, attention is shifting to the complete system around the model, including what context it can access, what actions it can take, where data is processed, and how its decisions and costs are governed.
>
> We believe the next phase of AI will be shaped not only by what models can do, but by how confidently you can delegate responsibility to the systems built around them. That confidence depends on systems that can understand the task in front of them, persist as it unfolds, and operate within clear organizational boundaries. August’s updates move in that direction, giving you stronger foundations for AI systems that can understand more, work longer, and take on demanding responsibility across enterprise, regulated, and physical environments.
>
> Reason over more context at scale with greater control
>
> Bring entire working sets and current web context into your OpenAI applications on Amazon Bedrock. GPT-5.6 Sol, Terra, and Luna now support million-token context windows with prompt caching, helping reduce cost and latency when context is reused. Web Search lets the models find current information beyond their training data, incorporate relevant results into their answers, and provide citations without requiring you to integrate a separate search provider. For use cases that need the freshest details, such as live pricing or newly released documentation, the models can also retrieve content directly from public websites. Together, these capabilities let you analyze an entire codebase or regulatory document, check its contents against the latest public information, and return a cited response from a single API call.
>
> Route inference globally without stitching together Regions. With cross-Region inference, you can access GPT-5.6 Sol, Terra, and Luna from more than 25 AWS Regions. Global profiles give you the broadest capacity at lower per-token prices, while Geo profiles keep inference processing within a defined geography. With these updates, you can increase throughput during demand spikes while choosing the geographic boundary that fits your application’s data-processing requirements.
>
> Understand and control inference spend as model usage grows. IAM principal cost allocation helps you attribute inference spend to a user, team, project, application, or cost center, while AWS Cost Anomaly Detection now monitors third-party foundation model spend on Amazon Bedrock and provides root-cause breakdowns when costs change unexpectedly. OpenAI also announced lower pricing across the GPT-5.6 family on Amazon Bedrock, including Luna, Terra, and Sol. This gives you greater visibility into which teams are driving spend, helps you catch unusual changes earlier, and supports more informed decisions as AI workloads scale.
>
> Faster cyber defense from detection to response
>
> Give security teams frontier AI for both defensive and authorized offensive workflows. Daybreak Red and Daybreak Blue from OpenAI are now available to eligible customers on Amazon Bedrock. Daybreak Blue supports defensive work such as vulnerability discovery, detection engineering, and incident response. Daybreak Red supports advanced, authorized tasks such as vulnerability research, exploit reproduction, and mitigation development. You can now investigate and address vulnerabilities faster while applying stronger identity verification, monitoring, access controls, and zero-operator-access infrastructure.
>
> Get more done with agents that stay on track
>
> Keep production agents running long enough to complete multi-day work. AgentCore runtime instances let you run agents on dedicated Amazon EC2 compute, including GPU-accelerated, memory-optimized, and compute-optimized instances, with sessions lasting up to 14 days. AgentCore also expanded to US West (N. California) and Asia Pacific (Hyderabad). You can now hand agents long-running research, coding, and monitoring work, match each workload to the compute it needs, and run it closer to the users and systems it serves.
>
> Let agents act more independently while keeping their behavior and spending within defined boundaries. Temporal policies evaluate each action against what an agent has already done, letting you enforce sequences, prerequisites, approval gates, matching values between calls, and data freshness. Rate limiting controls requests, inference tokens, and concurrent connections by user or group. AgentCore payments lets agents access and pay for APIs, MCP resources, and paid content with infrastructure-enforced spending limits and end-to-end observability. Together, these updates let you give agents more independence while controlling what can happen, in what order, at what rate, and within what budget.
>
> Give agents timely context without weakening data boundaries. Web Search in AgentCore lets agents include or exclude domains and filter results by publication date, helping them retrieve current information from approved sources. AgentCore memory can extract long-term memories from activity logs, behavioral events, system events, and other structured JSON data, not only from conversations. Fine-grained access control can then isolate those memories by user or tenant. Now you can ground agents in trusted sources, build memory from business events, and keep that context isolated without adding custom authorization logic to every application.
>
> Find and reuse approved agents and tools instead of rebuilding what already exists. AWS Agent Registry gives you a searchable, governed catalog for agents, MCP servers, skills, and custom resources. Organization-wide detection can identify agents on AgentCore Runtime and MCP servers on AgentCore Gateway across connected AWS accounts, while approved resources can also surface in Amazon Quick. You can find trusted capabilities by intent or name, reuse them across workflows, and reduce agent sprawl and duplicative development.
>
> Build with more choice in regulated environments
>
> Bring advanced models, agent capabilities, and cross-modal retrieval to regulated workloads. Claude Opus 5 is now available in AWS GovCloud (US) Regions with zero data retention enabled by default. OpenAI GPT-5.6 Terra and Luna are also available in AWS GovCloud (US) Regions, with million-token context windows and prompt caching. Amazon Nova Multimodal Embeddings brings retrieval across text, documents, images, video, and audio to AWS GovCloud (US-West), while AgentCore memory, policy, and the managed harness add managed context, controls, and orchestration. This helps you build coding agents, document-analysis systems, multimodal retrieval applications, and governed agent workflows in AWS GovCloud using more of the same capabilities available in commercial Regions.
>
> Extend AI agents into the physical world
>
> Move from robot demonstrations to training and physical deployment through one connected workflow. Strands Robots connects Strands Agents, LeRobot, and Hugging Face Storage Buckets, letting you record demonstrations, stream datasets in the LeRobot format, train policies, and deploy them to simulated or physical hardware without converting the underlying data. This allows you to iterate on robotics policies using one data format and one agent workflow from simulation through physical deployment.
>
> Coordinate multiple robots and devices without rebuilding the agent for each environment. Strands Robots supports mesh-based discovery and coordination across simulated and physical devices. Zenoh connects robots on the same local network, while AWS IoT Core supports geographically distributed fleets. Strands Robots and AWS are also participating in the limited research preview of the Model Hardware Standard. This makes it easier for you to prototype multi-robot workflows in simulation, move them across local and cloud-connected fleets with fewer code changes, and explore standardized controls for physical equipment.
>
> Get started
>
> Explore Amazon Bedrock, deploy agents with the AgentCore CLI, or build your first agent with the Strands Harness SDK.
>
> Interested in learning how Amazon Bedrock can support your team? Connect with us to start the conversation.
>
> About the authors
>
> Tanvi Girinath
>
> Tanvi Girinath is a Product Marketing Manager for Amazon Bedrock at Amazon Web Services (AWS), where she helps customers adopt and scale AI applications and agents with Amazon Bedrock.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。