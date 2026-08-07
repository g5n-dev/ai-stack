---
title: "Run production AI agents in n8n with Amazon Bedrock AgentCore harness"
date: 2026-08-06T11:37:46+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "Prompt 工程", "Advanced (300)", "Amazon Bedrock", "Amazon Bedrock AgentCore", "Technical How-to", "博客与播客"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:f173904c2aa554a29660ca6e241991f91c09150d2d384f82cd9a6173f849ad47"
source_payload_sha256: "sha256:cd4fc70738b6782a0b53bd56c5dfdc45be94bc72bf6409adc3543b8bfd4e95d8"
observation_id: obs_4a6b874ba5509dc494df62125cb5063d7247b899afb73b3adaa49b716ce55fe7
event_id: evt_64a2465a33d99e01f1f2ed638301debd0fbb7cbe6ea3390b8cc7cbccbac71888
revision_id: rev_5d74b82b42b9682906223d69656e835e8fb43014bd71536ba6d43d53f30aab39
source_published_at: 2026-08-05T18:00:57Z
first_seen_at: 2026-08-06T03:46:00Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 69
interpretation_sha256: "sha256:f07fe79e8f701f07995e0e1f55cca057a796c9162b528f137b54e47fe57e2c20"
description: "该内容介绍如何通过 n8n 的社区节点 ，在可视化编辑器里直接使用 Amazon Bedrock AgentCore harness，快速为工作流添加具备持久记忆、工具调用和模型自由切换的 AI Agent。"
external_url: https://aws.amazon.com/blogs/machine-learning/run-production-ai-agents-in-n8n-with-amazon-bedrock-agentcore-harness
parent_observation_id: null
last_seen_at: 2026-08-07T00:00:00Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/run-production-ai-agents-in-n8n-with-amazon-bedrock-agentcore-harness](https://aws.amazon.com/blogs/machine-learning/run-production-ai-agents-in-n8n-with-amazon-bedrock-agentcore-harness)
- **发布域名**: aws.amazon.com

## 要点解读

### 这是什么  
该内容介绍如何通过 n8n 的社区节点 `@aws/n8n-nodes-agentcore`，在可视化编辑器里直接使用 Amazon Bedrock AgentCore harness，快速为工作流添加具备持久记忆、工具调用和模型自由切换的 AI Agent。

### 用在哪里  
适用于已经在 n8n 中搭建自动化流程、希望把单步模型调用扩展为多轮交互和工具使用的团队；也适合想用低代码方式在 AWS 环境托管 AI Agent、避免自行编写编排层的技术人员。

### 可以推断的  
推测：该节点让 n8n 用户无需自行实现状态管理、上下文窗口和会话隔离等复杂底层逻辑，即可获得生产级 Agent，提升了 AI 自动化的落地效率。  
推测：因为支持在同一对话中切换模型供应商，团队在对比不同模型表现或在不同业务场景下更换模型时，无需重新设计工作流。

## 来源摘要/节选

> If you build and automate workflows in n8n without writing much code, you’ve probably used its AI Agent node to add a model call to a workflow. It’s a great start. But a production agent needs more than a single model call: memory that lasts beyond one run, tools it can actually use like a browser or a code sandbox, and room to work through longer tasks. Building that scaffolding yourself is the hard part.
>
> Amazon Bedrock AgentCore is a platform to build, connect, and optimize agents at scale, with any framework or model. AgentCore harness, a capability of Amazon Bedrock AgentCore, is now generally available and provides that scaffolding for you. A new open-source community node brings it into n8n’s visual editor. You get production agents with persistent memory, real tools, and the model provider of your choice, without writing infrastructure or agent code. You’re not tied to one model either. The node works with Amazon Bedrock, OpenAI, Google Gemini, and LiteLLM-supported providers, and you can switch providers between turns of the same conversation.
>
> In this post, you will install the node, @aws/n8n-nodes-agentcore, and build agents step by step in the n8n editor. You will start with an agent that remembers a conversation, scope memory to individual users, add a code interpreter tool, give the agent skills, and finish by running an agent privately in your own virtual private cloud (VPC). The node is open source under the MIT license, and AgentCore harness is powered by Strands Agents, the open source agent framework from AWS.
>
> What the node does
>
> An agent is more than a model. The model reasons, but the harness does the work around it: it runs the orchestration loop, calls tools, manages the context window, keeps state across turns, recovers from failures, and isolates each session. Building that layer is where most teams spend their time.
>
> AgentCore harness gives you that layer as a managed capability. You define an agent in configuration, including the model it uses, the tools it calls, the skills it has access to, and the instructions it follows, and AgentCore assembles and runs the loop for you. Each session runs in its own isolated environment with a filesystem and shell, memory across sessions, and web browsing. When configuration isn’t enough, you can export the harness to Strands code and keep running on the same system.
>
> n8n’s built-in AI Agent node is a good fit for a single model call in a workflow. The community node goes further by exposing the full harness in the n8n editor. It has one operation with a single deciding field, Harness ARN:
>
> Leave it blank and the node creates an agent for you on the first run, reuses it on later runs, and updates it when your configuration changes.
>
> Paste an existing harness ARN and the node invokes that agent directly, so you can use agents you created outside n8n.
>
> The node uses the same AWS credential pattern as the existing n8n AWS Lambda and Amazon Simple Storage Service (Amazon S3) nodes, so it feels familiar if you already automate AWS services in n8n.
>
> Prerequisites
>
> Before you begin, make sure you have the following:
>
> An n8n instance. You can run n8n either as a self-hosted install or on n8n Cloud. Both work with this node. If you’re new to n8n, see the n8n deployment documentation to choose an option and set up your instance, then complete the initial sign-in so you land in the editor where you will build the workflows in this post.
>
> The node installed. @aws/n8n-nodes-agentcore is a verified community node, so you can find it directly in the n8n nodes panel. In the editor, add a node, search for Amazon Bedrock AgentCore, and select it — n8n installs it for you. (You can also install it from Settings, Community Nodes, Install by entering @aws/n8n-nodes-agentcore.) This post uses node version 0.3.
>
> An AWS account with access to AgentCore harness in a supported AWS Region.
>
> AWS credentials for the caller (the identity whose keys go in the n8n credential) with the harness caller permissions, plus a separate AWS Identity and Access Management (IAM) execution role that the harness assumes at runtime. AWS maintains the least-privilege reference policies in AgentCore harness security documentation and the node README maps each feature to the permissions to add.
>
> Important: Where you can, use temporary credentials from AWS IAM Identity Center or AWS Security Token Service (AWS STS), and follow the principle of least privilege when you configure IAM permissions. Don’t commit credentials to source control.
>
> Note on cost: The AgentCore harness, the managed memory store it provisions, and (if you use it) VPC endpoints are billed AWS resources. Follow the Clean up section at the end to remove what you create for this walkthrough, and refer to the AgentCore documentation for pricing.
>
> Set up the credential
>
> You configure the AWS credential once, the same way you would for other AWS nodes in n8n.
>
> In n8n, go to Credentials and choose New.
>
> Search for and select Amazon Bedrock AgentCore API.
>
> Enter your Access Key ID and Secret Access Key, and a Session Token if you use temporary credentials.
>
> Select your Region and enter the Execution Role ARN that the harness assumes at runtime.
>
> Choose Test to confirm the connection, then choose Save.
>
> Amazon Bedrock AgentCore API credential in n8n, showing the access key, Region, and execution role ARN, with a successful connection test
>
> Build your first agent and give it memory
>
> In this walkthrough, you build an agent that remembers details across turns of a conversation. Memory is on by default, so the node provisions a managed memory store for you and there’s nothing extra to configure.
>
> Add a manual trigger to a new workflow, add the Amazon Bedrock AgentCore node after it and attach your credential.
>
> Leave Harness ARN blank so the node creates and reuses the agent.
>
> Enter an Agent Name, such as travel_concierge.
>
> Set Model Provider to Amazon Bedrock and enter a Model ID, such as a Claude model.
>
> Enter a System Prompt, such as You are a warm, concise travel concierge, and a Session ID, such as demo-travel-session. Reusing this session ID is what continues the conversation on later runs.
>
> Enter a Prompt for the first turn, such as “I love warm beaches and I’m vegetarian. Note that for me.”, and run the node.
>
> The first run takes about 30-60 seconds while AWS provisions the agent. The output includes the agent’s response, token usage, and a summary of what the node provisioned, including the memory store it created for you.
>
> Turn 1. The node output shows the agent’s response and a harness summary that confirms managed memory with a provisioned memory ARN.
>
> Now change only the Prompt to Suggest one destination and one dish I’d enjoy, based on what you know about me, keep the same session ID, and run again.
>
> Turn 2. The agent recalls the preferences from turn 1, warm beaches and vegetarian, because the conversation persisted through the same session ID.
>
> The output field sessionSource reads provided when you supply a session ID, and the input token count rises on turn 2 because the node loads the prior conversation before the agent reasons. If you leave the session ID blank, each run starts a new conversation.
>
> Scope memory per user with an actor ID
>
> When one agent serves many people, you can keep each person’s memory separate with an Actor ID. Memory is scoped by actor and session, so different actors get isolated histories from the same agent.
>
> The scoping is a hierarchy: the agent holds the shared configuration, the Actor ID isolates one user’s memory from another’s, and the Session ID isolates individual conversations within an actor. One actor can have many sessions. A different actor with the same session ID still gets its own separate memory.
>
> Use an agent such as team_assistant with managed memory.
>
> Under Additional Options, set Actor ID to a per-user value, such as user-alice, and set a Session ID for that user.
>
> Run a first turn, such as Remember my project is codenamed Aurora.
>
> Change the prompt to What’s my project codename? and run again with the same actor and session.
>
> The node configured with an actor ID and session ID for a specific user.
>
> Turn 1 for the actor user-alice, which stores a preference.
>
> Turn 2 for the same actor. The agent returns the value it stored for this user. A different actor ID keeps its own separate memory.
>
> Add a tool: run code in a sandbox
>
> Agents become far more capable when they can use tools. In this walkthrough, you give the agent a code interpreter that runs code in a sandboxed environment.
>
> Use an agent such as data_analyst with a Claude model.
>
> In the System Prompt, instruct the agent to write and run code to answer, then report the result.
>
> Turn on Add Tools, then under Tools, choose Add Tool and set Type to AgentCore Code Interpreter, a capability of Amazon Bedrock AgentCore.
>
> Enter a Prompt that requires computation, such as “Generate 500 random exam scores between 0 and 100, then report the mean, median, and standard deviation.”, and run the node.
>
> The agent writes and runs code in the sandbox and returns computed results for the mean, median, and standard deviation, rather than estimating them. The harness summary shows one tool configured.
>
> You add other tools the same way, including a cloud browser, AgentCore Gateway (a capability of Amazon Bedrock AgentCore), and remote Model Context Protocol (MCP) servers.
>
> Give the agent skills
>
> Skills are bundles of instructions and scripts that give an agent domain knowledge on demand. You load them from the AWS curated catalog, a Git repository, Amazon S3, or a filesystem path, and the harness loads them only when the task calls for them.
>
> Use an agent such as aws_architect with a Claude model.
>
> Turn on Add Skills, then under Skills, choose Add Skill and set the Source. For the curated catalog, choose AWS Skills and enter a glob pattern such as core-skills/*. You can add more skills, for example a Git source that points to a public repository.
>
> Enter a Prompt that benefits from the skill, such as “Outline a serverless image-upload pipeline on AWS”, and run the node.
>
> The agent applies the loaded skills to produce guidance, and the harness summary shows the number of skills configured.
>
> Run in your VPC
>
> For agents that need private network access, you can run the harness in your VPC. You set the network configuration on the credential, so every agent that credential provisions runs privately.
>
> Edit your Amazon Bedrock AgentCore API credential.
>
> Set Network Mode to VPC.
>
> Enter your VPC Subnet IDs and VPC Security Group IDs, then save.
>
> The credential configured for VPC mode with subnet and security group IDs.
>
> Your subnets don’t need internet access. The harness pulls its managed container image from a private Amazon ECR repository in the same Region, so you need VPC endpoints for Amazon ECR and Amazon S3 rather than a NAT gateway. Refer to the AgentCore harness network configuration documentation for the required endpoints and the execution role permissions. Refer to the AgentCore harness security documentation for the required endpoints and the execution role permissions.
>
> In a workflow, use an agent such as private_vpc_agent with the VPC-enabled credential.
>
> Enter a Prompt and run the node.
>
> The node output for a VPC agent. The harness summary shows the network mode is VPC.
>
> Clean up
>
> Each agent you create is a harness resource in your AWS account, and it can provision a managed memory store. To avoid ongoing charges, delete the agents you no longer need.
>
> List your harnesses with the AWS Command Line Interface (AWS CLI) or the Amazon Bedrock AgentCore console.
>
> aws bedrock-agentcore-control list-harnesses --region us-west-2
>
> Delete the ones you created for this post. For pricing details, refer to the AgentCore documentation.
>
> aws bedrock-agentcore-control delete-harness --harness-id &lt;harness-id&gt; --region us-west-2
>
> If you enabled a VPC, you might also want to remove any interface VPC endpoints you created for this walkthrough, because interface endpoints incur charges while they exist.
>
> Where to go next
>
> This post walked through memory, per-user scoping, a code interpreter tool, skills, and VPC networking. The node already supports more of the Amazon Bedrock AgentCore harness feature set. Here’s what to try next, each configured the same way you configured the features above:
>
> Your choice of model provider, switchable mid-session. Use OpenAI, Google Gemini, or LiteLLM-supported providers alongside Amazon Bedrock. Set the provider and model on the node, and switch between turns of the same session without losing context. Non-Bedrock providers use an API key stored in AgentCore Identity (a capability of Amazon Bedrock AgentCore).
>
> More tools. Add a cloud browser, AgentCore Gateway with optional OAuth outbound authentication, and remote MCP servers alongside the code interpreter.
>
> Inline functions. Let the agent call back into your n8n workflow for a human-in-the-loop step, then return the result to the agent.
>
> Custom containers. Bring your own Linux/arm64 container image so the agent runs with your own dependencies.
>
> Filesystem mounts. Use managed session storage, or mount Amazon Elastic File System (Amazon EFS) or Amazon S3 for data that outlives a session.
>
> OAuth-authenticated invocation. Invoke agents protected by an inbound JSON Web Token (JWT) authorizer with a token from your identity provider, set on the AgentCore credential.
>
> Versions and endpoints. Every configuration change becomes an immutable version, and named endpoints let you pin staging and production to specific versions.
>
> The examples folder in the GitHub repository includes importable workflows for many of these. For end-to-end use cases, the examples/templates folder has fuller workflows that show the agent working alongside other n8n nodes in complete, importable automations.
>
> Conclusion
>
> In this post, you installed the open-source AgentCore harness community node for n8n and built agents that remember conversations, keep per-user memory separate, run code in a sandbox, use skills, and run privately in a VPC, all from the n8n editor and with no infrastructure or agent code. Because the node works with Amazon Bedrock, OpenAI, Gemini, and LiteLLM providers, you choose the model that fits each task.
>
> To get started, add the Amazon Bedrock AgentCore node from the n8n nodes panel (or install @aws/n8n-nodes-agentcore from Settings &gt; Community Nodes), import an example workflow, and build your first agent. The node is open source under MIT and built on the open source Strands Agents framework, and contributions and feedback are welcome on the GitHub repository. To learn more about the underlying capability, refer to the AgentCore documentation.
>
> n8n is a trademark of n8n GmbH. All other trademarks are the property of their respective owners.
>
> About the author
>
> Sundar Raghavan
>
> Sundar is a Senior Solutions Architect at AWS on the Agentic AI Foundations team. He leads the developer experience for Amazon Bedrock AgentCore, owning the SDK and CLI, and drives the framework and ecosystem integrations strategy. He focuses on how developers build, deploy, and scale production AI agents on AWS. He is currently extending that focus into physical AI, collaborating on Strands Robots to bring the same agent developer experience to robotics.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。