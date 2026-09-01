---
title: "Manage agents, tools and skills at scale with AWS Agent Registry"
date: 2026-09-01T18:08:38+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "Amazon Bedrock AgentCore", "Announcements", "Expert (400)", "博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:5d3fee23da4795f52058e8a073d6d6e75e20e9c90ece8ba9df29469c4e909788"
source_payload_sha256: "sha256:df2f7ea9a43d70b1c9e7d025d421cffc0449d8b05d45e3d9608e4ec627f79dd9"
observation_id: obs_38765f3001f64af7cbf0caf63000a60437f98e23a031bc6694bd499a604250b5
event_id: evt_71d8c7b0aa6e6f4bc6467d3af8a3beedeb3c83b02a1cc416f515ec34a00005ac
revision_id: rev_c16fb9f80d3f56e669012dbb093c71a9d9157b8e3599c09b3b381c0d1e2c3f6d
source_published_at: 2026-08-31T19:18:09Z
first_seen_at: 2026-09-01T10:06:00.265990Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: true
source_truncation_reason: "crawler_feed_content_limit"
source_support: 1.0
source_title_chars_original: 64
interpretation_sha256: "sha256:320d9ca2cdb037738bdde709cece39b63c93abb0018ee9fe61a52b9cdce81532"
description: "这是一篇介绍 AWS 官方解决方案的博文，目标是帮助企业在大量使用 AI 代理、工具和技能时解决发现困难和治理缺失的问题。该方案通过提供统一的注册、搜索和管控目录，让不同团队能够复用已有资源并追踪其生命周期。"
external_url: https://aws.amazon.com/blogs/machine-learning/manage-agents-tools-and-skills-at-scale-with-aws-agent-registry
parent_observation_id: null
last_seen_at: 2026-09-01T10:06:00.265990Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/manage-agents-tools-and-skills-at-scale-with-aws-agent-registry](https://aws.amazon.com/blogs/machine-learning/manage-agents-tools-and-skills-at-scale-with-aws-agent-registry)
- **发布域名**: aws.amazon.com

## 要点解读

### 这是什么

这是一篇介绍 AWS 官方解决方案的博文，目标是帮助企业在大量使用 AI 代理、工具和技能时解决发现困难和治理缺失的问题。该方案通过提供统一的注册、搜索和管控目录，让不同团队能够复用已有资源并追踪其生命周期。

### 用在哪里

适用于已开始在生产环境中规模化部署 AI 代理的组织，尤其是多个团队并行建设、缺少统一资源清单和审核流程的企业。管理员可以用它来配置访问规则和合规标识，开发者可以用它来搜索和发现组织内已有的代理或工具。

### 可以推断的

推测：在代理数量较少时，团队通常靠文档或口头传播来共享工具，但随着规模增长，这种方式难以维持，需要引入结构化的注册机制来降低重复开发的风险。

推测：该方案的核心价值在于将治理和搜索两个需求分离，让管理员拥有完整的管控视图，同时让普通用户获得经过筛选、可信赖的资源列表。

## 来源摘要/节选

> Most organizations scaling their use of agents and tools hit the same challenges. Teams build in isolation, with no shared record of what exists, who owns it, or whether it’s been reviewed. The problem has moved from building agents and tools to discovering and governing them. AWS Agent Registry is purpose-built to solve this. Now generally available, it gives teams a single, searchable, governed catalog for agents, tools, skills and custom resources in their environment.
>
> In this post, we cover what Registry is, walk through its core publishing, curation, and discovery workflows, explore enterprise considerations, and look ahead at what’s next.
>
> Why do enterprises need a registry
>
> As organizations scale their agentic AI systems, three key challenges emerge.
>
> No authoritative inventory
>
> When every team maintains their own collection of agents and tools in isolation, there’s no single record of what exists, who owns it, or whether it’s still actively maintained. The result is duplicative effort, version drift, and an ever-growing sprawl of untracked capabilities scattered across the organization.
>
> No cross-team discovery
>
> Even when great tools, agents, and skills exist, they go unused because developers on other teams can’t find them. Without a searchable catalog, the default is to rebuild what already exists. That’s wasted engineering effort, redundant infrastructure to maintain, and ongoing operational cost that scales with every team that builds in isolation.
>
> No governance or audit trail
>
> Without a central registry, there’s no way to track who has access to which agents, tools, and skills, whether they’ve passed security review, or how to trace failure back to specific version and owner. At enterprise scale, each registered agent, tool, or skill needs an owner, a clear lineage, and an audit trail.
>
> AWS Agent Registry addresses all three: it provides a central, searchable catalog where teams register agents, tools and skills, discover what already exists across the organization, and apply governance through access control, lifecycle tracking, and approval workflows.
>
> What is AWS Agent Registry
>
> As an agentic system grows from a handful of tools to hundreds, finding what already exists and trusting what you find becomes the bottleneck. AWS Agent Registry alleviates that bottleneck. It gives teams a single, governed catalog to register, discover, and manage AI agents, tools, and capabilities with built-in semantic search and access control.
>
> Internally, Registry operates across two complementary planes:
>
> The Governance Plane.
>
> The Governance Plane is the comprehensive agents, tools, and skills that are registered. It’s designed to be the authoritative store for resources within its defined scope, regardless of their lifecycle state.
>
> This is where admins configure the rules that shape how resources are managed, such as:
>
> Compliance and security signals – metadata that tracks whether a resource has passed security review, meets regulatory requirements, or carries known risks.
>
> Discovery policies – entitlement-based search rules that control which consumers can see which resources based on their role or team.
>
> Custom metadata schemas – organization-specific fields (for example, cost center, data classification, SLA tier) that standardize how teams describe their resources.
>
> Over time, the Governance Plane will surface richer governance signals, giving admins a single view into the compliance and security posture of their entire agentic landscape.
>
> The Discovery Plane.
>
> The Discovery Plane is what consumers interact with day to day. It presents a curated, high-performance view of only the resources that have passed the organization’s approval bar.
>
> Key characteristics:
>
> Curated, not comprehensive – only records approved by an admin or curator appear here. Draft, rejected, or shadow resources are not visible to consumers.
>
> Built for scale – supports high-throughput queries so agents and developers can search programmatically without hitting rate limits.
>
> Semantic and lexical search – consumers find resources by intent (“find me a tool for ticket routing”) or by exact name, across the full approved catalog.
>
> Trust signals, not governance details – surfaces summarized compliance and security indicators framed to make decisions of using it rather than raw governance data.
>
> Together, the two planes separate concerns cleanly: admins get comprehensive visibility and policy control through the Governance Plane, while consumers get a fast, governed search experience through the Discovery Plane that only shows resources ready for use. Some of the features described earlier are forward looking and are detailed in a later section.
>
> What can be cataloged in the Registry
>
> Registry supports four record types:
>
> MCP – Model Context Protocol server, its tools, resources, and prompts.
>
> Agent – Agent2Agent (A2A) agent card defining agents and their skills.
>
> Skill – agent skill definitions in markdown files and associated code/packages.
>
> Custom – Custom descriptor which must be valid JSON.
>
> The following diagram gives an overview of Registry, its capabilities, and access surfaces.
>
> Figure 1: Overview of AWS Agent Registry and its access surfaces
>
> What customers are saying
>
> Customers and Partners across industries, segments, and geographies are already seeing the value of the AWS Agent Registry for solving the discoverability, governance, and operational challenges that emerge as organizations scale to managing hundreds or thousands of AI agents. Companies like Sony are using it to reuse agent patterns across business units. Mitsubishi Electric are looking to give developers a single place to discover and trust what they build against.
>
> For companies like Southwest having a centralized way to discover and govern agents helps teams move faster with confidence, reducing redundancy, preventing sprawl, and scaling innovation in a way that’s sustainable for the enterprise.
>
> “At Southwest Airlines, we’re building agentic AI tools and autonomous agents to streamline operations across our 70,000+ employees and enhance the experience for the millions of Customers we serve every day. We went from dozens of agents and tools scattered across multiple technology teams with no shared record of what existed to a single, governed catalog that the entire organization trusts. AWS Agent Registry gives our platform team complete visibility into what’s deployed, who owns it, and whether it’s been reviewed. Our developers now find approved capabilities through semantic search in seconds instead of rebuilding what another team already built. Registry cut duplicative development effort significantly and became the backbone of how we govern agentic AI.”
>
> — Lauren Woods, CIO/EVP, Southwest Airlines
>
> And for customers like PepsiCo, having a system of record for discovery and usage becomes critical.
>
> “Agent Registry solves that. It gives teams a centralized way to discover, govern, and reuse agents, tools, and integrations across the enterprise. Customers like PepsiCo are already thinking about this at scale.”
>
> — Athina Kanioura, Chief Strategy &amp; Transformation Officer, PepsiCo
>
> At Syngenta, the Registry became the foundation of their AI agent governance strategy, providing a centralized catalog that eliminates redundant rebuilding across teams.
>
> “At Syngenta, we built our AI agent governance on AWS Agent Registry. It gives our teams a single, trusted catalog of AI agents, tools, and skills. Teams publish once, then discover and reuse what already works – instead of rebuilding agents, connectors, and business procedures from scratch. We register, review, and approve every capability before sharing it across the organization, retaining clear ownership, versioning, and control over security and access.”
>
> — Sandeep Rayasa, Enterprise Architect, Data and AI
>
> “As a leading software and AI solutions to telecom industry, Amdocs is an early adopter of AWS Agent Registry. By integrating it into our aOS Cognitive Core platform, we gain a unified view of agent assets across diverse environments while streamlining governance, compliance, and lifecycle management. The Registry’s framework-agnostic design aligns with our open platform strategy and enables us to deliver a trusted control plane for managing large-scale agent ecosystems, accelerating AI adoption across the telecom industry.”
>
> — Ron Dublero, Cognitive Core, Chief Software Architect, Amdocs
>
> AWS Partner perspectives
>
> As the number of agents grow across multiple cloud environments, managing their lifecycle, preventing duplication, and governance becomes operationally critical. With teams building agents across AWS, the Registry is the centralized governance layer that standardizes how agent records are shared, discovered, and governed.
>
> “We see great value with AWS Agent Registry at our enterprise clients. It manages agent skills consistently across systems, while allowing for customized integration with their existing technology landscape. Beyond accelerating adoption, the centralized registry helps mitigate a common, emerging operational risk at scale: agent sprawl.”
>
> — Dr. Binqi Zhang, Managing Director, PwC Australia
>
> “As agents proliferate across an organization, it gets harder for humans, agents, and tools to know which agent to use when. AWS Agent Registry removes that undifferentiated heavy lifting, giving the right context to the right agent at the right time, and provides a scalable, secure way to grow as more agents get deployed. At Caylent, we worked with customers through the beta and deployed it in our own environment to cut the engineering friction of delivering growing multi-agent architectures.”
>
> — Randall Hunt, CTO, Caylent
>
> “AWS Agent Registry gives our clients the missing piece of enterprise agent governance: a single source of truth for discovering, authenticating, and trusting agents across the enterprise. This is a key capability to enable multi-agent architectures at scale, interconnecting line of business units.”
>
> — Pinaki Karfa, AI architect, Slalom
>
> Partners and ISVs are extending the AWS Agent Registry by building integrations that bring MCP tools and security directly into agentic workflows. From grounding agents in trusted data to continuously assessing security posture, the registry becomes the single source for not only where agents are discoverable, but also tools and skills that are secure for use at scale.
>
> Informatica is building the integration for Informatica hosted MCP (Model Context Protocol) servers to be listed, discovered, and securely integrated with agents through the AWS Agent Registry. The MCPs extend Informatica’s data management capabilities (including metadata exploration, data quality, and master data management) directly into agentic AI workflows. This provides the necessary data foundation for AI agents to access and act upon trusted, governed data supporting accuracy and compliance across the enterprise.
>
> “Informatica from Salesforce is proud to be a launch partner for the AWS Agent Registry. With Informatica MCP servers now discoverable in the Registry, enterprises can easily activate trusted, governed data and extend the full power of IDMC into agentic workflows on AWS. This means AI agents that are not just intelligent but also grounded in high-quality data, driving accuracy, trust, and real business impact.”
>
> — Gopinath Sankaran, VP, Strategic Cloud Alliance, Informatica from Salesforce
>
> Check Point is integrating Agent Registry to give customers continuous discovery and security posture assessment of their Amazon Bedrock AgentCore workloads.
>
> “Check Point views Registry as a foundational component of AI runtime security, it gives us the intended security posture of every deployed agent. By combining Registry metadata with runtime telemetry, we can correlate what an agent was designed to do with what it’s actually doing during execution. This lets us make security decisions based not just on individual prompts, but on the full context of the agent, its declared capabilities and its observed behavior. The result is richer detection, adaptive policy enforcement, and the ability to warn, require approval, block, sandbox, or terminate rogue agent activity when appropriate.”
>
> — Rob Parrish, Head of Product, AI Security, Check Point
>
> Purpose-built for agentic governance and collaboration
>
> The registry provides purpose-built capabilities for every persona involved in an organization’s agentic strategy. These personas range from the administrators who establish guardrails, to the builders who create and publish resources, to the users and autonomous agents that consume those resources for multi-agent collaboration and complex task and workflow completion.
>
> Registry is designed around four types of users:
>
> Admins – Central administrators set up the registry, configure guardrails and establish processes for agentic discovery and governance.
>
> Publishers – Developers, or non-technical personas, who build agents, tools, skills, and allow broader discovery of their resources.
>
> Consumers – Developers, business users or autonomous agents that discover and use agentic capabilities available and approved for use within the organization.
>
> Curators – Curate the agents, tools and skills available for discovery in the registry by approving or rejecting resources based on adherence to internal business needs (for example, Finance, Security, Compliance PoCs).
>
> Workflow for administrators and curators
>
> At the heart of Registry is a governance model built for the realities of enterprise scale. Admins can create and manage a single registry across the enterprise or multiple registry instances, making it straightforward to draw logical boundaries by business unit, environment, or compliance requirement. Each instance carries its own access policies, approval workflows, and lifecycle rules, so teams operate independently. Each registry instance can be independently configured for OAuth-based or IAM-based auth, for both the teams publishing capabilities and the teams consuming them.
>
> Admins govern the full lifecycle of everything in the registry. That means configuring approval workflows with role-based approver assignment that manage state transitions from draft through approval. Curators serve as the human-in-the-loop reviewers, managing lifecycle decisions for each agent, tool, or skill. When it’s time to retire a capability, curators transition the record to a deprecated state at any point in its lifecycle. AWS CloudTrail captures a full audit trail of every action taken on the Registry. Security and compliance assessments can be configured as part of the approval workflows.
>
> The following diagram illustrates a typical workflow set up by admins to approve/reject records when they are published into Registry.
>
> Figure 2: Administrator approval workflow for records published into Registry
>
> Step 1: CRUD Registry: The Admin initiates the process by accessing the registry management interface (available through AWS Command Line Interface (AWS CLI), SDK, or AWS Console) to perform Create, Read, Update, and Delete (CRUD) operations. This is the foundational step where the registry itself is set up and maintained.
>
> Step 2: Create &amp; administer the approval workflow: In parallel, the Admin designs and configures the approval workflow that will govern how agent and tool submissions are validated. This could include setting up security scans, de-duplication, and other validation checks.
>
> Step 3: Publish records: Records are published into the registry. Admins can also directly add records by either specifying active endpoints (which the registry can obtain metadata from), or directly publishing the full records into the registry.
>
> Step 4: Amazon EventBridge Trigger: After a record is submitted and is in pending approval status, the registry fires an event through Amazon EventBridge, which acts as the event broker. This event can be routed into the approval workflow set up in Step 2.
>
> Step 5: Approval Workflow: The approval workflow should include checks and balances that determine if the records should be enabled for broader discovery across the organization. The exact checks and balances are determined by the Admin based on internal organizational requirements.
>
> Step 6: Approval and discovery: Upon the final approval decision (conveyed to the registry through either the API or the Console), the registry updates the record status to approved and publishes it to the registry’s discovery plane.
>
> Step 7: Discovery by consumers: Consumers browsing the registry can now find the record in the registry’s discovery plane, which supports browsing and semantic or lexical (hybrid) search.
>
> Organization-wide auto-detection
>
> Organization-wide auto-detection addresses the concerns around Shadow AI. An admin enables endpoint detection once at the AWS Organization level, and Registry automatically detects agents and MCP servers running on AgentCore runtime, a capability of Amazon Bedrock AgentCore, and AgentCore Gateway across every account in the organization. Detected resources appear in a centralized “Detected Endpoints” view with their identifiers, endpoints, and descriptor metadata. From there, admins connect specific accounts (or entire organizational units) to a central Agent Registry, and detected resources flow in as draft records that follow the standard governance lifecycle: review, approve, and publish to the discovery plane. The relationship is continuous: when a new agent is deployed in a connected account, it appears in the Registry automatically without requiring the publishing team to take any action. This avoids shadow agents and gives central AI administrators the comprehensive visibility they need to enforce governance at scale.
>
> Publishing
>
> The Registry supports registration through the Console, CLI, and APIs, so teams can publish MCP Servers, A2A Agents, Skills, and custom resource metadata through whichever workflow fits their development process. Publishers can integrate registry record updates directly to existing continuous integration and continuous delivery (CI/CD) pipelines, avoiding manual changes for every release. After submitted, records progress through configured lifecycle states (draft to pending approval to approved, rejected, or deprecated) as reviewers grant approvals.
>
> Registry can also pull metadata directly from external MCP or A2A servers using the synchronization feature. It connects using OAuth, IAM, or unauthenticated access depending on the server’s configuration, and synchronizes record metadata automatically.
>
> The following diagram illustrates a publishing workflow where a CI/CD pipeline pushes records into Registry and the approval workflow moves them to Approved/Rejected status.
>
> Figure 3: Publishing workflow from a CI/CD pipeline into Registry
>
> Step 1: Discover the Registry – The developer uses their IDE and SDK to build an agent or tool. They first interact with the Registry to discover what’s already registered.
>
> Step 2: Dev-Controlled CI/CD Pipeline – Assume the developer’s code flows into their own CI/CD pipeline, which automates the packaging and preparation of the agent or tool for registration.
>
> Step 3: Generate Agent Card &amp; MCP Definition – The CI/CD pipeline can be setup to produce either Agent Card that contains the agent’s metadata, capabilities, and specifications or MCP Server with Endpoint URL that defines the tool’s interface and where it can be reached.
>
> Step 4: Submit &amp; Create Registry Record – The pipeline creates a record within the Registry and then submits it for approval.
>
> Steps 5-8: Approval workflow process – As explained in the previous diagram.
>
> Discovery and usage
>
> For consumers, discovery is built around a semantic search experience that spans the full catalog accessible through the Search API. For automated pipelines and agentic workflows, the Search API is also exposed as an MCP server, so agents can find and select tools and skills programmatically. Authentication follows the same pattern as the rest of the Registry: OAuth or IAM, as configured per instance by the admin. And for teams operating in locked-down network environments, AWS PrivateLink is used so that Registry remains reachable without compromising on security posture.
>
> The following diagram shows a discovery and access flow for developers or agents consuming agents and tools from Registry.
>
> Figure 4: Discovery and access flow for consumers of Registry resources
>
> Step 1: Search the Registry – The developer queries the Registry to discover available agents, tools and skills.
>
> Step 2: Receive Auth Info &amp; URIs – The registry responds with the authorization details and endpoint URIs for the resources the developer is interested in.
>
> Step 3: Request Access – The developer requests onboarding onto the A2A and MCP servers through the organization’s onboarding process.
>
> Step 4: Provide Credentials – The developer receives auth details for the requested endpoints, this could be clientID/secret, or API keys or IAM based access to the servers.
>
> Step 5: Call Resources with Auth – The developer (and their agent) can make authenticated calls to agents and tools using the credentials obtained in Step 4.
>
> Discovery from IDEs
>
> Registry exposes each registry instance as an MCP server. MCP compatible IDE, including Kiro and Claude Code, can connect to it natively. This means a developer can type a natural-language request like “find me an MCP server for problem tickets” directly in their IDE. The IDE queries specific registry instance in Registry, returns matching tools with their metadata and connection details, and if the developer has access, they can start using the tool immediately, without leaving their editor.
>
> The connection setup is lightweight: the IDE uses Dynamic Client Registration (DCR) to establish a trust relationship with Registry at runtime. No admin needs to pre-provision OAuth credentials. The developer authenticates once through their organization’s identity provider (for example, AWS IAM Identity Center), and the IDE receives a scoped access token. From that point on, searching the registry, browsing metadata, and retrieving connection details happen inline.
>
> Discovery from Amazon Quick
>
> Just as developers discover Registry resources from their IDE, business users and knowledge workers can now discover and invoke them directly from Amazon Quick. After a Quick admin connects their tenant to one or more Agent Registries, all approved agents, MCP servers, and skills appear on Quick’s Integrations page. Enterprise license users can browse and search the full catalog, view tool descriptions and capabilities, enable specific agents for their tenant, and share them with the appropriate teams. End users then access these agents through Quick Chat, Automations, Flows, and Deep Research. This means organizations no longer need to rebuild capabilities inside Quick that already exist elsewhere, a single governed catalog powers both developer and business-user experiences.
>
> State transitions
>
> Records in the registry go through a governed lifecycle with multiple state transitions, as shown in the following diagram.
>
> Figure 5: Record lifecycle state transitions in Registry
>
> Publisher Creates/Updates Registry Record – The Publisher initiates the process by creating a new registry record (or updating an existing one), placing it in the DRAFT state.
>
> Publisher Submits for Approval – The Publisher submits the draft record for review, transitioning it to the PENDING_APPROVAL state.
>
> Approver Updates Status – The Approver reviews the workflow outcome and takes one of two actions:
>
> Approves – Record moves to APPROVED state.
>
> Rejects – Record moves to REJECTED state.
>
> Alternatively, record moves to APPROVED state when the auto_approve flag is set to true.
>
> Publisher Updates Record (optional loop) – While the record is in PENDING_APPROVAL, or APPROVED state, the Publisher can make updates to it, which sends it back to DRAFT state, restarting the submission process.
>
> Curator Deprecates the Record – Curator can deprecate a record when it’s no longer needed, transitioning it to the DEPRECATED state.
>
> Enterprise considerations
>
> As you roll out Registry across an organization, a few decisions shape how you set it up and operate it at scale.
>
> Single vs multiple
>
> The first question most teams

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。