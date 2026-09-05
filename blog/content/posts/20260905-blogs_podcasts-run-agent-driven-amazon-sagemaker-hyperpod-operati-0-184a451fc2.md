---
title: "Run agent-driven Amazon SageMaker HyperPod operations with InstantStart"
date: 2026-09-05T12:28:20+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "Advanced (300)", "Amazon SageMaker HyperPod", "Thought Leadership", "博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:72aa540d92ff245e6afb648560a67d0f37225ab32ac3d07f92ac56063ceac2fb"
source_payload_sha256: "sha256:12b48fd6d26c12cda252187cc8bbf7725df25b3b5fe4bbee47a468a1f9a04607"
observation_id: obs_184a451fc248c54661fd642cd91ea7e5e5a954a4d78540e2f70a6e00078b9e56
event_id: evt_f8aed450d9997f130322240296641f981bf00dc1f7a023b8858bb8ef296048b8
revision_id: rev_30c389d57aba891db8bf7c96e48907f92098b8f6b875962238c6e6261226ff4b
source_published_at: 2026-09-04T16:12:17Z
first_seen_at: 2026-09-05T04:27:12.983411Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: true
source_truncation_reason: "crawler_feed_content_limit"
source_support: 1.0
source_title_chars_original: 71
interpretation_sha256: "sha256:bf8d3b9cbd8060e50015448cb86db27a2844473bb7bfa73b63bf35b036bae1ba"
description: "这是一篇关于 HyperPod InstantStart 的技术实现解读，介绍了如何通过 AI agent 驱动 SageMaker HyperPod 集群的自动化运维。该方案将集群创建、容量配置、训练和推理等工作流封装为统一的控制平面，同时提供 Web 界面和终端两种交互方式。"
external_url: https://aws.amazon.com/blogs/machine-learning/run-agent-driven-amazon-sagemaker-hyperpod-operations-with-instantstart
parent_observation_id: null
last_seen_at: 2026-09-05T04:27:12.983411Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/run-agent-driven-amazon-sagemaker-hyperpod-operations-with-instantstart](https://aws.amazon.com/blogs/machine-learning/run-agent-driven-amazon-sagemaker-hyperpod-operations-with-instantstart)
- **发布域名**: aws.amazon.com

## 要点解读

### 这是什么

这是一篇关于 HyperPod InstantStart 的技术实现解读，介绍了如何通过 AI agent 驱动 SageMaker HyperPod 集群的自动化运维。该方案将集群创建、容量配置、训练和推理等工作流封装为统一的控制平面，同时提供 Web 界面和终端两种交互方式。核心思路是把原本分散的 AWS 资源调用和 Kubernetes 操作整合为可组合的、受保护的 API 层。

### 用在哪里

适用于需要频繁创建和管理大规模机器学习基础设施的团队，尤其是已经在使用 Amazon EKS 作为编排平台、同时依赖 HyperPod 提供容错和弹性能力的场景。对于需要将集群生命周期管理集成到自动化流水线或 AI 工作流中的开发者，这条内容提供了架构层面的参考。

### 可以推断的

推测：该方案降低了跨服务编排的复杂度，但团队仍需理解 EKS 和 HyperPod 的边界划分。当故障发生时，准确定位是哪个层面出了问题需要一定的知识储备。

推测：AI agent 通过统一接口调用后端 API，而非直接操作 CLI，这意味着验证逻辑可以在单一位置生效，减少了不同入口处行为不一致的风险。

## 来源摘要/节选

> If you run foundation model (FM) workloads on Amazon SageMaker HyperPod, you know the work is rarely a single task. It is a chain of dependent ones. An infrastructure team creates the network and control plane, attaches accelerator capacity, and installs cluster dependencies in the right order. It also prepares storage and identity, keeps distributed jobs alive through hardware faults, deploys model servers, and watches all of it. Each step has its own API, its own failure modes, and its own waiting period. Most of the operational pain lives in the handoffs between them.
>
> Amazon SageMaker HyperPod removes a large share of that burden. It offers managed, resilient compute and Amazon EKS integrated capabilities for health monitoring, node autoscaling, training recovery, and inference. Amazon Elastic Kubernetes Service (Amazon EKS) stays the user-managed orchestration surface. This gives your team direct Kubernetes access. It also makes your team responsible for composing AWS resources, add-ons, workloads, and day-two operations into a coherent whole.
>
> HyperPod InstantStart is an open source control plane built around that composition problem. It gives you two ways to drive the same control plane. In the web interface, creating a cluster with dependencies installed, automatic node recovery on, and storage mounted is a form, a progress panel, and a refresh button. In a terminal, it is one sentence.
>
> [hypd-inst-agent] &gt; Help me create a new HyperPod cluster
>
> An AI agent then plans the multi-stage workflow, launches each stage, and polls asynchronous AWS operations to completion. It pauses only for the decisions that are genuinely yours, such as Availability Zone, instance type, and capacity type. Then it hands back a running cluster with storage mounted. Both interfaces call the same backend APIs, pass the same validations, and read the same persisted operation state. Neither one has private logic the other lacks.
>
> In this post, we walk through the system underneath both interfaces. We show how it turns cluster bootstrap, capacity, training, inference, and storage into guarded, retryable operations. We cover which parts are HyperPod managed capabilities and which parts the project adds. And we explain why encoding operational rules into a control-plane API, instead of handing an agent a raw CLI, is what makes agent-driven infrastructure dependable.
>
> Solution overview
>
> HyperPod InstantStart runs as a single out-of-band management container in your AWS account. It calls AWS service APIs and the Kubernetes API. It doesn’t sit in the data path of a training job or an inference request. Everything it creates is a standard AWS or Kubernetes resource. You can inspect it with the AWS Command Line Interface (AWS CLI) and kubectl.
>
> The following diagram illustrates the solution architecture and where responsibility changes hands.
>
> Read the diagram from left to right. Your infrastructure team drives one entry point. The web UI, the REST API, and the Model Context Protocol (MCP) tools that the AI agent uses are three faces of the same container, so both interfaces enter through one door. Behind them sits the staged provisioning and idempotent reconciliation logic that the rest of this post describes. From there the control plane calls two API surfaces.
>
> The Kubernetes side is Amazon EKS, which stays user-managed. It holds the Kubernetes API, the HyperPod training and inference operators installed as EKS add-ons, and the HyperPodPyTorchJob and InferenceEndpointConfig resources they reconcile into training and inference pods. The AWS side is Amazon SageMaker HyperPod, which is AWS managed. Its capabilities fall into four groups. Infrastructure covers health monitoring, deep health checks, and automatic node recovery. Capacity covers continuous provisioning and managed Karpenter autoscaling. Training covers process-level recovery and managed tiered checkpointing. Inference covers intelligent routing and tiered key-value (KV) caching.
>
> The two halves meet at the HyperPod instance groups. Kubernetes schedules pods onto them, and HyperPod manages them. That is the single most useful thing to know when something needs attention, because it tells you which half AWS operates and repairs without your involvement. AWS integrations sit around that path, and the diagram shows the storage and observability ones. Amazon Simple Storage Service (Amazon S3), Amazon FSx for Lustre, and Amazon Elastic Container Registry (Amazon ECR) carry images, data, and checkpoints. Amazon Managed Service for Prometheus and Amazon Managed Grafana receive health and utilization. Managed MLflow on Amazon SageMaker AI also receives metrics and artifacts.
>
> InstantStart organizes this environment into four layers.
>
> Layer
>
> InstantStart contribution
>
> Managed foundation
>
> Infrastructure
>
> Staged EKS creation or import, dependency reconciliation, network layout, multi-cluster state
>
> AWS CloudFormation and Amazon EKS
>
> Capacity and resilience
>
> Instance-group workflows, capacity-type choices, managed-feature configuration
>
> HyperPod health monitoring, automatic node recovery, continuous provisioning, managed Karpenter
>
> Workloads and data
>
> Training recipes, two inference paths, model download and storage workflows, MLflow integration
>
> HyperPod training and inference operators, Amazon S3, FSx for Lustre, managed MLflow
>
> Interfaces
>
> Web UI with live state, REST APIs, MCP tools, and agent skills
>
> AWS and Kubernetes APIs remain directly inspectable
>
> One design principle ties the two interfaces together. The MCP tools wrap the backend’s own REST APIs, the exact code paths the browser calls, rather than the AWS CLI or SDK, so a validation added once protects both. We return to why that matters for agents. First, let’s watch the control plane do its main job.
>
> Prerequisites
>
> Use least-privilege IAM roles for deployment and ongoing operations. Follow AWS guidance for CloudFormation access control and SageMaker HyperPod IAM, and limit Amazon S3 access to the designated project bucket. Two capacity items take AWS turnaround time, so start them early. Request an Amazon SageMaker service quota increase for Cluster Usage on each instance type you intend to run, and for high-end accelerator types, purchase an Amazon SageMaker Flexible Training Plan to reserve capacity. Check your virtual private cloud (VPC) quota as well, because the staged provisioning path creates a VPC per cluster by default.
>
> A management environment to run the container in. The project provides an AWS CloudFormation template that creates the environment, shared S3 bucket, and supporting IAM roles. Deploy it from the AWS Management Console or with the AWS CLI.
>
> On the instance created by the stack, clone the repository and run ui-panel/start-prod.sh. The script pulls the prebuilt container image from public Amazon ECR and starts it with your kubectl and AWS credentials mounted, serving the web interface on port 3099. Reach that port through an AWS Systems Manager port-forwarding session rather than opening it to the internet. The template’s security group allows public access to it for convenience. Restrict that before you use the environment for anything real.
>
> For the agent interface, Kiro CLI installed and authenticated. The MCP server and the agent skills ship inside the same container, so nothing else needs installing locally.
>
> Creating a cluster: A conversation and a console
>
> Moving from an empty account to usable HyperPod capacity takes several long-running, order-dependent stages. InstantStart deliberately separates them into EKS control-plane creation, active-cluster selection, dependency reconciliation, HyperPod cluster creation, and storage setup. Separating them means a failure in a later stage doesn’t roll back an earlier stage that already succeeded. EKS control-plane creation finishes in roughly 8–12 minutes. Every later stage records its own status and is independently retryable.
>
> Through the web interface, this is the Cluster Management page. You enter a cluster tag, create, and watch the staged progress indicators. Through the agent, the whole pipeline is a conversation. The following is a condensed transcript from a real session with the hypd-inst-agent, an agent configuration for Kiro CLI that loads the project’s MCP server and skills.
>
> [hypd-inst-agent] &gt; Help me create a new HyperPod cluster
>
> &gt; Creating a HyperPod cluster is a multi-step process:
>
> 1. Create EKS cluster (approximately 8-12 minutes)
>
> 2. Switch to the new cluster and verify
>
> 3. Install dependencies
>
> 4. Create HyperPod cluster
>
> 5. Configure S3 storage
>
> 6. Final verification
>
> Let me first check the existing cluster situation:
>
> Running tool cluster_list_all (from mcp server: hypd-inst)
>
> &gt; There are currently 2 existing clusters. Would you like to give the new cluster a tag name, or should I auto-generate one?
>
> [hypd-inst-agent] &gt; Go ahead
>
> Running tool cluster_create_eks {"clusterTag": "hypd-0304b"}
>
> &gt; EKS cluster creation has started. I'll check progress every 2 minutes.
>
> Running tool wait_seconds {"seconds": 120}
>
> Running tool cluster_get_eks_creation_status
>
> &gt; Still creating (about 4 minutes elapsed). Continuing to wait...
>
> ...
>
> &gt; Step 1 complete! EKS cluster hypd-0304b created successfully.
>
> ...
>
> &gt; Step 3 complete! All dependencies installed successfully.
>
> Now I need the following information from you to create HyperPod:
>
> Availability Zone, GPU instance type, instance count, and capacity type (On-Demand or Training Plan)?
>
> [hypd-inst-agent] &gt; us-west-2c, one g6.4xl
>
> Running tool hyperpod_create {"AcceleratedInstanceType": "ml.g6.4xlarge", "AcceleratedInstanceCount": 1, "availabilityZone": "us-west-2c", ...}
>
> ...
>
> &gt; HyperPod cluster creation fully complete! Summary:
>
> | EKS Cluster | eks-cluster-hypd-0304b |
>
> | HyperPod Cluster | hp-cluster-hypd-0304b |
>
> | Node | 1x ml.g6.4xlarge (On-Demand) |
>
> | Node Status | Ready / Schedulable |
>
> | S3 Storage | s3-claim mounted |
>
> Three behaviors in this transcript come from workflow rules encoded in the project’s agent skill, not from improvisation.
>
> The agent polls to completion. Every long-running operation is followed by wait_seconds and a status tool until it reaches a terminal state. The agent is not allowed to stop early and tell you to check back later. The conversation ends with a verified cluster, not a submitted request.
>
> The agent asks only decision-grade questions. Cluster tag, Availability Zone, instance type, and capacity type are your decisions. Subnet CIDRs, route tables, security groups, and installation order aren’t. They are control-plane work.
>
> The agent inspects before it creates. It lists existing clusters first. It queries valid Availability Zones and instance types before offering choices, so the options that you see are the ones this account and Region can actually satisfy.
>
> The networking that the conversation doesn’t mention shows what the control plane encodes. The AWS CloudFormation path can create or reuse the VPC. It separates EKS control-plane subnets from HyperPod compute subnets, because their address-space needs differ by an order of magnitude. Compute subnets are sized at /20 to hold large accelerator fleets. Every capacity path runs through one function, ensureComputeSubnet(), with a fixed priority. It uses an explicitly specified subnet, or reuses a compatible per-Availability-Zone subnet, or creates one complete with route table and S3 gateway endpoint association. Cluster creation and later capacity expansion share this logic, so there is exactly one place where the network layout can be right or wrong.
>
> Capacity choices, with resilience as the default
>
> After the control plane exists, capacity management becomes the recurring operation. You add an instance group for a new workload, choose how to pay for it, and trust the control plane to keep it healthy.
>
> InstantStart creates HyperPod clusters with automatic node recovery enabled. HyperPod can reboot or replace faulty nodes based on findings from its health-monitoring agent, basic health checks, and, when configured, deep health checks. Deep checks stress-test GPUs and Elastic Fabric Adapter (EFA) connectivity before nodes accept work. Health findings also project into Kubernetes labels, taints, and annotations, so your schedulers and tooling can react through the Kubernetes API without calling AWS.
>
> When you add an instance group, the system treats the full capacity decision as one create-time operation rather than scattered follow-up configuration.
>
> Capacity type. Choose On-Demand, Amazon Elastic Compute Cloud (Amazon EC2) Spot Instances for fault-tolerant workloads, or reserved capacity through an Amazon SageMaker training plan. A training plan pins its capacity to specific Availability Zones. The control plane reconciles your zone selection against the plan rather than letting the mismatch surface as a confusing failure. Capacity type is fixed for the life of the group.
>
> Network interface mode. Instance types with multiple network cards can request EFA-only interfaces, which conserve VPC IP addresses. This setting is fixed after the group is created. The InstantStart surfaces it as a create-time field instead of letting you discover the immutability from a rejected update.
>
> Subnet placement. By default, groups share the per-AZ compute subnet. A large group can request a dedicated subnet to avoid IP exhaustion, and that subnet deliberately outlives the group so a successor can reuse it.
>
> The following screenshot shows the Add Instance Group form, where these choices become one create-time step.
>
> Figure 2: The Add instance group form, where capacity choices become one create-time step
>
> Some instance-group fields are immutable and others are easy to lose. So the control plane doesn’t hand-assemble an update request. Whenever it resubmits an instance group, it normalizes the group through an explicit field allowlist. Settings such as OnStartDeepHealthChecks and NetworkInterface carry forward, so an unrelated scaling operation can’t silently reset a group’s health-check or EFA configuration. The same normalization runs whether the request came from the web interface or an MCP tool call.
>
> Managed Karpenter: Autoscaling without operating Karpenter
>
> A static instance group sets how much capacity you own. HyperPod managed Karpenter-based node autoscaling decides how much of it runs at any moment. AWS operates the Karpenter controller itself, and nodes launch from HyperPod instance groups scaled up from zero rather than from raw Amazon EC2. Autoscaled capacity therefore inherits the health monitoring and automatic node recovery described earlier, instead of arriving as unmanaged instances. Scheduling stays a standard Karpenter NodePool bound to a HyperpodNodeClass, which InstantStart provisions with working defaults, including consolidation that scales an idle group back toward zero. Because the control plane already defaults to continuous provisioning and automatic recovery, enabling managed Karpenter is a validated toggle rather than a runbook. One scoping note: HyperPod managed Karpenter manages HyperPod instance groups, not general-purpose Amazon EC2 capacity.
>
> Managed capabilities as reconciled state, not runbooks
>
> HyperPod ships several managed capabilities, and each has a documented multi-step setup. These include the training operator, the inference operator, managed tiered checkpointing, and managed autoscaling. InstantStart exposes them in one Advanced Features panel. The value is not the checkboxes. It is that each checkbox maps to a dependency-aware backend operation.
>
> The following screenshot shows the Advanced Features panel, where each toggle maps to a backend operation.
>
> Figure 3: The Advanced Features panel, where each toggle maps to a dependency-aware backend operation
>
> Enabling managed tiered checkpointing, for example, does more than flip a cluster setting. Managed tiered checkpointing uses multiple storage tiers, including cluster CPU memory. Persisting checkpoints requires an identity chain, a Kubernetes service account, an IAM role and policy, an OpenID Connect (OIDC) trust relationship, and the annotation binding them together. The toggle provisions that chain end to end, and disabling it removes the same chain. Half-provisioned IAM Roles for Service Accounts (IRSA) is one of the least pleasant things to debug on EKS, so the operation is closed-loop in both directions.
>
> The panel also taught the project a lesson about idempotency. An early implementation submitted every form value as desired state, and that produced a real bug. Enabling the inference operator installs cert-manager as a dependency when it is absent. The form’s cert-manager field still held a stale value. A later unrelated submission then removed the dependency that had just been installed. The fix was an explicit-diff contract. The interface submits only the fields the user actually touched. The backend checks field presence, reads actual cluster state, and no-ops when actual and requested state already match. That contract applies the same way to UI requests and MCP requests, which is exactly why an agent can be trusted to call the same endpoint.
>
> Through the agent, the whole panel is one exchange.
>
> [hypd-inst-agent] &gt; Help me install tiered storage and training operator
>
> Running tool hyperpod_get_advanced_features
>
> &gt; Currently both are not enabled. I'll enable them together.
>
> Running tool hyperpod_update_advanced_features {"tieredStorage": {"enabled": true, "configMode": "default"}, "trainingOperator": {"enabled": true&#125;&#125;
>
> &gt; Both features have been successfully enabled.
>
> The agent reads current state first and sends only the two features requested. The backend reconciles each independently. It is the same three-part discipline the web form follows.
>
> Training: Two submission paths and a recipe layer
>
> The training surface separates two decisions. How a job is submitted and kept alive is one. Which framework the job runs is another. The control plane gives you two task-submission paths at the bottom and a recipe layer on top. Adopting a new training framework doesn’t mean adopting a new operational model.
>
> Training and serving share the same cluster, and the control plane gives each of them two paths. The following diagram illustrates all four, the recipe layer above them, and the substrate they land on. Highlighted boxes mark where a HyperPod managed capability applies, and the sections below walk each path in turn.
>
> Figure 4: The two training paths and two inference paths, the recipe layer over them, and the shared HyperPod substrate
>
> The task layer: Recoverable submission through the training operator or KubeRay
>
> The first path is the Amazon SageMaker HyperPod training operator. It adds process-level fault recovery, hang-job detection through log-pattern monitoring, and outlier detection for distributed training. A single failed process no longer costs you a whole multi-node job restart. InstantStart installs it as an EKS add-on and submits work as HyperPodPyTorchJob resources, with the recovery policy visible in the workload specification rather than buried in defaults.
>
> runPolicy:
>
> jobMaxRetryCount: 5
>
> restartPolicy:
>
> numRestartBeforeFullJobRestart: 3
>
> evalPeriodSeconds: 21600
>
> maxFullJobRestarts: 1
>
> cleanPodPolicy: All
>
> Read that as a recovery budget. Up to three in-place process restarts within a six-hour evaluation window, then the operator escalates to a single full job restart. Containers launch through hyperpodrun instead of torchrun, and the operator injects topology values such as NNODES and NPROC_PER_NODE. That removes the most common source of distributed-launch misconfiguration while keeping the contract thin. You bring your own image and shell entry point. It also greatly simplifies the PyTorch distributed configuration you would otherwise assemble by hand.
>
> The second path is standard KubeRay, which InstantStart installs on request from the Advanced Features panel described earlier. Some workloads are Ray-native by design, most notably reinforcement learning, where a head node coordinates rollout and training workers. For those, forcing them through a PyTorch job abstraction would be the wrong shape. Ray clusters and jobs are submitted as first-class workloads onto the same HyperPod nodes, with the same storage mounts and the same monitoring views. Choosing a path is a statement about the workload’s orchestration model, not a fork in the control plane.
>
> The recipe layer: Frameworks as configuration
>
> On top of the task layer, the project ships recipes that integrate widely used training frameworks. Switching frameworks changes a form, not your operations.
>
> Recipes ship for plain PyTorch scripts, LLaMA-Factory, MS-Swift, and VERL reinforcement learning, the last of these on the KubeRay path. Each takes an entry script or a framework configuration file, and the repository documents the per-framework fields.
>
> The recipes share one data contract. The same S3 bucket is mounted at ~/workspace/s3 in the development environment and at /s3 inside pods. You can edit a training script or a dataset definition locally and the next job picks it up, with no image rebuild. Recipes that run through the training operator inherit its recovery behavior without per-framework work. That is the payoff of separating the two layers.
>
> Training also connects to day-two workflows. Job logs stream to the browser over WebSocket. Each recipe can optionally report metrics such as training throughput to managed MLflow on Amazon SageMaker AI. InstantStart automates the service-account IAM path that training pods use to write runs, and the UI reads run history for display, including cross-account experiment sharing under fine-grained IAM permissions. One accuracy note. Managed MLflow is an Amazon SageMaker AI capability, and the CSI drivers described later are Amazon EKS capabilities. InstantStart’s contribution is wiring them into the workflow, not reimplementing them.
>
> Serving models two ways
>
> For inference, the control plane offers two paths with genuinely different ownership models. Keeping both is a deliberate choice, not a transition.
>
> The managed path hands lifecycle to the HyperPod inference operator. You describe the endpoint declaratively, including model location in Amazon S3, worker image, invocation port, GPU resources, and replicas. The operator reconciles it into model workers, load balancing, and TLS. Two managed capabilities are the main reason to choose this path, and both are declared alongside the endpoint.
>
> kvCacheSpec:
>
> enableL1Cache: true
>
> enableL2Cache: true
>
> l2CacheSpec:
>
> l2CacheBackend: tieredstorage
>
> intelligentRoutingSpec:
>
> enabled: true
>
> routingStrategy: prefixaware
>
> Managed tiered KV caching keeps an L1 cache in CPU memory with an L2 tier backed by Redis or Amazon SageMaker managed tiered storage. Intelligent routing offers prefix-aware, KV-aware, session, and round-robin strategies. InstantStart’s job here is validation and generation. It renders the configuration, checks the parts that must agree with each other, and leaves reconciliation to the operator.
>
> The following screenshot shows the managed inference form, with KV caching and intelligent routing declared alongside the endpoint.
>
> Figure 5: The managed inference form, with KV caching and intelligent routing declared alongside the endpoint
>
> The self-managed path deploys a serving container of your choice, such as vLLM, SGLang, or your own, as a standard Kubernetes deployment. It offers three service shapes: an external load balancer, a cluster-internal service, or a model pool. The pool keeps warm GPU workers labeled business=unassigned. Reassigning one to a service changes a label instead of recreating a pod and reloading weights. Scale-in refuses to remove workers still bound to a service. For multi-replica SGLang serving, the control plane can also deploy the SGLang router with cache-aware routing and drive autoscaling through Kubernetes Event-driven Autoscaling (KEDA). The scale target is the model workers, not the router that supplies the metrics.
>
> Deployment through the agent shows the guardrails in the tool contract. The project’s deployment skill forbids inferring GPU count from a tensor-parallel flag, so the agent confirms it.
>
> [hypd-inst-agent] &gt; Help me deploy: vllm serve Qwen/Qwen3-0.6B --max-model-len 1280 --tensor-parallel-size 1
>
> &gt; Before deploying I need to confirm: how many GPUs should this deployment request? (--tensor-parallel-size is a model-parallelism parameter; I need you to confirm the

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。