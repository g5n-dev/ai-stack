---
title: "Managed NVIDIA Dynamo on Amazon SageMaker HyperPod Inference"
date: 2026-11-18T12:19:39+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "生成式 AI", "深度学习", "Prompt 工程", "Advanced (300)", "Amazon SageMaker HyperPod", "Announcements"]
categories: []
source: "blogs_podcasts"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:a6b0522258073f22b31601db07a69e71c769532d0b946c85e5c868d291d1285e"
source_payload_sha256: "sha256:a7380acd8457a91f98bc8b99b4029c448309589bad06425650a60e13bdb33a71"
observation_id: obs_4df567e64846f78674c5776162311be11b2f8e2bf8e52723529eaf159029fb79
event_id: evt_ff1bb866f4c19670002813834decb1d3e8ca638fe697b7f20df7768680052bc7
revision_id: rev_4fad24cbbea8d7f22e30a5054f843881cd1ebfc2b7baa7baa1e3db71f7fbb84f
source_published_at: 2026-11-17T23:33:26Z
first_seen_at: 2026-11-18T04:30:28Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 60
description: "当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。"
external_url: https://aws.amazon.com/blogs/machine-learning/managed-nvidia-dynamo-on-amazon-sagemaker-hyperpod-inference
parent_observation_id: null
last_seen_at: 2026-11-18T04:18:18.190854Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/managed-nvidia-dynamo-on-amazon-sagemaker-hyperpod-inference](https://aws.amazon.com/blogs/machine-learning/managed-nvidia-dynamo-on-amazon-sagemaker-hyperpod-inference)
- **发布域名**: aws.amazon.com

## 来源摘要/节选

> Serving large language models (LLMs) efficiently requires sufficient GPU memory and careful coordination of prompt processing and token generation. GLM-5.3’s FP8 weights, for example, exceed the 640 GB of GPU memory on a single ml.p5.48xlarge instance, before accounting for KV cache and runtime overhead. Long prompts can also slow token generation when both share the same GPUs.
>
> Amazon SageMaker HyperPod Inference now supports NVIDIA Dynamo, combining Dynamo’s distributed inference capabilities with the infrastructure management of HyperPod to address these challenges. Dynamo is an open source distributed inference framework that supports multi-node deployment, disaggregated prefill and decode, and KV-aware routing with engines such as vLLM, SGLang, and TensorRT-LLM. HyperPod supports these deployments with high-performance Elastic Fabric Adapter (EFA) networking, coordinated GPU scheduling, and node health monitoring and recovery. In this post, we illustrate multi-node and disaggregated serving through a deployment example, share benchmark results, and outline best practices for optimizing inference on HyperPod.
>
> How the integration works
>
> The HyperPod Inference add-on installs the Dynamo custom resource definitions and these serving and scheduling components:
>
> HyperPod Inference Operator manages endpoint deployment through an InferenceEndpointConfig (IEC) custom resource. Its dynamoSpec section supplies the Dynamo configuration.
>
> Dynamo operator manages resources defined in a DynamoGraphDeployment (DGD), including the frontend, model workers, replica counts, and resource requirements.
>
> Grove coordinates related groups of pods, including multi-node workers, and their scaling relationships.
>
> Kubernetes AI (KAI) Scheduler places pods on GPU resources, using gang scheduling to schedule the pods required for a multi-node worker together.
>
> AWS Deep Learning Containers (DLCs) provide the Dynamo runtime, while the add-on manages integrated component versions. To adopt a supported Dynamo release, update the add-on.
>
> Deployment architecture
>
> The following diagram shows the deployment paths, serving components, and infrastructure management for disaggregated inference on SageMaker HyperPod. The Dynamo frontend routes requests to prefill workers, which process prompts, and decode workers, which generate tokens. These separate pools allow independent scaling and tuning. Both pools load the full model weights, and KV cache transfers between them over EFA.
>
> Dynamo also supports aggregated serving, where prefill and decode run in the same worker. In either topology, workers can run on one instance or span multiple instances using tensor and pipeline parallelism. Dynamo’s KV-aware router considers reusable prefix KV cache and active worker load in both topologies. Prefix reuse can reduce prompt recomputation and improve time to first token, while load awareness helps avoid overloading workers. For more details on the Dynamo architecture, see the Dynamo Knowledge Base overview.
>
> HyperPod provides node, GPU, and EFA health monitoring and manages node replacement, while the orchestration components recreate affected workers. Deployments configured through InferenceEndpointConfig with dynamoSpec support invocation through SageMaker endpoints.
>
> Figure 1: Deployment paths, serving components, and infrastructure management for NVIDIA Dynamo on Amazon SageMaker HyperPod Inference
>
> Two ways to configure your deployment
>
> Whether you are new to HyperPod, new to Dynamo, or both, the add-on offers two deployment paths to fit your workflow:
>
> Bring-your-own DynamoGraphDeployment (DGD) lets existing Dynamo users continue using upstream documentation, recipes, and manifests, with the Dynamo operator managing the deployment. To bring an existing DGD to HyperPod, use a supported container image and configure storage, networking, and pod placement for your cluster.
>
> InferenceEndpointConfig with dynamoSpec lets existing HyperPod Inference users deploy a new Dynamo endpoint using the same configuration format and OpenAI-compatible interface they already know. For the inference engine, you can choose vLLM, SGLang, or TensorRT-LLM, with vLLM used by default. The operator also supplies defaults for KV-aware routing and replica counts.
>
> Both paths support single-instance and multi-node deployments. In either case, HyperPod manages node health and replacement. The table summarizes the responsibilities for each path.
>
> Bring-your-own DGD
>
> InferenceEndpointConfig with dynamoSpec
>
> You write
>
> Complete DGD manifest
>
> IEC containing dynamoSpec
>
> Best for
>
> Teams wanting direct control of the serving graph or reuse of existing DGDs
>
> Teams wanting managed endpoint setup through IEC
>
> Model weights
>
> You configure downloading or mounting the weights
>
> The operator stages weights from Amazon Simple Storage Service (Amazon S3) or Amazon FSx
>
> Endpoint, TLS, registration
>
> You configure and manage these resources
>
> Managed through the HyperPod Inference Operator
>
> Autoscaling
>
> You configure and manage scaling
>
> Kubernetes Event-driven Autoscaling (KEDA) through autoScalingSpec for aggregated and disaggregated deployments
>
> Deployment example: GLM-5.3
>
> The following excerpts use the InferenceEndpointConfig (IEC) deployment path with vLLM on ml.p5.48xlarge instances. Dynamo-specific settings belong under spec.dynamoSpec. Model source and endpoint settings are included in the complete manifest.
>
> Multi-node aggregated serving
>
> This configuration runs one model-worker replica across two instances (16 GPUs), with two frontend replicas for request handling. Setting dynamoSpec.frontend.routingMode to kv-aware turns on KV-aware routing.
>
> spec:
>
> replicas: 1
>
> dynamoSpec:
>
> modelServer: vllm
>
> frontend:
>
> replicas: 2
>
> routingMode: kv-aware
>
> aggregation:
>
> nodesPerReplica: 2
>
> tensorParallelism: 16
>
> Here, spec.replicas controls the number of model-worker replicas, while frontend.replicas controls the number of frontend replicas.
>
> Multi-node disaggregated serving
>
> Replace aggregation under spec.dynamoSpec with the following disaggregation block, keeping the preceding frontend configuration. Replica counts are set separately for prefill and decode. This example runs one prefill replica and two decode replicas, each spanning two instances, for a total of six instances.
>
> disaggregation:
>
> prefill:
>
> nodesPerReplica: 2
>
> tensorParallelism: 16
>
> replicas: 1
>
> decode:
>
> nodesPerReplica: 2
>
> tensorParallelism: 16
>
> replicas: 2
>
> Apply the deployment
>
> Apply the complete manifest with kubectl apply. The HyperPod Inference Operator makes the configured model weights available to the workers and generates the DGD. Grove and KAI Scheduler coordinate placement so that the pods required for each multi-node worker are scheduled together.
>
> After the SageMaker endpoint is ready and configured for chat completions, clients can send an OpenAI-compatible request payload through the SageMaker Runtime API:
>
> aws sagemaker-runtime invoke-endpoint \
>
> --endpoint-name glm53 \
>
> --content-type application/json \
>
> --body '{"model":"zai-org/GLM-5.3","messages":[{"role":"user","content":"Hello"}],"max_tokens":128}' \
>
> --cli-binary-format raw-in-base64-out \
>
> out.json
>
> Benchmarks
>
> We benchmarked Dynamo on SageMaker HyperPod across two models to compare serving configurations.
>
> Disaggregated prefill and decode for Qwen3-235B
>
> We used AIPerf to compare aggregated and disaggregated serving for Qwen3-235B-A22B-FP8 using Dynamo with TensorRT-LLM on two p5en.48xlarge instances (16 H200 GPUs). Requests contained 4,000 input tokens and 200 output tokens. We retained measured points that met two targets: P90 time to first token below one second, and median generation speed of at least 50 tokens per second per user. Among these points, disaggregated serving achieved 2.05× the highest aggregated throughput: 207 versus 101 output tokens per second per GPU, at concurrency 80 and 32, respectively.
>
> Figure 2: Aggregated compared to disaggregated serving throughput for Qwen3-235B-A22B-FP8
>
> Multi-node aggregated serving for Qwen3.5-397B
>
> Dynamo supports multi-node serving in both aggregated and disaggregated modes for models that exceed a single instance’s GPU memory. To evaluate a worker spanning nodes, we used AIPerf to benchmark multi-node aggregated serving for Qwen3.5-397B-A17B-FP8 with Dynamo and vLLM, using TP4 × PP2 and eight active H200 GPUs. This model fits on one instance, so in practice you would not split it. It serves here as a controlled baseline. We compared eight GPUs on one p5en.48xlarge against four GPUs on each of two instances, using the same model, parallelism, and workload configuration. With an agentic workload featuring high prefix reuse at concurrency 32, the two-node configuration delivered 126.4 output tokens per second per GPU, retaining 99.1 percent of single-node throughput. This shows that Dynamo on SageMaker HyperPod can serve a model that needs more than one instance across nodes. The node boundary itself does not become a significant throughput penalty.
>
> Figure 3: Single-node compared to two-node throughput for multi-node aggregated serving of Qwen3.5-397B-A17B-FP8
>
> Best practices for optimized inference
>
> NVIDIA Dynamo provides recipes and tools to help you select a serving configuration, benchmark performance, and tune your deployment on SageMaker HyperPod.
>
> Start with a matching recipe – Choose a Dynamo recipe for your model, inference engine, and GPU type. Account for model weights, KV cache, and runtime memory when sizing workers. For supported configurations, AISimulate can help compare aggregated and disaggregated serving, choose parallelism, and size prefill and decode worker pools before testing on GPUs.
>
> Verify communication before benchmarking – For deployments spanning instances, confirm that communication uses the intended EFA transport, including KV-cache transfers between prefill and decode workers. See the Dynamo EFA guide.
>
> Benchmark representative traffic – Replay your traffic with AIPerf, or use a generated agentic trace with representative prompt lengths, output lengths, and prefix reuse. Sweep concurrency for each configuration, retain points meeting your SLAs, and choose based on cost and latency priorities.
>
> Tune from measured bottlenecks – Adjust topology and worker allocation before engine settings, changing one variable at a time. Follow the performance tuning guide, or use Dynamo optimization agent skills to assist with benchmarking and tuning. Validate each candidate on your target HyperPod deployment.
>
> Conclusion
>
> NVIDIA Dynamo on SageMaker HyperPod Inference simplifies deploying and operating large models with multi-node serving, disaggregated prefill and decode, and KV-aware routing. The managed add-on installs the serving components, and configuration defaults simplify endpoint setup. HyperPod manages model weights, auto-scales clusters based on GPU and inference metrics, monitors node health, and replaces failed nodes. Together, these capabilities reduce undifferentiated infrastructure work so teams can focus on their models and applications. Get started with the setup instructions and complete deployment examples in the linked repository.
>
> Acknowledgements
>
> The authors would like to thank Eliuth Triana, Felipe Garcia, Sanjana Checker, Junyuan Yang, Jiahong Liu, Anish Maddipoti, Jacob Kern and Abdullahi Olaoye from NVIDIA for their contributions to this post. We also would like to thank Can Sun, Ophelia Yang, Aryaman Kothari, David Oh, and Ayush Kumar from AWS for their contributions.
>
> About the authors
>
> Vinay Arora
>
> Vinay is a Specialist Solution Architect for Generative AI at AWS, where he collaborates with customers in designing cutting-edge AI solutions, leveraging AWS technologies and Infrastructure for the past 6 years. Prior to AWS, Vinay has over two decades of experience in finance—including roles at banks and hedge funds—he has built risk models, trading systems, and market data platforms. Vinay holds a master’s degree in computer science and business management.
>
> Piyush Daftary
>
> Piyush is a Principal Software Engineer at AWS, where he builds inference systems for large language models on Amazon SageMaker HyperPod. He focuses on optimized routing, disaggregated serving, and autoscaling architectures that help customers extract maximum performance from their GPU fleets. His background spans distributed systems, databases, and search technologies. Outside of work, he enjoys traveling and spending time with family.
>
> Xuan Lu
>
> Xuan is a Software Development Engineer at AWS, where he works on Amazon SageMaker HyperPod Inference to build and scale large-scale LLM inference systems. His work focuses on distributed inference, intelligent request routing, and performance optimization, with experience across Kubernetes-based orchestration and LLM serving infrastructure. Outside of work, he enjoys traveling, exploring nature, and reading science fiction.
>
> Preethi Ravula
>
> Preethi is a Solutions Architecture Manager for Generative AI, Data, Storage &amp; Analytics on the ISV team at AWS. She leads a team that helps software vendors build and scale generative AI on AWS. She works on AI strategy and inference optimization, and she develops frameworks and playbooks that help customers run large language model workloads faster and more cost-effectively on AWS Trainium and NVIDIA GPUs. Preethi has spoken at GHC 2025, SJSU, and Women in Tech Dublin. She also champions AI education through an AWS program that teaches students to build applications with AWS generative AI services.
>
> Sai Devulapalli
>
> Sai has been leading the Amazon SageMaker AI world-wide GTM team over the past six years. He works closely with customer-facing AI Specialist leaders across AWS world-wide and engages with C/VP-level stakeholders at customers to understand their needs and offer guidance in building and executing on their company’s AI platform strategies. Sai works with SageMaker AI Service leadership to help guide service roadmap to better serve our customer needs and has been in AI/ML platform space over the past 16 years, leading business development and product management teams at Dell EMC and Pivotal and prior to that, leading Data Analytics and ML practice for Ericsson in North America.
>
> Aryaman Kothari
>
> Aryaman is a Senior Product Manager at Amazon SageMaker AI, where he leads AI inference on Amazon SageMaker HyperPod, helping enterprises run AI models at scale for production workloads. A Chicago Booth graduate, Aryaman previously led product and go-to-market for Quantiphi’s Conversational AI business. Outside work, he enjoys playing soccer, making chai, and hiking.
>
> Kshitiz Gupta
>
> Kshitiz is a Senior Solutions Architect at NVIDIA, where he helps cloud customers design and optimize GPU-accelerated data and AI systems. His work spans data processing, vector database, and LLM inference, partnering closely with AWS and Amazon teams to bring these capabilities into production. Outside of work, he enjoys music, yoga, and hiking.
>
> Marc Karp
>
> Marc is a Senior Solutions Architect at NVIDIA, where he helps customers deploy and scale AI inference on GPUs. He works across the inference stack, from model optimization and distributed serving to the engines that power them. Outside of work, he enjoys traveling and exploring new places.
>
> Wenhan Tan
>
> Wenhan is a solutions architect at NVIDIA, assisting customers in adopting NVIDIA AI solutions at large-scale. His work focuses on accelerating deep learning applications and addressing inference and training challenges.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。