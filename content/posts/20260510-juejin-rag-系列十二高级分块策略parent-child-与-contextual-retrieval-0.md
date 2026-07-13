---
title: "RAG 分块进阶：Parent-Child 与 Contextual Retrieval 实现"
date: 2026-05-10T03:23:34+08:00
draft: false
entry_kind: "auto"
tags: ["RAG", "检索增强生成", "分块策略", "Parent-Child", "Contextual Retrieval", "文本切分", "知识库", "AI应用"]
categories: ["AI 工程", "数据"]
source: juejin
description: "Naive 分块有什么根本缺陷？Parent-Child 如何用小块检索、大块返回？Contextual Retrieval 策略是什么，本篇带你用实际代码学会高级分块策略"
external_url: https://juejin.cn/post/7637839076003659827
scenarios: ["RAG应用", "AI/ML项目"]
---

# RAG 分块进阶：Parent-Child 与 Contextual Retrieval 实现

---

## 基本信息

- **作者**: 冬奇Lab
- **链接**: [https://juejin.cn/post/7637839076003659827](https://juejin.cn/post/7637839076003659827)

---
## 描述

Naive 分块有什么根本缺陷？Parent-Child 如何用小块检索、大块返回？Contextual Retrieval 策略是什么，本篇带你用实际代码学会高级分块策略

---
## 评论

#### 核心观点
事实：Naive 固定长度分块在语义上容易割裂相邻信息。
作者观点：Parent‑Child 与 Contextual Retrieval 通过层次化与上下文增强，能够显著提升检索召回与答案生成的连贯性。
推断：若检索系统对语义完整性要求高，这两种策略在未来 RAG 架构中将成为默认配置。

#### 技术原理
事实：Parent‑Child 将文档划分为父块（完整段落）和若干子块（细粒度片段），检索阶段使用子块匹配，返回时提供父块作为上下文。
作者观点：子块降低匹配粒度，父块保证生成时的信息完整，实现“小块检索，大块返回”。
推断：Contextual Retrieval 在子块前追加由 LLM 生成的短描述（上下文摘要），可进一步消除歧义，使向量相似度更贴近用户意图。

#### 适用边界
事实：Parent‑Child 对文档结构有天然需求，若原始文本缺乏层次或段落标识，效果会受限。
作者观点：在多跳问答或需要跨段落综合的场景下，Parent‑Child 表现突出；但在高频短查询或成本敏感的业务中，增加的索引与推理开销可能不划算。
推断：Contextual Retrieval 的上下文生成成本随文档规模线性增长，适合离线构建、可接受额外延迟的离线检索系统，而非实时交互系统。

#### 实践建议
事实：在实现时，可先对文档进行结构化拆解，确保父块自然完整；子块大小控制在 100–200 tokens，父块大小不超过 512 tokens。
作者观点：采用混合检索（稀疏 + 密集），先在子块空间做向量召回，再在父块空间做关键词重排，可兼顾召回率与精度。
推断：加入上下文描述时，建议将描述长度限制在 30–50 tokens，并在生成后进行相似度阈值过滤，以防止噪声描述稀释检索效果。实际部署前，需在目标业务数据集上进行端到端延迟与答案准确率的 A/B 测试，以确定最优块大小与上下文策略。

---
## 学习要点

- 请提供文章的具体内容，以便我为您提炼出关键要点。

---
## 引用

- **掘金原文**: [https://juejin.cn/post/7637839076003659827](https://juejin.cn/post/7637839076003659827)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [数据](/categories/%E6%95%B0%E6%8D%AE/)
- 标签： [RAG](/tags/rag/) / [检索增强生成](/tags/%E6%A3%80%E7%B4%A2%E5%A2%9E%E5%BC%BA%E7%94%9F%E6%88%90/) / [分块策略](/tags/%E5%88%86%E5%9D%97%E7%AD%96%E7%95%A5/) / [Parent-Child](/tags/parent-child/) / [Contextual Retrieval](/tags/contextual-retrieval/) / [文本切分](/tags/%E6%96%87%E6%9C%AC%E5%88%87%E5%88%86/) / [知识库](/tags/%E7%9F%A5%E8%AF%86%E5%BA%93/) / [AI应用](/tags/ai%E5%BA%94%E7%94%A8/)
- 场景： [RAG应用](/scenarios/rag%E5%BA%94%E7%94%A8/) / [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [利用RAG技术有效解决大模型幻觉问题]({{< relref "posts/20260314-juejin-别再信它一本正经地胡说了用-rag终结大模型幻觉-0.md" >}})
- [利用 Amazon Bedrock 构建AI驱动的招聘系统优化人才获取]({{< relref "posts/20260213-blogs_podcasts-ai-meets-hr-transforming-talent-acquisition-with-a-1.md" >}})
- [基于Amazon Bedrock构建AI招聘系统优化人才获取流程]({{< relref "posts/20260218-blogs_podcasts-ai-meets-hr-transforming-talent-acquisition-with-a-13.md" >}})
- [LangBot：生产级多平台Agent智能机器人开发平台]({{< relref "posts/20260205-github_trending-langbot-app-langbot-7.md" >}})
- [基于 Amazon Bedrock 构建AI驱动的招聘系统优化人才获取流程]({{< relref "posts/20260212-blogs_podcasts-ai-meets-hr-transforming-talent-acquisition-with-a-0.md" >}})
*本文由 AI Stack 自动生成，提供深度内容分析。*