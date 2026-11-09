---
title: "Getting started with Web Answer on Amazon Bedrock AgentCore"
date: 2026-11-06T08:15:05+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "Prompt 工程", "Amazon Bedrock", "Amazon Bedrock AgentCore", "Intermediate (200)", "Technical How-to", "博客与播客"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:cf1e9497fd874a4e0d10c5e4d66da4381d1f24b87b2e9238378daca8822c7303"
source_payload_sha256: "sha256:92507acda08d9293716d89aaa8f9b234f4f6f2fee81c84d9e16eeec82112c468"
observation_id: obs_614ec411e822a540898f15e570bc65f7c99b1de4d8e763c931bcb2cccaf8f043
event_id: evt_d1fb334d50dabd2939a698e52348a32ed767b5af7ed03e4beb97c88eb661747a
revision_id: rev_88d6824c759ca264bbd9d3483a217eb80d4213ea240d76bbea118555bc145eab
source_published_at: 2026-11-05T21:04:24Z
first_seen_at: 2026-11-06T00:24:00Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 59
interpretation_sha256: "sha256:f0dae21dd052a34073b7f7cbed5d4449262bd09277bb95763a25cfb120687951"
description: "Amazon Bedrock AgentCore 的 Web Answer 现已正式可用。开发者只需调用一次工具，即可获得基于当前网页信息、由模型综合生成并附带来源链接的回答，无需自行搭建搜索、检索、内容清洗和引用提取流程。"
external_url: https://aws.amazon.com/blogs/machine-learning/getting-started-with-web-answer-on-amazon-bedrock-agentcore
parent_observation_id: null
last_seen_at: 2026-11-09T00:00:00Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/getting-started-with-web-answer-on-amazon-bedrock-agentcore](https://aws.amazon.com/blogs/machine-learning/getting-started-with-web-answer-on-amazon-bedrock-agentcore)
- **发布域名**: aws.amazon.com

## 要点解读

### 这是什么
Amazon Bedrock AgentCore 的 Web Answer 现已正式可用。开发者只需调用一次工具，即可获得基于当前网页信息、由模型综合生成并附带来源链接的回答，无需自行搭建搜索、检索、内容清洗和引用提取流程。

### 用在哪里
它适合需要从实时网页回答具体事实问题、但希望减少检索管线维护工作的智能体开发者。管理员可通过 AgentCore Gateway 接入该工具，再以 MCP 工具形式供智能体调用。

### 可以推断的
- 推测：对重视答案可追溯性、同时不想维护完整搜索与引用系统的团队，这一工具可能明显降低接入成本。
- 推测：需要自行控制搜索结果处理方式的团队，可能更适合使用仅返回原始检索结果的 Web Search。

## 来源摘要/节选

> Today, we are announcing the general availability of Web Answer on Amazon Bedrock AgentCore. With Web Answer, agent builders get a synthesized, source-cited answer to a natural-language question with a single tool call. They no longer build a search, retrieve, synthesize, and citation pipeline themselves.
>
> If you have built agents that need to answer questions from current web sources, you know the pattern: call a search API, decide which results to trust, retrieve and clean page content, prompt a model to synthesize, and engineer citation extraction so the output traces back to a source. Every step is code you maintain, and every step is another place things can go wrong: hallucination when evidence is insufficient, stale content when the index moves, and broken attribution when a claim and its source drift apart.
>
> The Web Answer collapses that entire pipeline into one request. You send a question. You get back a cited answer in seconds. In this post, we explain what Web Answer does, compare it with Web Search on AgentCore, show how it works and what it returns, and walk through adding Web Answer to a gateway and calling it from an agent.
>
> What Web Answer does
>
> Figure 1: Request flow from an agent through the Gateway to Web Answer and back
>
> Your agent sends a question to your AgentCore Gateway, a capability of Amazon Bedrock AgentCore. The Gateway authenticates the call with AWS Identity and Access Management (AWS IAM) or a JSON Web Token (JWT). The Gateway calls Web Answer, a managed connector that AWS owns, using its own service role. Web Answer plans its searches, runs several in parallel, and reads key pages to check the facts. When the evidence is insufficient, it searches again. It then writes an answer that ties each claim to its source URL. The Gateway returns the answer and its citations to your agent as a Model Context Protocol (MCP) tool result.
>
> Web Answer is a managed AgentCore Gateway tool that takes a natural-language question and returns a synthesized answer in seconds grounded in current web sources. Here is what you get back:
>
> A grounded, cited answer, where each grounded claim maps to a citation, with a source URL where one is available.
>
> Current sources. Web Answer runs new searches for every question, and its model is given today’s date so it can search for up-to-date information.
>
> Agentic search: Web Answer plans its own searches, runs several in parallel, reads pages to verify facts, and decides when it has enough evidence to answer.
>
> Responsible AI safeguards: Web Answer is designed and tested with responsible AI safeguards.
>
> Figure 2: Demo video showing how to add Web Answer to an AgentCore Gateway, from setup to a finished, cited answer
>
> How it differs from Web Search
>
> Web Answer and the Web Search tools both support retrieval use cases, with different levels of integration complexity. The dividing line is who runs the model:
>
> Web Search: Returns ranked URLs, titles, snippets, and metadata. You keep your own model and control the synthesis. Use Web Search when you want full control over how results are processed.
>
> Web Answer: Runs the model, the agentic retrieval loop, synthesis, and attribution for you. You get a finished, cited answer. Use Web Answer when the question is a sub-task inside a larger agent and you do not want to own a retrieval pipeline for it.
>
> Many customers will use both. An agent might use Web Search for broad research tasks where it needs raw results, and Web Answer for specific factual questions where it needs a quick, cited answer.
>
> Set up and invoke Web Answer
>
> Web Answer is a connector that AWS owns. You reference it by ID, and the Gateway handles the tool schema, parameter governance, endpoint resolution, and authentication to the backend. In this walkthrough, you give your Gateway’s service role permission to call Web Answer, add a Web Answer target, and call it from a Strands agent.
>
> Getting started
>
> Getting started takes minutes. A Gateway administrator adds Web Answer as a target on an existing AgentCore Gateway, and the tool appears to any attached agent over MCP through tools/list and tools/call.
>
> Prerequisites
>
> An AWS account with AgentCore Gateway access.
>
> An AgentCore Gateway in us-east-1 that uses IAM (AWS_IAM) inbound authentication. To create one, see Create an Amazon Bedrock AgentCore Gateway in the Developer Guide.
>
> AWS credentials for an identity that has bedrock-agentcore:InvokeGateway on the Gateway, and Amazon Bedrock access to the model your agent uses.
>
> Python 3.10 or later, with the required packages:
>
> pip install boto3 strands-agents mcp mcp-proxy-for-aws
>
> Note: Following these steps creates AWS resources that incur charges. The Gateway and Web Answer invocations are billable. See the Pricing section that follows for details, and when you finish, delete the resources you created (see “Clean up resources”).
>
> Step 1: Grant the Gateway service role access to Web Answer
>
> The Gateway uses its service role to act on your behalf. The role’s trust policy allows bedrock-agentcore.amazonaws.com to assume it, scoped to your account. For Web Answer, the role needs:
>
> bedrock-agentcore:InvokeWebAnswer, to call Web Answer. The Gateway checks this permission on every request against the ARN that AWS owns, arn:aws:bedrock-agentcore:us-east-1:aws:tool/web-answer.v1.
>
> Attach the policy to the service role as an inline policy:
>
> import json
>
> import boto3
>
> iam = boto3.client("iam")
>
> iam.put_role_policy(
>
> RoleName="&lt;gateway-service-role&gt;",
>
> PolicyName="WebAnswerGuide",
>
> PolicyDocument=json.dumps({
>
> "Version": "2012-10-17",
>
> "Statement": [
>
> {
>
> "Sid": "InvokeWebAnswer",
>
> "Effect": "Allow",
>
> "Action": "bedrock-agentcore:InvokeWebAnswer",
>
> "Resource": "arn:aws:bedrock-agentcore:us-east-1:aws:tool/web-answer.v1",
>
> }
>
> ],
>
> }),
>
> )
>
> The role controls only the Gateway’s outbound calls. Who can call your Gateway is set by its inbound authorizer. The role also doesn’t need bedrock:InvokeModel: your agent’s model runs under your agent’s own identity.
>
> Step 2: Create the Web Answer target
>
> Add Web Answer as a connector target. The connectorId tells the Gateway which managed integration to provision: in this case, an agent that searches the web and writes a cited answer.
>
> import boto3
>
> gateway_client = boto3.client("bedrock-agentcore-control", region_name="us-east-1")
>
> target_response = gateway_client.create_gateway_target(
>
> name="web-answer-tool",
>
> gatewayIdentifier=gateway_id,
>
> targetConfiguration={
>
> "mcp": {
>
> "connector": {
>
> "source": {"connectorId": "web-answer"},
>
> "configurations": [{"name": "WebAnswer", "parameterValues": {&#125;&#125;],
>
> }
>
> }
>
> },
>
> credentialProviderConfigurations=[
>
> {"credentialProviderType": "GATEWAY_IAM_ROLE"}
>
> ],
>
> )
>
> target_id = target_response["targetId"]
>
> Outbound authentication is automatic for connectors. With GATEWAY_IAM_ROLE, the Gateway calls the Web Answer backend with the service role from Step 1, so you don’t create or store any credentials for the tool. Wait until get_gateway_target reports the target status as READY before you call it.
>
> As the Gateway administrator, you can also set a domain filter on the target. The filter applies to every call that goes through the target. To limit the target to a set of domains, set parameterValues to {"domainFilter": {"include": ["bis.org"], "exclude": ["unreliable-source.net"]&#125;&#125;.
>
> Step 3: Invoke Web Answer from a Strands agent
>
> Your agent discovers Web Answer through the Gateway’s tools/list and calls it with tools/call, like any other MCP tool. This works with Strands Agents, LangChain, LangGraph, CrewAI, or any other MCP-compatible client.
>
> from strands import Agent
>
> from strands.models.bedrock import BedrockModel
>
> from strands.tools.mcp import MCPClient
>
> from mcp_proxy_for_aws.client import aws_iam_streamablehttp_client
>
> gateway_url = "https://gateway-&lt;id&gt;.gateway.bedrock-agentcore.us-east-1.amazonaws.com/mcp"
>
> mcp_client = MCPClient(lambda: aws_iam_streamablehttp_client(
>
> endpoint=gateway_url,
>
> aws_region="us-east-1",
>
> aws_service="bedrock-agentcore",
>
> aws_profile="&lt;aws-profile-id&gt;", # identity with bedrock-agentcore:InvokeGateway on the Gateway
>
> ))
>
> model = BedrockModel(model_id="us.anthropic.claude-sonnet-5", max_tokens=1024)
>
> with mcp_client:
>
> tools = mcp_client.list_tools_sync() # Web Answer tool discovered from the Gateway
>
> agent = Agent(model=model, tools=tools)
>
> result = agent("What are the Basel III minimum requirements for Tier 1 capital?")
>
> print(result.message)
>
> When a question needs current information, your agent calls the Web Answer tool (web-answer-tool___WebAnswer). Web Answer runs the agentic search and returns a finished answer with citations.
>
> Besides the question, the Web Answer tool takes optional arguments that your agent can set on each call: a domain filter to include or exclude sites, a published-date range, and a country to localize results. The agent’s domain filter is combined with the target’s filter. The agent can exclude more domains, or limit results to some of the target’s included domains, but it can’t add a domain that the target’s filter blocks.
>
> Response format
>
> Web Answer returns an MCP tool result with both content and structuredContent fields. The answer is markdown text with inline citation markers like [1], and structuredContent.answer carries the same text alongside a structured citations list:
>
> {
>
> "content": [
>
> {
>
> "type": "text",
>
> "text": "Under Basel III, banks must hold Common Equity Tier 1 capital of at least 4.5% of risk-weighted assets [[1](https://www.bis.org/...)]..."
>
> }
>
> ],
>
> "structuredContent": {
>
> "answer": [
>
> {
>
> "text": "Under Basel III, banks must hold Common Equity Tier 1 capital of at least 4.5% of risk-weighted assets [[1](https://www.bis.org/...)]...",
>
> "citations": [
>
> { "domain": "bis.org", "url": "https://www.bis.org/..." }
>
> ]
>
> }
>
> ]
>
> },
>
> "isError": false,
>
> "_meta": {
>
> "latencyMs": 5210
>
> }
>
> }
>
> structuredContent.answer normally holds a single block. Each citation carries the source url and, when available, the domain.
>
> Clean up resources
>
> Delete the Web Answer target when you no longer need it:
>
> gateway_client.delete_gateway_target(gatewayIdentifier=gateway_id, targetId=target_id)
>
> If you created the Gateway only for this walkthrough, delete its targets first, then the Gateway (delete_gateway), and then the service role and its policy. There is no persistent infrastructure on the AWS side beyond these resources. After they are removed, you stop incurring charges.
>
> Enterprise controls, built in
>
> Web Answer inherits the same enterprise controls as other AgentCore tools:
>
> Gateway authentication. No separate API key to provision, rotate, or manage for Web Answer. Callers authenticate to the gateway with the inbound method you configure, such as AWS IAM (SigV4) or a JSON Web Token from your identity provider. The gateway then calls Web Answer with its own service role, which needs the bedrock-agentcore:InvokeWebAnswer permission.
>
> VPC and AWS PrivateLink. Your agents can call the gateway through an interface virtual private cloud (VPC) endpoint (com.amazonaws.us-east-1.bedrock-agentcore.gateway), so traffic stays off the public internet.
>
> Zero data egress. Your queries and results stay within your AWS environment.
>
> Amazon CloudWatch metrics. Operational metrics publish to CloudWatch from the first call.
>
> Per-account rate limits. Enforced from launch, with 10 transactions per second per account in US East (N. Virginia) (us-east-1). To request an increase, contact AWS Support.
>
> Admin-time policy bounds. The Gateway administrator sets domain filter bounds at target setup. Agents can narrow the filter bounds on each call but can’t widen them.
>
> Queries stay within AWS. Web Answer searches an Amazon-operated web index and Amazon’s knowledge graph, and doesn’t send your question to third-party search engines or external websites.
>
> Use cases
>
> Web Answer helps agents retrieve current, cited information to support a range of knowledge-intensive workflows. Example scenarios include:
>
> Financial services. Regulatory Q&amp;A agents answering questions about compliance requirements, market regulations, and policy changes, where every answer must trace to an authoritative source.
>
> Healthcare. Clinical support agents grounding responses in current medical literature and treatment guidelines published on the web.
>
> Customer service. Support agents answering product and policy questions in real time, where ten ranked links are not useful and a cited answer is.
>
> Legal and compliance. Research assistants answering questions about case law, regulatory filings, and policy interpretations with auditable citations.
>
> Enterprise knowledge workers. Internal copilots that answer questions from current public information without requiring employees to build their own search and synthesis workflow.
>
> Availability
>
> Web Answer is available in US East (N. Virginia) (us-east-1), with more AWS Regions coming soon.
>
> Pricing
>
> Web Answer on Amazon Bedrock AgentCore is priced at $10 per 1,000 tool calls.
>
> Conclusion
>
> In this post, we showed how Web Answer gives your agents current, cited answers through agentic search, with no search pipeline for you to build or maintain. We granted a Gateway service role access to Web Answer, added a Web Answer target, called it from a Strands agent, and read the answer and its citations from the response. Use Web Search on AgentCore when your own model should reason over raw results, and Web Answer when your agent needs a finished, cited answer.
>
> To get started, see:
>
> Web Answer on Amazon Bedrock AgentCore documentation
>
> Web Answer structured output schema
>
> Adding Web Answer to an Amazon Bedrock AgentCore Gateway
>
> Supported regions
>
> About the authors
>
> Adrianna Chudy
>
> Adrianna is a Senior Software Development Engineer at Amazon AGI, where she develops Web Answer on Amazon Bedrock AgentCore. She works on web search and agentic question answering for foundation models and AI agents, helping them give accurate, cited answers based on current information. Since she joined Amazon in 2020, she has built large-scale knowledge systems, first for Alexa and now for AWS.
>
> Gaurav Deshmukh
>
> Gaurav is a Senior Software Development Engineer at Amazon AGI with nine years of experience at Amazon building large-scale distributed systems. He works on the information retrieval, grounding, and agentic AI services that power foundation models and AI agents, including capabilities available through Amazon Bedrock AgentCore. His work helps AI agents access accurate, real-time information and perform complex research tasks, improving the reliability of agentic applications at scale.
>
> Kalyan Garimella
>
> Kalyan is a Principal Product Manager at Amazon AGI, where he leads the development and launch of web search capabilities for Amazon Bedrock AgentCore. His work focuses on solving a core limitation of modern AI agents; their inability to access real-time, factual information; by enabling agents to ground their reasoning in live web data. Kalyan lives in the Bay Area with his family.
>
> Kamrul Tarafder
>
> Kamrul is a Solutions Architect on the Product Marketing Demo Engineering team at AWS, specializing in AI/ML with Amazon Bedrock and Amazon Bedrock AgentCore. He combines interactive demos with technical storytelling to make complex technologies more accessible. Outside of work, he enjoys hiking in the Pacific Northwest, reading, and attending electronic music shows.
>
> Omar Abdelwahab
>
> Omar is a Technical Product Marketing Manager at Amazon Web Services (AWS), where he focuses on AI products including Agentic AI and Web Search. He holds a Ph.D. in Computer Science and enjoys working at the intersection of AI, technology, and go-to-market strategy to help customers build innovative applications.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。