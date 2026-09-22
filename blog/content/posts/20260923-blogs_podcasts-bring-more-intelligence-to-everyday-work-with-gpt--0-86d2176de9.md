---
title: "Bring more intelligence to everyday work with GPT-6 Sol and GPT-6 Luna on Amazon Bedrock"
date: 2026-09-23T02:57:15+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "Prompt 工程", "Amazon Bedrock", "Announcements", "Intermediate (200)", "博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:128d948bf157c1a244d1995af2856afce2db4b79e9fce7c8d070cca0e9d179b1"
source_payload_sha256: "sha256:cca3a40071baf997b12a97a46c74b0cfc40e83bd6512102c19d0eb2638b25c32"
observation_id: obs_86d2176de98238d5ddb9673084584074f310cd71ea2f47b8326fb696fa5ccc1c
event_id: evt_460acf5ca279933ce9a285875b651a3810d4085865e6c4c10c80921223380654
revision_id: rev_8d9138821748a2f717c09f4f90bd38840efefa7cf43191e01499f5b8dc1291c0
source_published_at: 2026-09-22T18:10:22Z
first_seen_at: 2026-09-22T19:07:26Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 88
description: "当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。"
external_url: https://aws.amazon.com/blogs/machine-learning/bring-more-intelligence-to-everyday-work-with-gpt-6-sol-and-gpt-6-luna-on-amazon-bedrock
parent_observation_id: null
last_seen_at: 2026-09-22T18:54:37.039693Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/bring-more-intelligence-to-everyday-work-with-gpt-6-sol-and-gpt-6-luna-on-amazon-bedrock](https://aws.amazon.com/blogs/machine-learning/bring-more-intelligence-to-everyday-work-with-gpt-6-sol-and-gpt-6-luna-on-amazon-bedrock)
- **发布域名**: aws.amazon.com

## 来源摘要/节选

> GPT-6 Sol and GPT-6 Luna are now generally available on Amazon Bedrock, giving you more options to match intelligence and efficiency to each workload.
>
> The value of AI at scale depends on two dimensions: what a model can do and how often you can put it to use. Greater intelligence expands the complexity a model can handle, from subtle coding problems to multistep processes across tools. Efficiency determines how broadly that intelligence can support everyday activity and repeatable tasks, where every additional token, retry, and second of latency multiplies across requests.
>
> GPT-6 Astra established the upper end of the GPT-6 family for the most ambitious projects, where achieving the highest-quality result matters more than cost. Organizations also need advanced intelligence for the recurring tasks that keep products and operations moving. GPT-6 Sol brings strong reasoning and coding capabilities to complex tasks performed throughout the week, with economics suited to regular use. GPT-6 Luna makes focused, repeatable tasks practical at high volume, where small differences in latency and cost multiply across requests.
>
> Today, GPT-6 Sol and GPT-6 Luna from OpenAI are generally available on Amazon Bedrock, running on an inference engine built for high performance, security and reliability at scale. Both models come at significantly lower API pricing than their GPT-5.6 predecessors, giving you more ways to bring GPT-6 intelligence into production with the performance, control, and flexibility your workloads require.
>
> Solve harder problems every day
>
> GPT-6 Sol is designed for demanding tasks that recur throughout development and operations. It can implement features, debug issues, refactor and review code, analyze data, and complete multistep processes across tools and applications. Improvements over GPT-5.6 Sol in coding and computer use help it carry a task from investigation through implementation and validation while preserving the context behind its decisions.
>
> As GPT-6 Sol handles more of that process, developers need to see what it changed, what it verified, and what it could not confirm. On an internal factuality evaluation, OpenAI found that GPT-6 Sol made approximately half as many factual mistakes as GPT-5.6 Sol. GPT-6 Sol also benefits from clearer communication about its work and results, helping teams identify gaps sooner and understand where human judgment is still needed.
>
> Together, stronger execution and clearer reporting make GPT-6 Sol practical across the development cycle. The relevant measure there is the total cost of reaching a usable result, including output quality, token usage, retries, and latency.
>
> Make focused intelligence economical at volume
>
> When a task runs thousands of times a day, the economics of each call determine whether the workflow scales. A single classification or summary is inexpensive on its own, but the cost of extraction, routing, and follow-up across a full document pipeline compounds with every additional request.
>
> GPT-6 Luna is designed for workloads where that volume matters. You can use it to extract information from large document collections, summarize incoming material, classify inputs, and answer focused questions across many users or applications.
>
> Efficiency at volume also requires consistent outputs. OpenAI’s evaluations show improvements in GPT-6 Luna’s factual reliability and clearer communication of results. You can also adjust reasoning effort per request to balance the quality, responsiveness, and cost each task requires.
>
> Match intelligence to each step without rebuilding context
>
> A single application may need different levels of intelligence as a request progresses. You might use GPT-6 Luna to classify incoming requests, GPT-6 Sol to investigate complex cases, and GPT-6 Astra when additional reasoning depth can materially change a decision. This concentrates intelligence where it creates the most value while managing latency and cost across the system.
>
> Within each stage, repeated calls to the same model may reuse instructions, tool definitions, policies, and reference material. Reprocessing that context can erode the efficiency gained by selecting the appropriate model.
>
> GPT-6 Sol and GPT-6 Luna support explicit prompt caching on Amazon Bedrock. You can mark prompt content for reuse, allowing subsequent requests to focus processing on new input. This is useful for coding assistants that reuse repository instructions, support applications grounded in the same policies, and document processes that apply a consistent extraction schema.
>
> Run GPT-6 at scale with performance and control
>
> As AI usage grows, model quality is only part of what determines whether an application succeeds in production. Teams also need infrastructure that maintains performance as demand changes, economics that hold across repeated requests, and controls that protect sensitive data. Amazon Bedrock provides that foundation for GPT-6 Sol and GPT-6 Luna through a high-performance inference engine built for security and reliability at scale.
>
> You can govern model access through AWS Identity and Access Management (IAM) policies and audit every invocation through AWS CloudTrail. Virtual private cloud (VPC) endpoints powered by AWS PrivateLink help keep traffic within your network boundaries. Inference runs on hardware-isolated infrastructure with zero-operator access, so even AWS operators cannot access your prompts or completions during inference.
>
> Your inference data isn’t used for model training, and using GPT-6 Sol and GPT-6 Luna doesn’t require you to opt into sharing your data with OpenAI. For automated abuse detection, classifier-flagged traffic is retained by AWS for up to 30 days and processed programmatically. You can request zero data retention through your AWS account team. See data retention for details.
>
> Get started
>
> You can get started with GPT-6 Sol and GPT-6 Luna in the Amazon Bedrock console or programmatically through supported Amazon Bedrock APIs. For information about supported AWS Regions, endpoints, APIs, features, inference profiles and pricing, see the Amazon Bedrock documentation.
>
> Interested in how Amazon Bedrock can support your team? Connect with us to start the conversation.
>
> About the authors
>
> Tanvi Girinath
>
> Tanvi is a Product Marketing Manager for Amazon Bedrock at Amazon Web Services (AWS), where she helps customers adopt and scale AI applications and agents with Amazon Bedrock.
>
> Chris Dickens
>
> Chris is a Member of Product Staff at OpenAI focused on the OpenAI APIs. His work includes collaboration with AWS on Amazon Bedrock to make OpenAI’s frontier models widely accessible to developers.
>
> Manish Rathaur
>
> Manish is a Senior Product Manager for Amazon Bedrock.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。