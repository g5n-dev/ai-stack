---
title: "Claude Opus 5.5 is now available on AWS"
date: 2026-09-23T14:01:21+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "生成式 AI", "Prompt 工程", "Amazon Bedrock", "Announcements", "Intermediate (200)", "博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:10e3d3ee212a7889529969ff864a7c99b4c192ec888dc5abae2df1ae597e2c17"
source_payload_sha256: "sha256:9c12c7605ac9cb19842f00d576700c5eb7ebf0ebc6dd445f89ab46acaaeff934"
observation_id: obs_7322241f50811c86635013fca1c2dec777d6bc59ec939d3fe261730326e52f31
event_id: evt_5a72d9ab512c38d471ff4932e5d913753dbaab58410c503d1a1ef6048c1460b1
revision_id: rev_8cf372ad8d56df63cccb05d0c6a85e6b2548ebfa3517b48dec2074071577a9dd
source_published_at: 2026-09-22T17:28:01Z
first_seen_at: 2026-09-23T06:12:07Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 39
interpretation_sha256: "sha256:5c74e44c5d9ab4e64d45ac4515ece5b932ab74bb52ab531070c7ea03041a1644"
description: "这是一篇公告，介绍 Anthropic 在 Amazon Bedrock 与 Claude Platform 上线最新的 Opus 5.5 模型，强调其在 token 利用率、费用以及安全分类器方面的提升，并提供接入示例。"
external_url: https://aws.amazon.com/blogs/machine-learning/claude-opus-5-5-is-now-available-on-aws
parent_observation_id: null
last_seen_at: 2026-09-23T05:58:33.845485Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/claude-opus-5-5-is-now-available-on-aws](https://aws.amazon.com/blogs/machine-learning/claude-opus-5-5-is-now-available-on-aws)
- **发布域名**: aws.amazon.com

## 要点解读

### 这是什么  
这是一篇公告，介绍 Anthropic 在 Amazon Bedrock 与 Claude Platform 上线最新的 Opus 5.5 模型，强调其在 token 利用率、费用以及安全分类器方面的提升，并提供接入示例。  

### 用在哪里  
适用于在云端进行自动化编码、知识文档处理以及长时间运行任务的开发者或企业，特别是关注成本控制、可解释性和安全合规的场景。  

### 可以推断的  
推测：由于 token 效率提升且定价更低廉，组织在部署大规模 Agent 工作流时有望降低整体计算成本。  
推测：模型内置的安全分类器涉及生物、网络安全和 AI 开发等领域，实际使用可能需要满足更严格的合规要求。

## 来源摘要/节选

> Today, we’re excited to announce the availability of Claude Opus 5.5 on Amazon Bedrock and Claude Platform on AWS, the first of the Claude 5.5 model family. Claude Opus 5.5 is Anthropic’s most capable Opus model suitable for agentic coding, knowledge work, and long-running tasks.
>
> This post covers Claude Opus 5.5’s improvements, practical guidance, and how to start building with the model on Amazon Bedrock.
>
> What makes Claude Opus 5.5 different
>
> According to Anthropic, Claude Opus 5.5 does more with fewer tokens than Claude Opus 5, and new pricing passes those gains straight to customers. Lower per-token prices and much cheaper cache reads stack on top of the efficiency gains. The result is an average lower cost per task than Claude Opus 5, so teams can run more ambitious agentic work at scale.
>
> Claude Opus 5.5 is trained to communicate more clearly. As it works, it surfaces what it did, what it found, and what it needs, making long-running tasks easier to follow. Adaptive thinking is always on, and Opus 5.5 decides how much reasoning each task needs. You can use effort as your control instead of manual thinking budgets.
>
> Claude Opus 5.5 is the first Opus model that comes with safety classifiers similar to Claude Fable 5.1 in biology, cyber security, and AI development. Requests will be refused more frequently as compared to previous Opus versions.
>
> Use cases
>
> Claude Opus 5.5 capabilities are a good fit for industries where consistency and depth matter most. In software development, Opus 5.5 is an improvement over Opus 5 for longer-running sessions with clear communication and explainability, making it easier to use, review, and trust. For knowledge work, it requires fewer corrections compared to Opus 5 while working with and creating long documents and reports.
>
> Getting started with Claude Opus 5.5 on Amazon Bedrock
>
> To try Claude Opus 5.5, open the Amazon Bedrock console, choose Test, then Playground, and select Claude Opus 5.5 as the model. From there, you can run a prompt directly against it.
>
> Figure 1: Selecting an Anthropic Claude model in the Amazon Bedrock console Playground
>
> Figure 2: Running a prompt against a Claude model in the Amazon Bedrock console Playground
>
> Programmatically, you can call the model with the Anthropic Messages API against bedrock-runtime and bedrock-mantle (through the Anthropic SDK). You can also stay on the Invoke and Converse APIs on bedrock-runtime through the AWS Command Line Interface (AWS CLI) and AWS SDK.
>
> Prerequisites
>
> Active AWS account with Amazon Bedrock access.
>
> AWS Command Line Interface (AWS CLI) installed and configured.
>
> Python 3.10+.
>
> Boto3 installed: pip install boto3.
>
> Anthropic SDK installed: pip install anthropic.
>
> The Amazon Bedrock Token Generator for Amazon Bedrock authentication installed: pip install aws_bedrock_token_generator.
>
> AWS Identity and Access Management (IAM) permissions: bedrock:InvokeModel and bedrock:InvokeModelWithResponseStream.
>
> Here’s a quick example using the AWS SDK for Python (Boto3):
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
> region_name="us-east-1"
>
> )
>
> # Invoke Claude Opus 5.5
>
> response = bedrock_runtime.invoke_model(
>
> modelId="global.anthropic.claude-opus-5-5",
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
> "content": "An S3 bucket serves 40 TB/month egress. Estimate the monthly egress cost at $0.09/GB, and state one architecture change to cut it. Show the calculation, keep it under 120 words."
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
> # Opus 5.5 is a reasoning model: the response may include a thinking block
>
> # before the text block, so select the text block rather than a fixed index.
>
> print(next(b["text"] for b in result["content"] if b["type"] == "text"))
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
> region_name="us-east-1"
>
> )
>
> # Invoke Claude Opus 5.5
>
> response = bedrock_runtime.converse(
>
> modelId="global.anthropic.claude-opus-5-5",
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
> "text": "Can you explain the features of Amazon Bedrock?"
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
> You can also use the Anthropic Messages API through the anthropic SDK package for a streamlined experience:
>
> from anthropic import Anthropic
>
> from aws_bedrock_token_generator import provide_token
>
> token = provide_token(region="us-east-1")
>
> client = Anthropic(
>
> base_url="https://bedrock-runtime.us-east-1.amazonaws.com/anthropic",
>
> api_key=token,
>
> )
>
> # Invoke Claude Opus 5.5
>
> response = client.messages.create(
>
> model="global.anthropic.claude-opus-5-5",
>
> max_tokens=1024,
>
> messages=[{"role": "user", "content": "Can you explain the features of Amazon Bedrock?"}],
>
> )
>
> print(response)
>
> You can explore the Getting Started notebook for more examples. You can monitor usage, performance, and costs through Amazon CloudWatch and AWS Cost Explorer to scale your applications as demand grows.
>
> Availability
>
> Claude Opus 5.5 is available today on Amazon Bedrock through the US Geo CRIS (us.), EU Geo CRIS (eu.), AU Geo CRIS (au.), JP Geo CRIS (jp.) and Global CRIS (global.) inference profiles on bedrock-runtime. The model also runs in the US East (N. Virginia) Region (us-east-1), AP SouthEast (Melbourne) Region (ap-southeast-4)  on bedrock-mantle.
>
> See the Amazon Bedrock documentation for the full list of supported Regions. For pricing information, see Amazon Bedrock pricing. It is also available through Claude Platform on AWS in North America.
>
> Give Claude Opus 5.5 a try in the Amazon Bedrock console, in Claude Platform on AWS, or explore the Getting Started notebooks on GitHub.
>
> About the authors
>
> Aamna Najmi
>
> Aamna is a Senior Specialist Solutions Architect for Generative AI focusing on Anthropic models and operationalizing and governing generative AI systems at scale on Amazon Bedrock. She helps ISVs solve their challenges, embrace innovation, and create new business opportunities with Amazon Bedrock.
>
> Dani Mitchell
>
> Dani is a Sr GenAI Specialist Solutions Architect at AWS and the SA lead for Amazon Bedrock Knowledge Bases. He helps enterprises across the world design and deploy generative AI solutions using Amazon Bedrock and Anthropic’s models and capabilities to build scalable, production-ready applications.
>
> Sofian Hamiti
>
> Sofian is a technology leader with over 12 years of experience building AI solutions, and leading high-performing teams to maximize customer outcomes. He is passionate about empowering diverse talents to drive global impact and achieve their career aspirations.
>
> Eugenio Soltero
>
> Eugenio is a Sr. Product Marketing Manager for Amazon Bedrock at AWS. With several years of experience in generative AI, he helps customers navigate the evolving landscape of foundation models and generative AI to adopt solutions that deliver measurable value.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。