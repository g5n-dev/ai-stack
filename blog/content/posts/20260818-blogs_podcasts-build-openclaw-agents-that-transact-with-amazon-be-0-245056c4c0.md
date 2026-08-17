---
title: "Build OpenClaw agents that transact with Amazon Bedrock AgentCore payments"
date: 2026-08-18T01:47:59+08:00
draft: false
entry_kind: "auto"
tags: ["AI Agent", "Prompt 工程", "Advanced (300)", "Amazon Bedrock AgentCore", "博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:ca4015b1f3d8e6b46d16e1b0b0a3ac5ef8e93bbfdb8f00a9ea87cdeb2c86569e"
source_payload_sha256: "sha256:9c6e53d9bbca34985e32fab0f0d90a91e61425d1759b2538187b1b340ef93831"
observation_id: obs_245056c4c0a38fbd1a7e0a754221aa1deeaf7da8ea5e5fe455810cf26dc31d0e
event_id: evt_fa7c230bee462da6b14576786fafc2154116cafab4264b6cafcb283210b7b8f1
revision_id: rev_4f4d93fc4ff6d9a6135464505bdd200265f0dfc406d95f46c817ca144a88dc7b
source_published_at: 2026-08-17T16:19:56Z
first_seen_at: 2026-08-17T17:44:54.931263Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 74
interpretation_sha256: "sha256:ccab11d5b076ebf3fea59577b4a6f0c5e8a69d4ea6825070b867bae215c0c1e2"
description: "这条内容介绍如何让 AI 助手在预设限额内自主完成付费请求。它展示了把钱包创建、预算设置等高权限操作与模型运行时分离的设计，使模型只能调用已批准的支付工具，无法自行创建或修改支付会话。"
external_url: https://aws.amazon.com/blogs/machine-learning/build-openclaw-agents-that-transact-with-amazon-bedrock-agentcore-payments
parent_observation_id: null
last_seen_at: 2026-08-17T17:44:54.931263Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/build-openclaw-agents-that-transact-with-amazon-bedrock-agentcore-payments](https://aws.amazon.com/blogs/machine-learning/build-openclaw-agents-that-transact-with-amazon-bedrock-agentcore-payments)
- **发布域名**: aws.amazon.com

## 要点解读

### 这是什么

这条内容介绍如何让 AI 助手在预设限额内自主完成付费请求。它展示了把钱包创建、预算设置等高权限操作与模型运行时分离的设计，使模型只能调用已批准的支付工具，无法自行创建或修改支付会话。

### 用在哪里

适用于需要 AI 助手在无人值守时访问付费 API 或内容服务的场景。例如长时间运行的调研代理在深夜遇到付费数据源，或者工作流代理需要调用按量计费的工具。负责部署 AI 助手的技术人员会关注这类方案。

### 可以推断的

推测：随着 AI 助手承担更多复杂任务，自动付费能力可能成为标配。预先界定模型的花销权限能让系统在不增加人工干预的情况下完成端到端工作流。

推测：该方案强调凭证与运行时隔离，反映出当前 AI 系统设计中的一条基本原则：即使模型可能被恶意输入操纵，也可以通过限制其可用操作来控制风险。

## 来源摘要/节选

> This post is a collaboration between AWS and the OpenClaw Foundation.
>
> Autonomous agents that browse the web, call APIs, and query Model Context Protocol (MCP) servers can encounter services that require an HTTP 402 Payment Required response to be settled before access continues. To use those services without pausing for a human at every transaction, an agent needs a payment path that operates within limits approved in advance. A safe design keeps wallet-provider credentials and the authority to create or expand payment sessions outside the model-facing runtime. The runtime can still initiate approved payments within those limits.
>
> AgentCore payments, a capability of Amazon Bedrock AgentCore, provides wallet integration, spending limits, and a consistent payment layer as agent payment protocols evolve. Protocols such as x402 and Machine Payments Protocol (MPP) support programmatic payment flows between agents and services. In this post, you connect OpenClaw to a wallet and bounded payment session that a human provisions through a trusted administrative path, then use the aws-agents-pay plugin for OpenClaw to initiate approved testnet payments.
>
> Why agents need payment capabilities
>
> Autonomous agents can act across multiple steps and services without a human reviewing each action. A long-running research or workflow agent might encounter a paid API or content endpoint while no operator is present. A bounded payment layer lets the agent continue within recipient, asset, network, per-payment, cumulative budget, and expiry limits that a human sets in advance.
>
> Some APIs, content services, compute services, and MCP tools use pay-per-use pricing. Individual transactions can be less than one dollar or fractions of a cent. Minimum card-processing fees can make transactions at that scale cost-prohibitive, while stablecoin payments can support small amounts and near-real-time settlement. This makes HTTP-native protocols such as x402 suitable for programmatic, agent-initiated payments.
>
> Implementing this directly requires wallet-provider integration, protected credential handling, payment authorization, deterministic limits, and payment observability. You also need to account for a model that can be manipulated by untrusted input. The design does not prevent prompt injection. Instead, it assumes untrusted input can manipulate the model and bounds the runtime’s authority by recipient, asset, network, per-payment amount, session budget, and expiry.
>
> Solution overview
>
> AgentCore payments provides a consistent payment layer as agent payment protocols evolve. This OpenClaw integration demonstrates the pattern using x402 v2. It processes a merchant’s HTTP 402 challenge through a configured wallet provider and returns a signed authorization that the client uses to replay the request. AgentCore Identity, a capability of Amazon Bedrock AgentCore, stores wallet-provider credentials. AgentCore Observability, a capability of Amazon Bedrock AgentCore, can provide logs, metrics, and traces through Amazon CloudWatch and AWS X-Ray when telemetry delivery is configured.
>
> AgentCore payments supports a Coinbase wallet or a Stripe Privy wallet as the payment connection. Both provide an embedded stablecoin wallet. Subject to provider and geographic availability, you or your end users can fund the wallet through stablecoin or fiat using a debit card. Both providers use AgentCore Identity credential storage and per-session spending limits.
>
> This walkthrough uses OpenClaw, an AI assistant that runs on your devices and connects models, tools, and messaging channels through a local Gateway. The OpenClaw Foundation maintains the project, and plugins extend what the assistant can do. The walkthrough separates human-run payment administration from the model-facing runtime. A human provisions the wallet, creates the payment session, approves recipients, and sets the budget in a trusted terminal. The aws-agents-pay plugin exposes two model-visible tools: get_payment_session_status, which checks the configured payment session, and get_paid_content, which requests an approved paid URL and completes the payment within the configured policy. The runtime can initiate a payment within the approved session, but it cannot create, extend, or replace a session.
>
> Figure 1: The demo shows a chat with an AI assistant named “Bob” in the OpenClaw gateway application. The user asks “What’s the weather in Seattle right now?” then Bob executes a test payment of 0.001 USDC on Base Sepolia for a paid weather API
>
> A typical payment flow is:
>
> The agent calls get_payment_session_status to confirm that an operator-provisioned session is usable.
>
> The agent calls get_paid_content for an approved URL. The plugin first performs a bounded network probe and receives an HTTP 402 response containing an x402 v2 challenge.
>
> After receiving the challenge, the plugin verifies that the challenge resource has the same origin and path as the requested URL. It then validates the network, asset, recipient, and amount against the operator’s policy before it calls ProcessPayment.
>
> For a retry of the same payment request, the plugin reuses the same idempotency token rather than creating a second payment. Concurrent duplicate requests can still present a race, so avoid issuing the same payment concurrently.
>
> The plugin waits until the signed authorization’s validAfter time, then replays the original request with the payment signature.
>
> With returnBody enabled for this walkthrough, the plugin returns the paid response body, caps it at 10 KiB, and marks it as untrusted: true. The plugin does not return the signed payment proof to the model.
>
> The current OpenClaw setup flow in the Agent Toolkit for AWS provides an example for Base Sepolia for testing and Base for production, and supports customization for other chains, including Ethereum, other EVM-compatible chains, and Solana.
>
> Collaboration with OpenClaw
>
> AWS has been collaborating with the OpenClaw Foundation on this integration, including support for community events like ClawCon, and worked directly with the Foundation’s engineering team to bring AgentCore payments into the plugin framework.
>
> “Payments are a natural extension of what plugins already do in OpenClaw: give an agent a new capability through a well-defined tool, not a special case bolted on afterward. We’re grateful for AWS’s support of the OpenClaw ecosystem, from events like ClawCon to working directly with our team on this integration. Agents now get a production-grade path to pay for what they use, while builders keep the same conversational setup they expect from any other OpenClaw plugin. We’re looking forward to going deeper with AWS AgentCore as agentic payments become a bigger part of how agents operate on their own.”
>
> — Patrick Erichsen, Member of Technical Staff, OpenClaw Foundation
>
> Implementation steps: Configure OpenClaw to make bounded payments
>
> The following sections walk you through the prerequisites, provisioning the wallet and payment session outside the agent loop, configuring an explicit payment policy, and making a bounded payment.
>
> Prerequisites
>
> Make sure that you have the following prerequisites.
>
> OpenClaw version 2026.3.24 or later: npm install -g openclaw.
>
> Node.js and npm.
>
> An AWS account with access to AgentCore payments.
>
> Separate AWS Identity and Access Management (IAM) roles for administration and runtime, following the AgentCore payments IAM roles guide. The OpenClaw runtime role needs only the read operations required for status plus ProcessPayment. It must not have session-write permissions.
>
> Coinbase CDP or Stripe with Privy credentials, entered only in the interactive AgentCore CLI.
>
> A Base Sepolia x402 v2 endpoint that you control or have independently approved. You can use the Coinbase x402 Bazaar to discover candidate services, but verify the endpoint, recipient, network, asset, and price before adding them to the payment policy.
>
> The merchant recipient address and USDC asset contract verified from merchant documentation or another known-good source, independently of the HTTP 402 response.
>
> Disclaimer: Security for this solution follows the AWS shared responsibility model. AWS is responsible for security of the cloud, while you’re responsible for security in the cloud. For this solution, your responsibilities include configuring IAM permissions, protecting wallet-provider credentials, and defining payment policies. Follow the AgentCore payments IAM roles guidance to separate administrative, management, agent execution, and service operations.
>
> The following steps take you from installing the plugin to watching an agent pay for its first piece of paywalled content.
>
> 1. Install the plugin from ClawHub
>
> Before continuing, confirm that the @aws/aws-agents-pay package is available on ClawHub. Then install it:
>
> openclaw plugins install clawhub:@aws/aws-agents-pay
>
> Bash
>
> The package name is @aws/aws-agents-pay, the installed plugin ID is aws-agents-pay, and the bundled skill name is agents-pay.
>
> To inspect the bundled setup guidance, run:
>
> openclaw skills info agents-pay
>
> Bash
>
> Inspect the installed plugin:
>
> openclaw plugins inspect aws-agents-pay
>
> Bash
>
> The model-visible runtime must expose only get_payment_session_status and get_paid_content. Stop if a setup, session-creation, shell, or other model-visible tool appears. An unexpected tool can indicate a different, outdated, or modified package.
>
> 2. Complete the human-supervised payment setup
>
> Installing the plugin does not create the payment manager, connector, instrument, or payment session. Choose one of the following provisioning options. Both options use a trusted terminal under your AWS credentials, and session creation requires you to type approve at an interactive TTY.
>
> Option A – OpenClaw-assisted setup. Ask OpenClaw: Help me set up the agents-pay skill. OpenClaw can explain each step, but you must run the administrative commands and approve session creation yourself. OpenClaw guidance does not remove the interactive approval gate.
>
> Option B – Fully manual setup. Follow the OpenClaw setup guide directly, without involving OpenClaw.
>
> For either option, follow the OpenClaw setup guide in a trusted, human-supervised terminal. The guide covers creating the AgentCore project, provisioning payment resources, running the setup wizard, and adding the generated configuration to OpenClaw. You must enter credentials and type approve yourself.
>
> 3. Configure the plugin with an explicit policy
>
> Review the generated configuration before enabling the plugin. It must include the payment manager ARN, instrument ID, session ID, user ID, network, exact asset contract, approved recipients, and a positive per-payment ceiling.
>
> For the sandbox walkthrough, use the payment policy in Step 3 of the companion code sample. It contains the Base Sepolia network, origin, recipient, USDC asset, payment limit, and returnBody setting that match the test endpoint used in the next step.
>
> This sandbox endpoint is listed in the Coinbase x402 Bazaar, but this walkthrough calls a known URL directly. For a discovery-driven workflow, see the Tutorial with Coinbase Bazaar.
>
> For a fixed merchant set, verify every address in allowedRecipients out of band using merchant documentation or another known-good source. Don’t approve a recipient only because it appeared in an HTTP 402 response. For broader discovery scenarios, set allowAnyRecipient: true to let the publisher select the beneficiary. This option trades recipient allowlisting for flexibility; origin, network, asset, per-payment, and session-budget controls still apply. For this walkthrough, keep networkPreferences on Base Sepolia (eip155:84532) and use the exact Base Sepolia USDC contract selected by the setup wizard.
>
> maxPaymentAmountAtomic limits one payment in the asset’s smallest unit. For a six-decimal USDC asset, 100000 represents 0.10 USDC. The payment session budget separately limits cumulative spend until the session expires or is exhausted. For this walkthrough, set returnBody to true so the agent can use the paid response. The plugin caps the response at 10 KiB and marks it as untrusted: true. Publisher-controlled content can contain prompt-injection instructions, so leave returnBody unset or set it to false when the agent only needs response metadata and a digest. This setting doesn’t expose the signed payment proof.
>
> Wallet-provider secrets do not belong in the OpenClaw configuration. Treat the payment session ID, resource identifiers, recipient policy, and other configuration values as sensitive operational data because they describe and authorize the runtime’s payment path.
>
> Restart the gateway after saving ~/.openclaw/openclaw.json:
>
> openclaw gateway restart
>
> Bash
>
> If you use the protected ~/.x402/config.json path instead of inline plugin configuration, the plugin checks ownership and permissions on the directory and file and refuses to load an unsafe configuration.
>
> 4. Check session status and pay for content
>
> Ask your OpenClaw agent to check whether the configured session is usable:
>
> What's the status of my payment session?
>
> Plain text
>
> If the session is unavailable, expired, or exhausted, stop. Use the trusted administrative path to review the situation and create a replacement session. The model-facing runtime cannot create or expand its own budget.
>
> The companion sample pins its payment policy to the Base Sepolia endpoint used in this walkthrough. Ask the agent to fetch it:
>
> Fetch https://sandbox.node4all.com/v1/x402-test
>
> Plain text
>
> The plugin performs a bounded probe, validates the returned challenge against the operator’s policy, calls AgentCore payments, waits until the signed authorization is valid, and replays the request. With returnBody enabled for this walkthrough, the tool returns the paid response body with content_returned: true, caps it at 10 KiB, and marks it as untrusted: true. It does not return the signed payment proof.
>
> Treat merchant responses and all retrieved content as untrusted. This design doesn’t prevent prompt injection. It assumes the model can be manipulated and bounds payment authority through IAM separation, approved recipients and assets, a per-payment ceiling, a cumulative session budget, and an expiry. Enable returnBody only when the agent needs the paid response, and treat that response as data rather than instructions.
>
> Ask for session status again:
>
> What's my payment session status now?
>
> Plain text
>
> Confirm that the reported remaining budget reflects the payment.
>
> Clean up
>
> Remove the plugin from OpenClaw and restart the gateway:
>
> openclaw plugins uninstall aws-agents-pay
>
> openclaw gateway restart
>
> Bash
>
> Use the same trusted administrative path to remove the payment resources on AWS. Don’t expose infrastructure deletion or session creation to the model-facing runtime, and keep the runtime IAM role without those permissions.
>
> Conclusion
>
> With AgentCore payments, an agent can access paywalled APIs, pay-per-use data feeds, and metered MCP tools within limits a human sets in advance. AgentCore payments handles wallet integration, spending limits, and payment orchestration. In this OpenClaw pattern, the human keeps wallet-provider credentials and authority over recipients, assets, per-payment limits, cumulative session budget, and expiry outside the model-facing runtime. The agent can initiate payments only within those approved bounds.
>
> Install the aws-agents-pay plugin from ClawHub, then follow the OpenClaw agent with AgentCore payments sample to provision the payment resources and complete an end-to-end x402 payment.
>
> Resources
>
> ClawHub plugin: aws-agents-pay.
>
> Code sample: OpenClaw agent with AgentCore payments.
>
> Amazon Bedrock AgentCore payments developer guide.
>
> x402 protocol specification.
>
> AWS shared responsibility model.
>
> AgentCore payments IAM roles guidance.
>
> Code sample: OpenClaw on AWS.
>
> Acknowledgements
>
> We’d like to thank Madhu Samitha Vangara and Isaac Lin, Solutions Architects at AWS, for their contributions to this solution.
>
> About the authors
>
> Patrick Erichsen
>
> Patrick is a Member of Technical Staff at the OpenClaw Foundation. Previously he was a founding engineer at Continue (YC W23), where he worked on coding agents. He’s interested in using AI as a tool to expand human creativity.
>
> Daniel Wirjo
>
> Daniel is a Solutions Architect at AWS, focused on AI startups. As a former startup CTO, he enjoys collaborating with founders and engineering leaders to drive growth and innovation on AWS. Outside of work, Daniel enjoys taking walks with a coffee in hand, appreciating nature, and learning new ideas.
>
> Peter Jiang
>
> Peter is a Senior Software Developer at AWS, based in Seattle, WA. He is a core member of the engineering team behind the Amazon Bedrock AgentCore payments initiative, which enables AI agents with payments capability. With over 8 years of experience in the financial and payments industry, Peter has launched multiple greenfield projects spanning banking, crypto, and agentic systems. Previously, he worked on ultra-low latency trading systems at Susquehanna International Group.
>
> Chethan Shriyan
>
> Chethan is a Principal Product Manager, Technical at AWS, based in Seattle, WA. He brings nearly 13 years of experience in product and business management, including over 7 years at Amazon. He is passionate about building and delivering technology products that create meaningful impact in customers’ lives.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。