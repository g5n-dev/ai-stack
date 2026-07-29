---
title: "Generate Autonomous Business Insights with AI Agent and MCP Servers"
date: 2026-07-30T06:16:28+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "Prompt 工程", "Advanced (300)", "Amazon Bedrock AgentCore", "Technical How-to", "博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:4438e77af0996923913d257d98a5d1c3fc6dfa6207f33033e4849a0cd45a1d34"
source_payload_sha256: "sha256:2e43d5575d29c20c0079c634d0a0a695c9fb845ad3e9e76977e0a9988564470b"
observation_id: obs_89bc6f5296e6a019d24b24118d840af109abf990309c044a5261a60244392ad2
event_id: evt_2da90263a6fff3edbb8c2f8efacf2aea9cdf375929b707ce0be0dfa2f145cdcc
revision_id: rev_6a8c574b0f2b1873218323169f4032993b154d401f4365c6d103c7bd96cfdf51
source_published_at: 2026-07-29T15:34:18Z
first_seen_at: 2026-07-29T22:38:52Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: true
source_truncation_reason: "crawler_feed_content_limit"
source_support: 1.0
source_title_chars_original: 67
description: "当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。"
external_url: https://aws.amazon.com/blogs/machine-learning/generate-autonomous-business-insights-with-ai-agent-and-mcp-servers
parent_observation_id: null
last_seen_at: 2026-07-29T22:15:46.811156Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/generate-autonomous-business-insights-with-ai-agent-and-mcp-servers](https://aws.amazon.com/blogs/machine-learning/generate-autonomous-business-insights-with-ai-agent-and-mcp-servers)

## 来源摘要/节选

> A Monday morning problem
>
> Sarah Chen manages 12 assembly lines and 2,000 machines. Before her 10 AM production review, she needs one answer: Which lines need attention this week?
>
> Simple question. Painful journey.
>
> She starts in the IoT dashboard. Line 4’s motor temperature is running 12°C above baseline — has been for three days. Calibration drift or bearing failure? The dashboard shows signals, not causes. So she pivots to the ERP system for maintenance history. Machine 42 had a bearing replaced eight months ago. Warranty says 12 months, but the operating hours log — buried in a separate historian database — shows it’s been running at 130% rated capacity since January.
>
> That context exists nowhere in the IoT dashboard.
>
> She pulls 30-day OEE trends. Line 4’s availability dropped from 94% to 87%. Line 9’s throughput also dipped 6%. Related? They share a coolant loop, but that relationship isn’t modeled in any system. She checks defect rates. Line 4’s scrap jumped 2.3% last Tuesday. Line 9 shows nothing — yet. Is the coolant theory wrong, or is Line 9 just lagging?
>
> She emails three supervisors. By 11:15 AM, she finally has a confident answer.
>
> Two floors down, Line Supervisor Raj Patel is doing the same exercise for Line 7 — except he can’t access the analytics dashboard. He’s working from a PDF export that’s three days stale. Maintenance Technician Priya Nair just wants to know if the vibration she flagged on Machine 42 last week has gotten worse. The data exists. She doesn’t have credentials to see it. She asks Raj. Raj asks Sarah’s analyst. A CSV arrives four hours later. By then, Priya has moved on to her next work order.
>
> Three people. Three different access levels. Five disconnected systems. The same underlying data. Hours of manual stitching, context-switching, and waiting—for answers that should take seconds. The data existed but it just couldn’t speak in one voice.
>
> The problem: Data-rich, insight-poor
>
> The average enterprise runs five to eight operational and analytical systems daily. Each has its own login, its own query interface, and its own access model. When a manager needs a cross-system view — the kind that actually drives decisions — a human being becomes the integration layer. Traditional BI dashboards show what happened yesterday. Single AI assistants can answer isolated questions. But neither can autonomously coordinate across your entire technology stack to deliver contextual, actionable intelligence exactly when needed. Managing complex ETL pipelines, fragmented data stores and access patterns, and multiple AI assistants and agents lead to additional challenges for end users. Custom multi-agent frameworks can theoretically span the full stack, but building one from scratch requires months of engineering: custom connectors, session isolation, memory infrastructure, security code, scaling logic, and orchestration logic — all before the first business question gets answered.
>
> Businesses should not need an engineering team just to ask questions about their own data. And the real cost is not engineering time — it is the decisions made on stale, partial information while the right answer was sitting in a system nobody had time to check.
>
> The solution: Configuration, not code
>
> Amazon Bedrock AgentCore flips the model. Instead of building an autonomous intelligence system from the ground up, you configure one. Amazon Bedrock AgentCore handles orchestration, security, memory, and scaling. You bring your data sources and your business rules. The result is a system where Sarah, Raj, and Priya can each ask natural language questions and get synthesized and personalized answers from across the entire technology stack — without knowing which system provided which piece of the answer.
>
> The model is three steps:
>
> Connect your existing systems using pre-built MCP server connectors — no custom integration code.
>
> Define who can see what using plain-English policy rules that Amazon Bedrock AgentCore translates into enforcement logic.
>
> Ask questions in natural language and let Amazon Bedrock AgentCore orchestrate the rest.
>
> Architecture overview
>
> The architecture is organized into five layers, each building on the one below. The layered structure is intentional: it separates user-facing intelligence from orchestration, from tool execution, from data access — keeping each layer independently scalable and replaceable.
>
> Users at the top, Amazon Bedrock AgentCore as the center of gravity, pre-built MCP server connectors in the middle, and the data infrastructure at the foundation. Every user interaction flows through Amazon Bedrock AgentCore — through authentication, policy, memory, and the Agent — before reaching data sources.
>
> Figure 1 — Autonomous BI architecture using Amazon Bedrock AgentCore
>
> The architecture follows a layered design, where a user queries in natural language through Amazon Bedrock for intent classification and response synthesis, then into Amazon Bedrock AgentCore, where the agent orchestrates execution across isolated run-times, a gateway, identity and policy enforcement, persistent memory, and a governed tool registry. Before selecting and routing to data connectors, the agent looks up the Semantic Layer powered by SageMaker Data Catalog, which exposes the right data sources — enabling the agent to understand what data exists across the enterprise and where it resides without hard-coded logic. Equipped with this metadata, the agent routes the query to the appropriate pre-built MCP server connector (equipment, IoT telemetry, supply chain, analytics, or custom low-code), which in turn pulls data from the underlying infrastructure — SageMaker Lakehouse, Redshift, S3 Tables, OpenSearch or Aurora. This separation of metadata discovery from data retrieval means new sources can be on-boarded by registering them in the Data Catalog rather than writing custom integration code, keeping the system extensible through configuration alone. The complete working implementation is available on GitHub.
>
> How it works
>
> Each layer of the architecture corresponds to a distinct set of capabilities. Below is a guided tour through each component, grounded in what Sarah, Raj, and Priya actually experience.
>
> Data infrastructure
>
> The data foundation is built on Amazon SageMaker Lakehouse — an open lakehouse architecture fully compatible with Apache Iceberg that unifies data across Amazon S3 data lakes (including S3 Tables), Amazon Redshift data warehouses, and operational data stores connected through zero-ETL integrations. The agent accesses this unified data through a combination of pre-built and custom MCP servers:
>
> Pre-built MCP servers (ready to configure): Amazon Redshift MCP server — warehouse queries for supply chain inventory and OEE analytics AWS S3 Tables MCP server — Iceberg-format historical data in S3 Amazon Aurora PostgreSQL MCP server — operational data for equipment registry and maintenance history
>
> Custom MCP servers (for services without a pre-built option): Custom MCP servers (for services without a pre-built option)- IoT Telemetry MCP server — queries Amazon Timestream for real-time sensor time-series (vibration, temperature, pressure). Built with FastMCP framework. Quality Analytics MCP server — queries Amazon OpenSearch Serverless for defect pattern matching and semantic search across quality inspection documents. Semantic Layer MCP server — queries SageMaker Data Catalog metadata to help the agent discover which data sources are relevant before calling them.
>
> Building a custom MCP server for a service like Timestream requires only defining the tool interface and delegating to the AWS SDK:
>
> from mcp.server import FastMCP
>
> mcp = FastMCP("IoT Telemetry Server", port=8002)
>
> @mcp.tool(description="Get sensor readings for a specific machine")
>
> def get_sensor_readings(machine_id: int, metric: str = "temperature", days: int = 7) -&gt; str:
>
> # Validate input, query Timestream via boto3, return JSON
>
> ...
>
> Once registered, a custom MCP server behaves identically to a pre-built one — the agent discovers its tools through the same MCP protocol and calls them the same way. This means enterprises can start with pre-built connectors for common services and add custom servers incrementally for specialized or legacy systems, without changing the agent or the orchestration logic.
>
> MCP servers: Pre-built connectors to your data
>
> The Model Context Protocol (MCP) is an open standard that defines how AI agents discover and invoke tools. In this architecture, each domain of your business — equipment status, IoT telemetry, supply chain, quality management — is represented by a dedicated MCP server. Each server exposes a set of typed tools: get_equipment_status, detect_anomaly, check_parts_inventory. The agent calls these tools, the way a developer calls an API. What makes this practical for enterprises is that you do not build these servers from scratch. Amazon Bedrock AgentCore provides pre-built MCP connectors for common systems: Amazon Redshift, Amazon Aurora, Amazon OpenSearch, and third-party systems through OAuth. For proprietary or custom systems, low-code MCP server templates on Amazon Bedrock AgentCore Runtime reduce the effort to configuration rather than development.
>
> Connectivity options span the full spectrum of enterprise systems:
>
> Semantic store through Amazon SageMaker Catalog for right data source identification, selection and querying.
>
> Relational databases: Amazon Aurora, RDS. Which bring in the operational data.
>
> Streaming services like Amazon MSK for real-time IoT sensor feeds and event streams to SageMaker Lakehouse.
>
> Vector stores: Amazon OpenSearch Service for supporting semantic search, real-time vector embedding with Amazon MSK, and hybrid keyword-vector queries on unstructured data in Amazon S3.
>
> Data Warehouses and Lakehouses with Zero ETL features to replicate data from various data stores to Amazon S3 Tables/Amazon Redshift in SageMaker Lakehouse. Thus storing multi-year historical records.
>
> Third-party SaaS: REST or GraphQL APIs via the Amazon Bedrock AgentCore Gateway OAuth integration (for example, Salesforce, SAP, ServiceNow).
>
> MCP servers can run in stateless mode (default, each call is independent) or stateful mode for multi-step operations that need to maintain intermediate results within a session.
>
> MCP servers: Advantages and trade-offs
>
> Advantages Loose coupling — each MCP server is deployed independently. Updating the CRM connector does not touch the IoT connector. Domain encapsulation means each server owns its schema and authentication context. Pre-built connectors for AWS-native services mean most enterprises can connect their core data sources within hours. The open MCP standard avoids vendor lock-in — MCP-compatible servers work with Amazon Bedrock AgentCore.
>
> Trade-offs Custom or legacy systems without a pre-built connector require a low-code template configuration, which adds a one-time setup step. Stateful MCP servers introduce session affinity requirements that need careful planning for horizontally scaled deployments. Each additional MCP server is one more endpoint to monitor and version. Consider using gateway to connect to MCP servers with or without pre-built connectors.
>
> Amazon Bedrock AgentCore Gateway: Unified entry point and intelligent routing
>
> The Gateway is the single entry point through which every agent-to-tool call flows. When a new MCP server is registered, the Gateway performs a protocol handshake and indexes its available tools — their names, input schemas, and descriptions. The agent does not need to know the address of a MCP server. It calls tools by name through the Gateway, which routes the request to the appropriate server. The Gateway implements a three-tier caching strategy designed to reduce latency for repeat queries. Organization-scoped cache holds reference data that all users share — equipment catalog records, product lists, threshold values — and refreshes daily. User-scoped cache holds recent query results that are personal to a specific user and respects their access context. The Policy engine determines which responses can be shared across users and which must remain isolated. For Precision Manufacturing, this means that a Plant Manager’s query about overall fleet status can be partially served from cache, while Priya’s query about Machine 42 is scoped to her.
>
> Amazon Bedrock AgentCore Runtime: Isolated execution for every user
>
> Amazon Bedrock AgentCore Runtime deploys agents to Firecracker microVM environments delivering isolation and security — the same technology that powers AWS Lambda and AWS Fargate — with no servers to manage and automatic scaling. When Sarah submits her query, Runtime spins up a dedicated microVM. Raj’s session runs in a separate microVM. Priya’s in a third. No shared filesystem, no shared memory, no shared networking. When the session ends, the microVM is destroyed. Multi-tenancy is a runtime attribute, not a software convention.
>
> In our implementation: deploy/agentcore/deploy_all.py provisions the full stack — Cognito identity, Gateway with Lambda tool targets, Cedar policies, and request/response interceptors. Amazon Bedrock AgentCore Gateway then handles session isolation, identity propagation, and policy enforcement automatically, with no changes to the agent code itself.
>
> Amazon Bedrock AgentCore Identity: Authentication that propagates
>
> Amazon Bedrock AgentCore Identity provides robust identity and access management so that agents can access resources or tools either on behalf of users or themselves, with pre-authorized user consent, minimizing the need for custom access controls and identity infrastructure development. Identity integrates with your existing providers (Okta, IAM, Cognito, OAuth 2.0 systems) and propagates user context through the entire call chain using the Mcp-Session-Id header. Two flows are supported: agent-level access (service-to-service) and user-delegated access (agent acts on behalf of a specific user with their scoped token). In practice for Precision Manufacturing: – Sarah’s token (from Cognito) grants access to all three plants, all 12 lines. – Raj’s token scopes to Plant 2, Line 7 only. – Priya’s token scopes to Machine 41-45. These restrictions come from the IdP. Amazon Bedrock AgentCore propagates them through the call chain and enforces them automatically. If Raj’s scope changes in Cognito, the system reflects it immediately without code changes.
>
> In our implementation: src/identity/models.py defines three user identities with explicit scopes. In production, these come from Cognito claims that AgentCore propagates automatically.
>
> Amazon Bedrock AgentCore Policy: Authorization in plain English
>
> Policy in Amazon Bedrock AgentCore integrates with Gateway to intercept every tool call in real time, verifying agents stay within defined boundaries. Teams create policies using natural language that automatically convert to Cedar — the AWS open-source policy language — with automated reasoning that validates policies for completeness before deployment. Policy enforcement happens at the Gateway level, intercepting every tool call before execution. Rules operate across multiple dimensions: user role, geographic scope, data classification, time of day, and specific tool parameters. A policy might read: “Line supervisors can call get_equipment_status only for lines within their assigned plant.” When Raj asks about Line 4, the Gateway evaluates his identity against this rule and returns a deny decision before the MCP server is ever called. Every decision is logged to AWS CloudTrail.
>
> In our implementation: Cedar policies deployed to the Amazon Bedrock AgentCore Gateway enforce fine-grained access at the infrastructure level — before Lambda tool targets execute. When Raj queries Line 4, the Gateway’s Policy Engine evaluates his JWT claims against the Cedar rules and returns a deny. The MCP server is not contacted. For local development without a deployed Gateway, src/identity/gateway_hook.py simulates this enforcement using Strands Agents’ BeforeToolCallEvent hook.
>
> Sequence diagrams: Access control flow
>
> The following diagrams illustrate the end-to-end access control flow implemented by Amazon Bedrock AgentCore Gateway. They show how user identity (through JWT claims from Cognito) flows through the REQUEST Interceptor, gets evaluated by the Cedar Policy Engine, and determines whether an MCP tool is invoked or the request is denied — all before data leaves the system.
>
> Diagram 1: End-to-end access control sequence
>
> This UML-style sequence diagram shows the complete lifecycle of a request, from user authentication through Cognito, to the agent’s LLM reasoning, through the Amazon Bedrock AgentCore Gateway’s enrichment and authorization layers, and finally to tool execution or denial.
>
> Key observations:
>
> Authentication: Cognito issues a JWT with custom claims (role, line_scope, plant_scope, equipment_scope) that encode the user’s data boundaries.
>
> Enrichment: The REQUEST Interceptor decodes the JWT and injects user_context into the tool call arguments — the agent/LLM does not see or control this step.
>
> Authorization: Cedar evaluates the enriched request against policies. A permit_all baseline allows access, while forbid_* rules check whether the requested parameter falls within the user’s scope.
>
> Execution vs Denial: If Cedar allows, the Gateway forwards to the Lambda tool target. If Cedar denies, the MCP server is not invoked — avoiding data exposure.
>
> Synthesis: The agent receives either tool results or a deny message, and composes a natural-language response. On denial, it explains the boundary and suggests alternatives within scope.
>
> Figure 2 — Amazon Bedrock AgentCore Gateway fine-grained access control sequence diagram
>
> Three personas — same interface, different access
>
> This comparison diagram demonstrates how the same agent interface produces different outcomes for different users. Each row represents a persona with a horizontal left-to-right flow through the system components. Personas:
>
> Sarah Chen (Plant Manager) — Full access. Queries are not denied because her role has the ‘has_full_access’ attribute, bypassing all forbid rules.
>
> Raj Patel (Line Supervisor) — Scoped to Line 7, Plant 2. Attempts to access Line 4 data are denied at the Cedar layer. The Lambda tool is not invoked.
>
> Priya Nair (Maintenance Technician) — Scoped to Machines 41-45. Attempts to access Machine 72 are denied. The agent suggests checking Machine 42 instead.
>
> Amazon Bedrock AgentCore components highlighted: The purple-shaded region in the diagram encloses the two Amazon Bedrock AgentCore-managed components: the Gateway (with its REQUEST Interceptor) and the Cedar Policy Engine. These operate server-side, external to the agent process, making sure that neither the LLM nor application code can bypass authorization.
>
> Figure 3 — Same agent, same interface, different data access (Amazon Bedrock AgentCore Gateway enforces Cedar policies at the parameter level)
>
> Key security properties illustrated
>
> Deterministic Authorization: Cedar evaluation is pure logic — same input produces the same output. The LLM cannot influence the policy decision regardless of prompt injection.
>
> Fail-Secure: If the interceptor crashes, context is not injected. Cedar has nothing to permit, so the result is DENY (deny-by-default).
>
> MCP Server Isolation: Denied requests do not reach the MCP server. The tool Lambda is not invoked. Data processing does not occur. Compute is not wasted.
>
> Graceful Degradation: The agent receives the deny message as a tool result and intelligently responds: explains what it CAN access, suggests alternatives, and does NOT retry the denied call.
>
> Amazon Bedrock AgentCore Memory: Context that persists
>
> Amazon Bedrock AgentCore Memory enables agents to learn and adapt from experiences, building knowledge over time, with support for episodic memory that creates more human-like interactions. Memory operates at two levels: Short-term memory captures turn-by-turn context within a single session. When Priya asks “Show me vibration trends on Machine 42,” then follows with “Compare that to last week,” the second question is understood in context without repeating the machine ID. Long-term memory persists selected insights across sessions. Amazon Bedrock AgentCore automatically extracts and stores preferences, recurring query patterns, and session summaries organized into namespaces:
>
> User-scoped: Priya’s preferred units, her assigned equipment list.
>
> Team-scoped: The maintenance team’s standard anomaly thresholds.
>
> Organization-scoped: Equipment catalog, site codes, product definitions. Retrieval passes through Policy — even if an insight exists in long-term memory, it will not surface to a user who lacks access to the underlying data.
>
> In our implementation: src/memory/manager.py provides two memory tiers — SessionMemory for turn-by-turn context within a conversation, and MemoryManager for long-term insights organized into user-scoped and team-scoped namespaces. Priya’s long-term memory retains last week’s Machine 42 vibration baseline (3.8 mm/s), so when she asks “has it gotten worse?”, the agent compares against that stored reading without repeating context. In production, Amazon Bedrock AgentCore Memory persists these insights across sessions and enforces policy on retrieval — a user only sees memories derived from data they’re authorized to access.
>
> Amazon Bedrock AgentCore Registry: Governed tool discovery
>
> Amazon Bedrock Agent Registry enables organizations to discover, share, and reuse agents, tools, and agent skills across the organization through a governed catalog with publish-and-approve workflows. New MCP servers enter the Registry in draft state. Administrators review and approve them. Once approved, the agent automatically discovers the new tools on the next invocation — no redeployment needed. The Registry also enables versioning: an updated connector can be staged alongside the current version, tested, and promoted without disrupting live sessions. This governance model means the system grows incrementally. New data sources, new tools, and new connectors are added through a structured publish-and-approve workflow rather than code changes to the orchestration layer.
>
> In our implementation: The Semantic Layer MCP server (src/servers/semantic_layer_server.py) maintains a registry of data sources — each entry declares its available tools, glossary terms, data origin, and refresh frequency. The agent calls discover_data_sources first, which keyword-matches against the catalog and returns ranked recommendations. Onboarding a new data source means adding one entry to the DATA_SOURCES registry — no agent logic changes, no redeployment of other servers.
>
> Three users, one system, three different views
>
> The real test of any multi-tenant system is not whether it works for one user — it is whether it works correctly for many users simultaneously, with each seeing exactly what they should and nothing more. Here is how the same Amazon Bedrock AgentCore deployment serves Sarah, Raj, and Priya differently.
>
> Sarah asks: “Which assembly lines need attention this week?”
>
> Amazon Bedrock AgentCore Runtime creates a microVM for Sarah’s session. The Gateway authenticates her through Okta — role: Plant Manager, scope: all associated assembly lines. The agent classifies the intent as multi-source and operational. It calls the Equipment MCP Server (get_equipment_status, all plants) and the IoT Telemetry MCP Server (detect_anomaly, all lines) in parallel. Policy evaluates each call: Sarah’s role permits all of them. Memory recalls that Sarah prefers severity-ranked output. The synthesized response — a ranked list of assembly lines with supporting evidence from both equipment and sensor data — arrives in seconds.
>
> Raj asks: “What’s the current status of Line 7?”
>
> Raj’s session runs in a separate microVM. His Okta token scopes him to Plant 2, Line 7 only. The agent routes the same tool calls to the Equipment and IoT MCP servers — but Policy intercepts the calls and enforces the scope restriction. Line 7 data returns. Lines 1 through 6 and 8 through 12 do not. The Gateway’s user-scoped cache serves part of this response from Raj’s recent query history, reducing latency. Raj sees a precise, line-specific

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。