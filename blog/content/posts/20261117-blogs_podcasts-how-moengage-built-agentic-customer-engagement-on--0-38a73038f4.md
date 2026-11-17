---
title: "How MoEngage built agentic customer engagement on Amazon Bedrock AgentCore"
date: 2026-11-17T04:29:14+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "生成式 AI", "Amazon Bedrock", "Amazon Bedrock AgentCore", "Customer Solutions", "博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:b7d01604dc1e006ac8f98ca6c96bf8a023e4644c205c789afe0ac81d82a35991"
source_payload_sha256: "sha256:2114878600c70bf990df1d76c189d5abe6501cbb7baef190be09e0f98e99da35"
observation_id: obs_38a73038f401258c1101cee1b87d010cae924cf6e06991abb42f655846d02772
event_id: evt_98de93f0e32c6857ffd11454fbfe512bba28bc245568db1d3b67b9601ed8f6af
revision_id: rev_25e48287736fe30fd99788d69189a496817b57cac2d30e3720265d8178299b6d
source_published_at: 2026-11-16T18:16:07Z
first_seen_at: 2026-11-16T20:39:02Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 74
interpretation_sha256: "sha256:6c6a9c16687e2eed6a230b03bb90616ef839f8907e08a9e3b03b2522c5b7a442"
description: "MoEngage 介绍其如何利用 Amazon Bedrock 与 Amazon Bedrock AgentCore 构建 Merlin AI，并通过 MCP 将分群、历史活动和内容库等能力开放给 Claude、ChatGPT 等兼容客户端。"
external_url: https://aws.amazon.com/blogs/machine-learning/how-moengage-built-agentic-customer-engagement-on-amazon-bedrock-agentcore
parent_observation_id: null
last_seen_at: 2026-11-17T00:00:00Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/how-moengage-built-agentic-customer-engagement-on-amazon-bedrock-agentcore](https://aws.amazon.com/blogs/machine-learning/how-moengage-built-agentic-customer-engagement-on-amazon-bedrock-agentcore)
- **发布域名**: aws.amazon.com

## 要点解读

### 这是什么
MoEngage 介绍其如何利用 Amazon Bedrock 与 Amazon Bedrock AgentCore 构建 Merlin AI，并通过 MCP 将分群、历史活动和内容库等能力开放给 Claude、ChatGPT 等兼容客户端。方案涵盖嵌入式、对话式、自定义和决策型智能体，并强调多租户数据隔离与操作可追踪。

### 用在哪里
适合营销与产品团队用自然语言完成文案生成、受众筛选、模板制作、旅程搭建、效果分析和跨渠道投放决策，也可作为企业将既有 API 封装为智能体工具的架构参考。

### 可以推断的
- 推测：将已有 API 转换为 MCP 工具，可能比重复建设智能体专用接口更容易接入外部助手。
- 推测：在客户触达场景中，租户隔离、权限控制与人工审核机制会直接影响方案能否投入实际运营。

## 来源摘要/节选

> This post was co-written with Ashwin Srinivasan, Nishan Das and Karthik Baile from MoEngage.
>
> A marketing or product team member planning a weekend flash sale often opens three tools before writing a single line of copy. First they open the analytics dashboard to see what worked last time, then the content library to find the right tone, and then the campaign builder to build the campaign itself. Repeat that across email, push, SMS, and WhatsApp, and much of a marketing team’s week goes to navigating tools instead of making decisions.
>
> The MoEngage Model Context Protocol (MCP) Connector gives an MCP-compatible assistant, such as Claude or ChatGPT, secure, tenant-scoped access to a brand’s segments, campaign history, and content library.
>
> This capability points to a broader shift in software platforms. Beyond a user interface for business users and an API for engineering teams, a third layer is emerging, where a user describes an outcome in plain language and an agent carries out the steps across the platform. For a customer engagement platform, that means a capability already exposed as an API can become a tool an agent calls, and a campaign that once moved across several tools can move through one conversation instead.
>
> MoEngage, the agentic customer engagement platform that more than 1,350 consumer brands use across channels including push, email, in-app, SMS, WhatsApp, and Rich Communication Services (RCS), set out to build this layer. MoEngage built Merlin AI, a set of artificial intelligence (AI) agents that work with live platform data. Marketing and product teams can now draft, analyze, and adjust campaigns from a single conversation, while agents decide what to send each customer. One customer, Glance, saw a 38% uplift in push notification click-through rates as a result.
>
> MoEngage treated this as an architecture problem. The question was how to give agents secure, tenant-scoped access to live data without rebuilding hundreds of existing APIs. In this post, we walk through how MoEngage solved it with Amazon Bedrock and Amazon Bedrock AgentCore, a platform to build, connect, and optimize AI agents at scale with any framework or model. The post covers the four agent modes in Merlin AI, how MoEngage exposed its existing APIs as MCP tools, and how the architecture keeps each tenant’s data isolated. It closes with the results MoEngage customers have seen and the pattern other software providers can reuse.
>
> Solution overview: Four agent modes in Merlin AI
>
> Merlin AI runs four kinds of agents. All four share the same foundation: foundation models in Amazon Bedrock for reasoning and generation, AgentCore runtime, a capability of Amazon Bedrock AgentCore, for hosting, and MCP for standardized access to data. Across all four modes, Merlin AI uses Anthropic Claude Sonnet 4.6, Claude Sonnet 5, and Claude Sonnet 5.5 on Amazon Bedrock for reasoning, tool-call planning, and content generation. For the full list of models, see Supported foundation models in Amazon Bedrock.
>
> Embedded agents in Merlin AI Studio
>
> Merlin AI Studio places purpose-built agents at the exact point in the workflow where marketing and product teams do that piece of work:
>
> Copywriter generates personalized push and transactional copy that stays consistent with the brand voice.
>
> Designer produces a marketing banner or image from a text description.
>
> Segment Assist turns a plain-language audience description into the correct set of attributes and filters. For example, a marketing or product team member can ask for users who abandoned a cart in the last 2 hours.
>
> Jinja Assist converts natural-language requests into working Jinja and Liquid markup for dynamic content.
>
> In-app Template Builder creates responsive, accessible HTML templates for in-app messages, including gamified formats, lead-capture pop-ups, and surveys.
>
> Flow Assist turns a high-level idea into a ready-to-deploy customer journey. Behind the scenes, a sequence of specialized steps interprets the request, proposes paths, builds the flow structure, refines it with historical data, and packages it for deployment.
>
> Conversational agents
>
> Conversational agents work across campaigns, analytics, segments, and flows. A user can ask a question in plain language and the agent calls the right tools to answer it or act on it. The Campaign Insights Agent, embedded on the analytics page, delegates to specialized sub-agents. One sub-agent runs analysis across several metrics at once. A second diagnoses why a metric is underperforming, and a third compares performance across time periods or segments. A final step formats the findings into a clear answer.
>
> Custom agents
>
> Custom agents let lifecycle and customer relationship management (CRM) teams design agents that run continuously on MoEngage data and tools, inside rules the product and marketing team defines. Every agent shows its work through an activity log of the data it pulled, the decisions it made, the channels it touched, and the content it sent. Teams can run an agent with full autonomy or require human review before anything executes.
>
> Decisioning agents
>
> Decisioning agents act for each individual customer. Each agent decides what to say, when, how often, and on which channel, and it learns from every outcome. Product and marketing teams set the content, goals, and guardrails, and the agents handle the rest, with visibility into every decision. Offer Decisioning selects the best offer on web and app surfaces. Campaign Decisioning delivers 1:1 decisions across email, push, SMS, and WhatsApp. Together with workflow agents, this puts both halves of agentic marketing in one system.
>
> Architecture overview
>
> The architecture has four layers. Each layer has a single responsibility and can change without affecting the others.
>
> Clients. Merlin AI agents inside the MoEngage product, and external MCP clients such as Claude and ChatGPT, through the MoEngage MCP Connector, connect to the MoEngage MCP server. Clients that support MCP can connect.
>
> MCP server on AgentCore runtime. MoEngage hosts its MCP server on AgentCore runtime. The server exposes MoEngage platform capabilities as MCP tools. It does not run its own model. Reasoning happens in the agent that calls it.
>
> MoEngage platform APIs. The MCP server calls the same OpenAPI 3.0-compatible APIs that MoEngage customers already use. These APIs enforce existing permissions and data residency rules.
>
> Foundation models in Amazon Bedrock. Agents use foundation models in Amazon Bedrock to plan tool calls, generate content, and summarize results. For model availability by Region, see Supported models by AWS Region in Amazon Bedrock.
>
> In a typical request, a user signs in to MoEngage and asks a question. The client sends the request with the user’s existing JSON Web Token (JWT). AgentCore runtime validates the token and starts an isolated session for that user. The agent asks a model in Amazon Bedrock which tools to call. The MCP server calls the MoEngage APIs with the user’s tenant context and returns the results. The agent then composes the answer.
>
> The following diagram shows how these components connect.
>
> Figure 1: MoEngage Merlin AI architecture on Amazon Bedrock and AgentCore runtime.
>
> Turning existing APIs into MCP tools
>
> MoEngage opens its platform to agents through an MCP server and agent-callable APIs. Its platform APIs for campaigns, analytics, segments, content, and flows were already OpenAPI 3.0-compatible, so MoEngage used the FastMCP framework to generate MCP tools from those specifications. Each operation becomes a tool with a structured schema, a description, and parameter validation.
>
> The following simplified example shows the pattern:
>
> import httpx
>
> from fastmcp import FastMCP
>
> spec = httpx.get(MOENGAGE_OPENAPI_URL).json()
>
> client = httpx.AsyncClient(base_url=MOENGAGE_API_BASE)
>
> mcp = FastMCP.from_openapi(openapi_spec=spec, client=client, name='moengage')
>
> if __name__ == '__main__':
>
> mcp.run(transport='streamable-http', host='0.0.0.0', port=8000)
>
> The tools fall into five groups:
>
> Campaign tools create, edit, schedule, and send campaigns across channels.
>
> Analytics tools query delivery funnels, click-through rates, conversions, and cohort performance.
>
> Segmentation tools list, inspect, and create segments from behavioral and attribute filters.
>
> Content tools manage content blocks, templates, and dynamic content rules.
>
> Flow tools inspect, pause, or modify automation journeys.
>
> The tools come from the specifications, so they stay in sync with the APIs. When a team updates a specification, the tool definitions update with it.
>
> Keeping tenants isolated and identity out of the model’s reach
>
> A multi-tenant system cannot let a model decide whose data it is reading. MoEngage made three design choices to help prevent that. First, the MCP server reuses the existing authentication model, accepting the same JWT-based authentication that MoEngage APIs already use, and AgentCore runtime validates each token before a request reaches the server. Second, workspace and user context travel in request headers that AgentCore runtime forwards to the server rather than as tool arguments, so the model does not see these values and cannot change them. Third, AgentCore runtime runs each user session in its own isolated environment, so one user’s conversation cannot read another’s session state.
>
> On top of this, Amazon Bedrock Guardrails apply content safety and personally identifiable information (PII) filters to agent responses. A backend-for-frontend layer then validates the structure of generated content before the MoEngage interface renders it.
>
> Give users control over agents. Users set guardrails on what each agent can do, review every action in its activity log, and choose between autonomous and human-reviewed execution.
>
> Why MoEngage chose AgentCore runtime
>
> AgentCore runtime provides the production capabilities that a multi-tenant MCP server needs, and each one addresses a specific requirement of MoEngage’s workload. AgentCore runtime scales sessions as demand changes, so MoEngage does not plan capacity for traffic bursts across its customer workspaces. Each session runs in its own isolated environment by default, which keeps one brand’s conversation and data separate from another’s. The built-in JWT authorizer validates tokens against MoEngage’s existing identity provider, so the MCP server uses the same authentication model as the APIs.
>
> Hosting on AgentCore runtime is also framework-agnostic. MoEngage can change models or agent frameworks without touching the MCP server, which matters as the agent layer evolves. Built-in metrics, logs, and traces through Amazon CloudWatch give MoEngage engineers visibility into every session. Together, these capabilities let the team focus on agent logic and marketing intelligence rather than hosting infrastructure.
>
> Inference through Amazon Bedrock gave MoEngage two more benefits. Merlin AI agents run on Anthropic Claude Sonnet 4.6, Claude Sonnet 5, and Claude Sonnet 5.5 on Amazon Bedrock, and MoEngage moves between these versions through the same Amazon Bedrock API. MoEngage also pays per token instead of operating GPU infrastructure. Amazon Bedrock does not use customer prompts or responses to train foundation models, which matters for a system that processes customer engagement data at scale.
>
> One campaign, one conversation
>
> The following example shows how a user builds a campaign without leaving the conversation.
>
> Ask for the draft. The user types:
>
> Draft a weekend flash sale push for our high-value segment, using the same tone as our best-performing December campaign.
>
> The agent calls the analytics tools to find the top December campaign, the segmentation tools to confirm the high-value segment, and the content tools to pull the brand voice. It returns a draft with several copy variants.
>
> Check what underperformed. The user asks:
>
> Which push notifications last month had below 2% click-through rate (CTR), and what do they have in common?
>
> The Campaign Insights Agent compares those campaigns and reports the shared pattern, such as send time or audience overlap.
>
> Adjust the journey. The user asks:
>
> Show me the drop-off at step 3 of our onboarding flow, and pause the SMS branch if it’s below 5% conversion.
>
> The agent reads the flow state through the flow tools and pauses the branch after the user confirms. This is the human-review mode in practice.
>
> Each step uses the same tools that power the MoEngage interface. The user does not open a separate dashboard.
>
> Results
>
> Merlin AI agents on this architecture have been in production for more than 6 months. One customer, Glance, reached campaign go-live 50% faster and saw a 38% uplift in push notification click-through rates. With Merlin AI Copywriter, Glance teams also produce about three times more content variants per campaign.
>
> Across the platform, MoEngage reports a 60–70% reduction in manual effort by marketing and product teams for channel, timing, and frequency decisions, and a 20–30% improvement in conversion rates from goal-based decisioning. Managed, pay-per-token inference in Amazon Bedrock reduced AI infrastructure costs by more than 50% compared with self-hosted models.
>
> AgentCore feature availability varies by AWS Region. For supported Regions, see the Amazon Bedrock AgentCore documentation.
>
> Conclusion
>
> MoEngage made its platform agent-ready without rebuilding it. Existing OpenAPI specifications became MCP tools. AgentCore runtime provided hosting, authentication, and session isolation. Foundation models in Amazon Bedrock provided reasoning and generation. The result is a platform where marketing and product teams move from question to action in one conversation, where MoEngage engineers spend their time on marketing intelligence rather than infrastructure, and where agents handle workflows for the team and decisions for every customer while users stay in control.
>
> The same pattern applies to other software providers with a mature API surface. Start from your existing specifications, keep identity outside the model, and let a managed runtime handle the production concerns.
>
> To build your own MCP server on the same foundation, start with the Amazon Bedrock AgentCore documentation and follow the AgentCore runtime guide to host it. To choose a foundation model for your agents and review the security and data-handling controls, see the Amazon Bedrock User Guide. To generate MCP tools from your existing OpenAPI specifications, review the FastMCP documentation. To see Merlin AI in action, visit MoEngage Merlin AI. To plan a similar architecture, contact your AWS account team or Solutions Architect.
>
> About the authors
>
> Ashwin Srinivasan
>
> Ashwin Srinivasan is a VP of Product at MoEngage, where he shapes the product vision around solving real-world customer pain points, ensuring team execution delivers reliable, scalable, and value-driven products that directly improve the user experience.
>
> Nishan Das
>
> Nishan Das is a Senior Director of Technology Partnerships at MoEngage, where he leads strategic technology partnerships and ecosystem alliances, driving product integration and expanding co-innovation initiatives across market partners.
>
> Karthik Baile
>
> Karthik Baile is a Partner Development Manager at MoEngage, where he manages partner marketing strategies, focusing on driving collaborative growth, brand alignment, and impactful go-to-market campaigns across strategic partner ecosystems.
>
> Bhupesh Chadha
>
> Bhupesh Chadha is a Principal Account Manager at Amazon Web Services, where he partners with independent software vendors (ISVs) to align their platform strategy with their business goals. He works with C-suite and senior leadership to accelerate growth, bring new capabilities to market, and turn technical investments into customer reach and differentiation.
>
> Anant Murarka
>
> Anant Murarka is a Solutions Architect at Amazon Web Services, where he works with ISV customers to design multi-tenant architectures and productionize AI-driven solutions. His areas of expertise include agentic AI, agent orchestration patterns, responsible AI, and helping product companies adopt generative AI on AWS. Outside of work, Anant is passionate about exploring how emerging AI paradigms reshape the way software products are built and delivered.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。