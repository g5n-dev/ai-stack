---
title: "Spreading the load: How Salesforce met Multi-AZ HA with SageMaker Inference Components"
date: 2026-08-29T22:30:38+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "生成式 AI", "Amazon SageMaker AI", "Customer Solutions", "博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:22ea30749474d73c18f9a9e8e3d2aa7a14b41b2e8044d84f97e3f0bc52b6f25f"
source_payload_sha256: "sha256:dc2120edbe5ecb8166f1d8eca011986e23afc0ba8b8e32f710e4e12315377764"
observation_id: obs_248c8d39f0ea551419cff5661f09d00bd73d21729cd29d2949b6ae020a3dc956
event_id: evt_fbe143087f90b03ca48ec4bbdb00b0de6f00c98331da53c4926b3915d30ed144
revision_id: rev_783cfebc22710a21444d31ce96ac71901064ae354c8d332ba5c3648a7379a882
source_published_at: 2026-08-28T16:20:40Z
first_seen_at: 2026-08-29T14:28:49.210641Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 86
interpretation_sha256: "sha256:1d240cd6d22ee7c97ec821c808396498b1ef072c617692f2ebbf9092b744c8f6"
description: "Salesforce 在使用 SageMaker 推理组件部署模型时，通过 API 中的 **SchedulingConfig** 参数对副本在多个可用区之间的放置进行细粒度控制，以满足自身的多可用区高可用合规要求。"
external_url: https://aws.amazon.com/blogs/machine-learning/spreading-the-load-how-salesforce-met-multi-az-ha-with-sagemaker-inference-components
parent_observation_id: null
last_seen_at: 2026-08-29T14:28:49.210641Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/spreading-the-load-how-salesforce-met-multi-az-ha-with-sagemaker-inference-components](https://aws.amazon.com/blogs/machine-learning/spreading-the-load-how-salesforce-met-multi-az-ha-with-sagemaker-inference-components)
- **发布域名**: aws.amazon.com

## 要点解读

### 这是什么  
Salesforce 在使用 SageMaker 推理组件部署模型时，通过 API 中的 **SchedulingConfig** 参数对副本在多个可用区之间的放置进行细粒度控制，以满足自身的多可用区高可用合规要求。  

### 用在哪里  
适用于在 AWS 上搭建需要跨可用区保持弹性的机器学习推理服务，特别是对容错有严格内部规范的企业或团队。  

### 可以推断的  
推测：调度算法在每一次创建或更新推理组件时，会把最终的多可用区分布纳入考量，而不是仅关注单次放置的局部最优。  
推测：采用 SPREAD 放置策略可将副本尽可能分布在不同实例上，从而降低单个实例或可用区故障导致的服务中断风险。

## 来源摘要/节选

> When Salesforce set out to make Agentforce (Salesforce’s AI foundation for agents) highly available (HA) across multiple Availability Zones (AZs), the team faced a gap. Amazon SageMaker AI Inference Components (ICs) could cut GPU costs, but their default placement didn’t guarantee the Multi-AZ resilience Salesforce’s compliance bar required.
>
> For Salesforce, the ICs delivered an 8x reduction in infrastructure costs by co-hosting multiple models on shared GPUs. However, this cost win introduced a new question: how do you make IC endpoints highly available across multiple AZs?
>
> This post explores how Salesforce used the new IC Placement capability (surfaced through the SchedulingConfig parameter in the CreateInferenceComponent API) to meet their Multi-AZ HA compliance requirements.
>
> The challenge: Single points of failure in IC deployments
>
> By default, the SageMaker placement algorithm optimizes each IC deployment operation independently, distributing new copies evenly across instances without considering AZ balance. Even with a multi-AZ endpoint, this per-operation view means copies of a specific model can end up unevenly distributed across AZs, creating potential single points of failure:
>
> Instance-level failure: A single instance crash takes down all copies of a model.
>
> AZ-level failure: An AZ outage makes the entire model unavailable.
>
> Compliance risk: Salesforce mandates 2-AZ support for every production model. Default placement for ICs, optimized for cost alone, did not yet meet their internal 2-AZ compliance bar.
>
> The solution: SchedulingConfig
>
> AWS introduced the SchedulingConfig parameter in the CreateInferenceComponent API. It gives customers fine-grained control over IC copy placement across instances and AZs. Two key sub-parameters drive the HA behavior:
>
> AvailabilityZoneBalance: Controls cross-AZ distribution, balancing copies evenly across Availability Zones with configurable imbalance tolerance.
>
> PlacementStrategy (within each AZ): SPREAD distributes copies across as many instances as possible for fault isolation. BINPACK packs copies onto fewer instances for utilization efficiency.
>
> Code example: Deploying an IC with Multi-AZ HA placement
>
> Scenario: Salesforce has a multi-AZ SageMaker endpoint with 4 instances distributed evenly across 2 Availability Zones (2 instances in AZ-1, 2 instances in AZ-2). The team wants to deploy a model with 4 IC copies so that they are spread across both AZs for high availability.
>
> The following CreateInferenceComponent call deploys the model with SPREAD placement and AZ balancing:
>
> response = client.create_inference_component(
>
> InferenceComponentName='salesforce-llm-ic-ha',
>
> EndpointName='salesforce-multiaz-endpoint',
>
> VariantName='AllTraffic',
>
> Specification={
>
> 'ModelName': 'salesforce-einstein-llm-v2',
>
> 'ComputeResourceRequirements': {
>
> 'NumberOfAcceleratorDevicesRequired': 1,
>
> 'MinMemoryRequiredInMb': 65536
>
> },
>
> 'DataCacheConfig': {'EnableCaching': True},
>
> 'SchedulingConfig': {
>
> 'PlacementStrategy': 'SPREAD',
>
> 'AvailabilityZoneBalance': {
>
> 'EnforcementMode': 'PERMISSIVE',
>
> 'MaxImbalance': 1
>
> }
>
> }
>
> },
>
> RuntimeConfig={'CopyCount': 4}
>
> )
>
> With SPREAD, SageMaker distributes 4 copies across 4 instances: 2 in AZ-1 and 2 in AZ-2. When you set MaxImbalance to 1, you configure the system to tolerate at most a 1-copy difference between any two AZs.
>
> For lighter models needing only 2 copies, MaxImbalance: 0 enforces strict balance: exactly 1 copy per AZ:
>
> # Lighter model: strict 1-copy-per-AZ balance
>
> 'SchedulingConfig': {
>
> 'PlacementStrategy': 'SPREAD',
>
> 'AvailabilityZoneBalance': {
>
> 'EnforcementMode': 'PERMISSIVE',
>
> 'MaxImbalance': 0
>
> }
>
> },
>
> RuntimeConfig={'CopyCount': 2}
>
> Scaling while preserving AZ balance
>
> When you perform scale-out and scale-in operations, SageMaker helps you maintain AZ balance through your configured SchedulingConfig parameters. When you scale out, SageMaker places new copies to maintain even AZ distribution. When you reduce CopyCount, SageMaker symmetrically removes copies across AZs.
>
> Important: Never set CopyCount to 1 for HA-critical models. A single copy can only reside in one AZ, which means you would immediately break your 2-AZ compliance requirements.
>
> update_response = client.update_inference_component(
>
> InferenceComponentName='salesforce-llm-ic-ha',
>
> RuntimeConfig={'CopyCount': 8} # Scale out: 4 per AZ
>
> )
>
> Note: SchedulingConfig governs the placement plan for each individual scale operation. For ongoing consolidation and rebalancing over time (for example, after repeated scale-in/scale-out cycles), configure the endpoint’s ScaleInPolicy with the CONSOLIDATION strategy. With this configuration, a background sweeper periodically consolidates IC copies and releases idle instances while honoring AZ balance constraints.
>
> # Step 1: Create an endpoint config with CONSOLIDATION ScaleInPolicy
>
> client.create_endpoint_config(
>
> EndpointConfigName='salesforce-multiaz-endpoint-config-v2',
>
> ProductionVariants=[{
>
> 'VariantName': 'AllTraffic',
>
> 'InstanceType': 'ml.g5.xlarge',
>
> 'InitialInstanceCount': 4,
>
> 'ManagedInstanceScaling': {
>
> 'Status': 'ENABLED',
>
> 'MinInstanceCount': 2,
>
> 'MaxInstanceCount': 8,
>
> 'ScaleInPolicy': {
>
> 'Strategy': 'CONSOLIDATION'
>
> }
>
> }
>
> }]
>
> )
>
> # Step 2: Update the endpoint to use the new config
>
> client.update_endpoint(
>
> EndpointName='salesforce-multiaz-endpoint',
>
> EndpointConfigName='salesforce-multiaz-endpoint-config-v2'
>
> )
>
> The three pillars of the placement algorithm
>
> The new placement algorithm introduced three fundamental improvements. Each directly addressed Salesforce’s HA requirements:
>
> Balanced final distribution: The algorithm considers the balance of the final distribution rather than only immediate placement needs.
>
> Availability-aware distribution: SageMaker evenly distributes copies across AZs on a best-effort basis. Endpoint and inference component update operations persist multi-AZ placement, so HA is preserved during model updates.
>
> Within-AZ optimization: Within each AZ, the PlacementStrategy controls instance-level distribution. BINPACK packs copies onto fewer instances to maximize GPU utilization. SPREAD distributes copies across as many instances as possible for maximum fault isolation.
>
> Salesforce chose SPREAD for Pillar 3, prioritizing fault isolation over packing density. This helps prevent a single instance failure from taking down multiple copies of the same model.
>
> Target architecture: Before and after
>
> Continuing the preceding scenario: Salesforce’s endpoint has 4 instances across 2 AZs. Over time, the team deploys three ICs to this endpoint, each created in separate operations: IC1 (4 copies), IC2 (2 copies), and IC3 (2 copies).
>
> Later, the team deploys IC3, a lighter model needing only 2 copies with strict AZ balance:
>
> response = client.create_inference_component(
>
> InferenceComponentName='salesforce-light-model-ic3',
>
> EndpointName='salesforce-multiaz-endpoint',
>
> VariantName='AllTraffic',
>
> Specification={
>
> 'ModelName': 'salesforce-summarizer-v1',
>
> 'ComputeResourceRequirements': {
>
> 'NumberOfAcceleratorDevicesRequired': 1,
>
> 'MinMemoryRequiredInMb': 16384
>
> },
>
> 'SchedulingConfig': {
>
> 'PlacementStrategy': 'SPREAD',
>
> 'AvailabilityZoneBalance': {
>
> 'EnforcementMode': 'PERMISSIVE',
>
> 'MaxImbalance': 0
>
> }
>
> }
>
> },
>
> RuntimeConfig={'CopyCount': 2}
>
> )
>
> With MaxImbalance: 0, you configure the algorithm to target exactly 1 copy per AZ, which helps you keep IC3 available even if an entire AZ fails.
>
> The following diagram illustrates how the default placement and the new SchedulingConfig placement differ when all three ICs are deployed to the same endpoint:
>
> Figure 1: Default placement compared to SchedulingConfig placement across two Availability Zones
>
> Note: Models requiring multiple GPUs per copy (for example, large language models (LLMs) needing 4 accelerators) follow the same placement logic. SPREAD helps place each multi-GPU copy on a separate instance, and AZ balancing distributes them evenly across zones.
>
> Implementation considerations
>
> The following sections cover capacity planning, configuration, and monitoring for Multi-AZ HA deployments.
>
> Capacity reservations
>
> AWS strongly recommends On-Demand Capacity Reservations (ODCR) for capacity planning in AZ-constrained Regions. Salesforce pre-provisions reserved GPU capacity in each target AZ to help verify balanced IC placement. Without ODCR, on-demand capacity constraints may limit the distribution you want in high-demand Regions.
>
> Note: The placement algorithm supports partial deployment. If capacity constraints prevent full AZ balance, SageMaker still places copies on available instances rather than failing the operation entirely. This means the feature is usable even without ODCR. However, balance may not be optimal.
>
> Key configuration parameters
>
> The following table summarizes the recommended parameter values for Multi-AZ HA placement:
>
> Parameter
>
> Value
>
> Purpose
>
> PlacementStrategy
>
> SPREAD
>
> Distribute copies across instances (not packed)
>
> EnforcementMode
>
> PERMISSIVE
>
> Best-effort AZ balance. Places copies wherever available if balance cannot be achieved (currently the only enforcement mode)
>
> MaxImbalance
>
> 0 or 1
>
> Max copy count difference between any two AZs
>
> CopyCount
>
> ≥ 2
>
> Minimum 2 copies required for 2-AZ compliance
>
> ManagedInstanceScaling.MinInstanceCount
>
> ≥ 2
>
> Minimum 2 instances to span 2 AZs
>
> DataCacheConfig.EnableCaching
>
> True
>
> Faster scale-out by caching model artifacts
>
> RoutingConfig.RoutingStrategy
>
> LEAST_OUTSTANDING_REQUESTS
>
> Automatic failover routing across AZs
>
> Note: DataCacheConfig and RoutingConfig are general endpoint/IC configuration features independent of the IC placement strategy. They are included in this table because they complement HA deployments, but they are not part of the SchedulingConfig placement feature itself.
>
> Monitoring AZ balance with SageMaker AI Insights
>
> SageMaker AI Insights provides built-in observability for IC placement health. With detailed observability enabled, the following metrics help validate and maintain Multi-AZ HA:
>
> AZ skew (Reliability tab): Shows distribution imbalance percentage across your fleet. Use this to detect drift from balanced placement after scaling events.
>
> IC copy count per AZ: Confirms each inference component maintains the expected copy distribution across Availability Zones.
>
> Rebalancing events and duration: Tracks when SageMaker automatically rebalances copies and how long the operation takes.
>
> Insufficient Capacity Error (ICE) count per AZ: Monitors ICE events by AZ and instance type. You can use this to help determine if ODCR capacity may need adjustment.
>
> You can access these metrics in the SageMaker AI Insights dashboard and through Amazon CloudWatch. A detailed walkthrough of observability for IC-based endpoints will be covered in an upcoming blog post.
>
> The following screenshot shows an example of the SageMaker AI Insights Reliability tab with AZ balance metrics:
>
> Figure 2: SageMaker AI Insights Reliability tab with AZ balance metrics
>
> Results
>
> By using the IC Placement capability, Salesforce’s AI team achieved:
>
> Multi-AZ HA compliance: Every model deployment in Salesforce’s fleet satisfies their 2-AZ support requirement.
>
> Eliminated single points of failure: No model can be fully taken offline by a single instance or AZ failure.
>
> Preserved cost efficiency: Multi-model co-hosting continues to deliver infrastructure cost savings, while SPREAD placement maximizes fault isolation across instances.
>
> Resilient scaling: Scale-up and scale-down operations preserve multi-AZ distribution.
>
> Persistent HA through updates: Model updates no longer risk breaking AZ balance.
>
> Key takeaways for enterprise AI teams
>
> Salesforce’s journey to Multi-AZ HA with SageMaker Inference Components offers several lessons. Enterprise AI teams should consider the following:
>
> Design HA at the IC level, not just the endpoint level. Even with a multi-AZ endpoint, IC copies can be concentrated in a single AZ without explicit placement controls.
>
> Use SchedulingConfig with SPREAD and AvailabilityZoneBalance for workloads with high availability requirements. This is the recommended starting configuration for most models with HA requirements.
>
> Pre-provision capacity with ODCR. To achieve balanced AZ placement, you must provision available capacity in each target AZ. Don’t rely on on-demand capacity for HA-critical deployments.
>
> Set minimum CopyCount to 2 and minimum instance count to 2 as the HA baseline.
>
> Never scale to CopyCount: 1 for HA-critical models. A single copy can only reside in one AZ, which means you would immediately break your 2-AZ compliance requirements.
>
> Monitor IC distribution continuously using SageMaker AI Insights. Track AZ Skew, IC Copy Count per AZ, and Rebalancing Events on the Reliability tab to detect and remediate imbalance before it becomes a reliability issue.
>
> Conclusion
>
> IC Placement gives enterprise AI teams the control they need to meet strict availability requirements without sacrificing cost efficiency. For Salesforce, this capability unlocked Multi-AZ HA compliance for their production Agentforce models. It also serves as a reference pattern for enterprises running AI workloads with strict availability requirements on SageMaker.
>
> AI workloads are increasingly business-critical with strict uptime requirements. The ability to control exactly how model copies are distributed across infrastructure is no longer a nice-to-have. It’s a fundamental requirement.
>
> Further reading
>
> For more information, see the following resources.
>
> API references
>
> CreateInferenceComponent API (Boto3) — Full parameter reference for deploying ICs with SchedulingConfig.
>
> InferenceComponentSchedulingConfig — PlacementStrategy (SPREAD/BINPACK) and scheduling configuration.
>
> InferenceComponentAvailabilityZoneBalance — EnforcementMode and MaxImbalance parameters.
>
> Blogs and articles
>
> Optimizing Salesforce’s Model Endpoints with Amazon SageMaker AI Inference Components — The original Salesforce + SageMaker cost optimization story.
>
> Monitor Endpoint Metrics and Create Alarms — SageMaker AI Insights observability metrics reference.
>
> Best practices
>
> Inference Cost Optimization Best Practices — SageMaker cost optimization strategies.
>
> Inference Optimization for SageMaker AI Models — Quantization, compilation, and model optimization.
>
> About the authors
>
> Rielah De Jesus
>
> Rielah is a Principal Solutions Architect at AWS who has successfully helped various enterprise customers in the DC, Maryland, and Virginia area adopt cloud services. In her current role, she acts as a customer advocate and technical advisor focused on helping organizations like Salesforce achieve success on AWS. She is also a staunch supporter of women in IT and is very passionate about finding ways to creatively use technology and data to solve everyday challenges.
>
> Anuja Pulijala
>
> Anuja is a Senior Member of Technical Staff on Salesforce’s Agentforce model-serving team. She is an LLM inference engineer and core engineer on the multi-cloud model deployment SDK that powers self-serve LLM deployments on AWS SageMaker for 50+ production models. Her recent work spans SageMaker Inference Component integration, multi-AZ high-availability rollout, and ODCR-based GPU capacity management across Salesforce’s production regions.
>
> Sai Guruju
>
> Sai is a Lead Member of Technical Staff on Salesforce’s Agentforce model-serving team. He takes models from benchmark to production – driving framework and serving choices, GPU capacity strategy, and the reliability of serving at scale. His recent work spans reasoning-model deployment (Nemotron-120B on H200/B200), speech-model serving for Agentforce Voice, code-generation models for Agentforce for Vibes and multi-cloud hosting evaluations across AWS SageMaker, Together AI.
>
> Srikanta Prasad S V
>
> Srikanta is a Senior Manager of Product Management at Salesforce, specializing in Generative Artificial Intelligence (AI) solutions on the Agentforce AI. He works on the LLM Gateway, the multi-provider inference layer that powers agentic workloads across Salesforce, and leads initiatives spanning model hosting, agent inference, model fleet management, and the model deployment lifecycle. With over 20 years of experience across semiconductors, aviation and aerospace, print media, and software technology, Srikanta previously worked at Oracle Cloud Infrastructure on Data Science and Generative AI solutions. Srikanta holds an MBA from the University of North Carolina and an MS from the National University of Singapore and a graduate certificate in Artificial Intelligence from Stanford University.
>
> Qiyun Zhao
>
> Qiyun is a Software Development Manager on the Amazon SageMaker Inference team, where he builds managed inference infrastructure that enables customers to deploy ML and GenAI workloads reliably at scale. He leads engineering efforts across system-level performance optimization, accelerator capacity management, model deployment guardrails, and security compliance — ensuring customers achieve high availability for their inference workloads.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。