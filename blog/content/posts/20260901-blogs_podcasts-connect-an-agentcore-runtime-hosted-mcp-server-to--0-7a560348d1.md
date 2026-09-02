---
title: "Connect an AgentCore Runtime hosted MCP server to Amazon Quick"
date: 2026-09-01T07:53:41+08:00
draft: false
entry_kind: "auto"
tags: ["AI Agent", "生成式 AI", "深度学习", "Amazon Bedrock AgentCore", "Amazon Quick Suite", "Foundational (100)", "Technical How-to", "博客与播客"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:d84e6b36b92d3660eedd37d7465c96ac53efcf0c3a9e8d24c03475619328ae0d"
source_payload_sha256: "sha256:17b1e6b8cdeb70a7a42df930a26ad6ba7db7fcfeda209024e8208f1883aed9b6"
observation_id: obs_7a560348d1cc3306ab45f5620282443bd54c754ff4a7a0e2fd5107234dd30de4
event_id: evt_45ce7b550ab2fa6c0c17bfb0148ffd53ba5470640983ace2c8af43cb65655642
revision_id: rev_3ffdea660c5584f48835f1da97a20930d8afd630e2120ea6666d5f8e14dd1bb9
source_published_at: 2026-08-31T22:47:53Z
first_seen_at: 2026-09-01T00:03:42Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 62
interpretation_sha256: "sha256:d5a5782530a0f43ab1485c8c2853d0baf4a9f4feeed9941a5368ab6941d81510"
description: "这是一篇关于将托管在 AgentCore Runtime 上的 MCP 服务器与 Amazon Quick 进行集成的操作指南，旨在帮助用户在 Amazon Quick 的聊天代理中复用已有的 AI 工具，避免重复开发。"
external_url: https://aws.amazon.com/blogs/machine-learning/connect-an-agentcore-runtime-hosted-mcp-server-to-amazon-quick
parent_observation_id: null
last_seen_at: 2026-09-02T00:00:00Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/connect-an-agentcore-runtime-hosted-mcp-server-to-amazon-quick](https://aws.amazon.com/blogs/machine-learning/connect-an-agentcore-runtime-hosted-mcp-server-to-amazon-quick)
- **发布域名**: aws.amazon.com

## 要点解读

### 这是什么
这是一篇关于将托管在 AgentCore Runtime 上的 MCP 服务器与 Amazon Quick 进行集成的操作指南，旨在帮助用户在 Amazon Quick 的聊天代理中复用已有的 AI 工具，避免重复开发。

### 用在哪里
当需要在 Amazon Quick 中扩展聊天代理的功能，例如让代理访问文件、数据库或 API 等外部资源时，可以参考此指南进行部署和集成。该指南面向具备 AWS 基础知识的开发者。

### 可以推断的
推测：对于已经拥有 MCP 服务器的用户，此集成方案可以降低接入成本，因为不需要为每个用例单独构建连接器。  
推测：集成过程中涉及的认证机制基于行业通用的 OAuth 2.0 协议，这意味着方案在安全性和兼容性方面遵循了现有标准。

## 来源摘要/节选

> Model Context Protocol (MCP) servers allow foundation models to access external data and tools, supporting standardized, secure access to files, databases, and APIs. They give AI agents the ability to interact with real-world applications, reduce hallucinations with accurate context, and offer stateful, multi-turn capabilities. Industry-standard architectures quickly evolved and adopted MCP to power agentic AI workflows.
>
> Amazon Quick supports MCP integrations for autonomous execution, real-time data access, and specialized AI sub-agent integrations. If you already have an MCP server, you can use this integration guide to integrate it with Amazon Quick. If you do not have an MCP server yet, you can use the AWS provided guidance for deploying MCP servers on AWS, which follows AWS Well-Architected pillars. Depending on your use case, you have several options:
>
> If you have your own REST API or one running on Amazon API Gateway, you can integrate Amazon Quick directly with your API using Amazon Bedrock AgentCore Gateway.
>
> If you prefer a serverless architecture and need only the bare minimum execution capability for your AI agent, you can author an AWS Lambda function and integrate with Amazon Quick using AgentCore Gateway.
>
> If you want a fully managed serverless MCP server solution with session isolation, extended execution time, persistent file systems, built-in authentication, observability, enhanced payload, bidirectional streaming, and evaluations, you can use AgentCore Runtime for MCP server hosting and connect with Amazon Quick using AgentCore Gateway.
>
> In this post, you will learn how to deploy and host your MCP server in AgentCore Runtime and integrate it with Amazon Quick, along with the prerequisites. With this pattern, you promote reusability and avoid duplication of AI tools, so clients can reuse commonly used tools and agents exposed through an MCP server instead of authoring them from scratch again. Your customers get a way to use your product inside Amazon Quick (chat agents and workflows) without building custom connectors for every use case.
>
> Solution overview
>
> As of this writing, you can use Amazon Quick in a web browser or the desktop app to work with a chat agent or Flows that provide AI agent capabilities. To connect the AI agent with the MCP server for access to additional tools and sub-agent capabilities, you need to integrate the MCP server with Amazon Quick. The integration is handled through connectors on the Amazon Quick end and AgentCore Gateway on the AgentCore end. AgentCore Gateway and Runtime are available in Amazon Bedrock AgentCore, a fully managed service for building generative AI applications. The authorization flow from Amazon Quick to AgentCore Gateway is referred to as Inbound Auth, and the flow from AgentCore Gateway to AgentCore Runtime is referred to as Outbound Auth. Inbound Auth handles authentication and authorizes the user to access the MCP server. For Inbound Auth, we use Amazon Cognito for authorization needs, but you can use another identity provider. Outbound Auth handles machine-to-machine authentication and authorization, and we use AgentCore Identity, a comprehensive identity and access management service purpose-built for AI agents. The MCP protocol currently requires OAuth 2.0 as the authentication protocol, so Outbound Auth uses OAuth 2.0.
>
> Prerequisites
>
> Before you begin, verify that you meet the following prerequisites to deploy the solution in your own AWS account using the step-by-step instructions in this post.
>
> An AWS account.
>
> Amazon Quick set up with an Author or higher subscription.
>
> Permission to create AWS Identity and Access Management (IAM) roles and policies, and AWS resources for AgentCore, Amazon Cognito, and Amazon CloudWatch.
>
> Basic knowledge of AWS services.
>
> For the Amazon Bedrock AgentCore setup:
>
> Access to a command-line environment with the AWS SDK and Python installed.
>
> Knowledge of the AWS CLI and Python.
>
> Amazon Bedrock with access enabled for Anthropic models.
>
> To run this tutorial:
>
> Python 3.10+.
>
> AWS credentials configured.
>
> Amazon Bedrock AgentCore SDK.
>
> MCP (Model Context Protocol) library.
>
> Running Docker daemon.
>
> Implementation steps
>
> Follow these steps to go from a locally authored MCP server to a fully integrated, authenticated tool available inside your Amazon Quick chat agent.
>
> Implement and deploy a sample remote MCP server on AgentCore Runtime.
>
> Integrate the MCP server with AgentCore Gateway with inbound and outbound auth.
>
> Register the MCP integration in Amazon Quick and integrate with your chat agent.
>
> Test the MCP server integration within Amazon Quick.
>
> Clean up resources.
>
> Step 1: Implement and deploy a remote MCP server on AgentCore Runtime
>
> In this step, we deploy a sample MCP server on AgentCore Runtime with basic dummy tools. The detailed step-by-step code is available in the AgentCore samples notebook on GitHub, and we cover it at a high level.
>
> Create the project structure and files as follows:
>
> Project structure
>
> mcp_server_project/
>
> ├── mcp_server.py # Main MCP server code
>
> ├── requirements.txt # Dependencies
>
> └── __init__.py # Python package marker
>
> File: requirements.txt
>
> mcp&gt;=1.10.0
>
> boto3
>
> bedrock-agentcore
>
> bedrock-agentcore-starter-toolkit&gt;=0.1.21
>
> strands-agents
>
> Install the requirements in your Python interpreter using the following command:
>
> uv venv sample-venv # Create Virtual Environment
>
> source sample-venv/bin/activate # Activate Virtual Environment
>
> uv pip install -r requirements.txt # Install the dependencies
>
> The following is a sample bare-minimum code. For more details on secure auth setup, see Building a secure auth code flow setup using AgentCore Gateway with MCP clients. When you configure an AgentCore Runtime with the MCP protocol, the service expects MCP server containers to be available at the path 0.0.0.0:8000/mcp, which is the default path supported by most official MCP server SDKs.
>
> File: sample_mcp_server.py
>
> from mcp.server.fastmcp import FastMCP
>
> mcp = FastMCP(host="0.0.0.0", stateless_http=True)
>
> @mcp.tool()
>
> def getOrder() -&gt; int:
>
> """Get an order"""
>
> return 123
>
> @mcp.tool()
>
> def updateOrder(orderId: int) -&gt; int:
>
> """Update existing order"""
>
> return 456
>
> if __name__ == "__main__":
>
> mcp.run(transport="streamable-http")
>
> The server uses FastMCP with stateless_http=True, which is required for AgentCore Runtime compatibility. This code does the following:
>
> FastMCP: Creates an MCP server that can host your tools.
>
> @mcp.tool(): Decorator that turns your Python functions into MCP tools.
>
> stateless_http=True: Required for AgentCore Runtime compatibility.
>
> You can test your MCP server locally using a local MCP server client by following the Creating Local Testing Client and Testing Locally sections in the notebook.
>
> Now, you are ready to deploy to AgentCore Runtime. You can deploy using the Bedrock starter kit from the terminal (described in the following steps) or through a Python script, as listed in the Launching MCP Server to AgentCore Runtime section in the notebook. We use the AgentCore starter kit in this tutorial.
>
> Open your terminal with the current working directory set to your project directory, and configure your project for deployment. The configure command is interactive with self-explanatory steps. You can pick the defaults for this tutorial.
>
> # Configure your AgentCore project
>
> agentcore configure --entrypoint mcp_server.py --name simple_mcp_server
>
> The configure command performs several key setup tasks automatically. It generates a Dockerfile and .dockerignore file for containerizing your agent so that your Python application runs consistently across different environments. Most importantly, it creates a .bedrock_agentcore.yaml configuration file that stores your agent’s runtime settings and deployment parameters.
>
> The --entrypoint parameter specifies the Python file that contains your agent’s main logic. This is the file with your @app.entrypoint decorated function. The --name parameter assigns a unique identifier to your agent within your AWS account, which is used for resource naming and management across AWS services.
>
> After you configure the project, you can initiate the deployment by running the following command.
>
> agentcore launch
>
> You should be able to see the MCP server in Runtime now.
>
> Step 2: Integrate the MCP server with AgentCore Gateway with inbound and outbound auth
>
> In this step, we configure AgentCore Gateway to act as the secure bridge between Amazon Quick and your deployed MCP server. The inbound and outbound flows are set up with recommended security best practices, including end-to-end TLS that is available out of the box. You can refer to the respective service documentation for customizations. This involves setting up an IAM role for the Gateway, configuring two Amazon Cognito user pools to handle Inbound Auth (authorizing requests from Amazon Quick) and Outbound Auth (authenticating calls to the MCP server through OAuth 2.0), and creating the Gateway endpoint. For programmatic setup, follow the MCP server as a target tutorial on GitHub.
>
> Step 2a: Create an IAM role for AgentCore Gateway to assume
>
> Go to the AWS Management Console, choose IAM, and then choose Create role. Select Amazon Bedrock AgentCore as the use case.
>
> You can attach the following inline IAM policy in Permissions:
>
> {
>
> "Version": "2012-10-17",
>
> "Statement": [
>
> {
>
> "Sid": "MCPServerRuntimePermissions",
>
> "Effect": "Allow",
>
> "Action": [
>
> "bedrock-agentcore:InvokeAgentRuntime",
>
> "bedrock-agentcore:InvokeRegistryMcp",
>
> "secretsmanager:GetSecretValue"
>
> ],
>
> "Resource": [
>
> "arn:aws:bedrock-agentcore:&lt;REGION&gt;:&lt;ACCOUNT_ID&gt;:runtime/&lt;RUNTIME_ID&gt;",
>
> "arn:aws:bedrock-agentcore:&lt;REGION&gt;:&lt;ACCOUNT_ID&gt;:runtime/&lt;RUNTIME_ID&gt;/runtime-endpoint/*"
>
> }
>
> ]
>
> }
>
> Use the sample role name agentcore-sample-mcpgateway-role (or pick your own). For Resource, populate it with the runtime ARN of the MCP server deployed on AgentCore Runtime.
>
> Step 2b: Create an Amazon Cognito user pool for inbound authorization to the Gateway
>
> Navigate to Amazon Cognito and create a new user pool that serves as the Inbound authorization layer, validating requests from Amazon Quick before they reach the Gateway.
>
> Go to Amazon Cognito and choose Create user pool.
>
> Next, configure the resource server for your user pool. In the navigation pane, choose Domain under Branding, and create a new resource server to define the protected custom scope invoke that the Gateway validates during authorization.
>
> Keep a note of the following Inbound Auth details from the user pool created earlier, because these are referenced in later steps:
>
> Client ID and Client Secret: In the navigation pane, choose App Clients, and then select your app client to view the credentials.
>
> Discovery URL: https://cognito-idp.{REGION}.amazonaws.com/{gw_user_pool_id}/.well-known/openid-configuration
>
> Step 2c: Create an Amazon Cognito user pool for outbound authorization
>
> Navigate to Amazon Cognito and create a second user pool that serves as the Outbound authorization layer, so the Gateway can authenticate itself when making calls to the MCP server hosted on AgentCore Runtime.
>
> Go to Amazon Cognito and choose Create user pool.
>
> Similar to inbound authorization, create a resource server for outbound authorization and get the details for the client ID, secret, and discovery URL with the protected custom scope invoke.
>
> Keep a note of the following information available from the user pool for Outbound Auth that is needed later:
>
> Client ID and Client Secret: In the navigation pane, choose App Clients, and then select your app client to view the credentials.
>
> Discovery URL: https://cognito-idp.{REGION}.amazonaws.com/{gw_user_pool_id}/.well-known/openid-configuration
>
> Next, create an OAuth credential provider in AgentCore Identity. Navigate to Amazon Bedrock AgentCore, choose Identity, and then choose Add Outbound Auth and Create OAuth Client. Populate the form with the Discovery URL, Client ID, and Client Secret from the app client created in the Outbound Auth Amazon Cognito user pool in the previous step.
>
> Step 2d: Create the AgentCore Gateway
>
> Navigate to Amazon Bedrock AgentCore, choose Gateway, and then choose Create Gateway. For this walkthrough, we name it ac-gateway-mcp-server. For Inbound Auth, select JWT as the authentication type, choose Use Existing Identity Provider Configuration, and provide the Discovery URL and Client ID from the Inbound Auth Amazon Cognito user pool created in Step 2b.
>
> In the Permissions section, use the IAM role we created in Step 2a.
>
> Under the Target section, register your MCP server as a target. Verify that you select OAuth Client as the authorization type, because the MCP protocol does not support other authorization methods at this time. To build the MCP endpoint URL, use the following template, replacing encoded_agentcore_runtime_mcp_server_arn with the URL-encoded ARN of your MCP server deployed on AgentCore Runtime.
>
> https://bedrock-agentcore.us-east-1.amazonaws.com/runtimes/{encoded_agentcore_runtime_mcp_server_arn}/invocations?qualifier=DEFAULT
>
> For the Outbound Auth configuration, use the OAuth client that we created in the Outbound Auth section.
>
> After the details are filled in, choose Create Gateway, and wait for both the Gateway and its Target to reach a Ready state before proceeding to the next step.
>
> Step 3: Register MCP integration in Amazon Quick
>
> Navigate to Amazon Quick, choose Connectors, and then choose Create for your team. Select Model Context Protocol (MCP) as the integration type to begin registering your newly created Gateway as an MCP integration.
>
> Provide a name and description for your integration, along with the MCP Server Endpoint, which is the Resource URL of the AgentCore Gateway created in Step 2d. For the connection type, you also have the option to choose private VPC connectivity to restrict the visibility of your MCP server over the network for better security.
>
> On the Authenticate screen, fill in the Inbound Auth details configured on the AgentCore Gateway in Step 2d. You can select the authentication type based on your use case. If your use case is authenticating individual users, select User authentication. If your use case is a more systematic integration, then select Service authentication. For this tutorial, we use User authentication with Amazon Cognito. You can connect your preferred identity provider. Fill in the Client ID, Client Secret, Token URL, and Authorization URL details based on the identity provider selected.
>
> For the Token URL, use the following template. Note that the underscore in the user pool ID must be removed (for example, us-west-2_qNBcTlLbR becomes us-west-2qNBcTlLbR). For the Authorize URL, use the same URL but replace token with authorize.
>
> Token URL template:
>
> https://{user_pool_id_without_underscore}.auth.{REGION}.amazoncognito.com/oauth2/token
>
> After the details are filled in, choose Create and Continue, and review your configuration. The screen shows only listTools for now and syncs the tools with the MCP server. The sync is complete after the Action is in the Available state.
>
> You should see the tools refreshed after the Action is in the Available or Ready state.
>
> Step 4: Test the MCP server integration within Amazon Quick
>
> You can choose Test Action APIs to verify that your MCP tools are accessible and functioning as expected.
>
> After the integration is set up, you can add it as an Action in your chat agent or Flows. The Actions integration allows your Quick agent or workflow to invoke MCP tools. For this tutorial, we create one sample chat agent. You can provide more context to the agent by linking a Space or uploading files, but we skip that for now and focus only on the MCP server integration.
>
> In the Actions section, choose Link Actions and select the Actions integration we created in Step 3.
>
> You can then test the integration with the MCP server within the chat agent and launch the chat agent after validating the results.
>
> Step 5: Clean up
>
> To avoid incurring unnecessary costs, delete the resources created in this walkthrough in the reverse order of creation to make sure that dependencies are cleanly removed before you delete the resources they rely on. You can also refer to the cleanup code in the tutorial notebook on GitHub.
>
> Delete the Amazon Quick chat agent or Flow.
>
> Delete the Amazon Quick Action.
>
> Delete the AgentCore Gateway.
>
> Delete the AgentCore Identity resources.
>
> Delete both the inbound and outbound auth Amazon Cognito user pools.
>
> Delete the AgentCore Runtime.
>
> Delete the AgentCore Gateway IAM role.
>
> Conclusion
>
> In this post, you learned how Amazon Quick integrates with custom MCP servers hosted on Amazon Bedrock AgentCore Runtime. You walked through deploying a remote MCP server on AgentCore Runtime, securing it with inbound and outbound authentication using Amazon Cognito and AgentCore Identity, bridging it to Amazon Quick through AgentCore Gateway, and registering it as an Action integration in Amazon Quick. This pattern promotes reusability of AI tools and agents across your organization, so teams can expose specialized capabilities through a standardized MCP interface and consume them directly within Amazon Quick chat agents and Flows, without building custom connectors for every use case.
>
> For more information about Amazon Quick and how you can get started, see the blog post Announcing Amazon Quick: your agentic teammate for answering questions and taking action. For more information about Amazon Bedrock AgentCore, see the blog post Introducing Amazon Bedrock AgentCore Gateway: Transforming enterprise AI agent tool development.
>
> About the authors
>
> Vivek Ghatala
>
> Vivek is a Senior Software Development Engineer at Amazon Web Services on the AWS FinTech team. He specializes in designing, building, and optimizing financial applications that scale to support AWS Data Center financial operations worldwide with accuracy. He seeks opportunities to build Generative AI applications that solve complex, error-prone, and time-intensive manual processes, helping Amazon Finance adopt Agentic AI and other technologies that boost productivity while avoiding pitfalls like hallucinations.
>
> Vishnu Elangovan
>
> Vishnu is a Worldwide Agentic AI Solution Architect with over a decade of experience in Applied AI/ML and Deep Learning. He loves building and tinkering with scalable AI/ML solutions and considers himself a lifelong learner. Vishnu is a trusted thought leader in the AI/ML community, regularly speaking at leading AI conferences and sharing his expertise on Agentic AI at top-tier events.
>
> Sreeja Das
>
> Sreeja is a Principal Engineer in AWS Fintech. Prior to her role in AWS Fintech, she spearheaded the re-architecture of Order &amp; Refund Processing, Billing, Checkbook, and the eCommerce Financial Integration Platform — systems collectively serving tens of trillions of customer requests daily — and holds two patents in distributed systems and data architecture.
>
> Lucien LaScala
>
> Lucien is a Data Engineer working with the DataStudio team in the AWS Fintech organization. He builds MCP servers and tools that allow finance stakeholders to quickly access, query, and understand complex financial data using natural language prompts. In his spare time, he enjoys watching 80s movies and hoping the Atlanta Falcons will be better next season.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。