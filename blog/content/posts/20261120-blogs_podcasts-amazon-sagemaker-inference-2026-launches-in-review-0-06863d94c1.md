---
title: "Amazon SageMaker Inference: 2026 launches in review, part 2"
date: 2026-11-20T11:13:52+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "生成式 AI", "Prompt 工程", "Advanced (300)", "Amazon SageMaker AI", "Announcements", "博客与播客"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:815a4e26730313192ea7bfff78767a7547cf14b31bdedb4bdbf07dae2b436259"
source_payload_sha256: "sha256:e5aa26dfaeb25fe0efeaeb220b6651d999683bd99eeb1be005ef55d5a9b3607a"
observation_id: obs_06863d94c187626f5c0040cd089396ebd8c0fde1a55f3f9834e8ca12590ad8ad
event_id: evt_5ebcb2b2ab3be8a3d2c7dbddc45b71e3f094c6c43c1242bb00b35da59258e2b9
revision_id: rev_90cf6fe2cc27fd2c0d6ca7348e952b49fd238994bf7507fffada2bb1d2cc9ad0
source_published_at: 2026-11-20T00:34:07Z
first_seen_at: 2026-11-20T03:12:04.575499Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: true
source_truncation_reason: "crawler_feed_content_limit"
source_support: 1.0
source_title_chars_original: 59
interpretation_sha256: "sha256:a8b5a240850899ea72d5895ad441b4f7dd446f196baa7335e43c623b5f5ae2ca"
description: "盘点 Amazon SageMaker 在 2026 年推出的推理能力更新，聚焦模型上线后的配置选型、GPU 资源利用、跨区域路由和延迟治理。内容通过一个客服助手团队，说明推理推荐、并发压测与部署的衔接方式。"
external_url: https://aws.amazon.com/blogs/machine-learning/amazon-sagemaker-inference-2026-launches-in-review-part-2
parent_observation_id: null
last_seen_at: 2026-11-20T03:12:04.575499Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/amazon-sagemaker-inference-2026-launches-in-review-part-2](https://aws.amazon.com/blogs/machine-learning/amazon-sagemaker-inference-2026-launches-in-review-part-2)
- **发布域名**: aws.amazon.com

## 要点解读

### 这是什么
盘点 Amazon SageMaker 在 2026 年推出的推理能力更新，聚焦模型上线后的配置选型、GPU 资源利用、跨区域路由和延迟治理。内容通过一个客服助手团队，说明推理推荐、并发压测与部署的衔接方式。

### 用在哪里
适合负责生成式模型服务、上线调优和成本控制的 ML/MLOps 团队，尤其适用于多 LoRA 适配器、多区域部署，以及设有 TTFT、吞吐量或成本目标的端点。

### 可以推断的
- 推测：将配置推荐接入 Python SDK、Studio 和编码代理，可能减少团队切换工具及重复执行压测的负担。
- 推测：跨区域、跨账户路由与自动推荐结合，可能使端点容量规划更适合纳入统一运维流程。

## 来源摘要/节选

> Once a model is in production, the questions change. Teams want to know which configuration the model should run on now that traffic is real, how to fit more models onto GPUs they already pay for, what to do when the next model is too large for one machine, why requests wait in one Region while GPUs sit idle in another, and why latency rose when nobody changed anything. This post takes those questions in the order teams usually meet them.
>
> For HyperPod Inference, it listed additional routing strategies, broader support for model serving frameworks, and expanded multi-Region networking. The Inference Gateway delivers the routing, and managed NVIDIA Dynamo is a new serving framework. For managed endpoints, the roadmap pointed to deeper integration with the rest of the AWS AI landscape. Inference recommendations now run from Amazon SageMaker AI Studio, the SageMaker Python SDK, and the coding agents engineers already use, and endpoints can now route requests across Regions and accounts.
>
> To keep each section concrete, we follow one hypothetical team through the blog post. In the spring, they launched a customer support assistant on a 70B-parameter model behind a single SageMaker AI endpoint, using the launches from part 1. By the fall, they need to support more product lines, adopt a larger reasoning model, serve customers in a second Region, and keep their GPU bill flat.
>
> The launches at a glance
>
> Figure 1: The five stages in this post and the launches in each
>
> Choose the right configuration from wherever you work
>
> The team picked its first configuration from a benchmark run in April. Since then, they have added four LoRA (Low-Rank Adaptation) adapters, one for each product line, and the product team has set a target of 500 milliseconds for time to first token (TTFT) at peak load. The April configuration was never tested against either change. The engineers who will re-run the analysis work in notebooks and coding agents, and few of them use the console.
>
> Inference recommendations launched in April as an API. Four updates since then make it available in more of the places teams work, and let it answer two harder questions: how many adapters an endpoint can carry, and how much concurrency it can take before it misses a latency target. A new agent skill brings the same expertise into coding agents.
>
> Inference recommendations in SageMaker AI Studio (July 2026)
>
> Blog: Launching UI for generative AI inference recommendations in Amazon SageMaker AI
>
> The April launch automated instance, container, and optimization selection through APIs. Inference recommendations are now also available in SageMaker AI Studio as a guided, low-code workflow. In Studio, choose Jobs, then Inference optimization. Choose a use-case profile (Interact, Generate, Summarize, or Custom), an optimization goal (minimize latency, maximize throughput, or minimize cost), and a model from SageMaker JumpStart, Amazon Simple Storage Service (Amazon S3), the Model Registry, or an existing SageMaker model.
>
> SageMaker AI benchmarks candidate configurations on real GPU infrastructure using NVIDIA AIPerf and applies techniques that match the goal, such as speculative decoding for throughput or kernel tuning for latency. You compare the ranked results by TTFT, inter-token latency, throughput, and cost, and then deploy the chosen configuration to a real-time endpoint from Studio.
>
> Inference recommendations in the SageMaker Python SDK v3 (August 2026)
>
> Blog: LLM optimization integration for Amazon SageMaker Python SDK
>
> Benchmarking and recommendations previously required SageMaker AI Studio or direct Boto3 calls. They are now part of the SageMaker Python SDK v3 (version 3.17.0 and later), the same interface teams use for training and deployment, so the workflow fits into notebooks, CI pipelines, and MLOps workflows. You can benchmark a live endpoint against your workload traffic, generate ranked recommendations for a latency, throughput, or cost goal, and deploy the top-ranked configuration to a real-time endpoint in a single call.
>
> The SDK also supports longer workflows. You can run recommendation jobs in parallel to compare serving frameworks such as LMI and vLLM, and you can resume from a completed job so that deployment happens in a different notebook or pipeline stage without re-running the benchmarks.
>
> LoRA adapter support in inference recommendations (September 2026)
>
> Developer guide: Get recommendations for models with LoRA adapters
>
> Many teams use LoRA adapters to specialize one foundation model for several use cases. Each adapter kept in GPU memory reduces the number of concurrent requests the endpoint can serve, and the right balance depends on the instance type, the number of adapters, and the traffic profile.
>
> Inference recommendations now accept adapters as Model Package Amazon Resource Names (ARNs), for adapters produced by SageMaker fine-tuning, or as S3 URIs, for adapters from external pipelines such as Hugging Face PEFT. SageMaker AI benchmarks combinations of adapter count and concurrency on real GPU infrastructure and returns ranked results for your workload. The output lists both formats for every adapter. The recommended deployment uses SageMaker Inference Components, with one component for the base model and one for each adapter, so you can add, update, or remove an adapter without disrupting the base model or the other adapters.
>
> SLA-based concurrency search (September 2026)
>
> Blog: Right-size generative AI endpoints with concurrency sweeps on Amazon SageMaker AI
>
> Right-sizing an endpoint means finding the highest concurrency it can sustain without breaching latency or error targets. Until now, that meant picking concurrency levels by hand, running a sweep, checking the results against the service level agreement (SLA), and repeating with a narrower range whenever the model or instance changed.
>
> Inference recommendations now include a search that finds that boundary directly. Set search_recipe to max-concurrency-under-sla and supply targets for any combination of maximum TTFT, maximum time per output token, maximum end-to-end latency, and maximum error rate. The benchmarking engine (AIPerf) starts from a broad range, narrows it based on which probes pass or fail, and converges in fewer iterations than a linear sweep. The result reports the largest passing concurrency (feasible_max) or, if no level qualifies, the smallest failing one (infeasible_min).
>
> The search uses the same CreateAIWorkloadConfig and CreateAIBenchmarkJob APIs as concurrency sweeps. Optional parameters (concurrency_min, concurrency_max, search_max_iterations, and search_initial_points) bound the cost and speed up convergence.
>
> Agent skill for optimized generative AI inference (October 2026)
>
> Blog: New agent skill: Amazon SageMaker optimized generative AI inference for your coding agent
>
> Engineers increasingly ask their coding agent which instance and container to use. Without grounded knowledge and access to real benchmarks, the agent can only guess, and a wrong instance choice shows up later as missed latency targets or wasted spend.
>
> The aws-ai-ml skill, available through the Agent Toolkit for AWS, gives coding agents such as Kiro built-in SageMaker AI inference expertise. Engineers describe what they need in plain language, and the agent can do the following:
>
> Find the right instance. Ranked deployment options with measured throughput, latency, and TTFT for a model in Amazon S3, SageMaker JumpStart, or the Hugging Face Hub.
>
> Benchmark a live endpoint. A report from real load covering throughput, P50 and P99 latency, inter-token latency, and supported concurrency.
>
> Compare runs. The percentage change on every metric, which shows whether a configuration change helped.
>
> Answers are grounded in measured performance and delivered as SageMaker Python SDK v3 code that engineers review and run under their own credentials. Setup takes about 10 minutes. The skill works with any agent that supports the Model Context Protocol (MCP) and in SageMaker AI Studio JupyterLab spaces.
>
> For the support team, one recommendation job that includes all four adapters, followed by a concurrency search against the 500 millisecond TTFT target, replaces the manual sweeps they ran in April. The engineer who owns it can start the job from a notebook or ask a coding agent to run it.
>
> Fit more models onto each GPU
>
> The support assistant does not run alone. An embedding model, a reranker, and a small classifier that routes tickets live in the same account, and each uses a fraction of a GPU. On a standard endpoint, each model copy still held a whole accelerator, so the team ran out of placement slots while GPU memory sat unused.
>
> Inference Components in the SageMaker AI console (October 2026)
>
> With Inference Components, you can host several models on one endpoint and size and scale each model separately. Until now, they were available only through the SDK and the AWS Command Line Interface (AWS CLI). Every create, resize, and scaling policy had to be scripted, and there was no single view of what each model was using.
>
> In the SageMaker AI console, you can now create, view, update, and delete inference components:
>
> Create and edit. Create an endpoint with inference components, add or delete components later, and change each component’s accelerators, CPU, memory, and copy count.
>
> Scale each model. Set an automatic scaling policy for each component, down to zero copies, so an idle model stops holding accelerators.
>
> Monitor. See alarms and per-component metrics on the same page.
>
> The console calls the same SageMaker AI APIs as the SDK and CLI, so teams can start on the console and automate later, or manage scripted components visually.
>
> GPU partitioning with NVIDIA Multi-Instance GPU (October 2026)
>
> Blog: SageMaker Inference now supports Multi-Instance GPU to maximize GPU utilization for model endpoints
>
> GPU partitioning uses NVIDIA Multi-Instance GPU (MIG) technology to divide one physical GPU into as many as seven partitions, depending on the accelerator. Each partition has dedicated GPU compute and memory, with complete hardware isolation. You define the partition layout when you create an endpoint for inference components and choose a partition type for each component. Applications keep invoking models by inference component name, so client code does not change.
>
> MIG isolates GPU compute and memory between partitions. Models on the same instance still share host CPU, host memory, networking, storage, and endpoint routing. You pay the standard rate for the full instance-hour, so the saving comes from placing more models on each instance, not from a lower hourly price.
>
> Figure 2: Three small models on three GPUs, compared with the same models in partitions of one GPU
>
> For the support team, the embedding model, the reranker, and the classifier now run in separate partitions of one GPU on a single endpoint, and the team manages every component, including the assistant and its adapters, from the console.
>
> Serve models larger than one instance
>
> The team’s next model is a reasoning model whose weights alone exceed the GPU memory of any single instance. They have also noticed that long, retrieval-heavy prompts slow token generation for every other user on the endpoint. For a model this size, they move the workload to HyperPod Inference, which gives them dedicated clusters and Kubernetes-native control. The support assistant stays on managed endpoints.
>
> Managed NVIDIA Dynamo on HyperPod Inference (November 2026)
>
> Blog: Managed NVIDIA Dynamo on Amazon SageMaker HyperPod Inference
>
> Part 1 covered two building blocks for large models on HyperPod: disaggregated prefill and decode in Inference Operator v3.2, and KV-aware routing as part of the managed tiered KV cache. This launch adds multi-node serving and changes who operates the stack. NVIDIA Dynamo is an open source inference framework that provides multi-node sharded serving, disaggregated prefill and decode, and KV-aware routing. Teams could already run Dynamo on their own Kubernetes clusters, but they had to build and operate everything around it: placing all the nodes of a replica together, wiring Elastic Fabric Adapter (EFA) networking so prefill can hand its KV cache to decode at hardware speed, maintaining serving images, and recovering when one failed node takes down a multi-node replica.
>
> With this launch, Dynamo runs as a managed serving engine on HyperPod. Dynamo makes the serving decisions: how the model is sharded, how prefill and decode are split, and where each request goes. HyperPod provides what those decisions depend on:
>
> Capacity and networking. GPU capacity and EFA networking, provisioned and wired automatically.
>
> Node recovery. Node health monitoring and replacement, with multi-node workers rescheduled automatically when a node fails.
>
> Endpoint operations. Autoscaling, endpoint registration, TLS, and observability.
>
> One install and upgrade path. The Inference Operator add-on installs Dynamo, the serving images, and the Grove and KAI schedulers as one unit and upgrades them together.
>
> The capabilities Dynamo brings to HyperPod are:
>
> Multi-node (sharded) serving. One copy of the model spans several nodes, so you can serve models that do not fit on any single instance.
>
> Disaggregated prefill and decode. Prompt processing and token generation run on separate GPU pools, each on an instance type suited to its work, so a long prompt no longer slows responses for other users.
>
> KV-aware routing. Each request goes to the worker that already holds its KV cache, which reduces TTFT.
>
> There are three ways to start. Teams running Dynamo on self-managed Kubernetes can bring their existing DynamoGraphDeployment (DGD) manifests largely unchanged. Teams already on HyperPod Inference can update the add-on and add a short dynamoSpec block to an existing InferenceEndpointConfig, which HyperPod converts into a DGD, while existing endpoints keep serving. Teams new to both can create a cluster with the add-on and Dynamo enabled from the console. In each case, clients call a standard OpenAI-compatible endpoint, so client code does not change.
>
> Managed Dynamo supports vLLM, SGLang, and TensorRT-LLM, and is available in the Regions where Amazon SageMaker HyperPod is available.
>
> Figure 3: Managed NVIDIA Dynamo on HyperPod Inference
>
> For the support team, the reasoning model runs as one sharded replica across several nodes, with separate prefill and decode pools. When a node fails, HyperPod replaces it and reschedules the replica without a page to the on-call engineer.
>
> Send each request to a GPU that can serve it
>
> The support assistant now serves customers in North America and Europe, so the team runs endpoints and HyperPod clusters in two Regions. During the US morning peak, requests queue in the US Region while GPUs the team already pays for sit idle in Europe. Some European traffic must also stay in Europe.
>
> Routing decides whether capacity a team owns does useful work. It happens at four levels, and the launches below cover one level each: which instance serves a request inside an endpoint, which pod inside a HyperPod cluster, which cluster across a fleet, and which Regional endpoint across Regions and accounts.
>
> Figure 4: Routing across Regions and inside each endpoint or cluster, on both deployment paths
>
> KV-cache-aware routing for endpoints (November 2026)
>
> Blog: Amazon SageMaker AI real-time endpoints now support KV cache aware routing
>
> Applications with long prompts or multi-turn conversations repeat a large prefix across requests. A model server can reuse the matching KV cache, but only if the next request reaches the instance that holds it. Prefix-aware routing, covered in part 1, fingerprints the start of each prompt and sends matching prompts to the same instance. Because it works from request history, its view of each instance’s cache becomes less accurate as the model server adds and evicts entries.
>
> KV-cache-aware routing uses the cache state the model container reports. The container publishes cache creation and eviction events to a central cache index, and SageMaker AI routes each request to an eligible instance that holds the longest matching cached prefix. This raises cache reuse for long-context prompts, multi-turn conversations, and workloads that share dynamic prompt prefixes.
>
> It works with single-model endpoints and endpoints that use inference components, including LoRA adapters. It supports InvokeEndpoint, InvokeEndpointWithResponseStream, and the OpenAI-compatible API for Completions and Chat Completions payloads. You turn it on in the endpoint configuration. The first release requires an AWS-verified model container that implements the cache-event, tokenization, metrics, and OpenAI-compatible interfaces. You can track KV cache hit rate in detailed inference observability.
>
> Which one to use. Prefix-aware routing works with any container and needs no container changes. KV-cache-aware routing needs a verified container and tracks the actual cache, which helps most when prefixes vary or caches turn over quickly.
>
> Inference Gateway for HyperPod (September 2026)
>
> Blog: Introducing Amazon SageMaker HyperPod Inference Gateway
>
> Inside a HyperPod cluster, capacity and demand rarely line up. One pod can be partway through a long-context request with its KV cache nearly full, while the next pod sits idle or already holds the prompt prefix or LoRA adapter the next request needs. Without visibility into that GPU state, new requests queue behind busy pods, and teams add GPUs to protect latency instead of using the ones they have. Each model also had its own endpoint, so clients had to track one endpoint per model.
>
> The Inference Gateway is a GPU-aware router that installs with the HyperPod Inference Operator add-on and gives each cluster one OpenAI-compatible endpoint for all of its models. For each request, it reads live signals from every model pod and picks the best one, with weights you can tune per workload:
>
> KV cache utilization. Avoids pods whose cache is nearly full.
>
> Queue depth and running requests. Avoids pods with a backlog and balances active work.
>
> Prefix cache hit rate. Prefers pods likely to hold the prompt prefix.
>
> LoRA adapter residency. Prefers pods that already hold the requested adapter, which avoids swap latency.
>
> Compared with round-robin routing, it reduced P99 TTFT by up to 97% on mixed GPU generations and by up to 98% under bursty traffic. It is available in all Regions where SageMaker HyperPod is available.
>
> Cross-Region Inference Routing in Amazon SageMaker AI
>
> Blog: Keep inference running through regional capacity shortfalls with cross-Region inference routing in Amazon SageMaker AI
>
> On managed endpoints, the same idea takes the form of the Cross-Region Inference Routing, managed routing that sends real-time and asynchronous requests across Regional endpoints a team has already deployed, in the same account or in different accounts. You group endpoints that serve the same model under a routing target, and the application invokes the target instead of a specific Regional endpoint. The router does not add capacity, replicate models, or deploy endpoints, and the existing invocation path keeps working.
>
> The router replaces the failover logic teams build themselves today:
>
> One invocation path. SageMaker tries the local endpoint first and moves traffic to another registered endpoint when the local one cannot serve a request.
>
> One routing policy. The policy combines endpoint metrics with service-side capacity signals, including insufficient capacity errors that customers cannot observe on their own.
>
> Private connectivity. Cross-Region traffic runs over AWS PrivateLink with a managed cross-account authorization model, so routing to another Region or account does not need internet or NAT gateways.
>
> Overflow and residency guardrails. The endpoint owner can cap how much cross-Region traffic a fallback endpoint accepts, and the application can restrict which Regions may serve a request.
>
> Figure 5: Cross-Region Inference Router request flow
>
> Keep endpoints tuned after launch
>
> Two months after the move, the team adds retrieval to the support assistant, and the average prompt length roughly doubles. TTFT is now higher than it was at launch, but nothing has failed, so every alarm stays green. When the team finds a better configuration, they will need to roll it out on large GPU instances that are hard to get more of.
>
> Continuous performance monitoring (November 2026)
>
> Blog: Amazon SageMaker AI now detects latency drift, idle GPUs, and missed optimizations on your inference endpoints
>
> Amazon SageMaker AI now continuously monitors your generative AI inference endpoints and tells you when a change could improve performance or lower cost. Monitoring is on by default for SageMaker AI inference endpoints, with no setup required, and you can opt out of endpoints. SageMaker AI looks only at operational signals: latency, GPU utilization, and the endpoint’s serving configuration. It does not read your requests or responses. When a finding clears its confidence threshold, a notification appears on the AWS Management Console, and the same message arrives by email for teams that work in notebooks and the CLI. The recommended action opens the SageMaker AI agentic experience in SageMaker AI Studio with the finding already filled in, so the analysis, the comparison, and the deployment change happen in one conversation. Nothing deploys until you apply it, and you can turn monitoring off at any time.
>
> There are three types of findings:
>
> Latency drift after a traffic change. When a change such as added retrieval lengthens prompts, TTFT rises. The finding quantifies the regression week over week and recommends re-running inference recommendations against recent traffic to find a configuration that brings TTFT back down.
>
> A configuration gap present since deployment. The endpoint was never well tuned for its workload, and the finding points to the change that would close the gap.
>
> Idle GPU capacity. When capacity stays unused week after week, the finding flags a chance to right-size the endpoint and reduce cost.
>
> In-place rolling model updates (November 2026)
>
> A standard rolling update replaces an endpoint one batch at a time, and every batch runs on newly provisioned instances. On a large GPU fleet, that means finding new capacity at every step, and an update can fail partway through when the next batch of instances is not available. Each released instance must also finish cleanup before it can be used again, which slows the rollout.
>
> SageMaker AI now updates models in place. It provisions one small batch of additional instances at the start, shifts traffic to that batch, and then updates the instances it frees, reusing them to roll the change across the rest of the fleet. The update still rolls out in stages, but it needs new capacity only once. For a fleet of 20 instances with a batch size of 2, the update acquires 2 new instances instead of 20. Customers do not need to change anything. As with container caching in part 1, the improvement applies automatically to rolling model updates.
>
> Figure 6: A rolling update acquires new instances at every step. An in-place rolling update acquires one batch at the start and reuses the rest of the fleet
>
> For the support team, a Drift Watch finding quantifies the TTFT regression and opens a new recommendation job against recent traffic. They roll out the updated model with one batch of extra instances, instead of finding new GPU capacity for every instance in the fleet.
>
> Summary: 13 launches, continuing from part 1
>
> The numbering continues from the 13 launches in part 1.
>
> 14. Inference recommendations in SageMaker AI Studio (July 2026). A guided, low-code workflow for ranked, benchmarked configurations, with deployment from Studio.
>
> 15. Inference recommendations in the SageMaker Python SDK v3 (August 2026). Benchmark, recommend, and deploy from a notebook or pipeline, with parallel and resumable jobs.
>
> 16. LoRA adapter support in inference recommendations (September 2026). Benchmarks adapter count against concurrency and deploys adapters as inference components.
>
> 17. SLA-based concurrency search (September 2026). Finds the highest concurrency that meets TTFT, latency, and error-rate targets.
>
> 18. Agent skill for optimized generative AI inference (October 2026). Instance selection, benchmarking, and run comparison from MCP-compatible coding agents.
>
> 19. Inference Components in the SageMaker AI console

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。