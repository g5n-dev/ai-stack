---
title: 我把本地文档 RAG 做成了可用系统：Flask + Vue3 + LangChain + FAISS（多知识
date: 2026-03-12 11:11:52+08:00
draft: false
entry_kind: auto
tags:
- RAG
- LangChain
- Flask
- Vue3
- FAISS
- 向量检索
- 流式输出
- 本地部署
categories:
- AI 工程
- 后端
source: juejin
description: 这是一篇关于构建**本地化文档 RAG（检索增强生成）系统**的技术项目总结。 该项目针对现有 RAG 演示（Demo）通常缺乏实用性的痛点，构建了一套基于
  **Flask + Vue3 + LangChain + FAISS** 的完整可用系统，并实现了**多知识库管理**与**流式输出**功能。 核心技术栈与架构
external_url: https://juejin.cn/post/7616184939038572579
scenarios:
- RAG应用
- AI/ML项目
content_mode: legacy_analysis
publication_tier: LEGACY
source_provenance: legacy_no_snapshot
source_support: 0.0
---

# 我把本地文档 RAG 做成了可用系统：Flask + Vue3 + LangChain + FAISS（多知识

---

## 基本信息

- **作者**: 心在飞扬AI
- **链接**: [https://juejin.cn/post/7616184939038572579](https://juejin.cn/post/7616184939038572579)

---

## 描述

我把本地文档 RAG 做成了可用系统：Flask + Vue3 + LangChain + FAISS（多知识库 + 流式输出） 很多 RAG Demo 都停留在“能回答一次问题”，但真正要用起来，至

---

## 摘要

这是一篇关于构建**本地化文档 RAG（检索增强生成）系统**的技术项目总结。

该项目针对现有 RAG 演示（Demo）通常缺乏实用性的痛点，构建了一套基于 **Flask + Vue3 + LangChain + FAISS** 的完整可用系统，并实现了**多知识库管理**与**流式输出**功能。

### 核心技术栈与架构
*   **后端**：使用 Python 的 Flask 框架，负责业务逻辑处理。
*   **前端**：采用 Vue3，提供现代化的用户交互界面。
*   **LLM 框架**：集成 LangChain，用于协调大模型与外部数据。
*   **向量存储**：使用 FAISS 进行本地化向量存储与检索，无需依赖昂贵的云向量数据库。
*   **核心功能**：
    *   **多知识库支持**：系统可以管理多个独立的文档库，解决了单一知识库场景受限的问题。
    *   **流式输出**：实现了类似 ChatGPT 的打字机效果，提升了用户体验。

### 项目亮点与实用性
作者强调，本项目不仅仅是“一次性问答”的玩具 Demo，而是注重了系统的**可用性**（Usability）。通过本地部署，用户可以在保证数据隐私的前提下，利用大模型对私有文档进行智能问答和分析。

---

## 学习要点

- 采用 Flask + Vue3 前后端分离架构，通过流式输出技术显著提升用户在长文本生成时的交互体验
- 利用 LangChain 框架集成 FAISS 向量数据库，实现了对本地私有文档的高效检索与精准问答
- 设计多知识库支持功能，允许用户针对不同文档源建立独立索引，有效隔离不同领域的知识背景
- 通过优化文档切分策略与 Prompt 提示词工程，解决了大模型在处理特定领域知识时的幻觉与准确性问题
- 基于开源技术栈构建了一套低成本的本地 RAG（检索增强生成）解决方案，保障了数据隐私与安全性

---

## 常见问题

### 该系统在处理大文件（如超过 100 页的 PDF）时，切分策略是如何设定的？如何避免语义断裂？

在基于 LangChain 和 FAISS 的 RAG 系统中，处理大文件的核心在于文档加载器和文本分割器的配置。
1.  **切分策略**：通常使用 LangChain 的 `RecursiveCharacterTextSplitter`。它会按优先级尝试双换行符、单换行符、空格等进行切分，尽量保持段落的完整性。
2.  **参数设置**：关键参数包括 `chunk_size`（例如 500 或 1000 字符）和 `chunk_overlap`（例如 50-100 字符）。`chunk_overlap` 至关重要，它能确保相邻块之间有重叠内容，从而防止关键信息正好落在两个块的交界处而被截断，有效避免语义断裂。
3.  **元数据保留**：在切分时，建议保留每个 Chunk 所属的源文件名和页码，这样在生成回答时可以追溯来源，提高可信度。

### 系统支持多知识库，但在查询时如何确保从正确的知识库中检索信息，而不是混淆不同库的内容？

实现多知识库隔离主要有两种常见的技术方案：
1.  **元数据过滤**：这是最推荐的方法。在向量化存入 FAISS 时，为每个向量块添加 `metadata` 字段（例如 `{"category": "tech_doc"}` 或 `{"source": "hr_policy"}`）。在查询阶段，通过 LangChain 的 `SelfQueryRetriever` 或在构建 FAISS 检索器时添加 `filter` 参数，强制搜索只在特定的元数据范围内进行。
2.  **多索引映射**：在系统中维护多个 FAISS 索引文件（如 `db_tech.index` 和 `db_hr.index`）。前端在发起请求时携带知识库标识，后端根据标识动态加载对应的 FAISS 实例进行检索。这种方法物理隔离性最好，但切换时会有轻微的 I/O 开销。

### 前端显示流式输出（Streaming）时，如何处理 Markdown 格式的渲染问题？避免出现未闭合的标签导致页面抖动。

这是实现流式 RAG 的典型痛点。由于 Markdown 语法（如 `**` 或 ```）是成对出现的，流式传输可能会将它们拆分到不同的数据包中。
1.  **后端处理**：使用 LangChain 的 `StreamingResponse` 或生成器迭代 Token，逐个或分批发送 SSE (Server-Sent Events) 事件。
2.  **前端处理**：
    *   **累积渲染**：不要对每个单独的 Delta 片段都进行 Markdown 解析。应该维护一个完整的 `fullText` 变量，将每次接收到的文本追加到变量中，然后对整个 `fullText` 进行 Markdown 解析和渲染。
    *   **增量解析库**：如果必须实时渲染格式，可以使用如 `markdown-it` 或 `marked` 等库的流式解析模式，或者使用专门的组件（如 `vue-markdown` 结合防抖策略）来尽量减少格式错误带来的视觉抖动。

### FAISS 向量检索的准确率不高，有哪些优化手段可以提升回答的相关性？

如果检索结果不精准，可以从以下三个维度进行优化：
1.  **调整检索参数**：增加 `k` 值（即检索返回的上下文块数量，例如从 4 增加到 10 或 20），给 LLM 提供更多参考素材。同时，调整 `score_threshold`（相似度阈值），过滤掉相关性过低的内容。
2.  **混合检索**：纯向量搜索对专有名词（如人名、特定型号）往往不敏感。可以结合关键词检索（BM25），使用 LangChain 的 `EnsembleRetriever` 将向量结果和关键词结果加权融合，通常能显著提升召回率。
3.  **重排序**：在检索出大量候选文档后，使用 Rerank 模型（如 Cohere Rerank 或开源的 BGE-Reranker）对结果进行重新打分排序，只取 Top-K 结果传给 LLM，这是提升效果最明显的手段之一。

### 本地部署该系统时，显存不足无法运行大模型，应该如何解决？

本地 RAG 系统的瓶颈通常在于 LLM 推理，而非 FAISS 检索。
1.  **模型量化**：使用 GGUF 或 GPTQ/AWQ 格式的量化模型。例如，使用 Ollama 或 LM Studio 运行量化后的 Llama 3 8B 或 Mistral 7B 模型（4-bit 量化），这可以在仅有 8GB 显存的显卡上流畅运行。
2.  **API 接入**：如果本地硬件实在无法支撑，可以保留 Flask + FAISS 的本地检索逻辑，但在 LangChain 中配置远程 API（

---

## 引用

- **掘金原文**: [https://juejin.cn/post/7616184939038572579](https://juejin.cn/post/7616184939038572579)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [后端](/categories/%E5%90%8E%E7%AB%AF/)
- 标签： [RAG](/tags/rag/) / [LangChain](/tags/langchain/) / [Flask](/tags/flask/) / [Vue3](/tags/vue3/) / [FAISS](/tags/faiss/) / [向量检索](/tags/%E5%90%91%E9%87%8F%E6%A3%80%E7%B4%A2/) / [流式输出](/tags/%E6%B5%81%E5%BC%8F%E8%BE%93%E5%87%BA/) / [本地部署](/tags/%E6%9C%AC%E5%9C%B0%E9%83%A8%E7%BD%B2/)
- 场景： [RAG应用](/scenarios/rag%E5%BA%94%E7%94%A8/) / [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [LangChain文本分割器原理、参数配置与RAG实践]({{< relref "posts/20260306-juejin-splitter学习笔记含rag相关流程与代码实践-1.md" >}})
- [LangChain RAG Loader：网页文档加载、智能分割与检索实现]({{< relref "posts/20260311-juejin-langchain中的rag-loader从网页加载文档并实现智能分割与检索-4.md" >}})
- [LangChain实战：结合Memory与OutputParser构建有记忆的结构化助手]({{< relref "posts/20260210-juejin-langchain-进阶实战当-memory-遇上-outputparser打造有记忆的结构化助手-3.md" >}})
- [ShapedQL：支持多阶段排序与RAG的SQL引擎]({{< relref "posts/20260129-hacker_news-show-hn-shapedql-a-sql-engine-for-multi-stage-rank-6.md" >}})
- [基于AWS与Hugging Face smolagents构建医疗AI智能体]({{< relref "posts/20260223-blogs_podcasts-agentic-ai-with-multi-model-framework-using-huggin-0.md" >}})
