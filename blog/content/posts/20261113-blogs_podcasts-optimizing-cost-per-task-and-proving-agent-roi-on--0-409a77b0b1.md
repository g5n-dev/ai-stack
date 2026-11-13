---
title: "Optimizing cost per task and proving agent ROI on Amazon Bedrock"
date: 2026-11-13T02:54:53+08:00
draft: false
entry_kind: "auto"
tags: ["AI Agent", "生成式 AI", "Prompt 工程", "Advanced (300)", "Amazon Bedrock", "Technical How-to", "博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:f539dbbac49f734f820e1b8568165e52cd86fe8f7c47316d95297534fed21980"
source_payload_sha256: "sha256:bfa6987b21284491781352f9b4b21f4009eddba4b133a65a4758fb3ee2e30c24"
observation_id: obs_409a77b0b17a5148c50fa2d34fd8e289467f415901180490ea46c922f91886bd
event_id: evt_75652dc861592c234e2fae4d15983948199915ef11c45d74b7e69306b21913aa
revision_id: rev_1f80b7f5adcb67e9e7a67a45ae2170b3944802fc89a7e7795d7ad4a4d65fe17d
source_published_at: 2026-11-12T18:43:19Z
first_seen_at: 2026-11-12T19:05:28Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 64
interpretation_sha256: "sha256:c6b9fa0100266f371dae04997f45084891d650c9bfaf2ae53a0c40c46872024e"
description: "这套方法不再只看模型的 token 单价，而是按完整任务核算成本，并纳入分词效率、输出冗长度、代理循环次数和推理开销。它还通过人工基线、对照实验和五维评分卡，衡量智能体相对人工的表现与投资回报。"
external_url: https://aws.amazon.com/blogs/machine-learning/optimizing-cost-per-task-and-proving-agent-roi-on-amazon-bedrock
parent_observation_id: null
last_seen_at: 2026-11-13T00:00:00Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/optimizing-cost-per-task-and-proving-agent-roi-on-amazon-bedrock](https://aws.amazon.com/blogs/machine-learning/optimizing-cost-per-task-and-proving-agent-roi-on-amazon-bedrock)
- **发布域名**: aws.amazon.com

## 要点解读

### 这是什么
这套方法不再只看模型的 token 单价，而是按完整任务核算成本，并纳入分词效率、输出冗长度、代理循环次数和推理开销。它还通过人工基线、对照实验和五维评分卡，衡量智能体相对人工的表现与投资回报。

### 用在哪里
适合在 Amazon Bedrock 上运行智能体、需要控制模型支出的应用与平台工程师。也适用于需要向管理层证明智能体投入合理性的产品负责人和 FinOps 团队。

### 可以推断的
- 推测：模型选型不应仅依据标价，实际工作负载中的任务成功率与调用轮次更适合用于成本比较。
- 推测：缓存、模型路由和输出约束可作为优化方向，但具体收益仍需用自身工作负载进行基准测试。

## 来源摘要/节选

> Part 1 of this series built the operating model that controls Amazon Bedrock spend: attribution with AWS Identity and Access Management (IAM) principal tags and Cost and Usage Report 2.0, observability with model invocation logging, enforcement at three tiers, and a review cadence. That layer answers who spent it, and you can stop them. It can’t tell you whether the spend was well spent.
>
> This post answers two questions that Part 1 deliberately left open. First: Why is this workflow expensive? The answer requires thinking in cost per task, not cost per token. Second: Is the agent better than the humans were? The answer requires baselines, controlled experiments, and a scorecard tied to decisions.
>
> In this post, you learn a framework for calculating true model cost (including four hidden cost drivers that the pricing page doesn’t show), techniques for reducing cost per task through caching, routing, and output constraints, and a discipline for measuring agent ROI with human baselines, holdout experiments, and a five-dimension scorecard. This post is written for two audiences: the application and platform engineers who own the optimization levers, and the product owners and FinOps partners who need to justify agent spend to leadership.
>
> Cost per task, not cost per token
>
> Price per token invites quick comparison, but it doesn’t reflect what you actually pay. The published rate reflects the cost of a single token. Your bill reflects the cost of completing a task. A task is one complete unit of work your application asks a model to do: resolve one support email, extract fields from one invoice, or answer one user question. A task runs from the request through to a usable result, however many model calls it takes.
>
> The lower-priced model might not be the cheaper one to run. A cheaper model might fragment your text into more tokens, pad responses with filler, misread your tool schema and loop through corrections, or burn thousands of reasoning tokens before answering. None of these costs appear on the Bedrock pricing page.
>
> The four hidden cost drivers
>
> Four model characteristics determine what that published rate actually costs you on your workload.
>
> Tokenizer efficiency
>
> A token isn’t a word, and it is not equal across models. Every model family uses a different tokenizer and vocabulary. The same text, code, or JSON payload splits into different token counts. If Model A’s list price is 15 percent lower but its tokenizer needs 40 percent more tokens for your data (common with structured schemas and numerical arrays), Model B is cheaper. The gap widens for non-English text: many tokenizers fragment non-Latin scripts into two to three times more tokens than the equivalent English.
>
> Output alignment and verbosity
>
> Output tokens commonly cost 3–5x more than input tokens (the ratio varies by family. Refer to the Bedrock pricing page). A model that ignores formatting constraints like “return only raw JSON” makes you pay that output premium for filler words. A model that follows formatting instructions closely saves money by generating fewer of these more expensive output tokens.
>
> Agentic loop efficiency
>
> Agentic workflows change the cost math entirely. Tool use (function calling) lets a model invoke external functions, requiring a multi-turn loop: analyze the prompt, decide to call a tool, wait for the observation, generate an answer. Each turn re-sends the full conversation history and tool results as input tokens. A model that takes four turns (each one re-sending a larger context payload) costs far more than one that finishes in a single pass.
>
> Reasoning overhead
>
> Many models support extended thinking, working through a chain of thought before the visible answer. Reasoning tokens bill as output tokens, so a model that thinks for 2,000 tokens before a 200-token answer bills you for 2,200. Some models redact the reasoning while still charging for it. Start with reasoning turned off and enable it only when benchmarks show a quality gap that justifies the cost.
>
> Cost per task: A worked example
>
> Figure 1: Comparing two models across five cost dimensions. List price is only one of five factors that determine actual cost
>
> Consider an agentic workflow that reads a 750-word customer email, extracts entities, calls an API to verify account status, and outputs strict JSON. The following comparison uses illustrative prices (always benchmark against your own data and current Bedrock pricing):
>
> Metric
>
> Model A (lower list price)
>
> Model B (higher list price)
>
> Input list price
>
> $0.50 / 1M tokens
>
> $1.00 / 1M tokens
>
> Output list price
>
> $1.50 / 1M tokens
>
> $3.00 / 1M tokens
>
> Tokenizer efficiency (turn 1 input)
>
> 1,500 tokens
>
> 1,000 tokens
>
> Output verbosity (final response)
>
> 450 tokens
>
> 150 tokens
>
> Agentic loops required
>
> 3 turns (error correction)
>
> 1 turn (zero-shot)
>
> Cumulative input tokens, all turns
>
> 6,150
>
> 1,000
>
> Cumulative output tokens, all turns
>
> 750
>
> 150
>
> Total task cost
>
> $0.0042
>
> $0.00145
>
> Model A: (6,150 x $0.50 + 750 x $1.50) / 1,000,000 = $0.0042
>
> Model B: (1,000 x $1.00 + 150 x $3.00) / 1,000,000 = $0.00145
>
> Figure 2: Why the higher-priced model costs 65% less. Each extra turn re-sends a growing context payload, compounding the bill
>
> Why the 2x-priced model costs 65 percent less: three compounding factors. Model A’s tokenizer fragments the email into 50 percent more tokens, inflating every input payload. It pads its JSON with filler, tripling output tokens. And it misaligns with the tool schema, needing two correction turns that each re-send a growing history.
>
> Cost per successful task
>
> The preceding example assumes both models eventually succeed. In production they won’t, and a failure is rarely free. The formulas:
>
> For retry-until-success workflows:
>
> cost per successful task = cost per attempt / success rate
>
> For escalate-on-failure workflows:
>
> cost per successful task = cost per attempt + (1 - success rate) x escalation cost
>
> Input further splits into three buckets when prompt caching is active: uncached input at base rate, cache reads below base rate, and cache writes above base rate.
>
> Measuring it on your own workload
>
> Which model is actually cheaper only shows up when you benchmark against your own data. Amazon Bedrock model evaluation is the managed feature for the quality half of that: define criteria, upload your prompt datasets, and get scored results with automatic metrics and optional human review, with no custom infrastructure required.
>
> Quality scores alone don’t produce a bill, though. Three more Bedrock features supply the token and turn counts you price against them:
>
> CountTokens returns the input token count a given model would charge for a given payload without running inference. It’s the cheapest way to compare tokenizer efficiency (driver #1) across candidates before you spend anything on generation.
>
> Model invocation response carries a usage block with inputTokens, outputTokens, cacheReadInputTokens, and cacheWriteInputTokens. Accumulating those across the turns of a single task gives you the four terms of the preceding cost-per-attempt formula. One gotcha: when caching is enabled, inputTokens counts only the uncached tokens, so your total input volume is inputTokens + cacheReadInputTokens + cacheWriteInputTokens. Sum them to know the footprint, but price them separately, since the three bill at different rates. Evaluate this multiple times throughout your journey and set the cache checkpoints based on what is the active current load. The drift in cache checkpoints happens as the application progresses and the tools become stale. This means that you will be writing more to the cache in 3 months from now when the drift has happened. Evaluating your data constantly for optimal cache usage becomes a primary lever to reduce cost.
>
> Model invocation logging writes per-invocation token counts to Amazon Simple Storage Service (Amazon S3) or Amazon CloudWatch Logs, so you can measure turns-to-completion against real production traffic instead of a sample. Tag calls with request metadata to slice those logged token counts by team, feature, or experiment. However, these are log fields, not cost allocation tags, and never appear in AWS Cost Explorer or your Cost and Usage Report. Application inference profiles do reach both, at a grain of one usage type per day. That grain is right for chargeback but too coarse for cost per task. Multiplying logged token counts by the published rates gives you a near real-time estimate rather than an invoice. It won’t reflect commitments, batch pricing, or provisioned throughput unless you model them. Reconcile against your Cost and Usage Report before you treat it as the bill.
>
> Reducing cost per task: Four levers
>
> Each of the four drivers has a lever, and each is documented in depth. Prompt caching cuts the re-sent context that made Model A expensive, which makes it the largest win on agentic paths. Intelligent prompt routing sends the easy requests to a cheaper model in the same family. A tool schema plus a maxTokens cap holds verbosity down more reliably than prose instructions do, and extended thinking stays off until a benchmark shows it earns its cost back. Batch inference halves the rate on bulk single-turn work, though it rules out tool calling and multi-turn exchange.
>
> Proving agent ROI: Describe the human baseline
>
> Efficient isn’t the same as valuable. An agent can be perfectly optimized and still not be worth running. The question that decides budgets is: is the agent better than the humans were?
>
> Document the human process first
>
> The biggest mistake in agent ROI is trying to prove value without first describing the human workflow. Before building or scaling an agent, write down the current process in operational terms: what triggers the work, which human roles are involved, where the handoffs sit, how completion is defined. This sounds like bureaucracy. It’s actually measurement design. Every instrumentation decision downstream (what counts as a run, what counts as success, where human time is spent) falls out of this description.
>
> Measure the baseline before the agent ships
>
> With the process described, measure the human baseline over a meaningful window: time to completion, queue time, active effort, reopen rate, escalation rate, cost per task, and outcome quality. Baselines must be measured before the agent goes live, not reconstructed from memory after the fact. Retrospective baselines are systematically flattering to the agent: people remember the average case and forget the fast ones.
>
> Instrument the workflow as an experiment
>
> After the baseline exists, instrument the agent workflow as an experiment from day one. Every run gets a trace ID, and every meaningful step is observable. A workflow-run record aggregates everything above the model call into a single analyzable unit:
>
> {
>
> "runId": "run-8f3a2c",
>
> "workflow": "renewal-risk-summary",
>
> "agent": "renewal-agent",
>
> "principalArn": "arn:aws:sts::123456789012:assumed-role/BedrockRuntimeRole/gw-alex",
>
> "team": "sales-ai",
>
> "costCenter": "CC-2041",
>
> "experiment": {
>
> "variant": "treatment",
>
> "holdout": False,
>
> "promptVersion": "v14",
>
> "policyVersion": "2026-07"
>
> },
>
> "ops": {
>
> "latencyMs": 41200,
>
> "retries": 1,
>
> "toolCalls": 6,
>
> "humanApprovals": 1,
>
> "humanMinutes": 35,
>
> "escalations": 0
>
> },
>
> "econ": {
>
> "inputTokens": 48210,
>
> "outputTokens": 3105,
>
> "cacheReadTokens": 31500,
>
> "estCostUsd": 0.87
>
> },
>
> "outcome": {
>
> "status": "success",
>
> "accepted": True,
>
> "reopened": False,
>
> "revenueEventId": "opp-44121"
>
> }
>
> }
>
> Three fields deserve emphasis:
>
> experiment block: Stamped at run creation and propagated into Bedrock request metadata, so model-level and workflow-level records join cleanly.
>
> humanMinutes: What most teams omit and most need. Without it, “the agent did the work” silently excludes the 35 minutes a human spent reviewing it.
>
> revenueEventId: The hook that makes revenue attribution possible later. It costs nothing to record and can’t be reconstructed afterward.
>
> The rule: If the workflow telemetry can’t answer the business question, the instrumentation is incomplete.
>
> Join cost to outcomes
>
> With invocation logs landing in Amazon S3 (Part 1) and workflow-run records in your analytics store, one join produces the metrics that matter. Amazon Bedrock logs record tokens, not dollars, so first build a view that prices each invocation from token counts and your model rate sheet, aggregated by run ID. Then query with Amazon Athena:
>
> SELECT
>
> w.workflow,
>
> w.variant,
>
> COUNT(*) AS runs,
>
> SUM(IF(w.outcome_status = 'success', 1, 0)) AS successes,
>
> ROUND(SUM(c.est_cost_usd) /
>
> NULLIF(SUM(IF(w.outcome_status = 'success', 1, 0)), 0), 2)
>
> AS cost_per_success,
>
> ROUND(SUM(w.retries) * 1.0 /
>
> NULLIF(SUM(IF(w.outcome_status = 'success', 1, 0)), 0), 2)
>
> AS retries_per_success,
>
> ROUND(SUM(w.human_minutes) /
>
> NULLIF(SUM(IF(w.outcome_status = 'success', 1, 0)), 0), 1)
>
> AS human_min_per_success
>
> FROM workflow_runs w
>
> JOIN invocation_costs_by_run c ON c.run_id = w.run_id
>
> GROUP BY w.workflow, w.variant
>
> ORDER BY cost_per_success DESC
>
> Note: Column names and join keys shown in the preceding query are illustrative. Verify against your invocation log schema and workflow telemetry store, which might vary by implementation.
>
> Cost per successful outcome, retries per success, and human minutes per success are the three numbers that survive contact with a skeptical CFO. Cost per call flatters agents that loop. Cost per success doesn’t. Note the variant grouping: the same query, split by experiment arm, is the ROI comparison.
>
> Compare agents and humans correctly
>
> The most credible evaluation is an A/B or holdout test. Controlled treatment and control groups compare the agent-assisted workflow against the human baseline without confusing the result with market, seasonal, or organizational changes.
>
> For customer-facing or revenue-linked workflows, randomize at the visitor, lead, account, or case level. For internal workflows (support operations, coding assistants), use matched cohorts: teams, repository groups, or pods.
>
> The comparison covers four dimensions:
>
> Efficiency: time to completion, hours recovered, queue-time reduction.
>
> Quality: error rate, approval rate, reopen rate, escalation rate.
>
> Cost: cost per task, cost per successful outcome, total cost to serve.
>
> Business value: conversion lift, retention lift, expansion rate, revenue per rep or per workflow.
>
> If the agent improves one dimension while meaningfully degrading another, the result is ambiguous and the deployment needs tuning.
>
> Revenue: The hardest metric
>
> Efficiency gains are the easiest part of the ROI story to prove. Revenue impact is harder, and it is the metric leadership funds against. In revenue-adjacent workflows, measure whether the agent improves conversion, time-to-response, deal progression, or revenue per rep. Holdout tests are the most reliable way to separate incremental revenue attributable to the agent from general business momentum.
>
> When revenue lift is real, the conversation changes. The organization stops asking whether the Bedrock bill went up and starts asking whether the additional spend is buying a meaningful increase in business output.
>
> The scorecard
>
> Based on what we have observed working with customers, a strong operating model doesn’t require fifty metrics. What works is a small scorecard tied to decisions, reviewed on a regular cadence for every production agent.
>
> The following thresholds are starting points, not prescriptions. Calibrate them against your own fleet data and organizational context.
>
> Dimension
>
> Metric
>
> Green
>
> Yellow
>
> Red
>
> Adoption
>
> Active users / intended users
>
> &gt;70%
>
> 40-70%
>
> &lt;40%
>
> Quality
>
> Tasks completed without rework
>
> &gt;90%
>
> 75-90%
>
> &lt;75%
>
> Efficiency
>
> Hours recovered per week
>
> &gt;target
>
> 50-100% of target
>
> &lt;50% of target
>
> Cost
>
> Cost per successful outcome
>
> ≤budget
>
> 1-1.5x budget
>
> &gt;1.5x budget
>
> Business impact
>
> KPI lift compared to baseline
>
> Significant
>
> Marginal
>
> None or negative
>
> Green means scale: the agent beats baseline while meeting cost and quality thresholds. Yellow means tune: promising but needs work. Red means retire or redesign: the agent consumes cost without enough measurable value. The willingness to actually retire a red agent is what makes the rest of the scorecard credible.
>
> Conclusion
>
> In this post, you learned how to calculate the true cost of a model by accounting for four hidden cost drivers (tokenizer efficiency, output alignment, agentic loop efficiency, and reasoning overhead), how to reduce cost per task through prompt caching, model routing, output constraints, and batch inference, and how to prove agent ROI by measuring human baselines, instrumenting workflows as experiments, joining cost to outcomes, and running holdout comparisons.
>
> The cost optimization half answers “why is this expensive and how do I fix it.” The ROI half answers “is the agent better than the humans were.” Together with Part 1’s operating model (attribute, observe, enforce, optimize, operate), they form a complete framework: you can see who spent it, explain why, reduce the waste, and justify what remains.
>
> To get started, benchmark your top model candidates against your own prompts using Amazon Bedrock model evaluation, capture tokens and turns from the usage block or your invocation logs, price them against current Bedrock pricing, and divide by success rate. For ROI measurement, consult the Well-Architected Agentic AI Lens for agent cost governance best practices.
>
> If you have found other techniques for reducing cost per task or measuring agent ROI on Amazon Bedrock, let us know in the comments.
>
> About the authors
>
> Majd Arbash
>
> Majd Arbash is an Enterprise Solutions Architect at AWS based in Toronto, where he helps enterprise customers build secure, scalable cloud solutions and adopt generative AI. A member of the Serverless and Generative AI Technical Field Communities, Majd focuses on application modernization, security, and hands-on generative AI experimentation.
>
> Aswath Ram A Srinivasan
>
> Aswath is a Senior Specialist Solutions Architect for Bedrock focusing on Bedrock Core models, Features and cost optimization/attribution. He helps ISVs and strategic customers solve their challenges and he works with enterprise teams to design inference architectures that balance performance, cost, and operational simplicity, responsibly. In his free time he is a photographer and loves reviewing science journal papers on neurosymbolic AI and Responsible AI.
>
> Ajit Mahareddy
>
> Ajit is an experienced Product and Go-To-Market (GTM) leader with over 20 years of experience in product management, engineering, and go-to-market. Prior to his current role, Ajit led product management building AI/ML products at leading technology companies, including Uber, Turing, and eHealth. He is passionate about advancing generative AI technologies and driving real-world impact with generative AI.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。