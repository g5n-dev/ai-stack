---
title: 易车 × Apache Doris：构建湖仓一体新架构，加速 AI 业务融合实践
date: 2026-03-06 09:25:00+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- MCP
- AI Agent
- 数据库
categories:
- AI 工程
- 数据
scenarios:
- AI/ML项目
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7613680097549762575
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:2dcfefc4d2d3e8c8695a715388a83756ddd5b8b8e6f3d1b186af1a4f9e982190
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 40
captured_at: '2026-07-18T04:18:38.835821Z'
source_capture_sha256: sha256:0afead7b5ac2d76a53825efb8abf82d5ec9f6b5e1ec04e3076c0df4b59d5e760
source_capture_chars_original: 4345
source_publication_excerpt_chars: 760
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_a1fb33c8dff1b050df08d8952a341dcb7fccc9660c4d02f9c983a8b46e901521
revision_id: rev_9629f0b2fa590bd24f703e77f8d6f0c8e55df01de421bb2aaca64e4f13cac5f2
event_id: evt_664b473bde551c6a9aa65d9d3d3f2e80e873191106ab89d579a1d3e6adec1790
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-03-06T01:25:00Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7613680097549762575](<https://juejin.cn/post/7613680097549762575>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 导读：
> 易车引入 Apache Doris 取得以下核心成果：
> 替换 Druid、Kudu、ClickHouse 等近 10 种数据引擎
> 构建 Apache Doris + Paimon + Hive 湖仓架构
> 探索 Doris + AI（ChatBI、Data Agent）融合应用
> 覆盖实时多维分析、用户画像、BI 报表等核心场景
> 数据的爆发式增长与业务对实时性的极致追求，驱动易车技术团队在实时湖仓建设上持续探索。目前易车已基于 Apache Doris + Paimon + Hive 构建了湖仓一体化数据平台，实现架构收敛统一：
> 逐步替换 Druid、Kudu、HBase、MongoDB、ClickHouse 等近 10 种引擎。
> 广泛应用于实时多维分析、用户画像及标签体系、BI 报表（实时报表、仪表盘）等核心场景。在此基础上，团队进一步探索
> Apache Doris +
> AI
> 的融合应用
> ，为智能化业务提供实时、统一的数据底座。本文将具体讲述易车数据平台架构的演进及具体实践。
> 一、早期架构：多引擎混用，流批难统一
> 易车数据平台的数据源丰富多样，涵盖业务日志、业务数据库（RDS/自建库）、消息系统、接口数据、第三方 API 及应用程序等。
> 团队通过内部数据集成工具将多源数据统一接入数据平台：底层离线数仓以 Hive 为主、基于 Hudi 构建数据湖；半结构化数据则主要存储在 Elasticsearch、HBase、MongoDB 中。
> 在 OLAP 引擎层面，团队先后使用过 Kudu、Kylin、Druid、ClickHouse 等多种引擎，即席分析 MPP 架构方面则使用了 Impala、Spark、Presto 等计算引擎，为数据分析、实时大屏、实时指标、个性化推荐等上层应用提供服务。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
