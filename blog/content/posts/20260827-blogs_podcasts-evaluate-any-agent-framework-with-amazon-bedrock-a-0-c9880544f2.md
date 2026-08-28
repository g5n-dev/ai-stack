---
title: "Evaluate any agent framework with Amazon Bedrock AgentCore Evaluations"
date: 2026-08-27T03:23:03+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "深度学习", "Prompt 工程", "Advanced (300)", "Amazon Bedrock AgentCore", "Announcements", "博客与播客"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:ba6b8a94b304bd55d57357eb40f61b9bbbe619e9eb5ae007de6438ded8e4cefd"
source_payload_sha256: "sha256:0fd349791eb23e2152a22d3d19627afb52f408600f9a56199d5bb452508aa51d"
observation_id: obs_c9880544f2a2bcc8af539f698c23ee907616e3100e1463359d5958cf63760848
event_id: evt_e1b84f1c4d0f4a11fd359be6cd44e34ecc8b757f3b1b329104c3e6ce5f9cecaf
revision_id: rev_fa5dfdace9d90127ae1ab2084898b0bde33f3c1aaa0707390b41a327949747de
source_published_at: 2026-08-26T19:13:35Z
first_seen_at: 2026-08-26T19:32:24Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 70
interpretation_sha256: "sha256:72f59f3eb5885b84711717a05990c3f4ddf642967d78c2d831b6ae5e6c01a5d4"
description: "这段内容介绍了一种评估方案，它能够对使用不同构建框架的 AI 代理进行统一评分。该方案通过读取遵循 OpenTelemetry 标准的链路（trace）中的特定 span 角色，重建对话会话后交由一套与框架无关的评估器进行打分。"
external_url: https://aws.amazon.com/blogs/machine-learning/evaluate-any-agent-framework-with-amazon-bedrock-agentcore-evaluations
parent_observation_id: null
last_seen_at: 2026-08-28T00:00:00Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/evaluate-any-agent-framework-with-amazon-bedrock-agentcore-evaluations](https://aws.amazon.com/blogs/machine-learning/evaluate-any-agent-framework-with-amazon-bedrock-agentcore-evaluations)
- **发布域名**: aws.amazon.com

## 要点解读

### 这是什么  
这段内容介绍了一种评估方案，它能够对使用不同构建框架的 AI 代理进行统一评分。该方案通过读取遵循 OpenTelemetry 标准的链路（trace）中的特定 span 角色，重建对话会话后交由一套与框架无关的评估器进行打分。

### 用在哪里  
适用于需要在多个代理开发框架之间保持一致评估能力的 AI 团队，尤其是那些已经采用 OpenTelemetry 进行遥测采集的系统。通过统一的评估流程，团队可以在不改变现有代码的前提下，对不同框架实现的代理进行质量对比。

### 可以推断的  
推测：只要代理在运行时会输出符合已有约定的链路信息，即使框架本身尚未被官方列举，评估服务也能够自动适配并完成评分。  
推测：由于评估逻辑与框架实现解耦，团队在更换或混合使用不同开发框架时，原有的评估规则和指标可以继续复用，减少了重复配置的工作量。

## 来源摘要/节选

> AI teams building production agents face a frustrating asymmetry: the diversity of agent frameworks keeps growing, but evaluation tooling has not kept pace. Most evaluation systems assume you built your agent in a specific way: a specific SDK, a specific large language model (LLM) client, a specific tracing pattern. The moment you step outside that narrow compatibility zone, the evaluation pipeline breaks.
>
> Teams build on LangGraph for its workflow orchestration model, on LlamaIndex for its tight integration with retrieval pipelines, and on the OpenAI Agents SDK when their organization standardizes on GPT models. They use Google ADK for multi-agent coordination, or the Claude Agent SDK for native Anthropic capability. They reach for Strands Agents because its model-driven loop gets a working agent running on Amazon Bedrock AgentCore in minutes rather than days. And increasingly, they deploy all of these on Amazon Bedrock AgentCore runtime, a capability of Amazon Bedrock AgentCore. It handles the hosting, scaling, memory, and observability infrastructure they would otherwise rebuild for each project.
>
> Amazon Bedrock AgentCore evaluations solves this fragmentation by decoupling evaluation from the framework choice. Every major framework supports OpenTelemetry, either natively or through a community instrumentation library. As long as an agent’s telemetry flows through OpenTelemetry, the evaluation service can score it, regardless of what SDK sits underneath. This post explains how that works: what telemetry the service reads, how it decides how to read your spans, which attributes carry the evaluation data, and how coverage extends to frameworks beyond the named list.
>
> OpenTelemetry as the common language
>
> OpenTelemetry is a vendor-neutral instrumentation framework that standardizes how distributed systems emit traces, metrics, and logs. A trace is a tree of spans, and each span represents a single step within a request: one unit of work with its name, timestamps, a set of typed attributes, and optional span events. Spans are exported over the OpenTelemetry Protocol (OTLP) and collected by a telemetry backend. On AgentCore runtime, that backend is the AWS Distro for OpenTelemetry (ADOT), which routes spans and event records to Amazon CloudWatch.
>
> An agent’s execution produces many kinds of span, because an agent does many kinds of work. A single user turn can generate spans for model calls, tool calls, document retrieval from a vector store or database, reranking of retrieved results, embedding generation, guardrail checks, prompt-template rendering, memory reads and writes, and the orchestration steps that tie them together. The two conventions name these explicitly: the OpenTelemetry GenAI conventions define operations such as chat, embeddings, retrieval, execute_tool, invoke_agent, create_agent, plan, and a family of memory operations. OpenInference defines span kinds such as LLM, TOOL, RETRIEVER, RERANKER, EMBEDDING, AGENT, CHAIN, GUARDRAIL, EVALUATOR, and PROMPT. A production trace routinely mixes several of these.
>
> Out of that full set, the evaluation service needs three span roles to reconstruct what happened in a session and score it:
>
> An invoke agent span represents the top-level request-response cycle, which is one user turn in a conversation. It carries the user prompt and the final agent response.
>
> Inference spans represent individual model calls, each carrying the message history passed to the model and the model’s reply.
>
> Execute tool spans represent each tool the agent called, carrying the tool name, input parameters, and result.
>
> These three are what the evaluators operate on. The service classifies every span it receives, reads the values it needs from these three roles, and passes over the rest. Richer traces that also carry retrieval, reranking, guardrail, or memory spans are handled without any special configuration. Those spans simply add context the evaluators don’t require. As frameworks and the conventions add new span kinds over time, this stays forward-compatible: an unfamiliar span kind is context the service skips, not an error.
>
> Session (one runtimeSessionId)
>
> └── Trace (one user turn, one trace_id)
>
> ├── invoke agent span ← read: user prompt + final agent response
>
> ├── inference span ← read: messages to model + model reply
>
> ├── execute tool span ← read: tool name + parameters + result
>
> ├── retriever span (context; not required by evaluators)
>
> ├── inference span ← read: next model call with tool result in history
>
> └── ... (guardrail, memory, reranker, orchestration spans, and more)
>
> The service reads the three marked span roles and treats the others as additional context.
>
> Different frameworks and instrumentation libraries record these three roles using different attribute names, nesting structures, and span-naming conventions. The OpenTelemetry GenAI semantic conventions and the OpenInference specification both define schemas for recording these three span roles, but they use different attribute keys and different span-kind vocabularies. AgentCore Evaluations bridges both schemas to the same result.
>
> How AgentCore Evaluations reads your traces
>
> When you run an evaluation, on demand or through an online evaluation config, the service fetches your agent’s spans and event records from CloudWatch and reconstructs the session. A session is grouped by session.id. Within it, each trace (one trace_id) is one user turn. Every turn is made up of the three span types described earlier.
>
> The service classifies each span, extracts the values it needs, and hands the reconstructed session to the evaluators. From that point on, evaluation is entirely framework-agnostic: the same evaluators, GoalSuccessRate, Correctness, Helpfulness, and custom LLM-as-a-judge, score every framework identically. This is shown visually in the following figure.
>
> Figure 1: Data flow from AgentCore Runtime through Amazon CloudWatch to AgentCore Evaluations
>
> You don’t configure any of this. Every OpenTelemetry instrumentation library stamps a scope.name on the spans and event records it produces, and the evaluation service uses that value to decide how to read them. The correct handling activates automatically from the instrumentation package you installed, with no changes to your agent code. Each supported framework and its scope name is listed in the Supported agent frameworks documentation, which today covers Strands Agents, LangGraph, the OpenAI Agents SDK, LlamaIndex, Google ADK, and the Claude Agent SDK, most with both OpenTelemetry and OpenInference instrumentation.
>
> Coverage reaches beyond the named frameworks. Any library whose scope name falls under opentelemetry.instrumentation.* (following the OpenTelemetry GenAI semantic conventions) or openinference.instrumentation.* (following the OpenInference specification) is read through a generic path. In practice, supporting a new framework is usually only a matter of installing a compliant instrumentation package: the scope-name prefix is how a library opts in. A scope named mycompany.agent.tracing will not be picked up, even if its spans follow the conventions exactly. The prefix is the signal that the instrumentation author deliberately conformed to a documented schema.
>
> Getting a session evaluated end to end comes down to two requirements. The first is grouping: your agent’s spans must carry a session.id attribute that matches the runtimeSessionId you invoked the agent with. That attribute is what lets the service assemble spans into traces and traces into a session. On AgentCore runtime, ADOT injects this attribute automatically, so no agent code changes are needed.
>
> The second requirement is that your data source includes the message content, not only the spans. For agents with unified observability (the default for newly created agents), this is automatic: message content lives in the same per-agent log group as the spans, so a single log group is sufficient. For existing agents still running the pre-unified configuration, however, spans land in the shared aws/spans log group. Message content is stored separately as correlated event records in the agent’s log group. In that configuration, if your data source covers only aws/spans, span classification still succeeds, but message content comes back empty, and any evaluator that scores response quality returns an error.
>
> OpenTelemetry GenAI semantic conventions: Attributes that drive evaluation
>
> The OpenTelemetry GenAI semantic conventions define a schema for spans produced by LLM frameworks. AgentCore Evaluations reads a specific subset of these attributes to classify spans and extract evaluation data. Knowing which attributes carry that data is useful when you are debugging an evaluation or writing custom instrumentation.
>
> Span classification starts with gen_ai.operation.name:
>
> invoke_agent marks the invoke agent span, the top-level span per turn, carrying the user prompt and final response.
>
> chat marks an inference span. The service reads the message history and the model’s reply.
>
> execute_tool marks an execute tool span. The service reads the tool name, input parameters, and result.
>
> When gen_ai.operation.name is absent, common in some LlamaIndex traces, the service falls back to traceloop.span.kind, where workflow maps to the invoke agent span, tool to an execute tool span, and llm to an inference span.
>
> Tool identity comes from gen_ai.tool.name, and gen_ai.tool.call.id is the correlation ID that links a tool call requested on an inference span to its result on the corresponding execute tool span. The gen_ai.tool.definitions attribute on inference spans carries a JSON-encoded array of tool schemas, which the GoalSuccessRate evaluator uses to verify that the tools the agent called were among those it declared available.
>
> Message content lives in one of two places, depending on how telemetry was collected. When telemetry is split, the content is in the correlated event record body (body.input.messages and body.output.messages). When it is not split, the content stays on the span, as gen_ai.input.messages or gen_ai.output.messages attributes or as inline span events. The service reads from whichever location holds the content, so you don’t need to know which path a given deployment took. For the full picture of where content lives, see Spans, event records, and telemetry signals.
>
> OpenInference conventions: An alternative semantic layer
>
> OpenInference is an open specification maintained by Arize AI and widely adopted across the LlamaIndex, Haystack, and Phoenix ecosystems. It represents LLM operations with different attribute names from the OpenTelemetry GenAI conventions. Several frameworks, including the OpenAI Agents SDK with openinference-instrumentation-openai-agents, Google ADK, and the Claude Agent SDK, produce OpenInference spans.
>
> Span classification in OpenInference uses openinference.span.kind. The values LLM, TOOL, AGENT, and CHAIN correspond to inference, execute tool, invoke agent, and structural container spans respectively.
>
> Inference-span message content uses a flat, indexed attribute convention. Input messages follow the pattern llm.input_messages.{i}.message.role and llm.input_messages.{i}.message.content, where i starts at zero and increments for each message in the history. Tool result messages carry an additional llm.input_messages.{i}.message.tool_call_id to link them to the corresponding tool call. Output messages follow the same indexed pattern, with tool calls nested further:
>
> llm.output_messages.0.message.role = "assistant"
>
> llm.output_messages.0.message.tool_calls.0.tool_call.function.name = "get_pto_balance"
>
> llm.output_messages.0.message.tool_calls.0.tool_call.function.arguments = "{\"employee_id\":\"EMP-001\"}"
>
> llm.output_messages.0.message.tool_calls.0.tool_call.id = "call_abc123"
>
> Tool schemas on inference spans use llm.tools.{i}.tool.json_schema, where each value is a JSON string encoding either a plain function schema or an OpenAI-style {"type": "function", "function": {...&#125;&#125; wrapper. The service handles both and reads the name, description, and parameters fields.
>
> Execute tool spans use three attributes: tool.name for the ID, input.value for the parameters (a JSON-encoded object for multi-argument tools, or a plain string for single-argument tools), and output.value for the result. The output.value format has evolved across versions of the OpenInference instrumentation library, and the service reads both the older and newer shapes, so you are not tied to a specific version.
>
> Evaluating any compliant framework
>
> The named frameworks are covered directly, but the design is deliberately open-ended. For any framework outside that list, the two generic paths introduced earlier provide broad coverage whenever the instrumentation follows a documented convention:
>
> The OpenInference path handles any scope under openinference.instrumentation.*. It classifies spans with openinference.span.kind, reads inference content from the indexed llm.input_messages and llm.output_messages attributes, and reads tool.name, input.value, and output.value for tool spans. This covers most frameworks that adopt the OpenInference specification, including ones released after a given framework was named explicitly.
>
> The OpenTelemetry path handles any scope under opentelemetry.instrumentation.*. It classifies spans with gen_ai.operation.name, reads message content from the event record body or span, and uses gen_ai.tool.name for tool identity.
>
> The scope-name prefix is what routes a library to one of these paths. For teams writing custom instrumentation that should be evaluated generically, naming your scope under opentelemetry.instrumentation.* or openinference.instrumentation.* is the way to opt in.
>
> From agent code to evaluation score: A walkthrough
>
> To make this concrete, the AgentCore samples repository provides complete working examples, for instance an HR assistant implemented with the OpenAI Agents SDK, Google ADK, LlamaIndex, and the Claude Agent SDK. Each deploys to AgentCore runtime and is evaluated with the same built-in and custom evaluators.
>
> Instrumentation setup requires no explicit code in either agent. On AgentCore runtime, AWS Distro for OpenTelemetry (ADOT) discovers the installed instrumentation package at startup and activates it automatically. For the OpenAI Agents SDK sample, adding opentelemetry-instrumentation-openai-agents to requirements.txt is sufficient. For the LlamaIndex sample, opentelemetry-instrumentation-llamaindex does the same job. The one thing the OpenAI Agents SDK agent must avoid is calling set_tracing_disabled(True): the instrumentation hooks into the SDK’s own tracing pipeline, so disabling SDK tracing silences the evaluation spans.
>
> For LlamaIndex specifically, agent structure matters. The agent must be built as a FunctionAgent or ReActAgent (workflow agents), not as a plain AgentExecutor. Workflow agents emit a top-level invoke agent span, which anchors the trace. Without it, there is no top-level span to reconstruct the turn from, and the session cannot be assembled from inference spans alone.
>
> To reliably deliver telemetry to CloudWatch, flush at the end of the invocation handler before returning the response. AgentCore runtime suspends the execution environment after the handler returns, while the OTel SDK buffers telemetry in client-side batch processors that export on a periodic timer. As a result, unexported data may still be sitting in the buffers at return time, and there is no guarantee that an export completes before suspension. In practice, missing telemetry from an omitted flush is the most common source of evaluation failures. The OpenAI Agents SDK and LlamaIndex samples implement this with the following pattern:
>
> def _flush_telemetry():
>
> from opentelemetry import trace as _trace
>
> from opentelemetry._logs import get_logger_provider as _get_lp
>
> for provider in (_trace.get_tracer_provider(), _get_lp()):
>
> flush = getattr(provider, "force_flush", None)
>
> if flush:
>
> flush()
>
> @app.entrypoint
>
> async def invoke(payload, context):
>
> prompt = payload.get("prompt", "")
>
> try:
>
> result = await run_agent(prompt)
>
> finally:
>
> _flush_telemetry()
>
> return str(result)
>
> The flush must cover both the tracer provider (spans) and the logger provider (event records): spans and event records go through separate client-side batch processors, so flushing only one of them leaves the other’s buffer untouched.
>
> AgentCore Evaluations uses EvaluationClient identically for both frameworks, after a CloudWatch ingestion wait of 90–150 seconds:
>
> from bedrock_agentcore.evaluation import EvaluationClient
>
> from bedrock_agentcore.evaluation.client import ReferenceInputs
>
> from datetime import timedelta
>
> ec = EvaluationClient(region_name=REGION)
>
> # The client resolves each evaluator's level (SESSION, TRACE, or TOOL_CALL)
>
> # automatically, so no level configuration is needed here.
>
> results = ec.run(
>
> evaluator_ids=[
>
> "Builtin.GoalSuccessRate",
>
> "Builtin.Correctness",
>
> "Builtin.Helpfulness",
>
> CUSTOM_RESPONSE_QUALITY_ID,
>
> CUSTOM_SESSION_COMPLETENESS_ID,
>
> ],
>
> agent_id=AGENT_ID,
>
> session_id=SESSION_ID,
>
> look_back_time=timedelta(hours=1),
>
> reference_inputs=ReferenceInputs(
>
> assertions=ASSERTIONS,
>
> expected_trajectory=EXPECTED_TRAJECTORY,
>
> expected_response=EXPECTED_RESPONSES[-1],
>
> ),
>
> )
>
> The GoalSuccessRate evaluator operates at the session level and checks whether the agent’s tool-call history matched the expected trajectory across all turns. Correctness and Helpfulness are trace-level evaluators that score each individual turn. Built-in evaluators are configured for the session, trace, tool levels and available to use as templates. For custom evaluators that you configure, you define if it works on the session, trace or tool level. It is possible to combine evaluators at various levels into a single evaluation call. The evaluation code for the different framework samples is structurally identical. The only differences are the agent names and resource IDs.
>
> On-demand and online evaluation modes
>
> The sample repository demonstrates both evaluation modes, which serve distinct purposes in a production agent workflow.
>
> On-demand evaluation is the natural fit for continuous integration and continuous delivery (CI/CD) pipelines and regression testing. You invoke the agent to generate a session, then call EvaluationClient.run() in the same script to score it. Because you control the invocation, you can supply ground truth through ReferenceInputs: expected responses, expected tool trajectories, and behavioral assertions. A pipeline that runs on every pull request can invoke a fixed set of test prompts, score them against ground truth, and fail the build if any evaluator drops below threshold.
>
> Online evaluation monitors live agent traffic continuously. You create an OnlineEvaluationConfig once, pointing it at the agent’s CloudWatch log group and specifying a sampling rate. The service picks up new sessions automatically as they arrive:
>
> _cp.create_online_evaluation_config(
>
> onlineEvaluationConfigName="hr_agent_online_eval",
>
> rule={"samplingConfig": {"samplingPercentage": 25.0&#125;&#125;,
>
> dataSourceConfig={
>
> "cloudWatchLogs": {
>
> "logGroupNames": [CW_LOG_GROUP],
>
> "serviceNames": [OTEL_SERVICE_NAME],
>
> }
>
> },
>
> evaluators=[
>
> {"evaluatorId": "Builtin.GoalSuccessRate"},
>
> {"evaluatorId": "Builtin.Correctness"},
>
> {"evaluatorId": "Builtin.Helpfulness"},
>
> ],
>
> evaluationExecutionRoleArn=ONLINE_EVAL_ROLE_ARN,
>
> enableOnCreate=True,
>
> )
>
> Online evaluation can only use evaluators that do not require ground truth, since live traffic has no associated expected responses. The built-in evaluators work in both modes. Custom LLM-as-a-judge evaluators that reference {expected_response} or {assertions} placeholders in their instructions are on-demand only.
>
> Online evaluation results land in a CloudWatch log group at /aws/bedrock-agentcore/evaluations/results/{config_id}. Building a CloudWatch alarm or dashboard from that data gives you continuous visibility into agent quality in production, across all frameworks, through a single consistent interface. Because the same evaluation pipeline processes on-demand and online traffic identically, scores from a CI test run and scores from production traffic are directly comparable when the agent’s behavior is stable.
>
> Conclusion
>
> AgentCore Evaluations is framework-agnostic. Whether you build with LangGraph, the OpenAI Agents SDK, LlamaIndex, Google ADK, the Claude Agent SDK, or Strands Agents, the same evaluators apply uniformly in on-demand and online modes, because the integration contract is built on OpenTelemetry standards. If your agent emits spans under a recognized scope name, includes tool schemas on inference spans, and surfaces message content through span attributes or event records, the evaluation service produces scores without any framework-specific code on your side. For frameworks beyond the named list, following the OpenTelemetry GenAI conventions or the OpenInference specification with the right scope prefix is all it takes. With one evaluation suite, across every agent that emits telemetry under a recognized scope, you can now assess quality consistently.
>
> Ready to try it yourself? Get started with the AgentCore Evaluations feature samples, and refer to the Supported agent frameworks documentation for full details on connecting your framework of choice.
>
> Acknowledgements
>
> Thank you to the AgentCore evaluations engineering team led by Shoaib Javed and Qiaoxuan Xue, and the engineers who contributed to this work: Swarnim Singhal, Lefan Zhang, Athul Iddya, Irene Wang, Ritvika Pillai, Aditya Arepalli.
>
> About the authors
>
> Swarnim Singhal
>
> Swarnim is a Software Development Engineer at AWS on the Amazon Bedrock AgentCore Evaluations team, where he has helped build the product’s evaluation capabilities from the ground up. He designs and builds the core services that let customers measure and improve the quality of their AI agents, with expertise spanning agent evaluation, optimization, and insights. Before AgentCore, he worked on Amazon OpenSearch Serverless, building the metadata services behind OpenSearch Serverless.
>
> Bharathi Srinivasan
>
> Bharathi is the technical go-to-market for Trustworthy AI at AWS, helping organizations safely move frontier AI concepts into real-world production environments. Passionate about AI reliability and developer enablement, she frequently publishes research and code samples on LLM evaluation, reliability, and security. In her free time, she enjoys exploring mountain trails, gearing up for backcountry adventures, and indulging in K-dramas.
>
> Renya Kujirada
>
> Renya is an AI/ML Specialist Solutions Architect at AWS Japan. He works with customers across industries to build AI agents, design agent platforms, and fine-tune LLMs. Before joining AWS, he worked as a Data Scientist developing deep learning models and building solutions powered by AI agents. He was selected as a 2025 Japan AWS Top Engineer and an AWS Community Builder.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。