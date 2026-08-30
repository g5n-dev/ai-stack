---
title: "Introducing OpenAI models on Amazon Bedrock for in-country inferencing in India"
date: 2026-08-30T14:43:08+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "RAG", "AI Agent", "生成式 AI", "Prompt 工程", "Amazon Bedrock", "Announcements", "Intermediate (200)"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:675ee1fb5ac738cb5cae1a4e9fe21a95b301a82f4a3b9d4366a98e6a209892f0"
source_payload_sha256: "sha256:b32c8a0cf7aca17c45214d242c242ee8e6c30de65246ee491c91e5d8875a1425"
observation_id: obs_e991f28971b78ffc4b870f48aedb48451906a0883992dfde8367c738a304e26f
event_id: evt_c144f90edb18ea51627cac0e95a021d6ea3cfb2f404006cd87ef3853caa380aa
revision_id: rev_2aab9aa200b65fa1d75349001640f0de419754cb55234d4eae7f71bd85e90114
source_published_at: 2026-08-27T18:36:08Z
first_seen_at: 2026-08-30T06:39:43.983138Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 79
interpretation_sha256: "sha256:a4db7003df4b360e7baea5f498b0a29cc6752a96b9b8428c84b82d155280b96e"
description: "Amazon Bedrock 在印度上线 OpenAI 系列模型，提供仅在境内流转的跨区域推理能力，支持长上下文和多模态输入。"
external_url: https://aws.amazon.com/blogs/machine-learning/introducing-openai-models-on-amazon-bedrock-for-in-country-inferencing-in-india
parent_observation_id: null
last_seen_at: 2026-08-30T06:39:43.983138Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/introducing-openai-models-on-amazon-bedrock-for-in-country-inferencing-in-india](https://aws.amazon.com/blogs/machine-learning/introducing-openai-models-on-amazon-bedrock-for-in-country-inferencing-in-india)
- **发布域名**: aws.amazon.com

## 要点解读

### 这是什么
Amazon Bedrock 在印度上线 OpenAI 系列模型，提供仅在境内流转的跨区域推理能力，支持长上下文和多模态输入。

### 用在哪里
适用于需要在印度本土处理敏感数据、满足当地监管要求的企业和开发者，尤其是金融、医疗和公共部门等场景。

### 可以推断的
推测：在印度境内进行模型推理可以降低因数据跨境而产生的合规风险。  
推测：大规模长文本或图文混合任务可以一次性在单次请求中完成，提高处理效率。

## 来源摘要/节选

> Amazon Bedrock now supports the OpenAI GPT-5.6 models, Terra and Luna, in India, with India geographic cross-Region inference. If you have local data processing requirements in India, including in financial services, healthcare, and the public sector, you can now use these OpenAI models at scale. Amazon Bedrock processes inference requests and data within India.
>
> Both models offer a 1-million-token context window, accept text and image input, and produce text output. Your applications can process long documents, large code bases, and mixed text-and-image workloads in a single request. The processing never leaves the country.
>
> In this post, we walk through how India geographic cross-Region inference works from the Mumbai and Hyderabad Regions. We also show how to get started from the Amazon Bedrock console and with code, using the OpenAI Responses API, OpenAI Chat Completions API, and the Amazon Bedrock Converse API.
>
> India geographic cross-Region inference
>
> Cross-Region inference automatically routes inference requests across multiple AWS Regions to help improve throughput, without you having to manage capacity in each Region yourself. It’s primarily a capacity mechanism. Instead of being bound to one Region’s capacity, your requests draw on a broader pool of compute. That helps you maintain throughput and consistent performance under load, which matters most during traffic peaks.
>
> With India geographic cross-Region inference, Amazon Bedrock routes requests only within the India geography across Regions such as Asia Pacific (Mumbai) Region (ap-south-1) and Asia Pacific (Hyderabad) Region (ap-south-2). You can scale to meet demand while keeping data processed within India to meet data residency requirements. You call the profile from either India Region as the source, and Amazon Bedrock routes the request to the destination India Region based on capacity. For the most current information about model availability in each Region, see Regional availability by models in the Amazon Bedrock User Guide.
>
> Cross-Region inference works through inference profiles. You call a profile ID as the model, and it defines the model and the AWS Regions Amazon Bedrock can route your request to. The India geographic inference profiles keep that routing within India. There are two profiles:
>
> in.openai.gpt-5.6-terra for GPT-5.6 Terra.
>
> in.openai.gpt-5.6-luna for GPT-5.6 Luna.
>
> With inference profiles, billing and quota consumption are tracked against your account in the source Region, regardless of which backend Region handled the request. Amazon CloudWatch and AWS CloudTrail record log entries in the source Region only, so your monitoring stays in one place.
>
> Choosing between Amazon Bedrock Mantle and Runtime endpoints
>
> For new applications, we recommend the bedrock-runtime endpoint. It supports the Bedrock-native InvokeModel and Converse APIs, the OpenAI-compatible Responses and Chat Completions APIs, and the Anthropic Messages API, and it is where Amazon Bedrock features such as Guardrails, intelligent prompt routing, and cross-Region inference are available.
>
> Data residency
>
> The India geographic profile keeps inference within India. Requests route only between ap-south-1 and ap-south-2. Your input prompts and output results might move between those two Regions. Data is encrypted in transit across the Amazon network. Amazon Bedrock uses a zero data retention (ZDR) data security model. This means that by default, Amazon Bedrock does not store model inputs or outputs. However, for certain models, including GPT-5.6, content flagged by the Amazon Bedrock automated abuse-detection classifiers is retained for offline abuse detection. Please see Abuse detection in the Amazon Bedrock User Guide for more details.
>
> Global cross-Region inference
>
> Amazon Bedrock also offers global cross-Region inference and global inference profiles (prefixed global.) in India that route to supported commercial AWS Regions worldwide for maximum capacity. You send your request to the India Region endpoint, either Asia Pacific (Mumbai) ap-south-1 or Asia Pacific (Hyderabad) ap-south-2, using the global profile ID as the model ID. Amazon Bedrock then decides which destination Region serves the request. Global cross-Region inference supports OpenAI GPT-5.6 models, including Sol, Terra, and Luna. However, if your workload has local data processing requirements, use the India (prefixed in.) profiles instead, because they keep inference within the country. To read more about global cross-Region inference, see Introduce cross-Region inference for OpenAI GPT-5.6 models on Amazon Bedrock.
>
> Access GPT-5.6 models from the Amazon Bedrock console
>
> You can try GPT-5.6 in the text playground in the Amazon Bedrock console, which requires no coding or SDK setup. You can send prompts, adjust inference parameters, and switch between variants to get a feel for each model before you integrate the API.
>
> Open the Amazon Bedrock console in a Region where the models are available, such as Asia Pacific (Mumbai) ap-south-1.
>
> In the navigation pane, under Test, choose Playground.
>
> Choose Select model in the middle of the page.
>
> Search for OpenAI GPT-5.6 Terra, select IN OpenAI GPT-5.6 Terra, and choose Apply.
>
> Enter a prompt and choose Run to generate a response.
>
> Figure 1: The OpenAI GPT-5.6 Terra model selected in the Amazon Bedrock console playground
>
> Call GPT-5.6 models with the OpenAI Responses API
>
> GPT-5.6 models on Amazon Bedrock natively support the OpenAI Responses API format. If your application already calls OpenAI models, you can point your existing OpenAI SDK client at the Amazon Bedrock endpoint in either India Region, Mumbai or Hyderabad, and pass an India geographic inference profile ID as the model parameter.
>
> For authentication, Amazon Bedrock accepts either standard AWS credentials or an Amazon Bedrock API key. The API key path is the straightforward fit for the OpenAI SDK, which passes it as the bearer token. For production, generate short-term API keys programmatically with the aws-bedrock-token-generator package. It derives a bearer token from your existing AWS credentials, so no static key needs to be stored.
>
> The following example uses Asia Pacific (Mumbai) ap-south-1 endpoint and India geographic inference profile ID to call OpenAI GPT-5.6 Terra on Amazon Bedrock.
>
> from aws_bedrock_token_generator import provide_token
>
> from openai import OpenAI
>
> # Point the OpenAI SDK at the Amazon Bedrock OpenAI-compatible
>
> # endpoint in the Asia Pacific (Mumbai) Region.
>
> client = OpenAI(
>
> base_url="https://bedrock-runtime.ap-south-1.amazonaws.com/openai/v1",
>
> api_key=provide_token(region="ap-south-1"), # short-term Amazon Bedrock API key, valid up to 12 hours
>
> )
>
> # Geographic (India) inference profile ID for GPT-5.6 Terra.
>
> model_id = "in.openai.gpt-5.6-terra" # "in.openai.gpt-5.6-luna" for luna
>
> response = client.responses.create(
>
> model=model_id,
>
> input="Extract the payment due date and total amount from the invoice text that follows, and return them as JSON. &lt;invoice text&gt;",
>
> max_output_tokens=512,
>
> )
>
> print(response.output_text)
>
> The Responses API uses a single input field and returns the generated text in output_text, with the output limit set through max_output_tokens. The same client also works with the Chat Completions API, useful if your application already uses this format.
>
> Controlling reasoning depth
>
> To control reasoning depth, set the optional reasoning parameter, for example reasoning={"effort": "low"}. GPT-5.6 models on Amazon Bedrock support the following reasoning effort levels: none, low, medium, high, xhigh, and max. For more information, see the related post Get started with OpenAI GPT-5.6 Sol, Terra, and Luna on Amazon Bedrock. Omitting the parameter uses the model default.
>
> response = client.responses.create(
>
> model="in.openai.gpt-5.6-terra",
>
> input="Extract the payment due date and total amount from the invoice text that follows, and return them as JSON. &lt;invoice text&gt;",
>
> reasoning={"effort": "high"}, # none | low | medium | high | xhigh | max
>
> max_output_tokens=512,
>
> )
>
> For the full list of supported parameters, see the OpenAI model documentation in the Amazon Bedrock User Guide.
>
> Multi-turn conversations with server-side state
>
> Set store=True to have Amazon Bedrock retain the response server-side, then reference it on the next turn with previous_response_id. You send only the new turn. You don’t resend the prior conversation history.
>
> first = client.responses.create(
>
> model="in.openai.gpt-5.6-terra",
>
> input="Remember this: my favorite number is 42. Reply with just 'stored'..",
>
> max_output_tokens=50,
>
> store=True,
>
> )
>
> second = client.responses.create(
>
> model="in.openai.gpt-5.6-terra",
>
> previous_response_id=first.id, # the model recalls the earlier turn
>
> input="what is my favourite number?",
>
> max_output_tokens=50,
>
> store=True,
>
> )
>
> print(second.output_text)
>
> If you chain with previous_response_id, the response you chain from must have been created with store=True. Chaining from an unstored response returns an error.
>
> Streaming responses
>
> For streaming, set stream=True and iterate over the events:
>
> stream = client.responses.create(
>
> model="in.openai.gpt-5.6-terra",
>
> input="Draft a short status update for a delayed shipment, in a polite and direct tone.",
>
> max_output_tokens=512,
>
> stream=True,
>
> )
>
> for event in stream:
>
> if event.type == "response.output_text.delta":
>
> print(event.delta, end="")
>
> Call GPT-5.6 models with the Converse API
>
> If you prefer the AWS SDK and SigV4 authentication over an API key, the Amazon Bedrock Converse API supports GPT-5.6 models with the same unified interface it provides for other models on Amazon Bedrock. ConverseStream covers the streaming case.
>
> import boto3
>
> # Standard AWS credentials (SigV4), no API key needed.
>
> client = boto3.client("bedrock-runtime", region_name="ap-south-1")
>
> model_id = "in.openai.gpt-5.6-terra" # India Geo inference profile
>
> response = client.converse(
>
> modelId=model_id,
>
> messages=[
>
> {
>
> "role": "user",
>
> "content": [{"text": "Classify this support ticket as billing, technical, or account: &lt;ticket text&gt;"}],
>
> }
>
> ],
>
> inferenceConfig={"maxTokens": 512},
>
> )
>
> print(response["output"]["message"]["content"]
>
> Prompt caching
>
> Your prompts might share a long, stable prefix, such as a system instruction, a knowledge base excerpt, or a set of few-shot examples. When they do, GPT-5.6 models on Amazon Bedrock support prompt caching. Cached reads are billed at a 90 percent discount compared to uncached input tokens. This adds up quickly for Retrieval Augmented Generation (RAG) and agent workloads that repeat the same context across many turns. You can find details on Amazon Bedrock prompt caching documentation.
>
> Prompt caching works with the India geographic inference profiles, so you keep the savings under the India data-residency boundary. Prompt caching runs in two modes, explicit and implicit. With implicit caching, Amazon Bedrock places the cache breakpoints for you automatically. Note that the minimum prefix length is 1,024 tokens. With explicit caching, you mark the cache boundary yourself for precise control, and the cached prefix stays warm for at least 30 minutes.
>
> response = client.responses.create(
>
> model="in.openai.gpt-5.6-terra",
>
> prompt_cache_key="ticket-agent-ver123", # same key across all requests
>
> input=[
>
> {
>
> "type": "message",
>
> "role": "developer",
>
> "content": [{
>
> "type": "input_text",
>
> "text": SYSTEM_INSTRUCTIONS, # long, static: guidelines, KB excerpts (&gt;= 1,024 tokens)
>
> "prompt_cache_breakpoint": {"mode": "explicit"},
>
> }],
>
> },
>
> {
>
> "type": "message",
>
> "role": "user",
>
> "content": [{
>
> "type": "input_text",
>
> "text": user_question, # changes on every request
>
> }],
>
> },
>
> ],
>
> extra_body={"prompt_cache_options": {"mode": "explicit"&#125;&#125;,
>
> )
>
> Every response tells you what the cache did, in usage.input_tokens_details:
>
> details = response.usage.input_tokens_details
>
> print(f"cached: {details.cached_tokens}, written: {details.cache_write_tokens}")
>
> On the first call, you will see cache_write_tokens populated as the prefix is stored. On subsequent calls, the same tokens come back as cached_tokens, billed at the cache-read rate. Because these counts are part of input_tokens rather than added on top, a cached token is counted and charged once.
>
> IAM permissions for India geographic cross-Region inference
>
> To allow an AWS Identity and Access Management (IAM) role to invoke GPT-5.6 models through the India geographic inference profile, grant the role access to three resources. These are the India geographic inference profile itself, the foundation model (FM) in the source Region, and the foundation model in each destination Region listed in the profile (ap-south-1 and ap-south-2). You can use the AmazonBedrockLimitedAccess managed policy or create your own.
>
> The following example grants permission to use the GPT-5.6 Terra model through the India geographic inference profile. The source Region is ap-south-1, and the destination Regions are ap-south-1 and ap-south-2. Replace &lt;ACCOUNT&gt; with your account ID, and duplicate the resources for in.openai.gpt-5.6-luna if the role needs both models. If you source from Hyderabad, use the ap-south-2 inference-profile ARN in the first statement. The foundation-model resources in the second statement stay the same, because they already list both India Regions.
>
> {
>
> "Version": "2012-10-17",
>
> "Statement": [
>
> {
>
> "Sid": "GrantGeoCrisInferenceProfileAccess",
>
> "Effect": "Allow",
>
> "Action": [
>
> "bedrock:InvokeModel*"
>
> ],
>
> "Resource": [
>
> "arn:aws:bedrock:ap-south-1:&lt;ACCOUNT&gt;:inference-profile/in.openai.gpt-5.6-terra",
>
> "arn:aws:bedrock:ap-south-1:&lt;ACCOUNT&gt;:project/default"
>
> ]
>
> },
>
> {
>
> "Sid": "GrantGeoCrisModelAccess",
>
> "Effect": "Allow",
>
> "Action": [
>
> "bedrock:InvokeModel*"
>
> ],
>
> "Resource": [
>
> "arn:aws:bedrock:ap-south-1::foundation-model/openai.gpt-5.6-terra",
>
> "arn:aws:bedrock:ap-south-2::foundation-model/openai.gpt-5.6-terra"
>
> ],
>
> "Condition": {
>
> "StringEquals": {
>
> "bedrock:InferenceProfileArn": "arn:aws:bedrock:ap-south-1:&lt;ACCOUNT&gt;:inference-profile/in.openai.gpt-5.6-terra"
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
> The first statement grants access to the India geographic inference profile for requests originating from the source Region. The second grants access to the foundation model in the source Region and in every destination Region listed in the profile. This access is scoped to that one profile through the bedrock:InferenceProfileArn condition. These policies grant bedrock:CallWithBearerToken and bedrock:InvokeModel on the project/default resource. The OpenAI Responses and Chat Completions APIs use this resource to authenticate with an Amazon Bedrock API key and run inference.
>
> Service Control Policy (SCP)
>
> If your organization uses Service Control Policies to block unused Regions, your Region-specific SCP conditions must allow every destination Region listed in the geographic inference profile.
>
> For the India geographic inference profile, both ap-south-1 and ap-south-2 must be permitted. Blocking either destination Region causes cross-Region inference to fail even though the source Region remains accessible.
>
> Setting up Codex with GPT-5.6 on Amazon Bedrock
>
> Codex can use the geographic inference profiles through Amazon Bedrock Runtime. Install the latest Codex CLI (codex-cli 0.149.1 or later) to use the Amazon Bedrock Runtime model provider. For organizations whose identity provider is Okta, Auth0, Microsoft Entra ID, Amazon Cognito, or AWS IAM Identity Center, the AWS OIDC Auth Helper repository provides a sample credential helper.
>
> First, follow the guide to configure your identity provider, the corresponding AWS federation resource, and an IAM role carrying the Bedrock permissions shown earlier. Then add a named profile to ~/.aws/config, so the helper does not replace credentials resolved by the default profile.
>
> [profile &lt;AWS_OIDC_PROFILE&gt;]
>
> credential_process = &lt;ABSOLUTE_PATH_TO_CREDENTIAL_PROCESS&gt; --profile &lt;OIDC_HELPER_PROFILE&gt;
>
> region = ap-south-1
>
> output = json
>
> This federation helper exchanges an OIDC token for temporary AWS credentials, and Codex reads through the standard AWS credential chain with no further configuration. Next, create or update ~/.codex/config.toml and reference the AWS profile, see the Codex configuration reference for other supported settings:
>
> model = "in.openai.gpt-5.6-terra"
>
> model_provider = "amazon-bedrock-runtime"
>
> model_reasoning_effort = "high"
>
> [model_providers.amazon-bedrock-runtime.aws]
>
> profile = "&lt;AWS_OIDC_PROFILE&gt;"
>
> region = "ap-south-1"
>
> If the helper does not have a valid cached session, it opens the configured sign-in page in your browser. After you authenticate, the helper returns temporary AWS credentials through credential_process. Requests are signed with AWS SigV4. When the profile is backed by AWS IAM Identity Center, the credentials are already short-term and rotate with the SSO session. To use this in the Asia Pacific (Hyderabad) Region, set the Region to ap-south-2 in the AWS profile and Codex configuration.
>
> If you already have AWS credentials configured locally, Codex can use them directly. Point the Amazon Bedrock Runtime provider at an AWS profile and an India Region, and set the model to an India geographic inference profile ID.
>
> Create or update ~/.codex/config.toml:
>
> model = "in.openai.gpt-5.6-terra"
>
> model_provider = "amazon-bedrock-runtime"
>
> model_reasoning_effort = "high"
>
> [model_providers.amazon-bedrock-runtime.aws]
>
> profile = "default"
>
> region = "ap-south-1"
>
> The profile value is any profile in ~/.aws/config or ~/.aws/credentials. In this case, it is shown as “default”, but you can use your own named profile if you keep multiple accounts.
>
> Monitoring and logging
>
> The India geographic inference profiles work with the same account-level controls you already use for other models on Amazon Bedrock. Requests appear in Amazon Bedrock model invocation logging the same way on-demand requests do. You can deliver those logs to Amazon Simple Storage Service (Amazon S3) or Amazon CloudWatch Logs. CloudWatch metrics for invocation count, token count, latency, throttles, and errors are published per inference profile. You can track GPT-5.6 models usage from Mumbai or Hyderabad without correlating logs across Regions yourself.
>
> To see which destination Region processed a given request, CloudTrail events include an additionalEventData field with an inferenceRegion key. For the India profile, this is always ap-south-1 or ap-south-2, which gives you an auditable record that inference stayed within India. Usage is itemized on AWS Cost Explorer and the AWS Cost and Usage Report. Spend attribution by model works the same way as for the rest of your Amazon Bedrock workloads.
>
> Conclusion
>
> Amazon Bedrock brings the OpenAI GPT-5.6 Terra and Luna models, with a 1-million-token context window, to customers building in India. The India geographic inference profiles are available on the bedrock-runtime  endpoint, which is the endpoint we recommend for new applications. With India geographic cross-Region inference, you can scale across the Mumbai and Hyderabad Regions while keeping inference within the country. You can call the models through the OpenAI Responses API, the OpenAI Chat Completions API, or the Amazon Bedrock Converse API. If you have an existing workload on the bedrock-mantle endpoint, it remains fully supported and no changes are required; to adopt the India geographic profiles, point that workload at the bedrock-runtime  endpoint in Mumbai or Hyderabad. Review the Amazon Bedrock pricing page for current GPT-5.6 rates before sizing a production workload.
>
> To get started, review the model cards for GPT-5.6 Terra and Luna and the Cross-Region inference section in the Amazon Bedrock User Guide. Try a prompt in the Amazon Bedrock console playground in Mumbai or Hyderabad, then wire up the code examples shared earlier in this post. If you run into an issue or want to ask the community, AWS re:Post is a good place to search or post a question.
>
> About the authors
>
> Sahil Verma
>
> Sahil is a Senior AI Specialist Solutions Architect at AWS based in India, where he focuses on Agentic AI and Generative AI initiatives for Banking, Financial Services, and Insurance (BFSI) customers. He works with customers from ideation to production—spanning agentic AI systems, AI engineering, foundation models, and inference-optimized architectures—to deliver measurable business outcomes.
>
> Melanie Li
>
> Melanie Li, PhD, is a Senior Generative AI Specialist Solutions Architect at AWS based in Sydney, Australia, where her focus is on working with customers to build solutions using state-of-the-art AI/ML tools. She has been actively involved in multiple generative AI initiatives across APJ, harnessing the power of large language models. Prior to joining AWS, Dr. Li held data science roles in the financial and retail industries.
>
> Saurabh Trikande
>
> Saurabh is a Senior Product Manager for Amazon Bedrock and Amazon SageMaker Inference. He is passionate about working with customers and partners, motivated by the goal of democratizing AI. He focuses on core challenges related to deploying complex AI applications, inference with multi-tenant models, cost optimizations, and making the deployment of generative AI models more accessible. In his spare time, Saurabh enjoys hiking, learning about innovative technologies, following TechCrunch, and spending time with his family.
>
> Stephanie Chiao
>
> Stephanie is a Generative AI Service and Capacity Lead at AWS.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。