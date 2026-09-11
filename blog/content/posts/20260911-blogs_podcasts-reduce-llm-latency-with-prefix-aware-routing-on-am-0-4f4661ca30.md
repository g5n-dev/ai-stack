---
title: "Reduce LLM latency with prefix-aware routing on Amazon SageMaker Inference"
date: 2026-09-11T08:13:30+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "RAG", "AI Agent", "生成式 AI", "机器学习", "深度学习", "Prompt 工程", "Advanced (300)"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:a734d6216d1d095a839054659130ee3dddeaf9e5800dfba0f78adbd982fbddef"
source_payload_sha256: "sha256:4a5dddd0f3de1b9e48691a646c59776a67f19f980a3e8ba9ceaf92cc2e5a0fdc"
observation_id: obs_4f4661ca3038bcff734b931e86ecdd698705f1878edb8f11f9c4fd7242cb67ec
event_id: evt_32493d736fa6c798587ec7cb458ab5ad1b94318203cf27858d9f7813c0d4d605
revision_id: rev_4a7c4e31ef63c3af81daca8ba8f22ae29e67d392ef13136dc6b4902d74716524
source_published_at: 2026-09-10T21:58:09Z
first_seen_at: 2026-09-11T00:23:18Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 74
interpretation_sha256: "sha256:fc21993abc5a42b2eefdaf22c5ae9597a4ef235260982a5d5c87b981087ba265"
description: "该内容介绍了一种在模型推理入口根据请求前缀将相同前缀的请求路由到同一实例的策略，以利用已有的前缀缓存来降低首次响应时间并提升吞吐。"
external_url: https://aws.amazon.com/blogs/machine-learning/reduce-llm-latency-with-prefix-aware-routing-on-amazon-sagemaker-inference
parent_observation_id: null
last_seen_at: 2026-09-11T00:11:50.092788Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/reduce-llm-latency-with-prefix-aware-routing-on-amazon-sagemaker-inference](https://aws.amazon.com/blogs/machine-learning/reduce-llm-latency-with-prefix-aware-routing-on-amazon-sagemaker-inference)
- **发布域名**: aws.amazon.com

## 要点解读

### 这是什么
该内容介绍了一种在模型推理入口根据请求前缀将相同前缀的请求路由到同一实例的策略，以利用已有的前缀缓存来降低首次响应时间并提升吞吐。

### 用在哪里
适用于在多实例部署的 LLM 服务中，请求常常携带相同的指令或上下文，并且已开启前缀缓存的推理框架的业务场景。

### 可以推断的
推测：在请求前缀分布相对集中时，该路由方式有望显著减少首次响应时间；若前缀高度分散，收益可能有限。  
推测：系统在检测到目标实例接近并发上限时，会将请求转向其他实例，以防止单点过载。

## 来源摘要/节选

> When you build an application on top of a large language model (LLM), the prompt you send to the model typically has two parts. There’s a fixed part that sets up context (instructions, reference documents, conversation history) and a variable part that contains the actual user input. Take a customer service bot as an example. Each request starts with the same block of text: “You are a support agent for AnyCompany. Here are our policies…” followed by whatever the customer typed. The instructions at the top might be 3,000 tokens. The customer’s question at the bottom might be 50 tokens.
>
> This means that across hundreds or thousands of requests, your model is processing that same 3,000-token beginning over and over again.
>
> LLM serving frameworks like vLLM and TensorRT-LLM have a solution for this. They cache the computed key-value (KV) pairs for prompt prefixes that have been seen before. When the same beginning shows up in a new request, the model reuses the cached computation and only processes the new tokens at the end. This is called prefix caching, and it can reduce time-to-first-token (TTFT) significantly.
>
> But there’s a problem when you scale beyond a single instance. If you have a fleet of machines behind an endpoint, requests get distributed across all of them. That same 3,000-token prefix lands on instance A for one request, instance B for the next, instance C after that. Each instance computes it from scratch because none of them see it frequently enough to build a reliable cache. The prefix caching feature is there, but the routing layer spreads requests too thinly for it to help.
>
> Today, Amazon SageMaker Inference introduces prefix-aware routing. It is a new routing strategy that looks at the beginning of each request and consistently sends requests with the same beginning to the same instance. The KV cache on that instance actually builds up and gets reused. In our benchmarks on Llama 3.1 70B, this reduced P50 TTFT by up to 77 percent and increased throughput by up to 16 percent. It also pushed KV cache hit rates from roughly 25 percent to over 80 percent.
>
> What prefix-aware routing does
>
> When a request arrives at your endpoint, Amazon SageMaker looks at the beginning of the payload and uses it to decide which instance should handle it. The same beginning goes to the same instance. Different beginnings spread across different instances. If 10 requests share a prefix or beginning, all 10 go to the same machine, and that machine’s cache stays warm for that prefix.
>
> You don’t need to tag requests or manage affinity yourself. The endpoint handles it based on the content of the request.
>
> There are two built-in safeguards:
>
> Overload protection. If one prefix is extremely popular and the target instance is already at capacity, the endpoint routes the request to a less busy instance instead. You configure the concurrency limit, and the endpoint respects it. You might miss a cache hit on that one request, but you avoid overwhelming a single machine.
>
> Stable behavior during scaling. When you add or remove instances, most requests continue going to the same instance they were going to before. Only a small fraction of traffic shifts to account for the changed fleet. Your caches don’t get invalidated every time you scale.
>
> Performance benchmarks
>
> We benchmarked prefix-aware routing against the default random routing baseline using Llama 3.1 70B Instruct on 7 ml.p5.48xlarge instances with vLLM (prefix caching enabled). We ran 16 test configurations covering single model endpoints, inference component endpoints, the native Invoke API, and the OpenAI-compatible API. All tests completed with 100 percent success rate.
>
> Long context workloads
>
> 8,000-token shared prefixes, sustained over 1 hour:
>
> P90 TTFT: reduced by 33–37 percent.
>
> P50 TTFT: reduced by 71–77 percent.
>
> KV cache hit rate: from approximately 25–82 percent.
>
> Throughput: increased 15–16 percent.
>
> Short context workloads
>
> Variable-length ShareGPT-style conversations, 30 minutes:
>
> P90 TTFT: reduced by 24–37 percent.
>
> P50 TTFT: reduced by 13–16 percent.
>
> KV cache hit rate: from approximately 30–80 percent.
>
> Throughput: increased 1.7–2.0 percent.
>
> The longer your shared prefix, the bigger the win. Long context workloads benefit the most because there is more computation to skip on each cache hit. Short context workloads still benefit, but the shared prefixes are smaller so the savings per request are proportionally smaller.
>
> Routing overhead
>
> The prefix-aware routing logic adds 1.3–1.9 milliseconds per request. Model TTFT in these tests ranged 63–280 milliseconds. The routing cost is negligible.
>
> Traffic distribution remained balanced across all scenarios. Each of the 7 instances received 13.3–15.4 percent of requests, within 1 percent of an ideal even split. No hot spots.
>
> Routing strategies on SageMaker Inference
>
> With this launch, Amazon SageMaker Inference offers three routing strategies for real-time endpoints:
>
> RANDOM (default): Distributes requests uniformly across instances. Recommended for general-purpose workloads, non-LLM models, or a situation where requests are interchangeable and there’s no benefit to sending specific requests to specific instances.
>
> LEAST_OUTSTANDING_REQUESTS: Sends each request to the instance with the fewest in-flight requests. Recommended when request processing times vary and you want to keep all instances equally busy. Helps prevent slow requests from piling up on one machine while others sit idle.
>
> PREFIX_AWARE (new): Sends requests sharing the same prompt prefix to the same instance. Recommended for LLM workloads where many requests share common text at the beginning and your serving framework has prefix caching enabled.
>
> You set the strategy per production variant in your endpoint configuration. You can switch between them by updating the endpoint configuration without redeploying your model.
>
> When to use prefix-aware routing
>
> The feature delivers value when your requests share text at the beginning. Here are the patterns where it has the most impact:
>
> Retrieval Augmented Generation (RAG) applications. You retrieve a document and prepend it before the user’s question. When multiple users ask questions about the same document, they all share that document as a prefix. Prefix-aware routing sends them to the same instance, where the KV cache for that document is already warm.
>
> Multi-turn conversations. Each turn in a conversation includes the full history of previous turns. As the conversation grows, that shared history becomes a longer and more expensive prefix. Routing on that prefix keeps the conversation’s cache on one instance across turns.
>
> Templated bots and assistants. Bots with long, structured instructions (policies, formatting rules, persona definitions) send those same instructions with every request. Only the user message at the end changes. Prefix-aware routing means that expensive instruction block gets processed once, not thousands of times.
>
> Code completion. Coding assistants include file contents as context. While a developer works in the same file, every completion request shares that file content as a prefix.
>
> How to enable it
>
> You configure prefix-aware routing when you create your endpoint configuration. Two parameters control the behavior:
>
> PrefixLength (1024–65536): How much of the request to use for routing. For the native Amazon SageMaker Invoke API, this is bytes from the beginning of the request body. For the OpenAI-compatible API, this is characters from the extracted message text. Set this to cover your shared prefix plus enough unique content to spread different workloads across instances.
>
> ConcurrencyThreshold (1–1024): The maximum in-flight requests on the target instance before overflow kicks in. If the target instance is at this limit, the request goes to a less loaded instance instead.
>
> Here is an example:
>
> aws sagemaker create-endpoint-config \
>
> --endpoint-config-name example-llm-config \
>
> --production-variants '[{
>
> "VariantName": "AllTraffic",
>
> "ModelName": "example-llm-model",
>
> "InitialInstanceCount": 3,
>
> "InstanceType": "ml.p5.48xlarge",
>
> "RoutingConfig": {
>
> "RoutingStrategy": "PREFIX_AWARE",
>
> "PrefixAwareRoutingConfig": {
>
> "PrefixLength": 4096,
>
> "ConcurrencyThreshold": 10
>
> }
>
> }
>
> }]'
>
> Then create your endpoint as usual:
>
> aws sagemaker create-endpoint \
>
> --endpoint-name example-llm-endpoint \
>
> --endpoint-config-name example-llm-config
>
> No changes to your model container or serving framework are needed. Prefix-aware routing operates entirely at the endpoint routing layer.
>
> Invoking the endpoint
>
> Nothing changes about how you call the endpoint. The same InvokeEndpoint and InvokeEndpointWithResponseStream APIs work exactly as before:
>
> aws sagemaker-runtime invoke-endpoint \
>
> --endpoint-name example-llm-endpoint \
>
> --content-type application/json \
>
> --body fileb://request.json \
>
> output.json
>
> Same for the OpenAI-compatible Chat Completion API:
>
> from openai import OpenAI
>
> from sagemaker.core.token_generator import generate_token
>
> client = OpenAI(
>
> base_url=f"https://runtime.sagemaker.us-west-2.amazonaws.com"
>
> f"/endpoints/example-llm-endpoint/openai/v1",
>
> api_key=generate_token(region="us-west-2")
>
> )
>
> response = client.chat.completions.create(
>
> model="example-model",
>
> messages=[
>
> {"role": "user", "content": "What is your return policy?"},
>
> ],
>
> )
>
> Multi-tenant prefix isolation
>
> If different tenants share the same prompt instructions but you want them routed separately (to keep cache contexts independent), pass an optional ID:
>
> Native Invoke API: set the X-Amzn-SageMaker-Prefix-Aware-Id header (up to 64 ASCII characters).
>
> OpenAI API: include the prompt_cache_key field in the request body.
>
> This ID combines with the prefix so that requests with identical prefixes but different IDs land on different instances.
>
> Inference components and LoRA adapters
>
> Prefix-aware routing works with inference component endpoints and dynamic Low-Rank Adaptation (LoRA) adapters. For inference components, it behaves the same as single model endpoints. For LoRA adapters, it operates within the adapter’s sticky instance set, using prefix-based selection among the instances that already have the adapter loaded.
>
> Practical guidance
>
> Enable prefix caching in your serving framework. Prefix-aware routing gets repeated prefixes to the same instance, but your container needs prefix caching turned on to actually store and reuse those KV pairs. In vLLM, this is enabled by default in recent versions. Other frameworks might require explicit configuration.
>
> Keep request serialization consistent. For the native Invoke API, PrefixLength operates on raw bytes. JSON whitespace, key ordering, and formatting all affect routing. If you serialize the same prompt differently across requests, they might end up on different instances. Use consistent serialization.
>
> Size PrefixLength carefully. Too short and all requests with the same short prefix get funneled to one instance, triggering overflow. Too long and small payload differences (like temperature values) scatter requests that should stay together. Start with the length of your shared prefix plus a modest buffer.
>
> You need at least two instances. With one instance, all requests go to the same place regardless of strategy.
>
> Monitor cache hit rates. Enable SageMaker detailed observability to track KV cache hit rates at the model level. This confirms whether prefix-aware routing is working for your specific workload.
>
> Conclusion
>
> Prefix-aware routing is available today on SageMaker real-time inference endpoints. Update your AWS SDK or CLI to the latest version to access the new RoutingStrategy and PrefixAwareRoutingConfig parameters. Refer to this notebook for examples of how to enable it during endpoint creation.
>
> About the authors
>
> Kareem Syed-Mohammed
>
> Kareem is a Principal Product Manager at AWS. He focuses on enabling generative AI model development and governance on Amazon SageMaker HyperPod. Prior to this, at Amazon Quick Sight, he led embedded analytics and developer experience. In addition to Quick Sight, he has been with AWS Marketplace and Amazon retail as a Product Manager. Kareem started his career as a developer for call center technologies, Local Expert and Ads for Expedia, and management consultant at McKinsey.
>
> Vivek Gangasani
>
> Vivek is a Worldwide Leader for Solutions Architecture, SageMaker Inference. He leads Solution Architecture, Technical Go-to-Market (GTM) and Outbound Product strategy for SageMaker Inference. He also helps enterprises and startups deploy and optimize generative AI models and build AI workflows with SageMaker and GPUs. Currently, he is focused on developing strategies and content for optimizing inference performance and use cases such as agentic workflows and RAG. In his free time, Vivek enjoys hiking, watching movies, and trying different cuisines.
>
> Dmitry Soldatkin
>
> Dmitry is a Worldwide Leader for Specialist Solutions Architecture, SageMaker Inference at AWS. He leads efforts to help customers design, build, and optimize generative AI and AI/ML solutions across the enterprise. His work spans a wide range of ML use cases, with a primary focus on generative AI, deep learning, and deploying ML at scale. He has partnered with companies across industries including financial services, insurance, and telecommunications. You can connect with Dmitry on LinkedIn.
>
> Vamsi Goparaju
>
> Vamsi leads Go-to-Market (GTM) and Revenue Acceleration initiatives at AWS, enabling Inference and ModelOps workloads for our customers, and driving OSS Use Cases and Product features for Amazon SageMaker AI and Generative AI. With over 16 years of experience spanning AWS, Dell, and Infosys, he brings a unique blend of technical depth and business knowledge across Cloud, High-performance computing (HPC), Artificial Intelligence (AI), Machine Learning (ML), and Analytics. He holds an MBA from Texas A&amp;M University’s Mays Business School.
>
> Xu Deng
>
> Xu Deng is a Software Engineer Manager with the SageMaker team. He focuses on helping customers build and optimize their AI/ML inference experience on Amazon SageMaker. In his spare time, he loves traveling and snowboarding.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。