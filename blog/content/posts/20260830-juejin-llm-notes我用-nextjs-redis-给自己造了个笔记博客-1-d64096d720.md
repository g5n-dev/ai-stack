---
title: "🏠 「LLM Notes」：我用 Next.js + Redis 给自己造了个笔记博客"
date: 2026-08-30T20:56:26+08:00
draft: false
entry_kind: "auto"
tags: ["掘金", "工程实践", "来源转写"]
categories: ["AI 工程"]
source: "juejin"
content_mode: "evidence_backed_rewrite"
publication_tier: "B"
source_capture_mode: "full_article"
source_snapshot_sha256: "sha256:6e0a2e870965a8c269fb24dfcf09cf75ce419da825ecedce9278468ad9196a5d"
source_payload_sha256: "sha256:88b8da99575702dbf13a9a86f9e06678cc68284433cd5c87d2b53b7c8ca579c9"
source_published_at: 2026-08-30T11:14:59Z
timestamp_confidence: feed
extractor_version: "source-contract-v2"
discovery_method: "article_html"
source_completeness: "complete"
parent_snapshot_sha256: "sha256:edd322a0fee2779187c9b19154fcbc5d3a042b2d048a3eab6bf28ac5743de143"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 43
description: "核心结论 该笔记系统基于 Next.js 脚手架构建，采用 React Server Component 与客户端组件分层协作的架构。数据存储选用 Redis 作为 key:value 内存数据库，利用 hash 类型存取笔记内容。组件规划遵循规范驱动编程方法，先绘制组件树再落笔实现代码。"
external_url: https://juejin.cn/post/7679341637068898313
observation_id: obs_d64096d720de8323f9a028fafb38f1ab468b15228184ef8a3de7ab24f9983b4d
revision_id: rev_905066672b94a2c71c8746d8b365cd6246331fe571bfcd1c026d594bd6cc788c
event_id: evt_f3c69c4ad01faf65c8a5dcd429d73b10ea9813bb0a45d3830853227610e8386c
lineage_relation: original
parent_observation_id: null
first_seen_at: 2026-08-30T12:53:28.391567Z
last_seen_at: 2026-08-30T12:56:26Z
---

## 转写说明

> 本文基于已校验的公开原文进行结构化转写与事实梳理，非原文转载。
> 转写保留可核验的技术事实，并将工程建议与来源观点明确分开。

- **原作者**: 默\_笙
- **原始来源**: [https://juejin.cn/post/7679341637068898313](https://juejin.cn/post/7679341637068898313)
- **原文发布时间**: Sun, 30 Aug 2026 11:14:59 GMT

## 核心结论

该笔记系统基于 Next.js 脚手架构建，采用 React Server Component 与客户端组件分层协作的架构。数据存储选用 Redis 作为 key:value 内存数据库，利用 hash 类型存取笔记内容。组件规划遵循规范驱动编程方法，先绘制组件树再落笔实现代码。SEO 优化通过根布局的 title、description、keywords 三项元数据实现。该项目为 Next.js 知识体系的综合实践，覆盖 App Router、异步组件、目录别名等核心概念。

## 能力机制

**组件分层机制**方面，系统采用四层 RSC 流水线结构。Sidebar 作为顶层 async 服务器组件直接 await 获取 Redis 数据，随后将笔记列表传递给 SidebarNoteList 继续遍历，再由 SidebarNoteItem 渲染单条笔记的标题与时间，最后通过 SidebarNoteItemContent 这个 'use client' 组件预留交互接口。RSC 组件可声明为 async，在服务器端等待数据到位后再输出完整 HTML，因此天然适合服务端渲染与 SEO 场景。

**数据访问机制**通过 ioredis 客户端驱动 Redis。笔记以 hash 类型存储在 'notes' 键下，hgetall 一次性取出所有字段。初始化阶段检测数据为空时，通过 hset 写入预设的初始数据，这种懒加载模式确保应用重启后仍可正常运行。hash 类型的 value 为笔记 JSON 序列化后的字符串。

**命名与路径规范**采用 BEM 命名约定，Block 与 Element 之间用单下划线连接。目录别名配置 @ 符号直接指向项目根目录，例如 @/lib/redis.js 替代多层相对路径 ../../../lib/redis.js。

## 快速开始

项目创建命令：

```
npx create-next-app
```

该命令等同于全局安装 create-next-app 后再运行，自带 SSR、SEO、RSC 等能力。

Redis 连接配置使用默认端口，ioredis 客户端无需额外配置密钥环境变量（生产环境需根据实际情况配置）。

关键文件目录结构：

```
app/           # 页面主目录
components/    # 组件目录
lib/           # 数据库操作与工具函数
```

导入示例：

```javascript
import { getAllNotes } from "@/lib/redis.js";
```

核心数据获取函数位于 lib/redis.js，通过 ioredis 的 hgetall 与 hset 操作笔记 hash 数据。

## 适用边界

该架构适用于需要服务端渲染与 SEO 支持的笔记类内容站点。Redis 作为内存数据库适合数据量可控且读写性能要求较高的场景，但不适合需要复杂查询或多表关联的场景。对于需要持久化存储的生产环境，建议将 Redis 作为 MySQL 前置缓存层使用，而非唯一数据存储。RSC 与 'use client' 的分层策略适用于交互程度由低到高的各类组件，服务器组件负责数据获取与静态展示，客户端组件处理用户交互与状态管理。

## 核验清单

- 组件树规划是否完整，Sidebar、SidebarNoteList、SidebarNoteItem、SidebarNoteItemContent 四层职责是否清晰
- RSC 组件是否正确声明为 async 并使用 await 获取数据
- 'use client' 是否仅在最内层交互组件使用
- Redis hash 类型的存取操作是否使用 hgetall 与 hset
- 根布局是否包含 title、description、keywords 三项 SEO 元数据
- BEM 命名规范是否在 CSS 类名中一致应用
- @ alias 路径别名是否正确配置并指向项目根目录
- 初始数据懒加载逻辑是否在 getAllNotes 函数中实现

## 来源与核验

- [原始文章](https://juejin.cn/post/7679341637068898313)
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