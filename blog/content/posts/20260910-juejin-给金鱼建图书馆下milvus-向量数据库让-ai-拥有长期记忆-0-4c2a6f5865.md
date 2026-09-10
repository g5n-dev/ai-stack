---
title: "💫 给金鱼建图书馆（下）：Milvus 向量数据库，让 AI 拥有长期记忆"
date: 2026-09-10T22:29:01+08:00
draft: false
entry_kind: "auto"
tags: ["掘金", "工程实践", "来源转写"]
categories: ["AI 工程"]
source: "juejin"
content_mode: "evidence_backed_rewrite"
publication_tier: "B"
source_capture_mode: "full_article"
source_snapshot_sha256: "sha256:c0d24c76a07c888c8e9cf67031d134daff1a490884482bd5513cb685adb3eaa0"
source_payload_sha256: "sha256:b4a455a93ed2a82251956298e1b3a3ec6f9c909a6e410e36bbdf9781c97d06d4"
source_published_at: 2026-09-10T13:07:22Z
timestamp_confidence: feed
extractor_version: "source-contract-v2"
discovery_method: "article_html"
source_completeness: "complete"
parent_snapshot_sha256: "sha256:102ad100b89eff52023e70c8dd2adab805ac001d6bb94320f76757c137ce1504"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 37
description: "核心结论 向量数据库解决了对话历史管理中关键词匹配失效的问题。当用户说“我的职业是什么”时，文件中存的是“我是一名数据科学家”，两者没有字面重叠，传统搜索无法命中。Milvus 通过将对话文本转为高维向量，按向量相似度排序检索，语义相近的内容会被排在前面。"
external_url: https://juejin.cn/post/7683753471716606006
observation_id: obs_4c2a6f58655ecc888dd6e362079868be748a5bc9dea57e360560c419ecec1125
revision_id: rev_dcf73df00b07394cee469e12288fdba1c57fa5f22d439b92cb96a5a196f238f8
event_id: evt_91506d92b489974eb5fa888546aff095fa4c4ebc1e8a48b3a5d79df7f9b81e97
lineage_relation: original
parent_observation_id: null
first_seen_at: 2026-09-10T14:26:18.092486Z
last_seen_at: 2026-09-10T14:29:01Z
---

## 转写说明

> 本文基于已校验的公开原文进行结构化转写与事实梳理，非原文转载。
> 转写保留可核验的技术事实，并将工程建议与来源观点明确分开。

- **原作者**: 默\_笙
- **原始来源**: [https://juejin.cn/post/7683753471716606006](https://juejin.cn/post/7683753471716606006)
- **原文发布时间**: Thu, 10 Sep 2026 13:07:22 GMT

## 核心结论

向量数据库解决了对话历史管理中关键词匹配失效的问题。当用户说“我的职业是什么”时，文件中存的是“我是一名数据科学家”，两者没有字面重叠，传统搜索无法命中。Milvus 通过将对话文本转为高维向量，按向量相似度排序检索，语义相近的内容会被排在前面。

短期记忆（截断/总结）与长期记忆（向量检索）并非互斥，而是互补关系。短期记忆保证当前会话的连贯性，长期记忆保证跨会话的知识召回。一种典型的组合模式是：每 N 轮对话生成一次摘要存入 Milvus，新会话启动时从 Milvus 按语义检索相关历史注入 prompt，再交由 LLM 回答。

## 能力机制

Milvus 是专为向量搜索设计的数据库，不支持日期类型，时间字段需用 VarChar 存 ISO 格式字符串。它由 etcd（元数据存储）、MinIO（对象存储）、Milvus 主服务三个容器组成，启动命令为 `docker compose -f ./milvus-standalone-docker-compose.yml up -d`，服务监听 19530 端口。

集合（Collection）是 Milvus 中的顶层结构，对应关系型数据库的“表”。集合包含多个字段：id（VarChar，主键）、vector（FloatVector，语义向量）、content（VarChar，原文）、round（Int64，对话轮次）、timestamp（VarChar，时间戳）。向量的维度由 embedding 模型决定，来源中使用 1024 维。

在搜索前必须为向量字段创建索引，否则需要遍历全部数据计算距离。来源中使用了 IVF_FLAT 索引类型（分桶搜索）和 COSINE 相似度度量（用向量夹角衡量语义相似度）。搜索时通过 `client.search()` 传入查询向量和 limit 参数（返回最相似的 k 条），结果包含原始 content 字段。

集合创建后默认不在内存中，每次重启需要手动加载：`client.loadCollection()`。这一设计是性能和内存的权衡。

## 快速开始

环境准备：Milvus 服务、Docker Compose 环境、Node.js 环境。

安装依赖：

```bash
pnpm i @zilliz/milvus2-sdk-node
pnpm i @langchain/openai dotenv
```

使用环境变量管理密钥，包括 OPENAI_API_KEY、EMBEDDING_MODEL_NAME、OPENAI_BASE_URL。

启动 Milvus：

```bash
docker compose -f ./milvus-standalone-docker-compose.yml up -d
```

创建集合并插入数据的基本流程：建立 MilvusClient 连接，创建集合（含 id、vector、content、round、timestamp 字段），为 vector 字段创建 IVF_FLAT 索引和 COSINE 相似度度量，加载集合，通过 embedding 模型将文本转为向量后插入。

语义检索流程：用户问题通过 embedding 模型转为向量，调用 `client.search()` 检索最相似的 k 条记录，将检索到的 content 字段格式化后注入 prompt，调用 LLM 回答，最后将新对话经 embedding 后存入 Milvus。

## 适用边界

Milvus 是向量搜索专用数据库，不适合需要复杂关系查询或日期类型存储的场景。关键词匹配失效、但语义关联明确的使用案例适合引入向量数据库，例如客服对话历史检索、用户画像跨会话召回、文档语义搜索等。

向量检索的计算开销高于简单截断或总结，适合对信息完整性要求高、且历史数据量达到一定规模（单会话无法容纳全部对话）的场景。对于简单abot 场景，截断或总结策略的性价比更高。

来源中提到的记忆架构是三层协作：短期记忆（内存/文件）管理当前会话，中期总结存入文件或向量库，长期记忆通过 Milvus 召回。三种策略可以组合使用——用总结压缩 token，用检索保留完整语义。

## 核验清单

确认 Milvus 服务已在 19530 端口正常运行。使用 `docker compose` 命令启动多容器应用时，需要对应的 docker-compose.yml 配置文件。

集合创建时需指定字段名称和数据类型，且向量维度必须与 embedding 模型输出维度一致。索引创建后才能进行高效搜索，索引字段为 vector，索引类型和度量类型需根据场景选择。

检索前需确保集合已加载到内存。环境变量需正确配置，包括 API 密钥和模型名称。向量化依赖 OpenAIEmbeddings 或其他兼容的 embedding 模型。

## 来源与核验

- [原始文章](https://juejin.cn/post/7683753471716606006)
- 页面事实以原始来源及其引用的官方资料为准；版本、星标和模型能力会随时间变化。
- AI Stack 不公开抓取到的全文快照，只发布独立转写与来源入口。

---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [掘金](/tags/%E6%8E%98%E9%87%91/) / [工程实践](/tags/%E5%B7%A5%E7%A8%8B%E5%AE%9E%E8%B7%B5/) / [来源转写](/tags/%E6%9D%A5%E6%BA%90%E8%BD%AC%E5%86%99/)

### 相关文章

- [6.结构化输出](/posts/20260718-juejin-6%E7%BB%93%E6%9E%84%E5%8C%96%E8%BE%93%E5%87%BA-0-80d50ad8af/)
- [GitHub Copilot for JetBrains 架构拆解：Provider / Endpoint / Skills / Sandbox / Polic](/posts/20260718-juejin-github-copilot-for-jetbrains-%E6%9E%B6%E6%9E%84%E6%8B%86%E8%A7%A3provider-endpoint-0-2a917f4cdc/)
- [从 Token 到 RAG：我这一周搭起的大模型基础认知地图](/posts/20260718-juejin-%E4%BB%8E-token-%E5%88%B0-rag%E6%88%91%E8%BF%99%E4%B8%80%E5%91%A8%E6%90%AD%E8%B5%B7%E7%9A%84%E5%A4%A7%E6%A8%A1%E5%9E%8B%E5%9F%BA%E7%A1%80%E8%AE%A4%E7%9F%A5%E5%9C%B0%E5%9B%BE-0-cd9514ced7/)
- [从零到一手撸 Agent 系列 — 第 1 篇：一个 Coding Agent 是什么？](/posts/20260718-juejin-%E4%BB%8E%E9%9B%B6%E5%88%B0%E4%B8%80%E6%89%8B%E6%92%B8-agent-%E7%B3%BB%E5%88%97-%E7%AC%AC-1-%E7%AF%87%E4%B8%80%E4%B8%AA-coding-agent-%E6%98%AF%E4%BB%80%E4%B9%88-0-b0628f7a64/)
- [从BFF到SSE：我在Vue项目里藏了个“AI翻译官”](/posts/20260719-juejin-%E4%BB%8Ebff%E5%88%B0sse%E6%88%91%E5%9C%A8vue%E9%A1%B9%E7%9B%AE%E9%87%8C%E8%97%8F%E4%BA%86%E4%B8%AAai%E7%BF%BB%E8%AF%91%E5%AE%98-0-9ec70466e8/)