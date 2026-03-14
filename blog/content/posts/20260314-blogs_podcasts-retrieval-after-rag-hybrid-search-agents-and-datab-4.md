---
title: "RAG 之后的检索：混合搜索、智能体与数据库设计"
date: 2026-03-14T03:08:48+08:00
draft: false
entry_kind: "auto"
tags: ["RAG", "混合搜索", "向量检索", "数据库设计", "AI 智能体", "BM25", "重排序", "Turbopuffer"]
categories: ["AI 工程", "数据"]
source: blogs_podcasts
description: "这段内容主要来自 Turbopuffer 联合创始人 Simon Hørup Eskildsen 的技术分享，核心围绕 **RAG（检索增强生成）之后的“检索”阶段**，探讨如何通过混合搜索、Agent 以及数据库设计来优化 AI 应用。 以下是主要内容总结： 1. 背景与起源 Turbopuffer 起源于一个阅读类"
external_url: https://www.latent.space/p/turbopuffer
scenarios: ["RAG应用", "AI/ML项目"]
---

# RAG 之后的检索：混合搜索、智能体与数据库设计

---

## 基本信息

- **来源**: Latent Space (blog)
- **发布时间**: 2026-03-12T22:56:01+00:00
- **链接**: [https://www.latent.space/p/turbopuffer](https://www.latent.space/p/turbopuffer)

---
## 摘要/简介

Turbopuffer 源于一个阅读应用。

---
## 导语

检索增强生成（RAG）虽然提升了大模型回答的准确性，但检索环节本身往往成为性能瓶颈。Turbopuffer 创始人 Simon Hørup Eskildsen 在本文中深入探讨了 RAG 之后的进阶路径，解析了混合检索、智能代理与数据库设计的协同作用。通过剖析从阅读应用到通用数据库的演进历程，文章为开发者提供了优化检索架构、平衡延迟与精度的实用视角。

---
## 摘要

这段内容主要来自 Turbopuffer 联合创始人 Simon Hørup Eskildsen 的技术分享，核心围绕 **RAG（检索增强生成）之后的“检索”阶段**，探讨如何通过混合搜索、Agent 以及数据库设计来优化 AI 应用。

以下是主要内容总结：

### 1. 背景与起源
Turbopuffer 起源于一个阅读类应用。在开发过程中，团队发现传统的向量检索在实际应用中存在局限性，因此转向构建更优的检索基础设施，旨在解决 AI 时代数据检索的效率和精度问题。

### 2. 混合搜索
单纯的向量搜索往往不足以应对复杂的查询需求。
*   **局限性**：向量搜索擅长语义理解，但在处理精确匹配（如专有名词、ID）时表现不佳。
*   **解决方案**：**混合搜索**（Hybrid Search）结合了**向量搜索**（语义相关性）和**关键词搜索**（BM25，字面匹配）。
*   **重排序**：在初步检索后，通常需要使用 Cross-encoder 或其他模型对结果进行精细的重排序，以平衡语义匹配和精确匹配，从而获得最相关的结果。

### 3. Agents（智能体）与检索
随着 AI Agent 的发展，检索模式正在发生变化。
*   **从单一到多跳**：Agent 的任务往往需要多步推理，检索不再是“一次性”的动作，而是一个循环、迭代的过程。
*   **工具使用**：Agent 需要将数据库作为工具，能够自主构建查询、过滤数据并根据检索结果调整下一步行动。
*   **自我修正**：Agent 系统需要具备判断检索质量的能力，如果结果不佳，能够自我修正并重新检索。

### 4. 数据库设计
为了支撑上述的混合搜索和 Agent 交互，底层数据库的设计至关重要：
*   **性能与扩展性**：传统的向量数据库在处理大规模数据或复杂过滤时往往面临性能瓶颈。Turbopuffer 提倡了一种基于 PostgreSQL 架构或专门优化的存储方案，以实现更快的检索速度和更灵活的过滤能力。
*   **基础设施的重要性**：高效的 RAG 系统不仅依赖大模型，更依赖底层数据库的查询吞吐量和延迟表现。

**总结**：Simon 强调，RAG 的成功关键在于“检索”本身。

---
## 学习要点

- RAG 系统的核心瓶颈通常在于检索而非生成，提升检索质量（特别是混合检索）比单纯优化模型参数更能有效改善最终答案的准确性。
- 向量数据库并非必须，通过将向量存储为 PostgreSQL 中的列并利用 SIMD 指令加速，可以在不牺牲太多性能的前提下实现更简单、更廉价的架构。
- 混合检索（结合关键词 BM25 和语义向量搜索）优于单一的向量搜索，因为它能同时精准匹配专有名词并理解语义意图。
- 在处理大规模数据时，近似最近邻（ANN）搜索中的 HNSW 算法虽然性能强大，但会占用大量内存，需要根据数据规模和硬件成本权衡索引策略。
- 智能体在检索过程中不应仅依赖一次性检索，而应具备根据上下文自主判断何时检索、检索什么以及如何重新检索的能力。
- 数据库设计应服务于查询模式，在构建 RAG 应用时，需要预先考虑如何切分文本块以及如何通过元数据过滤来提高检索的精确度。
- 评估 RAG 系统时，应关注检索系统的召回率与精确度，并建立针对检索环节的专门测试指标，而不是仅关注生成模型的表面效果。

---
## 引用

- **文章/节目**: [https://www.latent.space/p/turbopuffer](https://www.latent.space/p/turbopuffer)
- **RSS 源**: [https://www.latent.space/feed](https://www.latent.space/feed)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [数据](/categories/%E6%95%B0%E6%8D%AE/)
- 标签： [RAG](/tags/rag/) / [混合搜索](/tags/%E6%B7%B7%E5%90%88%E6%90%9C%E7%B4%A2/) / [向量检索](/tags/%E5%90%91%E9%87%8F%E6%A3%80%E7%B4%A2/) / [数据库设计](/tags/%E6%95%B0%E6%8D%AE%E5%BA%93%E8%AE%BE%E8%AE%A1/) / [AI 智能体](/tags/ai-%E6%99%BA%E8%83%BD%E4%BD%93/) / [BM25](/tags/bm25/) / [重排序](/tags/%E9%87%8D%E6%8E%92%E5%BA%8F/) / [Turbopuffer](/tags/turbopuffer/)
- 场景： [RAG应用](/scenarios/rag%E5%BA%94%E7%94%A8/) / [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [RAG后的检索优化：混合搜索、Agent与数据库设计]({{< relref "posts/20260313-blogs_podcasts-retrieval-after-rag-hybrid-search-agents-and-datab-3.md" >}})
- [Retrieval After RAG：混合搜索、智能体与数据库设计]({{< relref "posts/20260313-blogs_podcasts-retrieval-after-rag-hybrid-search-agents-and-datab-1.md" >}})
- [Turbopuffer谈RAG之后：混合搜索、Agent与数据库设计]({{< relref "posts/20260313-blogs_podcasts-retrieval-after-rag-hybrid-search-agents-and-datab-0.md" >}})
- [Turbopuffer 源自阅读应用的数据库设计]({{< relref "posts/20260313-blogs_podcasts-retrieval-after-rag-hybrid-search-agents-and-datab-2.md" >}})
- [RAG后的检索优化：混合搜索、Agent与数据库设计]({{< relref "posts/20260313-blogs_podcasts-retrieval-after-rag-hybrid-search-agents-and-datab-4.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*