---
title: "ai agent --- postgreSQL 关系型数据库"
date: 2026-10-01T03:22:34+08:00
draft: false
entry_kind: "auto"
tags: ["掘金", "工程实践", "来源转写"]
categories: ["AI 工程"]
source: "juejin"
content_mode: "evidence_backed_rewrite"
publication_tier: "B"
source_capture_mode: "full_article"
source_snapshot_sha256: "sha256:13040802e436ea7ea9ac9426d5251bd2b3b5ad9a6b3d9f4623c145e09754ef14"
source_payload_sha256: "sha256:968cefa8fad64ef9981d924896d84ef1d0d899e2dc03b6390e179636a7fe1af4"
source_published_at: 2026-09-30T14:39:55Z
timestamp_confidence: feed
extractor_version: "source-contract-v2"
discovery_method: "article_html"
source_completeness: "complete"
parent_snapshot_sha256: "sha256:8fe50607d4363d2916bb4c41644f644477553860a7f760b04d825b9b3fafe850"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 30
description: "核心结论 PostgreSQL 是免费、开源的对象关系型数据库，与 MySQL 同属关系型数据库范畴。其在 AI Agent 项目中的核心价值在于内置 pgvector 扩展，可直接存储向量并完成相似度检索，无需引入独立的向量数据库。"
external_url: https://juejin.cn/post/7691284233897951295
observation_id: obs_ea76285f58e77f501c97297d73453c6d56aa9b5551c01bce018054e9bb047d1c
revision_id: rev_dc4c495910a228d1e8a22d2f98577e4565b87d3099d539e8088d111c45bcb7cb
event_id: evt_8cc3eb3498d305314f3a186e4743b82f5ba86a1c0a6127bd33e0c9a6e089362b
lineage_relation: original
parent_observation_id: null
first_seen_at: 2026-09-30T19:19:13.939189Z
last_seen_at: 2026-09-30T19:22:34Z
---

## 转写说明

> 本文基于已校验的公开原文进行结构化转写与事实梳理，非原文转载。
> 转写保留可核验的技术事实，并将工程建议与来源观点明确分开。

- **原作者**: snow来了
- **原始来源**: [https://juejin.cn/post/7691284233897951295](https://juejin.cn/post/7691284233897951295)
- **原文发布时间**: Wed, 30 Sep 2026 14:39:55 GMT

## 核心结论

PostgreSQL 是免费、开源的对象关系型数据库，与 MySQL 同属关系型数据库范畴。其在 AI Agent 项目中的核心价值在于内置 pgvector 扩展，可直接存储向量并完成相似度检索，无需引入独立的向量数据库。相较于 MySQL 配合 Milvus 的双组件方案，PostgreSQL 单库即可完成文档存储与向量检索两个环节。

## 能力机制

PostgreSQL 向量检索的工作流程如下：首先将长文本按规则切分为文本块，再由嵌入模型将文本块转换为向量，通过 SQL 语句将文本块与向量一并存入数据库。当用户发起查询时，嵌入模型将问题转换为向量，由 pgvector 计算向量距离并返回最相似的文本块。最终将检索到的文本块拼接入提示词，提交给大语言模型生成回答。

pgvector 支持多种距离算法，不仅仅局限于余弦相似度。需特别注意，问题向量与文档向量必须使用同一嵌入模型生成，否则维度与语义空间不一致，无法进行有效比较。

## 快速开始

安装需准备三个组件：psql 服务端、pgAdmin4 图形化客户端、Node.js 环境下的 pg 包。pgAdmin4 连接数据库后可使用 SQL 语句进行数据操作。

初始化 Node.js 项目并安装依赖：

```bash
mkdir node-pg-demo
cd node-pg-demo
npm init -y
npm install pg dotenv
```

配置环境变量，使用环境变量名称 PGHOST、PGPORT、PGUSER、PGPASSWORD、PGDATABASE。连接数据库后可通过 pool.query 执行查询。创建表示例：

```sql
CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  age INT,
  created_at TIMESTAMPTZ DEFAULT NOW()
)
```

NestJS 项目中使用 TypeORM 配置连接，参数包括 type、host、port、username、password、database。autoLoadEntities 用于自动加载实体，synchronize 在开发环境自动同步表结构。Entity 定义使用 TypeORM 装饰器，Service 层封装 CRUD 操作，Controller 层通过装饰器映射路由。

## 适用边界

PostgreSQL 的优势在于架构简洁：单库同时管理结构化数据与向量数据，减少了组件间数据流转的复杂性。新建项目若无历史包袱，可直接选用 PostgreSQL 加 pgvector 方案。

MySQL 配合 Milvus 的方案在历史项目中仍有适用场景：Milvus 专精向量相似度对比，MySQL 负责结构化数据存储，两者各有专注。pgvector 在向量数量过多时检索能力可能下降，与 Milvus 在大规模向量场景下的性能表现存在差异。两者均可通过合理设计规避各自短板，需根据具体项目规模与已有架构做出选择。

## 核验清单

- [ ] PostgreSQL 服务端、pgAdmin4、pg 包均已正确安装
- [ ] Node.js 环境可成功连接数据库并执行查询
- [ ] 向量检索使用统一嵌入模型生成问题向量与文档向量
- [ ] NestJS 项目通过 TypeORM 正确配置 PostgreSQL 连接
- [ ] Entity、Service、Controller、Module 各层职责明确
- [ ] 生产环境需评估 pgvector 插件的向量规模承载能力

## 来源与核验

- [原始文章](https://juejin.cn/post/7691284233897951295)
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