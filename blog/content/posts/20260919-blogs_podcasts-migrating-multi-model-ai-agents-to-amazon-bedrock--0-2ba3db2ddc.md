---
title: "Migrating multi-model AI agents to Amazon Bedrock AgentCore runtime"
date: 2026-09-19T08:23:46+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "生成式 AI", "Prompt 工程", "Advanced (300)", "Amazon Bedrock AgentCore", "Technical How-to", "博客与播客"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:cbcc7e6ced907306abbc4a47830da04448ab35bcfd266d9e800984a7d1c8071b"
source_payload_sha256: "sha256:c2457b3909545799d6c19ce42e7932045418780e343b4a0f34ead35ac7ff1723"
observation_id: obs_2ba3db2ddc592fd6fddc0470161438eca7b0e5a18958de16fe36ddccb33c03e9
event_id: evt_e792a796ffe17c59f8a5e721e708325f6e90cd37317ef803a382d113278d27e6
revision_id: rev_103969f819e5f7f59d02b9ac35d551dffd5f286fb71e710348f17b495d2e9e95
source_published_at: 2026-09-18T15:38:53Z
first_seen_at: 2026-09-19T00:32:28Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 67
interpretation_sha256: "sha256:bce3a86294d6a2b9631e565444a9401d2eb17a63b46357dae1eaf1ad63e79aed"
description: "本文说明如何把一套在自管理容器上运行的多模型 AI Agent 迁移到 Amazon Bedrock AgentCore 的托管运行时，保留原有业务逻辑并利用平台提供的伸缩、身份和可观测能力。"
external_url: https://aws.amazon.com/blogs/machine-learning/migrating-multi-model-ai-agents-to-amazon-bedrock-agentcore-runtime
parent_observation_id: null
last_seen_at: 2026-09-22T00:00:00Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/migrating-multi-model-ai-agents-to-amazon-bedrock-agentcore-runtime](https://aws.amazon.com/blogs/machine-learning/migrating-multi-model-ai-agents-to-amazon-bedrock-agentcore-runtime)
- **发布域名**: aws.amazon.com

## 要点解读

### 这是什么
本文说明如何把一套在自管理容器上运行的多模型 AI Agent 迁移到 Amazon Bedrock AgentCore 的托管运行时，保留原有业务逻辑并利用平台提供的伸缩、身份和可观测能力。

### 用在哪里
适合已经在自建容器平台（如 Amazon ECS）上部署多模型 AI Agent 的团队，想要把容器编排、伸缩、身份和日志等运维工作交给平台，从而降低基础设施管理负担。

### 可以推断的
推测：迁移后开发者可以把更多时间投入到模型调度和业务规则优化上，而不必自行处理容器的生命周期和伸缩策略。  
推测：AgentCore 的框架无关特性意味着已有基于其他框架的 Agent 只需少量适配即可部署，无需大范围重写。

## 来源摘要/节选

> Organizations building multi-model agentic AI applications face growing infrastructure complexity. Managing container orchestration, scaling policies, identity, and observability for multiple model types adds operational overhead. Teams often spend more time on infrastructure than on agent logic development.
>
> Developers running agentic frameworks on self-managed infrastructure such as Amazon Elastic Container Service (Amazon ECS) with AWS Fargate have full control over their deployment configuration. As agentic workloads evolve and scale, teams might choose to adopt managed runtimes that provide built-in session management, identity, and observability.
>
> Amazon Bedrock AgentCore is a platform to build, connect, and optimize agents at scale, with any framework or model. AgentCore runtime, its managed deployment capability, handles container lifecycle, scaling, identity, and observability, so you can focus on your agent code.
>
> In a previous post, Agentic AI with multi-model framework using Hugging Face smolagents on AWS, we showed how to build a healthcare AI agent with multi-model orchestration on self-managed infrastructure. In this post, we show you how to migrate that multi-model agent to Amazon Bedrock AgentCore runtime. The migration reduces infrastructure management while preserving agent capabilities, including triple-model orchestration and vector-enhanced knowledge retrieval.
>
> Solution overview
>
> This solution migrates a multi-model healthcare AI agent to Amazon Bedrock AgentCore runtime while preserving the existing agent logic. The agent processes medical queries across three model backends with vector-enhanced knowledge retrieval, all running inside a single AgentCore-managed container. You can direct each query to the model backend suited to the task. A domain-specific model such as BioM-ELECTRA-Large-SQuAD2 on Amazon SageMaker AI handles specialized biomedical queries, and a foundation model (FM) such as Llama 3.1 70B Instruct by Meta on Amazon Bedrock handles broader medical reasoning. This approach helps healthcare teams address a range of query types while reducing the operational overhead of managing the underlying infrastructure.
>
> The standalone version from the previous post deployed on Amazon ECS with AWS Fargate includes container orchestration, scaling, identity, and observability configured by the user. The AgentCore version wraps the same agent logic with the AgentCore runtime decorator pattern, and AgentCore runtime handles these operational concerns automatically.
>
> Hugging Face smolagents is an open source Python library designed to build and run agents using a few lines of code. This solution uses Hugging Face smolagents framework as a reference implementation, demonstrating that AgentCore runtime supports any agentic framework. With the bring-your-own (BYO) agent approach, you can deploy existing agent code to AgentCore runtime without rewriting or adapting to a specific framework.
>
> Note: This solution is a sample implementation for demonstration purposes. Production deployments handling medical or other sensitive queries use Amazon Bedrock Guardrails for content filtering and grounding validation as a standard control.
>
> Architecture
>
> The solution consists of the following services and features:
>
> Amazon Bedrock AgentCore runtime for managed agent container deployment, scaling, identity, and observability.
>
> Amazon Bedrock with Llama 3.1 70B Instruct by Meta for complex medical reasoning. For model availability by AWS Region, refer to Supported models by AWS Region in Amazon Bedrock.
>
> Amazon SageMaker AI with BioM-ELECTRA-Large-SQuAD2 for specialized biomedical queries and managed auto scaling.
>
> Amazon OpenSearch Service for vector similarity matching and contextual knowledge retrieval with medical knowledge indexing.
>
> Containerized model server with BioM-ELECTRA-Large-SQuAD2 for self-hosted model deployment.
>
> AWS Identity and Access Management (IAM) for security and access control.
>
> Note: The previous post (standalone version) uses Claude 3.5 Sonnet V2 by Anthropic. This post uses Llama 3.1 70B Instruct by Meta, demonstrating that AgentCore runtime is model-agnostic. The model choice is an implementation decision, not a requirement.
>
> The following diagram illustrates the solution architecture and how the agent orchestrates across three model backends.
>
> Figure 1: Multi-model healthcare agent architecture on Amazon Bedrock AgentCore runtime
>
> A client web interface connects to Amazon Bedrock AgentCore runtime, which hosts the healthcare agent container. The container uses the Hugging Face smolagents framework with the AgentCore runtime decorator. AgentCore runtime provides built-in identity and observability. The agent orchestrates across three model backends: Amazon SageMaker AI with BioM-ELECTRA, Amazon Bedrock with Llama 3.1 70B Instruct by Meta, and a containerized model server with BioM-ELECTRA. The solution includes Amazon OpenSearch Service for vector-enhanced knowledge retrieval.
>
> This solution supports deployment options with each backend optimized for different scenarios:
>
> Amazon SageMaker AI for managed endpoints with auto scaling using Hugging Face Hub models.
>
> Amazon Bedrock for serverless access to foundation models and complex reasoning through AWS APIs.
>
> A containerized model server for self-hosted model deployment and tool integration from Hugging Face Hub (deployable on Amazon ECS, Amazon Elastic Kubernetes Service (Amazon EKS), or other container environments).
>
> The three backends implement Hugging Face Messages API compatibility, providing consistent request and response formats regardless of the selected model service.
>
> The complete implementation is available in the sample-healthcare-agent-with-agentcore-on-aws GitHub repository.
>
> Migrate the agent to AgentCore runtime
>
> This section walks through migrating the existing healthcare AI agent to Amazon Bedrock AgentCore runtime using the AgentCore CLI.
>
> Prerequisites
>
> Before you deploy the solution, you need the following:
>
> An AWS account with access to Amazon Bedrock AgentCore runtime and appropriate permissions to create IAM roles and Amazon OpenSearch Service domains.
>
> AWS Command Line Interface (AWS CLI) version 2.0 or later installed and configured.
>
> Node.js 20 or later (required for the deployment CLI).
>
> AWS Cloud Development Kit (AWS CDK) installed.
>
> AgentCore CLI installed.
>
> Python 3.10 or later for running deployment scripts.
>
> Docker installed and running (required for code execution isolation).
>
> Access to Amazon Bedrock model, Amazon SageMaker AI, and Amazon OpenSearch Service domain in your AWS Region with appropriate IAM permissions to create and manage resources.
>
> bedrock-agentcore Python SDK installed.
>
> For this implementation, we’re using Python 3.10+, smolagents framework, transformers 4.55.0+, and boto3.
>
> AgentCore runtime concepts
>
> Amazon Bedrock AgentCore runtime uses a decorator pattern to wrap your agent logic. The key components are:
>
> BedrockAgentCoreApp – initializes the AgentCore application.
>
> @app.entrypoint – decorates the function that AgentCore runtime calls when a request arrives.
>
> app.run() – starts the AgentCore runtime server.
>
> The following code shows the AgentCore integration pattern:
>
> from bedrock_agentcore.runtime import BedrockAgentCoreApp
>
> app = BedrockAgentCoreApp()
>
> @app.entrypoint
>
> def healthcare_agent_entrypoint(payload):
>
> user_input = payload.get("prompt", "")
>
> model_type = payload.get("model_type", "sagemaker")
>
> # Your existing agent logic here
>
> agent = TripleHealthcareAgent(vector_store=vector_store)
>
> response = agent.run(user_input, model_type=model_type)
>
> return str(response)
>
> if __name__ == "__main__":
>
> app.run()
>
> The agent code between the decorator and return statement remains unchanged from the standalone version. AgentCore runtime handles container lifecycle, scaling, identity, and observability automatically.
>
> Set up the project
>
> Create an AgentCore project and add your existing agent using the AgentCore CLI.
>
> Install the AgentCore CLI:
>
> npm install -g @aws/agentcore
>
> Create a new AgentCore project:
>
> agentcore create --project-name healthcareagent --no-agent --build Container --language Python --protocol HTTP --model-provider Bedrock --memory none
>
> Add your existing agent as a bring-your-own (BYO) agent:
>
> agentcore add agent --name healthcare_agentcore --type byo --build Container --language Python --protocol HTTP --network-mode PUBLIC --code-location ./agent-code --entrypoint healthcare_agentcore.py --framework Strands --model-provider Bedrock
>
> Note: The --framework flag specifies the CLI template. The actual agent code uses Hugging Face smolagents, which is compatible with AgentCore runtime regardless of the template selection.
>
> Prepare the container
>
> Create a pyproject.toml in your agent code directory to define dependencies:
>
> [project]
>
> name = "healthcare-agentcore"
>
> version = "1.0.0"
>
> requires-python = "&gt;=3.10"
>
> dependencies = [
>
> "smolagents&gt;=1.24.0",
>
> "transformers&gt;=4.55.0",
>
> "boto3&gt;=1.37.0",
>
> "opensearch-py&gt;=3.1.0",
>
> "requests-aws4auth&gt;=1.3.1",
>
> "bedrock-agentcore&gt;=0.1.0",
>
> "numpy&gt;=1.26.0",
>
> "requests&gt;=2.32.0",
>
> "docker&gt;=7.1.0",
>
> ]
>
> Create a Dockerfile:
>
> FROM public.ecr.aws/docker/library/python:3.12-slim
>
> RUN pip install --no-cache-dir uv
>
> WORKDIR /app
>
> COPY pyproject.toml ./
>
> RUN uv pip install --system -r pyproject.toml
>
> COPY . .
>
> EXPOSE 8080
>
> CMD ["python", "healthcare_agentcore.py"]
>
> Create a .dockerignore to keep the image size within the 2 GB limit:
>
> venv/
>
> .venv/
>
> __pycache__/
>
> .git/
>
> *.pyc
>
> Deploy to AgentCore runtime
>
> With the project configured, you can deploy the agent using a single CLI command.
>
> Deploy the agent:
>
> agentcore deploy -y
>
> The CLI builds the container, pushes it to Amazon Elastic Container Registry (Amazon ECR), and creates the AgentCore runtime agent. Deployment takes approximately 10–15 minutes.
>
> Test the deployed agent
>
> You can test the deployed agent in two ways: using the AgentCore CLI or programmatically with boto3.
>
> Invoke the agent using the AgentCore CLI:
>
> agentcore invoke --prompt '{"prompt": "What are the side effects of metformin?", "model_type": "llama"}'
>
> Or, invoke programmatically using boto3:
>
> This path invokes the same deployed agent as the CLI, using the boto3 SDK directly. The agentRuntimeArn identifies your deployed agent, contentType specifies the request format, and payload carries the prompt and model selection.
>
> import boto3, json
>
> client = boto3.client('bedrock-agentcore', region_name='us-west-2')
>
> payload = json.dumps({
>
> "prompt": "What are the side effects of metformin?",
>
> "model_type": "llama"
>
> })
>
> response = client.invoke_agent_runtime(
>
> agentRuntimeArn='&lt;your-agent-runtime-arn&gt;',
>
> contentType='application/json',
>
> accept='application/json',
>
> payload=payload.encode('utf-8')
>
> )
>
> result = response['response'].read().decode('utf-8')
>
> print(result)
>
> Key differences from self-managed deployment
>
> The standalone version and the AgentCore runtime version deploy the same agent in different ways. The following sections describe what each path provides.
>
> Amazon ECS with AWS Fargate deployment
>
> The standalone version runs on Amazon ECS with AWS Fargate. You define ECS task definitions and service configuration, set auto scaling policies, configure IAM roles per service, and set up observability through Amazon CloudWatch. Deployment uses a Docker build, an Amazon ECR push, and an ECS service update. This path gives you full control over container configuration, networking, and scaling behavior. The agent code lives in healthcare_agentcore.py, integrates with Amazon Bedrock, Amazon SageMaker AI, and the containerized backend, and uses Amazon OpenSearch Service for vector search.
>
> Amazon Bedrock AgentCore runtime deployment
>
> The AgentCore runtime version runs the same healthcare_agentcore.py agent code with the AgentCore decorator pattern. AgentCore runtime provides container orchestration, session-based scaling, identity management through IAM integration, and observability through built-in tracing and logging. Deployment uses a single command (agentcore deploy). The model integration (Amazon Bedrock, Amazon SageMaker AI, containerized backend) and vector search (Amazon OpenSearch Service) remain the same as the standalone version.
>
> Both deployment approaches have distinct advantages. Amazon ECS with AWS Fargate provides full control over container configuration, networking, and scaling policies, suitable for teams with existing container operations expertise or specific infrastructure requirements. Amazon Bedrock AgentCore runtime is suited for teams that prefer managed infrastructure and want to focus primarily on agent logic development.
>
> Regardless of the deployment path, the following elements remain unchanged when migrating from the standalone version to AgentCore runtime:
>
> Core agent logic (BedrockAgentCoreApp decorator + existing code).
>
> Multi-model orchestration across Amazon Bedrock, Amazon SageMaker AI, and containerized backends.
>
> Vector-enhanced knowledge retrieval with Amazon OpenSearch Service.
>
> Hugging Face Messages API compatibility across model backends.
>
> Clean up
>
> To avoid incurring future charges, delete the resources you created when you no longer need them. If you plan to continue using the deployed agent, no action is required.
>
> Remove the AgentCore runtime agent:
>
> First, remove all resources from your local configuration:
>
> agentcore remove all
>
> Then deploy again to tear down the AWS resources:
>
> agentcore deploy
>
> Delete the Amazon SageMaker AI endpoint:
>
> aws sagemaker delete-endpoint --endpoint-name healthcare-agentcore-endpoint-1 --region us-west-2
>
> Delete the Amazon OpenSearch Service domain:
>
> aws opensearch delete-domain --domain-name healthcare-vector-store --region us-west-2
>
> Conclusion
>
> In this post, we showed how to migrate a multi-model healthcare AI agent from self-managed Amazon ECS with AWS Fargate infrastructure to Amazon Bedrock AgentCore runtime. The migration required no changes to the core agent logic. The same healthcare_agentcore.py file orchestrates across Amazon Bedrock, Amazon SageMaker AI, and a containerized model server. It runs on AgentCore runtime with the addition of the AgentCore decorator pattern (BedrockAgentCoreApp, @app.entrypoint, and app.run()). For healthcare teams, this pattern directs specialized biomedical queries to a domain-specific model such as BioM-ELECTRA-Large-SQuAD2 on Amazon SageMaker AI. It routes broader medical reasoning to a foundation model such as Llama 3.1 70B Instruct by Meta on Amazon Bedrock. Together, these backends support a range of query types.
>
> For teams that choose managed infrastructure, AgentCore runtime handles container orchestration, scaling, identity management, and observability. You can focus on agent logic development instead. The framework-agnostic design supports a wide combination of models and agentic frameworks, making this migration pattern applicable across industries including healthcare, financial services, and manufacturing.
>
> To get started, clone the sample-healthcare-agent-with-agentcore-on-aws GitHub repository and follow the deployment steps in this post. To understand the standalone implementation that this post migrates from, see Agentic AI with multi-model framework using Hugging Face smolagents on AWS. If there are questions about getting started with Amazon Bedrock AgentCore, speak with an AWS generative AI Specialist.
>
> Further reading
>
> Agentic AI on AWS – Build, deploy, and scale AI agents with AWS
>
> Make agents a reality with Amazon Bedrock AgentCore: Now generally available
>
> Amazon Bedrock documentation
>
> Build trustworthy AI agents with Amazon Bedrock AgentCore Observability
>
> About the author
>
> Sanhita Sarkar
>
> Sanhita Sarkar, PhD, drives global AI/ML and generative AI partner solutions at AWS. She brings extensive leadership experience across edge, cloud, and data center environments, holds several patents, has published research papers, and serves as chair for technical conferences.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。