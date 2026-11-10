---
title: "The agent evaluation playbook: Built-in, DeepEval, and AutoEval on Amazon Bedrock AgentCore Evaluations"
date: 2026-11-11T07:19:10+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "机器学习", "Prompt 工程", "Advanced (300)", "Amazon Bedrock AgentCore", "Announcements", "博客与播客"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:3aa91fed70b1969b75892575302d7234174610c2b33431a07e9b6038d6a90b11"
source_payload_sha256: "sha256:c644b40be84f4bb1a3687cc2a95578b6bab1aa634ef3d9e1b31b2a1ef6e4e2ff"
observation_id: obs_6d77a575f579de9bddf060a1269b34c406ecd2d2de042436b64417f39ef25e85
event_id: evt_ef45433b032bc579e197be1c644e0ea3e441835116fed8a0b8d4f1a1949fee7e
revision_id: rev_765be2e6d25d45bf671660402b593c1ee51cc7f3b71955db27d94ab4b4e4a1d2
source_published_at: 2026-11-10T22:35:03Z
first_seen_at: 2026-11-10T23:17:59.953443Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 103
interpretation_sha256: "sha256:2120ee6654f88f72b9c4cec23cdc01e0c905902a0ebf6b02a81d5a8ac764522b"
description: "这是一篇关于智能体评估实践的技术文章，介绍如何以业务目标为起点，将成功标准拆解为可观察行为，再映射到轨迹级或会话级评估器。文章重点讲解 Amazon Bedrock AgentCore Evaluations 中内置评估器、DeepEval 和 AutoEval 的用途及组合方式。"
external_url: https://aws.amazon.com/blogs/machine-learning/the-agent-evaluation-playbook-built-in-deepeval-and-autoeval-on-agentcore
parent_observation_id: null
last_seen_at: 2026-11-10T23:17:59.953443Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/the-agent-evaluation-playbook-built-in-deepeval-and-autoeval-on-agentcore](https://aws.amazon.com/blogs/machine-learning/the-agent-evaluation-playbook-built-in-deepeval-and-autoeval-on-agentcore)
- **发布域名**: aws.amazon.com

## 要点解读

### 这是什么
这是一篇关于智能体评估实践的技术文章，介绍如何以业务目标为起点，将成功标准拆解为可观察行为，再映射到轨迹级或会话级评估器。文章重点讲解 Amazon Bedrock AgentCore Evaluations 中内置评估器、DeepEval 和 AutoEval 的用途及组合方式。

### 用在哪里
适用于需要将智能体投入生产、持续验证任务完成度、工具调用、对话质量与安全性的团队。尤其是使用 AgentCore、已经采用 DeepEval 或 AutoEval，或需要自定义评估模型与评分规则的团队，可参考其评估器选型方法。

### 可以推断的
- 推测：先明确业务成功标准再配置指标，有助于避免仅凭单一分数判断智能体是否可靠。
- 推测：同时覆盖任务完成、工具使用和安全行为，可以降低“得分不错但实际业务失败”的风险。

## 来源摘要/节选

> When you deploy an agent to production, one of the hardest questions is whether it’s actually working? The bar isn’t whether it runs. It’s whether it does what the business needs, at scale. Many teams will tell you they can’t really see this. They spot-check outputs, watch latency, and collect user feedback when they can get it. None of that tells you whether the agent finished the user’s task, stayed on topic across a long session, leaked personally identifiable information (PII), or quietly skipped half the steps it was supposed to follow.
>
> Figure 1: Teams usually watch surface signals, but business outcomes are decided by the agent behaviors below the waterline
>
> Agent evaluation solves this problem. What makes this challenging is that a good score on one metric can hide a failure on another. A support agent can resolve every ticket and still expose personal information in its replies. In this case, the agent is failing although it has a high completion rate. To get evaluation right, measure the behaviors that matter for each agent, at the right level of detail.
>
> This post shows how to do this on Amazon Bedrock AgentCore. We use the AgentCore built-in evaluators together with the DeepEval and AutoEval evaluators directly from AgentCore Evaluations.
>
> Start with business outcomes, instead of metric names
>
> The most common mistake is to start with the metric list and pick the names that sound right. “Helpfulness sounds good, so we use it.” The result runs and produces numbers, but it gives almost no useful insight. The metric fits its label, not what success means for the agent.
>
> Instead, start with three steps.
>
> Define success in business terms. For a customer support agent, that might be first-contact resolution. For a research agent, it might be producing a complete, well-sourced answer grounded entirely in retrieved documents. For a content moderation assistant, it means flagging everything that should be flagged and only what should be flagged.
>
> Break the outcome into observable behaviors. A customer support agent that achieves first-contact resolution will typically complete the user’s stated goal, stay coherent across turns when the issue requires clarification, keep responses within compliance boundaries, and correctly invoke backend tools like ticket creation or order lookup.
>
> Map each behavior to an evaluator at the right level. Trace-level metrics cover per-turn or per-tool-call behaviors. Session-level metrics cover outcomes that only make sense when you look at the whole conversation.
>
> Figure 2: Translating a business outcome into observable behaviors and then into specific evaluators at the trace or session level
>
> This three-step process is the mental model that makes evaluation useful. The rest of this post is about what AgentCore gives you to execute it.
>
> The evaluator catalog
>
> AgentCore has a broad catalog of evaluators from three sources:
>
> Built-in evaluators are authored and quality-tested by AWS. You reference them by their ID (Builtin.GoalSuccessRate, Builtin.Helpfulness, and 13 more) and the service handles everything else. They are benchmarked for reliability and cover the common dimensions, so they are the straightforward place to start.
>
> Third-party managed evaluators come from DeepEval and AutoEval, two established open-source evaluation libraries. When you use them in managed mode, AgentCore hosts the code, picks the judge model, and runs inference on its own capacity, exactly like built-in evaluators. If your team already uses one of these libraries in development, you can run the same metrics in production without a separate evaluation service.
>
> Custom evaluators take a built-in or third-party evaluator as a base, so you can swap in your own model and modify the prompt or rubric.
>
> Figure 3: The three evaluator tiers trade AWS quality assurance for increasing control over the model and account that run inference
>
> After creation, a custom derived evaluator is used exactly like other ones.
>
> The evaluator landscape
>
> AgentCore ships with a broad catalog of evaluators, so you rarely start from a blank page. Before you write a custom judge, check whether one already measures the behavior you care about. The following figure shows the whole landscape.
>
> Figure 4: The full evaluator landscape on AgentCore across built-in, DeepEval, AutoEval, and custom sources
>
> Built-in AWS evaluators fall into five groups:
>
> Response quality covers whether the answer is accurate, grounded, and well-formed: Correctness, Faithfulness, Helpfulness, ResponseRelevance, Conciseness, Coherence, InstructionFollowing, and Refusal.
>
> Task and goal completion has GoalSuccessRate, which looks at the whole session and asks whether the user’s goal was met.
>
> Tool use has ToolSelectionAccuracy and ToolParameterAccuracy, which check whether the agent picked the right tool and passed it the right arguments.
>
> Skills has SkillSelectionAccuracy and SkillInstructionFollowing, for agents that load skills: was the right skill invoked, and were its steps followed?
>
> Safety has Harmfulness and Stereotyping.
>
> Next to these are three ground-truth trajectory checks: TrajectoryExactOrderMatch, TrajectoryInOrderMatch, and TrajectoryAnyOrderMatch. They compare the agent’s actual tool path against the one you expected. Reach for them when how the agent got there matters as much as what it produced.
>
> DeepEval provides managed open-source metrics in four groups:
>
> Task and goal completion: TaskCompletion, GoalAccuracy, and ConversationCompleteness.
>
> Conversational quality: TurnRelevancy, KnowledgeRetention, and Summarization.
>
> Tool use: ToolUse.
>
> Safety: Bias, Toxicity, and PIILeakage.
>
> These metrics are especially useful for multi-turn agents. ConversationCompleteness catches an agent that answers the latest message but quietly drops earlier requests. KnowledgeRetention catches an agent that forgets something the user said three turns ago.
>
> AutoEval offers more specialized signals:
>
> Security flags malicious output, such as attempts to inject instructions or reveal system prompts.
>
> Possible catches over-cautious agents that wrongly declare a valid task impossible.
>
> Humor matters for consumer-facing agents where personality is part of the product.
>
> Custom evaluators. When no evaluator in the catalog fits, you can write a custom LLM-as-a-judge.
>
> Every evaluator’s exact definition, scoring scale, and input requirements are in the prompt template library in the AgentCore documentation. That includes the judge prompt it uses, the trace or session level it runs at, and whether it needs a reference answer or an expected trajectory. You can call the ListEvaluators API to get the full catalog and your own custom evaluators in one response.
>
> Multi-dimension evaluators
>
> Each evaluator so far returns one score per trace or session. That works when you measure one behavior. But step 2 of the outcome mapping rarely gives one behavior per evaluator. A support reply must resolve the issue, follow refund and data policy, and stay professional. One judge that weighs all three returns one number, and you cannot tell which criterion drove it.
>
> A multi-dimension evaluator is a custom LLM-as-a-judge with a list of dimensions instead of one scale. Each dimension has its own name, instruction, and numeric or categorical scale. The judge reads the trace once and scores every dimension in the same call. AgentCore returns one result per dimension.
>
> Figure 5: A multi-dimension evaluator scores several dimensions from a single judge call and returns one result per dimension with no composite score
>
> Use a multi-dimension evaluator when your success criteria can fail independently, such as an answer that’s accurate but non-compliant, or resolved but rude. It also needs every criterion to be judgeable from the same evidence, so that one judge call replaces several near-identical evaluators re-reading the same trace. When you score the criteria separately, you can gate on each one. A release that improves tone but regresses policy compliance fails, and a single blended score would hide that.
>
> Keep criteria in separate evaluators when an established built-in or third-party metric already covers them, such as Builtin.Correctness or ThirdParty.DeepEval.PIILeakage. Also keep them separate when they need different levels or judge models, because the dimensions in one evaluator share a single level and model. Do the same when some criteria need ground truth such as {expected_response} or {assertions}. Keeping the reference-free criteria in their own evaluator means it can still run on live traffic.
>
> Example stacks by agent type
>
> Each of the following stacks starts with two or three evaluators that best match the business outcome. Add the others when you find a failure mode the first set misses. Evaluators marked “needs ground truth” run in batch evaluation only, because live traffic has no reference answer or expected path.
>
> Customer support
>
> Multi-step research
>
> Domain content (medical, legal, financial)
>
> Business outcome
>
> Problem solved in one session, with no downstream risk
>
> Complete, well-sourced answer through a defined workflow
>
> Correct, unbiased, secure answers within the domain
>
> Main risk
>
> Dropped requests, unsafe or non-compliant replies
>
> Right answer through the wrong tool path, or lost context in long sessions
>
> A wrong answer. A wrong answer is worse than no answer.
>
> Start with
>
> Builtin.GoalSuccessRate (anchor)
>
> ThirdParty.DeepEval.ConversationCompleteness
>
> ThirdParty.DeepEval.PIILeakage
>
> Builtin.TrajectoryAnyOrderMatch (needs ground truth)
>
> ThirdParty.DeepEval.GoalAccuracy
>
> ThirdParty.DeepEval.KnowledgeRetention
>
> Builtin.Correctness (needs ground truth)
>
> ThirdParty.DeepEval.PIILeakage
>
> ThirdParty.AutoEval.Security
>
> Add when needed
>
> ThirdParty.DeepEval.Toxicity
>
> ThirdParty.AutoEval.Security (sensitive account data)
>
> Builtin.Helpfulness
>
> Builtin.SkillInstructionFollowing
>
> ThirdParty.AutoEval.Possible
>
> ThirdParty.DeepEval.Bias
>
> Builtin.Helpfulness
>
> Derived evaluators
>
> Optional
>
> Use for trajectory and skill metrics if inference must stay in your account
>
> Almost always, so every judge call stays under your data governance
>
> Running evaluations: The three modes
>
> AgentCore supports three evaluation modes.
>
> On-demand evaluation is the fastest feedback loop. Pass a session directly to client.evaluate() during development or debugging. Every evaluator in the system, including third-party, works here.
>
> import boto3
>
> client = boto3.client('bedrock-agentcore')
>
> response = client.evaluate(
>
> evaluatorId="ThirdParty.DeepEval.TaskCompletion",
>
> evaluationInput={"sessionSpans": session_span_logs}
>
> )
>
> for result in response["evaluationResults"]:
>
> print(f"Value: {result.get('value')}")
>
> print(f"Explanation: {result.get('explanation', '')}")
>
> Online evaluation attaches to your live agent runtime and samples real traffic at a configured rate. This is your production health signal. Built-in and third-party evaluators mix freely in a single online evaluation config.
>
> Batch evaluation runs a defined evaluator stack against a fixed set of sessions: your golden dataset for regression testing before releases. Use this to confirm that a prompt change or model upgrade preserved quality across every dimension you care about.
>
> All three modes use the same evaluator IDs. Switching from on-demand development testing to production online evaluation is a configuration change, not a code rewrite.
>
> Putting it together
>
> Increasingly, the hard part is choosing which evaluators to pick. Pick the two or three behaviors that best show whether you reached your business outcome, and measure those first. Add an evaluator when you find a failure your current set missed.
>
> To see the full catalog, call the ListEvaluators API. It returns the built-in, DeepEval, and AutoEval evaluators in one response along with any custom evaluators in your account. Before you pick any of them, answer two questions: “What does success look like for this agent?” and “What behavior in the trace shows that it happened?”
>
> About the authors
>
> Bharathi Srinivasan
>
> Bharathi is the technical go-to-market specialist for Trustworthy AI at AWS, helping organizations safely move frontier AI concepts into real-world production environments. Passionate about AI reliability and developer enablement, she frequently publishes research and code samples on LLM evaluation, reliability, and security. In her free time, she enjoys exploring mountain trails, gearing up for backcountry adventures, and indulging in K-dramas.
>
> Neha Thakur
>
> Neha is a Solutions Architect at AWS, working as both a generalist across the breadth of AWS services and a specialist in AI/ML. She works with some of the biggest banks and fintechs in the UK to help solve complex business challenges by leveraging AWS AI/ML services. She is deeply passionate about AI interpretability and committed to making artificial intelligence more transparent, explainable, and trustworthy.
>
> Visakh Madathil
>
> Visakh is a Solutions Architect at AWS, working with customers and internal teams to bring legibility, trust, and safety to production AI systems. His work on AI safety and reliability has been presented at machine learning conferences. Outside of work, he enjoys music, birding, and sports.
>
> Manoj Selvakumar
>
> Manoj is an AI Specialist Solutions Architect at AWS. He helps startups and enterprises build and scale AI applications and agents on Amazon Bedrock. His work spans model inference, agent harnesses, and agent evaluation, examining how models and agents behave under real-world requirements and what it takes to make them reliable at scale. He partners with AWS service teams to translate these production insights into product direction and service improvements.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。