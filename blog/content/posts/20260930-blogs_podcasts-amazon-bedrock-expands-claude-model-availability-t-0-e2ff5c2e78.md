---
title: "Amazon Bedrock expands Claude model availability to in-country inferencing in India"
date: 2026-09-30T21:45:34+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "生成式 AI", "Prompt 工程", "Amazon Bedrock", "Announcements", "Intermediate (200)", "博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:8b88b5f6fb3db7565fdb653101abbcb912b2b98af071c7145e51192c55529798"
source_payload_sha256: "sha256:8f70dd4ca4d8d2296838e08acd5d1d50d9c3896cf975455de1cd4d7892cd820f"
observation_id: obs_e2ff5c2e78222da2abceb57a3d37dd90a9a3ec8f3abe689f9c0e50057dd1dd8d
event_id: evt_a9def87d72331a78fb10884f56c818ab3dfa0dedcc7820d76a9c1cb434f1ef03
revision_id: rev_e9990cb52adaf789958b603933dff89b53c9db60c4ce362caec9fcb78c076420
source_published_at: 2026-09-30T01:13:14Z
first_seen_at: 2026-09-30T13:57:06Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 83
interpretation_sha256: "sha256:76a9b0ebaf143006fed73dd2532a58c0c92d4da4498ac49189c73c3c80e6eb48"
description: "亚马逊云服务在印度启用跨区域推理，使Claude Opus 5、Sonnet 5、Haiku 4.5在孟买和海得拉巴两个区域之间完成计算，数据始终保持在本地且默认不保留模型输入输出。"
external_url: https://aws.amazon.com/blogs/machine-learning/amazon-bedrock-expands-claude-model-availability-to-india-cross-region-inference
parent_observation_id: null
last_seen_at: 2026-09-30T13:42:44.272398Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/amazon-bedrock-expands-claude-model-availability-to-india-cross-region-inference](https://aws.amazon.com/blogs/machine-learning/amazon-bedrock-expands-claude-model-availability-to-india-cross-region-inference)
- **发布域名**: aws.amazon.com

## 要点解读

### 这是什么  
亚马逊云服务在印度启用跨区域推理，使Claude Opus 5、Sonnet 5、Haiku 4.5在孟买和海得拉巴两个区域之间完成计算，数据始终保持在本地且默认不保留模型输入输出。  

### 用在哪里  
适用于需要在印度本地满足数据驻留和合规要求的企业或开发者，可通过控制台的无代码测试环境或 InvokeModel、Converse、Anthropic Messages 等 API 直接调用模型进行文本生成、对话等业务场景。  

### 可以推断的  
推测：跨区域推理在两个可用区之间共享算力，能够在流量高峰时保持吞吐量和响应速度的稳定。  
推测：默认不保留输入输出的安全模型表明亚马逊在提供符合印度数据主权要求的 AI 服务上采取了更高强度的隐私保护，这可能促使金融、医疗等受监管行业加速采用。

## 来源摘要/节选

> We’re excited to announce the availability of Anthropic’s Claude Opus 5, Claude Sonnet 5, and Claude Haiku 4.5 in India. The India regional endpoint is served through geographic cross-Region inference. Customers in India can now access these models on Amazon Bedrock while processing the data in the India Regions in addition to the already supported global cross-Region inference. This can be useful when customers need to meet the requirements to process data locally in a desired geography.
>
> In this post, we discuss how India geographic cross-Region inference works from the Mumbai and Hyderabad Regions on Amazon Bedrock for Anthropic Claude models. We also show how to get started from the Amazon Bedrock console and with code, using Anthropic’s Messages API, Amazon Bedrock InvokeModel API, and Converse API.
>
> India inference
>
> To help you achieve the scale of your AI applications, Amazon Bedrock offers cross-Region inference profiles, a feature you can use to distribute inference across multiple AWS Regions without having to manage capacity in each Region. The request originates from your source Region where you make the API call and is automatically routed to one of the destination Regions defined in the inference profile. The India geographic profile keeps inference within India. Requests route only between ap-south-1 and ap-south-2. Your input prompts and output results might move between those two Regions. Instead of being bound to the capacity of one Region, your requests draw on a broader pool of compute. This helps you maintain throughput and consistent performance under load, which matters most during traffic peaks. Cross-Region inference operates through the secure AWS network with end-to-end encryption for data in transit. Customer data is not stored in a destination Region when using cross-Region inference. It remains exclusively within the source Region. Amazon Bedrock uses a zero data retention (ZDR) data security model. This means that by default, Amazon Bedrock does not store model inputs or outputs. However, certain models require human review by AWS as a condition if content is flagged by automatic safety classifiers. For more details, see Data retention in the Amazon Bedrock User Guide. Billing and quota consumption are tracked against your account in the source Region, regardless of which backend Region handled the request. Amazon CloudWatch and AWS CloudTrail record log entries in the source Region only, so your monitoring stays in one place. Geographic cross-Region inference is available on the bedrock-runtime endpoint. It supports Anthropic’s Messages API and the native Amazon Bedrock InvokeModel and Converse APIs, along with Amazon Bedrock features such as Amazon Bedrock Guardrails and intelligent prompt routing.
>
> Access Claude models from the Amazon Bedrock console
>
> You can access Claude models in the text playground in the Amazon Bedrock console, which requires no coding or SDK setup. You can send prompts, adjust inference parameters, and switch between variants to get a feel for each model before you integrate the API.
>
> Open the Amazon Bedrock console in the Region that you want to use as the source.
>
> In the navigation pane, under Test, choose Playground.
>
> Choose Select model in the middle of the page.
>
> Search for Anthropic Claude Opus 5, select IN Anthropic Claude Opus 5 as the inference profile under Inference, and choose Apply.
>
> Enter a prompt and choose Run to generate a response.
>
> Figure 1: The Claude Opus 5 model selected in the Amazon Bedrock console playground
>
> Call Claude models with the Anthropic Messages API and Amazon Bedrock InvokeModel and Converse API
>
> You can access Anthropic’s Claude Opus 5, Claude Sonnet 5, or Claude Haiku 4.5 programmatically with the India geographic inference profile ID using the Anthropic Messages API on bedrock-runtime through the Anthropic SDK, or keep using the InvokeModel and Converse APIs on bedrock-runtime through the AWS Command Line Interface (AWS CLI) and AWS SDK.
>
> Prerequisites
>
> Active AWS account with Amazon Bedrock access.
>
> AWS CLI installed and configured.
>
> Python 3.8+.
>
> Boto3 installed: pip install boto3.
>
> Anthropic SDK installed: pip install anthropic.
>
> The Bedrock Token Generator for Amazon Bedrock model inference authentication installed: pip install aws_bedrock_token_generator.
>
> AWS Identity and Access Management (IAM) role or user has the necessary permissions to invoke Amazon Bedrock models using a geographic cross-Region inference profile.
>
> Here’s a quick example using the AWS SDK for Python (Boto3) with the InvokeModel API:
>
> import boto3
>
> import json
>
> # Create a Bedrock Runtime client
>
> bedrock_runtime = boto3.client(
>
> service_name="bedrock-runtime",
>
> region_name="ap-south-1"
>
> )
>
> # Invoke Claude Sonnet 5
>
> response = bedrock_runtime.invoke_model(
>
> modelId="in.anthropic.claude-sonnet-5",
>
> contentType="application/json",
>
> accept="application/json",
>
> body=json.dumps({
>
> "anthropic_version": "bedrock-2023-05-31",
>
> "max_tokens": 4096,
>
> "messages": [
>
> {
>
> "role": "user",
>
> "content": " Can you explain the features of Amazon Bedrock? "
>
> }
>
> ]
>
> })
>
> )
>
> result = json.loads(response["body"].read())
>
> print(result["content"][0]["text"])
>
> You can also use the Amazon Bedrock Converse API for a unified multi-model experience:
>
> import boto3
>
> # Create a Bedrock Runtime client
>
> bedrock_runtime = boto3.client(
>
> service_name="bedrock-runtime",
>
> region_name="ap-south-1"
>
> )
>
> # Invoke Claude Opus 5
>
> response = bedrock_runtime.converse(
>
> modelId="in.anthropic.claude-opus-5",
>
> messages=[
>
> {
>
> "role": "user",
>
> "content": [
>
> {
>
> "text": " Can you explain the features of Amazon Bedrock?"
>
> }
>
> ]
>
> }
>
> ],
>
> inferenceConfig={
>
> "maxTokens": 4096
>
> }
>
> )
>
> if 'output' in response:
>
> blocks = response['output']['message']['content']
>
> print('\n'.join(b.get('text', '') for b in blocks if 'text' in b))
>
> You can also use the Anthropic Messages API using the anthropic SDK package for a streamlined experience:
>
> from anthropic import Anthropic
>
> from aws_bedrock_token_generator import provide_token
>
> token = provide_token(region="ap-south-1")
>
> client = Anthropic(
>
> base_url="https://bedrock-runtime.ap-south-1.amazonaws.com/anthropic",
>
> api_key=token,
>
> )
>
> response = client.messages.create(
>
> model="in. anthropic.claude-haiku-4-5-20251001-v1:0",
>
> max_tokens=1024,
>
> messages=[{"role": "user", "content": "Can you explain the features of Amazon Bedrock?"}],
>
> )
>
> print(response)
>
> You can monitor usage, performance, and costs through CloudWatch and AWS Cost Explorer to scale your applications as demand grows.
>
> Conclusion
>
> With the launch of Anthropic’s Claude Opus 5, Claude Sonnet 5, and Claude Haiku 4.5 using Amazon Bedrock with India geographic cross-Region inference, you can now build highly scalable, resilient generative AI applications while keeping inference within the country. To get started, access Anthropic’s Claude models in the Amazon Bedrock console, or call them with the API using the India geographic inference profile ID. For the most current information about model availability in each Region, see Regional availability by models in the Amazon Bedrock User Guide.
>
> About the authors
>
> Aamna Najmi
>
> Aamna is a Senior Specialist Solutions Architect for Generative AI focusing on Anthropic models and operationalizing and governing generative AI systems at scale on Amazon Bedrock. She helps ISVs solve their challenges, embrace innovation, and create new business opportunities with Amazon Bedrock.
>
> Eugenio Soltero
>
> Eugenio is a Sr. Product Marketing Manager for Amazon Bedrock at AWS. With several years of experience in generative AI, he helps customers navigate the evolving landscape of foundation models and generative AI to adopt solutions that deliver measurable value.
>
> Sofian Hamiti
>
> Sofian is a technology leader with over 12 years of experience building AI solutions, and leading high-performing teams to maximize customer outcomes. He is passionate about empowering diverse talents to drive global impact and achieve their career aspirations.
>
> Ayan Ray
>
> Ayan is a Principal Partner Solutions Architect and AI Tech Lead at AWS, serving as the Worldwide Tech Lead for Anthropic at AWS. He works at the intersection of cloud architecture and Artificial Intelligence, helping organizations adopt and scale Anthropic’s technologies on AWS.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。