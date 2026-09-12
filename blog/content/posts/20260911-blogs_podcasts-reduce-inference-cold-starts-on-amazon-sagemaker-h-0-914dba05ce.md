---
title: "Reduce inference cold starts on Amazon SageMaker HyperPod with model caching"
date: 2026-09-11T05:41:26+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "生成式 AI", "机器学习", "Amazon SageMaker HyperPod", "Announcements", "Expert (400)", "博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:5d08e93dcfd8e97a6cfece0d58c1783b4ad6128f07a411c98adf0c4a1f8d3c5d"
source_payload_sha256: "sha256:7194a013bd05a7351ac0bf6e0be183a474f3443193a6dc5262bda6874007aae4"
observation_id: obs_914dba05ced926e890fec0e4d1b835891a0fe2ac1f00716b81bb7d94aacc2f82
event_id: evt_5b222a8b4576a6bbf1c9760050496190df044861174d50a94fe037060db10314
revision_id: rev_6b7b313eb05776013a88615a71052a1349127aed3cbbc4fec27a4ca5832f9bdd
source_published_at: 2026-09-10T21:37:49Z
first_seen_at: 2026-09-10T21:50:02Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 76
description: "当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。"
external_url: https://aws.amazon.com/blogs/machine-learning/reduce-inference-cold-starts-on-amazon-sagemaker-hyperpod-with-model-caching
parent_observation_id: null
last_seen_at: 2026-09-12T00:00:00Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/reduce-inference-cold-starts-on-amazon-sagemaker-hyperpod-with-model-caching](https://aws.amazon.com/blogs/machine-learning/reduce-inference-cold-starts-on-amazon-sagemaker-hyperpod-with-model-caching)
- **发布域名**: aws.amazon.com

## 来源摘要/节选

> When you deploy a large language model (LLM) for inference on Amazon SageMaker HyperPod, there’s a gap between when you request a pod and when it’s ready to serve traffic. This gap is dominated by two sequential downloads: the inference server container image from Amazon Elastic Container Registry (Amazon ECR), and the model weights from your storage source, which can be Amazon Simple Storage Service (Amazon S3), Amazon FSx for Lustre, or HuggingFace Hub. For smaller models, this might be a few minutes. For large models, like DeepSeek-R1 at 600+ GB, you’re looking at 30 minutes or more before a single request can be served. Every scale-out event goes through the same download cycle, which means your autoscaling response time is gated by network throughput to your storage backend.
>
> Today we’re launching model caching for Amazon SageMaker Inference on HyperPod. Model caching pre-loads model weights and container images onto cluster nodes before pods need them. When you start your pod, it can read from local NVMe storage at approximately 7 GB/s instead of downloading over the network. After you enable model caching, your pods can typically start serving traffic in seconds rather than tens of minutes. In this post, we walk through the cold start problem, explain how model caching works, show you how to enable it, and share benchmark results.
>
> The cold start problem in detail
>
> To understand why model caching matters, consider what happens when an inference pod starts without it. The Kubernetes scheduler places the pod on a node. Kubelet begins pulling the container image from ECR. For inference server images like vLLM or LMI, these are multi-gigabyte images that take 5–7 minutes to pull. They bundle GPU drivers, CUDA libraries, and the serving framework. After the image is available, the container starts and the inference server begins downloading model weights from the configured source. For a 145 GB model on Amazon S3, this can take another 20+ minutes depending on network conditions and available bandwidth. For a 600+ GB model like DeepSeek-R1, this takes upwards of 30 minutes.
>
> During scale-out the same sequence repeats for every new pod. If traffic spikes and your HorizontalPodAutoscaler requests five new pods, all five go through this download sequence independently. The autoscaling policy may react in seconds. However, the actual time to serve additional traffic is 25–30+ minutes, because each new pod waits on downloads before it can take requests.
>
> How model caching works
>
> Model caching eliminates both of these latency sources by pre-loading data onto nodes before pods are scheduled. It introduces two independent capabilities that you can enable together or separately.
>
> Weights cache
>
> The weights cache downloads model weights to local NVMe storage on each node ahead of time. Here’s what happens when you enable it:
>
> You add modelCacheConfig with weightsCache enabled to your InferenceEndpointConfig or JumpStartModel resource and apply it.
>
> The HyperPod Inference Operator automatically creates a ModelDataCacheConfig resource and begins downloading model weights from your configured source (Amazon S3, Amazon FSx for Lustre, HuggingFace Hub, or JumpStart) to local NVMe on all target nodes.
>
> After the node completes the download, the operator labels that node as cache-ready.
>
> The operator waits until all target nodes become cache-ready before creating the inference deployment, so that your pods can always access local data.
>
> When you start your pod, it reads from local NVMe storage at typical speeds of approximately 7 GB/s instead of downloading over the network.
>
> The cache that you configure remains available across pod restarts on the same node. During scale-out, if new pods land on nodes that already have the weights cached, they start immediately.
>
> Image cache
>
> The image cache pre-pulls the inference server container image onto nodes so pods do not wait for ECR downloads. Here’s what happens when you enable it:
>
> You add modelCacheConfig with imageCache enabled to your resource and apply it.
>
> The operator creates a DaemonSet that pulls the container image onto all target nodes.
>
> The inference deployment is created immediately by the operator. Unlike the weights cache, the image cache does not block deployment creation.
>
> When you start a pod with the image already cached, it skips the ECR pull entirely, saving 5–7 minutes.
>
> When you start a pod before the image cache is complete on that node, it pulls from ECR normally.
>
> Multiple deployments that use the same container image share a single image cache resource. The operator tracks references and only cleans up the cached image when no deployments reference it.
>
> Fallback behavior
>
> Both caching capabilities use preferred scheduling rather than required scheduling. Pods prefer nodes with cached data, but they’re never blocked from starting. When your scheduler places your pod on a node without a warm cache (for example, during rapid scale-out that exceeds the number of cached nodes), it reads weights from the original Amazon S3/Amazon FSx source and pulls the image from Amazon ECR. This is the same behavior as a pod running without caching enabled. There’s no failure, no user intervention, and no degraded behavior beyond the normal download time.
>
> Architecture and CRDs
>
> The operator introduces two Custom Resource Definitions (CRDs) to manage caching lifecycles. The operator creates and manages these automatically when you enable caching. You don’t need to create them directly.
>
> ModelDataCacheConfig manages the full lifecycle of model weights caching. The operator creates one per InferenceEndpointConfig or JumpStartModel that has weights caching enabled. It controls downloading weights from the source to local NVMe on target nodes, labeling nodes as cache-ready after the download completes, monitoring cache health and removing node labels if the cache becomes unhealthy, and cleaning up cached files from all nodes when the parent resource is deleted.
>
> You can inspect the state of the weights cache at any time:
>
> kubectl get modeldatacacheconfig -n &lt;namespace&gt;
>
> NAME STATE TARGET READY AGE
>
> example-model-cache Ready 10 10 5m
>
> ModelImageCache manages the lifecycle of container image caching. It controls pre-pulling the inference server image onto all target nodes, labeling nodes as image-ready once the pull completes, reporting per-node pull status, and cleaning up when no deployments reference the cached image.
>
> kubectl get inferenceimagecache -n hyperpod-inference-system
>
> NAME PHASE CACHED TARGET AGE
>
> iic-vllm-openai-ml-g5-24xlarge-a1b2 Complete 10 10 3m
>
> When you change the model source (for example, pointing to a new Amazon S3 path with updated weights), the operator creates a new cache, rolls out the updated deployment, and then cleans up the old cache. The same applies to image changes, ensuring zero-downtime transitions with no stale data.
>
> How to enable model caching
>
> You enable model caching by adding a modelCacheConfig section to your existing InferenceEndpointConfig or JumpStartModel resource. No additional infrastructure setup is needed.
>
> InferenceEndpointConfig example
>
> apiVersion: inference.sagemaker.aws.amazon.com/v1
>
> kind: InferenceEndpointConfig
>
> metadata:
>
> name: example-model
>
> namespace: default
>
> spec:
>
> modelName: example-model
>
> modelSourceConfig:
>
> modelSourceType: s3
>
> s3Storage:
>
> bucketName: example-bucket
>
> region: us-west-2
>
> modelLocation: "models/example-model"
>
> modelCacheConfig:
>
> weightsCache:
>
> enabled: true
>
> imageCache:
>
> enabled: true
>
> instanceType: ml.g5.24xlarge
>
> worker:
>
> image: vllm/vllm-openai:latest
>
> modelInvocationPort:
>
> containerPort: 8000
>
> modelVolumeMount:
>
> name: model-weights
>
> mountPath: /opt/ml/model
>
> resources:
>
> limits:
>
> nvidia.com/gpu: "4"
>
> JumpStartModel example
>
> apiVersion: inference.sagemaker.aws.amazon.com/v1
>
> kind: JumpStartModel
>
> metadata:
>
> name: example-jumpstart-model
>
> namespace: default
>
> spec:
>
> model:
>
> modelId: "meta-textgeneration-llama-3-1-8b-instruct"
>
> acceptEula: true
>
> server:
>
> instanceType: ml.g5.24xlarge
>
> modelCacheConfig:
>
> weightsCache:
>
> enabled: true
>
> imageCache:
>
> enabled: true
>
> You can enable either capability independently. If you only want to cache the image, omit weightsCache or set it to false. The weights cache also supports an optional hostPath override if you want to use a non-default NVMe mount path (default is /opt/dlami/nvme). If configured on Amazon SageMaker JumpStart, the configuration carries for each deployment from Amazon SageMaker JumpStart.
>
> Supported model sources
>
> Model caching works across all model sources supported by HyperPod Inference:
>
> Source
>
> Weights cache
>
> Image cache
>
> Amazon S3
>
> Supported
>
> Supported
>
> Amazon FSx for Lustre
>
> Supported
>
> Supported
>
> HuggingFace Hub
>
> Supported
>
> Supported
>
> Amazon SageMaker JumpStart (non-gated)
>
> Supported
>
> Supported
>
> Amazon SageMaker JumpStart (gated)
>
> Supported
>
> Supported
>
> Benchmarks
>
> Benchmarks across models ranging from 57–145 GB show around 60 percent faster scale-out when weights caching is enabled. The image cache can remove over two minutes of cold image-pull time, typically achieving up to a 97 percent reduction compared to pulling fresh from ECR on every pod start. The benefit scales with model size because there is proportionally more data that would otherwise need to be downloaded over the network. For models in the over 600 GB range like DeepSeek-R1, you’re removing what would otherwise be an over 30 minute download.
>
> Instance storage reference
>
> Because model caching stores weights on local NVMe, your instance type needs sufficient storage capacity for your model:
>
> Instance Type
>
> NVMe Storage
>
> ml.g5.xlarge
>
> 250 GB
>
> ml.g5.12xlarge
>
> 3,800 GB
>
> ml.g5.48xlarge
>
> 7,600 GB
>
> ml.p4d.24xlarge
>
> 8,000 GB
>
> ml.p5.48xlarge
>
> 30,000 GB
>
> Limitations to be aware of
>
> The weights cache is per-node, meaning each node maintains its own copy of the model weights. This is by design since each node needs local access, but NVMe consumption scales with the number of nodes.
>
> The initial cache population still requires downloading from the remote source. The first time you enable caching for a model, you pay the download cost once. After that, pods on those nodes start from local storage.
>
> NVMe storage is finite. If your model is 300 GB and your instance type only has 250 GB of NVMe, caching won’t work. Choose your instance type with model size in mind.
>
> Source updates aren’t auto-detected. If you update the model files at the same Amazon S3 path without changing the InferenceEndpointConfig spec, the operator will continue serving the cached version. To pick up new weights, update the spec (for example, change the model path or add a version suffix).
>
> Cleanup
>
> When you delete the InferenceEndpointConfig or JumpStartModel resource, the operator automatically removes all cached data, DaemonSets, and node labels from the cluster. No manual cleanup is needed and the NVMe storage is freed for other workloads.
>
> Getting started
>
> Model caching for Amazon SageMaker Inference on HyperPod is now generally available in all regions where Amazon SageMaker HyperPod is available. To start using it, add the modelCacheConfig section to your existing deployment spec and apply it. The operator handles the rest.
>
> For full documentation, see the SageMaker HyperPod Inference documentation.
>
> About the authors
>
> Kareem Syed-Mohammed
>
> Kareem is a Principal Product Manager at AWS. He  focuses on enabling generative AI model development and governance on Amazon SageMaker HyperPod. Prior to this, at Amazon Quick Sight, he led embedded analytics and developer experience. In addition to Quick Sight, he has been with AWS Marketplace and Amazon retail as a Product Manager. Kareem started his career as a developer for call center technologies, Local Expert and Ads for Expedia, and management consultant at McKinsey.
>
> Vinay Arora
>
> Vinay is a Specialist Solution Architect for Generative AI at AWS, where he collaborates with customers in designing cutting-edge AI solutions leveraging AWS technologies. Prior to AWS, Vinay has over two decades of experience in finance—including roles at banks and hedge funds—he has built risk models, trading systems, and market data platforms. Vinay holds a master’s degree in computer science and business management.
>
> Vamsi Goparaju
>
> Vamsi leads Go-to-Market (GTM) and Revenue Acceleration initiatives at AWS, enabling Inference and ModelOps workloads for our customers, and driving OSS Use Cases and Product features for Amazon SageMaker AI and Generative AI. With over 16 years of experience spanning AWS, Dell, and Infosys, he brings a unique blend of technical depth and business knowledge across Cloud, High-performance computing (HPC), Artificial Intelligence (AI), Machine Learning (ML), and Analytics. He holds an MBA from Texas A&amp;M University’s Mays Business School.
>
> Ophelia Yang
>
> Ophelia is a Software Development Engineer at AWS working on Amazon SageMaker AI. She focuses on building inference infrastructure for SageMaker HyperPod that simplifies how customers deploy and manage AI models. Her background spans ML cluster management, inference systems, and model evaluations.
>
> Can Sun
>
> Can is a Software Development Engineer at AWS working on Amazon SageMaker AI. He focuses on building inference infrastructure for SageMaker HyperPod that helps customers deploy and scale large language models efficiently and securely. His background spans LLM serving, model hosting on Hyperpod/SageMaker endpoint, and ML feature store.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。