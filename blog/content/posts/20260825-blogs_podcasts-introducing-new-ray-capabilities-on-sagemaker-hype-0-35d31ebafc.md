---
title: "Introducing new Ray capabilities on SageMaker HyperPod"
date: 2026-08-25T12:57:25+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "机器学习", "Amazon SageMaker HyperPod", "Amazon SageMaker Studio", "Announcements", "Foundational (100)", "博客与播客"]
categories: []
source: "blogs_podcasts"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:108425573d541d426f9e0423d22e1d2a1d2320349f53fedb9f08ea083fb8f410"
source_payload_sha256: "sha256:bcd2a3275e66e15ec077f765e8d7b4577c6a77f904d001638b17d83dbab1443b"
observation_id: obs_35d31ebafcc15027dd0f6f6eb30e580fe67dbdb2e57923a460e2125e1c588fd0
event_id: evt_8c7ce239c59a7265d059a9782d3b68c7146b1076fa801428bdb7cd82a62a9843
revision_id: rev_316e67c90ae45f8bb8a3ef10be4262d73a0f6968f8016f07e85619f7304cfec1
source_published_at: 2026-08-24T19:32:14Z
first_seen_at: 2026-08-25T17:45:55.090974Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 54
description: "当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。"
external_url: https://aws.amazon.com/blogs/machine-learning/introducing-new-ray-capabilities-on-sagemaker-hyperpod
parent_observation_id: null
last_seen_at: 2026-08-25T04:53:52.319224Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/introducing-new-ray-capabilities-on-sagemaker-hyperpod](https://aws.amazon.com/blogs/machine-learning/introducing-new-ray-capabilities-on-sagemaker-hyperpod)
- **发布域名**: aws.amazon.com

## 来源摘要/节选

> Today, we are announcing new Ray capabilities on Amazon SageMaker HyperPod that integrate Ray with the HyperPod purpose-built infrastructure for foundation model training and serving.
>
> Ray is an open-source framework that data scientists use to scale distributed Python workloads across clusters of GPUs, from distributed training with Ray Train to model serving with Ray Serve. On Kubernetes, Ray clusters are managed by KubeRay, an open-source operator that handles cluster lifecycle through custom resources (RayCluster, RayJob, RayService). SageMaker HyperPod provides purpose-built infrastructure for large-scale machine learning (ML) on Amazon Elastic Kubernetes Service (Amazon EKS) with built-in node health monitoring and automatic recovery. Until now, running Ray on Kubernetes required data scientists to write YAML manifests, manage Docker image rebuilds for every dependency change, set up kubectl port-forward to access their Ray Dashboard, and configure Prometheus and Grafana manually for observability.
>
> With this launch, data scientists can create Ray clusters, open the Ray Dashboard and Amazon Managed Grafana observability dashboards, connect a JupyterLab or Code Editor workspace to their cluster, submit distributed jobs, and configure hung job detection, all from SageMaker Studio. At the application level, Ray training jobs gain automatic fault tolerance through HyperPod node health monitoring and recovery, plus tiered checkpointing for faster resume through HyperPod distributed tiered storage. SageMaker JumpStart integration loads model weights directly into Ray Serve endpoints, with KV cache offloading to tiered storage for serving long-context requests. These capabilities work with open-source KubeRay and standard Ray APIs, so existing scripts and workflows run without modification.
>
> In this post, we walk through how to get started with each of these capabilities.
>
> Prerequisites
>
> To follow along with this post, you need an Amazon SageMaker HyperPod cluster with Amazon EKS orchestration and the following components installed on your cluster:
>
> SageMaker Spaces EKS add-on, which enables JupyterLab and Code Editor workspaces in Amazon SageMaker HyperPod that attach to Ray clusters for interactive development.
>
> HyperPod Observability EKS add-on, which collects metrics from Ray workloads and provisions Grafana dashboards in Amazon Managed Grafana.
>
> KubeRay operator, which manages RayCluster, RayJob, and RayService as native Kubernetes resources.
>
> HyperPod Ray Endpoint Operator (Helm chart), which generates authenticated public endpoints for dashboard access and remote job submission.
>
> You also need a SageMaker Studio domain, which provides the console interface for creating Ray clusters, viewing workloads, opening dashboards, and managing HyperPod Spaces. For full setup instructions, see the Ray on HyperPod getting started guide.
>
> Purpose-built data scientist experience
>
> SageMaker Studio now provides a complete Ray development environment. Data scientists can create, manage, and monitor Ray clusters directly from the console without writing Kubernetes manifests or running kubectl commands. You can check out the full experience in this interactive demo.
>
> To get started, navigate to SageMaker Studio and choose HyperPod. Select your HyperPod cluster, then go to the Tasks tab. From the task type list, choose RayCluster. The console displays your Ray clusters with their status, instance types, and available actions. To create a new cluster, choose Create Ray Cluster.
>
> The creation form prompts you for a cluster name, head and worker instance types, worker count, and container image. By default, clusters use the SageMaker Distribution image, which comes with Ray pre-installed and is managed by AWS with regular vulnerability patching and software upgrades. You can also specify a custom container image if your workload requires additional dependencies.
>
> For customers who prefer kubectl or need advanced customization, an inline YAML editor in Studio exposes the full Kubernetes manifest. The KubeRay operator also integrates with HyperPod task governance, so administrators can set compute quotas and scheduling priorities for Ray workloads alongside other training jobs.
>
> During creation, enable remote endpoints so that you can access the Ray Dashboard, submit jobs, and retrieve logs from anywhere with internet access, securely and without local kubectl port-forwarding. To learn more, see Ray Dashboard access.
>
> After the create cluster form is submitted, go back to the tasks tab and it will show the cluster like in the screenshot below. From the Actions menu, you can open the Ray Dashboard, view Grafana metrics, edit the cluster configuration, or delete the cluster.
>
> After the cluster reaches Running status, choose Open Ray Dashboard from the Actions menu. The system generates a short-lived, IAM-authenticated URL scoped to the cluster creator. The Ray Dashboard opens in a new tab, showing cluster health, running jobs, and node status.
>
> Remote job submission
>
> For production workloads, you can submit jobs remotely to Ray clusters from Studio, your laptop, or continuous integration and continuous delivery (CI/CD) pipelines using the toolkit-for-ray-on-sagemaker-ai Python package. The package handles endpoint resolution and EKS API credential generation through IAM authentication, so you use standard Ray job submission APIs with a SageMaker-aware address resolver:
>
> $ aws eks update-kubeconfig --name &lt;eks-cluster-name&gt; --region &lt;region&gt;
>
> $ pip install toolkit-for-ray-on-sagemaker-ai
>
> $ ray job submit --address sagemaker_ray://&lt;ray-cluster-name&gt;/&lt;namespace&gt; \
>
> --working-dir &lt;your-code-directory&gt; \
>
> --python your-code.py
>
> # To list ray jobs
>
> $ ray job list --address sagemaker_ray://&lt;ray-cluster-name&gt;/&lt;namespace&gt;
>
> Interactive development with SageMaker Spaces
>
> Data scientists can attach a Ray cluster to a HyperPod JupyterLab or Code Editor space from Studio. The space joins the cluster as a zero-compute worker node, giving the notebook full native Ray driver access. You select your cluster from a list during space creation and begin working immediately.
>
> After creating a HyperPod JupyterLab or Code Editor space, a Ray cluster integration option appears in the configuration panel.
>
> Select the Ray cluster you want your workspace to connect to.
>
> Attaching a Ray cluster restarts the space. Once it restarts, open JupyterLab or Code Editor in your browser and call ray.init(address="auto"). You are connected to your Ray cluster and can run distributed workloads as if you were on the head node. Ray’s runtime_env parameter lets you inject Python dependencies at runtime without rebuilding container images, and you can scale workers up or down without recreating the cluster. For example, a data scientist training a model can start prototyping in a notebook with a single worker, then scale to four GPU workers by changing one line in ScalingConfig. The training runs distributed across the attached Ray cluster while the notebook remains interactive for monitoring progress, adjusting hyperparameters, or inspecting intermediate results. The entire workflow stays within the notebook.
>
> To learn more, see IDEs and Notebooks with Ray.
>
> Out-of-the-box observability
>
> Setting up Ray observability on Kubernetes with Amazon Managed Service for Prometheus and Amazon Managed Grafana is a multi-step process that involves installing Helm charts, creating PodMonitors and ServiceMonitors, configuring IAM roles for SigV4 signing, and manually importing dashboard JSON files.
>
> The HyperPod Observability EKS add-on now handles all of this. It automatically discovers Ray head and worker pods, scrapes their metrics endpoints, and provisions four pre-built Grafana dashboards in Amazon Managed Grafana: Ray Core, Ray Data, Ray Train, and Ray Serve. You do not need to create PodMonitors, configure scrape targets, or import dashboard JSON files.
>
> All four dashboards are organized under a Ray folder in Amazon Managed Grafana and support filtering metrics by specific Ray cluster. The Open Grafana action from the cluster list (shown in the first screenshot) takes you directly to the metrics for your specific cluster in one click. The dashboards appear alongside existing HyperPod infrastructure dashboards (GPU, EFA, task governance), so operations teams see Ray workload metrics and cluster health in one place.
>
> Resilient training
>
> SageMaker HyperPod provides three layers of resilience for Ray training workloads: automatic node recovery when hardware fails, hung job detection when training stalls, and tiered checkpointing for fast recovery after either event.
>
> Automatic node recovery
>
> SageMaker HyperPod continuously monitors node health and can automatically replace faulty nodes so your Ray training jobs can run for as long as needed without manual restarts. When a node is replaced, Ray reschedules worker pods onto the new healthy node. If your training code saves checkpoints periodically and includes logic to resume from the latest checkpoint, the job picks up where it left off. This requires no changes to your existing Ray training code. You only need to configure a sufficient number of retries in your RayJob’s FailureConfig so that jobs recover automatically rather than failing permanently on the first interruption. To learn more, see Automatic node recovery with Ray.
>
> Hung job detection
>
> Distributed training jobs can hang without producing errors. A single pod fails (because of a network partition, storage mount issue, or hardware fault), and every other pod blocks at the next collective operation, waiting indefinitely. GPUs stay allocated with memory loaded but produce no useful compute. Because there is no error message or crash, data scientists often discover the problem hours later when they check job progress manually. At scale, a few hours of undetected hang time across dozens of GPUs represents significant wasted cost.
>
> SageMaker HyperPod EKS now includes a per-node Job Monitoring Agent that detects these conditions for Ray Train workloads automatically, with no changes to your code. The agent monitors multiple node-level and job-level signals to determine when a training job has stalled, and notifies the user through the cluster’s Amazon CloudWatch log group and the Ray Train Grafana dashboard provisioned by the HyperPod Observability add-on.
>
> For custom detection rules, data scientists can use the toolkit-for-ray-on-sagemaker-ai library to define log patterns and timeout thresholds. When the configured action is cancel, HyperPod terminates the hung worker process and Ray Train’s built-in FailureConfig restarts workers from the last checkpoint. To learn more, see HyperPod Hung Job Detection on Ray.
>
> Tiered checkpointing
>
> Fast checkpoint recovery is critical for both node replacement and hung job restart scenarios. The amzn-sagemaker-checkpointing library integrates with HyperPod managed tiered checkpointing, which writes checkpoints to local disk and asynchronously uploads them to Amazon Simple Storage Service (Amazon S3). When a job restarts, the library checks HyperPod Tiered Storage first. If the checkpoint is still available there, recovery is faster than restoring from Amazon S3. For large models, this can reduce recovery time compared to restoring directly from Amazon S3. To learn more, see HyperPod Tiered Storage on Ray.
>
> Accelerated inference
>
> Ray Serve is Ray’s framework for deploying ML models as scalable, production-ready endpoints. It supports multi-model composition, autoscaling, and works with serving engines like vLLM. SageMaker HyperPod supports Ray Serve workloads on EKS, so you can deploy and scale inference endpoints on your HyperPod cluster.
>
> SageMaker JumpStart provides a catalog of pre-trained models. With this launch, the toolkit-for-ray-on-sagemaker-ai library now includes a JumpStart model loader that downloads model weights from the JumpStart catalog and deploys them directly into Ray Serve on HyperPod without manual weight download, model configuration, or container setup.
>
> One common challenge with large language model (LLM) serving is that inference latency grows with context length. Each new token requires recalculating attention over all previous tokens, making long documents and multi-turn conversations slow and expensive. SageMaker HyperPod addresses this with Managed Tiered KV Cache. The tiered cache stores attention key-value vectors in CPU memory on each node (L1) and on HyperPod Tiered Storage for cross-instance sharing (L2). Your Ray Serve deployments can take advantage of the Tiered Storage KV caching capabilities in SageMaker HyperPod with minimal code changes, reducing time-to-first-token for multi-turn conversations and long-document workloads. To learn more, see Accelerated Ray Inference on SageMaker HyperPod.
>
> Clean up
>
> To free up compute capacity on your cluster, delete any Ray clusters you created during this walkthrough. From the SageMaker Studio Tasks tab, select your Ray cluster and choose Delete from the Actions menu. If you created a HyperPod cluster, you can delete the cluster from the Amazon SageMaker AI console to stop incurring charges for the underlying compute instances. If you installed any prerequisite add-ons for testing, uninstall them from EKS console to free up compute capacity.
>
> Conclusion
>
> In this post, we walked through how Amazon SageMaker HyperPod now provides a complete Ray experience on EKS, from cluster creation and interactive notebooks to resilient training and accelerated inference. All of this works with open-source KubeRay and standard Ray APIs, so existing scripts run without modification. We’d like to thank Dhawal Parkar, Pradeep Cruz, Mark Vinciguerra, and Giuseppe Angelo Porcelli for their contributions to this post.
>
> This integration is available today in all AWS Regions where SageMaker HyperPod EKS is supported. To get started, see the Amazon SageMaker HyperPod documentation and the Ray on HyperPod getting started guide. You can also explore the full workflow in this interactive demo. If you’d like to discuss how Ray on HyperPod can support your workloads, contact an AWS representative.
>
> About the authors
>
> Nilesh PS
>
> Nilesh is a Senior Software Development Engineer at AWS working on Amazon SageMaker HyperPod. He focuses on Ray cluster management, training resiliency, and observability for large-scale distributed ML workloads on Kubernetes.
>
> Vishal Shahane
>
> Vishal is a Principal Engineer at AWS working on Amazon SageMaker HyperPod, where he focuses on building reliable, scalable infrastructure for large-scale AI/ML workloads.
>
> Shreyas Adiyodi
>
> Shreyas is a Product Manager at AWS based out of Seattle. He is focused on enabling Gen AI model development on SageMaker HyperPod, partnering with customers to simplify cluster provisioning, enhance OSS AI/ML framework support, and strengthen security and compliance.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。