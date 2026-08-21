---
title: "Introducing cross-Region inference for OpenAI GPT-5.6 models on Amazon Bedrock"
date: 2026-08-21T11:19:00+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "Prompt 工程", "Amazon Bedrock", "Announcements", "博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:611601f30a037b1e6de89eda49fe99da40779f9a75532f5811cd86806925ff1c"
source_payload_sha256: "sha256:5c802ee207234950731dd7cb0b0af62a6e3dcbe3a73ad3c8d7a2f4cd06bdd7cc"
observation_id: obs_5abe1b16819873d13507625a631a8dbc07a0a5c0e586d0f31acf533951b6615b
event_id: evt_d3a70f8ed62ce614150f4140f1681e92422159781d0969628e5e5a73d8f1c5c4
revision_id: rev_6ade1d851bddc5fb51ab2fdd30ca0ebab4db95bdeabb7e59ccfa166197d3c802
source_published_at: 2026-08-20T21:46:03Z
first_seen_at: 2026-08-21T03:16:04.056526Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: true
source_truncation_reason: "crawler_feed_content_limit"
source_support: 1.0
source_title_chars_original: 78
description: "当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。"
external_url: https://aws.amazon.com/blogs/machine-learning/introducing-cross-region-inference-for-openai-gpt-5-6-models-on-amazon-bedrock
parent_observation_id: null
last_seen_at: 2026-08-21T03:16:04.056526Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/introducing-cross-region-inference-for-openai-gpt-5-6-models-on-amazon-bedrock](https://aws.amazon.com/blogs/machine-learning/introducing-cross-region-inference-for-openai-gpt-5-6-models-on-amazon-bedrock)
- **发布域名**: aws.amazon.com

## 来源摘要/节选

> This post is co-written with Chris Dickens from OpenAI.
>
> Amazon Bedrock now offers OpenAI GPT-5.6 models on Amazon Bedrock in more than 25 AWS Regions, with cross-Region inference. Three GPT-5.6 variants support cross-Region inference, Sol, Terra, and Luna, each tuned for a different balance of capability and cost.
>
> Cross-Region inference (CRIS) in Amazon Bedrock works through inference profiles, which define a model and the AWS Regions to which Amazon Bedrock can route a request. You call the profile from a source Region, and Amazon Bedrock routes the request to a destination Region using compute in that Region. CRIS is primarily a capacity mechanism. By allowing requests to draw on a broader pool of compute rather than being bound to one Region’s available capacity, it improves throughput and helps maintain consistent performance under load. A geographic inference profile routes requests within a single geography, so you can scale while keeping data processed within that geography. For GPT-5.6, this launch introduces US geographic (US cross-Region inference) and global CRIS. A global inference profile routes across all supported AWS commercial Regions where the model is deployed, based on real-time capacity, giving you broad access to Amazon Bedrock capacity.
>
> In this post, we walk through an overview of GPT-5.6 models on Amazon Bedrock, how geographic and global cross-Region inference work for these models, and how to call them from the Amazon Bedrock console and in code with the OpenAI Responses API, the OpenAI Chat Completions API, and the Amazon Bedrock Converse API.
>
> GPT-5.6 on Amazon Bedrock
>
> The GPT-5.6 family on Amazon Bedrock includes general-purpose and specialized cyber security variants. This post covers the three general-purpose variants that support cross-Region inference, Sol, Terra, and Luna. All three accept text and image inputs and return text, have a 1 million token context window, and support reasoning mode, server-side tool calling, and prompt caching. You can call them with the OpenAI Responses API, the OpenAI Chat Completions API, and the Amazon Bedrock Converse API. Streaming is supported through the Responses and Chat Completions API (stream=True), and ConverseStream.
>
> Amazon Bedrock inference profiles are logical identifiers you pass instead of a raw model ID.
>
> A geographic inference profile (prefixed with a geography code such as us., for example us.openai.gpt-5.6-terra) keeps inference processing within the Regions of its predefined geography. Requests enter through your source Region and can only be routed to destination Regions inside that geography, so workloads with data residency requirements can scale across Regions while staying within the boundary.
>
> A Global inference profile (prefixed global. such as global.openai.gpt-5.6-terra) can route a request to any supported commercial AWS Region where the model is deployed, based on real-time capacity. It offers the widest capacity pool and is the right choice when your workload has no geographic processing requirements.
>
> Billing and quota consumption are tracked against your account regardless of which backend Region handled the request, so a single spending and throughput picture still applies. Data processed through global CRIS may cross the Regions in that model’s eligible set. If your workload has data residency requirements that restrict processing to specific geographies, use the geographic profile for that geography (such as us.openai.gpt-5.6-terra) or a direct call to one Region instead of the global profile. The Amazon Bedrock cross-Region inference documentation lists which Regions participate in each model’s global and geographic profile sets.
>
> The following tables list the source Regions where you can invoke the GPT-5.6 inference profiles and the destination Regions where your requests can be processed. The same routing applies to all three variants: Sol, Terra, and Luna.
>
> US cross-Region inference profile (us.openai.gpt-5.6-sol / -terra / -luna)
>
> Source Region
>
> Destination Regions
>
> US East (N. Virginia) us-east-1
>
> US East (N. Virginia) us-east-1, US West (Oregon) us-west-2, US East (Ohio) us-east-2
>
> US West (Oregon) us-west-2
>
> US East (N. Virginia) us-east-1, US West (Oregon) us-west-2, US East (Ohio) us-east-2
>
> US East (Ohio) us-east-2
>
> US East (N. Virginia) us-east-1, US West (Oregon) us-west-2, US East (Ohio) us-east-2
>
> US West (N. California) us-west-1
>
> US East (N. Virginia) us-east-1, US West (Oregon) us-west-2, US East (Ohio) us-east-2, US West (N. California) us-west-1
>
> Canada (Central) ca-central-1
>
> US East (N. Virginia) us-east-1, US West (Oregon) us-west-2, US East (Ohio) us-east-2, Canada (Central) ca-central-1
>
> Canada West (Calgary) ca-west-1
>
> US East (N. Virginia) us-east-1, US West (Oregon) us-west-2, US East (Ohio) us-east-2, Canada West (Calgary) ca-west-1
>
> Global cross-Region inference profile (global.openai.gpt-5.6-sol / -terra / -luna)
>
> Source Regions
>
> Destination Regions
>
> United States: US East (N. Virginia) us-east-1, US East (Ohio) us-east-2, US West (Oregon) us-west-2, US West (N. California) us-west-1
>
> Canada: Canada (Central) ca-central-1
>
> Europe: Europe (Stockholm) eu-north-1, Europe (Paris) eu-west-3, Europe (Ireland) eu-west-1, Europe (Frankfurt) eu-central-1, Europe (Spain) eu-south-2, Europe (Milan) eu-south-1, Europe (London) eu-west-2, Europe (Zurich) eu-central-2
>
> Asia Pacific: Asia Pacific (Melbourne) ap-southeast-4, Asia Pacific (Sydney) ap-southeast-2, Asia Pacific (Tokyo) ap-northeast-1, Asia Pacific (Osaka) ap-northeast-3, Asia Pacific (Seoul) ap-northeast-2, Asia Pacific (Mumbai) ap-south-1, Asia Pacific (Hyderabad) ap-south-2, Asia Pacific (Singapore) ap-southeast-1, Asia Pacific (Jakarta) ap-southeast-3, Asia Pacific (Thailand) ap-southeast-7, Asia Pacific (Malaysia) ap-southeast-5, Asia Pacific (Taipei) ap-east-2
>
> Middle East: Middle East (UAE) me-central-1, Israel (Tel Aviv) il-central-1
>
> South America: South America (São Paulo) sa-east-1
>
> Routes to supported AWS commercial Regions globally
>
> Try GPT-5.6 in the Amazon Bedrock console
>
> The quickest way to try GPT-5.6 is the text playground in the Amazon Bedrock console, which requires no coding or SDK setup. You can send prompts, adjust inference parameters, and switch between variants to get a feel for each model before you integrate the API. The model selector lists both the geographic and global cross-Region inference profiles, so you can test either cross-Region inference option before writing code. In the preceding screenshot, the source Region is US East (N. Virginia). The US entry in the model selector is the geographic inference profile, and the Global entry is the global inference profile.
>
> Open the Amazon Bedrock console in a Region where the models are available, such as US East (N. Virginia).
>
> In the navigation pane, under Test, choose Playground.
>
> Choose Select model in the middle of the page.
>
> Search for OpenAI GPT-5.6 Sol, select either US OpenAI GPT-5.6 Sol or Global OpenAI GPT-5.6 Sol, and choose Apply.
>
> Enter a prompt and choose Run to generate a response.
>
> Figure 1: Selecting a US or Global GPT-5.6 inference profile in the Amazon Bedrock console model selector
>
> Getting started with the API
>
> GPT-5.6 speaks the OpenAI Responses API formats natively on Amazon Bedrock. If your application already calls OpenAI models, you can point your existing OpenAI SDK client at the Amazon Bedrock OpenAI-compatible endpoint. Then swap in the inference profile ID (global or geographic) as the model parameter. For authentication, Amazon Bedrock accepts either standard AWS credentials or an Amazon Bedrock API key. The API key path is the most direct fit for the OpenAI SDK, which passes it as the bearer token. For production, generate short-term API keys programmatically using the aws-bedrock-token-generator package, which derives a bearer token from your existing AWS credentials (long-term keys are recommended only for exploration).
>
> from aws_bedrock_token_generator import provide_token
>
> from openai import OpenAI
>
> region = "us-east-1"
>
> # Point the OpenAI SDK at Amazon Bedrock's OpenAI-compatible endpoint for your Region. provide_token() generates a short-term Amazon Bedrock API key from your current AWS credentials (valid up to 12 hours), so no static key needs to be stored.
>
> client = OpenAI(
>
> base_url= f"https://bedrock-runtime.{region}.amazonaws.com/openai/v1",
>
> api_key=provide_token(region=region),
>
> )
>
> # Use the global inference profile ID for GPT-5.6 Terra.
>
> model_id = "global.openai.gpt-5.6-terra"
>
> response = client.responses.create(
>
> model=model_id,
>
> input="Summarize the difference between horizontal and vertical scaling in two sentences.",
>
> max_output_tokens=512,
>
> )
>
> print(response.output_text)
>
> For the full list of supported parameters, see the OpenAI GPT model parameters page in the Amazon Bedrock User Guide. The same client also works with the Chat Completions API, useful if your application already uses this format.
>
> response = client.chat.completions.create(
>
> # For US Geo CRIS, use "us.openai.gpt-5.6-terra".
>
> # Other variants: gpt-5.6-sol, gpt-5.6-luna
>
> model="global.openai.gpt-5.6-terra",
>
> messages=[
>
> {
>
> "role": "user",
>
> "content": "In one sentence, what is cross-Region inference in Amazon Bedrock?",
>
> }
>
> ],
>
> max_completion_tokens=2000,
>
> reasoning_effort="low",
>
> )
>
> print(response.choices[0].message.content)
>
> If you’re calling Amazon Bedrock directly rather than through the OpenAI SDK, use the Amazon Bedrock Converse API, which gives you the same request shape you already use for other models on Bedrock:
>
> import boto3
>
> client = boto3.client("bedrock-runtime", region_name="us-east-1")
>
> model_id = "global.openai.gpt-5.6-terra"
>
> response = client.converse(
>
> modelId=model_id,
>
> messages=[{"role": "user", "content": [{"text": "List three common uses for a message queue."}]}],
>
> inferenceConfig={"maxTokens": 512},
>
> )
>
> print(response["output"]["message"]["content"][0]["text"])
>
> For streaming responses, call converse_stream with the same arguments and iterate over the event stream:
>
> stream_response = client.converse_stream(
>
> modelId=model_id,
>
> messages=[{"role": "user", "content": [{"text": "List three common uses for a message queue."}]}],
>
> inferenceConfig={"maxTokens": 512},
>
> )
>
> for event in stream_response["stream"]:
>
> if "contentBlockDelta" in event:
>
> print(event["contentBlockDelta"]["delta"]["text"], end="")
>
> Security and compliance
>
> Cross-Region inference uses the same Amazon Bedrock security model as direct in-Region calls. Requests are authenticated with your AWS Identity and Access Management (IAM) credentials, and IAM policies control which inference profiles a role can invoke. Amazon Bedrock uses a zero-operator access (ZOA) security model enforced at the chip, so no AWS operators can access your prompts or completions. Every model call runs under your IAM policies, can be reached privately from your virtual private cloud (VPC) through a VPC endpoint, and is logged on AWS CloudTrail. Data perimeter policies help prevent exfiltration across account and network boundaries.
>
> For certain models, including GPT-5.6, content flagged by the Amazon Bedrock automated abuse-detection classifiers is retained for up to 30 days for offline abuse detection. To see which models this applies to and how it works, see Abuse detection in the Amazon Bedrock User Guide. To understand more about data retention configuration on Bedrock, see the Amazon Bedrock data retention documentation. For the authoritative list of Regions in each profile’s routing set, see the Amazon Bedrock cross-Region inference support page.
>
> Cross-Region inference requests appear on AWS CloudTrail in your source Region, and the additionalEventData.inferenceRegion field records which Region processed each request. If you enable model invocation logging, the request and response payloads are delivered to Amazon Simple Storage Service (Amazon S3) or Amazon CloudWatch Logs in the same account and Region.
>
> Setting up IAM permissions for cross-Region inference
>
> To let a role invoke GPT-5.6 through an inference profile, grant it access to the inference profile and to the foundation model in every Region the profile can route to. You can use this managed policy AmazonBedrockLimitedAccess or create your own.
>
> For a geographic inference profile, the policy has three statements. The first grants access to the geographic inference profile and the default project in your source Region. The second grants access to the foundation model in your source Region and in every destination Region in the geography, with a condition that limits this access to requests made through that profile. The third grants the bearer-token authentication the OpenAI-compatible APIs use.
>
> {
>
> "Version": "2012-10-17",
>
> "Statement": [
>
> {
>
> "Sid": "GrantGeoCrisProfileAndProjectAccess",
>
> "Effect": "Allow",
>
> "Action": ["bedrock:InvokeModel"],
>
> "Resource": [
>
> "arn:aws:bedrock:&lt;SOURCE REGION&gt;:&lt;ACCOUNT&gt;:inference-profile/us.openai.gpt-5.6-terra",
>
> "arn:aws:bedrock:&lt;SOURCE REGION&gt;:&lt;ACCOUNT&gt;:project/default"
>
> ]
>
> },
>
> {
>
> "Sid": "GrantGeoCrisDestinationModelAccess",
>
> "Effect": "Allow",
>
> "Action": ["bedrock:InvokeModel"],
>
> "Resource": [
>
> "arn:aws:bedrock:us-east-1::foundation-model/openai.gpt-5.6-terra",
>
> "arn:aws:bedrock:us-east-2::foundation-model/openai.gpt-5.6-terra",
>
> "arn:aws:bedrock:us-west-2::foundation-model/openai.gpt-5.6-terra"
>
> ],
>
> "Condition": {
>
> "StringLike": {
>
> "bedrock:InferenceProfileArn": "arn:aws:bedrock:&lt;SOURCE REGION&gt;:&lt;ACCOUNT&gt;:inference-profile/us.openai.gpt-5.6-terra"
>
> }
>
> }
>
> },
>
> {
>
> "Sid": "AllowBearerTokenAuth",
>
> "Effect": "Allow",
>
> "Action": ["bedrock:CallWithBearerToken"],
>
> "Resource": "*"
>
> }
>
> ]
>
> }
>
> A global inference profile uses a four-part policy. The first grants access to the global inference profile and the default project in your source Region. The second grants access to the foundation model in your source Region. The third grants access to the foundation model through the Region-agnostic global ARN, which is what enables cross-Region routing. The fourth grants the bearer-token authentication used by the OpenAI-compatible APIs.
>
> {
>
> "Version": "2012-10-17",
>
> "Statement": [
>
> {
>
> "Sid": "GrantGlobalCrisProfileAndProjectAccess",
>
> "Effect": "Allow",
>
> "Action": ["bedrock:InvokeModel"],
>
> "Resource": [
>
> "arn:aws:bedrock:&lt;REQUESTING REGION&gt;:&lt;ACCOUNT&gt;:inference-profile/global.openai.gpt-5.6-terra",
>
> "arn:aws:bedrock:&lt;REQUESTING REGION&gt;:&lt;ACCOUNT&gt;:project/default"
>
> ],
>
> "Condition": {
>
> "StringEquals": { "aws:RequestedRegion": "&lt;REQUESTING REGION&gt;" }
>
> }
>
> },
>
> {
>
> "Sid": "GrantGlobalCrisInRegionModelAccess",
>
> "Effect": "Allow",
>
> "Action": ["bedrock:InvokeModel"],
>
> "Resource": ["arn:aws:bedrock:&lt;REQUESTING REGION&gt;::foundation-model/openai.gpt-5.6-terra"],
>
> "Condition": {
>
> "StringEquals": {
>
> "aws:RequestedRegion": "&lt;REQUESTING REGION&gt;",
>
> "bedrock:InferenceProfileArn": "arn:aws:bedrock:&lt;REQUESTING REGION&gt;:&lt;ACCOUNT&gt;:inference-profile/global.openai.gpt-5.6-terra"
>
> }
>
> }
>
> },
>
> {
>
> "Sid": "GrantGlobalCrisGlobalModelAccess",
>
> "Effect": "Allow",
>
> "Action": ["bedrock:InvokeModel"],
>
> "Resource": ["arn:aws:bedrock:::foundation-model/openai.gpt-5.6-terra"],
>
> "Condition": {
>
> "StringEquals": {
>
> "aws:RequestedRegion": "unspecified",
>
> "bedrock:InferenceProfileArn": "arn:aws:bedrock:&lt;REQUESTING REGION&gt;:&lt;ACCOUNT&gt;:inference-profile/global.openai.gpt-5.6-terra"
>
> }
>
> }
>
> },
>
> {
>
> "Sid": "AllowBearerTokenAuth",
>
> "Effect": "Allow",
>
> "Action": ["bedrock:CallWithBearerToken"],
>
> "Resource": "*"
>
> }
>
> ]
>
> }
>
> These policies grant bedrock:CallWithBearerToken and bedrock:InvokeModel on the project/default resource, which the OpenAI Responses and Chat Completions APIs use to authenticate with an Amazon Bedrock API key and run inference. If you use the streaming Converse API (ConverseStream), add bedrock:InvokeModelWithResponseStream to the inference-profile and foundation-model statements.
>
> The statements work together, so removing one denies that profile’s cross-Region access for the role, which also gives you a clean way to turn either capability off for specific roles. Alternatively, you can attach an explicit deny that targets global. or us. inference profiles.
>
> Service control policy consideration for global cross-Region inference
>
> If your organization uses Region-restrictive service control policies (SCPs), Global CRIS requests set aws:RequestedRegion to unspecified rather than a specific Region name. Geographic CRIS requests are evaluated against every destination Region in the profile. The recommended approach is to exempt cross-Region inference with the bedrock:InferenceProfileArn condition rather than widening your Region allowlist. Amazon Bedrock sets that condition key when it authorizes the foundation model, so you can allow CRIS routing while keeping your allowlist tight for every other service. Your source Region still has to be in the allowlist. If you prefer not to use the condition, you can instead add the destination Regions and unspecified to your allowlist, but that opens those Regions to every service, not only Amazon Bedrock. For a ready-to-use SCP and step-by-step guidance, see the Bedrock CRIS Region-control SCP sample.
>
> The following SCP denies Amazon Bedrock inference outside your approved Regions (Sydney and N. Virginia are shown) and exempts the us. and global. inference profiles that GPT-5.6 uses. The first statement keeps the Region allowlist enforced for every other service, so include the global services your organization uses in its NotAction list.
>
> {
>
> "Version": "2012-10-17",
>
> "Statement": [
>
> {
>
> "Sid": "DenyOutsideApprovedRegionsExceptBedrockInvoke",
>
> "Effect": "Deny",
>
> "NotAction": [
>
> "iam:*", "sts:*", "organizations:*", "account:*",
>
> "route53:*", "cloudfront:*", "waf:*", "wafv2:*", "shield:*",
>
> "support:*", "trustedadvisor:*", "health:*",
>
> "budgets:*", "ce:*", "cur:*", "tax:*", "billing:*",
>
> "bedrock:Invoke*"
>
> ],
>
> "Resource": "*",
>
> "Condition": {
>
> "StringNotEquals": { "aws:RequestedRegion": ["ap-southeast-2", "us-east-1"] }
>
> }
>
> },
>
> {
>
> "Sid": "DenyBedrockInferenceOutsideApprovedRegionsUnlessCris",
>
> "Effect": "Deny",
>
> "Action": [
>
> "bedrock:Invoke*"
>
> ],
>
> "Resource": "*",
>
> "Condition": {
>
> "StringNotEquals": { "aws:RequestedRegion": ["ap-southeast-2", "us-east-1"] },
>
> "ArnNotLike": {
>
> "bedrock:InferenceProfileArn": [
>
> "arn:aws:bedrock:*:*:inference-profile/us.*",
>
> "arn:aws:bedrock:*:*:inference-profile/global.*"
>
> ]
>
> }
>
> }
>
> }
>
> ]
>
> }
>
> Model access must be enabled for the account and Region for both profile types. For the full checklist, see Prerequisites for inference profiles.
>
> Working with prompt caching
>
> All three GPT-5.6 variants support prompt caching on the bedrock-runtime endpoint. When your requests share a long prompt prefix, such as a system prompt or a set of few-shot examples, Amazon Bedrock caches that prefix. Later requests reuse the cached prefix instead of reprocessing it. This lowers input cost and latency for the cached portion.
>
> GPT-5.6 supports two caching modes on Amazon Bedrock. Implicit caching is the default: the service places a cache breakpoint at the latest user or tool message, which suits conversations that grow by appending messages. If your requests share a stable prefix followed by content that changes on every request, you can mark the end of the stable content with an explicit cache breakpoint instead. In both modes, pass the optional prompt_cache_key parameter so requests with the same prefix are routed to the same cache. Both modes work with geographic and global inference profiles. Each cache breakpoint needs a prompt prefix of at least 1,024 tokens. For more information, see Prompt caching for faster model inference.
>
> Prompt caching also affects quota usage. Cache read tokens are not counted toward your TPM quota, so requests that reuse a cached prefix consume less of it. The next section describes how quotas are calculated. The following example uses explicit prompt caching with the client and model_id from the Getting started section:
>
> # support_policy_manual is a long, stable prefix shared across requests.
>
> # The breakpoint marks the end of the stable content; the user question
>
> # after it changes on every request without invalidating the cached prefix.
>
> completion = client.chat.completions.create(
>
> model=model_id,
>
> messages=[
>
> {
>
> "role": "system",
>
> "content": [
>
> {
>
> "type": "text",
>
> "text": support_policy_manual,
>
> "prompt_cache_breakpoint": {"mode": "explicit"},
>
> }
>
> ],
>
> },
>
> {"role": "user", "content": "A customer wants a refund for a damaged laptop. What must I verify first?"},
>
> ],
>
> max_completion_tokens=300,
>
> prompt_cache_key="support-policy-v1",
>
> )
>
> To confirm that caching is working, check the usage object of each response.
>
> details = completion.usage.prompt_tokens_details
>
> print("Cached tokens:", details.cached_tokens)
>
> print("Written tokens:", details.cache_write_tokens)
>
> Quota management
>
> On-demand quotas for GPT-5.6 are managed as tokens per minute (TPM), and they attach to the inference profile you call: a geographic profile and a global profile for the same model carry separate quota allocations, so switching between them changes the pool you draw from. To view your current allocations or request an increase, search for the GPT-5.6 model inference quotas in the AWS Service Quotas console from the Region your application calls Amazon Bedrock in.
>
> When you size a quota increase request, account for the burndown rate: the rate at which input and output tokens convert into token quota usage for the throttling system. Input tokens count against your quota at 1:1, while output tokens can consume quota at a higher multiple. For GPT-5.6 models, the burndown rate is 10x for output tokens, meaning one output token consumes 10 tokens from your TPM quota, so output-heavy workloads use up quota considerably faster than raw token counts suggest. The per-request calculation is:
>
> Input token count + Cache write input tokens + (Output token count x Burndown rate)
>
> For example, a request with 2,000 input tokens and 1,000 output tokens depletes 12,000 tokens from your quota. Cache read tokens are not part of this calculation, which is what makes prompt caching (previous section) effective for quota management and cost. For the current burndown rates by model, see the Amazon Bedrock quotas page. Three practices help you avoid surprises:
>
> Request increases before deployment. If you anticipate high usage, request the increase through the Service Quotas console ahead of your launch rather than reacting to throttling in production.
>
> Monitor utilization. Amazon CloudWatch publishes quota utilization metrics in real time per inference profile, so you can set alerts when usage approaches thresholds and track historical patterns to plan future increases.
>
> Load test with realistic traffic (including peak patterns and production-size prompts) before you commit a workload to production, and validate against the profile type you will actually use, since geographic and global quotas are separate.
>
> Monitoring and logging
>
> Because GPT-5.6 requests run through the Bedrock Runtime API, requests made through a geographic or global inference profile appear in Amazon Bedrock model invocation logging the same way on-demand requests do, with the inference profile ARN recorded alongside the request and response payloads (subject to your logging configuration). You can deliver invocation logs to Amazon S3 or Amazon CloudWatch Logs. Whichever profile type you use, invocation logs and metrics are recorded in your source Region, so your observability stays in one place even when the request is processed elsewhere.
>
> Amazon CloudWatch metrics covering invocation counts, token counts, latency, throttles, and errors are published per inference profile. Because geographic and global profiles are distinct resources, their metrics are reported separately. Per-request latency will vary somewhat with the destination Region a request lands in, so if your dashboards break metrics down by Region today, consider adding a view that aggregates by inference profile ID instead, since that is the ID your application code and quota consumption are tied to. Usage is also itemized on AWS Cost Explorer and the AWS Cost and Usage Report, so you can attribute GPT-5.6 spend by model and by profile the same way you do for the rest of your Bedrock workloads.
>
> Conclusion
>
> GPT-5.6 brings three OpenAI model variants to Amazon Bedrock. With this launch you can call each of them through two kinds of cross-Region inference profiles. You can use a geographic profile when inference processing needs to stay within a geography (

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。