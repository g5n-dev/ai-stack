---
title: "Building Prometheus: How Backend Aggregation Enables Gi"
date: 2026-02-10T19:57:28+08:00
draft: false
entry_kind: "auto"
tags: ["blogs_podcasts"]
categories: ["效率与方法论"]
source: blogs_podcasts
description: "这篇文章介绍了Meta在构建吉瓦级AI集群（如Prometheus）时，**后端聚合（BAG）**技术所起的关键作用。 **核心内容总结如下：** 1. **实现大规模连接**：BAG技术使得Meta能够无缝连接分布在多个数据中心和不同区域的数千个GPU，从而构建起庞大的AI算力集群。 2. **网络架构融合**：BA"
external_url: https://engineering.fb.com/2026/02/09/data-center-engineering/building-prometheus-how-backend-aggregation-enables-gigawatt-scale-ai-clusters
scenarios: ["Web应用开发"]
---

# Building Prometheus: How Backend Aggregation Enables Gigawatt-Scale AI Clusters

---

## 基本信息

- **来源**: Meta Engineering (blog)
- **发布时间**: 2026-02-09T17:00:33+00:00
- **链接**: [https://engineering.fb.com/2026/02/09/data-center-engineering/building-prometheus-how-backend-aggregation-enables-gigawatt-scale-ai-clusters](https://engineering.fb.com/2026/02/09/data-center-engineering/building-prometheus-how-backend-aggregation-enables-gigawatt-scale-ai-clusters)

---
## 摘要/简介

We’re sharing details of the role backend aggregation (BAG) plays in building Meta’s gigawatt-scale AI clusters like Prometheus. BAG allows us to seamlessly connect thousands of GPUs across multiple data centers and regions. Our BAG implementation is connecting two different network fabrics – Disaggregated Schedule Fabric (DSF) and Non-Scheduled Fabric (NSF). Once it’s complete our AI [...] Read More... The post Building Prometheus: How Backend Aggregation Enables Gigawatt-Scale AI Clusters appeared first on Engineering at Meta .

---
## 导语

在构建千兆瓦级 AI 集群的过程中，后端聚合技术（BAG）成为了连接海量算力的关键纽带。本文深入解析 Meta 如何利用该技术打破物理限制，实现跨数据中心与区域的无缝 GPU 互联。通过探讨 BAG 如何融合 DSF 与 NSF 两种不同的网络架构，读者将了解支撑超大规模 AI 基础设施落地的核心网络设计思路。

---
## 摘要

这篇文章介绍了Meta在构建吉瓦级AI集群（如Prometheus）时，**后端聚合（BAG）**技术所起的关键作用。

**核心内容总结如下：**

1.  **实现大规模连接**：BAG技术使得Meta能够无缝连接分布在多个数据中心和不同区域的数千个GPU，从而构建起庞大的AI算力集群。
2.  **网络架构融合**：BAG的具体实现涉及连接两种不同的网络架构——**分散调度网络（DSF）**和**非调度网络（NSF）**。通过这种融合，优化了集群内部的数据传输与调度能力。

简而言之，BAG是Meta支撑超大规模AI基础设施的核心网络技术，确保了跨地域海量算力的高效互联。

---
## 引用

- **文章/节目**: [https://engineering.fb.com/2026/02/09/data-center-engineering/building-prometheus-how-backend-aggregation-enables-gigawatt-scale-ai-clusters](https://engineering.fb.com/2026/02/09/data-center-engineering/building-prometheus-how-backend-aggregation-enables-gigawatt-scale-ai-clusters)
- **RSS 源**: [https://engineering.fb.com/feed/](https://engineering.fb.com/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [效率与方法论](/categories/%E6%95%88%E7%8E%87%E4%B8%8E%E6%96%B9%E6%B3%95%E8%AE%BA/)
- 标签： [blogs_podcasts](/tags/blogs-podcasts/)
- 场景： [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/)

### 相关文章

- [OpenAI与Anthropic模型之争：Claude Opus 4.6对决GPT 5.3 Codex]({{< relref "posts/20260210-blogs_podcasts-ainews-openai-and-anthropic-go-to-war-claude-opus--8.md" >}})
- [OpenAI在ChatGPT测试广告以支持免费访问]({{< relref "posts/20260210-blogs_podcasts-testing-ads-in-chatgpt-1.md" >}})
- [Transformers.js v4 预览版已发布 NPM]({{< relref "posts/20260210-blogs_podcasts-transformersjs-v4-preview-now-available-on-npm-3.md" >}})
- [Transformers.js v4 Preview: Now Available on NPM]({{< relref "posts/20260210-blogs_podcasts-transformersjs-v4-preview-now-available-on-npm-4.md" >}})
- [🔥GPT-5职场革命！企业如何用AI重塑生产力？🚀]({{< relref "posts/20260127-blogs_podcasts-inside-gpt-5-for-work-how-businesses-use-gpt-5-9.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*