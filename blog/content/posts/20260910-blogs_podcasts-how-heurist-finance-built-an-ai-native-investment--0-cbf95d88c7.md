---
title: "How Heurist Finance built an AI-native investment workbench on Amazon Bedrock AgentCore"
date: 2026-09-10T02:38:15+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "Prompt 工程", "Advanced (300)", "Amazon Bedrock AgentCore", "Customer Solutions", "博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:ea3998e1df2b9e4ee6939e176a287833c67cab17b664bb0963b04d03f56eb00c"
source_payload_sha256: "sha256:8d78836d06c09c69225707a90d28fff3479f360359a2b4036ddbb3f423167a01"
observation_id: obs_cbf95d88c793339bc3c5c2ec76a8b00024643070744c610a87828291a4afd681
event_id: evt_d52f172ca8dbeb12ee8f59f8f0cfdf9dedc05acf47fc075ac96f651610c55111
revision_id: rev_083e34bfdae3352d2ab7295ed2a8d67c46d936c5d54b97602f4191b9a8a3c865
source_published_at: 2026-09-09T18:11:12Z
first_seen_at: 2026-09-09T18:48:45Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 87
interpretation_sha256: "sha256:c49f95cc978a177d6e29ce39f553cb1be84708a0a5628c129d150c7917819089"
description: "利用云端代理框架，把市场数据、新闻、财务报表等付费信息按查询购买，并与用户的持仓、风险偏好绑定，在隔离的沙箱中完成组合构建、情景分析和回测，同时记录身份、支付和操作的完整审计链。"
external_url: https://aws.amazon.com/blogs/machine-learning/how-heurist-finance-built-an-ai-native-investment-workbench-on-amazon-bedrock-agentcore
parent_observation_id: null
last_seen_at: 2026-09-09T18:36:02.133790Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/how-heurist-finance-built-an-ai-native-investment-workbench-on-amazon-bedrock-agentcore](https://aws.amazon.com/blogs/machine-learning/how-heurist-finance-built-an-ai-native-investment-workbench-on-amazon-bedrock-agentcore)
- **发布域名**: aws.amazon.com

## 要点解读

### 这是什么  
利用云端代理框架，把市场数据、新闻、财务报表等付费信息按查询购买，并与用户的持仓、风险偏好绑定，在隔离的沙箱中完成组合构建、情景分析和回测，同时记录身份、支付和操作的完整审计链。

### 用在哪里  
适用于面向散户的投资平台或金融工具，需要在保障安全合规的前提下提供机构级别的研究与分析功能，并希望降低前期数据采购成本。

### 可以推断的  
推测：采用按需付费的方式可以在用户规模较小的情况下保持对高质量数据的访问。  
推测：将身份、记忆、支付等关键能力统一封装，可帮助开发团队省去自建基础设施的工作量。

## 来源摘要/节选

> Heurist uses Amazon Bedrock AgentCore to build AI-powered financial intelligence for retail investors. Its flagship product, Heurist Finance, brings several institutional-style workflows into one chat experience: it gathers market data, reads filings and news, runs deep research, builds and stress-tests portfolios, and monitors positions. Each answer reflects the user’s portfolio and preferences. Heurist’s goal is to make tools such as unified risk-and-return views, whole-portfolio construction, and scenario analysis accessible to anyone with a market question.
>
> This post explains how Heurist built the system behind Heurist Finance on Amazon Bedrock AgentCore, using AgentCore payments, a capability of Amazon Bedrock AgentCore, to buy premium data per query. It shows how paid data access, sandboxed analysis, identity, memory, and observability come together in an auditable response.
>
> Business challenge
>
> Heurist gives retail investors access to research built on premium market, macroeconomic, fundamental, and alternative data. Those sources sit behind paywalls and bespoke APIs. No single vendor covers them all, and enterprise contracts are difficult to justify before a product has a large user base. Buying only the data required for each question offered a better economic model, but it introduced another problem. The agent would need to spend funds on a user’s behalf while enforcing custody, spending limits, and audit requirements.
>
> This creates a broader production challenge. Every action had to map to a specific user, session, and request, so identity needed to persist across the full workflow. The team also needed cross-session state, isolated code execution, payment orchestration, and end-to-end tracing. Building that infrastructure in-house could take months and divert the team from the research workflows and personalization that differentiate Heurist Finance.
>
> Solution overview
>
> Heurist deployed its agents on Amazon Bedrock AgentCore, a platform to build, connect, and optimize agents at scale with any framework or model. Heurist orchestrates its agents with Strands and uses Anthropic Claude, available on Amazon Bedrock. Figure 1 shows how the surrounding AgentCore services support each request.
>
> Figure 1: Heurist Finance solution architecture on Amazon Bedrock AgentCore
>
> Figure 1 shows the Strands orchestrator calling Anthropic Claude on Amazon Bedrock, loading portfolio data from Amazon Aurora PostgreSQL, and coordinating AgentCore Identity, Memory, Code Interpreter, Observability, and payments. Analysis artifacts go to Amazon Simple Storage Service (Amazon S3), and traces go to Amazon CloudWatch. Credentials remain in AWS Secrets Manager, while AgentCore payments connects paid data requests to USDC stablecoin settlement on the Base blockchain network.
>
> Answering a question across paid data
>
> A single user turn can combine prices, macroeconomic indicators, filings, fundamentals, and news, then run correlations, scenario analysis, charts, or backtests over the results. AgentCore Code Interpreter, a capability of Amazon Bedrock AgentCore, performs that work in an isolated sandbox with no arbitrary network egress. The sandbox runs in the AWS Cloud and tears down when the analysis finishes.
>
> Some of that data costs money, and Heurist Finance buys it per query through Amazon Bedrock AgentCore payments. A Payment Manager coordinates a CoinbaseCDP Payment Connector. Each interaction receives a Payment Session with a maxSpendAmount value that caps spending for that run and a Payment Instrument (an embedded crypto wallet) scoped to Base.
>
> Each paid request follows the x402 protocol:
>
> Heurist Finance requests a paid data feed from a merchant.
>
> The merchant returns HTTP 402 with x402 payment terms: amount, recipient, asset (USDC), and network (Base).
>
> AgentCore payments checks the payload against the Payment Session’s maxSpendAmount value. If the charge would exceed the cap, Heurist Finance tells the user and suggests alternatives.
>
> Within budget, Heurist Finance calls the Process Payment API, which signs the payment through the Payment Instrument. Credentials are retrieved at runtime from AWS Secrets Manager.
>
> Heurist Finance retries the request with proof in the X-PAYMENT header, and the merchant returns the data.
>
> With x402, Heurist Finance buys only the data a question needs, without a vendor contract or prepayment. Heurist implements the flow with AgentCore payments, a Payment Manager, a Payment Connector, and SDK integration.
>
> Research that knows the investor
>
> When a user asks a broad question, such as whether a specific stock is overvalued, Heurist Finance grounds the research in the user’s holdings, watchlist, time horizon, and risk preferences. The answer builds on prior context instead of starting from zero and becomes more specific as the profile develops.
>
> AgentCore memory, a capability of Amazon Bedrock AgentCore, stores the user’s preferences, thesis state, and conversation history across sessions. AgentCore Identity, a capability of Amazon Bedrock AgentCore, scopes that store to one user, so Heurist does not need to build a separate preference store and access-control layer.
>
> Isolation, security, and audit
>
> A user’s profile and conversation history can reveal beliefs, risk tolerance, time horizon, and positions. Heurist therefore treats identity, access, and audit as part of every request.
>
> AgentCore Identity carries the authenticated user through every service call. Each tool call, payment, and memory operation records the user ID, workload identity, request ID, and trace ID, creating one audit trail across services.
>
> Each service also enforces its own boundary. AgentCore Identity accepts OAuth and issues scoped credentials. AgentCore payments scopes the Payment Session and Payment Instrument per user, AgentCore memory binds profile and conversation data to one user, and AgentCore Code Interpreter isolates the analysis runtime.
>
> Amazon Bedrock Guardrails filters both input and output. Input filters help block prompt-injection attempts aimed at payment and data tools, while output filters help enforce Heurist’s policy against recommending an unhedged single stock. Payment credentials stay in AWS Secrets Manager, where the Payment Credential Provider retrieves them at runtime for the Payment Connector.
>
> Request flow: One user question
>
> Consider the question, “How does today’s PCE release impact my portfolio?” The orchestrator loads the user’s portfolio from Amazon Aurora PostgreSQL, with AgentCore Identity scoping the read to that user. The orchestrator then calls a paid consensus-forecast endpoint. After receiving HTTP 402, AgentCore payments checks the Payment Session spend cap and signs the payment through the Payment Instrument. The orchestrator retries the request with proof in the X-PAYMENT header.
>
> AgentCore Code Interpreter computes the portfolio impact and writes a chart to Amazon S3 from within its sandbox. Amazon Bedrock synthesizes the answer using the user’s holdings, time horizon, and risk preferences, and the response streams back with the chart attached. Figure 2 traces this sequence end to end.
>
> Figure 2: Request flow for a single user question, from profile lookup to paid data purchase to streamed answer
>
> The example brings Amazon Aurora, AgentCore Identity, AgentCore payments, AgentCore Code Interpreter, Amazon S3, Amazon Bedrock, and AgentCore Observability, a capability of Amazon Bedrock AgentCore, into one workflow. Shared user and trace context connects the paid data purchase to the resulting portfolio analysis.
>
> Outcome
>
> Heurist estimates roughly 80% less agent-system engineering than an in-house large language model (LLM) orchestration stack, because AgentCore manages identity, cross-session memory, sandboxing, and payments infrastructure. It also provides Heurist with predictable per-user marginal costs that support retail pricing.
>
> The architecture also provides two operational properties:
>
> AgentCore Observability traces make agent decisions reproducible, allowing compliance questions to be resolved in a single query, increasing compliance readiness and decreasing troubleshooting time.
>
> Payment credentials remain in AWS Secrets Manager and are retrieved at runtime by the Payment Connector, increasing safety for end users.
>
> “AgentCore does the platform work so we can double down our energy on the product work. The managed infrastructure saved us months.”
>
> — JW Wang, Founder of Heurist
>
> Conclusion
>
> Heurist’s experience shows how managed agent infrastructure can let a small team focus on differentiated financial research rather than the system beneath it. AgentCore payments is central to that model: it gives the product governed, auditable access to paid data without requiring Heurist to build payment infrastructure from scratch.
>
> What’s next
>
> With that foundation in place, Heurist is extending the product in three directions: event-driven research tied to earnings calendars, portfolio-aware analysis of market events, and recommendations based on what traders with similar horizons are researching.
>
> Get started
>
> AgentCore payments is available in the regions listed here. To learn more, visit the AgentCore payments documentation or the AWS News Blog.
>
> About the authors
>
> JW Wang
>
> JW is the founder of Heurist AI. He brings agentic AI to blockchains and financial markets, with a focus on making institutional-grade financial intelligence accessible to individual investors.
>
> Joshua Smith
>
> Joshua is a Fintech Solutions Architect at AWS. He is passionate about solving high-scale distributed systems challenges and helping customers build secure, reliable, cost-effective, and AI-enabled solutions including agentic commerce. He has a background in security and systems engineering in early startups, large enterprises, and federal agencies.
>
> Chethan Shriyan
>
> Chethan is a Principal Product Manager – Technical at AWS. He has 12+ years of experience in product and business management. Chethan is passionate about building and delivering technology products that create meaningful impact in customers’ lives.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。