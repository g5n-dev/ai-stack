---
title: "Control agent behaviors and cost beyond a single action: new capabilities in Amazon Bedrock AgentCore"
date: 2026-08-07T13:06:47+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "Amazon Bedrock AgentCore", "Announcements", "博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:d119d762b09b4874e05e53970e0cd47f37996f1c08299c1d0fdd12b3067fbd44"
source_payload_sha256: "sha256:53a3e39280254005f1feab67ee21c90d31dac3a848e8f00f3331358926090fb5"
observation_id: obs_9dd811c7faac69549d927640c410f91f272fa0bb141c9a3d8bb0e1b19f8e9dd8
event_id: evt_3e964a091e5e829afe7f08cbc1277b3af926d306cdb3b2f16746c747f8a83802
revision_id: rev_ee3e5b9090d447c83d00db6f65c2e8cc2b14724cb187d5787b5cac8492d89c32
source_published_at: 2026-08-06T16:43:19Z
first_seen_at: 2026-08-07T05:14:54Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 101
interpretation_sha256: "sha256:b2c29856fd6f4d01b9b18afadf2c95e2c1d50fcdd0109128451b332a208f2881"
description: "Amazon Bedrock AgentCore 新增了**时间策略**和**网关速率限制**两项功能。时间策略由开源的 Dogwood 策略语言实现，能够在 agent 的整个执行序列上检查行为是否符合预设规则，而不只是对单次调用做判断。"
external_url: https://aws.amazon.com/blogs/machine-learning/control-agent-behaviors-and-cost-beyond-a-single-action-new-capabilities-in-amazon-bedrock-agentcore
parent_observation_id: null
last_seen_at: 2026-08-07T05:04:03.594248Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/control-agent-behaviors-and-cost-beyond-a-single-action-new-capabilities-in-amazon-bedrock-agentcore](https://aws.amazon.com/blogs/machine-learning/control-agent-behaviors-and-cost-beyond-a-single-action-new-capabilities-in-amazon-bedrock-agentcore)
- **发布域名**: aws.amazon.com

## 要点解读

### 这是什么  
Amazon Bedrock AgentCore 新增了**时间策略**和**网关速率限制**两项功能。时间策略由开源的 Dogwood 策略语言实现，能够在 agent 的整个执行序列上检查行为是否符合预设规则，而不只是对单次调用做判断。网关速率限制则对 agent 在一次会话中消耗的 token 数或调用次数设定上限。

### 用在哪里  
在企业级平台上大规模部署自主 AI agent 时，需要在基础设施层统一强制执行安全和成本约束的业务场景。安全合规团队以及关注费用可控性的开发者可利用这两项能力在网关层面直接限制行为和消费，而不必在每个 agent 代码中单独实现。

### 可以推断的  
推测：把策略检查和速率限制放在网关而非 agent 本身实现，可降低因代码实现差异导致的安全漏洞风险，并简化跨团队的一致性管理。  
推测：Dogwood 作为开源策略语言，可能会被其他支持 AI agent 的系统采纳，形成跨平台统一的策略描述方式。

## 来源摘要/节选

> Agents are becoming more autonomous and teams are running more of them, but trust and security have not kept pace. According to McKinsey, roughly 80% of organizations have already encountered risky behavior from AI agents. As a result, security and risk concerns are the leading barrier to scaling agentic AI (McKinsey’s State of AI Trust in 2026, and Trust in the age of AI agents 2026).
>
> That makes trust the pacing factor for agent innovation and adoption. Earning it takes control across a wide surface, including identity, access, observability, evaluation, and traceability. We believe that investment in trust and security will accelerate agent adoption in enterprises. When guardrails are dependable, approving a new agent stops being a one-off negotiation and becomes something the platform handles at scale.
>
> The challenge is that most guardrails today were designed for software that behaves predictably. Agents decide their own path as they go, so every step can pass on its own while the shape of the whole goes unexamined. An agent looks up a customer’s account, then transfers money to a different account number, because each call was judged on its own. An agent places a series of orders that each sits under the approval threshold, because nothing is tracking the total against the budget. An agent hits a failing tool and retries through the night, running through the token budget, because nothing capped how much it could consume. Every one of those requests was legitimate. The problem appears only in the pattern, and the agent is the last thing you would rely on to catch it.
>
> We built Amazon Bedrock AgentCore to give teams what they need to build, connect, and optimize agents at scale without assembling the infrastructure themselves. One principle has guided it from the start: security controls belong in the infrastructure layer, enforced consistently across every agent, rather than in application code where each team implements them differently.
>
> AgentCore’s gateway is where that idea becomes concrete. The gateway is a fully managed, serverless entry point for AI traffic, routing requests to Model Context Protocol (MCP) servers, large language models (LLMs), agents, and knowledge bases. Because every call passes through it, the gateway is the natural place to apply limits that hold no matter how an agent behaves. Today we are advancing that work with new capabilities: temporal policies, powered by Dogwood, a new open source policy language purpose-built for AI agents, and rate limiting in the gateway.
>
> Boundaries on sequences of actions, not only individual ones with temporal policies
>
> Policies in AgentCore today give teams deterministic control over agent behavior, checking every action before it runs to evaluate who can call which tool and under what conditions. Those checks are stateless by design. Each request is judged on its own merits, quickly and provably, which is what authorization has always required. As agents take on longer tasks with less supervision, another question arises: whether its actions, taken together, add up to something that should be allowed. That is only visible when you look at the sequence of actions, not only individual ones.
>
> Temporal policies extend the policies in AgentCore to close that gap. Rather than judging a request in isolation, the policy engine also looks at what the agent has already done in that session, then permits or denies the call based on that sequence of actions. The transfer that used the wrong account number can be blocked by a policy requiring that a value passed into one call match what an earlier call returned. A policy can tally what an agent has spent in a session and block the next purchase once the budget is reached, even if that purchase is under the individual limit. Teams can also require that the steps happen in a set order, or that a significant action needs a recorded human approval. Permissions can narrow automatically when a person is no longer engaged.
>
> Temporal policies are enforced at the gateway layer, outside the agent’s own code. The agent does not see the policy logic and cannot reason around it, regardless of how it is prompted or whatever defects it carries. For security leaders being asked to approve autonomous systems, this is the distinction that matters. It is the difference between trusting an agent to behave and knowing the boundary holds over the course of its actions. Decisions are deterministic, deny by default, and logged with the full context behind them. A reviewer can see not only that a call was blocked but why.
>
> Powering temporal policies is Dogwood, a new policy language purpose-built for AI agents. Built on the foundation of Cedar, Dogwood was designed to address a new dimension of agent control: evaluating whether a sequence of agent actions conforms to a policy as it unfolds. Dogwood embeds Cedar and adds temporal constructs for agent governance including rate limits, time windows, prerequisite steps, and escalation triggers. Dogwood is available as an open source specification and reference implementation under Apache 2.0. This gives customers full visibility into how their policies are evaluated and allows the broader ecosystem to build supporting tooling.
>
> Control what agents consume with rate limiting on gateway
>
> AI cost is its own governance question, and with agents it starts with how fast they consume tokens and calls. An agent takes as many steps as it judges necessary, so what a task costs depends on how it chooses to work rather than on a predetermined rate. Left unbounded, a retry loop or an unusually heavy session consumes at whatever speed the agent decides. That unpredictability is a real constraint on approval. Forrester found that the reasons agentic AI rarely reaches scale starts with cost (The State Of Agentic AI In 2026). Teams need a ceiling that holds regardless of how an agent behaves.
>
> Available today, you can set those ceilings directly on AgentCore’s gateway. Rate limiting lets teams cap consumption per user across every tool, model, and agent behind the gateway, using the identities they already manage through OAuth or IAM. Limits can cover how many requests someone makes, how many tokens a model processes for them, and how long they hold connections open. Having all three matters because agents run up cost in different ways. A retry loop shows up as request volume, a reasoning-heavy task shows up as tokens, and a long research session shows up as a connection held open while very little traffic moves. Any single measure leaves a way to exhaust a service without tripping a limit.
>
> Limits apply in per-second and per-minute windows, which is what contains the failure mode teams actually hit: an agent consuming at a rate nobody intended, discovered after the fact. Rate limits take effect once they are configured, with no changes to agent code. Capacity allocation becomes something platform teams configure rather than build. Different users, teams, tools, and models can carry different ceilings, without throttling logic written into any of them.
>
> Where this is heading
>
> Models keep improving, and that progress is what makes agents worth deploying. It also raises what is at stake, because a more capable agent takes more consequential actions with less supervision. What an enterprise earns from better models depends on whether it can run those agents with the same discipline it applies to everything else in production.
>
> Trust in an agent is not really a judgment about the model. It is a judgment about the system the model runs inside, and whether that system holds when an agent behaves unexpectedly. Building that system is a young discipline, and the questions customers bring us now are noticeably more sophisticated than the ones they brought a year ago. We expect to keep moving quickly here, alongside continued investment in identity, observability, evaluation, and traceability. Every control that moves out of application code and into the platform is one fewer thing that must be rebuilt, reviewed, and trusted separately for each agent. The more reliably a platform can bound what agents do and how much they consume, the more autonomy you can extend without hesitation.
>
> Neither capability requires rearchitecting agents already in production, and you can adopt either on its own. To learn more, see the AgentCore documentation and pricing pages, and explore the Dogwood reference implementation.
>
> About the author
>
> Madhu Parthasarathy
>
> Madhu Parthasarathy is the GM of Amazon Bedrock AgentCore, where he leads the team building the platform that companies use to build, connect, and optimize production AI agents. He brings more than 20 years of experience building large-scale distributed infrastructure, including over 16 years at Amazon, where he has led major initiatives across Amazon Retail, Elastic Block Store (EBS), and now AgentCore. Before returning to Amazon, Madhu held senior leadership roles at LinkedIn, where he led the enterprise platform powering all of LinkedIn’s enterprise lines of business, and at a neo-cloud startup, where he led AI infrastructure and set the vision for security and developer experience. He is based in Santa Clara, California.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。