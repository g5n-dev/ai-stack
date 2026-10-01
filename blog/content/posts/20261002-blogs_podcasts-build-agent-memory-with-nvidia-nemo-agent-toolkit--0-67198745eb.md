---
title: "Build agent memory with NVIDIA NeMo Agent Toolkit and Amazon S3 Vectors"
date: 2026-10-02T02:56:36+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "机器学习", "Prompt 工程", "Advanced (300)", "Amazon Simple Storage Service (S3)", "Technical How-to", "博客与播客"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:e799821fc5d80032129991c34fdda2f8004d229b82dde308a5dff935a054d4d2"
source_payload_sha256: "sha256:8034800370e7bfa2c035268d2624f3214a26f61769e060b489ef0af7df04ba48"
observation_id: obs_67198745ebf529c8c209e54d56be0e93d5aabc176aa6799246283ea9d03a1b7a
event_id: evt_8aeb35feee6d6f8060447af81e8a0d10287d077ddd8371144a127a7f07e1fe7c
revision_id: rev_060e76327b5fa3af63e10f6f1672240e44e3229a02ba3b192de6541d40c63ffb
source_published_at: 2026-10-01T17:34:56Z
first_seen_at: 2026-10-01T19:08:32Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 71
interpretation_sha256: "sha256:b0ffbaa07520f3c965a07665cc5c8a8f1c163d635a90ee831e1046d418615f36"
description: "这篇内容展示如何把 Amazon S3 Vectors 作为持久化记忆后端，集成到 NVIDIA NeMo Agent Toolkit 的记忆子系统中，并在 Amazon EKS 上完成部署。"
external_url: https://aws.amazon.com/blogs/machine-learning/build-agent-memory-with-nvidia-nemo-agent-toolkit-and-amazon-s3-vectors
parent_observation_id: null
last_seen_at: 2026-10-01T18:54:50.149499Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/build-agent-memory-with-nvidia-nemo-agent-toolkit-and-amazon-s3-vectors](https://aws.amazon.com/blogs/machine-learning/build-agent-memory-with-nvidia-nemo-agent-toolkit-and-amazon-s3-vectors)
- **发布域名**: aws.amazon.com

## 要点解读

### 这是什么
这篇内容展示如何把 Amazon S3 Vectors 作为持久化记忆后端，集成到 NVIDIA NeMo Agent Toolkit 的记忆子系统中，并在 Amazon EKS 上完成部署。

### 用在哪里
适用于需要在多代理 AI 系统中长期保存向量检索记忆、并已在 AWS 环境使用 Kubernetes 的开发团队。

### 可以推断的
- 推测：通过实现插件接口，可把 S3 Vectors 的语义检索能力直接用于代理的记忆查询。  
- 推测：该方案主要面向对写入一致性、弹性扩展和成本控制有较高要求的大规模生产系统。

## 来源摘要/节选

> In my previous post: Building persistent memory for multi-agent AI systems with Amazon S3 Vectors, we explored why memory engineering is the foundational discipline for production multi-agent systems. We showed how Amazon S3 Vectors, a capability of Amazon Simple Storage Service (Amazon S3), meets the architectural requirements for agent memory: semantic retrieval, rich metadata, strong consistency, and elastic scale.
>
> In this post, we move from architecture to implementation. We show you how to use Amazon S3 Vectors as the persistent memory layer within the NVIDIA NeMo Agent Toolkit (NAT), deployed on Amazon Elastic Kubernetes Service (Amazon EKS) for full operational control.
>
> By the end of this post, you will understand how NAT’s memory subsystem works and how to implement Amazon S3 Vectors as a custom memory provider. You will also learn how to deploy the stack on Amazon EKS, using a multi-agent investment research use case as the running example.
>
> What is NVIDIA NeMo Agent Toolkit?
>
> NVIDIA NeMo Agent Toolkit (NAT) is an open source framework for building, profiling, and optimizing AI agents. It’s framework-agnostic, working with Strands Agents, LangChain, LlamaIndex, CrewAI, and custom implementations. NAT provides four capabilities relevant to production agent systems:
>
> Agent orchestration – Define agents as composable workflows with configurable large language models (LLMs), tools, and prompts. You run them locally with nat run or as persistent services with nat serve.
>
> Profiling – Track token usage, latency, throughput, and run times across agents and individual tools to identify bottlenecks in multi-agent workflows.
>
> Evaluation – Built-in evaluators for answer accuracy, context relevance, response groundedness, and agent trajectory, with support for custom evaluators.
>
> Optimization – Automated hyperparameter tuning (temperature, top_p, max_tokens) that maximizes quality while minimizing cost and latency.
>
> NAT’s memory module
>
> NAT includes a dedicated memory subsystem designed to store and retrieve conversation history, user preferences, and long-term knowledge across agent invocations. The memory module is extensible: you create custom memory providers (backends) by implementing NAT’s plugin interface. Key components include:
>
> MemoryEditor – The abstract interface that all memory backends must implement. It defines three methods: add_items(), search(), and remove_items().
>
> MemoryItem – The data model representing a piece of memory, containing fields for conversation history, tags, metadata, user_id, and an optional textual memory string.
>
> MemoryBaseConfig – A Pydantic base class that custom memory configurations extend. NAT discovers providers via the _type field in its YAML config.
>
> Automatic memory wrapper – The auto_memory_agent workflow type that wraps agents with automatic memory capture and retrieval, without requiring the LLM to explicitly invoke memory tools.
>
> NAT currently has these built-in memory providers: Mem0, MemMachine, Redis, and Zep. These cover common use cases. However, for production multi-agent systems that require elastic vector storage, strong write consistency, and cost-efficient scaling to billions of vectors, a custom provider backed by Amazon S3 Vectors is the right fit.
>
> Why Amazon S3 Vectors as the persistent memory backend
>
> Building persistent memory for multi-agent AI systems with Amazon S3 Vectors covers the architectural rationale in depth. The following table summarizes the properties that make S3 Vectors the right fit for NAT’s memory layer:
>
> Requirement
>
> S3 Vectors capability
>
> Semantic retrieval
>
> Vector similarity search with configurable distance metrics (cosine, euclidean)
>
> Scoped queries
>
> Filterable metadata on each vector (strings, numbers, Booleans, lists)
>
> Multi-agent coordination
>
> Strong write consistency. Memories are visible immediately after insertion
>
> Scale
>
> Up to 2 billion vectors per index with no capacity planning
>
> Cost efficiency
>
> Pay only for storage, writes, and queries with no idle compute
>
> Access control
>
> AWS Identity and Access Management (IAM) policies per bucket and index. Per-tenant indexes for hard isolation
>
> Prerequisites
>
> To follow along with the implementation in this post, you need:
>
> An AWS account with permissions to create Amazon S3 Vectors resources and Amazon EKS clusters.
>
> An existing Amazon EKS cluster (see Getting started with Amazon EKS).
>
> NVIDIA NeMo Agent Toolkit installed (tested with version 1.6).
>
> Python 3.11 or 3.12 (NAT requires &gt;=3.11, &lt;3.14).
>
> An embedding model for generating vector representations (this post uses Amazon Titan Text Embeddings V2).
>
> kubectl and Docker for container and cluster operations.
>
> Implementing S3 Vectors as a NAT memory provider
>
> The implementation has three steps:
>
> Step 1: Create the S3 Vectors infrastructure
>
> Step 2: Implement a custom MemoryEditor plugin
>
> Step 3: Configure the agent workflow
>
> Figure 1: The three steps to implement Amazon S3 Vectors as a NAT memory provider
>
> Step 1. Create the Amazon S3 Vectors infrastructure
>
> The following code creates a vector bucket and an index with a metadata schema designed for agent memory. The index uses 1024 dimensions to match the output of Amazon Titan Text Embeddings V2, and it marks the large content field as non-filterable metadata:
>
> import boto3
>
> REGION = "us-west-2"
>
> VECTOR_BUCKET = "amzn-s3-demo-research-agent-memory"
>
> INDEX_NAME = "agent-long-term-memory"
>
> s3vectors = boto3.client("s3vectors", region_name=REGION)
>
> # Create the vector bucket
>
> s3vectors.create_vector_bucket(vectorBucketName=VECTOR_BUCKET)
>
> # Create the index (1024 dimensions matches Amazon Titan Text Embeddings V2)
>
> s3vectors.create_index(
>
> vectorBucketName=VECTOR_BUCKET,
>
> indexName=INDEX_NAME,
>
> dataType="float32",
>
> dimension=1024,
>
> distanceMetric="cosine",
>
> metadataConfiguration={"nonFilterableMetadataKeys": ["content"]},
>
> )
>
> After creating the bucket and index, you can implement the memory provider that reads from and writes to them.
>
> Step 2. Implement a custom MemoryEditor plugin
>
> The following code implements the MemoryEditor interface as an Amazon S3 Vectors backend and registers it so that NAT can discover it:
>
> import boto3
>
> import json
>
> import uuid
>
> from datetime import datetime, timezone
>
> from nat.plugin_api import MemoryBaseConfig, MemoryEditor, MemoryItem, register_memory
>
> from nat.builder.builder import Builder
>
> class S3VectorsMemoryConfig(MemoryBaseConfig, name="s3vectors_memory"):
>
> """NAT memory provider configuration for Amazon S3 Vectors."""
>
> vector_bucket: str
>
> index_name: str
>
> aws_region: str = "us-west-2"
>
> default_top_k: int = 5
>
> class S3VectorsMemoryEditor(MemoryEditor):
>
> """NAT MemoryEditor backed by Amazon S3 Vectors."""
>
> def __init__(self, config: S3VectorsMemoryConfig):
>
> self._vector_bucket = config.vector_bucket
>
> self._index_name = config.index_name
>
> self._default_top_k = config.default_top_k
>
> self._s3vectors = boto3.client('s3vectors', region_name=config.aws_region)
>
> self._bedrock = boto3.client('bedrock-runtime', region_name=config.aws_region)
>
> def _get_embedding(self, text: str) -&gt; list[float]:
>
> """Generate embeddings using Amazon Titan Text Embeddings V2."""
>
> response = self._bedrock.invoke_model(
>
> modelId='amazon.titan-embed-text-v2:0',
>
> contentType='application/json',
>
> accept='application/json',
>
> body=json.dumps({
>
> 'inputText': text,
>
> 'dimensions': 1024,
>
> 'normalize': True
>
> })
>
> )
>
> return json.loads(response['body'].read())['embedding']
>
> async def add_items(self, items: list[MemoryItem], **kwargs) -&gt; None:
>
> """Store memory items as vectors in Amazon S3 Vectors."""
>
> vectors = []
>
> for item in items:
>
> # Build the text to embed from the memory content
>
> text = item.memory or json.dumps(item.conversation)
>
> embedding = self._get_embedding(text)
>
> # Use uuid4 to prevent key collisions within the same second
>
> key = f"mem_{item.user_id}_{uuid.uuid4().hex[:12]}"
>
> # Note: S3 Vectors metadata values have size limits.
>
> # Truncate content to 1024 characters for production use.
>
> content_for_metadata = text[:1024]
>
> mem_metadata = {
>
> 'user_id': item.user_id,
>
> 'memory_type': item.metadata.get('memory_type', 'episodic'),
>
> 'agent_id': item.metadata.get('agent_id', ''),
>
> 'team_id': item.metadata.get('team_id', ''),
>
> 'task_id': item.metadata.get('task_id', ''),
>
> 'confidence': item.metadata.get('confidence', 0.8),
>
> 'created_at_epoch': int(datetime.now(timezone.utc).timestamp()),
>
> 'is_shared': item.metadata.get('is_shared', True),
>
> 'source': item.metadata.get('source', 'agent'),
>
> 'content': content_for_metadata,
>
> }
>
> # Add domain-specific metadata if present
>
> if 'ticker' in item.metadata:
>
> mem_metadata['ticker'] = item.metadata['ticker']
>
> vectors.append({
>
> 'key': key,
>
> 'data': {'float32': embedding},
>
> 'metadata': mem_metadata
>
> })
>
> self._s3vectors.put_vectors(
>
> vectorBucketName=self._vector_bucket,
>
> indexName=self._index_name,
>
> vectors=vectors
>
> )
>
> async def search(self, query: str, top_k: int = None, **kwargs) -&gt; list[MemoryItem]:
>
> """Retrieve semantically relevant memories from Amazon S3 Vectors."""
>
> query_embedding = self._get_embedding(query)
>
> effective_top_k = top_k or self._default_top_k
>
> # Build metadata filter from kwargs
>
> filter_expr = {}
>
> for field in ('agent_id', 'memory_type', 'ticker', 'team_id', 'user_id'):
>
> if field in kwargs:
>
> filter_expr[field] = {'$eq': kwargs[field]}
>
> # Support boolean filter for is_shared
>
> if 'is_shared' in kwargs:
>
> filter_expr['is_shared'] = {'$eq': kwargs['is_shared']}
>
> response = self._s3vectors.query_vectors(
>
> vectorBucketName=self._vector_bucket,
>
> indexName=self._index_name,
>
> queryVector={'float32': query_embedding},
>
> topK=effective_top_k,
>
> filter=filter_expr if filter_expr else None,
>
> returnMetadata=True
>
> )
>
> results = []
>
> for vec in response.get('vectors', []):
>
> results.append(MemoryItem(
>
> conversation=[],
>
> tags=[vec['metadata'].get('memory_type', '')],
>
> metadata=vec['metadata'],
>
> user_id=vec['metadata'].get('user_id', ''),
>
> memory=vec['metadata'].get('content', '')
>
> ))
>
> return results
>
> async def remove_items(self, **kwargs) -&gt; None:
>
> """Remove memory items from Amazon S3 Vectors."""
>
> keys = kwargs.get('keys', [])
>
> if keys:
>
> self._s3vectors.delete_vectors(
>
> vectorBucketName=self._vector_bucket,
>
> indexName=self._index_name,
>
> keys=keys
>
> )
>
> # Register the memory provider so NAT can discover it
>
> @register_memory(config_type=S3VectorsMemoryConfig)
>
> async def build_s3vectors_memory(config: S3VectorsMemoryConfig, builder: Builder):
>
> yield S3VectorsMemoryEditor(config)
>
> The plugin generates embeddings with Amazon Titan Text Embeddings V2, stores each memory as a vector with scoped metadata, and translates search filters into Amazon S3 Vectors metadata queries.
>
> Step 3. Configure the NAT agent workflow
>
> With the plugin defined, configure it in NAT’s YAML config and wire it into an agent workflow:
>
> # config.yml - NAT agent configuration with Amazon S3 Vectors memory
>
> memory:
>
> agent_memory:
>
> _type: s3vectors_memory
>
> vector_bucket: "amzn-s3-demo-research-agent-memory"
>
> index_name: "agent-long-term-memory"
>
> aws_region: "us-west-2"
>
> functions:
>
> add_memory:
>
> _type: add_memory
>
> memory: agent_memory
>
> description: |
>
> Store important findings, patterns, or facts to long-term memory.
>
> Use this after discovering new information during research.
>
> get_memory:
>
> _type: get_memory
>
> memory: agent_memory
>
> description: |
>
> Retrieve relevant prior knowledge before starting research.
>
> Query with the current research topic to recall related findings.
>
> web_search:
>
> _type: web_search
>
> financial_data:
>
> _type: financial_data_api
>
> workflow:
>
> _type: auto_memory_agent
>
> inner_agent_name: research_agent
>
> memory_name: agent_memory
>
> llm_name: bedrock_llm
>
> save_user_messages_to_memory: true
>
> retrieve_memory_for_every_response: true
>
> save_ai_messages_to_memory: true
>
> llm:
>
> bedrock_llm:
>
> _type: bedrock
>
> model_id: "anthropic.claude-sonnet-4-20250514"
>
> temperature: 0.3
>
> With the auto_memory_agent wrapper, you can capture and retrieve memory automatically. User messages and agent responses are stored, and relevant context is injected before each agent call. This design removes the need for the LLM to explicitly invoke memory tools.
>
> Responsible AI and data handling considerations
>
> Because this solution persists conversation history and user memory, plan for how that data is retained and accessed. Set a retention policy for stored memories, and use the memory consolidation and removal paths in this post to expire data you no longer need. Avoid storing personally identifiable information (PII) in memory metadata, and redact or tokenize sensitive fields before you embed them. Scope access with per-tenant indexes and least-privilege IAM policies so that each agent reads and writes only the memory it owns.
>
> Putting Amazon S3 Vectors in practice: Multi-agent investment research
>
> The following use case demonstrates this pattern in practice. Consider three specialized agents collaborating on an investment research tool:
>
> Research Agent – Gathers market data, earnings reports, and news.
>
> Analysis Agent – Performs quantitative analysis and identifies patterns.
>
> Synthesis Agent – Produces reports combining findings from both agents.
>
> With persistent memory, each agent builds on prior work. The Research Agent recalls previously collected data, avoiding redundant API calls. The Analysis Agent builds on patterns identified in prior sessions. The Synthesis Agent accesses cumulative findings to produce progressively richer reports.
>
> Multi-agent memory coordination
>
> Each agent uses the same S3 Vectors index but writes with its own agent_id in the metadata. Agents retrieve shared knowledge using metadata filters:
>
> # Analysis Agent retrieves Research Agent's shared findings
>
> research_findings = await memory_client.search(
>
> query=f"Recent research findings for {ticker}",
>
> top_k=10,
>
> team_id='investment-research',
>
> is_shared=True
>
> )
>
> # Synthesis Agent queries all team knowledge
>
> all_team_knowledge = await memory_client.search(
>
> query=f"Complete analysis and research for {ticker} Q2 2026",
>
> top_k=20,
>
> team_id='investment-research'
>
> )
>
> NAT’s built-in multi-tenant memory isolation uses user_id to scope memory per user. For multi-agent team coordination, the team_id metadata field provides an additional grouping dimension within the same S3 Vectors index.
>
> Memory consolidation
>
> Over time, episodic memories accumulate. Periodically consolidating them into semantic memories (generalized knowledge) keeps retrieval precise and efficient. You can trigger consolidation through a scheduled cron job, a vector count threshold, or an agent-initiated signal after a configurable number of research cycles:
>
> async def consolidate_memories(ticker: str, memory_client, workflow):
>
> """Distill episodic memories into durable semantic knowledge."""
>
> episodes = await memory_client.search(
>
> query=f"All findings about {ticker}",
>
> top_k=50,
>
> memory_type='episodic',
>
> ticker=ticker
>
> )
>
> episode_texts = [e.memory for e in episodes if e.memory]
>
> consolidation_prompt = f"""Given these {len(episode_texts)} observations
>
> about {ticker}, identify durable patterns and generalized knowledge.
>
> {chr(10).join(episode_texts)}
>
> Return a JSON array of insight strings. Do not include specific dates
>
> or one-time events."""
>
> response = await workflow.run(consolidation_prompt)
>
> # Parse the response into a list of insights
>
> insights = json.loads(response)
>
> # Store each consolidated insight as semantic memory
>
> await memory_client.add_items([
>
> MemoryItem(
>
> conversation=[],
>
> tags=['semantic'],
>
> metadata={
>
> 'memory_type': 'semantic',
>
> 'confidence': 0.9,
>
> 'ticker': ticker,
>
> 'source': 'consolidation',
>
> 'is_shared': True,
>
> 'team_id': 'investment-research'
>
> },
>
> user_id='system',
>
> memory=insight
>
> )
>
> for insight in insights
>
> ])
>
> Deploying agent workloads on Amazon EKS
>
> Amazon EKS is a deliberate choice for teams that need full operational control over their agent workloads. With Amazon EKS, you control scaling, networking, and lifecycle management, and you integrate natively with AWS Identity and Access Management (IAM) for Amazon S3 Vectors access. If you prefer a fully managed runtime, Amazon Bedrock AgentCore provides a managed alternative that removes this operational overhead. You run NAT agents as containerized services using nat serve. Each agent type is a Kubernetes Deployment with IAM access granted through IAM Roles for Service Accounts (IRSA).
>
> Step 1: Build the agent container
>
> The following Dockerfile packages the agent with its configuration and memory plugin:
>
> FROM python:3.12-slim
>
> RUN pip install nvidia-nat[langchain] boto3
>
> COPY config.yml /app/config.yml
>
> COPY s3vectors_memory.py /app/s3vectors_memory.py
>
> WORKDIR /app
>
> CMD ["nat", "serve", "--config_file", "config.yml"]
>
> Step 2: Deploy with Kubernetes manifests
>
> The following manifests deploy the Research Agent with autoscaling:
>
> apiVersion: apps/v1
>
> kind: Deployment
>
> metadata:
>
> name: research-agent
>
> namespace: agent-team
>
> spec:
>
> replicas: 2
>
> selector:
>
> matchLabels:
>
> app: research-agent
>
> template:
>
> metadata:
>
> labels:
>
> app: research-agent
>
> team: investment-research
>
> spec:
>
> serviceAccountName: agent-sa
>
> containers:
>
> - name: agent
>
> image: ${ECR_REGISTRY}/research-agent:latest # Amazon Elastic Container Registry (Amazon ECR)
>
> ports:
>
> - containerPort: 8000
>
> env:
>
> - name: VECTOR_BUCKET
>
> value: "amzn-s3-demo-research-agent-memory"
>
> - name: INDEX_NAME
>
> value: "agent-long-term-memory"
>
> - name: AWS_REGION
>
> value: "us-west-2"
>
> resources:
>
> requests:
>
> cpu: "500m"
>
> memory: "1Gi"
>
> limits:
>
> cpu: "2000m"
>
> memory: "4Gi"
>
> ---
>
> apiVersion: autoscaling/v2
>
> kind: HorizontalPodAutoscaler
>
> metadata:
>
> name: research-agent-hpa
>
> namespace: agent-team
>
> spec:
>
> scaleTargetRef:
>
> apiVersion: apps/v1
>
> kind: Deployment
>
> name: research-agent
>
> minReplicas: 1
>
> maxReplicas: 10
>
> metrics:
>
> - type: Resource
>
> resource:
>
> name: cpu
>
> target:
>
> type: Utilization
>
> averageUtilization: 70
>
> IAM policy for S3 Vectors access
>
> The following IAM policy grants scoped access to the memory layer. Attach it to the IAM role associated with the agent-sa service account through IRSA:
>
> {
>
> "Version": "2012-10-17",
>
> "Statement": [
>
> {
>
> "Effect": "Allow",
>
> "Action": [
>
> "s3vectors:PutVectors",
>
> "s3vectors:QueryVectors",
>
> "s3vectors:GetVectors",
>
> "s3vectors:DeleteVectors"
>
> ],
>
> "Resource": "arn:aws:s3vectors:us-west-2:${ACCOUNT_ID}:vector-bucket/amzn-s3-demo-research-agent-memory/*"
>
> }
>
> ]
>
> }
>
> Deploy and verify
>
> After building and pushing the container image, deploy the agents:
>
> # Create the namespace
>
> kubectl create namespace agent-team
>
> # Apply the manifests
>
> kubectl apply -f kubernetes/research-agent-deployment.yaml
>
> # Verify pods are running
>
> kubectl get pods -n agent-team
>
> # Test the agent endpoint
>
> kubectl port-forward -n agent-team svc/research-agent 8000:8000
>
> curl -X POST http://localhost:8000/generate \
>
> -H "Content-Type: application/json" \
>
> -d '{"inputs": "What are the latest AAPL earnings trends?"}'
>
> S3 Vectors provides strong write consistency. Pods and agent types can immediately see memories that agent pods store, with no cache invalidation required. The HorizontalPodAutoscaler scales agent replicas based on CPU utilization. Each replica connects to the same S3 Vectors index through IRSA, supporting consistent memory access regardless of which pod handles a given request.
>
> Evaluating memory impact
>
> With NAT’s evaluation harness (nat eval), you can quantify the effect of memory on agent performance. Configure two evaluation runs: one with memory enabled and one without, using the same dataset:
>
> # Evaluate with memory enabled
>
> nat eval --config_file config_with_memory.yml \
>
> --dataset eval_dataset.jsonl \
>
> --metrics accuracy,groundedness,token_usage,latency
>
> # Evaluate without memory (baseline)
>
> nat eval --config_file config_no_memory.yml \
>
> --dataset eval_dataset.jsonl \
>
> --metrics accuracy,groundedness,token_usage,latency
>
> Based on the architectural properties of this design, you can expect the following qualitative outcomes when comparing these runs. These are directional expectations, not benchmarked measurements:
>
> Groundedness improves – Recalled memories provide verifiable source context that the agent can cite rather than relying on parametric knowledge alone.
>
> Token usage decreases – Agents skip re-deriving facts already established in prior sessions. The reduction scales with how much repeated context your workflows involve.
>
> Latency increases modestly – Each memory recall adds an S3 Vectors query (subsecond at standard access patterns), typically a small fraction of overall LLM inference time.
>
> Duplicate work drops – With shared memory, agents avoid repeating research or analysis that teammates have already completed.
>
> The magnitude of these effects depends on your workload: how much context is reused across sessions, how many agents coordinate, and how large your retrieval budget (top-k) is. NAT’s hyperparameter optimizer can systematically tune top_k and similarity threshold to find the optimal cost-quality trade-off for your use case.
>
> Clean up resources
>
> To avoid ongoing charges from resources created in this walkthrough, delete the following:
>
> Delete the Amazon EKS Deployment and associated resources:
>
> kubectl delete namespace agent-team
>
> Delete the S3 Vectors index and vector bucket:
>
> s3vectors.delete_index(vectorBucketName='amzn-s3-demo-research-agent-memory', indexName='agent-long-term-memory')
>
> s3vectors.delete_vector_bucket(vectorBucketName='amzn-s3-demo-research-agent-memory')
>
> Remove the IAM role and policy created for IRSA if no longer needed.
>
> Conclusion
>
> This post showed how to implement a custom NAT memory provider backed by Amazon S3 Vectors and deploy it on Amazon EKS. The key building blocks:
>
> NAT’s MemoryEditor interface provides the plugin contract for custom memory backends.
>
> The auto_memory_agent wrapper handles capture and retrieval automatically.
>
> Amazon S3 Vectors delivers the durable, semantically queryable backend with strong consistency for multi-agent coordination.
>
> Amazon EKS gives you full operational control over agent lifecycle, scaling, and network isolation.
>
> These patterns apply to domains where agents benefit from accumulated knowledge. They include classifying memory as episodic, semantic, or procedural, sharing memory across agents with metadata filtering, and consolidating memory with an LLM. Examples include customer support, DevOps automation, legal research, and scientific discovery.
>
> For the memory architecture foundations referenced throughout this post, see Building persistent memory for multi-agent AI systems with Amazon S3 Vectors. To get started with NAT, see the NVIDIA NeMo Agent Toolkit documentation and the Adding a Memory Provider guide.
>
> About the author
>
> Venkata Sistla
>
> Venkata is a Senior Specialist Solutions Architect at AWS, with over 12 years of experience in cloud architecture. He specializes in designing and implementing enterprise-scale AI/ML platforms across various industry sectors. He focuses on architecting highly scalable infrastructures that accelerate machine learning initiatives and deliver measurable business outcomes.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。