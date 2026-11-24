---
title: "Introducing the Amazon Bedrock Trusted Access API with Anthropic’s Enterprise Frontier Safeguards and Enterprise Data Controls"
date: 2026-11-24T14:01:40+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "生成式 AI", "Prompt 工程", "Amazon Bedrock", "Announcements", "Intermediate (200)", "博客与播客"]
categories: []
source: "blogs_podcasts"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:80405b69106e6384a3b8e48eb8630e283e84605fce87e7a17d60d8f28eca4e59"
source_payload_sha256: "sha256:401251ee48144c15e51c7f09df459a64c72abf07355b66d92e7d9a9f725cbfe6"
observation_id: obs_b24333cc89f9425e4c7b7f37e91c2730963337e70f4eaef977a7aab882a8bf68
event_id: evt_63414ebf64ace13d54e2c5269119a33e33978d8ce3b200a7c7497543470921ad
revision_id: rev_78dc0fe5f3c208b6866233d24b620c7d7c75d2421610f6a7ed8ea2212b7527ac
source_published_at: 2026-11-24T05:01:14Z
first_seen_at: 2026-11-24T06:16:24Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 126
description: "当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。"
external_url: https://aws.amazon.com/blogs/machine-learning/introducing-the-amazon-bedrock-trusted-access-api-with-anthropics-enterprise-frontier-safeguards-and-enterprise-data-controls
parent_observation_id: null
last_seen_at: 2026-11-24T06:00:23.958335Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/introducing-the-amazon-bedrock-trusted-access-api-with-anthropics-enterprise-frontier-safeguards-and-enterprise-data-controls](https://aws.amazon.com/blogs/machine-learning/introducing-the-amazon-bedrock-trusted-access-api-with-anthropics-enterprise-frontier-safeguards-and-enterprise-data-controls)
- **发布域名**: aws.amazon.com

## 来源摘要/节选

> Today we are announcing the general availability of the trusted access program API on Amazon Bedrock. The API gives you one place to discover, request, and enroll in model provider trusted access programs. We are also announcing the public preview of the first two offerings, Anthropic’s Enterprise Frontier Safeguards (EFS) and Enterprise Data Controls (EDC). Both are available on Amazon Bedrock, including Claude Fable, Claude Mythos, and Claude Opus 5.5 and Sonnet 5.5 used through the Cyber Verification Program (CVP).
>
> Frontier AI labs require stricter safety monitoring policies to their most capable models, and those policies still apply on Amazon Bedrock. For eligible customers, model providers also offer customers more control on how those policies are met, such as where retained data is stored and how it is reviewed. Each offering has its own terms, approvals, and settings.
>
> The Amazon Bedrock trusted access program API gives every provider offering one consistent Amazon Bedrock experience. Your teams discover offerings, check eligibility, and enroll in the same way for every provider. Your administrators decide who can enroll, using existing IAM policies and service control policies. As more model providers add offerings, those appear in the same place.
>
> EFS and EDC were built in partnership between AWS and Anthropic. They let you access Anthropic’s most capable models safely, from both a model use and a customer data perspective. With both EFS and EDC, when automated safety monitoring finds a risk, it creates a Safety Case for your team to review. With EFS, customers store their data in their own AWS account, and prompts and completions are not retained by Anthropic or Amazon Bedrock. With EDC, retained data is stored in Amazon-managed storage instead of your account and prompts and completions are not retained by Anthropic. One application gives access to both programs.
>
> In this post, we explain how the trusted access program API works, then walk through EFS and EDC storage options and setup.
>
> How trusted access programs work
>
> A trusted access program is a named provider program that gives customers more control of safety reviews and access to model capabilities in exchange for accepting the program’s terms. Amazon Bedrock trusted access program API now gives you one place to find the model and use case programs available to your account. EFS and EDC are the first offerings available today. Offerings that providers add later appear in the same place and follow the same steps.
>
> Anyone with access to the trusted access program API can list the offerings and check their status for an account, an organization in AWS Organizations, or an Amazon Bedrock project. The status tells you what to do next. eligible means you’re eligible for the offering and can enroll, requestable means you need approval for eligibility first, and the statusReason field in the response explains how to request it. The model provider (or AWS, as authorized by the model provider) approves your eligibility.
>
> Enrolling is a separate step where you accept the offering’s terms imposed by the provider. You enroll at the scope where you were approved: an account, every account in an organization from the management account, or a single project. You can opt out at any time. Each step is a call to the trusted access program API, so you control who can enroll with AWS Identity and Access Management (IAM) policies and service control policies (SCPs). More information is available in the trusted access programs documentation.
>
> Enterprise Frontier Safeguards
>
> With Enterprise Frontier Safeguards (EFS), you can retain your data in your own AWS environment with full control. It is designed with over 100 customers, including a quarter of the Fortune 100 and many companies in industries with strict rules on data visibility, like healthcare, financial services, and law.
>
> Automated safety monitoring looks for patterns that only show up across many requests. These include intentional misuse that could lead to serious harm, such as offensive cyber operations. They also include agents that go beyond what a user asked for, such as using a software exploit to reach an internal system.
>
> On Amazon Bedrock, AWS operates EFS and the customer inputs and outputs stay within the customer’s AWS account. Only automated safety monitoring within AWS reads the retained inputs and outputs. AWS human reviewers don’t review content for EFS. Your review stays with you. Neither AWS nor Anthropic humans access your retained inputs or outputs. Your inputs and outputs are never used for training.
>
> How it works
>
> Amazon Bedrock reaches your AWS Key Management Service (AWS KMS) key and Amazon Simple Storage Service (Amazon S3) bucket as a single AWS service principal and only through the key policy and bucket policy that you write. You can remove that access at any time, but Amazon Bedrock stops serving the covered models 24 hours after it loses access to your key or bucket.
>
> Figure 1: EFS workflow on Amazon Bedrock
>
> When you call a covered model including Claude Fable, Claude Mythos, and Claude Opus 5.5 and Sonnet 5.5 used through the Cyber Verification Program (CVP):
>
> Your application calls the model. Inference works as it does for any Amazon Bedrock model.
>
> Amazon Bedrock writes the prompt and response to its retention and key services.
>
> These services encrypt the data with your AWS KMS key.
>
> Bedrock writes the prompt and response to your bucket, encrypted with your key, or to Amazon-managed storage. When writing to your bucket, Amazon writes the content within minutes. On some failures with your key or bucket, we can retry for up to 72 hours.
>
> Automated safety monitoring, which runs in AWS owned and operated accounts, scans the data and looks for misuse across requests.
>
> If automated safety monitoring finds a potential risk, a case is created in your bucket for your review.
>
> How your team handles cases
>
> A Case summarizes what automated safety monitoring found and references the related transcripts. Retained records arrive under the transcripts/ prefix in your bucket, and case files arrive under review-cases/. Your team reviews each Case and writes a response file to review-responses/, stating whether it found a violation (violation or no_violation) and, for a violation, the applicable policy category.
>
> Enterprise Data Controls
>
> EDC offers the same automated safety monitoring as EFS and human review of flagged activity stays with your team. Unlike EFS, EDC stores retained data in Amazon managed storage, encrypted with AWS managed keys, so there’s no bucket or key to set up. Eligible customers can access both EFS and EDC through a single enrollment application. If your policy allows retained data to stay in Amazon-managed storage and encrypted with AWS-managed keys, enroll in EDC. If your policy instead requires retained data to be encrypted with your AWS KMS key and stay in your S3 bucket, enroll in EFS. Either way, your team will be able to review flagged activity.
>
> Outside EFS and EDC, you can use Claude Fable models on Amazon Bedrock in two ways today:
>
> With the aws_review data retention mode, Amazon Bedrock retains inputs and outputs for up to 30 days, where they are available for review within the AWS boundary.
>
> Eligible customers can use current Fable models for internal use with zero data retention (ZDR) through at least June 30, 2027. EFS is the long-term path after ZDR ends.
>
> Choose where retained data is stored
>
> With EFS, retained data is stored only in your own S3 bucket, encrypted with your KMS key. Neither Anthropic nor AWS keeps it in their own storage. The following table compares EFS with the other routes.
>
> Not Eligible for ZDR, EFS, or EDC
>
> ZDR exception (interim)
>
> EFS, your own Amazon S3 bucket (public preview)
>
> EDC, Amazon-managed storage (public preview)
>
> Data retention
>
> Up to 30 days
>
> None, through at least June 30, 2027, for current Fable models and existing Cyber Verification Program models for internal use
>
> Amazon Bedrock keeps no copy. Your lifecycle rules apply, 30 days minimum.
>
> Up to 30 days, then Amazon Bedrock deletes it
>
> Where the retained data is stored
>
> AWS managed storage
>
> Not retained
>
> Your Amazon S3 bucket
>
> Amazon-managed storage
>
> Encryption key
>
> AWS managed
>
> Not applicable
>
> Your AWS Key Management Service (AWS KMS) key
>
> AWS managed
>
> Safety monitoring
>
> Available for review within the AWS boundary
>
> None
>
> Automated. Cases arrive in your bucket for your team to review.
>
> Automated. Your team reviews flagged Cases. Cases aren’t delivered during the public preview.
>
> What your AWS CloudTrail shows
>
> Your Amazon Bedrock API calls
>
> Your Amazon Bedrock API calls
>
> Your Amazon Bedrock API calls, plus Amazon Bedrock’s use of your key and bucket
>
> Your Amazon Bedrock API calls
>
> Storage cost
>
> Not applicable
>
> Not applicable
>
> Usual Amazon S3 and AWS KMS charges
>
> Not applicable
>
> Table 1: Routes for Claude Fable models on Amazon Bedrock.
>
> Storage configurations apply to one Region at a time, and a Region without a configuration uses Amazon-managed storage. Save a configuration in every Region where you call covered models.
>
> Getting started
>
> Start by checking your EFS status with the trusted access program API:
>
> aws bedrock list-trusted-access-programs --region us-east-1
>
> If the status is eligible, your account is approved. If it’s requestable, follow the steps in the statusReason field to request access. Joining the preview turns off zero data retention for the accounts you add.
>
> After you’re approved, set up EFS in each Region where you call covered models:
>
> Create an AWS KMS key and an Amazon S3 bucket in the same Region. The key and bucket policies give Amazon Bedrock access only through its service principal and only for your account’s data.
>
> Give your role permission to save the storage configuration.
>
> Save your storage configuration. Amazon Bedrock checks your key and bucket settings before it saves, and the error names any check that fails.
>
> Set your data retention mode to aws_review.
>
> Call a Claude Fable model, then confirm that AWS CloudTrail shows Amazon Bedrock using your key. Retained records usually appear in your bucket within minutes but can take up to 72 hours if Amazon Bedrock has to retry.
>
> The EFS documentation has the complete key policy, bucket policy, IAM policy, and API calls for each step. It also covers organization and project configurations, and troubleshooting. To use enterprise data controls instead, skip steps 1 and 2 and choose Amazon-managed storage in step 3.
>
> Conclusion
>
> The trusted access program API, now generally available, gives you one way to find model provider offerings on Amazon Bedrock, check your status, and enroll, with IAM policies and SCPs controlling who can opt in. EFS and EDC are the first offerings in public preview. They give you control over your data when you use Claude Fable and Cyber Verification Program models. With your own Amazon S3 bucket, Amazon Bedrock keeps no copy of the retained data, your AWS KMS key encrypts it, and every access appears in your own AWS CloudTrail logs.
>
> To get started, check your EFS status with aws bedrock list-trusted-access-programs and enroll in the EFS preview. To learn more, see the trusted access programs documentation and the EFS/EDC documentation.
>
> To enroll in the EFS and EDC public preview, work with your AWS account team to submit a request. Have the AWS account IDs ready (or Amazon Bedrock runtime project ARNs for projects) and note that the preview is for customers already enrolled in EFS ZDR.
>
> About the authors
>
> Dani Mitchell
>
> Dani is a Senior Specialist Solutions Architect for Generative AI at AWS, working on go-to-market for Anthropic on Amazon Bedrock. He helps enterprises across the world design and deploy generative AI solutions using Anthropic’s models and capabilities on Amazon Bedrock to build scalable, production-ready applications.
>
> Munir Nanjee
>
> Munir is a Senior Technical Product Manager for Amazon Bedrock, working on Anthropic models. Munir currently focuses on Anthropic’s features and programs, including Enterprise Frontier Safeguards (EFS) and Enterprise Data Controls (EDC). Munir is passionate about helping customers use generative AI at scale. In his spare time, Munir enjoys volunteering, traveling, and listening to music.
>
> Rey Wang
>
> Rey Wang is a Principal Product Manager on the Amazon Bedrock team, where she focuses on Trust and Safety. She helps enterprises adopt frontier models with the safety, security, and data controls they need.
>
> Yiwen Zhang
>
> Yiwen Zhang is a Principal GenAI Solutions Architect at AWS. She develops both generative AI applications and enterprise integration strategies. With a PhD in computational statistics and a decade of experience developing and deploying AI/ML and data pipelines, she brings deep technical expertise to enterprise AI transformation. She focuses on token economics and interpretability-based model safety. Her goal is to help enterprises build generative AI agents into “outcome as a service” solutions.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。