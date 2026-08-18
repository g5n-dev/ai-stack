---
title: "Amazon Bedrock AgentCore payments is now generally available: Enabling agents to transact safely and autonomously at scale"
date: 2026-08-19T03:43:16+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "生成式 AI", "Prompt 工程", "Amazon Bedrock", "Announcements", "博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:7cae07c43646bfdeeba164055dba62a8e7a57bb717fc771b33196bef6d822f88"
source_payload_sha256: "sha256:e8ab17410d0354a9862d1303170e88db249d4668a513708bad4f981f0cae4c42"
observation_id: obs_9461bc7530aa1f1bca18e6617a0181f88c8cb2f1e3c10c6424b1c574e6b9f706
event_id: evt_b11d9924691eb96577c69ad7eb3994f5071c03786d34a200d52989a6160354d8
revision_id: rev_a53a144cbe534d40b11818a02189c69978b061a36a4ce76816e4b1b52fd4df8b
source_published_at: 2026-08-18T18:56:14Z
first_seen_at: 2026-08-18T19:41:10.758289Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 122
interpretation_sha256: "sha256:4b6f65402d2053df10c2840e71e88f53e350aa9fbf54423461dc31dd9d6662b3"
description: "Amazon Bedrock AgentCore payments 是一项让 AI 代理在生产环境中安全、自主完成付费任务的服务，整合了 Coinbase 与 Stripe（Privy）钱包、支持 x402 与 MPP 协议，并提供会话限额与可观测功能。"
external_url: https://aws.amazon.com/blogs/machine-learning/amazon-bedrock-agentcore-payments-is-now-generally-available-enabling-agents-to-transact-safely-and-autonomously-at-scale
parent_observation_id: null
last_seen_at: 2026-08-18T19:41:10.758289Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/amazon-bedrock-agentcore-payments-is-now-generally-available-enabling-agents-to-transact-safely-and-autonomously-at-scale](https://aws.amazon.com/blogs/machine-learning/amazon-bedrock-agentcore-payments-is-now-generally-available-enabling-agents-to-transact-safely-and-autonomously-at-scale)
- **发布域名**: aws.amazon.com

## 要点解读

### 这是什么  
Amazon Bedrock AgentCore payments 是一项让 AI 代理在生产环境中安全、自主完成付费任务的服务，整合了 Coinbase 与 Stripe（Privy）钱包、支持 x402 与 MPP 协议，并提供会话限额与可观测功能。

### 用在哪里  
适用于需要代理自行支付外部付费 API、MCP 或受版权保护内容的业务场景，例如实时网页检索、浏览器自动化平台以及企业级 AI 工作流。

### 可以推断的  
推测：在代理生态中，统一、微额的支付基础设施可能成为常态，推动更多内容和服务采用按次计费。  
推测：安全的钱钥托管与可观测特性有助于在受监管行业中合规部署自主代理。

## 来源摘要/节选

> Agents have evolved from simple chat applications to autonomous, long-running systems that dynamically discover and compose dozens of tools per task without human oversight. On the other side, service and content providers are moving from human-centric subscription-based, one-size-fits-all pricing to pay-per-use, per-execution models where costs are often a few cents. Today, agents are doing a great job at reasoning, choosing tools, and completing tasks, but they hit a roadblock when payment is involved. To address this, we launched AgentCore payments in collaboration with Coinbase and Stripe in preview in May, enabling agent developers to equip their agents to autonomously pay for paid APIs, MCPs, and content with a few lines of code. Today, we are happy to announce that this service is generally available, enabling enterprises to power agentic payments with security, guardrails, and observability for production workloads.
>
> Key features
>
> Wallet support
>
> Agents need a source of funds to make agentic transactions. AgentCore payments addresses this by integrating with Coinbase and Stripe Privy wallets, enabling developers to set up payment capabilities by providing Coinbase or Privy API keys and secrets. These are stablecoin wallets purpose-built for cost-effective microtransaction payments, often in cents. End users can fund their agent’s wallet through traditional payment methods like credit cards or through USDC stablecoin and must grant delegation to the agent to spend on their behalf. To verify security, AgentCore stores developer credentials in the AgentCore Identity Secrets Manager. The agent does not see the raw credentials. AgentCore payments uses short-lived tokens derived from these credentials to instruct the wallet provider to perform wallet operations (such as transaction signing) as directed by the developer’s agent, adding an extra layer of security for the interactions.
>
> For GA, we built a “Quick Create” option for Coinbase directly within AgentCore Payments (available through the console or CLI) that enables developers to provision credentials without leaving AgentCore, saving developers time and effort. For Stripe Privy, developers need to obtain the credentials from the Privy dashboard and provide those to AgentCore payments.
>
> Payment orchestration
>
> AgentCore payments is built to be protocol-agnostic, abstracting away the complexity so developers can integrate once and work with merchants regardless of which protocol they use. At preview, we launched with support for the x402 protocol. At GA, we have expanded protocol support to include the Machine Payment Protocol (MPP), another standard for machine payments co-authored by Stripe and Tempo, enabling developers to pay for any MPP-compatible service without an additional line of code. Additionally, we have introduced support for the “upto” scheme within x402, which enables an agent to set a spending ceiling rather than committing to a fixed price. This unlocks true pay-per-inference and dynamic pricing: a merchant serving LLM tokens, compute, or any usage-metered API can now charge for exactly what was consumed at the end of a call, rather than requiring a fixed price for requests (as with the “exact” scheme supported today).
>
> Discoverability of pay per use endpoints
>
> AgentCore exposes pay-per-use x402 endpoints offered by Coinbase as an MCP server via AgentCore Gateway, enabling agent developers to discover and select relevant paid endpoints based on their use case. We have now enhanced this discovery experience by updating the MCP server to a curated list of high-quality endpoints based on social proof, metadata richness, description quality, and availability.
>
> Payment limits
>
> Agents are inherently non-deterministic, so they can misinterpret a response as authorization to spend or repeat a payment because of an unexpected retry. In AgentCore payments, transactions run within a payment session, a scoped payment context for a single agent interaction. A payment session has two configurable caps: a maximum spend amount in a specified currency, and an expiry time. Before signing a payment, AgentCore payments checks the request against the session budget and rejects requests that would push the session past its cap. The check is deterministic and runs at the infrastructure layer.
>
> Observability
>
> As agents execute autonomous transactions, developers need comprehensive observability—including payment audit trails, detailed logs, and key metrics such as success rates and average transaction values—to maintain visibility and audit their agents’ spending behavior. AgentCore payments integrates with AgentCore Observability to give developers visibility into the payment lifecycle and automatically emits vended logs to your Amazon CloudWatch log group, and vended spans to AgentCore Observability. AgentCore Observability includes prebuilt dashboards that show end-to-end transaction health (for example, transaction success rate, average transaction value) across agents, payment sessions, and time periods.
>
> Use cases
>
> Pay for paid web content
>
> Publishers hosting content on the web today are blocking agent access and monetizing agent traffic. Enterprises deploying AI agents that access the web in real time, whether for information retrieval or web-based automation, AI browser tool providers, and agentic web search providers would benefit from integrating with the AgentCore payments service, which enables their agentic solutions to pay for paywalled web content without breaking the agent workflow. To enable this, we continue to collaborate with Content Delivery Networks (CDN) including Amazon CloudFront and Cloudflare. One of our customers, Anchor Browser, integrated with AgentCore payments to unlock paywalled web content for their customers.
>
> “Anchor Browser is one of the leading cloud-based browser automation platforms for enterprises with millions of traffic per day, purpose-built for AI agents. We are excited to integrate AgentCore payments to enable our customers to unlock paid web content within their web-based agentic workflows. The integration was smooth, and it offers a secure way to handle agentic transactions with built-in payment limits.”
>
> — Idan Raman, CEO, Co-Founder of Anchor Browser
>
> “Cloudflare sits in front of a significant share of the world’s content, APIs, and MCP servers. Our Monetization Gateway lets owners of those assets charge agents directly, per request and at a price they set using the open x402 protocol. With AgentCore payments, enterprises building agents on AgentCore can access and pay for these assets on day one.”
>
> — Stephanie Cohen, Chief Strategy Officer, Cloudflare
>
> Pay per inference
>
> Pay-per-inference is an emerging use case for agentic transactions, enabling agent developers to dynamically switch between models to optimize for cost without compromising on quality and the overhead of managing API keys and subscriptions with individual model providers. One of our customers, SpreadX, used AgentCore Payments in their new AI product, Incarna, to pay for inference through BlockRun — a routing and payment layer where agents pay per call over the x402 protocol.
>
> “We’re thrilled to collaborate with AgentCore payments, which offers a managed service that makes it easy for agents to securely access and pay for BlockRun’s pay-per-use endpoints, unlocking a whole new pay-per-inference use case.”
>
> — Vicky Fu, Founder and CEO, BlockRun
>
> Consumer and deep research use case
>
> Travala, a travel provider, has integrated AgentCore payments into their Travala Travel MCP servers, enabling end customers using agentic platforms like Claude to safely and securely book hotels conversationally in a single chat. Similarly, Elsa AI and Heurist AI use AgentCore payments to deliver financial research and advisory to their end customers by accessing pay-per-use APIs over the x402 protocol.
>
> “Integrating AgentCore payments into the Travala Travel MCP streamlines the agentic booking process for our 2.2 million properties globally. This integration offers a secure way to handle agentic transactions with built-in payment limits, improving the overall agentic booking experience for our customers.”
>
> — Juan Otero, CEO of Travala
>
> Get started with AgentCore payments
>
> AgentCore payments is available in the following regions. Developer experience and choice is the foundational design principle of AgentCore payments. With ready-to-use skills, an intuitive console, and integrations with popular open-source frameworks, we make it straightforward for developers to build with AgentCore payments so they can stay focused on what matters most: the quality and performance of their buyer agents securely at scale. You can set up and use AgentCore payments through multiple options:
>
> Coding assistant skill
>
> Whether you are building a transacting agent for the first time or adding autonomous payment capabilities to an existing agent, point your coding assistant (Claude Code, Kiro, Codex) to the skill. Your coding assistant will have the full context it needs to scaffold payment-enabled agents — from credential setup to transaction execution — so your agent can autonomously pay for paid service or content out of the box. For more details, refer to the Quick start guide.
>
> AWS Agent toolkit plugin
>
> Payment Skills &amp; CLI Samples
>
> AgentCore CLI
>
> Install the AgentCore CLI to scaffold, configure, and deploy fully transacting agents in a few commands. This wires up payment capabilities — including credential provisioning, transaction routing — giving you an end-to-end payment-enabled agent ready to transact in minutes, not days. For more details, refer to the Quick start guide.
>
> AWS Management Console
>
> You can get started with the Amazon Bedrock AgentCore console. In the navigation pane, under Build, choose Payments. The Quick Create option provides a way to create your Coinbase credentials on the console and set up your AgentCore payments resources.
>
> Open source framework integrations
>
> When building agents that transact, developers need to handle the HTTP 402 Payment Required response intercepted within their agent framework’s execution loop. AgentCore payments works with popular open source frameworks and any model. AgentCore payments provides integrations that add payment capabilities with minimal code changes. Explore the framework-specific implementations in the following section:
>
> Strands Agents plugin
>
> Documentation
>
> Example
>
> plugin = AgentCorePaymentsPlugin(config=AgentCorePaymentsPluginConfig(
>
> payment_manager_arn=os.environ["PAYMENT_MANAGER_ARN"],
>
> user_id="test-user-123",
>
> payment_instrument_id=os.environ["PAYMENT_INSTRUMENT_ID"],
>
> payment_session_id=os.environ["PAYMENT_SESSION_ID"],
>
> ))
>
> agent = Agent(model=BedrockModel(model_id=MODEL_ID, streaming=True), tools=[], plugins=[payment_plugin], system_prompt=SYSTEM_PROMPT)
>
> LangGraph middleware
>
> Documentation
>
> Example on AgentCore
>
> Example with LangSmith
>
> Blog post
>
> payments = AgentCorePaymentsMiddleware(config)
>
> agent = create_agent(model, tools=[], system_prompt=SYSTEM_PROMPT, middleware=[payments])
>
> OpenClaw plugin
>
> Explore ClawHub
>
> Example
>
> Blog post
>
> The agents-pay skill enables an agent to pay for x402-protected content at runtime — intercepting a 402 Payment Required paywall mid-task via AgentCore payments, allowing autonomous task completion without human intervention.
>
> Conclusion
>
> Today, AgentCore payments is generally available, marking a step in making the agentic economy a reality, where AI agents don’t just reason and act, but transact autonomously, securely, and at scale. By abstracting the complexity of payment protocols, wallet management, and transaction orchestration, we enable developers to focus on building intelligent agents while AgentCore handles the infrastructure. Our customers are already proving the breadth of what’s possible when payments become a native, first-class capability of the agent stack. With protocol-agnostic support, built-in spending guardrails, and production-ready observability, AgentCore payments gives developers the confidence to deploy transacting agents in production in minutes, not days. Get started today and equip your agents to transact.
>
> Resources
>
> AgentCore payments documentation
>
> AgentCore payments samples
>
> AgentCore payments skill
>
> How AgentCore payments enables safe agentic transactions
>
> Controlled agentic commerce with AgentCore payments and OpenAI Agents SDK
>
> About the authors
>
> Chethan Shriyan
>
> Chethan is a Principal Product Manager – Technical at AWS. He has 12+ years of experience in product and business management. Chethan is passionate about building and delivering technology products that create meaningful impact in customers’ lives.
>
> Madhu Samhitha Vangara
>
> Madhu is a Worldwide generative AI Specialist Solutions Architect at AWS, focusing on Agentic AI technical GTM for Amazon Bedrock AgentCore and Strands Agents. She brings deep enterprise experience translating emerging AI capabilities into measurable customer outcomes. Madhu is a speaker at AI conferences and specializes in production-grade Agentic AI.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。