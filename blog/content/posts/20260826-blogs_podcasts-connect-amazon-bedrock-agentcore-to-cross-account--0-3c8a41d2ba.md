---
title: "Connect Amazon Bedrock AgentCore to cross-account knowledge bases"
date: 2026-08-26T23:56:06+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "生成式 AI", "机器学习", "Prompt 工程", "Amazon Bedrock AgentCore", "Amazon Bedrock Knowledge Bases", "Expert (400)"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:67f61d8c3cfd29646d2709ebf0baa7979c8239391a4439b0c3b4f45b5f4dfc86"
source_payload_sha256: "sha256:5a75e87ce4c7b8c4e7db95040d9451e5ee6cca8738f496b772e15dce4a3c558c"
observation_id: obs_3c8a41d2ba407782092359430a0daeaf6a1fff5cf1d8b3039a111d5bb6840ab8
event_id: evt_c569b19c551b619c30a148de5430f4840d7a1c789643b04cf68c26ea4df449b4
revision_id: rev_f90de47feb32398964bb38f8c3006b2be06a6f2849bc52601e10d177f29d7ff1
source_published_at: 2026-08-26T15:48:10Z
first_seen_at: 2026-08-26T15:53:22.459248Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 65
interpretation_sha256: "sha256:c3e174744148a54c7bf2ea51788155dfc1f3d9f4bb9082b4d8a8f13fee77ca70"
description: "这是一篇关于在 Amazon Bedrock AgentCore 中实现跨账号访问知识库的技术实践，提供了代码化的 Strands agent 和声明式的 AgentCore harness 两种实现路径，并说明了它们在访问另一账号 Redshift Serverless 数据时的具体做法。"
external_url: https://aws.amazon.com/blogs/machine-learning/connect-amazon-bedrock-agentcore-to-cross-account-knowledge-bases
parent_observation_id: null
last_seen_at: 2026-08-26T15:53:22.459248Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/connect-amazon-bedrock-agentcore-to-cross-account-knowledge-bases](https://aws.amazon.com/blogs/machine-learning/connect-amazon-bedrock-agentcore-to-cross-account-knowledge-bases)
- **发布域名**: aws.amazon.com

## 要点解读

### 这是什么
这是一篇关于在 Amazon Bedrock AgentCore 中实现跨账号访问知识库的技术实践，提供了代码化的 Strands agent 和声明式的 AgentCore harness 两种实现路径，并说明了它们在访问另一账号 Redshift Serverless 数据时的具体做法。

### 用在哪里
适用于多账号 AWS 环境中构建 AI Agent 的场景，特别是需要让 Agent 在不复制数据的情况下访问其他账号受治理数据的企业。

### 可以推断的
推测：跨账号架构通常用于分离不同职责域（如数据域和业务域），以满足安全合规或成本核算需求。
推测：提供两种变体表明在实际落地时不同团队的控制能力不同，需要根据团队对编排逻辑的定制需求来选择实现方式。

## 来源摘要/节选

> Organizations often deploy agents using Amazon Bedrock AgentCore, a platform to build, connect, and optimize agents at scale, with any framework or model. These agents may access governed knowledge bases hosted in separate AWS accounts. This cross-account separation helps maintain clear workload boundaries but can introduce integration challenges.
>
> This post explains how AgentCore agents in one account can generate answers from a knowledge base (using Amazon Bedrock Knowledge Bases, the fully managed Retrieval Augmented Generation capability) backed by Amazon Redshift Serverless in another account without copying source data.
>
> This post covers the architecture, security boundary, request flow, and selection criteria for two generally available Amazon Bedrock AgentCore orchestration models. The linked GitHub sample provides the deployment procedures and implementation details for both variants:
>
> A code-based Strands agent on AgentCore runtime, a capability of Amazon Bedrock AgentCore.
>
> A declarative AgentCore harness, a capability of Amazon Bedrock AgentCore.
>
> The challenge
>
> Organizations that build AI agents using Amazon Bedrock can maintain structured data in Amazon Redshift Serverless. These data repositories can reside in separate AWS accounts from their AI agents. Amazon Bedrock Knowledge Bases resource policies support Retrieve and GetDocumentContent for cross-account operations. The supported resource policy actions do not include RetrieveAndGenerate. Because this solution needs the generated answer returned by RetrieveAndGenerate, the tool assumes a narrowly scoped AWS Identity and Access Management (IAM) role in the Knowledge Base account before calling the API.
>
> This creates a challenge for enterprises with multi-account architectures who want to:
>
> Generate natural-language answers over structured data in Amazon Redshift Serverless.
>
> Maintain account boundaries between agent workloads and data workloads.
>
> Avoid copying governed source data into the agent account.
>
> Grant least-privilege access through a dedicated cross-account IAM role.
>
> Solution overview
>
> The solution implements the cross-account query pattern in two ways. Variant 1 deploys a Strands agent to AgentCore runtime. Variant 2 uses a declarative AgentCore harness. Both implementations use the same data access boundary. The model-controlled tool assumes the Knowledge Base access role with AWS Security Token Service (AWS STS), calls RetrieveAndGenerate, and returns the generated answer and citations to the orchestration layer. The variants differ in who owns the agent loop and how the tool is hosted. Figure 1 compares the two orchestration paths and their shared cross-account data access boundary.
>
> Figure 1: Side-by-side AgentCore implementation paths
>
> Request flow
>
> The request follows this sequence:
>
> A user submits a natural-language question through Streamlit UI or an AgentCore API.
>
> Amazon Nova Pro decides to call the query_knowledge_base tool.
>
> In Variant 1, the tool runs in a local Model Context Protocol (MCP) subprocess packaged with AgentCore runtime. In Variant 2, the AgentCore harness calls an AWS Lambda tool through AgentCore Gateway, a capability of Amazon Bedrock AgentCore.
>
> The tool assumes the bedrock_kb_access_role in the Knowledge Base account by using AWS STS.
>
> The assumed-role session calls RetrieveAndGenerate with Claude Haiku 4.5. The Knowledge Base translates the question into a structured query against Amazon Redshift Serverless.
>
> The generated answer returns through the selected orchestration path to the user.
>
> Figure 2 shows the request path for the code-based Strands agent.
>
> Figure 2: Code-based Strands agent architecture
>
> Figure 3 shows the corresponding managed path for the declarative AgentCore harness.
>
> Figure 3: Declarative AgentCore harness architecture
>
> Choose the simplest sufficient pattern
>
> Before selecting an agent implementation, decide whether the workload needs an agent at all. This keeps the design proportional to the required behavior.
>
> If the application only needs retrieved content, evaluate native cross-account Retrieve with a Knowledge Base resource policy.
>
> If every request deterministically needs one generated answer, first confirm that the workload does not need tool selection, multi-step reasoning, or conversational state. If it does not, assume the Knowledge Base account role and call RetrieveAndGenerate directly from the application or an AWS Lambda function.
>
> Use an agent when the model must decide when or how to query the Knowledge Base as part of a broader conversation or tool-using workflow.
>
> When to use each AgentCore variant
>
> The cross-account requirement does not favor one variant. Choose according to how much of the orchestration loop your team needs to customize and operate.
>
> Decision area
>
> Code-based Strands agent
>
> Declarative AgentCore harness
>
> Best fit
>
> Teams that require custom orchestration, hooks, middleware, retry behavior, instrumentation, or direct control of tools and streaming.
>
> Teams whose use case fits the managed loop and who prefer a configuration-first lifecycle.
>
> Agent loop
>
> Your Python code runs the loop with the Strands Agents SDK.
>
> AgentCore runs the loop from the harness definition.
>
> Tool path
>
> AgentCore runtime to local MCP subprocess to Knowledge Base.
>
> AgentCore harness to AgentCore Gateway to AWS Lambda to Knowledge Base.
>
> Cross-account principal
>
> AgentCore runtime execution role.
>
> AWS Lambda execution role behind AgentCore Gateway.
>
> What you maintain
>
> agent.py, dependencies, MCP server, tool logic, and runtime configuration.
>
> AgentCore harness configuration, system prompt, AWS Lambda tool, IAM, and application behavior.
>
> Invocation API
>
> InvokeAgentRuntime.
>
> InvokeHarness.
>
> The decision is custom control versus managed orchestration.
>
> Prerequisites
>
> Before you begin, confirm that you have the following prerequisites:
>
> Two AWS accounts: an agent account and an agent-kb account.
>
> AWS Command Line Interface (AWS CLI) v2.24.22 or later with credentials for both accounts.
>
> Python 3.10 or later and jq.
>
> A structured Amazon Bedrock knowledge base connected to Amazon Redshift Serverless.
>
> Model access in US West (Oregon): us.amazon.nova-pro-v1:0 in the agent account and us.anthropic.claude-haiku-4-5-20251001-v1:0 in the agent-kb account. For model availability by Region, refer to Supported models by AWS Region in Amazon Bedrock.
>
> For the harness variant, install the current @aws/agentcore Node.js CLI in addition to the Python bedrock-agentcore CLI used by the code-based variant.
>
> Assumptions
>
> The examples use the following local profile aliases and placeholder account IDs:
>
> Profile
>
> Example account
>
> Purpose
>
> agent
>
> 111122223333
>
> Hosts AgentCore resources.
>
> agent-kb
>
> 999999999999
>
> Hosts the Knowledge Base and Redshift Serverless.
>
> The examples use the US West (Oregon) Region (us-west-2). Profile names are local aliases, so replace them with your configured profile names and discover account IDs instead of hardcoding them.
>
> AGENT_PROFILE=agent
>
> AGENT_KB_PROFILE=agent-kb
>
> REGION=us-west-2
>
> AGENT_ACCOUNT=$(aws sts get-caller-identity \
>
> --profile "$AGENT_PROFILE" --query Account --output text)
>
> AGENT_KB_ACCOUNT=$(aws sts get-caller-identity \
>
> --profile "$AGENT_KB_PROFILE" --query Account --output text)
>
> aws bedrock-agent list-knowledge-bases \
>
> --profile "$AGENT_KB_PROFILE" --region "$REGION"
>
> Implementation walkthrough
>
> This post focuses on architecture and decision guidance. Deployment procedures are maintained in the public GitHub sample. Use the Implementation walkthrough to prepare the structured Knowledge Base, cross-account IAM roles, and AgentCore memory, a capability of Amazon Bedrock AgentCore. Then follow Running the agent for the code-based Strands variant or Variant 2 – Declarative harness for the managed agent loop. The sample also includes the Streamlit end-to-end client for the Local, AgentCore, and Harness UI modes.
>
> Validation
>
> Use the same question, Knowledge Base ID, model, retrieval count, and fresh session when comparing variants. The prompt contract tells both agents to pass the user’s question to the tool exactly as written, but RetrieveAndGenerate remains generative. For row-level questions, specify a row count, date range, and sort order. Unbounded generated SQL can exceed result-handling limits. Validate business facts against the direct tool response and the underlying structured data.
>
> In the Streamlit client, select the invocation mode before comparing results. For AgentCore or Harness mode, confirm that the corresponding deployed resource Amazon Resource Name (ARN) is populated. Start a new conversation for each independent factual comparison.
>
> Figure 4: Select Local, AgentCore, or Harness in the Streamlit sidebar
>
> Figure 5 shows a successful bounded query in Harness mode.
>
> Figure 5: Harness mode with the deployed ARN and a successful bounded query
>
> Sample questions for the TPC-H dataset include:
>
> Who are the top 5 customers in Saudi Arabia?
>
> Who are the top parts suppliers in the United States by volume?
>
> What is the total revenue by region for 1998?
>
> Which products generated the highest revenue after discounts?
>
> Show the 100 highest-value orders marked 1-URGENT from October 1 through December 31, 1997.
>
> Recommended practices
>
> Apply these practices when deploying and validating either variant:
>
> Use fresh session IDs for independent factual comparisons.
>
> Log the exact tool query, Knowledge Base ID, model ID, and retrieval result count.
>
> Define derived business metrics with approved curated SQL and column descriptions.
>
> Bound row-level questions with an explicit row count, date range, and sort order to avoid oversized SQL result sets.
>
> Keep the cross-account role scoped to the required Knowledge Base and model resources.
>
> Use refreshable STS credentials in long-lived runtimes and warm AWS Lambda environments.
>
> Test system prompts, tool descriptions, IAM, and application behavior for both variants.
>
> Apply Amazon Bedrock Guardrails to evaluate user questions and generated answers for harmful content, denied topics, and sensitive information. Guardrails complement, but do not replace, least-privilege access, source data governance, citation-based verification, and human review for consequential decisions.
>
> Clean up resources
>
> Follow the sample’s cleanup section for the current commands and required order. When both variants are deployed, complete harness cleanup first so that its AWS Lambda execution-role trust grant is removed from the shared Knowledge Base access role. Then remove the code-based runtime and shared IAM resources. The scripts do not delete the project-managed AgentCore memory, Knowledge Base, or Redshift Serverless resources. Delete those separately when they are no longer needed.
>
> Summary
>
> This post describes how AgentCore agents can return generated answers from a structured Amazon Bedrock knowledge base across AWS account boundaries. Both implementations use a least-privilege role in the data account. The architectural choice is who owns the agent loop and how the tool is hosted. Start with native Retrieve or a direct RetrieveAndGenerate call when those patterns satisfy the workload. When model-controlled tools or conversational orchestration are required, choose the code-based Strands variant for custom loop behavior and direct control. Choose the AgentCore harness when its managed loop fits and your team prefers a configuration-first operating model. Both are valid, generally available paths. Here is the Amazon Bedrock AgentCore Documentation where you can get started with Amazon Bedrock AgentCore with code samples.
>
> About the authors
>
> Kunal Ghosh
>
> Kunal is an expert in AWS technologies. He is passionate about building efficient and effective solutions on AWS, especially involving generative AI, analytics, data science, and machine learning. Besides family time, he likes reading, swimming, biking, watching movies, and exploring food.
>
> Arghya Banerjee
>
> Arghya is a Sr. Solutions Architect at AWS in the San Francisco Bay Area, focused on helping customers adopt and use the AWS Cloud. His areas of focus include big data, data lakes, streaming and batch analytics services, and generative AI.
>
> Indranil Banerjee
>
> Indranil is a Sr. Solutions Architect at AWS in the San Francisco Bay Area, focused on helping customers in the high-tech and semiconductor sectors solve complex business problems using the AWS Cloud. His interests include modernization, migration, analytics platforms, and generative AI.
>
> Yoginder Sethi
>
> Yoginder is a Senior Solutions Architect on the Strategic Accounts Solutions Architecture team at AWS. He has extensive experience designing, building, and managing large-scale cloud architectures, DevOps tooling, and observability solutions. Based in the San Francisco Bay Area, California, he enjoys exploring new places, listening to music, and hiking outside of work.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。