---
title: "Introducing Amazon SageMaker HyperPod Inference Gateway"
date: 2026-09-20T02:05:14+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "生成式 AI", "Prompt 工程", "Amazon SageMaker HyperPod", "Announcements", "Expert (400)", "博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:d201ca8e8aab25735cfa96a73ed2f91b4dd491a7e5fc3a943c9b52c284f7cee9"
source_payload_sha256: "sha256:331ed9e8296fd9691b689ba7c0efe9252321b49c05a8b9e59152750edf61dc8f"
observation_id: obs_69854448ea9a16b5342c6b707b26e88ff58603602bede43187b62463d30f8d3e
event_id: evt_492dffa1882672e72ac97056e787135993f948c9037aab206ce0f9a803d20b5e
revision_id: rev_0ba2943437205e619ab67fc9243e8caaf18df9297177ed57cd35ab8f0fb2b5e2
source_published_at: 2026-09-18T13:08:34Z
first_seen_at: 2026-09-19T18:01:13.003718Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 55
interpretation_sha256: "sha256:16d0db708ac29d8027387ea6f2d519bc15124e1b650b06d77f6e4e2193900e44"
description: "这是一款运行在 Amazon SageMaker HyperPod 集群上的 Kubernetes 原生路由插件，利用实时 GPU 指标（缓存占用、队列深度、LoRA 适配器驻留等）在请求入口处自动选择最优后端，以降低首 token 延迟并提升 GPU 利用率。"
external_url: https://aws.amazon.com/blogs/machine-learning/introducing-amazon-sagemaker-hyperpod-inference-gateway
parent_observation_id: null
last_seen_at: 2026-09-19T18:01:13.003718Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/introducing-amazon-sagemaker-hyperpod-inference-gateway](https://aws.amazon.com/blogs/machine-learning/introducing-amazon-sagemaker-hyperpod-inference-gateway)
- **发布域名**: aws.amazon.com

## 要点解读

### 这是什么  
这是一款运行在 Amazon SageMaker HyperPod 集群上的 Kubernetes 原生路由插件，利用实时 GPU 指标（缓存占用、队列深度、LoRA 适配器驻留等）在请求入口处自动选择最优后端，以降低首 token 延迟并提升 GPU 利用率。

### 用在哪里  
适用于在 EKS 环境下大规模部署大语言模型推理的团队，尤其是传统负载均衡导致 GPU 资源浪费或延迟波动的场景。只需安装一个 addon 并为已有模型 Pod 打标签，无需改动模型服务器或客户端代码即可启用。

### 可以推断的  
推测：该插件通过把路由决策从传统轮询或最小连接算法转向基于硬件状态的实时调度，能够显著减少因请求堆积而产生的卡顿。  
推测：两层架构的第二层（全局推理路由）尚未上线，说明当前仅支持单集群智能路由，跨集群失效转移与全局流量整形功能仍在开发阶段。

## 来源摘要/节选

> Eliminate GPU waste. Reduce first-token latency by up to 82%. Install one Kubernetes-native addon with zero application changes.
>
> The problem: Naive routing wastes your most expensive resource
>
> Running large language models (LLMs) at scale on GPU clusters is expensive. The default Kubernetes load balancers are making it worse. Round-robin and least-connections algorithms have no visibility into what’s happening inside your GPUs: which pods have saturated KV caches, which are mid-way through long-context generations, or which already have the LoRA adapter your request needs loaded in memory.
>
> The result? Round-robin routing causes requests to pile up behind busy pods while idle capacity remains unused. First-token latency spikes to 4+ seconds during traffic bursts. GPU utilization becomes uneven and unpredictable. You over-provision to compensate. This burns money on GPUs that aren’t doing useful work.
>
> The solution: SageMaker HyperPod Inference Gateway
>
> Today, we’re excited to announce Amazon SageMaker HyperPod Inference Gateway. It is a Kubernetes-native, GPU-aware routing system that deploys as a single EKS managed addon on your existing HyperPod infrastructure. It uses real-time GPU signals to place every inference request on the best-suited pod, delivering lower latency with no changes to your model servers or client applications.
>
> “A chatbot user waiting 4.4 seconds for the first token now sees it in under 800 ms.”
>
> How it works: Two-tier architecture
>
> The Inference Gateway uses a two-tier design built entirely on Kubernetes-native primitives.
>
> Figure 1: Two-tier architecture of the Inference Gateway
>
> Tier 1 — Per-cluster gateway (EKS managed addon)
>
> The first tier installs directly on each HyperPod/EKS cluster as the amazon-sagemaker-hyperpod-inference addon. It consists of three core components, all built on the open-source Gateway API Inference Extension:
>
> 1. Envoy Gateway
>
> High-performance L7 proxy that terminates incoming HTTPS traffic and exposes a single private endpoint per cluster.
>
> 2. Body-Based Router (BBR)
>
> Inspects each incoming OpenAI-compatible request body, extracts the model field, and routes to the correct model pool. Supports multi-model routing: one gateway, many models.
>
> 3. Endpoint Picker (EPP)
>
> The intelligence layer. EPP consumes real-time Prometheus metrics from every model-serving pod and uses a weighted scoring algorithm to select the best-suited backend:
>
> KV cache utilization — avoids pods whose key-value memory is nearly full.
>
> Queue depth — avoids pods with deep request backlogs.
>
> LoRA adapter residency — prefers pods that already have the requested adapter loaded.
>
> Prefix cache hit rate — prefers pods likely to serve from cached prompt prefixes.
>
> Running requests — balances active work across the fleet.
>
> Each scorer carries a configurable weight, so you can tune routing behavior for your specific workload (latency-sensitive chat compared to throughput-optimized batch).
>
> Tier 2 — Global Inference Router (GIR) (coming soon)
>
> The second tier adds fleet-wide coordination across multiple clusters and regions, with cross-cluster failover, global rate limiting, and cost-aware traffic shaping. Tier 2 builds on top of Tier 1. Each cluster’s per-cluster gateway continues to handle local intelligent routing.
>
> Getting started in 5 minutes
>
> The Inference Gateway deploys with a single addon install and a declarative InferenceGatewayConfig custom resource. No sidecars, no service mesh, no application code changes.
>
> Step 1: Install the addon
>
> aws eks create-addon \
>
> --cluster-name my-hyperpod-cluster \
>
> --addon-name amazon-sagemaker-hyperpod-inference \
>
> --addon-version v2.0.0-eksbuild.1 \
>
> --configuration-values '{"inferenceGateway": {"enabled": true}, "inferenceOperator": {"enabled": true&#125;&#125;'
>
> Step 2: Label your model pods
>
> Add a label to your existing model server deployments so the gateway can discover them:
>
> spec:
>
> template:
>
> metadata:
>
> labels:
>
> app: vllm-llama # The gateway matches on this
>
> Step 3: Apply the gateway configuration
>
> Create a single InferenceGatewayConfig resource that defines your models and routing behavior:
>
> apiVersion: inference.sagemaker.aws.amazon.com/v1alpha1
>
> kind: InferenceGatewayConfig
>
> metadata:
>
> name: my-gateway
>
> spec:
>
> tls: {}
>
> bbr:
>
> enabled: true
>
> schedulers:
>
> - name: llama-70b
>
> modelName: "llama-3.1-70b"
>
> modelSelector:
>
> matchLabels:
>
> app: vllm-llama
>
> targetPort: 8000
>
> scheduler: llm-d
>
> Step 4: Send inference requests
>
> The gateway exposes a standard OpenAI-compatible endpoint. Your existing client code works unchanged:
>
> curl -X POST "http://&lt;gateway-endpoint&gt;/v1/chat/completions" \
>
> -H "Content-Type: application/json" \
>
> -d '{"model": "llama-3.1-70b", "messages": [{"role": "user", "content": "What is Kubernetes?"}], "max_tokens": 100}'
>
> That’s it. No SDK changes. No SigV4 signing for inference traffic. Standard HTTP with an OpenAI-compatible schema.
>
> Multi-model routing
>
> Running multiple models on the same cluster? The Body-Based Router handles it natively. Define multiple schedulers in your config, and the gateway automatically routes each request to the correct model pool based on the model field in the request body.
>
> One gateway. Multiple models. Zero routing logic in your application.
>
> LoRA adapter routing
>
> Serving fine-tuned LoRA adapters on a shared base model? The Inference Gateway routes adapter requests to pods that already have the adapter loaded in GPU memory. This eliminates costly adapter swap latency.
>
> The EPP’s LoRA Affinity Scorer identifies which pods have the requested adapter resident and routes accordingly. If no pod has it loaded, the request goes to the pod with the most available capacity to load it quickly.
>
> Graceful failure and self-healing
>
> The gateway degrades gracefully at every level:
>
> Failure Scope
>
> Behavior
>
> Recovery
>
> Pod failure
>
> EPP excludes pods with stale metrics. Routes to healthy pods
>
> Automatic when metrics resume
>
> Pool exhaustion
>
> Returns HTTP 429 with Retry-After header
>
> Autoscaling adds capacity
>
> Cluster failure
>
> GIR detects stale heartbeat, redirects traffic within 35s
>
> Gradual ramp-up on reintroduction
>
> Regional failure
>
> Cross-region routing activates automatically
>
> Higher latency, no availability impact
>
> Built-in observability
>
> The gateway emits metrics at every layer, all surfaced through your existing monitoring stack:
>
> Pod level — KV cache utilization, queue depth, running requests, adapter residency (Prometheus).
>
> Pool level — Request totals, duration histograms, token counts (Prometheus/Grafana).
>
> Cluster level — Average KV cache, error rate, P99 latency (Amazon CloudWatch).
>
> Fleet level — Routing decisions, failover events, rate limit hits (CloudWatch).
>
> Benchmarking
>
> How much performance are you leaving on the table with default Kubernetes routing? To find out, we benchmarked four models ranging from 8B to 235B parameters, deployed on p5.48xlarge (H100) and g5 (A10G) instances. All traffic was routed through internal Application Load Balancers, matching the exact path a production request travels. A dedicated client node group generated controlled load while model servers ran in isolation on a separate server node group, ensuring zero resource contention under high concurrency. Every result that follows uses the gateway’s default routing configuration, with no tuning required.
>
> GPU-aware routing delivers the biggest gains exactly where round-robin struggles most. We tested three real-world scenarios across four models (8B to 235B parameters).
>
> Mixed GPU generations
>
> In production, GPU fleets are rarely uniform. When a smaller-memory instance saturates under traffic that its larger peers handle comfortably, round-robin keeps sending requests to overloaded pods. The Inference Gateway detects this imbalance in real time.
>
> Figure 2: Mixed GPU generations, round-robin baseline compared to the Inference Gateway
>
> Bursty traffic
>
> Bursty demand is the norm for most LLM workloads. A single replica cycles between overloaded and idle, creating latency spikes that round-robin cannot smooth out. The gateway absorbs these bursts by steering requests toward pods with available capacity.
>
> Figure 3: Bursty traffic, round-robin baseline compared to the Inference Gateway
>
> Shared prompt prefixes
>
> Workloads like multi-turn conversations and document Q&amp;A share a common prompt prefix across requests. The gateway’s Prefix Cache Hit Rate scorer routes these requests to pods that already have the prefix cached, avoiding redundant computation.
>
> Figure 4: Shared prompt prefixes, round-robin baseline compared to the Inference Gateway
>
> The pattern across all three scenarios is consistent: the more your fleet diverges from uniform, the more you gain. On a fully uniform fleet under steady traffic, replicas hold near-identical utilization, and the gateway performs on par with round-robin. This makes intelligent routing most valuable for the conditions production traffic actually creates: mixed hardware, bursty demand, and shared prompt prefixes. You can turn it on without hand-tuning anything first.
>
> Summary of performance improvements
>
> All figures are measured against a Kubernetes round-robin baseline on the same model replicas, using the gateway’s default routing configuration.
>
> Workload Condition
>
> TTFT P95
>
> TTFT P99
>
> Throughput
>
> Mixed GPU generations (Llama-3.1-8B)
>
> –97%
>
> –97%
>
> +8%
>
> Mixed GPU generations (Qwen3-32B)
>
> –98%
>
> –97%
>
> +50%
>
> Bursty traffic (Llama-3.1-70B)
>
> –94%
>
> –98%
>
> +12%
>
> Bursty traffic (Qwen3-235B)
>
> Comparable
>
> –89%
>
> Comparable
>
> Shared prompt prefix (Llama-3.1-8B)
>
> –26%
>
> –43%
>
> Comparable
>
> Uniform fleet, steady traffic (Qwen3-235B)
>
> Comparable
>
> Comparable
>
> Comparable
>
> “Comparable” means the difference fell within run-to-run variance.
>
> Why Kubernetes-native matters
>
> The Inference Gateway is not a separate platform you deploy alongside Kubernetes. It is Kubernetes:
>
> Gateway API conformant — built on the official Kubernetes Gateway API and its Inference Extension.
>
> Declarative config — one CRD (InferenceGatewayConfig) defines your entire routing topology.
>
> No lock-in — works with any OpenAI-compatible model server (vLLM, SGLang, TGI, and so on).
>
> Existing tooling — kubectl, GitOps, Helm, ArgoCD — all work as expected.
>
> EKS addon lifecycle — install, upgrade, and rollback through the aws eks CLI or console.
>
> Availability
>
> SageMaker HyperPod Inference Gateway (Tier 1, per-cluster routing) is available today in regions where inference add-on is available.
>
> What’s next
>
> Tier 2: Global Inference Router (GIR) — Cross-cluster and cross-region intelligent routing with a centralized fleet gateway, global rate limiting, and cost-tier-aware traffic shaping.
>
> Canary traffic splitting — Route a percentage of traffic to new model versions using InferenceModelRewrite CRDs.
>
> Flow control and priority bands — Classify requests as Critical, Standard, or Sheddable with per-band admission control.
>
> Ready to stop wasting GPU capacity on naive routing? Install the Inference Gateway addon and start seeing first-token latency improvements in minutes rather than weeks.
>
> About the authors
>
> Vinay Arora
>
> Vinay is a Worldwide Leader for Specialist Solution Architect, Generative AI at AWS, where he collaborates with customers in designing cutting-edge AI solutions, leveraging AWS technologies. Prior to AWS, Vinay has over two decades of experience in finance—including roles at banks and hedge funds—he has built risk models, trading systems, and market data platforms. Vinay holds a master’s degree in computer science and business management.
>
> Piyush Daftary
>
> Piyush is a Senior Software Engineer at AWS, working on Amazon SageMaker with a focus on building performant, scalable inference systems for large language models. His technical interests span AI/ML, databases, and search technologies, where he specializes in developing production-ready solutions that enable efficient inference at scale. His work involves optimizing system performance, implementing intelligent routing mechanisms, and designing architectures that support both research and production workloads, with a passion for solving complex distributed systems challenges and making advanced AI capabilities more accessible to developers and organizations. Outside of work, he enjoys traveling, hiking, and spending time with family.
>
> Shreya Gangishetty
>
> Shreya is a Software Development Engineer at AWS, working on Amazon SageMaker with a focus on building scalable inference systems for large-scale AI workloads. She is passionate about developing reliable, high-performance solutions and delivering quality products that accelerate AI adoption through robust infrastructure. Outside of work, she enjoys traveling and cherishing moments with family.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。