---
title: "A shared agentic platform for Wood Mackenzie, on Amazon Bedrock AgentCore"
date: 2026-09-20T09:09:50+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "RAG", "AI Agent", "生成式 AI", "Amazon Bedrock AgentCore", "Customer Solutions", "博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:3ef5994700f163fe17ae3274537f965b591e57f80c94da035a3842a66a4e9ef4"
source_payload_sha256: "sha256:956561f4a0100a71c66f7f4a260aef8f0910bd64cfa7fc343c87816da03894d6"
observation_id: obs_c5c96ab0697aa5bf9ed6068c81dfbca130cd3c544c4991300c8e8be3c27a4d42
event_id: evt_2c15a6201ac45a4d913879373986d0c1e2b427aab5f9bc5121c594087a20b11b
revision_id: rev_cc744e73f2a22c1724f67455d4697ceae6bfcaea1f074d5d199a435857559a0f
source_published_at: 2026-09-17T15:41:03Z
first_seen_at: 2026-09-20T01:08:13.931244Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: true
source_truncation_reason: "crawler_feed_content_limit"
source_support: 1.0
source_title_chars_original: 73
interpretation_sha256: "sha256:6658c38cd116244d8a4406107ebdcb29ce249dce77e1f32dac0d0ab5b49830b3"
description: "这是一篇企业案例，介绍Wood Mackenzie公司如何在Amazon Bedrock AgentCore基础上构建统一的AI代理平台（APEX），让多个业务团队无需各自搭建基础设施，即可快速上线代理功能。"
external_url: https://aws.amazon.com/blogs/machine-learning/a-shared-agentic-platform-for-wood-mackenzie-on-amazon-bedrock-agentcore
parent_observation_id: null
last_seen_at: 2026-09-20T01:08:13.931244Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/a-shared-agentic-platform-for-wood-mackenzie-on-amazon-bedrock-agentcore](https://aws.amazon.com/blogs/machine-learning/a-shared-agentic-platform-for-wood-mackenzie-on-amazon-bedrock-agentcore)
- **发布域名**: aws.amazon.com

## 要点解读

### 这是什么
这是一篇企业案例，介绍Wood Mackenzie公司如何在Amazon Bedrock AgentCore基础上构建统一的AI代理平台（APEX），让多个业务团队无需各自搭建基础设施，即可快速上线代理功能。

### 用在哪里
适合企业技术负责人或AI平台架构师参考，尤其在评估是否采用托管服务来统一管理AI代理的编排、安全和可观测性时，可从中了解选型思路和平台设计要点。

### 可以推断的
推测：大型企业在推进AI代理规模化落地时，往往面临各团队重复建设的问题，共享平台模式有助于集中资源、统一标准并降低整体投入。  
推测：托管型AI代理运行时可能逐渐成为主流，因为它把扩容、监控、合规等运维工作转移给云服务商，让业务团队更专注于应用逻辑本身。

## 来源摘要/节选

> Building a working agentic prototype takes an afternoon. Getting it to production is where the work explodes. The moment an agent has to serve more than one user, a new layer of engineering appears and it’s critical to tell whether the agent is doing the right thing on real traffic. Concurrency, session isolation, identity, persistent state, scaling, and guardrails are all layers that most teams rebuild from scratch every time, even though a standardized platform for each agent is a more repeatable approach.
>
> The result is a wide gap between experimentation and production. Industry surveys through early 2026 put enterprise AI experimentation near universal while only about a quarter of organizations have scaled agents into production in even one function. Internally at Wood Mackenzie, we have found that 88 percent of AI proofs-of-concept never reach widescale deployment. The reasons are consistent across analysts, and they are mostly architectural rather than model-related. Forrester attributes agent failures largely to ambiguity, miscoordination, and unpredictable system behavior rather than ordinary bugs. The most-named single blocker is evaluation and observability: teams cannot reliably tell ahead of time when a non-deterministic agent will be wrong, and standard regression tests do not catch it. Governance and identity follow close behind, with a large share of executives reporting they could not immediately shut down a misbehaving agent. Underneath all of it is duplicated infrastructure: each team re-implements authentication, guardrails, memory, and tracing, and hardcodes a model so that swapping providers means rewriting code.
>
> This is the problem a shared agentic platform solves. Instead of every team rebuilding the same foundation, one runtime handles orchestration, safety, observability, identity, and connectivity, and teams spend their effort on the business logic that differentiates their product.
>
> In this post we show how we built APEX (Agentic Platform for Energy eXperience), a shared platform so every team can ship agents without reinventing infrastructure. APEX is built on Amazon Bedrock AgentCore, a platform to build, connect, and optimize agents at scale, with any framework or model. We cover why we selected AgentCore over self-hosted solutions, how the architecture is composed, how APEX Studio gives teams a single control plane to operate it, how we bring interactive AI into real applications for both internal users like Woody and external consumers like Lens. We will also dive into how the same infrastructure serves both under identity-aware entitlements, how we close the evaluation and governance gaps that stall most agent programs, and where the platform is heading as multi-agent systems become the default.
>
> Why a shared platform, and why AgentCore
>
> Before APEX, three applications were each on their way to building their own agent stack: Woody, Lens AI, and the ST Trading App. Left alone, each would have stood up its own runtime, wired its own identity, bolted on its own observability, and hardcoded its own model. We would have paid the same infrastructure tax three times and ended up with three stacks that could not share memory, tools, or evaluation.
>
> AgentCore resolves this problem by providing a platform capable of meeting the needs of an enterprise scale agentic deployment. We evaluated AgentCore against the requirements of a production platform: hosting model, cost model, whether it is model agnostic, scalability, governance, and enterprise support.
>
> Framework
>
> Hosting
>
> Cost Model
>
> Model Agnostic
>
> Scalability
>
> Governance
>
> Enterprise Support
>
> LangChain
>
> Self-Hosted
>
> Free/Enterprise
>
> Yes
>
> Manual
>
> DIY
>
> Community
>
> LangChain
>
> Self-Hosted/ LangSmith
>
> Free + LangSmith
>
> Yes
>
> Manual
>
> LangSmith
>
> Community
>
> CrewAI
>
> Self-Hosted/ CrewAI-Cloud
>
> Free/ Cloud
>
> Yes
>
> Limited
>
> Basic
>
> Community
>
> n8n
>
> Self-Hosted/ Cloud
>
> Free/ Pro
>
> No
>
> Moderate
>
> Workflow
>
> Community + Pro
>
> Frontier Model Direct
>
> Provider-hosted
>
> Per-token
>
> No
>
> Provider-Managed
>
> None
>
> Provider SLA
>
> Bedrock AgentCore
>
> AWS managed
>
> Pay-per-use
>
> Yes
>
> Automatic scaling
>
> Native Amazon Bedrock Guardrails and Policy
>
> AWS Enterprise SLA
>
> AgentCore provides us a managed platform rather than a library we would need to operate ourselves. It works with any open source framework, including Strands Agents, LangGraph, LangChain, LlamaIndex, CrewAI, Google ADK, OpenAI Agents SDK, and with any model whether or not it runs on Amazon Bedrock. It supports both the Model Context Protocol (MCP) and the Agent-to-Agent (A2A) protocol. That meant we didn’t need to choose between open source flexibility and AWS service security. This allowed us to standardize the platform layer while leaving each team free to pick its own framework and model.
>
> Five capabilities decided it for us:
>
> Managed infrastructure. There’s no cluster to operate. AWS handles scaling, patching, and availability, so our platform team focuses on agent capabilities instead of backend plumbing. AgentCore reached general availability (GA) in October 2025, and at GA all services added support for Amazon Virtual Private Cloud (VPC), AWS PrivateLink, AWS CloudFormation, and resource tagging.
>
> True model agnosticism. Claude, GPT-4.1, Amazon Nova, Mistral, and Llama are all reachable through a single platform. A team can plan with one model and execute with another, run a price-performance test by swapping providers, or move off a model that shipped a regression, without losing conversation context and without touching business logic.
>
> Automatic scaling. AgentCore runtime, a capability of Amazon Bedrock AgentCore, goes from zero to thousands of concurrent agent invocations with no capacity planning, with complete session isolation and execution windows up to 8 hours.
>
> Native guardrails and identity. Content filtering, personally identifiable information (PII) detection, and policy enforcement are managed capabilities rather than something each team reimplements. Policy in Amazon Bedrock AgentCore integrates with the Gateway to intercept every tool call in real time and converts natural-language rules into Cedar, the AWS open source policy language, so development, compliance, and security teams can author and audit rules without custom code. AgentCore Identity, a capability of Amazon Bedrock AgentCore, adds AWS Identity and Access Management (IAM) integration, VPC isolation, and encryption, so agents support your compliance requirements and can act on behalf of a user or on their own under defined access controls.
>
> AWS Enterprise Support. AWS Enterprise Support provides 24/7 support as well as a technical account manager (TAM) and account team relationship that helps customers influence the roadmap for products like AgentCore based on our needs.
>
> AgentCore uses consumption-based pricing with no upfront commitments or minimum fees. Each service is billed independently, so a team can adopt a single capability such as AgentCore memory, a capability of Amazon Bedrock AgentCore, without migrating its entire agent. Runtime billing is based on active CPU and memory consumption calculated per second, and CPU charges don’t accrue during I/O wait. This matters for agentic workloads, which typically spend 30–70 percent of their time waiting on model responses, tool calls, or database queries. With pre-allocated compute you would pay for that idle time. With AgentCore, you do not.
>
> Solution overview
>
> APEX is organized in layers, shown in Figure 1. At the top, end users interact with three applications: Woody, Lens AI, and the ST Trading App. Those applications talk to the APEX frontend, which exposes a framework so product teams can drop agentic capabilities into a user interface without rebuilding the connection to the backend each time. The APEX backend is where AgentCore does the work.
>
> Two infrastructure tracks sit alongside the backend. The WM infrastructure as code (IaC) Framework uses the AWS Cloud Development Kit (AWS CDK) and GitHub to provision and version platform resources, with guardrails defined in code. The MCP layer connects the platform to third-party and external access, including AWS Marketplace and partner systems, over a standard protocol rather than bespoke integrations.
>
> Users reach three applications through the APEX frontend SDK. The APEX backend runs on AgentCore (Runtime, Identity, Gateway, Memory, Observability) with an Orchestrator, a vector database for retrieval, model access through the Amazon Bedrock model catalog, and Amazon Bedrock Guardrails. The WM IaC Framework provisions resources through AWS CDK and GitHub, and the MCP layer connects external systems.
>
> Figure 1: APEX reference architecture
>
> Inside the backend, a request flows through these components.
>
> User Authentication and AgentCore Identity establish who is calling and what they are entitled to do. Identity and entitlements are woven into every agent invocation rather than checked once at the edge, so an agent acting on a user’s behalf carries that user’s permissions through every downstream tool and data call. Federation to your identity provider of choice is also important. We use Okta as our source of truth.
>
> The Orchestrator routes the request and consults the Woodmac Agent Registry, a single place to discover, share, and reuse agents, tools, and skills across the organization with built-in governance and approval workflows. This is how one team’s agent becomes available to another without copying code.
>
> AgentCore runtime hosts the agent code in a serverless, session-isolated environment. Inside the runtime we run AI Agents Studio (built on Amazon Quick with Strands Agents, LangGraph, CrewAI, n8n, Vertex, and OpenAI), so each team keeps its preferred framework. The runtime invokes models through the Amazon Bedrock model catalog, which is where model agnosticism becomes concrete: the agent points at a model by name and we swap providers without rewriting the agent.
>
> Tools are exposed to the agent as composable building blocks. The architecture shows how Wood Mackenzie uses a Code Interpreter tool for secure code execution and an Amazon Nova Act web tool for browser actions. These tools are reached through AgentCore Gateway, a capability of Amazon Bedrock AgentCore, which turns APIs, AWS Lambda functions, and existing MCP servers into agent-compatible tools and provides a single secure endpoint for discovery and invocation. The Gateway pulls from a Tools Repository for discovery and invocation, and supports IAM, OAuth 2.1, and API key authentication.
>
> Retrieval Augmented Generation (RAG) over a vector database grounds the agent in our own content, including unstructured documents, so responses are based on retrieved facts rather than the model’s parametric memory alone. We use Amazon Bedrock Knowledge Bases as a serverless and managed way to provide RAG to our agents.
>
> AgentCore memory gives the agent short-term and long-term context, so a conversation persists across sessions and agents can share state instead of each maintaining its own store.
>
> Amazon Bedrock Guardrails and Policy govern allowed prompts and intercept tool calls, enforcing content filtering, PII detection, and the Cedar-based rules described earlier.
>
> Observability and evaluation determine whether an agent survives in production. Agent output is non-deterministic, so the hard question isn’t does it work but can we tell when it stops working. AgentCore Observability, a capability of Amazon Bedrock AgentCore, emits telemetry in OpenTelemetry-compatible format to Amazon CloudWatch, covering session count, latency, duration, token usage, and error rates. Wood Mackenzie can then trace a single request from a session down to an individual span, with logs from each component surfaced at the right step instead of scattered across log groups. On top of that, AgentCore Evaluations, a capability of Amazon Bedrock AgentCore, gives us built-in evaluators for quality dimensions such as helpfulness, tool selection, and accuracy, plus custom model-based scoring, so we can score agents against real traffic.
>
> APEX Studio: The control plane
>
> The architecture described earlier is the runtime. APEX Studio is the back office that operates it, a single interface where a team builds, deploys, and monitors agents without touching the underlying infrastructure. It’s the human-facing control plane over AgentCore, and it’s how a team gets from idea to a live agent without filing a ticket for each step.
>
> The Studio dashboard, shown in Figure 2, surfaces the platform’s operational state at a glance, active agents, workflows, and connectors, along with recent deployments and their status, so an operator can see what is running in production and what is still in staging. Six capabilities cover the agent lifecycle.
>
> Agent Builder is template-driven agent creation, where a team configures an agent’s persona, its tools, and its guardrails rather than wiring those by hand. This is the Golden Path in practice: a new agent starts from a paved template, not a blank repository.
>
> Workflow Designer is visual multi-step orchestration with branching, loops, and human-in-the-loop steps, so a multi-step process is composed and reviewed in one place instead of encoded across scattered services.
>
> Connector Registry lets a team browse, configure, and publish MCP-compatible data connectors. It’s the operator’s view of the same gateway and tools layer described earlier, which keeps tool publishing governed and reusable across teams.
>
> Live Chat Testing provides real-time agent interaction for validation before a production deploy. This is where the evaluation discipline starts. An operator exercises the agent against real inputs before it reaches users, which is the first line of defense against the non-deterministic failures that stall most agent programs.
>
> App Deployment covers the full application lifecycle from build to production launch, and Monitoring Dashboard shows agent health, cost, latency, and accuracy metrics in one view, fed by AgentCore Observability and Evaluations. Together they close the loop from shipping an agent to watching how it behaves once it is live.
>
> Underneath the Studio is an embedded software development lifecycle (SDLC) integration we call vibe coding: a team can create an agent through natural language, with automated testing, a preview, and one-click production deployment. The point is the same one that runs through the whole platform: the operator expresses intent and the platform handles the build, the test harness, and the deploy, so the time from idea to a governed production agent is measured in hours.
>
> Figure 2: APEX Studio control plane
>
> The dashboard shows active agents, workflows, and connectors with recent deployment status, and exposes Agent Builder, Workflow Designer, Connector Registry, Live Chat Testing, App Deployment, and a Monitoring Dashboard over AgentCore.
>
> The single integration pattern that does the most work in APEX is the hub-and-spoke model we built on AgentCore Gateway, shown in Figure 3. Without it, every consumer would maintain a bespoke connection to every data service. With N consumers and M services, that is an N by M integration problem: each new application or agent multiplies the number of point-to-point connections we must build, secure, and maintain, and each connection reimplements the same cross-cutting concerns.
>
> The hub-and-spoke model avoids that. Every application and agent connects through one gateway instead of holding its own connection to each data service. On the consumer side, an internal analyst, a client chatbot, and a trading agent all speak to the same hub. On the data side, the gateway fans out to Lens Direct for analytics and curves, Short Term Trading for real-time execution, Digital Content for upstream models, and the P&amp;R Dataset calculators. Adding a new consumer or a new data service means wiring one spoke to the hub, not rebuilding the full mesh.
>
> Figure 3: Unified MCP Gateway
>
> Consumers (internal analyst, client chatbot, trading agent) connect through a single Amazon Bedrock AgentCore Gateway speaking the MCP protocol, which fans out to data services (Lens Direct, Short Term Trading, Digital Content, P&amp;R Dataset). Cross-cutting concerns are enforced once at the hub.
>
> The gateway speaks the Model Context Protocol (MCP), so it presents a consistent tool interface regardless of what sits behind each spoke. AgentCore Gateway turns existing APIs, AWS Lambda functions, and existing MCP servers into agent-compatible tools, and acts as a single secure endpoint for agents to discover and invoke those tools without custom integration code. It supports IAM, OAuth 2.1, and API key authentication, and AWS partner tools procured through AWS Marketplace can be imported into the gateway directly.
>
> Because traffic funnels through one hub, the cross-cutting concerns are enforced once at the gateway rather than re-implemented in every consumer or spoke: identity, observability, evaluation and guardrails, skills and tools, rate limiting, data protection, and compliance. A policy change applies everywhere the moment it lands at the hub, and every tool call inherits the same identity context, the same telemetry, and the same guardrails. This is also where the MCP server option matters for external access: exposing our data services through a governed MCP endpoint means partners can reach them through a single, controlled interface for direct AI-powered data access rather than through a sprawl of point integrations.
>
> Generative UI: Dynamic components with AG-UI, A2UI, and Strands
>
> A platform is only useful if the agent can surface its work to a user, and rebuilding a streaming, stateful interface for every agent would reintroduce the exact duplication APEX exists to remove. We solve the presentation layer the same way we solved connectivity: with shared protocols. The APEX frontend SDK is built on two complementary protocols, with CopilotKit providing the web components and tooling.
>
> AG-UI is the transport. It’s the bi-directional, event-driven runtime connection between an agentic backend and a user-facing application, carrying a stream of typed events such as token streaming, tool calls, and state updates over standard HTTP or Server-Sent Events. It works across stacks, from web to mobile to the command line.
>
> A2UI is the payload. It’s a declarative generative UI specification, originated by Google, that an agent uses to return UI as a JSON blueprint of components rather than text or executable code. The client renders each component from its own catalog of trusted, native widgets, which keeps the UI matched to the host application’s styling and avoids arbitrary code execution. AG-UI carries A2UI blueprints to the frontend, and CopilotKit supports A2UI as a launch partner. In short, A2UI describes what the agent wants to display, AG-UI delivers it, and the client renders it.
>
> The agents themselves are Strands agents running in AgentCore runtime. Strands integrates with AG-UI directly, and the combination gives us three capabilities that the ST Trading App, Lens AI, and Woody all reuse rather than rebuild.
>
> Streaming chat. AG-UI handles the streaming of messages between users and the agent, so a conversational surface is a configured component rather than a hand-built transport layer.
>
> Tool-based generative UI. This is where dynamic components come from. The agent does not return only text. AG-UI shares tool information with the client, and the client maps a tool invocation to a rendered component. When an agent calls a tool, the frontend renders the matching component with the tool’s arguments, so a curve-analytics request from Lens Direct or a real-time execution result from Short Term Trading comes back as a live widget rather than a wall of text. For richer cases the agent emits an A2UI blueprint and the client renders it from its trusted component catalog, so the agent can compose an interface, a chart, a form, a result card, without the frontend hardcoding it in advance. A tool the agent already exposes becomes a UI element with a small render binding on the client, which is the composable-building-blocks principle applied to the interface: a single widget or a full workflow, assembled from the same parts.
>
> Shared state. Strands agents are stateful, and AG-UI synchronizes that state in both directions. The agent sees changes the user makes in the interface, and the interface reflects state the agent updates, so a user editing a parameter and an agent revising a calculation stay in sync without custom wiring.
>
> Deployment follows the standard AgentCore path. The Strands agent is configured and launched onto AgentCore runtime, which exposes the POST /invocations interaction endpoint and a GET /ping health check. Authentication is handled through AgentCore Identity using an OAuth authorizer backed by Amazon Cognito, so the same identity model that governs tool calls at the gateway also governs the UI session. The frontend then connects to the deployed runtime endpoint with a bearer token, and the generative UI is live in production.
>
> The result is that a team adds a new agent-backed feature by writing agent logic and binding tools and component blueprints, while streaming, state synchronization, identity, and the production runtime all come from the platform.
>
> AG-UI in Lens: Interactive AI on a live dashboard
>
> The clearest example is Synapse AI, the generative AI assistant embedded in our Lens application. A user viewing the Lens Power Summary dashboard can open the assistant in a side panel and ask a question in plain language, such as which countries have the most renewable capacity. The agent does not answer from a generic web search. It calls a tool, extractWidgetConfig, that reads the configuration and data of the ranking widgets already on the dashboard the user is looking at, then returns a ranked table of solar and wind capacity by country rendered inline in the conversation.
>
> This is AG-UI doing exactly what it is for. The agent’s reasoning steps and tool calls stream into the panel as typed events as they happen, so the user sees the agent think and then act rather than waiting on a spinner. The result comes back not as a paragraph but as a structured table the agent composed, rendered by the client from its component catalog. And because the assistant reads the dashboard’s own widget state, the response is grounded in the data the user already trusts, not a disconnected query. The interactive assistant is a configured surface on top of a Strands agent, so Lens got a grounded, streaming, in-context analyst without building a transport layer, a state-sync mechanism, or a rendering pipeline of its own.
>
> Figure 4: Synapse AI inside Lens
>
> The user asks a question against the Power Summary dashboard. The agent streams its reasoning, calls the extractWidgetConfig tool to read the dashboard’s ranking widgets, and renders a ranked solar-and-wind capacity table inline in the assistant panel.
>
> Agentic flow in Woody: Orchestrating tools into a deliverable
>
> Woody, our internal Wood Mackenzie application, shows the same protocol carrying a longer-running workflow that chains several tools into a finished deliverable. In one flow, an analyst gives Woody a single instruction: research the impact of the Iran conflict on oil prices using both web sources and the Lens Direct dataset, generate charts, and produce a PowerPoint presentation.
>
> What follows is the agent planning and then executing across multiple tools. It first reasons about the task and checks which tools it has available, then uses them in sequence: a web search agent tool for open source research, the Lens Direct MCP server for our proprietary data, a Vega-Lite charting tool to generate the visualizations, and a PowerPoint generator to assemble the output. The agent streams its reasoning and its access status as it goes, web research complete, Lens Direct data retrieved, then delivers a research package: four interactive charts covering the oil price trajectory, supply disruption and buffer mechanisms, a price-scenario comparison, and Strait of Hormuz flow, plus a downloadable 15-slide presentation. One natural-language request became a coordinated multi-tool workflow ending in an artifact the analyst can use directly.
>
> Two things in this flow matter for the platform argument. First, the agent mixes a public web tool, a proprietary MCP data connector, a charting tool, and a document generator in a single run, and

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。