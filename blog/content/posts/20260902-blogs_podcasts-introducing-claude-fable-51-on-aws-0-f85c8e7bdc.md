---
title: "Introducing Claude Fable 5.1 on AWS"
date: 2026-09-02T12:35:39+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "生成式 AI", "Prompt 工程", "Amazon Bedrock", "Announcements", "Intermediate (200)", "博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:5d7d34fd136edd2905a0b21567852a285b8c2fbadf4cd5d84e26b45356407d20"
source_payload_sha256: "sha256:e94810c142d74f414b5852c09a69df992fff18079b65c88c9eadf3662e1ff0da"
observation_id: obs_f85c8e7bdc49608ebcf8fca8ac0a74b6edbac62f873c5035c805a451f668710c
event_id: evt_c09627f3946a356fe88562ebfdf4c6bcc708f3febdbd208327b900d125dc745a
revision_id: rev_02938260c30f32d20744e857e47e957d2cc3910d31f1582c894c694c67c17969
source_published_at: 2026-09-01T19:12:43Z
first_seen_at: 2026-09-02T04:32:40.033876Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 35
interpretation_sha256: "sha256:988f7c16e3e7b1d7b9d9a57014fa25cb70de1cf1d98e9efdc6f6c60be52f8da7"
description: "该博客宣布 Anthropic 的最新推理模型在 Amazon Bedrock 与 AWS 平台上正式上线，具备更强的代码编写、科研分析和跨应用工作流能力，并说明了相应的数据保留政策和企业防护方案。"
external_url: https://aws.amazon.com/blogs/machine-learning/introducing-claude-fable-5-1-on-aws
parent_observation_id: null
last_seen_at: 2026-09-02T04:32:40.033876Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/introducing-claude-fable-5-1-on-aws](https://aws.amazon.com/blogs/machine-learning/introducing-claude-fable-5-1-on-aws)
- **发布域名**: aws.amazon.com

## 要点解读

### 这是什么  
该博客宣布 Anthropic 的最新推理模型在 Amazon Bedrock 与 AWS 平台上正式上线，具备更强的代码编写、科研分析和跨应用工作流能力，并说明了相应的数据保留政策和企业防护方案。  

### 用在哪里  
适用于需要在多步骤、长时间任务中进行自主规划与执行的开发者、数据分析团队以及对数据安全有合规要求的企业用户。  

### 可以推断的  
推测：更强的自主纠错与进度反馈特性可能吸引企业在关键业务系统中采用此类模型。  
推测：数据保留与人工审查的要求会影响部分用户对模型使用方式的选择。

## 来源摘要/节选

> Today, we’re excited to announce the availability of Claude Fable 5.1 on Amazon Bedrock and Claude Platform on AWS. Claude Fable 5.1 delivers frontier intelligence for ambitious tasks across coding, scientific research, and enterprise workflows.
>
> Given its capabilities, Anthropic has designated Fable 5.1 a Covered Model, a category of Claude models that carry additional data retention, safety review, and access policies wherever they’re offered. For more information, see Amazon Bedrock abuse detection and Anthropic’s Covered Models page. Anthropic also announced the Enterprise Frontier Safeguards, a solution that will give customers the option to safely deploy Anthropic’s most capable models while keeping their data in cloud infrastructure they control. The Enterprise Frontier Safeguards section that follows covers what this means on Amazon Bedrock.
>
> This post covers Claude Fable 5.1’s improvements, the Enterprise Frontier Safeguards, and how to start building with the model on Amazon Bedrock.
>
> What makes Claude Fable 5.1 different
>
> Anthropic reports Fable 5.1 is a clear improvement over Fable 5 on the hardest reasoning tests Anthropic runs. These tests include competition mathematics, graduate-level questions in engineering and the sciences, and long multi-step problems where reliability is key. In day-to-day use that shows up as better judgment on ambiguous tasks and fewer confident wrong answers:
>
> Agentic coding. Carries more of a project on its own, from code base-spanning features to code review and performance work, across multi-hour sessions. It is also more honest: if it gets stuck it says so, and it is less likely to disable a failing test to pass.
>
> Autonomous operation. Built for multi-hour jobs that span many applications. It plans, uses the tools it needs, recovers when a step fails, and keeps you updated without being asked.
>
> End-to-end knowledge work. Takes an analysis from first question to finished document, doing the research, building the spreadsheet, writing the memo or deck, and checking its numbers as it goes. Built for everyday finance, accounting, and healthcare work.
>
> Scientific research. Supports research campaigns from literature and hypotheses to models, experiments, and formal verification.
>
> Improved usability. Keeps you updated on long tasks, writes more clearly, and follows instructions more closely.
>
> Data retention
>
> Because Claude Fable 5.1 is a Covered Model, its use is subject to data retention for up to 30 days and human review by Amazon personnel. With Amazon Bedrock, you can control data retention through a mode on your account or Amazon Bedrock project, which you configure with the data retention API. Using Claude Fable 5.1 requires the aws_review mode, which you set before you invoke the model. In this mode, AWS retains your prompts and outputs for human safety review within the AWS boundary. Claude Fable 5.1 does not require sharing with the model provider. See Amazon Bedrock data retention for more details.
>
> Enterprise Frontier Safeguards
>
> Enterprise Frontier Safeguards (EFS), built in partnership between AWS and Anthropic, will help eligible customers use Claude Fable 5 and Claude Fable 5.1 models while keeping their data in a cloud environment they control.
>
> If you are an EFS-eligible customer, you can use Claude Fable 5 and Claude Fable 5.1 with zero data retention (ZDR) on Amazon Bedrock and Claude Platform on AWS. This is available for internal use through December 31, 2026. Additional Enterprise Frontier Safeguards will be available later this year, you will be able to keep your prompts and outputs in your AWS account, under your own encryption keys, access policies, and audit logging. Safety monitoring will be through automated review with no human review required.
>
> Getting started with Claude Fable 5.1 on Amazon Bedrock
>
> To try Fable 5.1, open the Amazon Bedrock console, go to Test &gt; Playground, and select Fable 5.1 as the model. From there, you can run a prompt directly against it.
>
> Programmatically, you can call the model with the Anthropic Messages API against bedrock-runtime (through the Anthropic SDK). You can also stay on the Invoke and Converse APIs on bedrock-runtime through the AWS Command Line Interface (AWS CLI) and AWS SDK.
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
> AWS Identity and Access Management (IAM) permissions: bedrock:InvokeModeland bedrock:InvokeModelWithResponseStream.
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
> # Invoke Claude Fable 5.1
>
> response = bedrock_runtime.invoke_model(
>
> modelId="global.anthropic.claude-fable-5-1",
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
> # Fable 5.1 is a reasoning model: the response may include a thinking block
>
> # before the text block, so select the text block rather than a fixed index.
>
> print(next(b["text"] for b in result["content"] if b["type"] == "text"))
>
> You can explore the Getting Started notebook for more examples.
>
> Availability
>
> Claude Fable 5.1 is available today on Amazon Bedrock through the US Geo CRIS (us.) and Global CRIS (global.) inference profiles. In AWS GovCloud (US), it is available on both the bedrock-runtime and bedrock-mantle endpoints. See the Bedrock documentation for the full list of supported Regions. For pricing information, see Amazon Bedrock pricing. It is also available through Claude Platform on AWS in North America.
>
> Give Claude Fable 5.1 a try in the Amazon Bedrock console, in Claude Platform on AWS, or explore the Getting Started notebooks on GitHub.
>
> About the authors
>
> Dani Mitchell
>
> Dani is a Sr. generative AI Specialist Solutions Architect at AWS and the SA lead for Amazon Bedrock Knowledge Bases. He helps enterprises across the world design and deploy generative AI solutions using Amazon Bedrock and Anthropic’s models and capabilities to build scalable, production-ready applications.
>
> Aamna Najmi
>
> Aamna is a Senior Specialist Solutions Architect for Generative AI focusing on Anthropic models and operationalizing and governing generative AI systems at scale on Amazon Bedrock. She helps ISVs solve their challenges, embrace innovation, and create new business opportunities with Amazon Bedrock.
>
> Sofian Hamiti
>
> Sofian is a technology leader with over 12 years of experience building AI solutions, and leading high-performing teams to maximize customer outcomes. He is passionate about empowering diverse talents to drive global impact and achieve their career aspirations.
>
> Antonio Rodriguez
>
> Antonio is a Principal Generative AI Tech Leader at Amazon Web Services. He helps companies of all sizes solve their challenges, embrace innovation, and create new business opportunities with Amazon Bedrock.
>
> Ayan Ray
>
> Ayan is a Principal Partner Solutions Architect and AI Tech Lead at AWS, serving as the Worldwide Tech Lead for Anthropic at AWS. He works at the intersection of cloud architecture and Artificial Intelligence, helping organizations adopt and scale Anthropic’s technologies on AWS.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。