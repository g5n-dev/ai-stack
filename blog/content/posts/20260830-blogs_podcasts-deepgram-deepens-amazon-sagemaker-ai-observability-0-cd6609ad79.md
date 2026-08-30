---
title: "Deepgram deepens Amazon SageMaker AI observability with Enhanced Metrics"
date: 2026-08-30T20:56:26+08:00
draft: false
entry_kind: "auto"
tags: ["AI Agent", "生成式 AI", "Advanced (300)", "Amazon SageMaker AI", "Technical How-to", "博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:7100c0949934178e4f255b15a8ea98b7b65662b4c5892df41b83b86dd1d0c9cf"
source_payload_sha256: "sha256:6756d86fcec1d613caa1ca6955f99329189d86c275ae0ce5df90659b30474723"
observation_id: obs_cd6609ad79310a0d482d61dd33f61ca6c0ec7d9d8ddbc10113b2399cfd1704d5
event_id: evt_b304ebfd9eb7f83b23250ab8df9ec2419465532b1635252bc5dffc8c55402d70
revision_id: rev_8c3081590b9b23e0fd59fdeeb5784de983d131cab250b96464f408d8fdb7a13e
source_published_at: 2026-08-27T16:11:27Z
first_seen_at: 2026-08-30T13:06:05Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 72
description: "当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。"
external_url: https://aws.amazon.com/blogs/machine-learning/deepgram-deepens-amazon-sagemaker-ai-observability-with-enhanced-metrics
parent_observation_id: null
last_seen_at: 2026-08-30T12:53:46.029882Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/deepgram-deepens-amazon-sagemaker-ai-observability-with-enhanced-metrics](https://aws.amazon.com/blogs/machine-learning/deepgram-deepens-amazon-sagemaker-ai-observability-with-enhanced-metrics)
- **发布域名**: aws.amazon.com

## 来源摘要/节选

> Self-hosted speech AI has historically carried an observability trade-off. The service can tell you an endpoint is up and how many requests it served. The questions that actually drive capacity planning and cost management stay locked inside the vendor’s container: what you are billed for, which features your traffic uses, and what the inference engine is doing on each GPU.
>
> If you run Deepgram’s speech-to-text (STT) and text-to-speech (TTS) models on SageMaker AI, audio and transcripts stay inside your own AWS account. This can help support your data residency and compliance efforts without giving up a managed control plane for deployment, scaling, and monitoring. Your specific obligations depend on your own controls and assessments, so consult your compliance team and review the AWS shared responsibility model.
>
> Deepgram is closing the gap on billing, feature usage, and engine behavior with the following two innovations, available today on Deepgram SageMaker AI deployments.
>
> Deepgram Enhanced Metrics: Usage and billing metrics that the Deepgram container publishes directly into your Amazon CloudWatch account, with no agent, no sidecar, and no additional IAM permissions. These are the same consumed-unit values that drive AWS Marketplace metered billing, so you can reconcile your AWS bill against actual traffic down to the model and transport.
>
> Prometheus and OpenTelemetry support: Engine-level Prometheus metrics scraped straight from the Deepgram container, and per-GPU accelerator and host metrics. Both are collected through SageMaker AI detailed observability and queryable with PromQL from CloudWatch, Grafana, or any Prometheus-compatible tool.
>
> In this post, we walk through both capabilities: how they work, what they show you that you couldn’t see before, and how to start using them on a Deepgram SageMaker AI endpoint.
>
> Deepgram on Amazon SageMaker AI
>
> Deepgram’s speech models are available as model packages on AWS Marketplace and deploy as SageMaker AI real-time endpoints in your account. With SageMaker AI, you get baseline observability on your endpoints automatically: invocation metrics such as ConcurrentRequestsPerModel and FirstChunkLatency in CloudWatch, container logs in Amazon CloudWatch Logs, and alarm-driven automatic scaling.
>
> AWS Marketplace model packages run with network isolation. The container cannot make outbound connections, which is why security-conscious customers choose this deployment model. The same isolation, however, is what normally makes vendor-level telemetry hard. The container can’t push metrics to an external collector, and you can’t see inside the container. Both capabilities in this post work within that constraint: neither requires the container to open a network path, and both land the data in your own CloudWatch account.
>
> A note on terminology: SageMaker AI has its own endpoint feature called enhanced metrics (EnableEnhancedMetrics in MetricsConfig), which adds per-instance and per-GPU utilization dimensions to the standard endpoint metrics. The SageMaker AI feature is distinct from and complementary to Deepgram Enhanced Metrics, the Deepgram-published billing and usage metrics described in the following sections. This post covers the Deepgram capability. For the SageMaker AI capability, see Deepgram’s SageMaker observability guide.
>
> Innovation 1: Billing and usage transparency with Deepgram Enhanced Metrics
>
> Deepgram Enhanced Metrics answer two questions no standard endpoint metric can: exactly what you’re being billed for, and how your traffic actually uses Deepgram’s features.
>
> How it works: Metrics that ride the logging path
>
> The Deepgram container writes CloudWatch Embedded Metric Format (EMF) records to container stdout. SageMaker AI already forwards container output to the endpoint’s CloudWatch log group, and CloudWatch Logs extracts EMF records into metrics automatically. The EMF path gives you the following benefits.
>
> No agent, sidecar, or collector to deploy.
>
> No additional IAM permissions beyond what the endpoint already has for logging.
>
> Works under AWS Marketplace network isolation, because metrics travel over the existing SageMaker-to-CloudWatch logging path rather than any outbound network connection.
>
> Classic CloudWatch metrics: They appear in aws cloudwatch list-metrics and work with get-metric-statistics, dashboards, alarms, and metric math, with nothing to enable on the endpoint configuration.
>
> All dimensions are low-cardinality and contain no personally identifiable information (PII): no transcripts, TTS input, or per-request identifiers.
>
> Deepgram Enhanced Metrics aggregate across the Deepgram endpoints in your AWS account and Region. The dimensions cover category, model, and transport, but not endpoint name or instance ID, so you cannot filter this stream to a single endpoint or instance. For per-endpoint, per-instance, or per-GPU breakdowns, use the Prometheus and OpenTelemetry metrics in the next section.
>
> Reconcile your AWS Marketplace bill: The Deepgram/SageMakerInference namespace
>
> The billing namespace emits one record per completed request, covering each streaming session, pre-recorded request, and TTS request. The ConsumedUnits metric carries the same billable-unit values that drive AWS Marketplace metered billing. The following table lists the metrics this namespace publishes.
>
> Metric
>
> Unit
>
> Description
>
> ConsumedUnits
>
> Count
>
> Billable inference units for the request. Sum over a period is the total billed volume.
>
> AudioDurationSeconds
>
> Seconds
>
> Duration of audio processed (speech-to-text).
>
> CharCount
>
> Count
>
> Characters synthesized (text-to-speech).
>
> Dimensions are published at three granularities ([Category], [Category, Model], and [Category, Model, Transport]), so you can answer what did streaming STT cost this month and how much of that was nova-3 with the same namespace. For example, total consumed units per hour for streaming speech-to-text:
>
> aws cloudwatch get-metric-statistics \
>
> --namespace Deepgram/SageMakerInference \
>
> --metric-name ConsumedUnits \
>
> --dimensions Name=Category,Value=stt_streaming \
>
> --start-time $(date -u -d '24 hours ago' +%Y-%m-%dT%H:%M:%S) \
>
> --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
>
> --period 3600 \
>
> --statistics Sum SampleCount \
>
> --region YOUR_AWS_REGION
>
> SampleCount is the number of billed requests. Because these are ordinary CloudWatch metrics, you can build a finance-facing billing dashboard or set a budget alarm on consumed units.
>
> Understand how your endpoint is used: The Deepgram/SelfHosted namespace
>
> A second stream, emitted by the Deepgram API server itself, breaks raw usage down by method, model tier, and enabled feature, independent of billing. It answers product-level questions: how much traffic is streaming versus pre-recorded, which model tiers process the most audio, and which features (diarization, smart formatting, redaction, keyterm prompting) your applications actually enable. The following table lists the metrics in this namespace and the dimensions each one carries.
>
> Metric
>
> Dimensions
>
> What it tells you
>
> AudioMs, Requests
>
> Deployment, Method
>
> Volume by streaming compared to pre-recorded
>
> TierAudioMs
>
> Deployment, Tier
>
> Audio processed per model tier (for example, nova-3, flux)
>
> FeatureAudioMs, FeatureTokens
>
> Deployment, Feature
>
> Utilization per enabled feature (for example, diarize, smart_format, redact)
>
> TtsCharacters, Tokens, VoiceAgentMs
>
> Deployment, Method
>
> TTS, intelligence-feature, and voice-agent volume
>
> For example, how much audio ran with diarization enabled in the last 24 hours:
>
> aws cloudwatch get-metric-statistics \
>
> --namespace Deepgram/SelfHosted \
>
> --metric-name FeatureAudioMs \
>
> --dimensions Name=Deployment,Value=sagemaker Name=Feature,Value=diarize \
>
> --start-time $(date -u -d '24 hours ago' +%Y-%m-%dT%H:%M:%S) \
>
> --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
>
> --period 3600 \
>
> --statistics Sum \
>
> --region YOUR_AWS_REGION
>
> The usage stream is on by default and can be disabled with a single environment variable override in the endpoint configuration (DEEPGRAM_API_01: emf.enabled=false). The billing stream cannot be disabled. It is part of the metering pipeline.
>
> Innovation 2: Engine-level and per-GPU visibility with Prometheus and OpenTelemetry
>
> Deepgram containers serve a Prometheus metrics endpoint, and SageMaker AI detailed observability runs an AWS managed OpenTelemetry Collector on each instance backing the endpoint. The collector scrapes the container and exports the results to CloudWatch, and it exports per-GPU and host-level metrics.
>
> With detailed observability enabled, three metric sources publish to the CloudWatch OTel-compatible metric store. The following table describes each source and why it matters.
>
> Source
>
> Example metrics
>
> Why it matters
>
> GPU (DCGM exporter)
>
> DCGM_FI_DEV_GPU_UTIL, DCGM_FI_DEV_FB_USED
>
> Per-GPU series. On multi-GPU instances, each GPU reports separately, so a saturated device can’t hide behind a summed or averaged utilization number.
>
> Host (node exporter)
>
> node_cpu_seconds_total, node_memory_MemTotal_bytes
>
> Standard Prometheus node-exporter metrics for each instance.
>
> Deepgram engine
>
> engine_active_requests{kind="stream"}, engine_estimated_stream_capacity
>
> The collector scrapes the Deepgram container’s Prometheus endpoint directly. These are the same API and Engine metrics Deepgram’s self-hosted customers use for capacity planning, now available on SageMaker AI without running any collector yourself. See Deepgram’s Metrics Guide for the complete reference.
>
> engine_estimated_stream_capacity is the Deepgram engine’s own estimate of how many concurrent streams the instance can sustain. Comparing it against engine_active_requests gives you an engine-reported headroom signal for scaling decisions.
>
> Every series carries SageMaker resource labels, including aws.sagemaker.endpoint.name, the variant name, and the instance ID. You can filter to a single endpoint, isolate one instance in a scaled-out fleet, or compare GPUs within an instance. Because the collector runs on the host, outside the model container, this works under AWS Marketplace network isolation.
>
> Enabling it
>
> Detailed observability is on by default for newly created endpoints, publishing every 60 seconds. To set it explicitly, for example on an endpoint created before the feature launched, or to change the publish frequency, use MetricsConfig on the endpoint configuration:
>
> aws sagemaker create-endpoint-config \
>
> --endpoint-config-name YOUR_CONFIG_NAME \
>
> --production-variants file://production-variants.json \
>
> --metrics-config '{"EnableDetailedObservability": true, "MetricPublishFrequencyInSeconds": 60}' \
>
> --region YOUR_AWS_REGION
>
> For an endpoint already serving traffic, create a new endpoint configuration and run update-endpoint. The update is a blue/green deployment, and the endpoint stays in service.
>
> Query with PromQL from CloudWatch, Grafana, or anything Prometheus-compatible
>
> The metrics land in the CloudWatch OTel metric store and are queried with PromQL. In the CloudWatch console’s PromQL editor, filter per-GPU utilization to one endpoint:
>
> DCGM_FI_DEV_GPU_UTIL{"aws.sagemaker.endpoint.name"="YOUR_ENDPOINT_NAME"}
>
> CloudWatch also exposes a standard Prometheus-compatible HTTP API for these metrics, authenticated with SigV4:
>
> awscurl --service monitoring --region YOUR_AWS_REGION \
>
> "https://monitoring.YOUR_AWS_REGION.amazonaws.com/api/v1/query?query=engine_active_requests"
>
> If you’ve standardized on Grafana or another Prometheus-native observability stack, you can point your existing tooling at your SageMaker AI fleet: no parallel monitoring stack, no export pipeline.
>
> Choosing the right metric stream
>
> The two innovations complement the built-in metrics of SageMaker AI rather than replacing them. The following table maps common questions to the metric stream that answers them.
>
> Question
>
> Where to look
>
> Is the endpoint healthy? Are requests erroring or slow to start?
>
> Standard SageMaker metrics (ConcurrentRequestsPerModel, FirstChunkLatency, Invocation5XXErrors)
>
> What is my Marketplace bill going to be, and which models drove it?
>
> Deepgram Enhanced Metrics (Deepgram/SageMakerInference, account-level)
>
> Which features and model tiers does my traffic actually use?
>
> Deepgram Enhanced Metrics (Deepgram/SelfHosted, account-level)
>
> How saturated is each GPU? How much stream capacity remains on each instance of a specific endpoint?
>
> Prometheus/OTel through detailed observability (DCGM and Deepgram engine metrics, per endpoint/instance/GPU)
>
> Get started
>
> Deepgram Enhanced Metrics require no setup: they flow into your CloudWatch account from the moment a Deepgram SageMaker AI endpoint serves traffic. Detailed observability is on by default for new endpoints and takes one endpoint-configuration change to add to existing ones. To get started, use the following resources.
>
> Deploy Deepgram from AWS Marketplace and follow Deploy Deepgram on Amazon SageMaker.
>
> Reference: Deepgram Enhanced Metrics, Prometheus &amp; OpenTelemetry Metrics, and the Metrics Guide for the complete list of Deepgram API and Engine metrics.
>
> AWS documentation: Detailed observability for SageMaker AI endpoints.
>
> Conclusion
>
> Self-hosting speech AI no longer leaves a gap between the service’s request counters and the vendor’s invoice. Deepgram Enhanced Metrics land the exact units that drive AWS Marketplace billing in your own CloudWatch account, with zero infrastructure. The feature-level usage behind those units lands there too. With Prometheus and OpenTelemetry support through SageMaker AI detailed observability, the Deepgram engine’s own capacity and load metrics and per-GPU utilization are one PromQL query away in the tools your team already uses.
>
> These capabilities are Deepgram’s latest investment in SageMaker AI as a preferred deployment option for self-hosted speech AI, following IAM Temporary Delegation for support access. They continue the commitment of making the day-two experience match the day-one experience. Deepgram models currently listed on SageMaker AI, including Nova, Flux, and Aura-2, come with a 14-day trial at no additional cost. Your team can stand up a real deployment in your own AWS account before committing. Running Deepgram models on SageMaker AI incurs charges for endpoint hosting, including GPU instances. It also incurs charges for Amazon CloudWatch logs and metrics and associated networking resources. While the Deepgram trial is offered at no additional cost, AWS infrastructure costs apply from the start of deployment. Review the SageMaker AI pricing and use AWS Cost Explorer to monitor your spending.
>
> About the authors
>
> Victor Wang
>
> Victor is a Staff Software Engineer at Deepgram and Technical Advisor to the VP of Engineering based in San Francisco, CA. Before joining Deepgram, Victor held multiple roles at AWS including Sr. Solutions Architect, Technical Program Manager, Proserve Consultant, and Software Developer. His passion is learning new technologies and traveling the world. Victor has flown over 2 million miles and plans to continue his eternal journey of exploration.
>
> Andre Gomes
>
> Andre is a Frontier AI Solutions Architect at AWS, working with startups on large-scale training and real-time inference. As a former startup co-founder and CEO, he partners with founders to scale their workloads on AWS and reach customers worldwide. Andre earned his PhD at UFMG, with research at the Institute for Manufacturing, University of Cambridge, applying large language models and neural topic modeling to technology roadmapping.
>
> Daniel Wirjo
>
> Daniel is a Solutions Architect at AWS, focused on AI and SaaS startups. As a former startup CTO, he enjoys collaborating with founders and engineering leaders to drive growth and innovation on AWS. Outside of work, Daniel enjoys taking walks with a coffee in hand, appreciating nature, and learning new ideas.
>
> Kareem Syed-Mohammed
>
> Kareem is a Product Manager at AWS. He focuses on enabling generative AI model development and governance on Amazon SageMaker HyperPod. Earlier, at Amazon QuickSight, he led embedded analytics and developer experience. He has also been with AWS Marketplace and Amazon retail as a Product Manager. Kareem started his career as a developer for call center technologies, Local Expert and Ads for Expedia, and management consultant at McKinsey.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。