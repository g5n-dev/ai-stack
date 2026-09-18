---
title: "Introducing Kimi K3 on Amazon Bedrock"
date: 2026-09-19T02:30:37+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "生成式 AI", "Prompt 工程", "Amazon Bedrock", "Announcements", "Intermediate (200)", "博客与播客"]
categories: []
source: "blogs_podcasts"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:38138bb8383cc5b6ab305ea795381973d9ffb662d167320f8bd7379f1c3b13b4"
source_payload_sha256: "sha256:71c9401af8e2f4100d46f207d992456c754ece203266eea9a34942a087738eb9"
observation_id: obs_a6fcd04e2285ba1fc4c508d6caaa61edd4f837d631a64f81374d12406e56478e
event_id: evt_a60ea1bcd2999735d7fca200419f656573f3d87cc5734c9787c77c8e860ef69c
revision_id: rev_2a2098655d7c8d50cc63a0576a9e25325debed58737282932b74c133984b3eba
source_published_at: 2026-09-18T16:52:01Z
first_seen_at: 2026-09-18T18:28:28.107581Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 37
description: "当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。"
external_url: https://aws.amazon.com/blogs/machine-learning/introducing-kimi-k3-on-amazon-bedrock
parent_observation_id: null
last_seen_at: 2026-09-18T18:28:28.107581Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/introducing-kimi-k3-on-amazon-bedrock](https://aws.amazon.com/blogs/machine-learning/introducing-kimi-k3-on-amazon-bedrock)
- **发布域名**: aws.amazon.com

## 来源摘要/节选

> Open-weight models are changing the economics of building and deploying AI at scale. Rapid gains in intelligence and efficiency mean companies can match each workload with the right balance of capability, speed, and cost. AWS is building for a future in which organizations can adopt open-weight innovation with the reliability and security required for production.
>
> Today, Kimi K3 from Moonshot AI is available on Amazon Bedrock, giving you a powerful new option for coding and knowledge work. According to Moonshot AI, Kimi K3 is its most capable model and the first open model to reach 2.8 trillion parameters. It combines native vision capabilities with a 1-million-token context window and delivers an approximate 2.5x improvement in scaling efficiency over Kimi K2. These advances make Kimi K3 well suited to long-running coding and knowledge workflows that require sustained context across large repositories, documents, and images. Kimi K3 is the first open-weight model on Amazon Bedrock to support explicit prompt caching, helping you reduce latency and input costs when reusing context across model calls.
>
> The launch of Kimi K3 reflects the sustained investment by AWS in open-weight models on Amazon Bedrock. Since 2025, Bedrock has added dozens of open-weight models from providers including DeepSeek, Google, MiniMax, Mistral AI, Moonshot AI, NVIDIA, OpenAI, and Qwen. Supporting this expanding selection is continued advancement of the inference technology that serves these models at scale. In 2026, Bedrock added support for tool calling, structured output, reasoning, response streaming, and the Responses and Chat Completions APIs. Because these are platform capabilities rather than per-model integrations, new open-weight models can benefit from them as they become available on Amazon Bedrock.
>
> As with all open-weight models on Amazon Bedrock, you can adopt Kimi K3 without changing your security posture. Your data is processed within the AWS data boundary, is not shared with the model provider, and is not used to train the underlying model. Zero data retention is always enabled for inference requests, while zero operator access prevents even AWS operators from accessing your prompts and completions during inference. Together, these protections let you use open-weight models with confidence while maintaining control of your data.
>
> Get started with Kimi K3 on Amazon Bedrock
>
> To try Kimi K3, open the Amazon Bedrock console, go to Test &gt; Playground, and select Kimi K3 as the model. From there, you can test your first prompt.
>
> Programmatically, you can call the model using the bedrock-runtime endpoint, which supports the OpenAI-compatible Responses and Chat Completions APIs, and the Amazon Bedrock Invoke and Converse API APIs.
>
> You can invoke Kimi K3 through a cross-Region inference profile. For workloads without regional restrictions we recommend using the global profile, global.moonshotai.kimi-k3, which routes each request to any supported commercial AWS Region worldwide. Global cross-Region inference costs approximately 10% less than a geographic profile. The US geographic profile, us.moonshotai.kimi-k3, keeps processing within the US geography for data residency requirements.
>
> Prerequisites
>
> An active AWS account with Amazon Bedrock access.
>
> Python 3.10+.
>
> AWS Identity and Access Management (AWS IAM) permissions to call the model: bedrock:InvokeModel, bedrock:InvokeModelWithResponseStream, and bedrock:CreateInference.
>
> Here is a quick example that uses the OpenAI SDK and the aws-bedrock-token-generator library for Python to generate short-term bearer tokens for authentication to Amazon Bedrock.
>
> from aws_bedrock_token_generator import provide_token
>
> from openai import OpenAI
>
> region = "us-west-2"
>
> oai_client = OpenAI(
>
> api_key=provide_token(region=region),
>
> base_url=f"https://bedrock-runtime.{region}.amazonaws.com/openai/v1",
>
> )
>
> resp = oai_client.responses.create(
>
> input="What is Byte-Pair Encoding, in AI?",
>
> model="global.moonshotai.kimi-k3",
>
> )
>
> print(resp.output_text)
>
> Optimize inference with explicit prompt caching
>
> Long-running coding and knowledge workflows often resend stable context, such as repository instructions, tool definitions, or reference documents. With explicit prompt caching, you identify reusable prompt prefixes so later requests can use cached content. When a request matches a cached prefix, Amazon Bedrock can reduce response latency and input token costs.
>
> Caching for Kimi K3 on Amazon Bedrock:
>
> You can mark the exact end of a reusable prompt prefix (after at least 1,024 tokens) by adding a prompt_cache_breakpoint to a supported input content.
>
> In explicit mode, tokens written to cache are billed at a higher rate but are then kept in cache for at least 30 minutes.
>
> For matching subsequent requests that hit the cache, input tokens will be billed at a discounted rate and will not count against input-tokens-per-minute quotas.
>
> With the OpenAI Python API, explicit caching can be configured as shown in the following example:
>
> resp = oai_client.responses.create(
>
> model="global.moonshotai.kimi-k3",
>
> # Enable explicit caching mode:
>
> extra_body={"prompt_cache_options": {"mode": "explicit"&#125;&#125;,
>
> input=[
>
> {
>
> "type": "message",
>
> "role": "system",
>
> "content": [
>
> {
>
> "type": "input_text",
>
> "text": SYSTEM_PROMPT,
>
> # A long, static system prompt is a great target for caching:
>
> "prompt_cache_breakpoint": {"mode": "explicit"},
>
> },
>
> ]
>
> },
>
> {
>
> "type": "message",
>
> "role": "user",
>
> "content": [
>
> {
>
> "type": "input_text",
>
> "text": USER_INPUT,
>
> # Multiple breakpoints can also be defined, for layered cache:
>
> "prompt_cache_breakpoint": {"mode": "explicit"},
>
> },
>
> ],
>
> },
>
> ],
>
> )
>
> if resp.usage.input_tokens_details.cached_tokens:
>
> print("Hit cache!")
>
> You can explore the Moonshot AI on AWS samples repository for more examples.
>
> Kimi K3 in practice
>
> In addition to using the APIs directly, you can use Kimi K3 through the wide range of coding assistants, personal agents, and agentic frameworks that support Amazon Bedrock specifically, or OpenAI-compatible model providers in general.
>
> Coding assistants
>
> There are several popular coding agents available to builders today, so consider OpenCode as an example. OpenCode is open source, model agnostic, and has a native amazon-bedrock model provider, which uses the Converse API.
>
> To get started, you can configure the amazon-bedrock provider either in your user-level or project-level opencode.json configuration files as shown in the OpenCode documentation. With the provider configured, OpenCode will automatically detect available Amazon Bedrock models which you can select from using the /models command. For example, a minimal ~/.config/opencode.json file could look like:
>
> {
>
> "$schema": "https://opencode.ai/config.json",
>
> "model": "amazon-bedrock/global.moonshotai.kimi-k3",
>
> "provider": {
>
> "amazon-bedrock": {
>
> "options": {
>
> "region": "us-west-2",
>
> "profile": "PLACEHOLDER-YOUR-AWS-PROFILE-NAME"
>
> }
>
> }
>
> }
>
> }
>
> Once the Amazon Bedrock provider is set up, you can use the /models command to switch models to global.moonshotai.kimi-k3 and start building.
>
> Kimi K3 can build substantial features and work over long-horizon tasks. In the following video, we try it out building a single-file browser-based game to get started:
>
> Figure 1: Building a browser-based game with Kimi K3 in OpenCode
>
> Productivity agents
>
> Beyond coding, Hermes Agent is one example of an open source assistant for general productivity. It can be used through a desktop app or popular messaging apps as well as the terminal, and supports use cases like deep research and task automation where Kimi K3 can also perform well.
>
> As detailed in their documentation, Hermes natively supports models on Amazon Bedrock. To get started:
>
> Run hermes model from your terminal.
>
> Scroll down the list of providers to “AWS Bedrock” (Hermes mislabels “Amazon Bedrock” as “AWS Bedrock”).
>
> If prompted, select the source AWS Region you’d like Hermes to send requests to.
>
> Select either the default credential chain (recommended) to use AWS Command Line Interface credentials already set up in your environment, or generate an Amazon Bedrock API key.
>
> Select Kimi K3 from the auto-discovered list of models, or if it is not available, enter global.moonshotai.kimi-k3 as a custom model name.
>
> If you use named profiles to manage multiple AWS credentials in your environment, then at the time of writing you need to set the AWS_PROFILE environment variable or use your default profile for Hermes. Alternatively, you can switch to an API key. Follow the open issue here for updates on support for setting AWS profile via the Hermes configuration file.
>
> Once the Amazon Bedrock provider is set up and the model configured, you can start using Kimi K3 for your agentic workflows in Hermes. For example, see the following short video in which we ask the agent to build out a personalized study plan:
>
> Figure 2: Building a personalized study plan with Kimi K3 in Hermes Agent
>
> Availability
>
> Kimi K3 is available today on Amazon Bedrock through the US Geo (us.) and Global (global.) cross-Region inference profiles. See Bedrock documentation for the full list of supported Regions. For pricing information, see Amazon Bedrock pricing.
>
> Give Kimi K3 a try in the Amazon Bedrock console, or explore the Moonshot AI on AWS samples repository on GitHub.
>
> Interested in how Amazon Bedrock can support your team? Connect with us to start the conversation.
>
> About the authors
>
> Alex Thewsey
>
> Alex is an AI Specialist Solutions Architect at AWS, based in Singapore. He focuses on how open source technologies and open weight models can help customers around the world to build innovative AI solutions and tackle AI governance challenges.
>
> Saurabh Trikande
>
> Saurabh is a Senior Product Manager for Amazon Bedrock and Amazon SageMaker Inference. He is passionate about working with customers and partners, motivated by the goal of democratizing AI. He focuses on core challenges related to deploying complex AI applications, inference with multi-tenant models, cost optimizations, and making the deployment of generative AI models more accessible. In his spare time, Saurabh enjoys hiking, learning about innovative technologies, following TechCrunch, and spending time with his family.
>
> William Yap
>
> William is Principal Product Manager for Amazon Bedrock.
>
> Tanvi Girinath
>
> Tanvi is a Product Marketing Manager for Amazon Bedrock at Amazon Web Services (AWS), where she helps customers adopt and scale AI applications and agents with Amazon Bedrock.
>
> Sofian Hamiti
>
> Sofian is a technology leader with over 12 years of experience building AI solutions, and leading high-performing teams to maximize customer outcomes. He is passionate about empowering diverse talents to drive global impact and achieve their career aspirations.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。