---
title: Reference your own AWS Secrets Manager secrets in Amazon Bedrock AgentCore
  Identity | Amazon Web Services
date: 2026-06-01 23:28:09+08:00
draft: false
entry_kind: auto
tags:
- 博客与播客
- AI Agent
- 命令行工具
categories:
- AI 工程
scenarios:
- AI/ML项目
- 命令行工具
source: blogs_podcasts
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://aws.amazon.com/blogs/machine-learning/reference-your-own-aws-secrets-manager-secrets-in-amazon-bedrock-agentcore-identity
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:5ee7f36c87a654d01d4bb879e073e948ddcdb709e54b4d1637b56070b2dc97f8
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 105
captured_at: '2026-07-18T04:21:35.087463Z'
source_capture_sha256: sha256:5d403a7e08fdb591ef7a42fd4b88e823fb1699fd2f0a10737233967e6d0e0bf2
source_capture_chars_original: 5916
source_publication_excerpt_chars: 785
source_truncation_reason: historical_capture_limit,historical_publication_excerpt_limit
observation_id: obs_4b054c4815e3a5da1f82d78d902e5b87506c0e21eff45389dfc8fd4226fad13b
revision_id: rev_d91cbc5bac63098dd768eb74162f28b948984371f6e255d9d6a8b2d79003aeb9
event_id: evt_973842ac50af1afd2f9d0d644039dd1212c66c0ba31999648c6d61393cf21f56
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-06-02T00:13:50Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: blogs\_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/reference-your-own-aws-secrets-manager-secrets-in-amazon-bedrock-agentcore-identity](<https://aws.amazon.com/blogs/machine-learning/reference-your-own-aws-secrets-manager-secrets-in-amazon-bedrock-agentcore-identity>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> AI agents are only as powerful as the tools they can access. Whether retrieving customer data from a CRM, posting updates to Slack, or querying a GitHub repository, agents need to call external APIs, and that means securely passing credentials at runtime. Getting that right, without hardcoding secrets in code or exposing them in agent prompts, is one of the defining challenges of building production-ready agentic systems.
>
> Amazon Bedrock AgentCore Identity meets this challenge through credential providers and a token vault that automatically create and manage a secret in AWS Secrets Manager in your account for each Outbound credential provider resource. This secret contains either the API key or client secret along with the other metadata for the external identity provider.…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
