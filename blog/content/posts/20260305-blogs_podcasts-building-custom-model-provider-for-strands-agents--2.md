---
title: Building custom model provider for Strands Agents with LLMs hosted on SageMaker
  AI endpoints | Amazon Web Services
date: 2026-03-05 17:47:47+08:00
draft: false
entry_kind: auto
tags:
- 博客与播客
- AI Agent
- 大语言模型
- Docker
categories:
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
- 云原生/容器
source: blogs_podcasts
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://aws.amazon.com/blogs/machine-learning/building-custom-model-provider-for-strands-agents-with-llms-hosted-on-sagemaker-ai-endpoints
aliases:
- /posts/20260305-blogs_podcasts-building-custom-model-provider-for-strands-agents--3/
- /posts/20260306-blogs_podcasts-building-custom-model-provider-for-strands-agents--10/
- /posts/20260306-blogs_podcasts-building-custom-model-provider-for-strands-agents--3/
- /posts/20260306-blogs_podcasts-building-custom-model-provider-for-strands-agents--4/
- /posts/20260306-blogs_podcasts-building-custom-model-provider-for-strands-agents--5/
- /posts/20260306-blogs_podcasts-building-custom-model-provider-for-strands-agents--6/
- /posts/20260306-blogs_podcasts-building-custom-model-provider-for-strands-agents--9/
- /posts/20260307-blogs_podcasts-building-custom-model-provider-for-strands-agents--10/
- /posts/20260307-blogs_podcasts-building-custom-model-provider-for-strands-agents--9/
- /posts/20260308-blogs_podcasts-building-custom-model-provider-for-strands-agents--10/
- /posts/20260309-blogs_podcasts-building-custom-model-provider-for-strands-agents--10/
- /posts/20260309-blogs_podcasts-building-custom-model-provider-for-strands-agents--11/
- /posts/20260309-blogs_podcasts-building-custom-model-provider-for-strands-agents--12/
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:e1f1c63401ea6fac3ee4c87f79b96aa5778920870355301104faa5f540ce5587
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 114
captured_at: '2026-07-18T04:18:34.545294Z'
source_capture_sha256: sha256:cdfc7dec5fe0fe0e137d4d3877642768c0a454cba34cecc94ae0d696efdd9a11
source_capture_chars_original: 5738
source_publication_excerpt_chars: 797
source_truncation_reason: historical_capture_limit,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: blogs\_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/building-custom-model-provider-for-strands-agents-with-llms-hosted-on-sagemaker-ai-endpoints](<https://aws.amazon.com/blogs/machine-learning/building-custom-model-provider-for-strands-agents-with-llms-hosted-on-sagemaker-ai-endpoints>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> Organizations increasingly deploy custom large language models \(LLMs\) on Amazon SageMaker AI real-time endpoints using their preferred serving frameworks—such as SGLang, vLLM, or TorchServe—to help gain greater control over their deployments, optimize costs, and align with compliance requirements. However, this flexibility introduces a critical technical challenge: response format incompatibility with Strands agents. While these custom serving frameworks typically return responses in OpenAI-compatible formats to facilitate broad environment support, Strands agents expect model responses aligned with the Bedrock Messages API format.
>
> The challenge is particularly significant because support for the Messages API is not guaranteed for the models hosted on SageMaker AI real-time endpoints.…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
