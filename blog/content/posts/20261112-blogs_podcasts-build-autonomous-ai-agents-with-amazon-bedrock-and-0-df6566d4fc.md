---
title: "Build autonomous AI agents with Amazon Bedrock and Spring AI"
date: 2026-11-12T10:59:23+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "RAG", "AI Agent", "Prompt 工程", "Amazon Bedrock", "Expert (400)", "Technical How-to", "博客与播客"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:ccc49ca6ff0b732072d6e80dcc6ff869b3d16ad5221fac0b51ce29e28dde5153"
source_payload_sha256: "sha256:6fe46b6173e4f1ac4ae00592cfd3ad71563450bc0e3d8c6cfd2e23e7bbfe058a"
observation_id: obs_df6566d4fc91840890def19461933475d9c7a30723709bdf51469ad99565d346
event_id: evt_334f59cf098e7f637657ae0b8e4f421c7eb680e9141e248df31f58dce8db47f4
revision_id: rev_73a86100a569adc5f6a217250e88c0ba226953a4628f274263c337c44942c856
source_published_at: 2026-11-12T01:18:23Z
first_seen_at: 2026-11-12T02:57:51.825123Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: true
source_truncation_reason: "crawler_feed_content_limit"
source_support: 1.0
source_title_chars_original: 60
interpretation_sha256: "sha256:cbd803a92b6c5f8e337dc11708656f090daa9da5bb37c0730ab0317f1e6f4b82"
description: "这是一篇面向 Java 团队的实战指南，介绍如何结合 Spring AI 与 Amazon Bedrock 构建可规划任务、调用工具并保留上下文的自主 AI 智能体。示例涵盖单智能体旅行助手和多智能体文档处理系统。"
external_url: https://aws.amazon.com/blogs/machine-learning/build-autonomous-ai-agents-with-amazon-bedrock-and-spring-ai
parent_observation_id: null
last_seen_at: 2026-11-12T02:57:51.825123Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/build-autonomous-ai-agents-with-amazon-bedrock-and-spring-ai](https://aws.amazon.com/blogs/machine-learning/build-autonomous-ai-agents-with-amazon-bedrock-and-spring-ai)
- **发布域名**: aws.amazon.com

## 要点解读

### 这是什么
这是一篇面向 Java 团队的实战指南，介绍如何结合 Spring AI 与 Amazon Bedrock 构建可规划任务、调用工具并保留上下文的自主 AI 智能体。示例涵盖单智能体旅行助手和多智能体文档处理系统。

### 用在哪里
适合希望将 AI 智能体从原型投入生产，并已使用 Spring Boot、JVM 或 AWS 基础设施的团队。文中还给出了运行时、记忆、工具调用、可观测性及基础设施部署等生产实践模式。

### 可以推断的
- 推测：单智能体旅行助手更适合用于快速理解和验证智能体的基本能力。
- 推测：涉及规则分流、告警与人工复核的文档流程，可能更适合采用多智能体架构。

## 来源摘要/节选

> Java teams have established JVM tooling, continuous integration and continuous delivery (CI/CD) pipelines, and operational patterns, yet taking AI agents from prototype to production is hard: agent frameworks do not solve scalability, governance, security, and operational concerns by default. Amazon Bedrock and Spring AI close those gaps, so Java teams can build autonomous AI agents that plan, call tools and APIs, and maintain context across multi-turn conversations. Agentic AI is moving beyond prompt-response interactions toward autonomous systems that execute complex multi-step tasks.
>
> Java remains one of the widely used programming languages in enterprise software. Teams have existing CI/CD pipelines, operational expertise, and established patterns built around the JVM. Spring AI brings AI capabilities to the JVM through familiar Spring patterns: auto-configuration, dependency injection, and composable advisors. Developers can build AI agents using the same idioms they use for REST APIs, security, and data access.
>
> Amazon Bedrock AgentCore is a platform to build, connect, and optimize agents at scale, with any framework or model. With AgentCore, you can build, deploy, and operate AI agents at scale. It is framework-agnostic and model-agnostic: you bring your preferred agent framework and foundation model (FM). With AgentCore, you can access the production infrastructure you need: managed runtime, memory, browser automation, code execution, and identity management.
>
> In this post, we show you how to build autonomous AI agents in Java using Spring AI and Amazon Bedrock with spring-ai-agentcore. We explore the key implementation patterns for two systems. The first is a single-agent travel assistant that demonstrates tool calling and memory. The second is a multi-agent intelligent document processing (IDP) system that shows how specialist agents, a rules engine, and alerting work together.
>
> Prerequisites
>
> To follow along with this walkthrough, you need the following:
>
> Java – JDK 21 (required)
>
> Spring Boot – 4.1 (with Spring AI 2.0 and spring-ai-agentcore 2.0)
>
> Maven – 3.9+.
>
> Node.js – 18+ (for the React frontend)
>
> Terraform – 1.5+.
>
> Docker – with Buildx for multi-architecture builds.
>
> AWS Command Line Interface (AWS CLI) – v2, configured with credentials.
>
> An AWS account.
>
> What makes a system an agent
>
> A chat completion call can generate text, but it can’t decide what to do next, reach into external systems, or remember what happened yesterday. An agent can, because it unites three capabilities:
>
> Planning – Given a goal, the model breaks it into steps, prioritizes them, and revises the plan as new information arrives.
>
> Tool use – Beyond generating text, the model can select and invoke external functions such as APIs, databases, and code interpreters to act in the world.
>
> Memory – Context carries across turns (short-term) and across sessions (long-term), so each decision builds on what came before.
>
> A Retrieval Augmented Generation (RAG) application has limited tool use (retrieval) but no planning loop. An agent has all three, operating in a goal-directed loop until the task is complete or it determines it cannot proceed.
>
> The following diagram shows these capabilities in an end-to-end agentic pipeline, from request to grounded answer.
>
> Figure 1: Agentic reference architecture. A request flows through the runtime, guardrails, classification, a specialist agent, tools, the foundation model, memory, rules, and human review to a grounded answer, with resilience and observability as cross-cutting concerns
>
> The pipeline has 11 stages. A client submits a document and question. The request passes through a runtime gateway for authentication and rate limiting, then input guardrails screen for harmful content. A router classifies the document and routes it to a specialist agent, which plans its workflow and calls tools, the Amazon Bedrock foundation model, memory, and a rules engine as needed. Low-confidence or flagged results go to a human review queue before the grounded answer returns to the client. Resilience, observability, logging, and least-privilege AWS Identity and Access Management (IAM) apply across all stages.
>
> Solution overview
>
> The solution consists of two deployable systems that share common patterns:
>
> Travel agent – A single autonomous agent with tool calling (weather lookups, itinerary search), streaming responses, conversation memory, and resilience patterns. This is the recommended starting point.
>
> IDP multi-agent system – A multi-agent intelligent document processing platform with five specialist agents (Lawyer, Mortgage, Insurance, Tax, General), rules and workflow engine, alerting, and observability. This demonstrates production patterns at a scale.
>
> Both systems share the following architecture:
>
> Spring Boot application with Spring AI ChatClient, Spring AI agentcore and Amazon Bedrock Converse API.
>
> AgentCore runtime, a capability of Amazon Bedrock AgentCore, defines the contract (POST /invocations, GET /ping) for managed deployment.
>
> Conversation memory through AgentCore memory, a capability of Amazon Bedrock AgentCore, for both short-term and long-term context.
>
> Tool calling with @Tool annotated methods.
>
> Structured output mapped to Java records.
>
> ARM64 container image optimized for AWS Graviton.
>
> Modular Terraform for infrastructure provisioning.
>
> The travel assistant is the recommended starting point. The following diagram illustrates how a Spring Boot agent interacts with AgentCore runtime, tools, memory, and models available on Amazon Bedrock.
>
> Figure 2: Single-agent travel assistant. The Spring Boot application exposes both REST endpoints for the React UI and the AgentCore runtime contract, calling Amazon Bedrock through the Converse API while tool calling, streaming, and memory run inside one code base.
>
> The travel assistant runs a single Spring Boot application with two entry points, the /invocations and /ping contract required by AgentCore runtime. Spring AI orchestrates calls to Amazon Bedrock through the Converse API and resolves tool invocations locally inside the same process. Server-Sent Events stream tokens to the client as they are generated. AgentCore memory supplies both short-term context within a session and long-term context across sessions, so the agent retains conversation history without external state management.
>
> The following diagram shows the architecture for the IDP multi-agent system.
>
> Figure 3: IDP multi-agent system architecture. Specialist agents process documents through a shared ChatClient pattern, with results flowing through a rules engine and alert service.
>
> The IDP multi-agent system routes documents through five specialist agents (Lawyer, Mortgage, Insurance, Tax, and General), each built on a shared AbstractDocumentAgent template. A ClassifierAgent reads each document and forwards it to the appropriate specialist. The specialist extracts structured JSON with confidence scores using the multimodal Converse API of Amazon Bedrock. A rules engine evaluates Spring Expression Language (SpEL) expressions from application.yml against the extraction. ALERT or BLOCK severity rules dispatch through the AlertService. Low-confidence documents go to human review. Metrics, audit trail, resilience, and observability apply across all stages.
>
> Agent collaboration patterns
>
> When multiple agents work together, how they coordinate determines system behavior. This solution uses three patterns:
>
> The following diagram compares the three coordination patterns used in this solution.
>
> Figure 4: Agent collaboration patterns
>
> Three patterns shown side by side. The router dispatches each request to one specialist by document type. The evaluator passes specialist findings through a rules engine that applies to severity levels and dispatches alerts or blocks for human review. The parallel fan-out sends one request to multiple specialists concurrently and aggregates results before the rules engine runs.
>
> Router pattern: A lightweight orchestrator examines the incoming request and routes it to the appropriate specialist. In the IDP multi-agent system, the router inspects document type metadata and forwards it to the Lawyer, Mortgage, Insurance, Tax, or General agent. The router holds no domain logic. It is a dispatch layer only.
>
> Parallel fan-out (optional extension): The base solution implements the router and evaluator patterns. The batch endpoint processes documents sequentially. When a document needs several perspectives at once, you can add a parallel fan-out as a drop-in extension. Dispatch to specialists concurrently and aggregate their results before the rules engine runs. Wall-clock time for the combined analysis is then bounded by the slowest single agent call rather than the sum of all calls.
>
> Evaluator pattern: After specialists return their findings, a rules engine evaluates the combined output against configurable business rules. Rules that trigger ALERT or BLOCK severity dispatch through a pluggable AlertService for human review.
>
> Walkthrough
>
> The following sections walk you through the key implementation patterns, starting with the AgentCore runtime contract and progressing through tool calling, memory, resilience, and multi-agent orchestration.
>
> Fulfilling the AgentCore runtime contract
>
> Amazon Bedrock AgentCore runtime manages agent lifecycle and scaling. For current rates, see Amazon Bedrock AgentCore pricing and Amazon Bedrock pricing. The runtime routes incoming requests to your agent and monitors its health. Your agent must expose two endpoints:
>
> POST /invocations – Receives requests and returns responses as JSON or Server-Sent Events (SSE) streaming.
>
> GET /ping – Reports health status (Healthy or HealthyBusy). Long-running tasks must signal busy status, or the runtime might scale down the agent.
>
> The following diagram shows how the Spring AI developer model maps onto AgentCore runtime, Memory, Browser, Code Interpreter, and Evaluations.
>
> Figure 5: Spring AI AgentCore SDK on Amazon Bedrock AgentCore. Annotations, the ChatClient, tool callbacks, and advisors map through the spring-ai-agentcore SDK onto AgentCore runtime, AgentCore memory, AgentCore Browser, AgentCore Code Interpreter, and AgentCore Evaluations.
>
> Two layers connected by the spring-ai-agentcore SDK. The application layer uses Spring AI components: @AgentCoreInvocation for endpoint wiring, ChatClient for model interaction, @Tool callbacks, and advisors for memory and guardrails. The infrastructure layer provides AgentCore runtime, AgentCore memory, AgentCore Browser, AgentCore Code Interpreter, and AgentCore Evaluations, all capabilities of Amazon Bedrock AgentCore. The SDK bridges both, so developers write standard Spring AI code while AgentCore handles production infrastructure.
>
> With the Spring AI AgentCore SDK, a single annotation handles this contract automatically:
>
> @Service
>
> public class TravelAgent {
>
> private final ChatClient chatClient;
>
> public TravelAgent(ChatClient.Builder builder) {
>
> this.chatClient = builder.build();
>
> }
>
> @AgentCoreInvocation
>
> public Flux&lt;String&gt; chat(PromptRequest request) {
>
> return chatClient.prompt()
>
> .user(request.prompt())
>
> .stream()
>
> .content();
>
> }
>
> }
>
> The @AgentCoreInvocation annotation auto-configures the /invocations and /ping endpoints, handles JSON serialization, manages SSE framing for streaming responses, and reports health status. The same project also exposes REST endpoints for the React UI, so the agent serves both AgentCore runtime and a browser from one code base.
>
> A note on streaming: the preceding minimal example returns the model stream directly, which is ideal for a chat UI. When an agent makes multi-argument tool calls, assemble the response with a blocking call() and then chunk the result for streaming, so the tool arguments bind reliably. The travel assistant serves both the AgentCore runtime and the React UI from one service method:
>
> @RestController
>
> public class AgentController {
>
> private final AgentService agentService;
>
> public AgentController(AgentService agentService) {
>
> this.agentService = agentService;
>
> }
>
> // One annotation wires up POST /invocations + GET /ping, JSON/SSE framing, and health.
>
> @AgentCoreInvocation
>
> public Flux&lt;String&gt; invoke(PromptRequest request, AgentCoreContext context) {
>
> String sessionId = context.getHeader(AgentCoreHeaders.SESSION_ID);
>
> return agentService.streamChat(request.prompt(), sessionId,
>
> request.guardrailsEnabled(), request.memoryEnabled());
>
> }
>
> // The same app also serves the React UI from the same code base.
>
> @PostMapping(value = "/api/chat", produces = MediaType.TEXT_PLAIN_VALUE + ";charset=UTF-8")
>
> public Flux&lt;String&gt; chatStream(@Valid @RequestBody PromptRequest request) {
>
> return agentService.streamChat(request.prompt(), request.sessionId(),
>
> request.guardrailsEnabled(), request.memoryEnabled());
>
> }
>
> }
>
> Implementing tool calling
>
> With tool calling, the model can invoke external functions during reasoning. In Spring AI, you annotate a method with @Tool and the model decides when to call it and with what arguments:
>
> @Tool(description = "Get a short weather forecast for a city")
>
> public String getWeather(
>
> @ToolParam(description = "City name") String city) {
>
> return forecastService.lookup(city);
>
> }
>
> You register tools on the ChatClient, and the model decides when to call them:
>
> ChatClient chatClient = chatClientBuilder
>
> .defaultSystem(properties.getSystemPrompt())
>
> .defaultTools(new DateTimeTools(), new TravelTools())
>
> .build();
>
> For structured output, request a Java record type. For multimodal input, attach media to the user message:
>
> ProcessedDocument review = chatClient.prompt()
>
> .system(personaSystemPrompt)
>
> .user(u -&gt; u.text(question).media(mimeType, fileResource))
>
> .call()
>
> .entity(ProcessedDocument.class);
>
> Note: We verified this example with Anthropic Claude Sonnet 4.5 on Amazon Bedrock. Spring AI adds the record’s schema to the prompt and parses the reply back into the Java type. Behavior can differ for other model families, so refer to the Spring AI structured output documentation and the Amazon Bedrock documentation for current support. It is best-effort, meaning that models can occasionally return output that does not match the schema. For stricter results, use a provider with native schema enforcement or Spring AI validation and retry.
>
> The model receives the tool definitions as part of its context, reasons about when a tool call would help satisfy the user request, and returns a structured tool call response. Spring AI intercepts this, invokes the annotated method, and feeds the result back to the model for further reasoning.
>
> Adding conversation memory
>
> Real-world agents must remember what users said earlier in a conversation (working memory) and what they have learned over time (persistent memory). The Spring AI AgentCore SDK integrates with AgentCore memory through the advisor pattern: interceptors that enrich prompts with context before they reach the model.
>
> chatClient.prompt()
>
> .advisors(agentCoreMemory.advisors)
>
> .advisors(a -&gt; a.param(
>
> ChatMemory.CONVERSATION_ID, "user:" + sessionId))
>
> .user(prompt)
>
> .stream()
>
> .content();
>
> The session ID becomes a conversation ID in actor:session form, so each user’s history stays isolated. For user-facing deployments, derive the actor from a verified OAuth 2.0 (JWT) identity rather than a client-supplied value, so users cannot access one another’s history.
>
> In addition, AgentCore memory offers long-term memory support, employing the following strategies to identify and capture key insights from conversations:
>
> Semantic – Factual information about users (for example, “User works in finance”)
>
> User preference – Explicit settings and choices (for example, “Metric units preferred”)
>
> Summary – Condensed conversation history for continuity across sessions.
>
> Episodic – Past interactions and lessons learned.
>
> Long-term memory extraction is asynchronous and optional. You choose which strategies to enable when you create the memory, and AgentCore extracts and consolidates records in the background after each conversation, so it never blocks the agent’s response. Choose strategies by workload: use user preference for the travel assistant so it remembers units and seating choices. Use summary when sessions span many turns. Use episodic when the agent should reuse lessons from past tasks. And use semantic to retain durable facts about the user.
>
> Configuring the rules engine
>
> Reading a document is only half the job. Acting on what it finds is the other half. The IDP multi-agent system includes a rules engine so operators can add business checks without touching code. This is an in-process rules evaluator that applies SpEL conditions to extraction results, not a workflow orchestration service such as AWS Step Functions. Rules live in application.yml and each condition is a SpEL expression evaluated against the extraction:
>
> idp:
>
> review:
>
> enabled: ${REVIEW_ENABLED:true}
>
> confidence-threshold: ${REVIEW_CONFIDENCE_THRESHOLD:0.7}
>
> rules:
>
> - id: legal-unsigned
>
> agentType: LAWYER
>
> condition: "field('signaturePresent') == 'false' || missing('signaturePresent')"
>
> severity: ALERT
>
> message: "Document appears unsigned; get all parties to sign before relying on it."
>
> - id: mortgage-high-dti
>
> agentType: MORTGAGE
>
> condition: "field('dtiRatio') != '' &amp;&amp; T(java.lang.Double).parseDouble(field('dtiRatio')) &gt; 0.43"
>
> severity: WARN
>
> message: "Debt-to-income ratio exceeds 0.43; likely needs manual underwriting."
>
> - id: low-confidence
>
> agentType: ALL
>
> condition: "confidence &lt; 0.6"
>
> severity: WARN
>
> message: "Low extraction confidence; consider human verification."
>
> Severity levels control the engine’s behavior. INFO and WARN are logged, while ALERT dispatches through a pluggable AlertService. The default logs and emits a metric, but you can substitute Amazon Simple Notification Service (Amazon SNS), Slack, or email by providing your own bean. BLOCK holds the document for manual review. Because rules are operator configuration rather than end user input, they provide a safe and auditable extension point. Adding new workflows is a configuration change, not a deployment.
>
> The evaluator pattern is implemented by the rules engine and a pluggable AlertService. The default implementation logs the alert and emits a metric. You provide your own bean to route to Amazon SNS, Slack, or email:
>
> public class LoggingAlertService implements AlertService {
>
> @Override
>
> public void send(RuleResult result, AgentType agentType, ProcessedDocument document) {
>
> registry.counter("idp.alerts.sent",
>
> "severity", result.severity().name(), "type", agentType.name()).increment();
>
> logger.warn("ALERT [{}] rule={} type={} message=\"{}\"",
>
> result.severity(), result.ruleId(), agentType, result.message());
>
> }
>
> }
>
> Production readiness patterns
>
> The following patterns address common production requirements that prototypes typically skip.
>
> Resilience
>
> Every model call uses a Resilience4j retry with exponential backoff, a circuit breaker that fails fast when model calls repeatedly fail or time out, and a timeout. Streaming paths emit a fallback message instead of a raw error. When traffic exceeds your account and Region service quotas, AgentCore runtime returns HTTP 429 and the retry handles it. For current limits, see the Amazon Bedrock AgentCore quotas documentation.
>
> Twelve-factor configurations
>
> Every configurable value (Region, model ID, memory ID, timeouts, rate limits, system prompt) is an environment variable bound to a typed @ConfigurationProperties class. The application is stateless, starts fast, drains in-flight turns on scale-down, and ships as one immutable ARM64 image promoted unchanged from development to production.
>
> Security and identity
>
> The Agentcore runtime uses AWS Identity and Access Management (IAM) authentication by default. For user-facing agents, add an OAuth 2.0 (JWT) authorizer (such as Amazon Cognito) and derive the memory actor ID (actorId) from the verified identity. The IAM execution role follows least privilege:
>
> Amazon Elastic Container Registry (Amazon ECR) pull.
>
> Scoped Amazon CloudWatch Logs and AWS X-Ray.
>
> Amazon Bedrock InvokeModel actions.
>
> Scoped workload access tokens (GetWorkloadAccessTokenForJWT) for the agent’s workload identity.
>
> AgentCore memory actions limited to the specific Memory resource ARN.
>
> AgentCore Gateway, a capability of Amazon Bedrock AgentCore, enforces inbound authentication (acting as an OAuth 2.0 resource server that validates JWT bearer tokens through Cognito, Okta, Auth0, or your own OIDC provider) and supports configurable rate limiting at the gateway layer. Rate limits are fail-open by default, so they should complement your core security controls rather than replace them.
>
> Responsible AI controls
>
> Autonomous agents that take real-world actions need safety controls as a first-class concern. The sample ships with a stand-in demonstration of a lightweight in-process pre-check called GuardrailService. This service screens prompts for disallowed intent and prompt injection, toggled per request with the guardrailsEnabled flag. Production deployments use Amazon Bedrock Guardrails as a standard control applied to every request, not a per-request toggle.
>
> To upgrade the demo service for production, front the agent with Amazon Bedrock Guardrails. Guardrails apply configurable policies outside the model call, covering both input and output:
>
> Content filtering. Blocks harmful or off-topic content based on configurable thresholds for both prompts and responses.
>
> Denied topics. Prevents the agent from engaging with topics you define as out-of-scope.
>
> Sensitive information filters. Detects and redacts PII in both prompts and responses, supporting requirements such as GDPR and HIPAA.
>
> For agents that retrieve external knowledge, enable grounding checks to reduce hallucination risk before the agent acts on tool calls with real-world side effects.
>
> To wire Bedrock Guardrails into Spring AI, implement CallAdvisor and StreamAdvisor functions that call the ApplyGuardrail API and register it with defaultAdvisors on the ChatClient. Because policies live in the guardrail, security teams can update filters independently of the application release cycle.
>
> Observability
>
> The example instruments with the Micrometer Observation API (@Observed), producing timers that become distributed trace spans when you add a tracing bridge (OTLP to AWS X-Ray). The system emits domain metrics:
>
> idp.documents.processed{type,status}
>
> idp.extraction.confidence{type}
>
> idp.alerts.sent{severity,type}
>
> idp.processing.duration{type}
>
> These metrics are exposed through /actuator/prometheus. The application also emits structured JSON logs to standard output, which Amazon Bedrock AgentCore runtime captures in Amazon CloudWatch Logs.
>
> Optional extension that’s not implemented in this post: The sample includes the Micrometer OpenTelemetry bridge and OTLP exporter dependencies, but this post’s deployment does not provision an OpenTelemetry collector or enable trace sampling. You can add distributed tracing by setting a nonzero TRACING_SAMPLING value, pointing OTLP_TRACES_ENDPOINT to an OpenTelemetry or AWS Distro for OpenTelemetry collector, and configuring the collector to forward traces to AWS X-Ray.
>
> Optional extension that’s not implemented in this post: The sample doesn’t implement an automated evaluation or optimization feedback loop. You can add one by persisting application metrics, traces, audit events, and human-review outcomes as an evaluation dataset. AgentCore evaluations or a separate evaluation pipeline can then compare versioned prompts, models, tools, and routing rules against quality, safety, latency, and cost thresholds. Promote changes only after evaluation and human approval.
>
> Deploying the solution
>
> This GitHub repository contains two AI agent applications demonstrating different use cases for autonomous AI. This guide shows you how to deploy them to AWS using Amazon Bedrock AgentCore runtime.
>
> The following diagram shows the deployment architecture: a single Arm64 image promoted through modular Terraform to the AgentCore runtime, with an optional Amazon Elastic Kubernetes Service (Amazon EKS) path.
>
> Optional: running on Amazon EKS. Teams already standardized on Kubernetes can run the same Arm64 image on Amazon EKS, using their existing cluster for scaling and health checks against the /ping endpoint, with IAM Roles for Service Accounts (IRSA) for scoped, least-privilege pod-level access to Amazon Bedrock and AgentCore

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。