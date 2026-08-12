---
title: "Tiered KV cache for large LLMs on Amazon SageMaker HyperPod with Curvine"
date: 2026-08-13T01:14:51+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "RAG", "Prompt 工程", "Advanced (300)", "Amazon SageMaker HyperPod", "博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:79d20bad6682f5c162fbf7da0127a60c409066276770ac2ecc36b86d610d198b"
source_payload_sha256: "sha256:bcf60579064d1b9040a178dce3a1bd22363cf0eb4f38e8cd47390019dcdd35ab"
observation_id: obs_c2ed76bfcf51bfba74a867f5c453c4e233f7f3c0b5425ebf063cced04764f8e0
event_id: evt_7ed0fa389c9d159e85fbee24daa438255588a564d4aaf701ca4e936aa3284e3e
revision_id: rev_63c923999a1fcf68846476c7f42138db805b42266d9ae85d54bc40253705cd1c
source_published_at: 2026-08-12T13:42:48Z
first_seen_at: 2026-08-12T17:12:07.978922Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: true
source_truncation_reason: "crawler_feed_content_limit"
source_support: 1.0
source_title_chars_original: 72
interpretation_sha256: "sha256:596004b1ec550d6b7654240d895c9d3fb504dad6d49655fdf9a91fdfcfb922e2"
description: "该方案在 SageMaker HyperPod 集群上构建三层 KV 缓存架构，将缓存从 GPU HBM 向外延伸至 CPU 内存，再扩展到跨节点的分布式 NVMe 存储池，并通过感知式路由将请求导向持有相关缓存块的副本。"
external_url: https://aws.amazon.com/blogs/machine-learning/tiered-kv-cache-for-large-llms-on-amazon-sagemaker-hyperpod-with-curvine
parent_observation_id: null
last_seen_at: 2026-08-12T17:12:07.978922Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/tiered-kv-cache-for-large-llms-on-amazon-sagemaker-hyperpod-with-curvine](https://aws.amazon.com/blogs/machine-learning/tiered-kv-cache-for-large-llms-on-amazon-sagemaker-hyperpod-with-curvine)
- **发布域名**: aws.amazon.com

## 要点解读

### 这是什么
该方案在 SageMaker HyperPod 集群上构建三层 KV 缓存架构，将缓存从 GPU HBM 向外延伸至 CPU 内存，再扩展到跨节点的分布式 NVMe 存储池，并通过感知式路由将请求导向持有相关缓存块的副本。

### 用在哪里
适用于在多个业务线端点、RAG 流程或多轮对话场景中部署多种开源基础模型的团队，也适合面临推理成本高、首 token 延迟不稳定的运维人员。

### 可以推断的
推测：该方案通过增加共享的 L2 缓存层，可以在不大幅增加实例规格的前提下提升缓存命中率，从而降低对高端 GPU 实例的依赖。
推测：三层缓存中 L0 仍驻留在 GPU 本地以保证最低延迟，CPU 层承担溢出暂存，NVMe 层负责跨副本共享，这种分层设计平衡了访问速度与容量扩展需求。

## 来源摘要/节选

> Running large language model (LLM) inference at scale typically forces a KV cache trade-off: you either pay for oversized GPU instances to accommodate a growing KV cache, or you accept slow time-to-first-token (TTFT) as identical prompts get recomputed on every request. For teams deploying a broad catalog of publicly available foundation models (FMs), such as Qwen, Llama, DeepSeek, and others, across per-business-line endpoints, Retrieval Augmented Generation (RAG) pipelines, or multi-turn dialogue applications, this trade-off translates directly into higher infrastructure cost and degraded user experience.
>
> The root cause is straightforward. During generation, vLLM stores the attention keys and values for every token it has already processed in a KV cache, so it doesn’t recompute them on each step. Prefix caching extends this by reusing that cache across requests that share the same leading tokens (like a common system prompt). On cost-efficient instances like ml.g6e.4xlarge (48 GB per GPU), once model weights and runtime allocations are accounted for, the memory left for prefix caching is limited, and it tightens further with larger models or higher concurrency. Cache hit rates drop on long prompts, identical system prompts get re-prefilled on every request, and horizontally scaled vLLM replicas each maintain isolated caches. Routing to a different replica is functionally a cold start.
>
> In this post, we build a tiered KV cache architecture on Amazon SageMaker HyperPod that extends the cache hierarchy beyond GPU and CPU memory into a shared, distributed NVMe pool. It builds on two HyperPod capabilities, Managed Tiered KV Cache and Intelligent Routing, and adds Curvine, a lightweight distributed cache filesystem, as the shared L2 tier (GPU to CPU to shared NVMe). With this setup, you can reuse KV cache across replicas at near-local-disk speeds.
>
> We walk through the end-to-end implementation, from enabling HyperPod Tiered Storage to deploying Curvine workers on node-local NVMe to patching the Inference Operator for filesystem-backed L2. On a test deployment, this achieved up to a 100 percent cross-Pod cache hit rate, up to a 2.7x TTFT improvement, and cross-node L2 read latency of about 56 ms for a approximately 1,900-token prompt. See the Benchmarking section for the full methodology and results. With this architecture, workloads that previously required P5 instances can run on lower-cost G6e instances, reducing per-endpoint cost. Actual savings depend on model size and traffic profile.
>
> Solution design
>
> The central idea is to extend the KV cache beyond what fits on a single Pod. Rather than accepting that each vLLM replica lives in isolation, which is its own GPU blocks, its own CPU spill area, no sharing, we build a three-tier hierarchy: L0 (GPU HBM), L1 (local CPU/host memory), and L2 (Curvine, a shared cross-node cache), and overlay it with cache-aware request routing.
>
> L0 – GPU prefix cache. This is vLLM’s native paged-attention layer, holding the hottest KV blocks at the lowest access latency, but its capacity is only whatever GPU memory is left after the model weights. On a 48 GB GPU, a 7B model in bf16 uses around 14 GB for weights, leaving over 30 GB for KV blocks, which is plenty of headroom, so L0 pressure is minimal. A 32B model uses around 64 GB of weights and doesn’t even fit on one 48 GB GPU. Even after sharding, far less memory remains for KV, so the cache fills quickly and evicts under concurrency. That shrinking headroom is exactly why extending the cache off-GPU matters as you scale up model size and traffic.
>
> L1 – CPU memory offload. When GPU blocks are evicted, LMCache catches them in host DRAM before they’re lost. This runs inside each inference Pod and is managed automatically by the SageMaker HyperPod Inference Operator when you set enableL1Cache: true in the InferenceEndpointConfig CRD. Think of it as a safety net. It’s fast, Pod-local, and sized by InstanceMemoryAllocationPercentage (we recommend starting at 20 percent).
>
> L2 – Shared distributed NVMe pool. This is where cross-replica reuse happens. Curvine, a lightweight distributed cache filesystem, pools the local NVMe drives that ship with G6e/P5 instances into a single namespace, which a FUSE client (a user-space driver that presents the pool as an ordinary mounted directory) mounts as a ReadWriteMany PVC (PersistentVolumeClaim) into every inference Pod. LMCache reads and writes through its fs:// connector, so the distributed pool looks like a local directory. Because every Pod mounts the same namespace, a KV block written by one replica is immediately readable by others.
>
> Curvine itself is straightforward to operate: a Primary Node (called the “Master” in Curvine’s documentation) handles metadata and journaling, persisted on Amazon Elastic Block Store (Amazon EBS) for durability, while Worker components run on each GPU node and store data on the node’s NVMe (typically mounted at /opt/dlami/nvme/curvine-data). If a Worker dies, the cache it held is recomputed, no data-loss concern, since these are reproducible KV blocks.
>
> Intelligent routing – getting requests to the right replica. A three-tier cache only delivers its full benefit if requests land on replicas that already hold relevant KV blocks. The HyperPod Inference Operator includes a built-in router that supports three strategies:
>
> Strategy
>
> Best for
>
> prefix-aware (default)
>
> Multi-turn dialogue, shared system prompts
>
> kv-aware
>
> Long document processing, extended sessions
>
> round-robin
>
> Stateless batch inference, load testing
>
> The router maintains a prefix tree (prefix-aware) or queries each worker’s cache state (kv-aware) to select the replica most likely to produce a cache hit. This happens transparently, no client-side changes are needed.
>
> How these pieces fit together. The Inference Operator is installed as an Amazon Elastic Kubernetes Service (Amazon EKS) add-on and manages the full lifecycle. It spins up vLLM Pods with LMCache sidecars, configures L1 and L2 backends, deploys the router, and exposes a single load-balanced endpoint. You declare the cache topology you want in the InferenceEndpointConfig CRD (enableL1Cache, enableL2Cache, l2CacheBackend, routingStrategy), and the Operator renders the correct environment variables, volume mounts, and routing rules. The one caveat today: the CRD’s l2CacheBackend field only accepts redis or tieredstorage natively. To point L2 at a Curvine FUSE mount, we patch the LMCACHE_REMOTE_URL environment variable in the vLLM container spec to fs://localhost:0/mnt/curvine/l2cache/. We walk through this patch in Stage 4 of the implementation.
>
> The net effect is a request arrives at the router, gets dispatched to the replica with the best prefix match, that replica checks GPU blocks (L0), then CPU (L1), then the shared NVMe pool (L2). Only on a complete miss does it re-prefill from scratch. For workloads with moderate-to-high prompt overlap (roughly over 40 percent shared leading tokens, for example a common system prompt or shared RAG context), skipping that re-prefill substantially reduces TTFT.
>
> Figure 1 shows the full data path. Each vLLM Pod stacks an L0 GPU prefix cache and an L1 CPU offload. Below them, all Pods share the L2 tier on a Curvine distributed filesystem pooled from node-local NVMe and mounted ReadWriteMany over FUSE, while the Curvine metadata node persists to Amazon EBS. The HyperPod Intelligent Router sits in front, directing each request to the replica most likely to already hold the relevant cache.
>
> Figure 1: Tiered KV cache architecture
>
> Curvine is a high-performance distributed cache file system that sits between applications and underlying storage such as Amazon Simple Storage Service (Amazon S3), HDFS, or NAS. Clients reach it through the CLI, SDK, FUSE, or CSI. Primary Nodes handle metadata, and Workers serve data with local disk cache for low-latency I/O. Figure 2 shows the Curvine architecture and its key components.
>
> Figure 2: Curvine architecture
>
> How Curvine works (cluster view):
>
> Clients send metadata RPC to Masters and data I/O to Workers.
>
> Masters coordinate Workers using heartbeats and place blocks for load balance and HA.
>
> Workers read/write local tiers and promote/demote data by heat.
>
> On miss or policy-driven persistence, Curvine loads from / dumps to UFS, so durability stays on the underlying store while Curvine accelerates access.
>
> Prerequisites
>
> Amazon SageMaker HyperPod Tiered Storage is a cluster-level capability that provisions a node-local cache tier for inference workloads. After Tiered Storage is active, SageMaker HyperPod deploys the ai-toolkit DaemonSet on every GPU node, reserves a configurable share of host memory (InstanceMemoryAllocationPercentage) for the L1 CPU offload, and exposes the local NVMe instance store under /opt/dlami/nvme so that Curvine Workers can pool it into a shared L2 namespace. The Inference Operator consumes these tiers automatically when enableL1Cache and enableL2Cache are set on the InferenceEndpointConfig CRD.
>
> This walkthrough assumes a SageMaker HyperPod cluster orchestrated by Amazon EKS. To create one, follow Orchestrating SageMaker HyperPod clusters with Amazon EKS in the SageMaker documentation, or with AWS CloudFormation, using the reference templates on the AWSome Distributed AI repository. Provision at least two GPU nodes. A single node can’t demonstrate cross-node reuse. Throughout this post we use the cluster name hyperpod-cluster-eks and the US West (Oregon) AWS Region (us-west-2) as examples, replace them with your own cluster name and Region to reproduce this solution in your account.
>
> Verify the following are in place:
>
> GPU capacity with local NVMe: A SageMaker HyperPod EKS cluster with at least one GPU instance group. G6e or P5 is recommended for their local NVMe, which Curvine pools into L2.
>
> CLI tooling: On your workstation: AWS Command Line Interface (AWS CLI) v2 (with permissions for sagemaker:UpdateCluster and eks:CreateAddon), kubectl configured against the cluster with aws eks update-kubeconfig, and Helm v3.
>
> AWS Identity and Access Management (IAM) for EBS attach: Grant the EBS CSI driver role sagemaker:AttachClusterNodeVolume, sagemaker:DetachClusterNodeVolume, and eks:Describe* so the Curvine metadata node can attach its EBS volume. Keep the Amazon Virtual Private Cloud (Amazon VPC) CNI and EBS CSI add-ons current.
>
> Model weights: this post pulls Qwen2-7B from HuggingFace, so no bucket is required. To stage weights yourself, use an Amazon S3 bucket with the SageMaker HyperPod execution role granted read access. TLS certificates are generated automatically.
>
> Tiered Storage is enabled in Stage 1. The Inference Operator, Amazon S3 and Amazon FSx CSI drivers, Metrics Server, and Cert Manager are installed in Stage 2 (or through console Quick Install), the EBS CSI driver and Curvine in Stage 3.
>
> Step-by-step implementation
>
> The following procedure uses this implementation as a worked example, organized into five stages. Cluster names and Regions shown are placeholders, substitute your own.
>
> Stage 1: Enable HyperPod Tiered Storage
>
> Tiered Storage is a cluster-level toggle. Once Tiered Storage is active, HyperPod automatically deploys the ai-toolkit DaemonSet to every node.
>
> # Enable on an existing cluster via update-cluster (recommended)
>
> aws sagemaker update-cluster \
>
> --cluster-name hyperpod-cluster-eks \
>
> --tiered-storage-config Mode=Enable,InstanceMemoryAllocationPercentage=20 \
>
> --node-recovery Automatic
>
> API note. Calling update-cluster with --tiered-storage-config alone returns ValidationException. At least one of --node-recovery or --instance-groups must also be supplied. The approach is to read the current NodeRecovery value by running describe-cluster and pass it back unchanged. This has no side effect on the cluster configuration.
>
> InstanceMemoryAllocationPercentage accepts 20–100. Begin at 20 and increase as needed based on observed throughput and hit rate. Verify with the following commands:
>
> aws sagemaker describe-cluster --cluster-name hyperpod-cluster-eks \
>
> --query 'TieredStorageConfig'
>
> # Expected: {"Mode": "Enable", "InstanceMemoryAllocationPercentage": 20}
>
> kubectl get ds -n aws-hyperpod ai-toolkit
>
> # Expected:
>
> # NAME DESIRED CURRENT READY UP-TO-DATE AVAILABLE NODE SELECTOR AGE
>
> # ai-toolkit 2 2 2 2 2 &lt;none&gt; 45s
>
> Stage 2: Install the Inference Operator and dependencies
>
> The most convenient approach is Quick Install in the SageMaker console, which provisions the IAM role and installs S3 CSI, FSx CSI, Metrics Server, Cert Manager, and the Inference Operator in one action. The CLI alternative:
>
> EKS_CLUSTER_NAME=$(aws sagemaker describe-cluster --cluster-name hyperpod-cluster-eks \
>
> --query 'Orchestrator.Eks.ClusterArn' --output text | cut -d'/' -f2)
>
> for addon in aws-mountpoint-s3-csi-driver aws-fsx-csi-driver metrics-server cert-manager; do
>
> aws eks create-addon --cluster-name $EKS_CLUSTER_NAME --addon-name $addon --region us-west-2
>
> done
>
> aws eks create-addon \
>
> --cluster-name $EKS_CLUSTER_NAME \
>
> --addon-name amazon-sagemaker-hyperpod-inference \
>
> --configuration-values file://addon-config.json \
>
> --region us-west-2
>
> Stage 3: Deploy the Curvine distributed cache
>
> Several prerequisites must be in place before deploying Curvine. Upgrade the VPC CNI plugin and the EBS CSI driver to a current version, with IRSA preferred over Pod Identity to avoid additional IP consumption on nodes. Grant the aws-ebs-csi-dri-role the EBS-attach permissions listed in Prerequisites (without them, EBS attach on SageMaker HyperPod nodes returns ValidationException). Finally, verify an EBS StorageClass (for example ebs-sc) is available in the cluster. Check the actual name with kubectl get sc. On SageMaker HyperPod EKS clusters the default EBS StorageClass is often gp3. Use that name for master.storage.meta.storageClass and master.storage.journal.storageClass in the Helm install that follows, or create an ebs-sc StorageClass first:
>
> apiVersion: storage.k8s.io/v1
>
> kind: StorageClass
>
> metadata:
>
> name: ebs-sc
>
> provisioner: ebs.csi.aws.com
>
> volumeBindingMode: WaitForFirstConsumer
>
> reclaimPolicy: Delete
>
> Install the Curvine CSI
>
> helm repo add curvine https://curvineio.github.io/helm-charts
>
> helm repo update
>
> helm install curvine-csi curvine/curvine-csi \
>
> -n curvine --create-namespace \
>
> --version 0.3.2-alpha \
>
> --set controller.sidecars.provisioner.image=registry.k8s.io/sig-storage/csi-provisioner:v3.6.0 \
>
> --set node.sidecars.nodeDriverRegistrar.image=registry.k8s.io/sig-storage/csi-node-driver-registrar:v2.10.0 \
>
> --set controller.container.securityContext.privileged=true \
>
> --set node.container.securityContext.privileged=true
>
> kubectl get csidrivers | grep curvine # confirm driver registered
>
> The CSI install doesn’t create a StorageClass automatically. One must be created manually:
>
> kubectl apply -f - &lt;&lt;'EOF'
>
> apiVersion: storage.k8s.io/v1
>
> kind: StorageClass
>
> metadata:
>
> name: curvine-sc
>
> provisioner: curvine
>
> reclaimPolicy: Delete
>
> volumeBindingMode: Immediate
>
> allowVolumeExpansion: true
>
> parameters:
>
> master-addrs: "curvine-master-0.curvine-master.curvine.svc.cluster.local:8995"
>
> fs-path: "/l2cache"
>
> path-type: "DirectoryOrCreate"
>
> EOF
>
> kubectl get sc curvine-sc # confirm curvine-sc created
>
> Curvine CSI 0.3.x and later requires three StorageClass parameters: master-addrs (the Curvine master RPC endpoint, which must match the service DNS created by the Helm install, and comma-separate multiple addresses if the master component has replicas), fs-path (the mount-path prefix inside the Curvine filesystem), and path-type (DirectoryOrCreate lets the CSI create the directory automatically). Without them, PVC provisioning fails with Parameter 'master-addrs' is required.
>
> Install the Curvine server (Primary + Worker components)
>
> For KV cache workloads, node-local NVMe with hostPath is the recommended Worker data backend: G6e/P5 instances ship with NVMe (approximately 3 GB/s), which delivers far higher performance than EBS gp3, incurs no additional cost, and is acceptable for caches where loss is recoverable.
>
> # Step 1: first-time install (bootstrap). Format flags initialise the
>
> # metadata / journal / data directories. Required on 0.3.x, otherwise the
>
> # master pod fails with "RocksDB directories not found".
>
> helm install curvine curvine/curvine -n curvine --create-namespace \
>
> --version 0.3.2-alpha \
>
> --set image.pullPolicy=Always \
>
> --set cluster.formatMaster=true \
>
> --set cluster.formatWorker=true \
>
> --set cluster.formatJournal=true \
>
> --set master.replicas=1 \
>
> --set worker.replicas=2 \
>
> --set "master.nodeSelector.sagemaker\.amazonaws\.com/compute-type=hyperpod" \
>
> --set "worker.nodeSelector.sagemaker\.amazonaws\.com/compute-type=hyperpod" \
>
> --set master.storage.meta.storageClass=ebs-sc \
>
> --set master.storage.journal.storageClass=ebs-sc \
>
> --set "worker.storage.dataDirs[0].name=data1" \
>
> --set "worker.storage.dataDirs[0].type=SSD" \
>
> --set "worker.storage.dataDirs[0].enabled=true" \
>
> --set "worker.storage.dataDirs[0].size=100Gi" \
>
> --set "worker.storage.dataDirs[0].storageClass=" \
>
> --set "worker.storage.dataDirs[0].hostPath=/opt/dlami/nvme/curvine-data" \
>
> --set "worker.storage.dataDirs[0].mountPath=/data/data1"
>
> # Step 2: once all pods are Running, IMMEDIATELY disable the format flags
>
> # so a future pod restart cannot re-format and wipe existing cache/metadata:
>
> helm upgrade curvine curvine/curvine -n curvine \
>
> --version 0.3.2-alpha --reuse-values \
>
> --set cluster.formatMaster=false \
>
> --set cluster.formatWorker=false \
>
> --set cluster.formatJournal=false
>
> kubectl get pods -n curvine # confirm pods stay Running / come back cleanly
>
> Constraints. Master meta and journal must use durable EBS storage. Loss of metadata or WAL upon node rebuild isn’t acceptable. When the Worker dataDirs[0].storageClass is empty and hostPath is set, the Helm chart enables hostPath mode. The two are mutually exclusive and exactly one must be chosen.
>
> Create a ReadWriteMany (RWX) PVC for inference Pods
>
> kubectl apply -f - &lt;&lt;'EOF'
>
> apiVersion: v1
>
> kind: PersistentVolumeClaim
>
> metadata:
>
> name: curvine-pvc
>
> namespace: default
>
> spec:
>
> accessModes:
>
> - ReadWriteMany
>
> storageClassName: curvine-sc
>
> resources:
>
> requests:
>
> storage: 100Gi
>
> EOF
>
> kubectl get pvc curvine-pvc # WAIT for Bound before proceeding
>
> Stage 4: Deploy a vLLM endpoint with tiered KV cache
>
> With Tiered Storage enabled, the operator installed, and Curvine running, the final stage deploys the inference endpoint and points its L2 cache at Curvine. This involves three steps: declaring the endpoint with an InferenceEndpointConfig CRD, patching the rendered Deployment to mount the Curvine PVC, and overriding the operator-injected cache URL so L2 reads and writes go to Curvine.
>
> Deploy using the Inference Operator
>
> Apply the InferenceEndpointConfig CRD below (deploy-qwen-kvcache.yaml). The SageMaker HyperPod Inference Operator reconciles it into a Deployment, vLLM Pods (each with an LMCache sidecar), the intelligent router, and a single load-balanced endpoint. Three points differ from a stock deployment:
>
> Model source is huggingface: the Operator’s built-in init container downloads the weights to /opt/ml/model at Pod startup, so no S3 staging is needed. (Set modelSourceType: s3 with an s3Storage block if you prefer to stage weights yourself.)
>
> LMCACHE_REMOTE_URL is intentionally NOT listed in the CRD. When enableL2Cache: true, the Operator injects its own value. Declaring it here as well produces a duplicate env entry that you would then need to find and remove by index. Leave it out and override the injected value with the patch in the next section.
>
> tlsConfig is omitted: it’s not a required field, and the Operator auto-generates the endpoint certificate into its default output bucket.
>
> # deploy-qwen-kvcache.yaml
>
> apiVersion: inference.sagemaker.aws.amazon.com/v1
>
> kind: InferenceEndpointConfig
>
> metadata:
>
> name: qwen2-7b-instruct-kvcache
>
> namespace: default
>
> spec:
>
> modelName: qwen2-7b-instruct
>
> instanceType: ml.g6e.4xlarge
>
> invocationEndpoint: v1/chat/completions
>
> replicas: 2
>
> modelSourceConfig:
>
> modelSourceType: huggingface # Operator downloads weights to /opt/ml/model
>
> prefetchEnabled: true
>
> huggingFaceModel:
>
> modelId: Qwen/Qwen2-7B-Instruct # public model; add tokenSecretRef for gated models
>
> kvCacheSpec:
>
> enableL1Cache: true
>
> enableL2Cache: true
>
> l2CacheSpec:
>
> l2CacheBackend: "tieredstorage" # placeholder to pass CRD validation; overridden by the Stage 4 patch
>
> intelligentRoutingSpec:
>
> enabled: true
>
> routingStrategy: prefixaware
>
> # tlsConfig is intentionally omitted: the Operator auto-generates the
>
> # endpoint certificate into its default output bucket.
>
> metrics:
>
> enabled: true
>
> modelMetrics:
>
> port: 8000
>
> loadBalancer:
>
> healthCheckPath: /health
>
> worker:
>
> image: public.ecr.aws/deep-learning-containers/vllm:0.11.1-gpu-py312-cu129-ubuntu22.04-ec2-v1.0
>
> args:
>
> - "--model"
>
> - "/opt/ml/model"
>
> - "--max-model-len"
>
> - "16384"
>
> - "--tensor-parallel-size"
>
> - "1"
>
> resources:
>
> limits:
>
> nvidia.com/gpu: "1"
>
> requests:
>
> cpu: "8"
>
> memory: 32Gi
>
> nvidia.com/gpu: "1"
>
> modelInvocationPort:
>
> containerPort: 8000
>
> name: http
>
> modelVolumeMount:
>
> name: model-weights
>
> mountPath: /opt/ml/model
>
> environmentVariables:
>
> # Do NOT add LMCACHE_REMOTE_URL here: when enableL2Cache is true the
>
> # Operator injects its own value; declaring it here creates a duplicate
>
> # env entry. It is replaced with the Curvine fs:// URL by the Stage 4
>
> # patch after the Deployment is rendered.
>
> - name: LMCACHE_REMOTE_SERDE
>
> value: "naive" # cachegen serde has a zip bug under the fs connector
>
> - name: PYTHONHASHSEED
>
> value: "0" # required: identical cache keys across Pods
>
> Two of those environment variables deserve explanation, because both look arbitrary and neither is:
>
> LMCACHE_REMOTE_SERDE=naive – the cachegen serializer has a zip-serialization bug under LMCache’s filesystem connector. The naive serializer is the stable choice.
>
> PYTHONHASHSEED=0 – LMCache derives cache keys from Python hashes. Without a pinned seed, each Pod computes different keys for the same prompt and cross-Pod sharing silently doesn’t hit.
>
> Apply it and wait for both Pods to become Ready (each Pod runs three containers: vLLM, reverse-proxy, otel-collector):
>
> kubectl apply -f deploy-qwen-kvcache.yaml
>
> kubectl get pods -l app=qwen2-7b-instruct-kvcache -w # WAIT: 2 Pods, 3/3 Running
>
> Patch the Deployment to mount the Curvine PVC
>
> The Operator-rendered Deployment needs two adjustments that the CRD cannot express: mounting the Curvine PVC into the vLLM container, and repointing L2 at the FUSE mount. When enableL2Cache: true, the Operator injects LMCACHE_REMOTE_URL=sagemaker-hyperpod://$(NODE_IP):9200 (its node-local backend), and because l2CacheBackend accepts only redis or tieredstorage, there’s no CRD field to point L2 at a Curvine path. So we patch the rendered Deployment directly.
>
> There is a complication: the Operator runs a reconcile loop, and patches applied to a live Deployment are overwritten the next time it re-renders. The reliable sequence is therefore: pause the Operator, scale the Deployment to zero, apply every patch in a single command, scale back up, and restore the Operator only after the Pods are Ready. Scaling to zero also sidesteps a rolling-update deadlock: with replicas equal to available GPUs (two replicas, two single-GPU nodes), the default maxSurge tries to start a new Pod before freeing an old one, and the new Pod sticks in Pending forever waiting for a GPU that never frees.
>
> Start by pausing the Operator and draining the Deployment:
>
> DEPLOY_NAME="qwen2-7b-instruct-kvcache"
>
> # 1. Pause the Operator so its reconcile loop cannot overwrite the patch
>
> kubectl scale deployment hyperpod-inference-controller-manager \
>
> -n hyperpod-inference-system --replicas=0
>
> # 2. Scale the model Deployment to 0 (frees the GPUs; avoids the maxSurge deadlock)
>
> kubectl scale deployment $DEPLOY_NAME --replicas=0
>
> Next, find where the Operator placed LMCACHE_REMOTE_URL in the container’s env array. Don’t hardcode the index, it varies between Operator versions:
>
> # 3. List env vars with their indices; note the index of LMCACHE_REMOTE_URL
>
> kubectl get deployment $DEPLOY_NAME \
>
> -o jsonpath='{.spec.template.spec.containers[0].env}' | \
>
> python3 -c "import json,sys; [print(f'{i}: {e[\"name\"]}') for i,e in enumerate(json.load(sys.stdin))]"
>
> Now, apply all three patches in one command, the URL replacement, the Curvine volume, and its mount. Replace N with the index you found in the previous step:
>
> # 4. Apply ALL patches in one shot
>
> kubectl

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。