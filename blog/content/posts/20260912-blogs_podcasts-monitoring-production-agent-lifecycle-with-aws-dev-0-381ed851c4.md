---
title: "Monitoring production agent lifecycle with AWS DevOps Agent and AgentCore Evaluations"
date: 2026-09-12T02:35:20+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "Prompt 工程", "Advanced (300)", "Amazon Bedrock AgentCore", "Best Practices", "DevOps", "博客与播客"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:a4d29f0d39e3206cdcbe5f60d44848e2292872febfe4491eaf6107c92d522a50"
source_payload_sha256: "sha256:3a3147c8793b06aec2b057e2d5949153b468c6c94d2f0d1d6b440e4c1cd83041"
observation_id: obs_381ed851c46a02e93d1534aa03fdca93a958451c12187f93437bc710a5e32162
event_id: evt_54ca990baa98051f48bcba8058bb2496a33728fa3de9e0de5e509d19420a5c84
revision_id: rev_065c1a576e868e3abc44cb01142cea389460ec0120199f076d1309ea5812d986
source_published_at: 2026-09-11T18:26:38Z
first_seen_at: 2026-09-11T18:45:13Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: true
source_truncation_reason: "crawler_feed_content_limit"
source_support: 1.0
source_title_chars_original: 85
interpretation_sha256: "sha256:37c4afc0cdbe597bc92570a9a7a98ee248be8b930fb92dcf1251aaf550b46986"
description: "该方案通过两层监控来追踪生产环境中的多智能体系统：一边持续评估智能体的输出质量，一边自动调查底层基础设施的健康状态，以发现传统指标难以捕获的异常。"
external_url: https://aws.amazon.com/blogs/machine-learning/monitoring-production-agent-lifecycle-with-aws-devops-agent-and-agentcore-evaluations
parent_observation_id: null
last_seen_at: 2026-09-12T00:00:00Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/monitoring-production-agent-lifecycle-with-aws-devops-agent-and-agentcore-evaluations](https://aws.amazon.com/blogs/machine-learning/monitoring-production-agent-lifecycle-with-aws-devops-agent-and-agentcore-evaluations)
- **发布域名**: aws.amazon.com

## 要点解读

### 这是什么  
该方案通过两层监控来追踪生产环境中的多智能体系统：一边持续评估智能体的输出质量，一边自动调查底层基础设施的健康状态，以发现传统指标难以捕获的异常。

### 用在哪里  
适用于在云平台部署 AI 智能体的团队，尤其是需要兼顾智能体行为有效性和服务可靠性的复杂编排系统。常见于需要跨服务追踪调用链和权限错误的场景。

### 可以推断的  
推测：质量评估层通过对比实际交互与预期目标，帮助快速识别工具选错或任务未完成等行为层面的缺陷。  
推测：基础设施调查层能够自动聚合日志与调用链路信息，减少人工排查时间，尤其在调用深度较大、异常不直接抛出的情况下更具价值。

## 来源摘要/节选

> Multi-agent systems in production experience issues in ways that traditional monitoring misses. For example, the agent can’t invoke its foundation model (FM) and returns an empty response. This could be because of a missing AWS Identity and Access Management (IAM) permission on an agent’s execution role that doesn’t throw a 500 error. A supervisor agent with a poorly scoped prompt doesn’t increase error rates but instead starts routing 20 percent of requests to the unintended specialist while the infrastructure metrics stay green.
>
> Infrastructure monitoring and agent effectiveness monitoring require different approaches. Amazon CloudWatch metrics show whether systems executed correctly, but not whether agents helped users accomplish their goals. An agent can successfully invoke Amazon Bedrock, call every tool without errors, and return a response while completely misunderstanding what the user needs. Infrastructure issues often manifest as reduced agent behavior rather than clear errors. When permissions are revoked or services throttle, agents might experience silent issues. For example, the booking agent stops completing reservations, but the logs show successful tool executions because the issue occurred three calls deep in a chain that didn’t surface an exception.
>
> These problems compound in multi-agent systems where a single user request triggers a supervisor agent that routes work to multiple specialists, each with their own tools and model invocations. There’s typically no fixed execution graph to instrument, failures can occur at multiple handoff points, and their propagation through the system is not always predictable.
>
> We built a production airline reservation system with four specialized agents that combine Amazon Bedrock AgentCore Evaluations for continuous agent quality assessment and AWS DevOps Agent for autonomous infrastructure incident investigation. Amazon Bedrock AgentCore is a platform to build, connect, and optimize agents at scale, with any framework or model. AgentCore Evaluations addresses the quality monitoring gap, continuously scoring live interactions to catch wrong tool selections, task failures, and quality regressions that infrastructure metrics miss entirely. AWS DevOps Agent addresses the second, autonomously tracing failures across service boundaries, correlating IAM policies, invocation logs, and orchestration traces without manual investigation. These two layers show whether the agent works correctly and whether the infrastructure supports it.
>
> Key technologies
>
> The system uses several AWS services:
>
> Amazon Bedrock provides API access to foundation models from leading AI companies including Anthropic, Meta, Mistral, and Amazon. In our airline reservation system built on AgentCore runtime, Amazon Bedrock powers the language understanding. For model availability by AWS Region, refer to Supported models by AWS Region in Amazon Bedrock.
>
> AgentCore runtime handles agent orchestration and manages interaction lifecycles, with built-in observability through OpenTelemetry instrumentation.
>
> With the Fullstack AgentCore Solution Template (FAST), teams can quickly deploy a secured React frontend connected to an AgentCore backend.
>
> AgentCore Evaluations is a quality assessment framework integrated into AgentCore runtime. It continuously scores agent interactions using LLM-as-a-Judge methodology, providing metrics on helpfulness, correctness, goal completion, and other quality dimensions.
>
> AWS DevOps Agent is an autonomous investigation tool that acts as an on-call engineer for your infrastructure. When incidents occur, it automatically analyzes Amazon CloudWatch logs, traces failures across service boundaries, and provides root cause analysis with remediation recommendations.
>
> Strands Agents is an open source SDK for building AI agents with a model-driven approach, supporting multi-agent collaboration patterns including Swarm, Graph, and Agents-as-Tools.
>
> OpenTelemetry is an open source observability framework that provides standardized instrumentation for collecting traces, metrics, and logs. AgentCore runtime uses OpenTelemetry to emit monitoring data to Amazon CloudWatch, facilitating consistent observability across the system.
>
> The Swarm Pattern is a multi-agent orchestration approach where a supervisor agent dynamically routes work to specialized agents based on the task at hand. Unlike fixed workflows, Swarm supports adaptive execution paths that change based on runtime decisions, making it powerful for complex tasks but challenging to monitor.
>
> Dual-layer monitoring: quality and infrastructure
>
> The monitoring architecture answers two questions: Is the agent working well? Is the infrastructure healthy?
>
> Amazon Bedrock AgentCore Evaluations: Continuous quality monitoring
>
> AgentCore Evaluations scores live agent interactions on helpfulness, correctness, and goal completion. The system samples a configurable percentage of production requests and evaluates them in the background. Every score comes with reasoning that explains why that score was assigned based on the conversation context, tools used, and task requirements.
>
> When quality metrics drop, it runs pattern analysis across recent low-scoring sessions to identify common failure modes. If the agent consistently chooses the wrong tool for a specific request type, or provides correct information in an unhelpful format, the pattern analysis surfaces that. It then generates concrete recommendations: specific prompt changes, tool selection adjustments, or orchestration logic improvements.
>
> AWS DevOps Agent: Autonomous infrastructure investigation
>
> AWS DevOps Agent monitors system health across metrics, logs, and error patterns. When something breaks, the agent investigates on its own. It pulls relevant Amazon CloudWatch logs, builds a topology graph of affected resources, correlates errors across services (IAM, Amazon Bedrock, your agent runtime), traces the failure path, and delivers specific fix recommendations. In addition to sending an alert with a link to Amazon CloudWatch, it also does the investigation by connecting a blank agent response to a missing IAM permission or linking a spike in timeouts to Amazon Bedrock throttling in a specific Region.
>
> How the layers work together
>
> AgentCore Evaluations replaces intuition with quantitative quality metrics, so teams can measure the actual impact of changes. AWS DevOps Agent automates much of the investigation that previously required manual war rooms by autonomously investigating infrastructure incidents the moment they occur. Together they create the continuous feedback loop, monitor, analyze, improve, deploy, that production multi-agent systems require.
>
> The airline reservation system: why it’s hard to monitor
>
> To demonstrate this architecture end to end, we built an airline reservation system that handles complex, dynamic queries: multi-city bookings, loyalty program benefit application, and company travel policy compliance, all within a single conversational turn. This use case demands exactly the kind of multi-agent coordination that makes production monitoring hard: parallel operations, multiple data sources, sequential dependencies, and strict correctness requirements where errors have real consequences.
>
> Consider a request like this one: “Book me from Seattle to Boston on March 15th, then Boston to Miami on March 18th. Use my companion certificate for the second leg and make sure both flights comply with my company’s travel policy. I’m Gold status so apply any eligible upgrades.”
>
> Handling this in a single conversational turn requires searching two separate routes and retrieving loyalty status and certificates from a different data source while the flight search runs. The bookings must then be sequenced in the right order, because the companion certificate can’t be applied until the flight is selected and the fare class is known. Applying a certificate to an ineligible flight frustrates users. Booking a flight that violates corporate policy wastes money.
>
> We built this with four specialized agents using the Swarm pattern (Figure 1). The Supervisor Agent receives requests and acts as an entry point, uses a think tool to plan subtasks, routes work to other agents which can hand off tasks to each other. The Flight Agent searches routes and handles multi-city connections. The User Agent fetches loyalty status, certificates, and profile data. The Reservation Agent creates, modifies, and cancels bookings, validating before committing changes.
>
> In a Swarm, agents share working memory and hand off work to one another dynamically. Each specialist decides who should act next based on what it finds, rather than following a predetermined execution plan. The supervisor is only the entry point. After a request is in flight, control passes to whichever peer is best suited to the next step, not back through a central router. If flight search finds no direct route, the Flight Agent runs the connection search itself, then hands off to the Reservation Agent once it has options to book. If a user’s certificate doesn’t apply, the User Agent adjusts and passes the task along. This handles unpredictable request structures without a predefined execution graph, but it also means there is no fixed call graph to instrument.
>
> Failures can occur at any handoff point, and because execution paths change based on runtime decisions, the failure path changes each time too. A quality failure and an infrastructure failure can look nearly identical from the outside, but they require completely different responses. From the outside, a quality failure and an infrastructure failure look the same. AgentCore Evaluations catches the first kind: everything executes but the agent still fails the user. AWS DevOps Agent catches the second: infrastructure breaks silently and surfaces as degraded behavior.
>
> Figure 1: Swarm multi-agent pattern
>
> Dual monitoring architecture
>
> The following diagram shows how these components connect.
>
> Figure 2: Full system architecture showing the React frontend, AgentCore runtime, Amazon CloudWatch, and AWS DevOps Agent
>
> We built a React frontend hosted on AWS Amplify that connects through Amazon Bedrock AgentCore Identity, a capability of Amazon Bedrock AgentCore, to Amazon Bedrock AgentCore runtime, where the four-agent swarm handles user requests. AWS Amplify hosts the conversational interface, Amazon Simple Storage Service (Amazon S3) handles session storage, and Amazon Bedrock AgentCore Identity manages authentication between the frontend and the runtime.
>
> Monitoring data originates from a single source: the Amazon Bedrock AgentCore runtime hosting the four-agent swarm. Amazon Bedrock AgentCore Observability, a capability of Amazon Bedrock AgentCore, instruments the runtime directly, capturing traces and metrics in OpenTelemetry format and forwarding them to Amazon CloudWatch. Amazon Bedrock AgentCore Evaluations draws from those same runtime traces to score live interactions, with evaluation results also flowing into Amazon CloudWatch. This means operational metrics, distributed traces, and quality scores land in one place.
>
> The second monitoring layer connects to this same backend. When an incident occurs, a team member submits it to AWS DevOps Agent through a signed webhook. The agent pulls Amazon CloudWatch logs and metrics, investigates autonomously, and returns findings and remediation steps without requiring anyone to navigate between tools.
>
> Getting started
>
> Open source: We built this system on FAST and the complete source code for this system including CDK infrastructure, evaluation dashboard, and AWS DevOps Agent integration is available in the GitHub repository. We used the AgentCore Evaluations Guide in the fullstack-solution-template-for-agentcore (FAST) as reference.
>
> To use Amazon Bedrock AgentCore Evaluations, you need:
>
> AgentCore CLI (https://github.com/aws/agentcore-cli)
>
> AWS credentials with bedrock-agentcore and Amazon CloudWatch permissions.
>
> The bedrock-agentcore Python SDK (Boto3 client)
>
> Layer 1: Amazon Bedrock AgentCore Evaluations, is the agent working well?
>
> Silent quality issues in production agents impact team efficiency, user trust, and business outcomes. AgentCore Evaluations catches these failures the moment they begin by continuously scoring live interactions against structured quality dimensions.
>
> Video 1: Extracting evaluation metrics for sessions, traces, and spans; viewing metrics on the dashboard to understand agent performance; performing on-demand evaluation by exploring session traces and spans; running the AI engine to identify patterns across low-scoring sessions; and uploading prompts to receive AI-generated improvement recommendations
>
> Amazon Bedrock AgentCore provides 16 built-in evaluators organized by what they measure and when they run. There are 13 LLM-as-a-Judge evaluators to score interactions with detailed explanations, so teams can verify judgments and understand exactly why an interaction received a particular rating, and three deterministic trajectory matchers.
>
> Evaluator
>
> Definition
>
> Evaluation Level
>
> Goal Success Rate
>
> Assesses whether the AI assistant successfully completed the user goals within a conversation session by analyzing the entire conversation end-to-end.
>
> Session
>
> Coherence
>
> Assesses the logical consistency and cohesion of a response, checking for self-contradictions, logic gaps, and soundness of reasoning without evaluating factual accuracy.
>
> Trace
>
> Conciseness
>
> Measures how efficiently the assistant communicates, assessing whether responses provide necessary information using minimal words without unnecessary elaboration.
>
> Trace
>
> Correctness
>
> Assesses the factual accuracy of a response to a given task, focusing on whether the content and solution are accurate regardless of style or presentation.
>
> Trace
>
> Faithfulness
>
> Assesses whether a response remains consistent with the conversation history, identifying conflicts between the current response and previous interactions within the same conversation.
>
> Trace
>
> Harmfulness
>
> Detects potentially harmful content in a response, including insults, hate speech, violence, inappropriate sexual content, and stereotyping.
>
> Trace
>
> Helpfulness
>
> Assesses how effectively a response helps users progress toward their goals, evaluated purely from the user’s perspective on whether the response moves them closer to their objectives.
>
> Trace
>
> Instruction Following
>
> Assesses whether a response adheres to the explicit instructions provided in the user’s input, focusing on compliance with specific directives regardless of overall response quality.
>
> Trace
>
> Refusal
>
> Detects when the assistant declines to address or fulfill a user’s request, identifying both direct declines and indirect avoidance of the requested task.
>
> Trace
>
> Response Relevance
>
> Assesses how well a response addresses the specific question or request, measuring the focus and relevance of the response to the given input.
>
> Trace
>
> Stereotyping
>
> Detects bias and stereotypical content in a response, identifying prejudicial assumptions or generalizations about specific groups of people.
>
> Trace
>
> Tool Parameter Accuracy
>
> Assesses whether the assistant correctly uses contextual information when making tool calls, verifying that tool parameters are accurately derived from the conversation context.
>
> Tool
>
> Tool Selection Accuracy
>
> Assesses whether the assistant chooses the appropriate tool for a given situation, determining if the selected action is justified and optimal at a specific point in the conversation.
>
> Tool
>
> Trajectory Any Order Match
>
> Validates that expected tools are present regardless of order.
>
> Session
>
> Trajectory Exact Order Match
>
> Validates that actual tools match expected tools in exact order with no extras.
>
> Session
>
> Trajectory In Order Match
>
> Validates that expected tools appear in order within actual trajectory, extras allowed between.
>
> Session
>
> Table 1: Built-in evaluator metrics supported by AgentCore Evaluations
>
> Online evaluation: continuous production monitoring
>
> Online evaluation monitors live agent interactions by continuously sampling a configurable percentage of traces (from 0.01–100 percent) and scoring them asynchronously against your chosen evaluators. This asynchronous, event-driven design means evaluation runs alongside production traffic without adding to user-facing response latency.
>
> Amazon Bedrock AgentCore emits evaluation metrics in real time to Amazon CloudWatch through OpenTelemetry. If you’re already collecting traces for observability, online evaluation adds quality scores alongside your existing operational metrics without requiring code changes or redeployments. You can set Amazon CloudWatch alarms that trigger the moment a quality metric drops below your defined threshold catching silent quality failures before they reach a broad set of users.
>
> For our airline reservation system online evaluation, we selected three built-in Amazon Bedrock AgentCore evaluators that provide comprehensive coverage of agent quality: Helpfulness, Correctness, and Goal Success Rate. We chose these metrics because they represent the three fundamental dimensions of agent performance that matter most to end users. Together, these three metrics create a balanced scorecard that captures both the quality of individual responses and the effectiveness of the overall interaction. This gives teams actionable insights into where their agents excel and where they need improvement.
>
> Metric
>
> Why it matters
>
> Example scenarios
>
> Helpfulness
>
> Captures user satisfaction beyond correctness. Identifies responses that are technically accurate but not useful. Helps optimize for user experience, not only accuracy. Detects when agents provide too much or too little information.
>
> High helpfulness: Agent provides a clear, actionable answer with context. Low helpfulness: Agent gives a correct but overly technical response to a simple question.
>
> Correctness
>
> Facilitates reliability and trustworthiness. Catches hallucinations and factual errors. Critical for domains requiring accuracy (finance, healthcare, legal). Builds user confidence in the agent.
>
> High correctness: Agent provides accurate data and valid reasoning. Low correctness: Agent makes up facts or provides incorrect calculations.
>
> Goal Success Rate
>
> Measures actual business value delivered. Captures multi-turn conversation effectiveness. Identifies when agents get stuck or fail to complete tasks. Aligns with user intent and business objectives.
>
> High goal success: User wanted to book a flight, and the agent completed the booking. Low goal success: User wanted to book a flight, but the agent only provided flight options.
>
> Workflow to set up the online evaluation configuration:
>
> Online evaluation runs in production without interruption in the background, automatically sampling sessions at your configured rate and writing results to Amazon CloudWatch Logs without impacting production latency.
>
> Workflow diagram for setting up the online evaluation configuration
>
> Why not more metrics?
>
> Avoid metric overload: Too many metrics make it hard to identify what matters.
>
> Reduce evaluation costs: Each evaluator adds latency and cost per invocation.
>
> Focus on actionable insights: These three cover the dimensions that matter most to users.
>
> Enable quick iteration: Teams can quickly understand and act on these metrics.
>
> Additional evaluators (Faithfulness, Instruction Following, Tool Use Quality) are available but not enabled by default. Teams can add them based on their specific needs.
>
> Evaluation dashboard showing agent quality score summaries
>
> Figure 3: Evaluation dashboard displaying average scores across sessions with distribution breakdown by score range (0.0–1.0)
>
> The evaluation dashboard transforms raw Amazon CloudWatch logs and OpenTelemetry traces into an actionable view of how your agent is actually performing (Figure 3). Instead of sifting through thousands of JSON log entries across multiple log groups to piece together what happened in a single session, the dashboard surfaces session timelines, span hierarchies, and evaluation scores in a visual interface. You can filter sessions by date range and drill into individual traces to see exactly where an agent spent time or encountered errors. You can also run on-demand evaluations against specific sessions with built-in or custom evaluators.
>
> Responsible AI safeguards
>
> Evaluators like Correctness and Faithfulness catch hallucinated or inaccurate outputs after the fact, but because online evaluation runs asynchronously on a sample of sessions, a problematic response can still reach the user before it’s scored. For production agent systems, Amazon Bedrock Guardrails provides a complementary inline layer that operates on every response before it’s returned. Key capabilities include content filtering to block harmful or inappropriate content, denied topic detection to help prevent agents from responding to out-of-scope queries (for example, medical or legal advice in an airline context), contextual grounding checks that flag responses not grounded in retrieved source material, and sensitive information redaction to mask PII such as credit card numbers or passport details that may surface in tool outputs.
>
> For a system like the airline reservation agent, these controls address real-time risks that asynchronous evaluation cannot: a model fabricating flight pricing that sounds plausible but wasn’t returned by any tool, an agent offering legal commitments about refund policies it has no authority to make, or PII from one customer’s profile leaking into another session. Where AgentCore Evaluations scores quality after the fact on a sample of sessions, Guardrails acts synchronously on every response, providing the real-time safety net that sampled evaluation alone cannot. Together they form a complete quality and safety posture: Guardrails help prevent harmful outputs from reaching users in the first place, while Evaluations identifies subtler quality regressions that accumulate over time.
>
> On-demand evaluation: development and CI/CD integration
>
> While online evaluation provides continuous monitoring, on-demand evaluation helps you investigate specific sessions: a user complaint, an edge case, or a session flagged by your monitoring. Production metrics operate on a sampling rate (typically 10 percent), so not every session gets scored. On-demand evaluation fills that gap, so you can evaluate a specific session against a selected evaluator at any time. Beyond the three default metrics (Helpfulness, Correctness, Goal Success Rate), Amazon Bedrock AgentCore provides a full catalog of built-in evaluators you can run on-demand as shown in Table 1.
>
> You can also create custom evaluators with your own scoring rubrics and instructions tailored to your domain. The dashboard surfaces these through the evaluators API, so you can browse what’s available and run combinations against individual sessions or in batch across multiple sessions (Figure 4). This makes on-demand evaluation the go-to tool for root cause analysis: when a production metric dips, you pick the problematic sessions and run targeted evaluators to understand exactly what went wrong.
>
> Figure 4: Viewing trace and span data and performing on-demand evaluation against a session’s trace, spans, and tool calls
>
> Workflow for on-demand evaluation:
>
> On-demand evaluation follows a synchronous workflow where you request evaluation of a specific session and receive immediate results with scores and explanations.
>
> Workflow diagram for on-demand evaluation
>
> The AI analysis engine: from scores to improvements
>
> After retrieving evaluation metrics, build an analysis layer that detects patterns in low-performing sessions, runs statistical analysis to separate systemic issues from isolated incidents, and generates concrete prompt improvements. This layer should apply:
>
> Unsupervised pattern detection to surface recurring failure modes across evaluation dimensions.
>
> Statistical analysis (frequency, correlation) to identify which failure patterns are systemic versus isolated.
>
> LLM-based reasoning to generate concrete prompt optimization recommendations grounded in production evidence.
>
> The AI Engine identifies common failure patterns: poor tool selection, missing context, or specific criteria that score low. Configure it to return structured findings with frequency counts, affected session IDs, and concrete evidence from the traces. For example, your engine

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。