---
title: Scaling PostgreSQL to power 800 million ChatGPT users
date: 2026-01-25 12:39:55+08:00
draft: false
entry_kind: auto
tags:
- 博客与播客
- 数据库
categories:
- 数据
scenarios: []
source: blogs_podcasts
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://openai.com/index/scaling-postgresql
aliases:
- /posts/20260126-blogs_podcasts-scaling-postgresql-to-power-800-million-chatgpt-us-2/
- /posts/20260126-blogs_podcasts-scaling-postgresql-to-power-800-million-chatgpt-us-3/
- /posts/20260127-blogs_podcasts-scaling-postgresql-to-power-800-million-chatgpt-us-3/
- /posts/20260127-blogs_podcasts-scaling-postgresql-to-power-800-million-chatgpt-us-4/
- /posts/20260127-blogs_podcasts-scaling-postgresql-to-power-800-million-chatgpt-us-5/
- /posts/20260127-blogs_podcasts-scaling-postgresql-to-power-800-million-chatgpt-us-7/
- /posts/20260127-blogs_podcasts-scaling-postgresql-to-power-800-million-chatgpt-us-8/
- /posts/20260127-blogs_podcasts-scaling-postgresql-to-power-800-million-chatgpt-us-9/
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:b475ff6ed6f05f19e76a513e19272fd892b1f0e0f4fd17c71883b1cd9b742009
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 53
captured_at: '2026-07-18T04:11:29.694091Z'
source_capture_sha256: sha256:51708177830d9e0f0a9aaef73512c6cfec7aeb1ac584b693cf79ca2349adf3e8
source_capture_chars_original: 5882
source_publication_excerpt_chars: 602
source_truncation_reason: historical_capture_limit,historical_publication_excerpt_limit
observation_id: obs_89a221162f32c17ddc19377e1b50b84e5b55da0e618a54b1edad14a99c1e4792
revision_id: rev_21b9bd61d4441d8bf52f3b4d97376ed006a994376a7b02543a69bdcdca4ab54f
event_id: evt_1dd1912a3d4a64aa38a3c3f5b183bbec2f9f3aaeced379b51a52ccc9d9f1a80d
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: blogs\_podcasts
- **原始来源**: [https://openai.com/index/scaling-postgresql](<https://openai.com/index/scaling-postgresql>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> By Bohan Zhang, Member of the Technical Staff
>
> For years, PostgreSQL has been one of the most critical, under-the-hood data systems powering core products like ChatGPT and OpenAI’s API. As our user base grows rapidly, the demands on our databases have increased exponentially, too. Over the past year, our PostgreSQL load has grown by more than 10x, and it continues to rise quickly.
>
> Our efforts to advance our production infrastructure to sustain this growth revealed a new insight: PostgreSQL can be scaled to reliably support much larger read-heavy workloads than many previously thought possible.…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
