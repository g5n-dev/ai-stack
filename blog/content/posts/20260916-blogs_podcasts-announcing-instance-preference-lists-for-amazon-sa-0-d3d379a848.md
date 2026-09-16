---
title: "Announcing instance preference lists for Amazon SageMaker AI training jobs"
date: 2026-09-16T14:04:01+08:00
draft: false
entry_kind: "auto"
tags: ["AI Agent", "生成式 AI", "机器学习", "Amazon SageMaker AI", "Announcements", "Intermediate (200)", "博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:77c23df1854ad57ae630edc5317a1f7d3bc04bdb42f16f756a784270c2d4a16f"
source_payload_sha256: "sha256:2d66e93dab5ad9513c1c749a923f6af100c01a370cfd1bb97def247eb4b2023a"
observation_id: obs_d3d379a848ac4d3495cc1e66ac819a0f604b997049ba38bbcd33168e5d3d1129
event_id: evt_18187952db50536184ab7e71b555b760cf9e5da3aa9a6a2c24fb7e8f46f36b26
revision_id: rev_d494d56359795a49d3c7b32f0ffb7f49bd1713d8ae3967986831c7be4223a7fa
source_published_at: 2026-09-15T16:01:47Z
first_seen_at: 2026-09-16T06:01:12.518391Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 74
interpretation_sha256: "sha256:ef078a0fa8204d67c533678f0851be8dd9dca9f74704a86e2fa889bf800366be"
description: "Amazon SageMaker AI 为训练和处理任务新增了实例偏好列表功能，可在提交时指定最多五个实例类型的优先级顺序，系统自动挑选首个有可用容量的类型启动任务。"
external_url: https://aws.amazon.com/blogs/machine-learning/announcing-instance-preference-lists-for-amazon-sagemaker-ai-training-jobs
parent_observation_id: null
last_seen_at: 2026-09-16T06:01:12.518391Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/announcing-instance-preference-lists-for-amazon-sagemaker-ai-training-jobs](https://aws.amazon.com/blogs/machine-learning/announcing-instance-preference-lists-for-amazon-sagemaker-ai-training-jobs)
- **发布域名**: aws.amazon.com

## 要点解读

### 这是什么
Amazon SageMaker AI 为训练和处理任务新增了实例偏好列表功能，可在提交时指定最多五个实例类型的优先级顺序，系统自动挑选首个有可用容量的类型启动任务。

### 用在哪里
适用于需要在高峰时段抢占 GPU 资源、或希望把预留容量与按需容量结合使用的机器学习团队，尤其是运行大规模训练或周期性处理的工作流。

### 可以推断的
推测：该功能可以减少因单一实例类型缺货导致的反复手动重试，从而提升实验迭代速度。  
推测：因为只在加速实例（如 ml.p、ml.g、ml.trn 系列）上生效，CPU 为主的普通作业不受此约束影响。

## 来源摘要/节选

> Getting access to the right GPUs when you need them is one of the biggest challenges in training or customizing AI models at scale. During peak demand periods, your preferred GPU may not be immediately available – and when your job is tied to one specific GPU configuration, the only option is to wait or manually try alternatives. This slows down experimentation and pulls engineering focus away from model development. What if you could submit a single job with a list of suitable GPU options and have Amazon SageMaker AI automatically find available capacity from your list – reducing wait times and getting your teams back to building?
>
> Today, we’re excited to announce Instance preference lists for Amazon SageMaker AI Training Jobs and Amazon SageMaker Processing Jobs, helping you secure on-demand capacity faster by automatically checking across your preferred instance types. With this feature, you can specify an ordered list of up to five acceptable instance types when creating a training or processing job. Amazon SageMaker AI automatically evaluates your list in priority order and launches on the first type with available capacity – making it faster to secure GPU resources and start training. This removes the manual retry loops, complex monitoring scripts, and additional time teams sometimes invest in building systems to manage job submission for jobs that can run across multiple instance types.
>
> The result is faster job starts, higher capacity utilization, and more time spent building models rather than managing constraints.
>
> Customer challenges
>
> During peak demand periods, securing your preferred GPU instances on-demand can be challenging. When a training job is pinned to a single instance type and that capacity isn’t immediately available, some teams might resort to submitting multiple requests across different types to find where capacity exists. This manual process can slow down the experimentation cycle. For time-critical workloads like nightly re-training pipelines, production fine-tuning runs, and scheduled data processing, these delays can impact model freshness and iteration speed.
>
> Figure 1: A training job pinned to one instance type waits for capacity while other instance types may have capacity
>
> Teams have responded with custom retry scripts that poll job status, cancel stalled requests, and resubmit with alternative instance types. But these workarounds are brittle. They don’t integrate with reserved capacity options such as Flexible Training Plans (FTP), and they add operational overhead that compounds across multiple training runs.
>
> The core challenge is that pinning a training job to a single instance type creates fragility. Many training workloads run equivalently on two or three instance families, so teams with Flexible Training Plans need a way to express a preference order. They can then try the reservation first and fall back to alternative instance types using on-demand capacity.
>
> Consider these scenarios. A team training a multi-billion parameter model submits multiple job requests to find available capacity, while equivalent compute on another instance type is available. A nightly processing pipeline is pinned to a single type and fails at 2 AM with an InsufficientCapacityError. Had the platform evaluated alternative types at launch, the job would have started. An organization with a Training Plan wants their reservation evaluated first, then an alternative type on on-demand if the plan is fully consumed, without resubmitting. In each case, the answer is the same: let the platform evaluate multiple instance types automatically at job creation, in a single API call.
>
> Solution: Instance preference lists
>
> Instance Preferences lists on SageMaker Training and Processing Jobs: instead of requesting one instance type, you provide an ordered priority list of up to five types. Amazon SageMaker AI handles the rest. It evaluates your list in priority order, selects the first type with available capacity, and launches your job without manual intervention.
>
> The following diagram illustrates the end-to-end provisioning workflow. It shows how a training job request flows through the instance preference list, beginning with the reserved capacity check and then falling back to alternative instance types using on-demand capacity if the preferred type is unavailable.
>
> Figure 2: End-to-end provisioning workflow for an instance preference list, from the reserved capacity check to on-demand fallback
>
> Step 1: You submit your job with an ordered preference list of up to five instance types as shown in the preceding diagram.
>
> Step 2: Amazon SageMaker AI validates your job configuration and preference list against supported instance types and resource limits.
>
> Step 3: The scheduler performs a single in-memory sweep across your ordered types and identifies the first with available capacity.
>
> Step 4: The winning instance type provisions immediately and your job begins execution.
>
> Retry (if needed): If no listed type has capacity at the moment of evaluation, the job enters an efficient event-driven queue and automatically retries when capacity becomes available. This retry window is bounded by MaxPendingTimeInSeconds, which gives you control over maximum queue time.
>
> MaxPendingTimeInSeconds takes effect only for jobs that request accelerated computing instance types, such as instances in the ml.p, ml.g, and ml.trn families. It has no effect on jobs that request CPU-only instance types.
>
> If the job specifies InstancePreferences, MaxPendingTimeInSeconds bounds the total time Amazon SageMaker AI spends working through your list of instance types. This timeout applies to the entire preference list, not to each instance type individually. It only takes effect when the list includes at least one accelerated computing instance type.
>
> Your job either starts immediately on the first available type or waits with automatic retry. There are no custom scripts and no polling loops.
>
> Training Plan integration
>
> Organizations that have invested in Flexible Training Plans (FTPs), which reserve GPU capacity for a defined duration at discounted rates, gain a natural extension with instance preference lists. You can attach a Training Plan to specific preferences in your list and leave others on on-demand. The sweep evaluates your reservation first. If that preference can’t provision, it moves to the next type in your list, which might use on-demand capacity.
>
> The diagram compares two provisioning paths. The first path uses a Flexible Training Plan, which provides reserved GPU capacity that is pre-paid and guaranteed. This option takes priority in the preference list, and the plan type must match the specified preference (for example, ml.p5.48xlarge with a TrainingPlanArn). If reserved capacity is unavailable, the system falls back to the second path, which provisions on-demand capacity at standard rates with no commitment required (for example, ml.p5.24xlarge). Whichever path has capacity first wins, and no manual switching is required.
>
> Figure 3: Reserved Flexible Training Plan capacity takes priority, with automatic fallback to on-demand capacity
>
> Now that you understand how instance preference lists work on Amazon SageMaker training jobs, we will walk through the implementation with code examples.
>
> Code example: Training job with instance preferences
>
> The following examples demonstrate how to configure instance preferences using the Amazon SageMaker Python SDK v3 with the ModelTrainer class. Each example shows a different real-world scenario you can adapt for your own workloads.
>
> Example 1: Uniform count of 3 GPU types (P5 to P4d to P4de)
>
> This example specifies three GPU instance types with the same instance count. Amazon SageMaker AI attempts to provision the first preference (P5) and falls back to P4d or P4de if capacity is unavailable.
>
> Using the Amazon SageMaker Python SDK v3 (ModelTrainer):
>
> from sagemaker.core.shapes.shapes import InstancePreference
>
> from sagemaker.train.model_trainer import ModelTrainer
>
> from sagemaker.train.configs import Compute, OutputDataConfig
>
> trainer = ModelTrainer(
>
> training_image="763104351884.dkr.ecr.us-east-1.amazonaws.com/pytorch-training:2.3.0-gpu-py311-cu121-ubuntu22.04-sagemaker",
>
> source_code="train.py",
>
> role="arn:aws:iam:: 111122223333:role/SageMakerExecutionRole",
>
> base_job_name="large-model-training-70b",
>
> output_data_config=OutputDataConfig(
>
> s3_output_path="s3:// amzn-s3-demo-bucket /training-output/"
>
> ),
>
> compute=Compute(
>
> instance_count=8, # Same count regardless of which type wins
>
> volume_size_in_gb=500,
>
> keep_alive_period_in_seconds=3600,
>
> instance_preferences=[
>
> InstancePreference(instance_type="ml.p5.48xlarge"), # Priority 1: H100
>
> InstancePreference(instance_type="ml.p4d.24xlarge"), # Priority 2: A100
>
> InstancePreference(instance_type="ml.p4de.24xlarge"), # Priority 3: A100 (80GB)
>
> ],
>
> ),
>
> )
>
> trainer.train(wait=False)
>
> print(f"Job submitted: {trainer._latest_training_job.training_job_name}")
>
> Example 2: Per-preference counts for compute equivalency
>
> Not all instance types deliver the same throughput per node. When your preference list includes instance types with different GPU architectures, you can specify a different instance count for each entry to achieve roughly equivalent total compute. In this example, two ml.g6.48xlarge instances (16 L40S GPUs total) are listed as the first preference, with four ml.g5.48xlarge instances (32 A10G GPUs total) as the fallback to compensate for lower per-GPU performance.
>
> compute = Compute(
>
> volume_size_in_gb=500,
>
> instance_preferences=[
>
> # 2× g6.48xlarge (8× L40S GPUs each = 16 GPUs total)
>
> InstancePreference(instance_type="ml.g6.48xlarge", instance_count=2),
>
> # 4× g5.48xlarge (8× A10G GPUs each = 32 GPUs, but lower per-GPU perf)
>
> InstancePreference(instance_type="ml.g5.48xlarge", instance_count=4),
>
> ],
>
> )
>
> Tip: Use per-preference counts when your training script can adapt to different GPU counts (for example, through torchrun with --nproc_per_node=auto). Each configuration should deliver roughly equivalent total throughput for your workload.
>
> Example 3: Training Plan integration (reserved and on-demand hybrid)
>
> This example combines reserved capacity from a Training Plan with on-demand fallback so that jobs can start even when reserved capacity is fully utilized.
>
> compute = Compute(
>
> instance_count=4,
>
> volume_size_in_gb=500,
>
> instance_preferences=[
>
> # Priority 1: Use my reserved P5 capacity (guaranteed, no wait)
>
> InstancePreference(
>
> instance_type="ml.p5.48xlarge",
>
> training_plan_arns=[
>
> "arn:aws:sagemaker:us-west-2:111122223333:training-plan/my-p5-reservation"
>
> ],
>
> ),
>
> # Priority 2: On-demand P4d (if reservation is fully consumed)
>
> InstancePreference(instance_type="ml.p4d.24xlarge"),
>
> # Priority 3: On-demand P4de (last resort)
>
> InstancePreference(instance_type="ml.p4de.24xlarge"),
>
> ],
>
> )
>
> So far, the examples have focused on training jobs where instance flexibility accelerates model experimentation. The same capacity challenges also affect data processing workloads.
>
> The implementation follows a similar pattern. Instead of configuring instance preferences on the training resource, you specify them on the ClusterConfig for your processing job. You provide an ordered list of acceptable instance types, and Amazon SageMaker AI evaluates them in priority order at launch time. The first type with available capacity provisions your processing cluster automatically.
>
> Code example: Processing job with instance preferences
>
> Processing jobs support the same fallback mechanism on ClusterConfig:
>
> from sagemaker.processing import Processor
>
> processor = Processor(
>
> role="arn:aws:iam::123456789012:role/SageMakerExecutionRole",
>
> image_uri="763104351884.dkr.ecr.us-east-1.amazonaws.com/pytorch-training:2.3.0-gpu-py311-cu121-ubuntu22.04-sagemaker",
>
> instance_count=2,
>
> volume_size_in_gb=100,
>
> entrypoint=["python3", "process.py"],
>
> instance_preferences=[
>
> {"InstanceType": "ml.g5.12xlarge"}, # Priority 1
>
> {"InstanceType": "ml.g5.4xlarge"}, # Priority 2
>
> {"InstanceType": "ml.m5.12xlarge"}, # Priority 3 (CPU fallback)
>
> ],
>
> )
>
> processor.run(
>
> inputs=[...],
>
> outputs=[...],
>
> )
>
> Note: Processing jobs don’t support training plan integration. The TrainingPlanArns field is for training jobs only.
>
> Best practices
>
> Keep these guidelines in mind when you configure instance preference lists for your training jobs.
>
> 1. List only compatible instance types
>
> Amazon SageMaker AI doesn’t validate cross-type compatibility (GPU architecture, Elastic Fabric Adapter (EFA) support, driver versions). Make sure that your training container works on all listed types.
>
> 2. Use per-preference counts for throughput equivalency
>
> If your preference list has different per-node compute power, adjust counts to match total throughput:
>
> { "InstanceType": "ml.p5.48xlarge", "InstanceCount": 2 }, // 2× H100 nodes
>
> { "InstanceType": "ml.p4d.24xlarge", "InstanceCount": 4 } // 4× A100 nodes ≈ same total FLOPS
>
> 3. Combine with Training Plans for guaranteed and flexible capacity
>
> Place your reserved capacity first in the preference list so that Amazon SageMaker AI attempts to launch with pre-paid resources before falling back to on-demand alternatives.
>
> Priority 1: Reserved P5 (via training plan) → instant if reservation available
>
> Priority 2: On-demand P4d → good fallback at standard rates
>
> Priority 3: On-demand P4de → last resort
>
> 4. Bound queue time with MaxPendingTimeInSeconds
>
> Choose how long the job may keep retrying the list before it stops (only applies to accelerated computing instance types):
>
> StoppingCondition={
>
> "MaxRuntimeInSeconds": 86400,
>
> "MaxPendingTimeInSeconds": 1800 # Fail after 30 minutes if no capacity
>
> }
>
> Conclusion
>
> Instance Preferences transforms GPU capacity management from an engineering burden into a one-line configuration change. Instead of building custom retry logic, monitoring capacity dashboards, and waking up on-call engineers for failed overnight pipelines, you declare your flexibility upfront and let SageMaker AI handle the rest.
>
> Get started today:
>
> Update your Amazon SageMaker Python SDK: pip install --upgrade sagemaker.
>
> Add instance_preferences to your Compute configuration using the Amazon SageMaker AI Developer Guide.
>
> List 2–5 compatible instance types in priority order.
>
> Submit your job from the Amazon SageMaker AI console and let Amazon SageMaker AI find capacity automatically from your preferred list.
>
> To learn more about instance types, pricing, and Training Plans, see the Amazon SageMaker AI detail page and the GitHub code for implementation.
>
> About the authors
>
> Kanwaljit Khurmi
>
> Kanwaljit is a Senior Manager of Solutions Architecture and Data Scientists at Amazon Web Services, specializing in AI and ML. He collaborates with AWS product teams, engineering, and customers to provide guidance and technical assistance for maximizing the value of their hybrid GenAI solutions on AWS. Kanwaljit specializes in helping customers with containerized, data science, and machine learning applications.
>
> Mona Mona
>
> Mona currently works as Sr AI/ML specialist Solutions Architect at Amazon. She is a published author of three books and her latest book is AI Agents on AWS. She has authored 20+ blogs on AI/ML and cloud technology and a co-author on a research paper on CORD19 Neural Search which won an award for Best Research Paper at the prestigious AAAI (Association for the Advancement of Artificial Intelligence) conference.
>
> Michael Oguike
>
> Michael is a Product Manager for Amazon SageMaker AI. He is passionate about using technology and AI to solve real-world problems. At AWS, he helps customers across industries build, train, and deploy AI/ML models at scale. Outside of work, Michael enjoys exploring behavioral science and psychology through books and podcasts.
>
> Deep Shah
>
> Deep is a Software Development Engineer on the Amazon SageMaker team, where he works on the infrastructure that powers model training on AWS. When he’s not scaling training systems, he enjoys sim racing, reading, and traveling.
>
> Safir Alvi
>
> Safir is a Worldwide GenAI/ML Go-To-Market Specialist at AWS based in New York. He focuses on advising strategic global customers on scaling their model training and inference workloads on AWS, and driving adoption of Amazon SageMaker AI Training Jobs and Amazon SageMaker HyperPod. He specializes in optimizing and fine-tuning generative AI and machine learning models across diverse industries, including financial services, healthcare, automotive, and manufacturing.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。