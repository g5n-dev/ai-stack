---
title: "Monitor on-premises and multi-cloud AI agents with AgentCore Observability"
date: 2026-08-14T00:12:58+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "RAG", "AI Agent", "生成式 AI", "Prompt 工程", "Advanced (300)", "Amazon Bedrock AgentCore", "Technical How-to"]
categories: []
source: "blogs_podcasts"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:d4cb55046c67762db51c0ff2455a918db4d99759f9397e8b4df167f658b80b26"
source_payload_sha256: "sha256:5aba323a129229eda8b48b941d46bfa34c2ede5b3ee849b2483c92458cb148ac"
observation_id: obs_5e7836db2c1590662c40c19382d6bdf91af2a53f42f19fbd97ff6c18495188d4
event_id: evt_fb4a80be93594f40fbffe55ae9c1cb72d04eada7031d88f7f68d590ff5acdba4
revision_id: rev_4258235690bb58efcf075e2b891c0ed7f9d65cfff9ca46a2b61a764033c6a285
source_published_at: 2026-08-13T16:02:10Z
first_seen_at: 2026-08-13T16:22:37Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 74
description: "当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。"
external_url: https://aws.amazon.com/blogs/machine-learning/monitor-on-premises-and-multi-cloud-ai-agents-with-agentcore-observability
parent_observation_id: null
last_seen_at: 2026-08-15T00:00:00Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/monitor-on-premises-and-multi-cloud-ai-agents-with-agentcore-observability](https://aws.amazon.com/blogs/machine-learning/monitor-on-premises-and-multi-cloud-ai-agents-with-agentcore-observability)
- **发布域名**: aws.amazon.com

## 来源摘要/节选

> When you deploy AI agents built with frameworks like Strands Agents, LangGraph, and CrewAI, you need observability into their performance. This holds true whether they run on Amazon Elastic Kubernetes Service (Amazon EKS), Amazon Elastic Container Service (Amazon ECS), AWS Lambda, on-premises, or another cloud provider such as Google Cloud Platform (GCP) or Microsoft Azure.
>
> Amazon Bedrock AgentCore is a platform to build, connect, and optimize agents at scale, with any framework or model. Although Amazon Bedrock AgentCore Observability, a capability of Amazon Bedrock AgentCore, provides native tracing, monitoring, and analytics that local cloud monitoring tools don’t offer out of the box, it natively supports only agents deployed on AgentCore runtime in the AWS Cloud. If your agents run anywhere else, you need additional configuration to send telemetry to the dashboard.
>
> In this post, we show you how to set up observability for agents running outside AWS. You learn how to configure the AWS Distro for OpenTelemetry (ADOT) auto-instrumentation in non-AWS environments, route telemetry to the AgentCore Observability dashboard, and validate the setup end to end.
>
> The following diagram shows the end-to-end observability pipeline and how telemetry flows from agents to the AgentCore Observability dashboard.
>
> Figure 1: End-to-end observability pipeline from agents to the AgentCore Observability dashboard
>
> Solution overview
>
> The solution uses the AWS Distro for OpenTelemetry (ADOT) running in-process with the agent application. ADOT auto-instruments the agent framework and captures generative AI semantic convention spans, then exports the telemetry directly to the Amazon CloudWatch OpenTelemetry Protocol (OTLP) endpoint using SigV4 authentication with AWS Identity and Access Management (IAM) credentials.
>
> Sending telemetry from your AI agent to Amazon Bedrock AgentCore Observability requires three core components:
>
> ADOT auto-instrumentation: The AWS Distro for OpenTelemetry handles the complexities of exporting telemetry from non-AWS environments.
>
> IAM credentials: The ADOT uses these access keys to authenticate with CloudWatch and forward your agent’s telemetry (traces, metrics, and logs) to the AgentCore Observability dashboard.
>
> Environment variables: These contain specific OpenTelemetry settings related to routing and authentication.
>
> As seen in the following diagram, this cross-platform observability solution integrates several AWS services. Amazon CloudWatch serves as the foundation, handling telemetry ingestion and storage. Amazon Bedrock AgentCore Observability adds specialized monitoring dashboards for AI agents. AWS Distro for OpenTelemetry (ADOT) provides the cross-platform instrumentation capabilities. IAM secures the authentication between your external environments and AWS.
>
> Figure 2: Cross-platform observability architecture and the AWS services involved
>
> Observability is a foundational pillar of responsible AI. By routing telemetry to AgentCore Observability, you gain visibility into agent reasoning chains, tool invocations, and model outputs. This allows you to detect hallucinations, monitor for harmful or off-topic responses, track token usage for cost governance, and audit agent behavior across environments. This is especially critical for agents running outside AWS, where problematic outputs might go unnoticed without centralized observability.
>
> Prerequisites
>
> Before you begin, verify that you have:
>
> An AWS account:
>
> with Amazon Bedrock model access configured (this walkthrough uses Claude Haiku). For model availability by AWS Region, refer to supported models by AWS Region in Amazon Bedrock.
>
> for designated AgentCore Observability and designated log group(s).
>
> CloudWatch Transaction Search turned on in your account (one-time setup)
>
> Python 3.10 or later installed on your non-AWS environment.
>
> IAM user credentials (access key ID and secret access key) with permissions for:
>
> bedrock:InvokeModel.
>
> logs:CreateLogGroup, logs:CreateLogStream, logs:PutLogEvents.
>
> xray:PutTraceSegments, xray:PutTelemetryRecords, xray:GetSamplingRules, and xray:GetSamplingTargets.
>
> cloudwatch:PutMetricData.
>
> Outbound HTTPS access to AWS endpoints from your environment.
>
> Turn on CloudWatch Transaction Search
>
> If you haven’t turned on Transaction Search, run the following (one-time per account):
>
> aws xray update-trace-segment-destination --destination CloudWatchLogs --region us-east-1
>
> Verify it’s active:
>
> aws xray get-trace-segment-destination --region us-east-1
>
> # Expected: {"Destination": "CloudWatchLogs", "Status": "ACTIVE"}
>
> How it works
>
> The ADOT auto-instrumentation (aws-opentelemetry-distro) handles the complexity of exporting telemetry from non-AWS environments to CloudWatch:
>
> Auto-instrumentation: The opentelemetry-instrument command injects the ADOT into the Python runtime. It automatically patches boto3 (for Amazon Bedrock calls) and the Strands framework (for agent reasoning spans) to emit OpenTelemetry traces.
>
> SigV4 authentication: The aws_configurator uses the boto3 credential chain to sign OTLP export requests with SigV4. From non-AWS environments, this uses the AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables.
>
> CloudWatch OTLP endpoint: The ADOT exports traces and logs to the CloudWatch native OTLP ingestion endpoint. The OTEL_EXPORTER_OTLP_LOGS_HEADERS header directs logs to the specific AgentCore log group, which is how CloudWatch indexes the data under the generative AI observability dashboard. For details on how the CloudWatch OTLP endpoint URL is determined and configured, see CloudWatch OTLP endpoint.
>
> Generative AI semantic conventions: The Strands [otel] package emits spans following the OpenTelemetry generative AI semantic conventions, including agent reasoning steps, tool invocations, and model calls with token usage.
>
> The following diagram shows how telemetry export through ADOT auto-instrumentation works from non-AWS environments to CloudWatch.
>
> Figure 3: Telemetry export through ADOT auto-instrumentation from non-AWS environments to CloudWatch
>
> Walkthrough
>
> Follow these steps to configure and run a Strands agent in a non-AWS environment, with telemetry routed to AgentCore Observability.
>
> Step 1: Install dependencies
>
> On your non-AWS environment (on-premises server, GCP VM, Azure VM, or a compute with internet access):
>
> pip install "aws-opentelemetry-distro&gt;=0.10.0" boto3 "strands-agents[otel]"
>
> The aws-opentelemetry-distro package includes the ADOT auto-instrumentation with OTLP exporters specific to AWS and the aws_configurator that handles SigV4 authentication. The strands-agents[otel] package provides OpenTelemetry trace emission from the Strands framework.
>
> Step 2: Configure AWS credentials
>
> Set your IAM user credentials as environment variables.
>
> export AWS_ACCESS_KEY_ID=&lt;your-access-key-id&gt;
>
> export AWS_SECRET_ACCESS_KEY=&lt;your-secret-access-key&gt;
>
> export AWS_REGION=us-east-1
>
> Security note: For production deployments, consider using IAM Roles Anywhere instead of long-lived access keys. With IAM Roles Anywhere, on-premises workloads can obtain temporary credentials using X.509 certificates.
>
> Step 3: Set OpenTelemetry environment variables
>
> These environment variables configure the ADOT to route telemetry to the AgentCore Observability dashboard:
>
> export AGENT_OBSERVABILITY_ENABLED=true
>
> export OTEL_PYTHON_DISTRO=aws_distro
>
> export OTEL_PYTHON_CONFIGURATOR=aws_configurator
>
> export OTEL_RESOURCE_ATTRIBUTES="service.name=my-external-agent,aws.log.group.names=/aws/bedrock-agentcore/runtimes/my-external-agent"
>
> export OTEL_EXPORTER_OTLP_LOGS_HEADERS="x-aws-log-group=/aws/bedrock-agentcore/runtimes/my-external-agent,x-aws-log-stream=runtime-logs,x-aws-metric-namespace=bedrock-agentcore"
>
> export OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf
>
> export OTEL_TRACES_EXPORTER=otlp
>
> Key configuration details:
>
> AGENT_OBSERVABILITY_ENABLED=true activates generative AI-specific telemetry processing in the ADOT.
>
> OTEL_PYTHON_DISTRO=aws_distro and OTEL_PYTHON_CONFIGURATOR=aws_configurator activate the OpenTelemetry configuration specific to AWS, including SigV4 signing for the CloudWatch OTLP endpoint.
>
> OTEL_RESOURCE_ATTRIBUTES with aws.log.group.names tells CloudWatch to index the telemetry under the AgentCore Observability dashboard. Without this, traces go to generic Amazon CloudWatch Logs.
>
> OTEL_EXPORTER_OTLP_LOGS_HEADERS with x-aws-metric-namespace=bedrock-agentcore routes metrics in embedded metric format to the correct CloudWatch namespace.
>
> Step 4: Create the agent application
>
> Create a file named agent_test.py with a Strands agent:
>
> from strands import Agent
>
> from strands.models.bedrock import BedrockModel
>
> from opentelemetry import baggage
>
> from opentelemetry.context import attach
>
> import time
>
> # Configure the Bedrock model
>
> model = BedrockModel(
>
> model_id="us.anthropic.claude-haiku-4-5-20251001-v1:0",
>
> region_name="us-east-1"
>
> )
>
> # Create the agent
>
> agent = Agent(
>
> model=model,
>
> system_prompt="You are a helpful travel assistant."
>
> )
>
> # Set session ID for AgentCore session tracking
>
> # All agent calls after attach() share same session ID for multiple requests/responses
>
> session_id = f"external-session-{int(time.time())}"
>
> ctx = baggage.set_baggage("session.id", session_id)
>
> attach(ctx)
>
> # Run the agent
>
> response = agent("What are the top 3 things to do in Tokyo?")
>
> print(response)
>
> Step 5: Run with ADOT auto-instrumentation
>
> The opentelemetry-instrument command wraps your Python process with the ADOT, automatically instrumenting Amazon Bedrock calls and Strands framework operations:
>
> opentelemetry-instrument python3.12 agent_test.py
>
> The agent’s response appears in the terminal. Behind the scenes, the ADOT captures traces, spans, and logs, and exports them to CloudWatch.
>
> Step 6: Verify in AgentCore Observability
>
> You see telemetry data within two to three minutes of execution. Open the Amazon CloudWatch console:
>
> Choose GenAI Observability, then Bedrock AgentCore.
>
> In the Agents tab, look for my-external-agent.
>
> Choose the agent to view sessions, traces, and span metrics.
>
> The following screenshot shows the telemetry from the Strands agent (my-external-agent) running in a non-AWS environment, as seen in the AgentCore Observability dashboard in CloudWatch.
>
> Figure 4: The my-external-agent telemetry in the AgentCore Observability dashboard
>
> The console shows:
>
> Agent name: my-external-agent.
>
> Sessions: at least one session.
>
> Traces: trace spans showing the agent’s reasoning and Amazon Bedrock model invocations.
>
> Span details: invoke_agent, chat, execute_event_loop_cycle, and chat.us.anthropic.claude-haiku spans with latency and token metrics.
>
> The following screenshot shows a successful trace from the Strands agent (my-external-agent) with four spans, model information, and latency and token details in the AgentCore Observability dashboard.
>
> Figure 5: Trace detail for my-external-agent with span, latency, and token metrics
>
> Validating from Google Cloud Platform
>
> To confirm the solution works from a third-party cloud provider, we tested the same setup from Google Cloud Shell, a browser-based terminal running on GCP infrastructure.
>
> Set up the environment on Google Cloud Shell:
>
> # Create a virtual environment
>
> python3.12 -m venv venv
>
> source venv/bin/activate
>
> # Install dependencies
>
> pip install "aws-opentelemetry-distro" boto3 "strands-agents[otel]"
>
> # Set AWS credentials
>
> export AWS_ACCESS_KEY_ID=&lt;your-access-key-id&gt;
>
> export AWS_SECRET_ACCESS_KEY=&lt;your-secret-access-key&gt;
>
> export AWS_REGION=us-east-1
>
> # Set ADOT environment variables
>
> export AGENT_OBSERVABILITY_ENABLED=true
>
> export OTEL_PYTHON_DISTRO=aws_distro
>
> export OTEL_PYTHON_CONFIGURATOR=aws_configurator
>
> export OTEL_RESOURCE_ATTRIBUTES="service.name=gcp-hosted-agent,aws.log.group.names=/aws/bedrock-agentcore/runtimes/gcp-hosted-agent"
>
> export OTEL_EXPORTER_OTLP_LOGS_HEADERS="x-aws-log-group=/aws/bedrock-agentcore/runtimes/gcp-hosted-agent,x-aws-log-stream=runtime-logs,x-aws-metric-namespace=bedrock-agentcore"
>
> export OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf
>
> export OTEL_TRACES_EXPORTER=otlp
>
> Run the agent from GCP:
>
> cat &gt; agent_test.py &lt;&lt; 'EOF'
>
> from strands import Agent
>
> from strands.models.bedrock import BedrockModel
>
> from opentelemetry import baggage
>
> from opentelemetry.context import attach
>
> import time
>
> model = BedrockModel(
>
> model_id="us.anthropic.claude-haiku-4-5-20251001-v1:0",
>
> region_name="us-east-1"
>
> )
>
> agent = Agent(model=model, system_prompt="You are a helpful assistant.")
>
> # Set session ID for AgentCore session tracking
>
> # All agent calls after attach() share same session ID for multiple requests/responses
>
> session_id = f"gcp-session-{int(time.time())}"
>
> ctx = baggage.set_baggage("session.id", session_id)
>
> attach(ctx)
>
> response = agent("What are the top 3 things to do in Paris?")
>
> print(response)
>
> EOF
>
> opentelemetry-instrument python3.12 agent_test.py
>
> The following screenshot shows the Strands agent (gcp-hosted-agent) running on Google Cloud Shell (GCP) and returning a successful response.
>
> Figure 6: The gcp-hosted-agent running in Google Cloud Shell
>
> Verify cross-cloud telemetry
>
> Within two to three minutes of execution, the gcp-hosted-agent appears in the AgentCore Observability dashboard alongside agents running on AgentCore runtime or other environments.
>
> The following screenshot shows a successful trace from the Strands agent (gcp-hosted-agent) running on GCP with four spans, model information, and latency and token details in the AgentCore Observability dashboard.
>
> Figure 7: Trace detail for gcp-hosted-agent running on GCP
>
> The telemetry is identical to what an AgentCore runtime-hosted agent produces. Sessions, traces, span metrics, token usage, and latency are all visible in the same dashboard, regardless of where the agent runs.
>
> Although this walkthrough uses Strands Agents, the same ADOT-based pattern applies to other OpenTelemetry-compatible agent frameworks.
>
> When choosing how to deploy your AI agents, understanding the observability trade-offs between different runtime environments helps you make the right architectural decision. Agents deployed directly on Amazon Bedrock AgentCore runtime benefit from automatic observability configuration. Agents running in non-AWS environments require additional manual setup but offer greater deployment flexibility. The following comparison highlights the key differences in telemetry collection, credential management, and use cases to help you determine the best approach for your requirements.
>
> Aspect
>
> Non-AWS Runtime
>
> AgentCore runtime
>
> Telemetry supported
>
> ADOT – manual OTEL variables required
>
> ADOT – Automatic in-built OTEL variables
>
> Credential management
>
> IAM access key/secret or IAM Roles Anywhere
>
> Automatic (IAM role)
>
> Best for
>
> Agents on-premises, GCP, Azure, or a non-AWS environment
>
> Agents deployed on AWS with AgentCore
>
> Validated environments
>
> We tested the ADOT auto-instrumentation approach across two non-AWS environments:
>
> Environment
>
> Platform
>
> Result
>
> On-premises (simulated)
>
> Standalone server running in non-AWS environment
>
> Strands agent reporting telemetry (sessions, traces, spans) in AgentCore Observability
>
> Google Cloud Shell (GCP)
>
> Browser-based terminal running on Google Cloud Platform
>
> Strands agent reporting telemetry (sessions, traces, spans) in AgentCore Observability
>
> Best practices
>
> Based on our testing, we recommend the following when setting up cross-platform AgentCore Observability:
>
> Use consistent naming: The service.name in OTEL_RESOURCE_ATTRIBUTES becomes the agent name on the dashboard. Use descriptive names that identify the environment (for example, prod-onprem-support-agent and staging-gcp-research-agent).
>
> Verify with get-caller-identity first: Before running the agent, confirm that your credentials work by running python -c "import boto3; print(boto3.client('sts').get_caller_identity())". If this fails, the ADOT also fails silently.
>
> Use Python 3.10 or later: The ADOT requires Python 3.10 or later. We recommend Python 3.12 for the best compatibility with all dependencies.
>
> Set session IDs for multi-turn conversations: Use the OpenTelemetry baggage API to propagate session IDs:
>
> from opentelemetry import baggage
>
> from opentelemetry.context import attach
>
> ctx = baggage.set_baggage("session.id", "my-session-123")
>
> attach(ctx)
>
> Rotate credentials regularly: For production deployments, avoid long-lived access keys. Consider IAM Roles Anywhere for on-premises workloads, or use your cloud provider’s identity federation to assume AWS IAM roles.
>
> Clean up
>
> To remove the resources created during this walkthrough:
>
> # Delete the IAM access key (if created for testing)
>
> aws iam delete-access-key --user-name &lt;your-user&gt; --access-key-id &lt;your-key-id&gt;
>
> # Optionally delete the auto-created CloudWatch log groups
>
> aws logs delete-log-group --log-group-name /aws/bedrock-agentcore/runtimes/my-external-agent --region us-east-1
>
> aws logs delete-log-group --log-group-name /aws/bedrock-agentcore/runtimes/gcp-hosted-agent --region us-east-1
>
> This walkthrough uses Amazon Bedrock, Amazon CloudWatch, and AWS X-Ray, which incur costs. See the respective pricing pages for details.
>
> Conclusion
>
> Amazon Bedrock AgentCore Observability isn’t limited to agents running on AgentCore runtime or within AWS. Using ADOT auto-instrumentation with IAM credentials and the correct OpenTelemetry environment variables, you can send telemetry from your choice of environment with internet access. Your agents can run on-premises, on GCP, on Azure, or anywhere else and still report to the same AgentCore Observability dashboard.
>
> The setup requires a pip install and a set of environment variables. The resulting telemetry is identical to what AgentCore runtime-hosted agents produce: sessions, traces, span metrics, and token usage, all in one unified view.
>
> To get started, clone the sample code from GitHub and follow the instructions in the README to configure and run the agent in your environment.
>
> For agents already running on AWS but outside AgentCore runtime (EKS, ECS, Lambda), refer to the AgentCore Observability for EKS-hosted agents tutorial. For agents on AgentCore runtime, observability is configured automatically. See Add observability to your AgentCore resources.
>
> About the authors
>
> Vipul Gargav
>
> Vipul is a Technical Account Manager in AWS Enterprise Support, where he supports startup customers across a range of workloads with a specialization in monitoring and observability. He assists customers in designing and optimizing their cloud solutions for reliability and performance. Outside of work, Vipul enjoys woodworking and spending time outdoors biking and camping.
>
> Rajesh Kumar Ravi
>
> Rajesh is a Worldwide Specialist and Senior Solutions Architect at Amazon Web Services specializing in Amazon Bedrock AgentCore and Amazon Quick. He is an accomplished technology leader with years of experience in cross-functional leadership, scalable platforms, and enterprise AI product development, with a current focus on multi-agent systems, RAG, and cloud-native SaaS. Outside of work, he enjoys walking and short hiking trips.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。