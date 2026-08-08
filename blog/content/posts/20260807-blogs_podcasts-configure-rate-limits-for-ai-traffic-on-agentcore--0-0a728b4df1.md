---
title: "Configure rate limits for AI traffic on AgentCore gateway"
date: 2026-08-07T11:18:52+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "Advanced (300)", "Amazon Bedrock AgentCore", "Announcements", "博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:830e2bb7285ed0c2fb9bc2e413d0f5a5abf64aad795aa125457537b783f784be"
source_payload_sha256: "sha256:2eca273a02337f330f03fc5d7c4e746ed957ebd7ea3710424dd91156d4b7f98d"
observation_id: obs_0a728b4df1ea2e24ba1c82d26b599c97bdb14f7c45ec405936ae9072a6839848
event_id: evt_1a916f1761e439b7556a7faeb14f00d7b9db3f4ae2cd4d75060208fe4ca9d06a
revision_id: rev_54a9e80414fabfcab8dfa7348e6ecf619d2a9e5227d96730ae5250335dee97bc
source_published_at: 2026-08-06T17:50:42Z
first_seen_at: 2026-08-07T03:27:19Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: true
source_truncation_reason: "crawler_feed_content_limit"
source_support: 1.0
source_title_chars_original: 57
interpretation_sha256: "sha256:a6e5754ce7d25564da2950db5d6bad7a5cd4e552219b00a215afd1eb0fdab06c"
description: "本文说明在托管 AI 网关上为流量设置速率限制的方案，支持按用户、目标或令牌维度进行细粒度管控。"
external_url: https://aws.amazon.com/blogs/machine-learning/configure-rate-limits-for-ai-traffic-on-agentcore-gateway
parent_observation_id: null
last_seen_at: 2026-08-08T00:00:00Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/configure-rate-limits-for-ai-traffic-on-agentcore-gateway](https://aws.amazon.com/blogs/machine-learning/configure-rate-limits-for-ai-traffic-on-agentcore-gateway)
- **发布域名**: aws.amazon.com

## 要点解读

### 这是什么
本文说明在托管 AI 网关上为流量设置速率限制的方案，支持按用户、目标或令牌维度进行细粒度管控。

### 用在哪里
适用于需要在多租户或分层用户环境中保护下游服务的技术人员，可通过身份认证信息和策略对请求、连接和令牌使用量进行限制。

### 可以推断的
推测：速率限制的效果取决于网关能够获取的请求上下文，如用户标识和目标名称，这些信息在配置时需保持可用。  
推测：仅在调用模型推理时会涉及令牌速率限制，而对 MCP 服务器或 HTTP 直通目标的限制主要体现在请求速率或并发连接数上。

## 来源摘要/节选

> Amazon Bedrock AgentCore gateway is a fully managed, serverless AI gateway that provides a single, secure entry point for AI traffic. AgentCore gateway routes traffic to tools such as managed web search, managed knowledge bases, MCP servers, inference models (LLMs), agents (A2A, agents as tools, etc.), or HTTP endpoint. Today, we are announcing support for rate limiting on AgentCore gateway, giving you fine-grained control over how much traffic individual users can consume through your gateway.
>
> Rate limiting in AgentCore gateway gives you per-user control over how users consume your tools, inference models, and agents. Define OAuth or IAM-based rules for requests per minute, concurrent connections, and token throughput, making sure downstream services remain available under heavy traffic spikes.
>
> Centralized rate limiting for AI traffic with AgentCore gateway
>
> AgentCore gateway provides three target types: MCP targets, inference targets, and HTTP passthrough targets. The following rate limiting metrics are supported on the targets.
>
> Request rate limits, measured in requests per second (RPS) and requests per minute (RPM), apply to all target types. Each limit defines a maximum count of requests permitted within the given time window, and the gateway measures every incoming request against it. A request counts as exactly one unit toward the configured limit, regardless of how long it takes to complete, a request that finishes in 50 milliseconds and one that streams for 90 seconds each consume exactly one unit from the per-second or per-minute limit.
>
> Token rate limits, measured in tokens per minute (TPM), apply to inference targets only. Token rate limiting accounts for both input tokens and output tokens. The full round-trip token cost of a request counts against the limit. AgentCore gateway uses a general-purpose tokenizer to estimate the incoming tokens for a request and deducts it from the rate-limit bucket upfront before the gateway dispatches the inference call. Once the inference call returns a response, which includes actual input and output token usage reported by the model provider, the gateway reconciles the limit by accounting for the true token consumption.
>
> Connection rate limits, measured in connections per second (CPS), apply to all target types. Unlike request rate limits, connection rate limiting tracks how long each request holds an open connection. For example, if a streaming inference call takes 100 seconds to complete, that request consumes one connection slot for the entire duration. CPS provides an additional mechanism for protecting targets against long-lived concurrent sessions particularly useful when you need to cap how many simultaneous connections a target sustains, rather than how many requests arrive in each window.
>
> For this use case, assume three user groups: Basic, Advanced, and Beta. AgentCore Identity handles inbound authentication using JSON Web Tokens (JWT) with Microsoft Entra ID as the identity provider and also serves as the token vending service for outbound targets. Policy in Amazon Bedrock AgentCore enforces role-based access control (RBAC), scoping each group’s access to specific targets and models. The following diagram illustrates this configuration.
>
> Figure 1: AgentCore gateway rate limiting architecture with user groups, identity, and policy enforcement
>
> Basic users operate under more restrictive rate limits than Advanced users, while Beta users receive elevated limits on restricted models, enabling the organization to benchmark performance and suitability before rolling these models out to the broader organization. Before setting up rate limits for each user-group, review the rate limit structure.
>
> Rate limit structure
>
> A rate limit configuration consists of two parts: dimension keys and entries. Dimension keys define how the gateway groups incoming traffic into rate buckets. Entries define the allowed throughput for each bucket.
>
> In this post, we use the AWS Command Line Interface (AWS CLI) to create the rate limit configuration. The following example demonstrates the relationship between dimension keys and entries. This rate limit uses targetName as the dimension key and defines two entries: a specific entry for the Booking target (MCP server), a high-traffic target, at 100 requests per second, and a wildcard entry that applies 10 requests per second individually to each remaining target, meaning every other target receives its own 10 RPS bucket.
>
> Figure 2: Rate limit structure with dimension keys and entries
>
> Dimension keys define how the gateway groups traffic into rate buckets. When a request arrives, the gateway resolves each dimension key to its value from the request context and uses the resulting combination to assign the request to the correct rate bucket. AgentCore gateway supports the following dimension keys: targetName, toolName, qualifiedModelId, $.context.jwt.&lt;claim&gt;, $.context.iam.principal, and $.context.iam.sourceIdentity. We will explore each of these through examples in the sections that follow.
>
> Entries are the rules within a rate limit. Each entry specifies a set of dimension keys to match, and the allowed throughput for that match. Entries support the special catch-all default value * that gives each distinct value its own independent bucket at the configured rate. When the gateway evaluates a request, it checks whether an entry matches by name before falling back to the wildcard. A named entry takes precedence because it refers to the value explicitly rather than relying on the catch-all.
>
> Taking the preceding rate limit as an example, when a request arrives for the Booking target (MCP server), the gateway matches the first entry and allows up to 100 RPS. This entry takes precedence because the most specific value match wins over default value * as it refers to the Booking target by name. For any other target, no named entry exists, so the gateway falls back to the wildcard entry and allows up to 10 requests per second. Each target that matches the wildcard (Docs, BedrockMantle, CustomPlatform, and awsdocsagent) gets its own independent bucket.
>
> You can combine multiple dimension keys for more granular control. For example, dimensionKeys: [“targetName”, “$.context.jwt.role”] groups traffic by both target and caller identity role claim, giving each user-group (Basic, Advanced, or Beta in the preceding example) their own independent rate bucket per target.
>
> Types of rate limits and example configurations
>
> AgentCore gateway enforces two layers of rate limiting: customer-defined rate limits and Service Quotas. Customer-defined rate limits are evaluated first. If the request passes, service quotas are evaluated. The following sections explain service quotas and the different types of customer-defined rate limits.
>
> Service managed quotas.
>
> These are the limits enforced on AgentCore gateway per AWS account by the service. Service managed quotas define the ceiling that customer-defined rate limits cannot exceed. The effective rate for requests is the minimum of the customer-defined limit and the service-managed limit. You can request increases for some quotas using the Service Quotas console.
>
> Customer-defined user limits.
>
> User-level limits use $.context.jwt.&lt;claim&gt;, $.context.iam.principal, and $.context.iam.sourceIdentity as the dimension keys to control how much traffic individual users or entire user-group can consume. These limits enforce fair usage across your caller base and prevent any single caller from monopolizing gateway capacity. The following example assigns different request rates per user group. The JWT role claim is an array, so each unique combination requires its own entry.
>
> aws bedrock-agentcore-control create-gateway-rate-limit \
>
> --gateway-identifier my-gateway-abc1234567 \
>
> --dimension-keys '["$.context.jwt.role"]' \
>
> --description "Per-role request and connection limit" \
>
> --entries '[
>
> {
>
> "dimensions": {"$.context.jwt.role": "[\"Basic\"]"},
>
> "requests": [{"rate": 100, "period": "minute"}],
>
> "connections": [{"rate": 50, "period": "second"}]
>
> },
>
> {
>
> "dimensions": {"$.context.jwt.role": "[\"Advanced\"]"},
>
> "requests": [{"rate": 300, "period": "minute"}],
>
> "connections": [{"rate": 150, "period": "second"}]
>
> },
>
> {
>
> "dimensions": {"$.context.jwt.role": "[\"Advanced\", \"Beta\"]"},
>
> "requests": [{"rate": 300, "period": "minute"}],
>
> "connections": [{"rate": 200, "period": "second"}]
>
> },
>
> {
>
> "dimensions": {"$.context.jwt.role": "*"},
>
> "requests": [{"rate": 80, "period": "minute"}],
>
> "connections": [{"rate": 10, "period": "second"}]
>
> }
>
> ]'
>
> In this configuration, Basic users receive two buckets, 100 RPM and 50 CPS, meaning every request from any Basic user counts toward the same 100 RPM total, and every connection counts toward the same 50 CPS total. If one Basic user sends 80 requests in a minute, only 20 remain for all other Basic users in that window. Advanced users receive their own two buckets at 300 RPM and 150 CPS, governed by the same collective behavior. Users with [“Advanced”, “Beta”] group membership receive two buckets at 300 RPM and 200 CPS. The higher connection allowance accommodates their streaming-heavy benchmarking workloads.
>
> However, within a group, a single user can still consume the entire group rate bucket, throttling everyone else in that group. For example, one Basic user sending 100 requests in a minute would leave zero capacity for all other Basic users. To prevent this, we create the following rate limit configuration as well.
>
> aws bedrock-agentcore-control create-gateway-rate-limit \
>
> --gateway-identifier my-gateway-abc1234567 \
>
> --dimension-keys '["$.context.jwt.role", "$.context.jwt.sub"]' \
>
> --description "Per-user request and connection limit within each role" \
>
> --entries '[
>
> {
>
> "dimensions": {"$.context.jwt.role": "[\"Basic\"]", "$.context.jwt.sub": "*"},
>
> "requests": [{"rate": 20, "period": "minute"}],
>
> "connections": [{"rate": 10, "period": "second"}]
>
> },
>
> {
>
> "dimensions": {"$.context.jwt.role": "[\"Advanced\"]", "$.context.jwt.sub": "*"},
>
> "requests": [{"rate": 60, "period": "minute"}],
>
> "connections": [{"rate": 30, "period": "second"}]
>
> },
>
> {
>
> "dimensions": {"$.context.jwt.role": "[\"Advanced\", \"Beta\"]", "$.context.jwt.sub": "*"},
>
> "requests": [{"rate": 60, "period": "minute"}],
>
> "connections": [{"rate": 50, "period": "second"}]
>
> },
>
> {
>
> "dimensions": {"$.context.jwt.role": "*", "$.context.jwt.sub": "*"},
>
> "requests": [{"rate": 20, "period": "minute"}],
>
> "connections": [{"rate": 20, "period": "second"}]
>
> }
>
> ]'
>
> With this configuration, each individual user is capped at their own rate regardless of how many users exist in their group. The $.context.jwt.sub claim from the JWT uniquely identifies each user, enabling the gateway to track and enforce limits at the individual level. Even if the group-level limit allows 100 RPM total for Basic, no single user can consume more than 20 RPM and 10 CPS of that shared pool. The same logic applies to Advanced and Beta users at their respective individual caps. Together, the per-group limit and the per-user limit create a two-layer enforcement model: the group ceiling helps prevent one group from starving another, and the per-user ceiling helps prevent one individual from starving their peers within the same group.
>
> Both rate limits are evaluated independently using AND semantics. A request must pass both the group-level limit and the per-user limit to proceed. If either check denies the request, the gateway returns a throttling response. For example, if Arnav (Basic) has consumed 20 RPM individually, his next request is denied by the per-user limit even though the Basic group still has 80 RPM of remaining capacity. Conversely, if the Basic group has collectively consumed 100 RPM, all Basic users are throttled regardless of their individual consumption.
>
> Customer defined target-level limits.
>
> Target-level limits use targetName, qualifiedModelId, or toolName as the dimension key to control throughput to specific downstream targets, models, or tools. These limits protect backend capacity and distribute load across your target resources. The following example limits traffic on a per-target basis.
>
> aws bedrock-agentcore-control create-gateway-rate-limit \
>
> --gateway-identifier my-gateway-abc1234567 \
>
> --dimension-keys '["targetName"]' \
>
> --description "Per-target rate limit" \
>
> --entries '[
>
> {
>
> "dimensions": {"targetName": "Booking"},
>
> "requests": [{"rate": 20, "period": "second"}]
>
> },
>
> {
>
> "dimensions": {"targetName": "Docs"},
>
> "requests": [{"rate": 15, "period": "second"}]
>
> },
>
> {
>
> "dimensions": {"targetName": "awsdocsagent"},
>
> "requests": [{"rate": 10, "period": "second"}],
>
> "connections": [{"rate": 60, "period": "second"}]
>
> },
>
> {
>
> "dimensions": {"targetName": "BedrockMantle"},
>
> "tokens": [{"rate": 100000, "period": "minute"}],
>
> "connections": [{"rate": 250, "period": "second"}]
>
> },
>
> {
>
> "dimensions": {"targetName": "CustomPlatform"},
>
> "tokens": [{"rate": 50000, "period": "minute"}],
>
> "connections": [{"rate": 100, "period": "second"}]
>
> },
>
> {
>
> "dimensions": {"targetName": "*"},
>
> "tokens": [{"rate": 10000, "period": "minute"}],
>
> "requests": [{"rate": 10, "period": "second"}],
>
> "connections": [{"rate": 50, "period": "second"}]
>
> }
>
> ]'
>
> You can also use qualifiedModelId to set connection rate limits (CPS) per model, or toolName to set request rate limits (RPS) per individual tool such as Booking___bookTool or Docs___searchDocsTool.
>
> Note: We exclude customer-defined target-level rate limits from our use-case configuration. Beta users run heavy benchmarking workloads against restricted models, consuming a disproportionate share of a shared target-level limit. Because this limit dimensions only on targetName, all users share a single ceiling, meaning high traffic from one group or individual can starve everyone else on that target. When a subset of users is expected to dominate token or connection consumption on a specific target, scope the limit by identity instead (for example, [“targetName”, “$.context.jwt.role”]). See the following example.
>
> Customer defined target-user level limits.
>
> Hybrid limits combine target and user dimensions in a single rate limit configuration, giving you the most granular control. Using multi-dimension keys, you can scope rate limits to a specific user or user group on a specific target, model, or tool.
>
> The following example enforces token limits at the model level, scoped to each user within their group. The qualifiedModelId dimension is the fully qualified model identifier for inference targets. It uniquely identifies the model being invoked (see documentation).
>
> aws bedrock-agentcore-control create-gateway-rate-limit \
>
> --gateway-identifier my-gateway-abc1234567 \
>
> --dimension-keys '["$.context.jwt.role", "qualifiedModelId", "$.context.jwt.sub"]' \
>
> --description "Per-user per-role per-model TPM and access limit" \
>
> --entries '[
>
> {
>
> "dimensions": {"$.context.jwt.role": "[\"Advanced\", \"Beta\"]", "qualifiedModelId": "anthropic.claude-fable-5", "$.context.jwt.sub": "*"},
>
> "tokens": [{"rate": 80000, "period": "minute"}]
>
> },
>
> {
>
> "dimensions": {"$.context.jwt.role": "[\"Basic\"]", "qualifiedModelId": "anthropic.claude-fable-5", "$.context.jwt.sub": "*"},
>
> "requests": [{"rate": 0, "period": "second"}]
>
> },
>
> {
>
> "dimensions": {"$.context.jwt.role": "[\"Advanced\"]", "qualifiedModelId": "anthropic.claude-fable-5", "$.context.jwt.sub": "*"},
>
> "requests": [{"rate": 0, "period": "second"}]
>
> },
>
> ... (repeat for openai.gpt-5.6-luna and openai.gpt-5.6-terra)
>
> {
>
> "dimensions": {"$.context.jwt.role": "[\"Advanced\"]", "qualifiedModelId": "*", "$.context.jwt.sub": "*"},
>
> "tokens": [{"rate": 40000, "period": "minute"}]
>
> },
>
> {
>
> "dimensions": {"$.context.jwt.role": "[\"Basic\"]", "qualifiedModelId": "*", "$.context.jwt.sub": "*"},
>
> "tokens": [{"rate": 20000, "period": "minute"}]
>
> }
>
> ]'
>
> In this configuration, anthropic.claude-fable-5 is a restricted model. Only users with the [“Advanced”, “Beta”] role can invoke it, receiving 80,000 TPM per user for benchmarking and evaluation workloads. Both [“Basic”] and [“Advanced”] users are blocked* from invoking this model with a rate of zero. The same pattern applies to other restricted models (openai.gpt-5.6-luna and openai.gpt-5.6-terra), make sure to add entries following the same structure for each. For generally available models, Basic users receive 20,000 TPM per user while Advanced users receive 40,000 TPM per user through wildcard entries.
>
> Specific entries take precedence over wildcards following the most-specific-match-wins rule. When María (sub: “María”, role: [“Advanced”, “Beta”]) invokes anthropic.claude-fable-5, the gateway matches the explicit entry and applies 80,000 TPM scoped to María individually. If María exhausts 80,000 TPM limit, other Beta users remain unaffected because * on $.context.jwt.sub gives each user their own isolated bucket. When John (sub: “John”, role: [“Advanced”]) attempts anthropic.claude-fable-5, the gateway matches the explicit [“Advanced”] entry for that model, which sets requests to zero blocking the call. When John invokes a generally available model like anthropic.claude-sonnet-5, no explicit entry exists for that model-role combination, so the gateway falls through to the wildcard entry for [“Advanced”] and applies 40,000 TPM. When Arnav (sub: “Arnav”, role: [“Basic”]) invokes the same generally available model, he receives 40,000 TPM through the Basic wildcard entry.
>
> You can also combine dimensions such as [“$.context.jwt.role”, “targetName”] for per-role per-target request limits, [“$.context.jwt.sub”, “targetName”] for per-user per-target combined request and token limits, or [“$.context.jwt.role”, “toolName”] for per-role per-tool request limits. For more rate limiting configurations, see Rate limit API examples.
>
> Rate limits for agentic workloads
>
> Consider the following AgentCore gateway configuration where a user invokes the AWS Documentation Agent. The agent uses two downstream resources through the gateway: the Docs MCP target for document search and retrieval, and the BedrockMantle inference target for reasoning through the anthropic.claude-sonnet-5 model. The following architecture shows this:
>
> Figure 3: Agentic workload rate limiting with downstream resource consumption
>
> There are two types of rate limits to consider for agentic workloads:
>
> Rate limits on agent invocation.
>
> The first type protects how frequently users or other services can invoke the agent. These are request (RPM) and connection (CPS) limits scoped to the agent target itself. At the simplest level, you can dimension on targetName alone, for example, {“targetName”: “awsdocsagent”}, so that all users share a single invocation ceiling. For more granular control, pair targetName with user dimensions such as [“targetName”, “$.context.jwt.role”] or [“targetName”, “$.context.jwt.role”, “$.context.jwt.sub”] to cap how often each user group or individual user can invoke the agent.
>
> Rate limits on resources consumed by the agent.
>
> The second type protects the downstream resources the agent consumes on each invocation. AWS Documentation Agent triggers multiple downstream requests. The agent calls the Docs MCP target for document retrieval and the BedrockMantle target for inference. How you rate limit these downstream calls depends on how the agent authenticates with the gateway when invoking those resources.
>
> If the agent performs an on-behalf-of (OBO) token exchange based on the user’s incoming JWT token, then the downstream requests carry the original user’s identity. All existing user-based rate limits apply. The per-role and per-user limits you configured previously will enforce on the agent’s downstream calls as if the user made them directly.
>
> However, if the agent performs a machine-to-machine grant to obtain a new token (for example, a client credentials flow), the downstream requests carry the agent’s own identity rather than the caller’s. In this case, the user-based rate limits will not match the user’s claims. You should add rate limits that identify the agent itself, based on your identity provider, use a claim that uniquely identifies the agent, such as $.context.jwt.azp (authorized party), and limit accordingly to prevent a single agent from exhausting shared resources.
>
> Rate limiting best practices
>
> Follow these best practices when creating rate limits with AgentCore gateway:
>
> If you are using Policy in AgentCore to enforce RBAC authorization, it is important to understand the evaluation order. Rate limits are applied first; AgentCore Policy is evaluated after. This means that even if a user or role is ultimately denied access by AgentCore Policy, their request still consumes the rate limit bucket before that denial occurs. To avoid this consumption, create a rate limit entry that explicitly assigns a rate of zero to users or groups that AgentCore Policy would block, this makes sure the request is rejected at the rate limit layer without depleting the budget available to authorized callers.
>
> The gateway evaluates rate limits with more dimension keys first (more specific limits take priority). Within the same number of dimensions, the gateway evaluates rate limits with tighter (lower) rates first. Evaluation short-circuits on the first denial, meaning the gateway does not evaluate remaining rate limits once a request is denied. Design your rate limit configuration so that your tightest limits live at the highest-dimension level (for example, the three-key [“$.context.jwt.role”,“qualifiedModelId”,“$.context.jwt.sub”] limit).
>
> Two rate limits with same dimension key but with different orders cannot be created. For example, you cannot create a rate limit with [“$.context.jwt.role”, “qualifiedModelId”, “$.context.jwt.sub”] and [“qualifiedModelId”, “$.context.jwt.role”, “$.context.jwt.sub”] dimension key on the same gateway. However, the order of the dimension key matters. When a rate limit has multiple dimension keys, the order you declare them determines how wildcards can be used. The catch all default * can only appear in trailing positions. If you use * at position N, all subsequent positions must also be *. This trailing-only constraint facilitates predictable matching behavior. To understand this behavior, see examples.
>
> Avoid using high-cardinality or unbounded JWT claims as dimension keys (for example, $.context.jwt.jti, $.context.jwt.nonce, or request IDs). These create an unbounded number of rate buckets, and may reduce the effectiveness of rate limiting. Use stable, bounded identifiers such as sub, role, team, or tier instead.
>
> The gateway uses fail-open semantics for rate limit evaluation. Because of fail-open behavior, do not rely solely on rate limits as a security boundary. Use rate limits for traffic management and quality of service, and use authentication, authorization, and AWS WAF rules for security enforcement.
>
> Enable application logs on your AgentCore gateway. This gives you access to rate limiting logs. The gateway emits OpenTelemetry (OTEL) span attributes on the server span for every request where customer rate limits are evaluated. Use these attributes for debugging and monitoring.
>
> Make sure to include a catch-all entry, consider a gateway with a single rate limit for simplicity:
>
> aws bedrock-agentcore-control create-gateway-rate-limit \
>
> --gateway-identifier my-gateway-abc1234567 \
>
> --dimension-keys '["$.context.jwt.sub"]' \
>
> --description "Per-sub request limit" \
>
> --entries '[
>
> {
>
> "dimensions": {"$.context.jwt.sub": "Arnav"},
>
> "requests": [{"rate": 100, "period": "minute"}]
>
> }
>
> ]'
>
> In this configuration, only Arnav has an explicit entry. If John ($.context.jwt.sub: “John”) invokes the gateway, the request does not match any entry, the rate limit is effectively skipped, and John falls through to service-managed quotas with no customer-defined enforcement. Adding a wildcard catch-all entry makes sure that all callers without an explicit entry receive their own per-user rate limit bucket:
>
> aws bedrock-agentcore-control create-gateway-rate-limit \
>
> --gateway-identifier my-gateway-abc1234567 \
>
> --dimension-keys '["$.context.jwt.sub"]' \
>
> --description "Per-sub request limit" \
>
> --entries '[
>
> {
>
> "dimensions": {"$.context.jwt.sub": "Arnav"},
>
> "requests": [{"rate": 100, "period": "minute"}]
>
> },
>
> {
>
> "dimensions": {"$.context.jwt.sub": "*"},
>
> "requests": [{"rate": 50,

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。