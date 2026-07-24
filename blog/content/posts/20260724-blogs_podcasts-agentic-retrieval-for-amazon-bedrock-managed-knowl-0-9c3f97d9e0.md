---
title: "Agentic retrieval for Amazon Bedrock Managed Knowledge Base"
date: 2026-07-24T00:49:38+08:00
draft: false
entry_kind: "auto"
tags: ["Amazon Bedrock", "Amazon Bedrock AgentCore", "Intermediate (200)", "Technical How-to", "博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:d0e4df81d2c93656c1a4c927af069354ee961fb4db4ea566cb0d914b988bdadb"
source_payload_sha256: "sha256:3bbaf7739f5bf0b7208705f39fd2042af93f6cfe8a7abeca60a91a3134dc1eae"
observation_id: obs_9c3f97d9e0a04dd255508d5a7e3b3a0b49402fd2daef69c69f9ac69d1bd5530f
event_id: evt_d979b6febe4224368bb0eee71852c735ab2921e7517a8b48ac481c339f4e0be5
revision_id: rev_b3c8f096918bec19e3fc0e48c40cc97814c84dd0706680c2a2950b9f9a10b4f5
source_published_at: 2026-07-23T16:30:20Z
first_seen_at: 2026-07-23T17:12:15Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 59
description: "当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。"
external_url: https://aws.amazon.com/blogs/machine-learning/agentic-retrieval-for-amazon-bedrock-managed-knowledge-base
parent_observation_id: null
last_seen_at: 2026-07-24T00:00:00Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/agentic-retrieval-for-amazon-bedrock-managed-knowledge-base](https://aws.amazon.com/blogs/machine-learning/agentic-retrieval-for-amazon-bedrock-managed-knowledge-base)

## 来源摘要/节选

> Your users ask multi-part, comparative, and exploratory questions that span PDFs, slides, tickets, transcripts, and web content. Classic single-shot retrieval breaks down on these questions. Answers miss context, support tickets escalate, and analysts waste hours re-running searches. Agentic retrieval for Amazon Bedrock Managed Knowledge Bases is designed for these questions.
>
> Consider two questions an analyst might ask: “Compare our 2020 and 2023 strategy. What changed?” and “What are the three biggest risks across product lines?” Neither is a single-shot lookup. A multi-intent question has no single point in embedding space that represents it well, so top-k chunks come back as an average of competing sub-intents.
>
> Agentic retrieval plans and iterates over retrieval and can generate a response in the same call. This post focuses on why classic retrieval falls short on multi-part questions, how the AgenticRetrieveStream API works (including request construction and trace parsing), and when to choose it over the standard Retrieve API.
>
> Why single-shot retrieval falls short
>
> A worked example makes the gap concrete. Suppose you have ingested 25 years of Amazon shareholder letters into a Managed Knowledge Base. Your first question is direct:
>
> “What is the most important message in the documents?”
>
> The standard Retrieve API returns five chunks by hybrid score. In our test corpus, the top result is high-scoring but low-value: it covers the Amazon logo color scheme. The following chunks cover hiring, builders, and differentiation. The retriever did its job and ranked by similarity to the query embedding. But “most important message” is vague, and the scorer has no signal for what matters.
>
> Now escalate to a realistic question:
>
> “Compare how Amazon talked about hiring, long-term investment, and customer obsession in 2020 vs 2023. Where did emphasis shift?”
>
> Single-shot retrieval must now serve three intents across two time periods with one query vector. You get one of two outcomes: a scatter of loosely related chunks, or a tight cluster dominated by the strongest signal. Neither is what a human analyst would do.
>
> What a human analyst would do
>
> A human would decompose the question. They would search hiring in 2020, then hiring in 2023, then investment philosophy in each year. They would read the results, notice gaps, refine the search, and run it again. With enough evidence in hand, they would synthesize.
>
> Agentic retrieval automates this workflow as an API.
>
> Gaps left by single-shot retrieval
>
> Multi-part questions: A single embedding may not represent a multi-intent query well, so top-k results tend to blend intents together.
>
> Comparative reasoning: “Compare A and B across dimension X” requires targeted retrieval per item, not one blended search.
>
> Cross-source questions: When evidence spans multiple knowledge bases, static routing rules are brittle and might not adapt well per query.
>
> Sufficiency: Classic retrieval doesn’t judge “enough.” It returns k chunks regardless.
>
> Exploration: Some questions need follow-up searches based on what the first results reveal. Single-shot retrieval can’t iterate.
>
> Teams have addressed this gap with custom agent frameworks built on the Retrieve API. They prompt a model to plan and call Retrieve API in a loop, manage sub-queries, deduplicate, and decide when to stop. It works, but it becomes custom plumbing in every application, each instance carrying its own latency, cost, and reliability risks.
>
> What agentic retrieval is
>
> Agentic retrieval is a new retrieval mode in Amazon Bedrock Managed Knowledge Bases, available through the AgenticRetrieveStream API. Instead of one similarity search, it runs a planning loop driven by a foundation model: the model decomposes your question, retrieves against each part, judges whether it has enough evidence, and iterates as needed. It generates a grounded response by default in the same call. Set generateResponse=False to return retrieval results without generating a response.
>
> You see every step of that loop as an ordered stream of trace events. Each event carries a step and a status, so you can see what the planner did and why:
>
> SpeculativeRetrieval: An initial retrieval that runs before the first planning step to reduce end-to-end latency. With a single KB, it uses the raw user query. With multiple KBs, it is a probe search used to route sub-queries. It doesn’t count toward maxAgentIteration.
>
> Planning: The foundation model (FM) analyzes the query, reviews prior results, and emits sub-queries aligned to retrievable intents. Between iterations, this is also where the model judges sufficiency and decides whether to stop or search again.
>
> Retrieval or FullDocumentExpansion: One event per sub-query execution, each with its own status. In agentic retrieval, this action/event can fetch a full document if the agent determines that the passage context is insufficient to answer the query. Often, queries that require summarization, listing elements, or information from various parts of a document benefit from this action. The loop may run several iterations if more evidence is needed, bounded by maxAgentIteration.
>
> Result: The final event. It contains the deduplicated source chunks collected across the iterations. For multi-KB requests, each chunk identifies its sourceRetriever. Because response generation is enabled by default, the result event also contains the grounded answer and citations unless you set generateResponse=False.
>
> A note on deduplication and the trace. Deduplication applies only to the final result event. When multiple sub-queries retrieve the same chunk, that chunk appears only once in the final results. Trace events remain available for reviewing the individual planning and retrieval steps.
>
> Two parameters do most of the tuning. The first is maxAgentIteration, the ceiling on planning-plus-retrieval iterations. Use 3 for a single KB and 4–5 for multi-KB or comparative queries, though the planner may exit early after its evaluation step finds the evidence sufficient. See Quotas and limits for defaults and maximums.
>
> The second is the foundation model configuration. The foundationModelType field determines whether agentic retrieval uses the service-managed model or a custom model. When you set it to CUSTOM, provide the model through foundationModelConfiguration.
>
> Note on pricing: Agentic retrieval is priced per call, and the model you choose for the orchestration sets the rate. With the managed model, you pay $4 per 1,000 agentic retrieval calls plus $1 per 1,000 underlying Retrieve API calls. If you choose a model available in Amazon Bedrock, you pay standard pass-through Bedrock pricing for that model plus the same $1 per 1,000 underlying Retrieve calls. See more details on the pricing page.
>
> API walkthrough
>
> Now that you have seen how the planning loop works, we examine the AgenticRetrieveStream API in practice.
>
> Single knowledge base
>
> The most direct case: one KB, one query, let the planner decompose. You send the request, then consume the stream, which delivers trace events, generated-response chunks when response generation is enabled, and a final result event.
>
> import boto3
>
> bedrock_agent_runtime = boto3.client(
>
> "bedrock-agent-runtime",
>
> region_name=REGION,
>
> )
>
> MODEL_ARN = (
>
> "arn:aws:bedrock:us-west-2:"
>
> "&lt;account-id&gt;:inference-profile/&lt;planner-model-id&gt;"
>
> )
>
> response = bedrock_agent_runtime.agentic_retrieve_stream(
>
> messages=[{"role": "user", "content": {"text": QUERY&#125;&#125;],
>
> retrievers=[
>
> {
>
> "configuration": {
>
> "knowledgeBase": {
>
> "knowledgeBaseId": KB_ID,
>
> "retrievalOverrides": {
>
> "maxNumberOfResults": 10,
>
> },
>
> }
>
> }
>
> }
>
> ],
>
> agenticRetrieveConfiguration={
>
> "foundationModelType": "CUSTOM",
>
> "foundationModelConfiguration": {
>
> "type": "BEDROCK_FOUNDATION_MODEL",
>
> "bedrockFoundationModelConfiguration": {
>
> "modelConfiguration": {
>
> "modelArn": MODEL_ARN,
>
> }
>
> },
>
> },
>
> "maxAgentIteration": 3,
>
> },
>
> )
>
> # Consume trace events, generated-response chunks, and the final result
>
> for event in response["stream"]:
>
> if "traceEvent" in event:
>
> attrs = event["traceEvent"]["attributes"]
>
> print(f"[TRACE] step={attrs.get('step')} status={attrs.get('status')}")
>
> if attrs.get("step") == "Retrieval":
>
> for chunk in attrs.get("retrievalResponse", []):
>
> preview = chunk.get("content", {}).get("text", "")[:60]
>
> print(f" {preview}")
>
> elif "responseEvent" in event:
>
> print(event["responseEvent"]["text"], end="", flush=True)
>
> elif "result" in event:
>
> print()
>
> for chunk in event["result"].get("results", []):
>
> source_retriever = chunk.get(
>
> "sourceRetriever", {}
>
> ).get("identifier", "")
>
> preview = chunk.get("content", {}).get("text", "")[:80]
>
> print(f"[RESULT] {source_retriever} | {preview}")
>
> That is the whole loop: one request, no orchestration code, and a stream you read top to bottom. The trace events tell you what the planner did. The result event gives you the deduplicated chunks. In production, log these trace events to Amazon CloudWatch for cost attribution, latency budgeting, and debugging. Each iteration is one planner invocation plus its sub-query retrievals, so the number of iterations is what drives both cost and wall-clock latency.
>
> Multiple knowledge bases
>
> Multi-KB routing is what agentic retrieval does that the other APIs cannot. Register up to five Managed KB retrievers in one request and attach a natural-language description to each. The planner reads those descriptions to route each sub-query to the most relevant KB.
>
> response = bedrock_agent_runtime.agentic_retrieve_stream(
>
> messages=[{"role": "user", "content": {"text": QUERY&#125;&#125;],
>
> retrievers=[
>
> {
>
> "configuration": {
>
> "knowledgeBase": {
>
> "knowledgeBaseId": KB_PRODUCT_DOCS,
>
> "retrievalOverrides": {
>
> "maxNumberOfResults": 10,
>
> },
>
> }
>
> },
>
> "description": "Public product documentation and API reference.",
>
> },
>
> {
>
> "configuration": {
>
> "knowledgeBase": {
>
> "knowledgeBaseId": KB_SUPPORT_TICKETS,
>
> "retrievalOverrides": {
>
> "maxNumberOfResults": 10,
>
> },
>
> }
>
> },
>
> "description": "Resolved customer support tickets and runbooks.",
>
> },
>
> ],
>
> agenticRetrieveConfiguration={
>
> "foundationModelType": "CUSTOM",
>
> "foundationModelConfiguration": {
>
> "type": "BEDROCK_FOUNDATION_MODEL",
>
> "bedrockFoundationModelConfiguration": {
>
> "modelConfiguration": {
>
> "modelArn": MODEL_ARN,
>
> }
>
> },
>
> },
>
> "maxAgentIteration": 5,
>
> },
>
> )
>
> You consume the stream the same way. The routing decision shows up in the result: each chunk carries a sourceRetriever ID, so you can see which KB answered which sub-query. The descriptions are the contract the planner routes on, so write each as a one-sentence pitch for its KB. Vague descriptions lead to vague routing.
>
> Choosing the right retrieval API
>
> Managed Knowledge Bases give you two query surfaces: Retrieve and AgenticRetrieveStream. You pick based on the shape of the question.
>
> Use Retrieve for short, well-scoped questions where one similarity search is enough. It has no planner, the lowest cost per call, and the tightest latency, and you keep full control over how you generate an answer.
>
> Use AgenticRetrieveStream when questions are multi-part, comparative, exploratory, or span multiple knowledge bases. It decomposes the question, retrieves per intent, evaluates sufficiency, and can generate a grounded response in the same call, or return chunks for you to synthesize with a model you control. It costs more and takes longer because it makes multiple model calls, but it finds evidence a single search can miss.
>
> Feature
>
> Retrieve
>
> AgenticRetrieveStream
>
> Output
>
> Raw chunks + relevance scores
>
> Deduplicated chunks (streaming), optional grounded answer
>
> Multi-KB support
>
> No
>
> Yes, up to 5.
>
> Query decomposition
>
> No
>
> Yes
>
> Streaming
>
> Sync only
>
> Always
>
> User query size, English text (characters)
>
> 10,000
>
> 10,000
>
> Foundation model cost per call
>
> None
>
> Multiple invocations
>
> Latency
>
> Lowest
>
> Highest
>
> Self-Managed KB (VECTOR)
>
> Yes
>
> No (Managed KB only)
>
> Relevance scores
>
> In results directly
>
> In trace events only
>
> Reranking
>
> Optional
>
> Optional (one reranker across retrievers)
>
> Guardrails
>
> Supported
>
> BLOCK only (MASK unsupported)
>
> How agentic retrieval performs on benchmarks
>
> We evaluated agentic retrieval on MuSiQue (Trivedi et al., 2022), a public benchmark of multi-hop questions. On these questions it showed 20 percent absolute recall improvement over single-shot retrieval, with the largest gains on the hardest questions. Single-hop questions show smaller gains (under five points).
>
> Each MuSiQue question is designed to require two, three, or four retrieval steps, and a human annotator identified the exact document chain needed to answer it. That chain is an oracle decomposition: the ideal retrieval plan to measure against.
>
> Question Complexity
>
> Δ (Gain) with Agentic Retrieve
>
> Agentic Hops (avg)
>
> 2-hop questions
>
> +22.8
>
> 1.98
>
> 3-hop questions
>
> +31.9
>
> 3.50
>
> 4-hop questions
>
> +37.3
>
> 4.78
>
> Two patterns stand out. First, the harder the question, the bigger the gain. The more steps a question requires, the more a single search misses, and the more agentic retrieval recovers. Questions that need several steps simply cannot be answered in one pass.
>
> Second, the system takes about as many steps as the question actually needs. The benchmark tells us the ideal number of steps for each question (the chain a human expert traced). Agentic retrieval’s own number of steps stays within roughly one of that ideal, so it searches enough to answer the question without wandering.
>
> Example
>
> We demonstrate how agentic retrieval solves a 4-hop query in the MuSiQue dataset.
>
> Query: “When did the explorer reach the headquarters location of the group Study in Brown’s record label is part of?”
>
> Agentic Retrieve Trace:
>
> Hop
>
> Retrieved Gold Documents (about)
>
> 0
>
> Study in Brown
>
> 1
>
> Emarcy Records
>
> 2
>
> The Right Stuff Records
>
> 3
>
> &lt;recovered same documents as 2&gt;
>
> 4
>
> Santa Monica California
>
> We illustrate the retrieval process using the following t-SNE plot over the corpus representation space. It shows how single-step Retrieve results (dotted-red boundary) compare to multi-step agentic retrieve. In each hop, agentic retrieve breaks down the query. It arrives at the document containing the answer.
>
> Best practices
>
> These practices reduce cost, improve latency, and keep agentic retrieval predictable in production.
>
> Start with a small, fast planner model. Agentic retrieval makes many short calls. A large planner rarely justifies the latency.
>
> Set maxAgentIteration based on scope. Use 3 for single-KB, 4–5 for multi-KB. Measure, then tune.
>
> Write retriever descriptions like product marketing. Be specific, concrete, and distinctive.
>
> Stream the trace to Amazon CloudWatch Logs with a correlation ID per request. This supports replay and debug.
>
> Plan costs by iterations, not by tokens alone. Iterations drive both cost and wall-clock latency.
>
> Combine with reranking. Agentic retrieval can use a reranking model to improve the relevance of retrieved results. For AgenticRetrieveStream, configure reranking through agenticRetrieveConfiguration.rerankingModelType. When using a custom reranking model, provide its configuration through agenticRetrieveConfiguration.rerankingConfiguration.
>
> Treat results as evidence, not as an answer. Synthesize with a model you control so you can enforce tone, citations, and guardrails.
>
> Security, governance, and observability
>
> Agentic retrieval inherits the access model of Managed Knowledge Bases. The calling AWS Identity and Access Management (IAM) principal needs four actions: bedrock:AgenticRetrieveStream to invoke the stream; bedrock:Retrieve and bedrock:GetDocumentContent, scoped to specific knowledge base ARNs, to retrieve passages and full document content; and bedrock:InvokeModelWithResponseStream to invoke the planner model and stream the generated response. For the full policy and setup, see the documentation.
>
> Two details are specific to agentic retrieval and worth calling out. Guardrails are configured through policyConfiguration.bedrockGuardrailConfiguration, and only the BLOCK action is supported; the MASK action is not supported with agentic retrieval. Because the planner generates intermediate sub-queries, those sub-queries are as important to audit as the final results. Log the full trace to Amazon CloudWatch so you can review what the planner searched for, not just what it returned.
>
> For observability, Managed Knowledge Bases emit CloudWatch metrics for invocations, client errors, server errors, and throttles. AgenticRetrieveStream also emits the TotalIterationCount metric. Managed knowledge base telemetry integrates with Amazon Bedrock AgentCore Observability. See the documentation for the full metric list, namespaces, and log routing options.
>
> Conclusion
>
> This post explained why single-shot retrieval falls short on multi-part questions, introduced the AgenticRetrieveStream API, and showed when to choose it over standard Retrieve. Agentic retrieval moves planning, iteration, and sufficiency evaluation into the Managed Knowledge Bases service, so you get a single, observable API with consistent security, logging, and cost behavior instead of custom orchestration in every application.
>
> Start with Retrieve for direct lookups, and reach for AgenticRetrieveStream when users ask multi-part, comparative, or exploratory questions, or when evidence spans multiple knowledge bases. To build your first agentic knowledge base, follow the companion notebook on GitHub. For API details, see the AgenticRetrieveStream API reference, or explore the feature in the Amazon Bedrock console.
>
> About the authors
>
> Omar Elkharbotly
>
> Omar is a Senior GenAI/ML Specialist Solutions Architect at AWS. He works with enterprise customers across the UK and Ireland to design and deploy generative AI and machine learning solutions using Amazon Bedrock, Amazon Bedrock AgentCore, and the broader AWS AI/ML stack to build scalable, production-ready applications.
>
> Shreya Pawaskar
>
> Shreya is a Delivery Consultant specializing in AI/ML at AWS Professional Services. She helps enterprise customers design and deploy agentic retrieval and generative AI solutions on Amazon Bedrock. She holds a Master’s degree in Computer Science from the University of California, Irvine. Outside of work, she enjoys hiking Bay Area trails and discovering new restaurants.
>
> Sailik Sengupta
>
> Sailik is a Senior Scientist in the Agentic AI team at AWS. They specialize in designing large scale retrieval and reranking systems, and alignment and decoding of language models. They hold a Ph.D. in Computer Science from Arizona State University and was awarded an IBM Ph.D. Fellowship for their work on AI-driven Cyber-defenses. Their work spans large language model alignment, embedding models, game theory, automated task planning, and cybersecurity, with contributions published at venues including ACL, ICLR, NAACL, AAAI, EMNLP, NeurIPS, etc. Outside of work, he loves to travel, hike, and read books.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。