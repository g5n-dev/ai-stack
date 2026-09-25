---
title: "Scaling MoE reinforcement learning on Amazon EKS with EFA and DeepEP with 40% more throughput"
date: 2026-09-26T06:21:11+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "深度学习", "Amazon Elastic Kubernetes Service", "Technical How-to", "博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:b73d704e7f8962abf5e3f7d852f8fad4a2add019fb94dc2a889548c6ea61ff78"
source_payload_sha256: "sha256:4abe419b23c335e1b8b99604748cfc907c0c4a3f265c53e1bced75a8e60ad393"
observation_id: obs_95f314d9972fcd384b1f5504b60da9ec16098cd7e2786cba33337dfe9c55d3d4
event_id: evt_b588dda905b82a0f33b600ed36ae05ebcf6744d0f340fe5853ff1fd6980c671f
revision_id: rev_ea375e47ea343d67ba5fd4b9178b4d73b36b67c04c8ed8fa30b5e04ced44eaae
source_published_at: 2026-09-25T16:29:50Z
first_seen_at: 2026-09-25T22:19:24.961994Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: true
source_truncation_reason: "crawler_feed_content_limit"
source_support: 1.0
source_title_chars_original: 93
interpretation_sha256: "sha256:f5d84b41d211ee021e44cbead8158fead3cb8b36797e6d1171c9118007d6b9e0"
description: "这是一篇关于在云平台上搭建大规模 MoE 模型强化学习训练架构的技术方案，介绍了如何通过容器编排和高速网络互联来协调推理生成与策略训练两类异构工作负载。"
external_url: https://aws.amazon.com/blogs/machine-learning/scaling-moe-reinforcement-learning-on-amazon-eks-with-efa-and-deepep-with-40-more-throughput
parent_observation_id: null
last_seen_at: 2026-09-25T22:19:24.961994Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/scaling-moe-reinforcement-learning-on-amazon-eks-with-efa-and-deepep-with-40-more-throughput](https://aws.amazon.com/blogs/machine-learning/scaling-moe-reinforcement-learning-on-amazon-eks-with-efa-and-deepep-with-40-more-throughput)
- **发布域名**: aws.amazon.com

## 要点解读

### 这是什么

这是一篇关于在云平台上搭建大规模 MoE 模型强化学习训练架构的技术方案，介绍了如何通过容器编排和高速网络互联来协调推理生成与策略训练两类异构工作负载。

### 用在哪里

适用于需要训练千亿参数以上 MoE 模型、并采用 RLHF 或 GRPO 等强化学习方法的团队。当训练规模扩展到多节点、需要在分布式推理与紧耦合训练之间保持平衡时，可以参考此类架构思路。

### 可以推断的

推测：MoE 模型的多专家并行机制会引入动态的跨设备令牌路由，这种细粒度的 all-to-all 通信在扩展到多节点时会显著增加网络压力，相比稠密模型更需要关注节点间带宽。

推测：该方案涉及的工作负载既有注重吞吐量的分布式推理，也有需要同步更新的紧耦合训练，两者资源需求不同，需要统一的调度层来避免硬件空闲或训练不稳定。

## 来源摘要/节选

> When you post-train a Mixture-of-Experts (MoE) model with Reinforcement Learning from Human Feedback (RLHF) or Group Relative Policy Optimization (GRPO) at scale, three simultaneous challenges emerge. The first requires coordinating heterogeneous compute for rollout generation and policy training. Second, sustaining high-throughput communication across hundreds of accelerators. And third, dynamically orchestrating every subsystem to keep them in balance. On AWS, you can address these challenges using Amazon Elastic Kubernetes Service (Amazon EKS), Elastic Fabric Adapter (EFA), and DeepEP.
>
> Mixture-of-Experts (MoE) has become a standard architecture for scaling large language models (LLMs) to hundreds of billions or even trillions of parameters, while maintaining efficient inference through sparsity. However, sparsity doesn’t remove infrastructure complexity in training. As part of the standard training pipeline, these models must undergo pre-training, mid-training, supervised fine-tuning (SFT), and reinforcement learning (RL). Among these stages, large-scale RL training places unusual demands on infrastructure because it combines elastic inference work with tightly coupled model training that requires high-bandwidth communication. Reward models, verifiers, and checkpoint updates add further memory, networking, and orchestration pressure. This type of multi-workload optimization reflects a common infrastructure challenge when you run model training, inference, and evaluation on shared resources without creating bottlenecks or leaving capacity idle.
>
> Compared with dense models, post-training MoE models introduce a new infrastructure challenge: as newer MoE architectures become increasingly sparse to reduce inference costs, training becomes constrained more by communication than by compute. A key source of this communication overhead is Expert Parallelism (EP). EP introduces dynamic all-to-all token routing across devices, in addition to the dense, structured communication patterns of Tensor Parallelism (TP), Data Parallelism (DP), and Pipeline Parallelism (PP). In tightly coupled asynchronous RL workloads, the heterogeneous compute and communication demands of MoE training must be balanced with inference-based generation. Slow training steps stall inference workers, while insufficient inference throughput leaves training accelerators idle. This challenge is common across large-scale reinforcement learning workloads, including RLHF pipelines based on Proximal Policy Optimization (PPO) and newer approaches such as GRPO.
>
> PPO typically uses a critic model to estimate value during policy optimization, while GRPO avoids the need for a separate critic model by using group-based relative rewards. Although their algorithmic and model requirements differ, both impose similar infrastructure demands: large-scale rollout generation, tightly coupled policy training, and high-bandwidth inter-node communication.
>
> In this post, we describe an architecture optimized to accelerate MoE training that combines Amazon Elastic Kubernetes Service (Amazon EKS) and EFA to orchestrate and accelerate large-scale RL training and how DeepEP optimizes expert-parallel communication over EFA.
>
> Challenges of large-scale RL training
>
> Large-scale RL training presents three interrelated challenges:
>
> Balancing the competing resource demands of rollout generation and policy training.
>
> Managing accelerator compute, memory, and network bandwidth simultaneously.
>
> Handling the shift from high-bandwidth intra-node communication to lower-bandwidth inter-node links as jobs scale beyond a single instance.
>
> The rollout-training loop
>
> Large-scale asynchronous RL jobs have two distinct, simultaneous workloads to optimize: rollout generation and policy training. During rollout generation, the system performs large-scale distributed inference focused on maximizing aggregate throughput rather than minimizing time to first token (TTFT) or inter-token latency. In contrast, policy training requires tightly coupled workers that progress in lockstep, much like pre-training or SFT. Any latency spike or straggling worker can stall the entire job or trigger NVIDIA Collective Communications Library (NCCL) timeouts. RL systems must balance these two workloads because any mismatch in their rates can leave hardware idle or introduce training instability.
>
> Figure 1: The asynchronous RL loop, where rollout workers generate experience through distributed inference while policy-training workers consume batches and update model weights
>
> Compute, memory, and bandwidth pressure
>
> RL workloads have heterogeneous compute and communication demands. As a result, any RL system must balance three resource constraints: accelerator compute, memory, and network bandwidth. Policy training is compute-intensive and must keep pace with rollout generation. At the same time, distributed inference must manage KV-cache capacity and token generation. Balancing memory bandwidth and compute is critical for maximum throughput because MoE layers add sparse, dynamic all-to-all communication as tokens are routed across devices. Reward models provide feedback during training, and data movement adds further pressure. All of these subsystems must be balanced jointly to help prevent any one from becoming a bottleneck.
>
> Intra-node versus inter-node communication
>
> As RL training jobs scale beyond a single instance, model partitions and parallelism groups span multiple nodes, shifting communication from the high-bandwidth intra-node NVLink fabric to lower-bandwidth inter-node links. MoE models intensify this shift: unlike the structured patterns of Tensor Parallelism and Pipeline Parallelism, Expert Parallelism dynamically routes tokens across devices through sparse, fine-grained all-to-all communication traffic that becomes increasingly inter-node as the expert parallelism degree grows.
>
> Figure 2: Communication domains in multi-node MoE training, where NVLink carries high-bandwidth intra-node traffic while EFA handles inter-node token routing for Expert Parallelism, Tensor Parallelism, and Data Parallelism
>
> AWS accelerated computing instances such as P5 and P6 use two primary communication domains: an intra-instance NVLink fabric, typically connected through NVSwitch, and inter-instance networking through EFA. EFA provides high-bandwidth communication traffic between instances. On supported configurations, EFA works with NVIDIA GPUDirect RDMA and OS bypass to transfer data directly between GPU memory buffers across instances, reducing CPU and operating-system involvement in the communication path. Optimizing bandwidth utilization in RL workloads requires balancing these two communication domains by determining which operations can run efficiently over EFA and which must remain within the NVLink fabric.
>
> Architecture overview
>
> To scale RL workloads on AWS, we combine Amazon EKS, EFA, and Amazon Simple Storage Service (Amazon S3) so that orchestration, high-performance communication, and durable storage can scale independently. With Amazon EKS, you can manage the lifecycle and placement of heterogeneous workers. With EFA, you get the inter-node data path for communication-intensive GPU workloads. With Amazon S3, you can store datasets, model checkpoints, and completed training artifacts including the model weights. The following sections describe how to map the distinct layers of the RL system, covering orchestration, high-performance networking, and durable storage, and how each layer scales independently.
>
> EKS cluster topology
>
> The Amazon EKS cluster contains separate node groups optimized for each stage of the RL workflow. GPU-accelerated instances run rollout generation, reward-model inference, and policy training, while CPU instances execute environments and preprocessing tasks. Memory-optimized instances host experience buffers and checkpoint caches, allowing producers and consumers to exchange data without placing durable storage directly on the critical path.
>
> Figure 3: EKS cluster topology with GPU node groups for policy training and rollout generation, CPU node groups for environment workers and preprocessing, and memory-optimized instances for experience buffers and checkpoint caches
>
> RL job topology
>
> During rollout, the model generates samples through interactions with CPU-based environment pods, and the resulting experience flows into a memory-optimized buffer. From there, the policy-training step consumes batches, updates model weights, and publishes new checkpoints that feed back into the next round of rollout generation. Checkpoints and completed training artifacts are also persisted to Amazon S3 for durable storage, recovery, and downstream use. Policy training, weight updates, and new checkpoint generation can all run on the EKS cluster.
>
> Figure 4: RL job data flow on EKS, where rollout workers generate experience through CPU environment interactions and write to a shared memory buffer, and policy-training workers consume batches, publish updated checkpoints, and persist artifacts to Amazon S3
>
> Network and execution layers
>
> EKS provides the control plane for scheduling, scaling, failure recovery, and coordination across different worker groups. Within GPU instances, NVLink and NVSwitch carry high-bandwidth intra-node communication. EFA supports latency-sensitive inter-node communication for distributed policy training and other tightly coupled GPU operations. The experience buffer and Amazon S3 form the data layer, separating high-frequency samples and checkpoint exchange from long-term artifact storage.
>
> Performance and cost optimizations
>
> This section covers two key optimizations: using DeepEP to reduce expert-parallel communication overhead over EFA, and using Amazon Elastic Compute Cloud (Amazon EC2) Spot Instances to help lower the cost of rollout generation.
>
> DeepEP over EFA
>
> DeepEP, along with other topology-aware expert-parallel communication techniques, is a common optimization for MoE workloads that aims to reduce communication bottlenecks. Standard all-to-all collectives are most efficient for dense, regular communication, but MoE workloads generate sparse, fine-grained, and imbalanced traffic as tokens are dynamically routed across experts. As Expert Parallelism spans multiple nodes, synchronization and per-message overhead increase, making inter-node communication a dominant bottleneck. DeepEP addresses this by replacing generic all-to-all collectives with specialized dispatch and combining kernels. These kernels use NVLink for intra-node communication and an RDMA-capable backend for inter-node communication.
>
> Amazon has contributed several features to migrate DeepEP’s communication primitives to libfabric. This makes the transport layer portable across libfabric-supported network fabrics and optimizes MoE training over EFA. With these changes, DeepEP v2 gains native EFA support. Additionally, NCCL 2.31 incorporates the latest EFA optimizations for dense collective communication. In the following section, we describe how DeepEP over EFA improves rollout-generation throughput by reducing the communication overhead of expert dispatch and combining operations.
>
> How DeepEP communicates over EFA
>
> DeepEP replaces standard NCCL all-to-all collectives with two specialized GPU kernels: a dispatch kernel that routes tokens from local GPUs to remote experts, and a combine kernel that gathers processed tokens back. For intra-node transfers, these kernels use NVLink through NVSwitch. For inter-node transfers, DeepEP uses libfabric to send data over EFA. On supported instance types such as P5 and P6, EFA works with NVIDIA GPUDirect RDMA to transfer data directly between GPU memory buffers across instances, bypassing the CPU and operating system. The upstream contributions from Amazon migrate DeepEP’s communication primitives from a CUDA-specific RDMA backend to libfabric. This makes the transport portable across EFA-supported configurations and reduces per-message overhead for the sparse, fine-grained traffic patterns that Expert Parallelism generates.
>
> Across 48 P5en instances (16 dedicated to training, 32 to inference) running a super-sparse MoE model, enabling DeepEP over EFA increased aggregate RL rollout throughput by 40 percent. Figure 5 shows the throughput comparison with and without DeepEP.
>
> Figure 5: RL rollout throughput with and without DeepEP over EFA across 48 P5en instances
>
> Spot Instances for rollout generation
>
> Rollout generation is well suited to Amazon EC2 Spot Instances because it consists of distributed inference tasks that can be partitioned across independent workers. Unlike policy training, where tightly coupled workers must progress together, the interruption of a rollout worker does not require the entire RL job to stop. Unfinished rollout tasks can be returned to the queue and reassigned while the remaining workers continue generating experience.
>
> With Amazon EKS, you can scale Spot-based rollout node groups according to rollout demand and queue depth while maintaining stable capacity for policy training. Rollout workers should process bounded units of work and publish completed samples frequently. When a Spot interruption notice arrives, workers drain active requests and return unfinished tasks to the queue. This separation can help reduce rollout-generation costs. Policy-training workers remain insulated from Spot interruptions, delays, or NCCL timeouts.
>
> Putting it all together
>
> This section walks through provisioning the infrastructure described in the previous sections, from cluster creation through running an RL job with DeepEP communication enabled.
>
> Prerequisites
>
> Before running RL on Amazon EKS, verify the following requirements are met:
>
> AWS account with appropriate AWS Identity and Access Management (IAM) permissions.
>
> Amazon EKS 1.31 or later.
>
> EFA installer 1.49 with AWS OFI NCCL plugin.
>
> DeepEP 2.0.0, NCCL 2.31.2, SGLang 0.5.17, PyTorch 2.12.1 (CUDA 13.0).
>
> Supported GPU instances, such as p5.48xlarge, p5e.48xlarge, or p6-b200.48xlarge.
>
> Familiarity with Kubernetes and distributed training concepts.
>
> EKS cluster setup
>
> This architecture can be deployed on Amazon EKS by separating policy training, rollout generation, and supporting services across independently managed node groups. This preserves the isolation between tightly coupled training workloads and more elastic rollout workers while allowing each component to use the capacity model optimized for its execution characteristics.
>
> Managed node groups streamline provisioning, updates, and instance lifecycle management. Policy-training workers can run on stable GPU capacity, while rollout-generation capacity can scale independently and incorporate Spot Instances where interruption tolerance permits. CPU-based services, including orchestration and supporting components, can be placed in separate node groups to avoid competing with GPU workloads for capacity.
>
> The following eksctl ClusterConfig defines a general-purpose CPU node group and a GPU accelerator node group for the cluster:
>
> apiVersion: eksctl.io/v1alpha5
>
> kind: ClusterConfig
>
> metadata:
>
> name: my-eks-cluster
>
> region: us-west-2
>
> version: "1.33"
>
> managedNodeGroups:
>
> # ------------------------------------------------------------
>
> # General-purpose CPU node group
>
> # ------------------------------------------------------------
>
> - name: general-purpose-ng
>
> minSize: 3
>
> desiredCapacity: 3
>
> maxSize: 6
>
> capacityType: ON_DEMAND
>
> privateNetworking: true
>
> launchTemplate:
>
> id: lt-xxxxxxxxxxxxxxxxx
>
> version: "1"
>
> labels:
>
> workload-type: general-purpose
>
> tags:
>
> Name: eks-general-purpose
>
> NodeGroup: general-purpose-ng
>
> Workload: general-purpose
>
> updateConfig:
>
> maxUnavailable: 1
>
> # ------------------------------------------------------------
>
> # GPU / accelerator node group
>
> # ------------------------------------------------------------
>
> - name: accelerator-ng
>
> minSize: 3
>
> desiredCapacity: 3
>
> maxSize: 6
>
> capacityType: ON_DEMAND
>
> privateNetworking: true
>
> launchTemplate:
>
> id: lt-yyyyyyyyyyyyyyyyy
>
> version: "1"
>
> labels:
>
> workload-type: accelerator
>
> accelerator: nvidia-b300
>
> taints:
>
> - key: nvidia.com/gpu
>
> value: "true"
>
> effect: NoSchedule
>
> tags:
>
> Name: eks-accelerator
>
> NodeGroup: accelerator-ng
>
> Workload: accelerator
>
> updateConfig:
>
> maxUnavailable: 1
>
> The listed Ampere, Hopper, and Blackwell instance types (p4d.24xlarge, p4de.24xlarge, p5.48xlarge, p5e.48xlarge, p6-b200.48xlarge, and p6-b300.48xlarge) support large-scale RL training and can be used for either rollout or training workloads.
>
> Figure 6: Representative EKS deployment topology showing GPU node groups (P5/P6) for
>
> training and rollout, Spot-backed capacity for inference workers, and CPU node groups for
>
> orchestration services.
>
> Setting up EFA drivers and plugins
>
> To optimize asynchronous RL on Amazon EKS, communicating nodes must be in the same Availability Zone (AZ) and the EFA Kubernetes device plugin must be set up. With EFA, you get fast and efficient model updates, high-performance model training, and low-latency communication. To apply the EKS EFA device plugin, you can use kubectl to apply it directly to the cluster.
>
> apiVersion: apps/v1
>
> kind: DaemonSet
>
> metadata:
>
> name: aws-efa-k8s-device-plugin
>
> namespace: kube-system
>
> labels:
>
> app: aws-efa-k8s-device-plugin
>
> spec:
>
> selector:
>
> matchLabels:
>
> app: aws-efa-k8s-device-plugin
>
> updateStrategy:
>
> type: RollingUpdate
>
> template:
>
> metadata:
>
> labels:
>
> app: aws-efa-k8s-device-plugin
>
> spec:
>
> # Only install on the accelerator node group
>
> nodeSelector:
>
> eks.amazonaws.com/nodegroup: accelerator-ng
>
> priorityClassName: system-node-critical
>
> hostNetwork: true
>
> automountServiceAccountToken: false
>
> tolerations:
>
> - operator: Exists
>
> containers:
>
> - name: aws-efa-k8s-device-plugin
>
> # Current AWS EFA K8s device plugin
>
> image: 602401143452.dkr.ecr.us-west-2.amazonaws.com/eks/aws-efa-k8s-device-plugin:v0.5.20
>
> securityContext:
>
> privileged: true
>
> allowPrivilegeEscalation: true
>
> runAsUser: 0
>
> runAsNonRoot: false
>
> resources:
>
> requests:
>
> cpu: 10m
>
> memory: 20Mi
>
> volumeMounts:
>
> - name: device-plugin
>
> mountPath: /var/lib/kubelet/device-plugins
>
> - name: infiniband
>
> mountPath: /dev/infiniband
>
> volumes:
>
> - name: device-plugin
>
> hostPath:
>
> path: /var/lib/kubelet/device-plugins
>
> - name: infiniband
>
> hostPath:
>
> path: /dev/infiniband
>
> For additional instructions and performance testing, see the EKS EFA setup instructions.
>
> Launching DeepEP
>
> The reference implementation combines the CUDA, PyTorch, communication, and inference components required to support the optimizations described in the previous sections. The following table lists the benchmark environment:
>
> CUDA: 13.0.
>
> PyTorch: 2.12+cu130.
>
> NCCL: 2.31.
>
> EFA: 1.49.
>
> DeepEP: 2.0.
>
> SGLang: 0.5.17.
>
> Miles: 0.1.0.
>
> Keeping these components aligned is critical. GPU kernels, collective communication libraries, and the underlying EFA transport each contribute to end-to-end performance. Using the 763104351884.dkr.ecr.&lt;region&gt;.amazonaws.com/sglang:0.5.17-gpu-py312-cu130-ubuntu24.04-ec2 image (available in the SGLang Deep Learning Containers catalog) is a practical starting point. The following Dockerfile can be used to set up the training stack.
>
> # syntax=docker/dockerfile:1.7
>
> # Reference base from the AWS Deep Learning Containers SGLang catalog.
>
> # Override AWS_REGION at build time if the image is pulled from another region.
>
> ARG AWS_REGION=us-west-2
>
> ARG SGLANG_DLC_TAG=0.5.17-gpu-py312-cu130-ubuntu24.04-ec2
>
> FROM 763104351884.dkr.ecr.${AWS_REGION}.amazonaws.com/sglang:${SGLANG_DLC_TAG}
>
> ARG BUILD_JOBS=16
>
> ARG NVCC_THREADS=1
>
> # Reference implementation version matrix.
>
> ARG PYTORCH_VERSION=2.12.1
>
> ARG EFA_INSTALLER_VERSION=1.49.0
>
> ARG NCCL_VERSION=2.31.2
>
> ARG NVSHMEM_VERSION=3.7.2
>
> ARG SGLANG_VERSION=0.5.17
>
> ARG DEEPEP_VERSION=2.0.0
>
> ARG DEEPEP_COMMIT=b306af06afd412c88e51e71802951606e40b7358
>
> ARG MILES_VERSION=0.1.0
>
> ARG MILES_REF=v0.1.0
>
> # Existing optimization pins retained from the original Dockerfile.
>
> ARG DEEPGEMM_COMMIT=731e7c7a97d269e4b9f482ea18d0e709a948f293
>
> ENV PIP_RETRIES=20 \
>
> PIP_DEFAULT_TIMEOUT=60 \
>
> LIBFABRIC_HOME=/opt/amazon/efa
>
> RUN apt-get update &amp;&amp; \
>
> apt-get install -y --no-install-recommends \
>
> autoconf automake build-essential ca-certificates cmake curl git \
>
> libtool ninja-build pkg-config patch
>
> # PyTorch 2.12.1 built for CUDA 13.0. This is installed explicitly rather than
>
> # relying on whatever PyTorch minor version happened to ship in the base image.
>
> RUN pip install --no-cache-dir --force-reinstall \
>
> --index-url https://download.pytorch.org/whl/cu130 \
>
> "torch==${PYTORCH_VERSION}"
>
> # Install the EFA 1.49 userspace stack and its NGC-compatible OFI NCCL plugin.
>
> # The EFA kernel module is supplied by the EKS/EC2 host, not by this container.
>
> RUN apt-get remove -y libnccl-ofi &amp;&amp; \
>
> rm -f /etc/ld.so.conf.d/aws-ofi-nccl.conf &amp;&amp; \
>
> curl -fsSL "https://efa-installer.amazonaws.com/aws-efa-installer-${EFA_INSTALLER_VERSION}.tar.gz" -o /tmp/aws-efa-installer.tar.gz &amp;&amp; \
>
> mkdir -p /tmp/aws-efa-installer &amp;&amp; \
>
> tar -xzf /tmp/aws-efa-installer.tar.gz -C /tmp/aws-efa-installer --strip-components=1 &amp;&amp; \
>
> cd /tmp/aws-efa-installer &amp;&amp; \
>
> ./efa_installer.sh -y --skip-kmod --no-verify --build-ngc --skip-mpi
>
> # DeepEP V2 uses NCCL Gin. Keep NCCL on the requested 2.31 line and install it
>
> # before compiling DeepEP so build-time headers and runtime libraries agree.
>
> RUN pip install --no-cache-dir --force-reinstall --no-deps \
>
> "nvidia-nccl-cu13==${NCCL_VERSION}" \
>
> "nvidia-nvshmem-cu13==${NVSHMEM_VERSION}"
>
> ENV DEEPEP_REPO=https://github.com/deepseek-ai/DeepEP.git \
>
> DEEPEP_SRC_DIR=/opt/amazon/DeepEP \
>
> TORCH_CUDA_ARCH_LIST="9.0 10.0 10.3 12.0" \
>
> CUDASTDCXX_INCLUDE=/usr/local/lib/python3.12/dist-packages/flashinfer/data/cccl/libcudacxx/include \
>
> DEEPGEMM_REPO=https://github.com/sgl-project/DeepGEMM.git \
>
> DEEPGEMM_SRC_DIR=/opt/amazon/DeepGEMM \
>
> TVM_FFI_CUDA_ARCH_LIST="9.0 10.0 10.3 12.0" \
>
> DG_FORCE_BUILD=1
>
> ENV CPATH="${CUDASTDCXX_INCLUDE}" \
>
> CPLUS_INCLUDE_PATH="${CUDASTDCXX_INCLUDE}"
>
> # Build DeepEP from the pinned public-release commit.
>
> RUN export MAX_JOBS="${BUILD_JOBS}" CMAKE_BUILD_PARALLEL_LEVEL="${BUILD_JOBS}" &amp;&amp; \
>
> mkdir -p /opt/amazon &amp;&amp; \
>
> rm -rf "${DEEPEP_SRC_DIR}" &amp;&amp; \
>
> git clone --filter=blob:none --no-checkout "${DEEPEP_REPO}" "${DEEPEP_SRC_DIR}" &amp;&amp; \
>
> cd "${DEEPEP_SRC_DIR}" &amp;&amp; \
>
> git fetch --depth 1 --no-tags origin "${DEEPEP_COMMIT}" &amp;&amp; \
>
> git checkout FETCH_HEAD &amp;&amp; \
>
> pip install --no-cache-dir wheel &amp;&amp; \
>
> python setup.py bdist_wheel &amp;&amp; \
>
> pip install --no-cache-dir --force-reinstall --no-deps dist/*.whl
>
> # Keep the existing DeepGEMM optimization layer.
>
> RUN export MAX_JOBS="${BUILD_JOBS}" CMAKE_BUILD_PARALLEL_LEVEL="${BUILD_JOBS}" &amp;&amp; \
>
> mkdir -p /opt/amazon &amp;&amp; \
>
> rm -rf "${DEEPGEMM_SRC_DIR}" &amp;&amp; \
>
> git clone --filter=blob:none --no-checkout "${DEEPGEMM_REPO}" "${DEEPGEMM_SRC_DIR}" &amp;&amp; \
>
> cd "${DEEPGEMM_SRC_DIR}" &amp;&amp; \
>
> git fetch --depth 1 --no-tags origin "${DEEPGEMM_COMMIT}" &amp;&amp; \
>
> git checkout FETCH_HEAD &amp;&amp; \
>
> pip install --no-cache-dir --upgrade "apache-tvm-ffi==0.1.11" &amp;&amp; \
>
> ./build_sgl_deep_gemm.sh &amp;&amp; \
>
> pip install --force-reinstall --no-deps --no-cache-dir dist/sgl_deep_gemm*.whl
>
> # Miles 0.1.0 is installed without dependency resolution so it cannot replace
>
> # the benchmark-critical PyTorch/NCCL/SGLang versions above.
>
> ENV MILES_REPO=https://github.com/radixark/miles.git \
>
> MILES_SRC_DIR=/opt/amazon/miles
>
> RUN rm -rf "${MILES_SRC_DIR}" &amp;&amp; \
>
> git clone --branch "${MILES_REF}" --depth 1 "${MILES_REPO}" "${MILES_SRC_DIR}" &amp;&amp; \
>
> pip install --no-cache-dir --no-deps -e "${MILES_SRC_DIR}"
>
> # Re-assert NCCL after every source/package install, then validate the complete
>
> # reference matrix declared in the documentation paragraph.
>
> RUN pip install --no-cache-dir --force-reinstall --no-deps \
>
> "nvidia-nccl-cu13==${NCCL_VERSION}" \
>
> "nvidia-nvshmem-cu13==${NVSHMEM_VERSION}"
>
> RUN grep -Fx "# EFA installer version: ${EFA_INSTALLER_VERSION}" /opt/amazon/efa_installed_packages &amp;&amp; \
>
> test -f /opt/amazon/efa/lib/libfabric.so.1 &amp;&amp; \
>
> test -f /opt/amazon/ofi-nccl/lib/libnccl-net-ofi.so
>
> Launch a job
>
> With TorchX, you can submit RL workloads to Amazon EKS while keeping application configuration separate from infrastructure configuration. TorchX translates job requirements into Kubernetes resources, including compute requests, storage mounts, and runtime configuration. This separation makes it easier to vary model and training configurations without coupling them to cluster provisioning.
>
> The following command uses TorchX to submit an RL training job to your Amazon EKS cluster. The reference train_rl.py script, available

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。