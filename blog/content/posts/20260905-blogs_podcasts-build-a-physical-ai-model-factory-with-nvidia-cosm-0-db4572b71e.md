---
title: "Build a Physical AI model factory with NVIDIA Cosmos 3 on SageMaker HyperPod"
date: 2026-09-05T05:31:02+08:00
draft: false
entry_kind: "auto"
tags: ["AI Agent", "生成式 AI", "深度学习", "Advanced (300)", "Amazon SageMaker HyperPod", "Technical How-to", "博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:437db99a2ad0b0a39fce4b917acc0a74adcc4da3b8216839a1e348db199ef214"
source_payload_sha256: "sha256:b144180ece01dbfe696596e2cde4d0016de825f7e5429d6fa2694f33b2f89c9e"
observation_id: obs_db4572b71eb09cccddf27d76236d4dc5d129d84d0c831a8ecd0d3b1f22ae58fe
event_id: evt_92b34a0be6061e61a820efd82cb68ed3258aff13aab1b5a5091c0e4646d1f45b
revision_id: rev_5c86583d63895e3c13f79bd3250c7128ca508bf5e7e64b263a19b88e817907bf
source_published_at: 2026-09-04T16:16:00Z
first_seen_at: 2026-09-04T21:28:51.322133Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: true
source_truncation_reason: "crawler_feed_content_limit"
source_support: 1.0
source_title_chars_original: 76
interpretation_sha256: "sha256:270fe2fcbaf92a06e8e5d5455de8461ad3042e7c4bd01ce242311dea7e127d20"
description: "这条内容介绍如何利用NVIDIA Cosmos 3在Amazon SageMaker HyperPod上构建一条持续的物理AI模型生产流水线，把合成数据生成、感知与策略后训练以及闭环仿真评估统一在同一模型框架中。"
external_url: https://aws.amazon.com/blogs/machine-learning/build-a-physical-ai-model-factory-with-nvidia-cosmos-3-on-sagemaker-hyperpod
parent_observation_id: null
last_seen_at: 2026-09-04T21:28:51.322133Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/build-a-physical-ai-model-factory-with-nvidia-cosmos-3-on-sagemaker-hyperpod](https://aws.amazon.com/blogs/machine-learning/build-a-physical-ai-model-factory-with-nvidia-cosmos-3-on-sagemaker-hyperpod)
- **发布域名**: aws.amazon.com

## 要点解读

### 这是什么  
这条内容介绍如何利用NVIDIA Cosmos 3在Amazon SageMaker HyperPod上构建一条持续的物理AI模型生产流水线，把合成数据生成、感知与策略后训练以及闭环仿真评估统一在同一模型框架中。

### 用在哪里  
适用于需要在机器人或自动驾驶等多种硬件上实现端到端感知‑决策闭环的研发团队，也适合希望在一套GPU资源上共享生成、后训练和评估工作负载的组织。

### 可以推断的  
推测：在同一节点池上调度生成、后训练和评估可以降低资源碎片化，提高整体GPU利用率。  
推测：采用统一的token流和多专家结构有助于在同一模型内部实现跨模态联合学习，从而简化部署和更新流程。

## 来源摘要/节选

> A Physical AI system, such as a robot or autonomous vehicle (AV) that translates real-world data into physical actions, can’t be built in a single training job. Instead, it takes a continuous pipeline: a loop of generating synthetic data, post-training perception and policy models, so the system understands its surroundings and can act, and evaluating both in closed-loop simulation. Running that pipeline continuously is the job of a Physical AI model factory, turning a stream of new real-world data into better models, round after round.
>
> This post shows how to build a Physical AI model factory with NVIDIA Cosmos 3 on Amazon SageMaker HyperPod, covering:
>
> What is unique about Cosmos 3: a Mixture-of-Transformers (MoT) design with per-layer joint attention and a deliberate train-versus-inference asymmetry.
>
> Why the design choices map cleanly onto Amazon SageMaker HyperPod with Amazon Elastic Kubernetes Service (Amazon EKS).
>
> Cluster and shared multi-terabyte storage layer setup.
>
> Distributed post-training for three representative workloads, with a complete end-to-end walkthrough of the robot-policy stage on a public DROID dataset.
>
> The accompanying repository contains the manifests and configuration files for each stage. You can find the runnable code, including the infrastructure templates and job manifests that turn this design into a working cluster, in the awsome-distributed-ai GitHub repository.
>
> Running the loop is a capacity commitment. Acquiring GPUs stage by stage adds variability at this scale: availability and lead times can vary, and the capacity that you do get might land in an Availability Zone or AWS Region away from your data. Committing capacity to the whole loop avoids that churn, whether through a flexible training plan for a bounded campaign or a capacity reservation for an open-ended one. Because you pay for that capacity whether or not the pipeline is making progress on it, the metric that governs cost is not the peak throughput of any one job. It is GPU goodput: the useful pipeline progress per reserved GPU-hour across the whole loop.
>
> Physical AI pipelines often provision separate GPU capacity for each stage: one set of nodes to generate synthetic data, another to post-train, another to evaluate, each with its own lifecycle to stand up and tear down. NVIDIA Cosmos 3 makes that unnecessary. As an open omnimodal world foundation model, Cosmos 3 treats video, image, action, and sound as a single token stream. It runs the same transformer trunk in three modes: a forward-dynamics world model for synthetic video generation, an inverse-dynamics action labeler, and a deployable action policy. Because one model family covers generation, post-training, and evaluation, those stages become three workloads scheduled onto one persistent, resilient GPU node pool under a single cluster control plane. It’s time-shared capacity rather than a separate pool per stage. NVIDIA released it under the Linux Foundation’s OpenMDW-1.1 license, and describes the architecture in the Cosmos 3 technical report.
>
> 1. How Cosmos 3 works
>
> A common pattern for world models is to pair a diffusion-transformer video generator with a separate vision-language model that provides text conditioning. Cosmos 3 takes a different approach: one trunk that handles both, integrated at every layer. That integration is what makes it useful as the engine of an end-to-end Physical AI model factory. Three architectural choices define it:
>
> One token stream. Every modality feeds into a single shared sequence, so one model can both read and generate across modalities. Images the model reads for understanding, pixels it generates, and a compact per-embodiment vector of pose deltas and grasp state each get their own encoder. A vision transformer (ViT) handles image understanding while a frozen Wan2.2 video variational autoencoder (VAE) handles pixel generation. That one action vector is what lets the same model drive both an AV and a robot arm. The sequence puts an autoregressive (AR) zone (the text and vision it reads) ahead of a diffusion zone (the video, audio, and action it produces).
>
> Two experts, joined at every layer (MoT). Each layer runs a reasoner that predicts the next token and a generator that denoises video, audio, and actions. Dual-stream attention joins them so generation stays grounded in the reasoner’s output at every layer, not only once at the end. The common alternative bolts a diffusion transformer (DiT) onto a vision-language model (VLM) and cross-attends to its final output once. Cosmos 3 grounds generation in the reasoner all the way down.
>
> Asymmetric at inference. Training and deployment do not run the same amount of work. Training runs the full denoising schedule and decodes video back to pixels, because that predicted video is part of the loss. On the robot, the same model runs a few denoise steps and skips video decoding entirely. The video latents are still produced internally to ground the action, but only the action tokens are decoded into the joint positions the robot executes.
>
> The following diagram shows the first two choices in one view: the shared token stream and the two experts joined by attention. The autoregressive (AR) subsequence (text and the vision tokens the model reads to understand) and the diffusion-model (DM) subsequence (the video, audio, and action tokens it generates) run through the shared Reasoner and Generator towers. The attention mask on the right shows how the two experts differ: DM queries attend over both AR and DM keys (full attention), while AR queries stay causal and never see the diffusion tokens.
>
> Figure 1: The Cosmos 3 shared token stream and its two experts joined by per-layer attention
>
> (source: Cosmos 3: Omnimodal World Models for Physical AI)
>
> Three action modes, one architecture
>
> The mid-trained base checkpoint runs three jobs by changing which tokens start as noise. Post-training then specializes a checkpoint to a single mode and control frequency.
>
> Forward dynamics (world model). Actions clean, video noisy. “Given this frame and this action, what comes next?” This is the synthetic-data engine, fanned out to generate long-tail driving scenes or rare manipulation interactions that real collection cannot reach affordably.
>
> Inverse dynamics (action labeler). Video clean, action noisy. “Given these two frames, what action caused the change?” Converts unlabeled video (raw teleoperation recordings, third-person robot video, YouTube driving footage) into action-labeled training data.
>
> Policy (the deployed robot). Both noisy, conditioned on 3-view image plus proprioception. It outputs 32 future joint positions, with predicted video frames as a byproduct that grounds the action prediction.
>
> The model family has two tiers: Cosmos3-Nano (16B parameters, on a dense 8B parameter Qwen3-VL backbone) and Cosmos3-Super (64B parameters, on a dense 32B parameter Qwen3-VL backbone). Task variants such as Cosmos3-Nano-Policy-DROID build on these tiers. NVIDIA also released Cosmos3-Edge, a compact 4B tier for on-device deployment (benchmarked on Jetson Thor and Orin). Edge shares the same physical-world pretraining data as Nano and Super but is built on a dense ~2B backbone trained from scratch rather than initialized from Qwen3-VL, so it is a separate weight lineage: you post-train Edge directly for the target hardware rather than shrinking a Nano checkpoint into it.
>
> The following diagram shows the three modes side by side, with solid boxes for clean (known) tokens and dashed boxes for noisy tokens the model denoises. Forward dynamics keep the actions and the current frame clean and denoises future video. Inverse dynamics keep the video clean and denoises the actions. The policy sees only the first frame clean and denoises the actions the robot will execute. The same architecture runs all three, and only the pattern of clean versus noisy tokens changes. In the base checkpoint all three modes are available; a post-trained variant such as Cosmos3-Nano-Policy-DROID is specialized to policy mode at 15 Hz with a 32-step horizon.
>
> Figure 2: The three action modes of one checkpoint, set by which tokens start as noise
>
> (source: Cosmos 3: Omnimodal World Models for Physical AI)
>
> 2. From one model to a perpetual model factory
>
> A team producing a robot or AV does not run one fine-tuning workload. It runs a loop: ingest real data, curate it, augment it with synthetic data, post-train, evaluate in a closed-loop simulation, deploy the policy, collect more data, and repeat.
>
> Figure 3: The Physical AI model factory as a four-stage flywheel
>
> The loop has four stages. (1) Ingest and curate real-world Physical AI data (DROID, BridgeData2, AV sensor logs) into a shared corpus on Amazon Simple Storage Service (Amazon S3) and Amazon FSx for Lustre. (2) A Cosmos3-Super teacher generates synthetic data to augment that corpus. (3) The combined synthetic and real corpus post-trains a deployable Cosmos3-Nano policy, with vision fine-tuning applied across both the Nano and Super tiers. (4) The policy is evaluated in closed-loop simulation, and its failures become new generation targets that re-enter the corpus for the next round.
>
> Ideally, that loop doesn’t stop, with each stage running again as new data arrives. That cadence makes the cost driver GPU goodput (useful pipeline progress per reserved GPU-hour) rather than the peak throughput of any one job. Goodput is highest when the stages share one pool, so few GPU-hours are lost re-provisioning or moving data between separate clusters. Cosmos 3 makes that possible: it unifies three model classes (a world-sim generator, a policy, a perception model) into one model running in different modes. To support that flywheel, the cluster underneath must match that shape: one persistent pool on one control plane, instead of a disparate compute environment per job.
>
> Amazon SageMaker HyperPod on Amazon EKS delivers exactly that shape. Each of the architectural choices behind Cosmos 3 creates a concrete cluster demand. The single token stream and the 64B MoT structure make training a long-sequence, multi-node job that needs a low-latency interconnect. The train-versus-inference asymmetry keeps generation, post-training, and evaluation on one model and one storage layer, so they can time-share one committed pool of capacity rather than fragmenting it stage by stage. Running the flywheel continuously requires capacity that is reserved and continuously monitored. Four Amazon SageMaker HyperPod properties answer those demands in turn:
>
> One cluster for all stages. Because Amazon SageMaker HyperPod orchestrates the cluster with EKS, the three engines of the loop run as ordinary Kubernetes workloads on a single shared GPU pool. Generation runs on the vLLM-Omni server, post-training on cosmos-framework under torchrun (Fully Sharded Data Parallel (FSDP2) plus Ulysses context parallelism), and evaluation on a single-GPU policy server. They also share one storage layer. An Amazon FSx for Lustre file system, accessed over Elastic Fabric Adapter (EFA), backed by an Amazon S3 bucket through a data repository association (DRA), mounts once and serves all three stages from the same path. Generation writes synthetic clips, post-training reads them, and the policy server loads its checkpoint off the same volume. There are no re-provisioning steps or terabyte-scale data migrations between stages, and Region-locked AV data stays in one in-Region cluster.
>
> Health-checked, auto-recovering capacity. A continuous loop wants capacity that is already provisioned and actively monitored: generation is bursty and dominates GPU-hours, and post-training runs for days across many nodes. Amazon SageMaker HyperPod continuously detects faulty nodes and reboots or replaces them automatically, and you can commit that capacity ahead of time with flexible training plans. Its managed job auto-resume then turns a worker failure into a bounded recovery. The Kubeflow PyTorchJob recreates the pod gang, NCCL re-forms, and cosmos-framework resumes from the latest PyTorch Distributed Checkpoint (DCP). A node failure therefore costs at most one checkpoint interval of redone work plus the node-replacement and reschedule latency, rather than a lost run.
>
> EFA already wired for multi-node NCCL. The long sequences that Cosmos 3 packs together for training (video latents plus text plus action, tens of thousands of tokens each) push the 64B tier into context parallelism on top of FSDP2. Every layer issues cross-node collectives. Standing that up by hand is the usual multi-node time sink: matching the EFA stack, the NCCL plugin, and the exact torch and NCCL versions the cosmos-framework pins. Amazon SageMaker HyperPod ships it pre-configured, and when paired with an AWS Deep Learning Containers (DLC) image, whose torch and aws-ofi-nccl versions match what the framework pins, NCCL over EFA is configured to work out of the box.
>
> Optional: task governance for many embodiments. If the factory serves several robot types or AV variants at once, Amazon SageMaker HyperPod task governance (built on Kueue) carves the pool into namespace-scoped queues with quotas, priorities, and preemptions. Dozens of heterogeneous jobs then share one capacity reservation instead of contending for it ad hoc, which raises goodput by keeping otherwise-idle GPUs busy across projects. A single-embodiment program can skip it, but task governance pays off once many jobs compete for the same pool.
>
> The choice between Amazon SageMaker HyperPod and a lighter option comes down to the unit of work. A one-shot fine-tuning workload does not necessarily need the resilience and persistence of an Amazon SageMaker HyperPod cluster. An ephemeral managed training job (for example, an Amazon SageMaker AI training job) suffices, because a short run rarely hits a node failure. Amazon SageMaker HyperPod is well-suited for the sustained Cosmos 3 flywheel, where generation runs continuously, post-training is multi-node and long-running, evaluation is co-located on the same storage layer, and failures are statistically frequent.
>
> 3. What we are building
>
> The solution post-trains three representative workloads, each a stage of the flywheel, and exercises the generation and evaluation stages end-to-end. All three run end-to-end on p5en.48xlarge (8x NVIDIA H200 GPUs) nodes with real checkpoints. The three are a robot-manipulation policy and two vision-perception fine-tuning workloads.
>
> Workload
>
> Stage
>
> Model
>
> What it exercises
>
> Robot policy (DROID)
>
> Post-train (policy)
>
> Cosmos3-Nano (~16B)
>
> Action-policy post-training on a public LeRobot v3 dataset (droid_policy.toml). The lightest per-step workload
>
> Vision Supervised Fine-Tuning (SFT)
>
> Post-train (perception)
>
> Cosmos3-Nano (~16B)
>
> Video plus caption SFT (vision_sft_nano.toml). Substantially heavier per step than the policy workload
>
> Vision Low-Rank Adaptation (LoRA)
>
> Post-train (perception)
>
> Cosmos3-Super (~64B)
>
> LoRA fine-tuning of the 64B model with context parallelism (vision_sft_super.toml). The heaviest per-step workload
>
> Although AV post-training is not specifically covered here, Cosmos3’s base models were trained on a public synthetic-driving corpus (SDG-DriveSim, the nvidia/PhysicalAI-WorldModel-Synthetic-Autonomous-Driving-Scenarios dataset on Hugging Face). Its per-embodiment action projection is designed to extend to an AV ego-pose action space, so the same recipe and cluster setup covered in this post applies to AV post-training too.
>
> The training stack is NVIDIA’s cosmos-framework, run with no forks or source edits to the framework package, so upstream updates drop in cleanly. It trains with FSDP2 and scales to hybrid sharded data parallelism (HSDP) and context parallelism as sequence length and node count grow. Section 6.2 covers how those parallelism choices are set per tier.
>
> This guide uses p5en.48xlarge as the reference instance type throughout. Rather than publishing a cross-instance ranking, we give you a goodput methodology you can run on your own hardware (Section 7). It is built on per-step time, GPU saturation, and a configurable Model FLOPs Utilization (MFU). With it you can size your chosen platform, including the NVIDIA Blackwell platform (B200, B300, and rack-scale GB200/GB300 NVL72), against your own measurements.
>
> 4. Cluster setup on SageMaker HyperPod EKS
>
> Setting up the cluster breaks down into satisfying the prerequisites, enabling NCCL over EFA, turning on deep health checks and auto-recovery, choosing a base training image, and staging and validating the result.
>
> 4.1 Prerequisites
>
> You can satisfy most of these prerequisites with the Amazon SageMaker HyperPod-EKS Terraform modules. These modules provision the EKS-orchestrated Amazon SageMaker HyperPod cluster, the virtual private cloud (VPC) and EFA-enabled security groups, the Amazon FSx for Lustre file system and CSI driver, the Kubeflow training operator, and the observability add-on. If you prefer, you can also use the Amazon SageMaker AI console to create these resources using AWS CloudFormation. Alternatively, you can bring your own equivalents.
>
> You need the following in place before the first job runs:
>
> Cluster. An Amazon SageMaker HyperPod cluster orchestrated by Amazon EKS, with a GPU instance group of p5en.48xlarge nodes in a single Availability Zone (see Creating an Amazon SageMaker HyperPod cluster with Amazon EKS orchestration). At this scale, GPU capacity is the binding constraint: p5en is rarely available on demand, so plan on a flexible training plan or a capacity reservation to secure the nodes.
>
> Service quota. Because GPU capacity constrains availability, a sufficient service quota for the chosen instance type in the target Region, requested through AWS Service Quotas before you scale up the cluster.
>
> Job submission. kubectl configured against the cluster and the Kubeflow Training Operator installed, so that PyTorchJob custom resources are recognized.
>
> Storage. The FSx for Lustre CSI driver installed and an Amazon FSx for Lustre file system attached in the same VPC and subnet as the GPU nodes. The Terraform modules provision both when you turn on the FSx module, or you can attach an existing file system.
>
> Credentials. A Hugging Face read token with the nvidia/Cosmos-Guardrail1 license accepted on the token’s account, stored as a Kubernetes secret named hf-token, because the generation and policy-serving paths pull this gated guardrail repository at startup.
>
> 4.2 Enabling NCCL over EFA
>
> EFA gives NCCL a kernel-bypass, remote direct memory access (RDMA) capable transport for multi-node collectives, and each p5en.48xlarge node advertises 16 EFA Network Interface Cards (NICs). On Amazon SageMaker HyperPod EKS the EFA drivers (from the Deep Learning AMI) and the EFA device plugin (pre-installed by the HyperPod service) are already in place. The pod spec only requests vpc.amazonaws.com/efa resources alongside the GPUs (see the sample manifests). The training image must carry an aws-ofi-nccl plugin built against the same NCCL version the framework uses, which is exactly why this sample builds on the AWS DLC (Section 4.4).
>
> EFA being present on the hardware is not the same as NCCL actually using it, so verify the transport rather than assume it. The training manifest runs a short diagnostic preamble before training starts, and with NCCL debug logging on, a healthy multi-node run reports EFA with GPUDirect RDMA as the selected transport. A fallback to TCP appears as NET/Socket in the logs, meaning the collectives are running over the wrong transport. To validate the interconnect end-to-end before a real run, run a standard multi-node NCCL test (for example, all_reduce_perf) and confirm the achieved bus bandwidth (see the NCCL tests guide). For the exact diagnostic commands and the full log signature, see the repository README.
>
> 4.3 Deep health checks and auto-recovery
>
> A per-node health-monitoring agent continuously runs basic, passive checks (DCGM policy violations, nvidia-smi errors, GPU-count validation), while deep health checks (DCGM level-4 diagnostics and NCCL/EFA benchmarks) run when nodes join or the cluster is updated. When you turn on automatic node recovery, a fault from any of these sources triggers Amazon SageMaker HyperPod to reboot or replace the faulty instance, and auto-resume restarts the job from the last checkpoint once the replacement is ready.
>
> 4.4 Choosing the base training image
>
> Getting distributed training to run across nodes can consume a surprising amount of setup time, so it is worth treating the base-image choice as a deliberate decision rather than an assumption. The choice hinges on one question: do NCCL collectives ride EFA across nodes, and do the cosmos-framework pinned CUDA wheels load? The framework’s virtual environment (venv) pins torch==2.10.0+cu130 (CUDA 13), and its CUDA wheels (flash-attn, transformer-engine, natten) are published for CPython 3.13 only. These pins drive the base-image choice in two ways: the image’s NCCL must match the torch wheel’s bundled NCCL for EFA to work, and the image must provide a CPython 3.13 environment for the wheels to install at all.
>
> A mismatched base image may block multi-node. A general-purpose GPU PyTorch base image can validate single-node yet fail cross-node NCCL over EFA at initialization (for example, fi_getinfo() No data available) even when EFA itself is fully functional. The root cause is a version-matrix mismatch. The cosmos-framework venv’s torch bundles a specific NCCL (here, 2.28.9), but if the base image’s bundled aws-ofi-nccl plugin was built against a different NCCL, the plugin and the runtime don’t line up. Setting NCCL_NET_PLUGIN=none sidesteps the error, but only by dropping cross-node traffic onto TCP instead of EFA, a non-starter for multi-node performance.
>
> A version-matched AWS Deep Learning Containers image removes this work. The AWS Deep Learning Containers (DLC) for PyTorch ships torch 2.10.0+cu130, an exact match to the cosmos-framework pin. It also bundles an AWS tuned, version-matched EFA stack (EFA 1.47.0, libfabric 2.4, aws-ofi-nccl 1.18.0, GDRCopy 2.5.1). Because the DLC ships the same torch wheel the venv installs, NCCL and the aws-ofi-nccl build in the DLC line up. Multi-node EFA is then configured to work without a plugin rebuild or a version mismatch to work around.
>
> Two further build-time issues surfaced in the DROID video-decode path on the DLC: an FFmpeg version too old for torchcodec, and a missing shared libpython. Both are packaging problems with clean fixes baked into the Dockerfile in the accompanying repository.
>
> In short, pick the base image by cosmos-framework version compatibility and verified NCCL over EFA, not by brand or familiarity. For this framework version, the version-matched AWS DLC can be a lower-effort path.
>
> 4.5 Staging and validation
>
> With the base image chosen and the prerequisite cluster in place, you stage the image and storage and validate the result before running a workload. Each step is backed by code in the accompanying repository, so you run templates rather than hand-assemble resources.
>
> Build and push the training image to Amazon Elastic Container Registry (Amazon ECR), and apply the storage class and the optional Amazon S3 data repository association so datasets and base checkpoints hydrate into /fsx on first access:
>
> ./build-push.sh
>
> envsubst &lt; storage/storage-fsx-efa-sc.yaml | kubectl apply -f -
>
> envsubst &lt; storage/storage-fsx-dra.yaml | kubectl apply -f -
>
> Before submitting a job, you validate that the cluster is ready: confirm that every GPU node shows Ready and the Kubeflow training-operator pod shows Running.
>
> kubectl get nodes
>
> kubectl get pods -n kubeflow
>
> With provisioning and validation done, Section 6.1 walks through preparing data, launching the robot-policy job, monitoring it, and validating its output, and Section 10 covers how to tear the workloads and cluster back down when you’re finished.
>
> 5. Wiring the storage layer
>
> The flywheel moves multi-terabyte datasets between stages, so the storage layer is a first-class design decision rather than an afterthought.
>
> Staging: Hugging Face to S3 to FSx for Lustre. Datasets and base checkpoints stage from Hugging Face into an in-Region Amazon S3 bucket, which is then attached to an FSx for Lustre filesystem through a DRA. FSx for Lustre presents one POSIX namespace at /fsx to each pod, and the DRA lazily loads objects from S3 on first access or preloads them on demand.
>
> Two I/O regimes. The

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。