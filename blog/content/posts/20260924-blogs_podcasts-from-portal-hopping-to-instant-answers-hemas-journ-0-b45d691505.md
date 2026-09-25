---
title: "From portal-hopping to instant answers: HEMA’s journey with MCP and Amazon Bedrock"
date: 2026-09-24T04:23:48+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "RAG", "AI Agent", "Amazon Bedrock", "Amazon Bedrock AgentCore", "Customer Solutions", "博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:38ed1a9cbaa3d5414801d1bfc91d69b79fb015bd2f39a154ae7e11b118f63c2d"
source_payload_sha256: "sha256:509b9b83e359d87dc8e3fbb3768d37f0c09502fee80d08351ee10225bc352c7f"
observation_id: obs_b45d69150568a41c7c8d0e965415108ec9764820ec42b2563aeefefdb1257114
event_id: evt_ca199fd86563c43de1552b2181029588144e8bad74b9e3d89faec2d8cba4f830
revision_id: rev_fed752990f28caf1fe946b6b321e06f0c95c30b0c26894849acc2153c52373f9
source_published_at: 2026-09-23T18:41:09Z
first_seen_at: 2026-09-23T20:33:59Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 82
interpretation_sha256: "sha256:626ec80160200bfaa104ce600ad5737163ce8d4f6785477662ae4e62d65a3769"
description: "这条内容介绍了一家荷兰零售商如何通过构建内部AI助手来解决内部知识分散的痛点。团队利用MCP（Model Context Protocol）作为标准化接口，将分散在不同系统的知识整合到统一平台中，并通过Amazon Bedrock AgentCore托管AI代理能力。"
external_url: https://aws.amazon.com/blogs/machine-learning/from-portal-hopping-to-instant-answers-hemas-journey-with-mcp-and-amazon-bedrock
parent_observation_id: null
last_seen_at: 2026-09-25T00:00:00Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/from-portal-hopping-to-instant-answers-hemas-journey-with-mcp-and-amazon-bedrock](https://aws.amazon.com/blogs/machine-learning/from-portal-hopping-to-instant-answers-hemas-journey-with-mcp-and-amazon-bedrock)
- **发布域名**: aws.amazon.com

## 要点解读

### 这是什么
这条内容介绍了一家荷兰零售商如何通过构建内部AI助手来解决内部知识分散的痛点。团队利用MCP（Model Context Protocol）作为标准化接口，将分散在不同系统的知识整合到统一平台中，并通过Amazon Bedrock AgentCore托管AI代理能力。

### 用在哪里
适合企业IT部门或数字化转型团队参考，尤其是那些面临内部文档、流程、接口信息分散在多个系统中的组织。对关注如何借助AI助手提升内部协作效率的技术管理者有一定参考价值。

### 可以推断的
推测：MCP作为AI客户端与后端能力之间的标准化协议，能够降低多工具整合的二次开发成本。
推测：零售等业务分散型企业对内部知识整合的需求较为普遍，相关技术方案可能具有跨行业借鉴意义。

## 来源摘要/节选

> This post is co-written with Mauro Rallo and Patrick van der Plas from HEMA.
>
> When engineers at HEMA needed an answer, they went portal-hopping, navigating disconnected wikis, service catalogs, and IT portals to find it. To turn that friction into instant answers, the 100-year-old Dutch retailer built a knowledge layer on Amazon Bedrock AgentCore. HEMA has over 750 stores across multiple countries, served by a technology organization of engineers, product owners, and business analysts driving digital transformation. It needed a solution that worked across roles and tools.
>
> Over the years, HEMA had quietly built something valuable: a large, structured picture of its own technology landscape. A service catalog mapped people to teams, teams to services, and services to the APIs we expose, and the business capabilities we support. The problem was never that the knowledge didn’t exist. It was that the knowledge was hard to reach. As the engineering organization grew, the informal “just ask the person next to you” model broke down, and teams ended up scattering answers across portals, wikis, and documentation that few people knew how to navigate.
>
> In this post, we describe the challenge HEMA faced with fragmented internal knowledge, why we chose to build HAL, HEMA’s internal AI assistant, using Model Context Protocol (MCP) and Amazon Bedrock AgentCore, and how it changed the way our teams work.
>
> The idea rests on two complementary goals. HAL puts knowledge in one place, and MCP delivers that knowledge inside the tools people already use (the HAL chat, Kiro, Claude, and other agents). Security is anchored in Microsoft Entra ID, with no AWS credentials on the client. What began as a developer tool is already a cross-role assistant. The same architecture will be the foundation for a next step: turning HAL from a read-only knowledge layer into an action layer.
>
> The challenge: Portal-hopping and knowledge fragmentation
>
> HEMA’s knowledge problem had two distinct layers.
>
> The first layer, structured infrastructure knowledge, was actually in good shape. For years, HEMA has maintained a service catalog that captured how the technology estate fits together: which teams own which services, what APIs those services expose, and how they map to business capabilities. Structured data from systems such as the product information management (PIM) engine and the data-mesh tables had been imported and organized. For anything about what exists and who owns it, the answer was usually available, if you knew where to look.
>
> The second layer was the gap. Knowing what exists is not the same as knowing how to do something. “How do I request access to an API? How do I get a new group provisioned? What’s our rule for X?”. These procedural questions had no single home. When teams were small and everyone knew each other, that was fine. People asked directly. As HEMA grew and onboarded new engineers, that model stopped scaling, and there was little written documentation to fall back on.
>
> That translated into slow onboarding for new joiners, inconsistent answers depending on where someone looked, constant context-switching, and friction that pulled people out of their actual work. Finding an answer that once meant navigating three or four portals, sometimes across an entire afternoon, now happens in seconds, from inside the Integrated Development Environment (IDE) or chat window.
>
> Figure 1: The “before” state, showing the sources a user had to consult
>
> Why MCP and Amazon Bedrock AgentCore
>
> Two goals shaped the solution, and they map cleanly onto the two technologies we chose.
>
> The first goal belongs to HAL: consolidate HEMA’s fragmented knowledge into one governed source of truth. The second goal belongs to MCP: deliver that knowledge to people where they already work, rather than forcing them to visit yet another portal.
>
> Why MCP: Model Context Protocol gives us a standardized interface between AI clients and backend capabilities. Instead of building a bespoke integration for every knowledge source and re-building it for every client application, we expose each source once as an MCP tool.
>
> MCP-compatible clients such as the HAL web chat, Kiro, Claude, and other agents can then consume the same tools without custom work. This is what makes “access from your daily tool” practical rather than a per-tool engineering project.
>
> Why Amazon Bedrock AgentCore: Amazon Bedrock AgentCore is a platform to build, connect, and optimize agents at scale, with any framework or model. For HEMA, it meant building HAL without standing up and operating custom MCP server infrastructure. The capabilities that mattered most:
>
> Gateway turns OpenAPI specifications and AWS Lambda functions into MCP tools directly. There is no custom MCP server code to write or run.
>
> Identity provides managed inbound JSON Web Token (JWT) authentication and managed outbound OAuth2 (a token vault) to our internal APIs.
>
> Runtime hosts the internal agent (built with the Strands framework) as a container.
>
> Memory and Amazon Bedrock Guardrails provide conversation memory and content filtering, with EU inference regions and Dutch-language support.
>
> Together, these gave us enterprise-appropriate footing: Entra ID OAuth, read-only access today, and access control driven by existing Active Directory groups, safe enough to expose real internal knowledge.
>
> Building HAL, step by step
>
> HAL didn’t arrive fully formed. It grew in two deliberate steps. First, the team built a standalone assistant with its own chat UI. Then, once that foundation proved itself, we opened it up to the tools people already work in through MCP.
>
> Step 1: HAL as a standalone assistant
>
> The first version of HAL was a self-contained assistant: a web chat UI (built with Next.js) backed by an agent that could answer questions from HEMA’s knowledge. There were no MCP and no external clients yet, only the HAL UI talking to the HAL agent.
>
> The HAL agent is a Strands agent packaged as a Linux/ARM64 container and hosted on AgentCore runtime, together with AgentCore memory (short-term conversation context) and Amazon Bedrock Guardrails (Standard tier, EU Cross-Region inference for Dutch-language support). AgentCore runtime and AgentCore memory are capabilities of Amazon Bedrock AgentCore.
>
> The agent reaches knowledge along two distinct paths:
>
> Local tools, direct to the Knowledge Bases. The agent’s semantic-search tools are local Strands tools that call the Amazon Bedrock Retrieve API directly over the Knowledge Bases, no gateway in between. This is the bread-and-butter “answer from the knowledge base” path.
>
> MCP to an AgentCore Gateway, for live APIs. For live data, full OpenAPI specifications, service-catalog lookups, and people/team queries, the agent connects over MCP to its own AgentCore Gateway, a capability of Amazon Bedrock AgentCore. This Gateway is authenticated with AWS Identity and Access Management (IAM) SigV4, which in turn calls our internal APIs.
>
> Figure 2: Step 1, HAL as a standalone assistant
>
> We started from the structured data we already had, the service catalog, and added the highest-value documentation, prioritizing by pain and by how often something was asked. Behind HAL sit several knowledge bases built on Amazon Bedrock Knowledge Bases, the fully managed Retrieval Augmented Generation (RAG) capability: IT and how-to documentation, API/OpenAPI specifications, Kafka event-streaming topics and their Avro schemas, Data Consolidation Layer (DCL) data-exchange channels, and the service catalog (people, teams, services, and APIs).
>
> There’s no custom MCP server code. AgentCore Gateway generates the MCP tools directly from OpenAPI specifications for the API passthrough targets, and from a Lambda function for semantic search over the Knowledge Bases. Pointing the Gateway straight at our existing API specifications isn’t the ideal end state. An API designed for system-to-system use does not always map cleanly onto a tool an agent can reason about, so we plan to refactor those definitions into more agent-friendly tools.
>
> For now, though, exposing the APIs as-is delivered high value for little effort. The kb-search Lambda wraps the Amazon Bedrock Retrieve API over the Knowledge Bases. It’s scoped by AWS Identity and Access Management (IAM) to the specific Knowledge Base Amazon Resource Names (ARNs), plus read access to the source-document Amazon Simple Storage Service (Amazon S3) bucket.
>
> Retrieval follows a two-step pattern: an initial Knowledge Base search answers most questions, and fetch_full_document pulls the complete document when a single chunk isn’t enough. Retrieval quality is improved with Amazon Bedrock reranking on semantic queries and team_id metadata filtering for team-scoped lookups.
>
> Step 2: Opening HAL to daily tools with MCP
>
> HAL worked well in its own chat UI, but people live in other tools: their IDE, their AI assistant. The second step was to let external MCP clients such as Kiro and Claude reach the same knowledge and tools, without handing out AWS credentials. That meant adding a second AgentCore Gateway, authenticated with Microsoft Entra ID instead of IAM.
>
> Because an AgentCore Gateway supports only a single inbound authentication type, we could not reuse the agent’s IAM-authenticated Gateway from Step 1 for these external clients. So, we added a second Gateway, an Entra MCP Gateway authenticated with a custom JWT through Microsoft Entra ID, dedicated to external MCP clients such as Kiro and Claude. It shares only the read-only Knowledge Bases with the agent Gateway. There is no shared code, so the external-facing surface can evolve, or fail, without impact on the internal agent.
>
> Figure 3: Step 2, opening HAL to daily tools with MCP
>
> AgentCore Gateway exposes tools from OpenAPI specifications and Lambda functions. To surface the knowledge bases as a Gateway target, we built a small intermediate Lambda function that the Gateway calls as a tool, and which performs the semantic search over the knowledge bases on behalf of the Gateway. The live internal APIs, by contrast, are exposed directly as OpenAPI targets.
>
> The hard part: Authentication and Dynamic Client Registration (DCR)
>
> One interesting piece is how external clients authenticate without AWS credentials. In front of the Entra Gateway sits an MCP auth proxy, an Amazon API Gateway v2 HTTP API backed by a single Lambda, that reconciles the MCP OAuth specification with the specifics of Entra ID. It serves the OAuth discovery documents and rewrites the requested scope to the resource app’s invoke scope. It also strips the legacy resource parameter that Entra v2.0 rejects, adds response_mode=query so desktop clients can capture the authorization code, and proxies /mcp with the bearer token.
>
> One detail is worth calling out because it is the only place DCR appears in the whole system. MCP clients expect DCR, a POST /register call that hands back a client ID. Rather than implementing true dynamic registration, the proxy uses a stubbed /register that returns a fixed, pre-provisioned client ID. DCR is emulated, not real.
>
> The full handshake looks like this:
>
> Figure 4: The OAuth and DCR authentication sequence
>
> For the end user, the payoff is that configuration is only the proxy URL and an empty oauthScopes list, no AWS credentials, a browser login on first connect, and automatic token refresh thereafter.
>
> Deployment on Amazon Bedrock AgentCore
>
> The infrastructure is defined in AWS Cloud Development Kit (AWS CDK), a TypeScript monorepo using npm workspaces. The internal agent runs as a Docker container on AgentCore runtime. Environment-specific configuration, such as tenant, client, and resource identifiers, is supplied through AWS Systems Manager (SSM) parameters.
>
> Testing and rollout
>
> Before going live, HEMA deployed HAL to a staging environment and opened it to both engineers and business users for hands-on testing over a one-month period. This validated answer quality, coverage gaps, and day-to-day usability before the solution was promoted to production for wider adoption across the organization.
>
> Who uses HAL today
>
> HAL began as a developer tool, but it is already a cross-role assistant, and that breadth is the point.
>
> Developers use the full technical surface: documentation, API specifications, Kafka topics and schemas, the service catalog, and DCL channels, from inside Kiro and the chat.
>
> Product owners rely on HAL for documentation, how-to, and process knowledge: the procedural layer that used to have no home.
>
> Business analysts use HAL for infrastructure knowledge: which services exist, what APIs they expose, and which teams own them, drawing directly on the service catalog.
>
> The pull from non-developer roles is real and growing: HEMA’s end-to-end team, mapping and optimizing product-manager processes, is already engaging with HAL as part of that work. Internally, HAL is distributed through an “Everyone Skill” and accompanying steering files, shared and maintained through the monthly HEMA AI Development Forum.
>
> What’s next: From answers to actions
>
> Today, HAL is read-only and delivers instant answers. The next step is instant action, performed by the same assistant.
>
> This is feasible now precisely because the underlying portals are already API-enabled and already integrated with existing Microsoft Entra ID single sign-on. That means HAL can expose those operations as MCP action tools using the very same Entra ID authentication and Active Directory group authorization model that already secures the read tools. No new security model is required, only new, carefully scoped tools.
>
> The flagship example is provisioning a new AWS account. Today a developer goes to a dedicated portal to request one. Next, they will make the same request directly from chat, Kiro, Claude, or other agents without visiting the portal at all. And because HAL already serves product owners and business analysts, the same action pattern extends naturally beyond developer operations to the wider set of operational requests those roles make every day.
>
> The lesson is that the read architecture earns the write step: by getting identity, multi-client access, and governance right for answers, we have laid the groundwork for actions.
>
> Conclusion
>
> HAL puts HEMA’s organizational knowledge in one governed place. MCP and Amazon Bedrock AgentCore make that knowledge reachable, multi-client, and secure without forcing every consuming application to rebuild authentication, authorization, or routing from scratch. The outcome isn’t a developer chatbot, but a cross-role assistant for developers, product owners, and business analysts alike. The knowledge layer is live. The logical next step is extending it into an action layer. There, the same governed, authenticated infrastructure that today answers questions could tomorrow execute requests: provisioning access, triggering workflows, and acting on behalf of users directly from chat, Kiro, Claude, or other MCP-compatible agents.
>
> If you want to explore the building blocks used in this post, the following resources are a good starting point. To learn about MCP server hosting, authentication, and gateway routing, see the Amazon Bedrock AgentCore documentation. For the Model Context Protocol specification and client compatibility guidance, visit the MCP specification site. To get hands-on with Strands Agents, the open source agent framework used to build HAL’s internal agent, see the Strands Agents GitHub repository. If you’re building a similar knowledge layer for your organization, the Amazon Bedrock workshop walks through RAG patterns, Knowledge Bases, and guardrails in a guided environment.
>
> For related reading, see Building and connecting a production-ready ecommerce MCP server using Amazon Bedrock AgentCore and Mistral AI Studio and Introducing Amazon Bedrock AgentCore Identity: Securing agentic AI at scale.
>
> About the authors
>
> Mauro Rallo
>
> Mauro is an Enterprise Architect and DevOps Product Owner for HEMA’s central platform (CIP), where he focuses on architecture, developer experience, and making engineering knowledge easy to reach across the organization.
>
> Patrick van der Plas
>
> Patrick is a Software Engineer on HEMA’s AI team, where he built the MCP gateway and tooling behind HAL, HEMA’s internal AI assistant. He also builds the wider platform for HEMA’s AI agents to run on and drives adoption of AI-assisted development across HEMA’s engineering teams. Outside the office, Patrick spends his time in the gym, running, competitive gaming, and enjoying life with his fiancée.
>
> Amit Singh
>
> Amit is a Senior Solutions Architect at AWS, working with enterprise retail customers in the Benelux region. He helps customers design cloud-native architectures, navigate complex modernization journeys, and adopt AI/ML capabilities at scale. Outside of work, he enjoys exploring new places and chasing the perfect shot, whether through a camera lens or on a running trail.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。