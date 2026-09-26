---
title: "Speaker-labeled transcription with WhisperX on SageMaker AI"
date: 2026-09-25T03:13:20+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "生成式 AI", "机器学习", "深度学习", "Advanced (300)", "Amazon SageMaker AI", "Technical How-to"]
categories: []
source: "blogs_podcasts"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:59e3c8835ef565a51ad405a078f72d5eca2db65541972dff0d370aec28ff3281"
source_payload_sha256: "sha256:f085391d0071fc6c8c871d7d625d36537ce7be1b90e4a063381d6cda4206415a"
observation_id: obs_779a1ba64af323a34a47ec8faadab92b3dda7836d54ea3b4e91007e1a0fc79b7
event_id: evt_219361563ff24996d41759b53a76b18ef475b5f43d3ee2d64dcafeef5aba97bf
revision_id: rev_32f8bf428fb1af5b891f5df03cd1f0ba0c0bdc4a49216b204f24d799c146fd70
source_published_at: 2026-09-24T16:20:12Z
first_seen_at: 2026-09-24T19:23:44Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 59
description: "当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。"
external_url: https://aws.amazon.com/blogs/machine-learning/speaker-labeled-transcription-with-whisperx-on-sagemaker-ai
parent_observation_id: null
last_seen_at: 2026-09-26T00:00:00Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/speaker-labeled-transcription-with-whisperx-on-sagemaker-ai](https://aws.amazon.com/blogs/machine-learning/speaker-labeled-transcription-with-whisperx-on-sagemaker-ai)
- **发布域名**: aws.amazon.com

## 来源摘要/节选

> Any team working with spoken audio hits the same wall with generic speech-to-text. Think contact-center calls, all-hands meetings, podcasts, depositions, and broadcast media. These workloads need two things that standard transcription gets wrong. First, timestamps land at the utterance level, off by several seconds. Second, there’s no reliable answer to “who said what.” Those gaps make transcripts hard to search, caption, redact, or analyze at scale. A missing speaker label breaks compliance review, and an imprecise timestamp breaks a caption or a redaction.
>
> WhisperX closes both gaps. It wraps OpenAI’s Whisper with batched inference, adds wav2vec2 forced alignment for precise per-word timestamps, and adds speaker diarization to label who spoke. These capabilities map directly to real workloads. Contact centers can measure talk time, check script adherence, and run sentiment analysis, while teams turn meetings into searchable notes. Media and e-learning teams generate accurate captions (in SubRip Subtitle (SRT) and Web Video Text Tracks (VTT) format) for large content libraries. Time-sensitive uses get text the moment someone speaks. In regulated fields like healthcare, legal, and finance, speaker-labeled transcripts support audits and legal discovery.
>
> The AWS WhisperX Deep Learning Container (DLC) packages all of this into a GPU-ready image. You deploy it to an Amazon SageMaker AI real-time or asynchronous endpoint without building a custom image. In this post, we show how to deploy both endpoint types and when to choose each. We also cover the production details that matter: the GPU AMI pin, scaling, Amazon Simple Storage Service (Amazon S3) setup, and cost controls. This post is part of a multimodal series showcasing specialized AWS DLCs. The series spans three AWS DLCs across four use cases: (1) vLLM-Omni for text-to-speech, (2) vLLM-Omni for image and video, (3) WhisperX for speech-to-text (this post), and (4) llama.cpp.
>
> What is WhisperX, and what workloads it unlocks
>
> Whisper is a popular open source automatic speech recognition (ASR) model family from OpenAI that transcribes spoken audio into text accurately across many languages. It focuses on high-quality transcription and produces timestamps at the phrase or segment level. WhisperX is an open source project that builds on Whisper and extends it for production workloads. It adds per-word timestamps, speaker labels, and faster transcription, three capabilities that together turn raw audio into structured, analyzable transcripts.
>
> Why a purpose-built Deep Learning Container
>
> The AWS WhisperX DLC is a maintained, GPU-ready image that already contains Whisper, the alignment models, and the diarization weights, with no Hugging Face token required. It follows the standard Amazon SageMaker AI serving contract, so you deploy it like any other model.
>
> Serving contract: The container serves on port 8080 and exposes POST /invocations for inference and GET /ping for health checks.
>
> Request format: The endpoint expects multipart/form-data, with the audio as the file part plus optional string fields such as language, diarize, and response_format. Amazon SageMaker AI passes the ContentType header (including the multipart boundary) through to the container unchanged.
>
> Output formats: json, verbose_json, srt, and vtt, so the same endpoint feeds analytics pipelines and video editors alike.
>
> Choosing between real-time and asynchronous endpoints
>
> Amazon SageMaker AI supports both real-time and asynchronous endpoints, so you can serve the same WhisperX DLC through either pattern. The decision usually comes down to clip length and interactivity. For long audio, use the asynchronous endpoint: it’s the recommended path when transcription, alignment, and diarization need more time to run. Reserve the real-time endpoint for short, interactive clips that finish within the Amazon SageMaker AI 60-second response cap.
>
> Dimension
>
> Real-time endpoint
>
> Asynchronous endpoint
>
> Best for
>
> Short, interactive clips
>
> Long audio, high-volume batch
>
> Latency
>
> Synchronous, must finish &lt; 60s
>
> Submit-and-poll. No response cap
>
> Invocation
>
> InvokeEndpoint (inline body)
>
> InvokeEndpointAsync (S3 reference)
>
> I/O
>
> Body in request / response
>
> Input + output in Amazon S3
>
> Scaling
>
> Add instances (one request/container)
>
> Add instances. Can autoscale to zero
>
> Cost profile
>
> Bills while endpoint is up
>
> Scale-to-zero when idle saves cost
>
> Solution architecture
>
> Both patterns share the same container contract. Amazon SageMaker AI forwards each request to the WhisperX DLC on port 8080. The real-time pattern is synchronous, and the asynchronous pattern brokers input and output through Amazon S3. Instance selection (ml.g4dn.xlarge for cost, ml.g5.2xlarge for headroom) and the required GPU AMI pin apply to both, and you scale throughput by adding instances rather than concurrency. The request/response sequence for each endpoint type is shown in its walkthrough section.
>
> Prerequisites
>
> An AWS account and an Amazon SageMaker AI execution role that can create_model, create_endpoint, and (for asynchronous inference) read and write S3.
>
> GPU service quota for your endpoint instance type (for example, ml.g4dn.xlarge or ml.g5.2xlarge).
>
> The WhisperX DLC image URI from Amazon Elastic Container Registry (Amazon ECR) (for example, 763104351884.dkr.ecr.&lt;region&gt;.amazonaws.com/whisperx:3.8.6-cu128-amzn2023-sagemaker).
>
> For asynchronous inference, an S3 bucket whose name contains “sagemaker.” The default AmazonSageMakerFullAccess policy grants S3 access only to such buckets.
>
> A complete, runnable JupyterLab notebook that walks through these steps end to end is available in the AWS Samples repository. You can run it in Amazon SageMaker AI Studio against your own audio.
>
> Walkthrough: Real-time endpoint
>
> The real-time endpoint returns the transcript in the same synchronous call. Use it for short clips that comfortably finish within the 60-second cap. Figure 1 is a sequence diagram that traces a single real-time request end to end, from the client call through in-container transcription to the inline transcript.
>
> Figure 1: Real-time endpoint synchronous InvokeEndpoint flow, in-container transcription, and inline transcript within the 60-second cap
>
> Reading the sequence end to end: the client assembles a multipart/form-data body (the audio as the file part plus fields such as language, diarize, and word-level timestamp granularity) and calls InvokeEndpoint. Amazon SageMaker AI forwards the request to the container on port 8080, passing the ContentType and its multipart boundary through unchanged. Inside the container, WhisperX runs voice-activity detection and batched Whisper transcription, wav2vec2 forced alignment for per-word timestamps, and speaker diarization to label who is speaking. It then serializes the result. The runtime returns the transcript (segments, words with timestamps, and speaker labels) inline to the client, which must complete within the Amazon SageMaker AI 60-second response cap.
>
> Create the model and endpoint config
>
> Register the WhisperX DLC as a model, where IMAGE_URI points at the WhisperX DLC in Amazon ECR, then create an endpoint config. On every GPU variant, you must set InferenceAmiVersion to al2-ami-sagemaker-inference-gpu-3-1. Without this pin, the endpoint fails to start with a zero-log CannotStartContainerError. Allow a generous startup health-check timeout because the weights load lazily.
>
> sm = boto3.client("sagemaker")
>
> # The WhisperX Deep Learning Container image (Python 3.12, CUDA 12.8, Amazon Linux 2023).
>
> REGION = "us-west-2"
>
> IMAGE_URI = f"763104351884.dkr.ecr.{REGION}.amazonaws.com/whisperx:3.8.6-cu128-amzn2023-sagemaker"
>
> sm.create_model(
>
> ModelName=MODEL_NAME,
>
> PrimaryContainer={"Image": IMAGE_URI}, # WhisperX DLC; large-v2 is the default model
>
> ExecutionRoleArn=ROLE_ARN,
>
> )
>
> sm.create_endpoint_config(
>
> EndpointConfigName=ENDPOINT_CONFIG_NAME,
>
> ProductionVariants=[{
>
> "VariantName": "AllTraffic",
>
> "ModelName": MODEL_NAME,
>
> "InitialInstanceCount": 1,
>
> "InstanceType": "ml.g4dn.xlarge",
>
> "InferenceAmiVersion": "al2-ami-sagemaker-inference-gpu-3-1", # required for CUDA 12.8 DLC
>
> "ContainerStartupHealthCheckTimeoutInSeconds": 900,
>
> }],
>
> )
>
> sm.create_endpoint(EndpointName=ENDPOINT_NAME, EndpointConfigName=ENDPOINT_CONFIG_NAME)
>
> sm.get_waiter("endpoint_in_service").wait(EndpointName=ENDPOINT_NAME)
>
> Invoke with diarization and word timestamps
>
> Build a multipart/form-data body with the audio as the file part and fields such as language=en, diarize=true, and response_format=verbose_json. The response contains segments, per-word timestamps, and speaker labels.
>
> def build_multipart(audio_path, fields):
>
> """Audio as the `file` part + optional string fields, per the WhisperX DLC contract."""
>
> boundary = uuid.uuid4().hex
>
> body = b""
>
> for name, value in fields.items():
>
> body += (f"--{boundary}\r\n"
>
> f'Content-Disposition: form-data; name="{name}"\r\n\r\n'
>
> f"{value}\r\n").encode()
>
> body += (f"--{boundary}\r\n"
>
> f'Content-Disposition: form-data; name="file"; filename="audio.wav"\r\n'
>
> f"Content-Type: audio/wav\r\n\r\n").encode()
>
> body += open(audio_path, "rb").read() + b"\r\n"
>
> body += f"--{boundary}--\r\n".encode()
>
> return body, f"multipart/form-data; boundary={boundary}"
>
> body, content_type = build_multipart("audio.wav", {
>
> "language": "en",
>
> "response_format": "verbose_json",
>
> "timestamp_granularities[]": "word", # word-level timestamps
>
> "diarize": "true", # speaker labels
>
> })
>
> resp = sm_runtime.invoke_endpoint(
>
> EndpointName=ENDPOINT_NAME, ContentType=content_type, Body=body,
>
> )
>
> transcription = json.loads(resp["Body"].read())
>
> The example GitHub repository uses a public-domain recording of the air traffic control (ATC) communications from US Airways Flight 1549, the 2009 “Miracle on the Hudson” emergency landing. It’s a real multi-party radio exchange with background noise, radio compression, and rapid callsign and frequency readouts. Those conditions make it a strong test of transcription accuracy, word-level timestamps, and speaker diarization. The full approximately 3-minute recording is sent to the asynchronous endpoint, and a 40-second segment to the real-time endpoint.
>
> Running this against a 40-second segment of the source audio returns the following diarized, word-timed transcript:
>
> [00:02] SPEAKER_01: Cactus 1549, turn left heading 270.
>
> [00:04] SPEAKER_00: This is Cactus 1539, head first to Placid Crest, I'm hoping it's returning back towards LaGuardia.
>
> [00:11] SPEAKER_01: Okay, you need to return to LaGuardia, turn left heading of 220.
>
> [00:14] SPEAKER_01: 220.
>
> [00:18] SPEAKER_01: Tower, stoppy to park, he's got emergency returning.
>
> [00:22] SPEAKER_01: Who is it?
>
> [00:23] SPEAKER_01: It's 1529, he, uh, bird strike, he lost all engine, he lost the thrust in the engine, so he's returning immediately.
>
> [00:28] SPEAKER_01: Check, it's 1529, which engines?
>
> [00:30] SPEAKER_01: He lost thrust in both engines, he said.
>
> [00:32] SPEAKER_01: Got it.
>
> [00:34] SPEAKER_01: Check, it's 1529, if we can get it for you, do you want to try to land 131.3?
>
> Walkthrough: Asynchronous endpoint
>
> The asynchronous endpoint removes the 60-second cap and is the recommended path for long audio. Input and output are brokered through Amazon S3, and you poll for the result. Figure 2 is a sequence diagram that traces the full asynchronous lifecycle, from the S3 upload and InvokeEndpointAsync call through container processing to the S3 output and failure paths.
>
> Figure 2: Asynchronous endpoint S3 by-reference InvokeEndpointAsync flow, single-worker processing, and results through the S3 output and failure paths
>
> Reading the sequence end to end: the client uploads the multipart body to Amazon S3 and calls InvokeEndpointAsync with the object’s InputLocation. It receives an OutputLocation and FailureLocation immediately rather than waiting for the transcript. Amazon SageMaker AI reads the input from Amazon S3 and forwards it to the container on port 8080. There, the same voice-activity detection, batched transcription, forced-alignment, and diarization pipeline runs, one request per container. On success, the container writes the transcript to the S3 output path, or an error document to the failure path. The client polls the output path for the result and checks the failure path, so a failed job surfaces an error instead of looping indefinitely. Because work is brokered through Amazon S3, this path isn’t bound by the 60-second cap and suits long audio.
>
> Create the asynchronous endpoint config
>
> The only structural difference from the real-time endpoint is the endpoint config: it adds an AsyncInferenceConfig with an S3 OutputPath and S3FailurePath. Set MaxConcurrentInvocationsPerInstance=1 to match the container’s single-worker limit, and keep the same InferenceAmiVersion pin. IMAGE_URI is the same WhisperX DLC used for the real-time endpoint.
>
> # Same WhisperX DLC image as the real-time endpoint.
>
> IMAGE_URI = f"763104351884.dkr.ecr.{REGION}.amazonaws.com/whisperx:3.8.6-cu128-amzn2023-sagemaker"
>
> sm.create_model(
>
> ModelName=ASYNC_MODEL_NAME,
>
> PrimaryContainer={"Image": IMAGE_URI}, # WhisperX DLC
>
> ExecutionRoleArn=ROLE_ARN,
>
> )
>
> sm.create_endpoint_config(
>
> EndpointConfigName=ASYNC_ENDPOINT_CONFIG_NAME,
>
> ProductionVariants=[{
>
> "VariantName": "AllTraffic",
>
> "ModelName": ASYNC_MODEL_NAME,
>
> "InitialInstanceCount": 1,
>
> "InstanceType": "ml.g5.2xlarge",
>
> "InferenceAmiVersion": "al2-ami-sagemaker-inference-gpu-3-1",
>
> "ContainerStartupHealthCheckTimeoutInSeconds": 1200,
>
> }],
>
> AsyncInferenceConfig={
>
> "OutputConfig": {
>
> "S3OutputPath": f"s3://{BUCKET}/whisperx-async/output/",
>
> "S3FailurePath": f"s3://{BUCKET}/whisperx-async/failure/",
>
> },
>
> "ClientConfig": {"MaxConcurrentInvocationsPerInstance": 1}, # 1 request/container
>
> },
>
> )
>
> sm.create_endpoint(EndpointName=ASYNC_ENDPOINT_NAME, EndpointConfigName=ASYNC_ENDPOINT_CONFIG_NAME)
>
> sm.get_waiter("endpoint_in_service").wait(EndpointName=ASYNC_ENDPOINT_NAME)
>
> The rest of the workflow is identical to the real-time walkthrough. Building the multipart/form-data request (the build_multipart helper and transcription fields) is unchanged. You submit it with invoke_endpoint_async by S3 reference instead of invoke_endpoint, then read the transcript from the OutputLocation and check the FailureLocation. Cleanup is also the same.
>
> Submitting the full approximately 3-minute recording to the asynchronous endpoint returns the following transcript (first and last five lines shown):
>
> [00:02] SPEAKER_00: Cactus 1549, turn left heading 270.
>
> [00:04] SPEAKER_01: This is Cactus 1539, head first to Placid Crest, I'm hoping it's returning back towards LaGuardia.
>
> [00:11] SPEAKER_00: Okay, you need to return to LaGuardia, turn left heading of 220.
>
> [00:14] SPEAKER_00: 220.
>
> [00:18] SPEAKER_00: Tower, stoppy to park, he's got emergency returning.
>
> ......
>
> [02:38] SPEAKER_02: 2-1-0, 4718, I think he said he's going in the Hudson.
>
> [02:43] SPEAKER_00: Cactus 1529, Houston.
>
> [02:51] SPEAKER_00: Cactus 1529, if you can, you got runway 29 available at Newark, it'll be 2 o'clock in 7 miles.
>
> [03:01] SPEAKER_00: You can fly 4718, climb and maintain 1-2-thousand.
>
> [03:04] SPEAKER_02: 1-2-thousand, and keep it private, please.
>
> Cleaning up
>
> A GPU endpoint bills continuously until you delete it. When you are done, delete the endpoint, endpoint config, and model for both endpoints, and remove any S3 input and output artifacts you no longer need.
>
> # A GPU endpoint bills until deleted. Delete endpoint -&gt; config -&gt; model for each endpoint.
>
> for name, cfg, model in [
>
> (ENDPOINT_NAME, ENDPOINT_CONFIG_NAME, MODEL_NAME),
>
> (ASYNC_ENDPOINT_NAME, ASYNC_ENDPOINT_CONFIG_NAME, ASYNC_MODEL_NAME),
>
> ]:
>
> sm.delete_endpoint(EndpointName=name)
>
> sm.delete_endpoint_config(EndpointConfigName=cfg)
>
> sm.delete_model(ModelName=model)
>
> Best practices and production considerations
>
> Pin the GPU AMI – Always set InferenceAmiVersion=al2-ami-sagemaker-inference-gpu-3-1 on GPU variants. The default host AMI ships drivers that fail to start this CUDA 12.8 image.
>
> Scale by instances, not concurrency – Inference is serialized to one request per container. Set MaxConcurrentInvocationsPerInstance=1 on asynchronous endpoints and add instances or containers for throughput.
>
> Autoscale asynchronous endpoints to zero – For bursty batch workloads, scale the asynchronous endpoint to zero instances when idle to cut cost, and use Amazon Simple Notification Service (Amazon SNS) completion notifications instead of tight polling.
>
> Right-size the GPU, and use instance pools for availability – Use ml.g4dn.xlarge (T4) for cost or ml.g5.2xlarge (A10G) for headroom. To avoid insufficient-capacity errors, list up to five instance types in an Amazon SageMaker AI instance pool. It provisions the highest-priority type first and falls back automatically when capacity is unavailable.
>
> Secure the S3 artifacts – Turn on S3 Block Public Access, default SSE-S3 or SSE-KMS encryption, and BucketOwnerEnforced ownership on the asynchronous bucket. Scope the execution role to specific buckets and keys.
>
> Handle personally identifiable information (PII) responsibly – Transcripts of calls and meetings might contain sensitive data, so encrypt artifacts, restrict access, and apply redaction downstream using the word-level timestamps.
>
> Observe and retry – Monitor with Amazon CloudWatch, alarm on failures, and retry around the cold-start behavior described earlier. For deeper GPU and inference visibility, turn on the Amazon SageMaker AI detailed metrics and Insights dashboard on CloudWatch.
>
> Conclusion
>
> In this post, we showed how to deploy the AWS WhisperX Deep Learning Container to Amazon SageMaker AI for word-level, speaker-labeled transcription. We used a real-time endpoint for short interactive clips and an asynchronous endpoint for long, high-volume audio. We covered the production details that matter most: the required GPU AMI pin, single-request-per-container scaling, S3 bucket naming, and cost controls.
>
> To go further, explore the WhisperX DLC deployment guide, review Amazon SageMaker AI asynchronous inference, and try the accompanying demo notebook against your own audio. You can also find the full working example in the AWS Samples GitHub repository.
>
> Acknowledgements
>
> The authors thank the AWS Deep Learning Containers and Amazon SageMaker AI teams for their technical review and contributions to the sample.
>
> About the authors
>
> Ayush Sharma
>
> Ayush is a Senior AI Specialist Solutions Architect at AWS, working with ISVs and startups on generative AI. His interests span multi-agent architectures and the design patterns that make autonomous AI systems reliable at scale. He works closely with model deployment, fine-tuning, and cost-efficient inference across the AWS AI/ML stack. He is passionate about turning emerging AI research into practical, real-world systems.
>
> Daniel Wirjo
>
> Daniel is a Solutions Architect at AWS, focused on frontier AI startups. As a former startup CTO, he enjoys collaborating with founders and engineering leaders to drive growth and innovation on AWS. Outside of work, Daniel enjoys taking walks with a coffee in hand, appreciating nature, and learning new ideas.
>
> Dmitry Soldatkin
>
> Dmitry is the Worldwide Leader for Specialist Solutions Architecture, SageMaker Inference at AWS. He helps customers design, build, and optimize generative AI and machine learning solutions, with interests in deep learning and deploying machine learning at scale. He has a passion for continuous innovation and using data to drive business outcomes.
>
> Yadan Wei
>
> Yadan is a Software Development Engineer on the AWS Deep Learning Containers team. He builds containers that package tested framework versions, dependencies, and AWS deployment configuration for Amazon SageMaker AI, Amazon Elastic Compute Cloud (Amazon EC2), Amazon Elastic Container Service (Amazon ECS), and Amazon Elastic Kubernetes Service (Amazon EKS), including the vLLM-Omni DLC used in this post.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。