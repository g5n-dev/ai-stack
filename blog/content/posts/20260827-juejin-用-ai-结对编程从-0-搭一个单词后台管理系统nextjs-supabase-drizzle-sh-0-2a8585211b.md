---
title: "用 AI 结对编程从 0 搭一个\"单词后台管理系统\"：Next.js + Supabase + Drizzle + shadcn/ui 全记录"
date: 2026-08-27T01:04:33+08:00
draft: false
entry_kind: "auto"
tags: ["掘金", "工程实践", "来源转写"]
categories: ["AI 工程"]
source: "juejin"
content_mode: "evidence_backed_rewrite"
publication_tier: "B"
source_capture_mode: "full_article"
source_snapshot_sha256: "sha256:77bcf226606e50a278f29944446aff2d21f1958e9eeb68593f9ec86e77899e4f"
source_payload_sha256: "sha256:9bcbafc371fddf234d231dbd52288244a860851e72c5ac1e46ed7b4f23bae4b3"
source_published_at: 2026-08-26T14:12:50Z
timestamp_confidence: feed
extractor_version: "source-contract-v2"
discovery_method: "article_html"
source_completeness: "complete"
parent_snapshot_sha256: "sha256:e909c5095c7b20858e16ffb4a9a812734f5f7d3c02a37087be0f9e8a8ac849e2"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 71
description: "核心结论 该项目是一个单词后台管理系统的技术实践，采用 Next.js App Router 作为前端框架，Supabase 提供云端 PostgreSQL 数据库服务，Drizzle ORM 处理数据库操作，shadcn/ui 组件库构建界面。 关键技术选型理由如下。"
external_url: https://juejin.cn/post/7678239521201307657
observation_id: obs_2a8585211b5f29b0f4d8a35bbba6ce44502f4ec120acc6203acd9a347a972f11
revision_id: rev_f8c468698f4d22a3edbb30ae83c144c0a3b01c692a4e3bb19628407f0f1a7b20
event_id: evt_15eedc8bf781d478f61627495b89365ed6f56018d7ccf9381ee114b235b7ebeb
lineage_relation: original
parent_observation_id: null
first_seen_at: 2026-08-26T17:00:03.542540Z
last_seen_at: 2026-08-26T17:04:33Z
---

## 转写说明

> 本文基于已校验的公开原文进行结构化转写与事实梳理，非原文转载。
> 转写保留可核验的技术事实，并将工程建议与来源观点明确分开。

- **原作者**: dzhd
- **原始来源**: [https://juejin.cn/post/7678239521201307657](https://juejin.cn/post/7678239521201307657)
- **原文发布时间**: Wed, 26 Aug 2026 14:12:50 GMT

## 核心结论

该项目是一个单词后台管理系统的技术实践，采用 Next.js App Router 作为前端框架，Supabase 提供云端 PostgreSQL 数据库服务，Drizzle ORM 处理数据库操作，shadcn/ui 组件库构建界面。

关键技术选型理由如下。shadcn/ui 并非传统组件库，而是将组件源码直接复制到项目 `components/ui` 目录，允许开发者自由修改和定制，配合 Tailwind CSS 实现原子化样式管理。Supabase 作为 BaaS 平台，托管 PostgreSQL 数据库并提供鉴权、实时订阅等后端能力，降低运维成本。Drizzle ORM 支持 TypeScript 类型从表定义直接推导，通过迁移工具自动生成建表 SQL，避免手动编写数据库脚本。

认证环节采用 scrypt 算法对密码进行哈希加盐存储，使用 `timingSafeEqual` 进行时间安全比较以防止计时攻击。会话通过 Cookie 机制管理，配置 `httpOnly`、`secure`、`sameSite` 等属性增强安全性。

## 能力机制

**组件库机制**

shadcn/ui 的核心设计是将组件源码作为项目代码的一部分进行管理。开发者通过 CLI 安装时，组件文件会写入 `components/ui` 目录，后续可像修改普通代码一样直接编辑。这种模式区别于传统 npm 包式的组件库，提供了完全的定制自由度。配合 Tailwind CSS 的原子类体系，界面构建通过组合 `flex`、`p-4`、`text-sm` 等语义化类名实现。

**数据库连接机制**

开发环境中存在 HMR 热模块替换机制，模块重载不会重启 Node 进程。若每次重载都新建数据库连接池，会快速耗尽 Supabase 免费版的连接限额。解决方案是将 postgres.js 客户端挂载到 `globalThis` 对象，模块重载时优先复用已有连接，避免连接数快速增长。

**密码处理机制**

数据库不存储明文密码，而是存储密码哈希值。哈希函数具有单向性，从输出无法反推输入。引入盐值（随机数据）防止彩虹表攻击，即使相同密码因盐值不同也会产生不同哈希结果。存储格式为 `盐:哈希`，登录时使用存储的盐重新计算并比对。验证环节使用 `timingSafeEqual` 进行固定时间比较，防止通过响应时间差异推断密码特征。

**会话管理机制**

HTTP 协议本身无状态，服务端通过 Cookie 机制识别用户身份。登录成功后服务端生成随机 token，存入数据库会话表，同时通过 `Set-Cookie` 响应头下发。浏览器后续请求自动携带该 Cookie。验证时通过 ORM 的 `innerJoin` 将会话表与用户表联查，确认 token 有效且未过期。

**数据校验机制**

使用 Zod 定义校验规则 Schema，同一套规则可同时用于前端表单实时校验和后端 API 最终校验。前端校验不可信，用户可直接调用 API 绕过浏览器端逻辑，后端必须重复校验以实现纵深防御。

## 快速开始

**环境配置**

项目依赖以下环境变量用于数据库连接：

```
DATABASE_URL
```

此变量需配置为 PostgreSQL 连接字符串格式。

**数据库迁移命令**

项目 package.json 中定义了以下 Drizzle 相关脚本用于管理数据库结构：

```json
"db:generate": "drizzle-kit generate",
"db:migrate": "drizzle-kit migrate",
"db:push": "drizzle-kit push",
"db:studio": "drizzle-kit studio"
```

`generate` 命令对比 schema 定义与当前数据库结构，生成迁移文件。`push` 命令直接将 schema 变更推送到云端数据库，适用于开发阶段快速同步。`studio` 启动本地可视化数据库浏览工具。

**认证相关环境变量**

认证模块中密码哈希和会话管理相关操作依赖 Node.js 内置 `crypto` 模块，无需额外配置密钥环境变量。

## 适用边界

**组件库适用边界**

shadcn/ui 适用于需要高度定制化界面的项目。如果团队需要快速交付且定制需求较低，Ant Design、Element UI 等开箱即用的组件库可能更合适。该组件库要求开发者具备 Tailwind CSS 使用经验。

**数据库适用边界**

Supabase 提供的是托管式 PostgreSQL，适合不想自行运维数据库的团队。若项目需要完全自托管或对数据存储位置有严格合规要求，需考虑传统自建方案。当前项目使用 localStorage 模拟 books 数据层作为过渡，待数据库表结构完善后再切换为真实数据库查询。

**认证适用边界**

当前认证系统基于 Cookie 会话机制，适用于同源前端应用。若后续开发小程序或移动端，需评估 Cookie 在这些场景的兼容性。超级管理员注册限制在首个注册用户，这一业务规则通过服务端 API 层强制执行，前端仅做引导性校验。

**ORM 适用边界**

Drizzle 适合 TypeScript 项目，类型安全要求高的场景。其迁移机制替代了手动建表流程，但需要开发者理解关系型数据库的基本概念（如主键、外键、表关联）。对于习惯手写 SQL 或使用非类型安全方案的团队，初始学习成本需要考虑。

## 核验清单

开发环境验证时需确认：Node.js 和 npm/pnpm 环境可用；Supabase 项目已创建且数据库服务已激活；`.env` 文件中 `DATABASE_URL` 已正确配置且可连接。

数据库层面需验证：`db:push` 命令执行成功后在 Supabase 控制台确认表结构与 schema 定义一致；外键关联正确建立（删除管理员用户时关联会话记录自动清除）；迁移文件历史完整。

认证功能需验证：首次访问注册页面可正常创建超级管理员账户；非管理员状态访问管理页面自动重定向至登录页；Cookie 在浏览器开发者工具中检查 `httpOnly` 属性已设置；使用错误密码登录返回明确错误信息，密码哈希值在数据库中为不可读格式。

组件库层面需验证：`components/ui` 目录包含所需组件源码文件；Tailwind 配置正确识别 shadcn/ui 的样式类名；按需引入的组件未导致包体积显著增加。

前端数据层需验证：localStorage 的书籍数据读取逻辑位于 `useEffect` 内部，避免服务端渲染阶段访问 `window` 对象报错；搜索过滤和统计计算通过 `useMemo` 派生，避免重复计算。

版本控制层面需验证：Git 提交信息遵循 Conventional Commits 规范，格式为 `type: description`，其中 type 包括 feat、fix、docs、refactor、perf、test、chore、revert 等类型。

## 来源与核验

- [原始文章](https://juejin.cn/post/7678239521201307657)
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