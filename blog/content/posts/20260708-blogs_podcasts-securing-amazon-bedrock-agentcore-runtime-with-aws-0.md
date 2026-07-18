---
title: Securing Amazon Bedrock AgentCore Runtime with AWS WAF | Amazon Web Services
date: 2026-07-08 16:56:13+08:00
draft: false
entry_kind: auto
tags:
- 博客与播客
- AI Agent
- 生成式 AI
- Docker
categories:
- AI 工程
scenarios:
- AI/ML项目
- 云原生/容器
source: blogs_podcasts
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://aws.amazon.com/blogs/machine-learning/securing-amazon-bedrock-agentcore-runtime-with-aws-waf
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:cce8fbcc5c64e361bc45cf72f109c9504b00e97f9489075021e29e6b922dc684
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 76
captured_at: '2026-07-18T04:21:52.714593Z'
source_capture_sha256: sha256:26247de71a2ef920cda42343a63c35073ac2d7601fa3c48a9031e6241d728561
source_capture_chars_original: 5837
source_publication_excerpt_chars: 799
source_truncation_reason: historical_capture_limit,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: blogs\_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/securing-amazon-bedrock-agentcore-runtime-with-aws-waf](<https://aws.amazon.com/blogs/machine-learning/securing-amazon-bedrock-agentcore-runtime-with-aws-waf>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> When you deploy generative AI agents with Amazon Bedrock AgentCore as production API endpoints, you might want to enforce web application firewall policies, rate limiting, protection against common web threats, or audit controls via AWS WAF .
>
> AWS WAF integrates with Elastic Load Balancing Application Load Balancers \(ALBs\), Amazon CloudFront distributions, and Amazon API Gateway REST APIs. We use an internet-facing ALB as the integration point: it passes headers through transparently, supports VPC-internal routing, and attaches directly to an AWS WAF WebACL. From there, you route traffic to AgentCore through a VPC Interface Endpoint for the Bedrock AgentCore data plane service.
>
> This is where the challenge appears. ALBs require health checks to verify that backend targets are responsive.…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
