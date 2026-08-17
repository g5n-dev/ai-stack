---
title: "NVIDIA Nemotron 3.5 Lightning now available in Amazon SageMaker JumpStart"
date: 2026-08-18T05:43:36+08:00
draft: false
entry_kind: "auto"
tags: ["AI Agent", "机器学习", "Advanced (300)", "Amazon SageMaker AI", "Amazon SageMaker JumpStart", "Announcements", "博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:b59e76fd06ca97f3d14993cd3de07ed5dd046d3121ca641a76938e926b3bf0c1"
source_payload_sha256: "sha256:a81ef8c2dd682be8d48e249cf65be3f65e30a43531a1e8ff7823d5da5a2900ff"
observation_id: obs_0eadff1b96c5b07c2a9da2a0da496ae04560f4cb6ca0e8a54de3a0e7ebbe46bc
event_id: evt_0264235dc7ec995cdccd6a103ea0a3cf261a1cf0bf12d0cb256280b6871c6c6a
revision_id: rev_6759724518c02d94188f0b30fa10bc757ad7b63db54a77f05f360e24d57f0ff3
source_published_at: 2026-08-17T18:06:33Z
first_seen_at: 2026-08-17T21:40:18.545099Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 73
interpretation_sha256: "sha256:9d779b4a319cacb24d939842744de4fb0413b4597bdbd047c011604b4619cacc"
description: "这是一条关于 NVIDIA Nemotron 3.5 Lightning——一款面向大量代理任务、采用稀疏专家混合结构的轻量模型——已在 Amazon SageMaker JumpStart 上开放使用的公告。"
external_url: https://aws.amazon.com/blogs/machine-learning/nvidia-nemotron-3-5-lightning-now-available-in-amazon-sagemaker-jumpstart
parent_observation_id: null
last_seen_at: 2026-08-17T21:40:18.545099Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/nvidia-nemotron-3-5-lightning-now-available-in-amazon-sagemaker-jumpstart](https://aws.amazon.com/blogs/machine-learning/nvidia-nemotron-3-5-lightning-now-available-in-amazon-sagemaker-jumpstart)
- **发布域名**: aws.amazon.com

## 要点解读

### 这是什么
这是一条关于 NVIDIA Nemotron 3.5 Lightning——一款面向大量代理任务、采用稀疏专家混合结构的轻量模型——已在 Amazon SageMaker JumpStart 上开放使用的公告。

### 用在哪里
适用于需要长时间运行、频繁调用模型的代理系统，例如金融、安防、电信、零售等行业中执行分类、抽取、监控等重复性任务的场景。

### 可以推断的
推测：稀疏激活的设计能够在保持多任务能力的同时，提升单位时间的请求吞吐量，从而降低高频调用场景的计算成本。  
推测：模型提供的长上下文窗口和高速解码能力，可帮助代理在跨多轮会话时保留状态，减少重复检索的开销。

## 来源摘要/节选

> NVIDIA Nemotron 3.5 Lightning is designed for the fast, specialized model execution required by high-volume agentic workloads. With NVIDIA Nemotron 3.5 Lightning on Amazon SageMaker JumpStart, you can access an open model designed for high-volume agentic workloads.
>
> With this launch, you can deploy Nemotron 3.5 Lightning from Amazon SageMaker JumpStart without configuring the serving infrastructure yourself. NVIDIA describes Lightning as the fastest open model in its class for powering always-on agents. It delivers up to 4x higher throughput and up to 30% faster task completion on high-volume agentic workloads. At 30B total parameters with only 3B active, it can run on a single supported GPU. Repetitive, specialized steps in agent workflows can therefore run without frontier-scale infrastructure. In this post, we show you how to deploy Nemotron 3.5 Lightning from SageMaker JumpStart.
>
> Overview of NVIDIA Nemotron 3.5 Lightning
>
> Nemotron 3.5 Lightning is a publicly available foundation model distilled from NVIDIA’s frontier Nemotron 3 Ultra and developed with the Nemotron Coalition. It uses a hybrid Mixture-of-Experts (MoE) architecture and is trained specifically for agentic tool use across popular agent harnesses. It is trained on open datasets and released as an open model, so you can customize it, own the resulting weights, and deploy it wherever your agents run.
>
> The following table summarizes the key specifications and performance characteristics of NVIDIA Nemotron 3.5 Lightning.
>
> Specification
>
> Details
>
> Architecture
>
> Hybrid Mixture-of-Experts (MoE)
>
> Parameters
>
> 30B total / 3B active
>
> Context length
>
> Up to 1M tokens
>
> Input / Output
>
> Text in, text out
>
> Speculative decoding
>
> DFlash
>
> Throughput
>
> Up to 4x higher for high-volume agentic workloads
>
> Task completion
>
> Up to 30% faster
>
> Distilled from
>
> NVIDIA Nemotron 3 Ultra
>
> Not every agent step needs a frontier model
>
> Always-on agents work continuously: they gather context, observe their environment, reason over what they know, and act. Many of these steps can involve model calls, but they do not all require the same level of capability. Planning a multi-stage workflow or orchestrating sub-agents can demand frontier-level reasoning. Classifying an alert, extracting fields from a form, or checking a record against a policy can often be handled by a smaller, specialized model. These tasks can account for a large share of call volume.
>
> In many cases, running all model-backed steps through a single large model can add frontier-model cost and latency to work that a smaller, specialized model can handle. A system-of-models approach can instead route each step to a model suited to the task.
>
> Nemotron 3.5 Lightning is built for the high-volume end of that system. Its MoE architecture activates 3B of 30B parameters per forward pass, helping maintain high throughput across long, multi-turn sessions. DFlash speculative decoding can further reduce per-token latency. The 1M-token context window allows an agent to carry accumulated state across a long-running session without repeated re-grounding.
>
> If NVIDIA NeMo Switchyard is part of your stack, it can route individual workflow steps across your chosen model pool. Lightning can be selected for high-volume specialized steps where its speed and domain-specific accuracy are a good fit.
>
> Accuracy across reasoning and agentic benchmarks
>
> Across the published evaluations, NVFP4 remains close to BF16 on many tasks, as summarized in the following table. NVIDIA reports that the evaluation recipes and commands used to produce these results are published in NeMo Gym. Accuracy results were measured by NVIDIA under a consistent harness and may differ from vendors’ self-reported numbers.
>
> The following table compares the BF16 and NVFP4 variants of Nemotron 3.5 Lightning across key reasoning and agentic benchmarks.
>
> Benchmark
>
> BF16
>
> NVFP4
>
> MMLU Pro
>
> 81.94
>
> 81.62
>
> GPQA Diamond
>
> 75.44
>
> 75.57
>
> SWE-bench Verified
>
> 51.56
>
> 52.80
>
> PinchBench
>
> 85.37
>
> 83.43
>
> IFBench
>
> 71.88
>
> 72.88
>
> AA-LCR
>
> 52.00
>
> 49.19
>
> Customizing for domain accuracy
>
> Organizations can post-train the model with NVIDIA NeMo for domain-specific tools, workflows, and policies, then deploy the resulting model in their chosen environment. The SageMaker JumpStart model card for this launch does not expose JumpStart customization.
>
> Enterprise use cases
>
> Lightning is built for the specialized, high-frequency work inside agent workflows:
>
> Personal agents: Long-running assistants handling email, calendar, projects, and bookings, with the option to run locally for contextual data.
>
> Financial services: Extracting data from documents, checking policy rules, monitoring risk signals, and preparing structured summaries.
>
> Cyber security operations: Enriching alerts, classifying incidents, querying logs, validating controls, correlating indicators, and preparing findings for analysts.
>
> Telecom: Triaging network alarms, optimizing network configurations, and answering billing questions.
>
> Retail: Enriching product catalogs, resolving inventory and fulfillment exceptions, assisting product discovery, and handling order, return, and loyalty questions.
>
> Getting started with SageMaker JumpStart
>
> You can deploy Nemotron 3.5 Lightning through Amazon SageMaker JumpStart without manually configuring the serving framework.
>
> Prerequisites
>
> Before you begin, make sure you have:
>
> An AWS account.
>
> Appropriately scoped permissions for SageMaker JumpStart.
>
> Sufficient service quota for GPU instances (for example, ml.g6e.12xlarge, ml.p4d.24xlarge, or ml.p5.48xlarge).
>
> Important: Deploying this model creates a SageMaker AI endpoint that incurs charges while running. For details, see Amazon SageMaker AI pricing. Delete your endpoint when finished to avoid ongoing charges.
>
> Deploy using SageMaker Studio
>
> Open Amazon SageMaker Studio.
>
> In the navigation pane, choose SageMaker JumpStart.
>
> Search for Nemotron 3.5 Lightning.
>
> Figure 1: Searching for Nemotron 3.5 Lightning in SageMaker JumpStart
>
> Select the model card. The NVFP4 model ID is huggingface-reasoning-nemotron-3-5-lightning-30b-a3b-nvfp4. For BF16, use huggingface-reasoning-nemotron-3-5-lightning-30b-a3b-bf16.
>
> Figure 2: The Nemotron 3.5 Lightning model card in SageMaker JumpStart
>
> Figure 3: Model card details for Nemotron 3.5 Lightning
>
> Choose Deploy.
>
> Select your instance type (for example, ml.g6e.24xlarge).
>
> Figure 4: Selecting an instance type for deployment
>
> Review the deployment settings. The defaults are sufficient for most use cases.
>
> Choose Deploy to create the endpoint.
>
> Wait for the endpoint status to show InService before running inference.
>
> Figure 5: Endpoint status showing InService
>
> Deploy from Hugging Face
>
> You can also deploy NVIDIA Nemotron 3.5 Lightning to Amazon SageMaker AI from its Hugging Face model page. On the Hugging Face model page, choose Deploy, select Amazon SageMaker AI, and then choose Deploy on SageMaker AI. This opens the SageMaker AI deployment workflow, where you can configure and deploy the model.
>
> Figure 6: Deploying from the Hugging Face model page
>
> Deploy using the SageMaker Python SDK
>
> With SageMaker JumpStart, you can access the NVFP4 and BF16 variants. The following example uses the NVFP4 model ID huggingface-reasoning-nemotron-3-5-lightning-30b-a3b-nvfp4. For BF16, use huggingface-reasoning-nemotron-3-5-lightning-30b-a3b-bf16.
>
> from sagemaker.jumpstart.model import JumpStartModel
>
> model_id = "huggingface-reasoning-nemotron-3-5-lightning-30b-a3b-nvfp4"
>
> model_version = "*"
>
> model = JumpStartModel(model_id=model_id, model_version=model_version)
>
> predictor = model.deploy()
>
> Clean up
>
> To avoid unnecessary charges, delete the SageMaker AI endpoint when you are done:
>
> predictor.delete_endpoint()
>
> Conclusion
>
> NVIDIA Nemotron 3.5 Lightning brings fast, specialized agent execution to Amazon SageMaker JumpStart. NVIDIA reports up to 4x higher throughput and up to 30% faster task completion for high-volume specialized work. Its hybrid MoE architecture, 3B active parameters, DFlash speculative decoding, and 1M-token context are designed for high-volume agent workflows. Because the model is open and designed for customization, you can post-train it for your own tools and policies and retain control of the resulting model.
>
> Nemotron 3.5 Lightning can support specialized agent workloads across personal assistants, financial services, security operations, telecom, and retail. You can deploy it today from SageMaker JumpStart.
>
> Get started by searching for Nemotron 3.5 Lightning in Amazon SageMaker JumpStart. For deployment guidance, see JumpStart foundation model usage in the Amazon SageMaker AI Developer Guide.
>
> About the authors
>
> Venu Kanamatareddy
>
> Venu is an AI Specialist Solutions Architect at Amazon Web Services, where he works with high-growth, AI-native startups to design, scale, and operationalize production-grade AI systems.
>
> Evan Kravitz
>
> Evan is a software engineer at Amazon Web Services, working on SageMaker JumpStart. He is interested in the confluence of machine learning with cloud computing. Evan received his undergraduate degree from Cornell University and master’s degree from the University of California, Berkeley. In 2021, he presented a paper on adversarial neural networks at the ICLR conference. In his free time, Evan enjoys cooking, traveling, and going on runs in New York City.
>
> Vivek Gangasani
>
> Vivek is a Senior Machine Learning Solutions Architect at Amazon Web Services. He works with Machine Learning startups to build and deploy AI/ML applications on AWS. He is currently focused on delivering solutions for MLOps, ML Inference and low-code ML. He has worked on projects in different domains, including Natural Language Processing and Computer Vision.
>
> Naidile Murali
>
> Naidile is a Product Manager at AWS based in Bellevue, WA. She focuses on enhancing the AI/ML developer experience on Amazon SageMaker AI, including onboarding, IDE connectivity, and GPU capacity management. Prior to AWS, she worked as a software engineer at HSBC. Naidile holds an MBA from Georgetown University.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。