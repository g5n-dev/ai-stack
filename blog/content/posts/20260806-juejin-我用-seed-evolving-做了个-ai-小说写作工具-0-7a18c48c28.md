---
title: "我用 Seed Evolving 做了个 AI 小说写作工具"
date: 2026-08-06T17:52:54+08:00
draft: false
entry_kind: "auto"
tags: ["掘金", "工程实践", "来源转写"]
categories: ["AI 工程"]
source: "juejin"
content_mode: "evidence_backed_rewrite"
publication_tier: "B"
source_capture_mode: "full_article"
source_snapshot_sha256: "sha256:0c28a99a212e784323a82d2a4c7806d66d464b220576382efd5ace5ea536e980"
source_payload_sha256: "sha256:0c0c9a3a4fef52d7272c7d67f08d482fd7c62e67525629b7dcae9f59562e8542"
source_published_at: 2026-08-06T09:41:44Z
timestamp_confidence: feed
extractor_version: "source-contract-v2"
discovery_method: "article_html"
source_completeness: "complete"
parent_snapshot_sha256: "sha256:d49fb91100f94020da14f8d53c8e3f09323056d423a404dd4167a5f54fc39ac9"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 30
description: "核心结论 用大语言模型做长篇小说创作的核心瓶颈不在于模型能否生成文字，而在于生成后模型是否仍记得之前写过的内容，以及故事能否真正收尾。这一问题的根因是上下文和状态管理，而非模型本身的生成能力。"
external_url: https://juejin.cn/post/7670752654530461747
observation_id: obs_7a18c48c282526f2dfe1fbc522260b86bd5627756fe241602b419293731b14cb
revision_id: rev_3b157006edbb370fb707b196ef451db991c577ed3200063b2f8a4faa491d8098
event_id: evt_4bb5287daa42beded29d09eca5634701024b3d0c0ed48258a91d35ebcba2ae19
lineage_relation: original
parent_observation_id: null
first_seen_at: 2026-08-06T09:51:10.448122Z
last_seen_at: 2026-08-06T09:52:54Z
---

## 转写说明

> 本文基于已校验的公开原文进行结构化转写与事实梳理，非原文转载。
> 转写保留可核验的技术事实，并将工程建议与来源观点明确分开。

- **原作者**: 码事漫谈
- **原始来源**: [https://juejin.cn/post/7670752654530461747](https://juejin.cn/post/7670752654530461747)
- **原文发布时间**: Thu, 06 Aug 2026 09:41:44 GMT

## 核心结论

用大语言模型做长篇小说创作的核心瓶颈不在于模型能否生成文字，而在于生成后模型是否仍记得之前写过的内容，以及故事能否真正收尾。这一问题的根因是上下文和状态管理，而非模型本身的生成能力。Seed Evolving 的 1M 上下文窗口为长篇叙事的状态维护提供了工程上的冗余空间，使得上下文组装策略不必在“裁剪哪些内容”上反复权衡。

## 能力机制

脉络项目的核心设计围绕四个机制展开。

Chat-first 交互模式：不采用传统的表单填写流程，而是在单个输入框中通过多轮对话逐步建立世界观、角色和剧情设定。系统在对话中自动将结构化信息写入项目记录，每轮返回固定格式的 JSON 包含 reply、actions、quick_replies 和 primary_action 字段。

关系图谱与一致性检查：基于 Cytoscape.js 实现力导向关系图谱，支持角色、地点、组织和剧情线四种节点类型。节点位置持久化保存，新增节点单独定位不会触发全图重排。一致性检查采用规则实现，检测不可变特征矛盾、死亡角色活动、终止关系异常和性别漂移等问题，冲突节点和边在图谱中以红色高亮标识。

上下文组装与流式生成：每次生成正文前，Context Composer 将世界观、大纲、角色卡（含 immutable_traits 不可变特征）、活跃关系图谱、全局剧情摘要、角色状态快照、最近 3 章正文、RAG 检索片段和当前创作意图注入 prompt。生成过程采用 SSE 流式输出，支持随时中止。

完结模式：当用户表达完结意图时，系统开启完结模式，提示词要求收束全部未解线索并以“全书完”收尾。服务端检测到结束关键词后强制执行 end_story，并将小说状态置为 done，前端禁止续章生成入口。

## 快速开始

项目基于 Node.js + SQLite 实现本地零外部依赖部署。项目地址在 GitHub 和 GitCode 均有托管，采用 MIT 协议开源。部署流程为克隆仓库后执行 npm install 安装依赖，再执行 npm run dev 启动开发服务器。用户需要自备 API Key，数据存储在本地 SQLite 数据库中，密钥以 AES-256-GCM 加密存储。RAG 功能支持配置 Embedding API，未配置时自动降级为中文关键词检索以保证基本功能可用。

## 适用边界

该项目适用于需要维持长篇叙事的连贯性、但不愿依赖传统表单填写流程的创作者。由于采用 BYOK（自备密钥）设计，数据处理在本地完成。规则版一致性检查能够覆盖约 80% 的常见叙事矛盾场景，剩余部分计划在后续版本中由 LLM Judge 补充。当前 V1 版本的一致性检查不适合对叙事细节有严格要求的场景；关系图谱的节点位置持久化设计适合需要长期维护角色关系的连载型创作；完结模式的存在表明该项目针对有明确结局预期的完整故事设计。

## 核验清单

验证该工具时可通过以下方式核验核心功能：创建一句话设定后，观察系统是否通过多轮对话而非表单完成世界观和角色建立；生成章节后检查关系图谱是否自动更新、不可变特征矛盾是否触发红色高亮；连续生成多章后检查后续章节的人物特征是否与早期设定保持一致；在对话中表达完结意图后，观察系统是否生成明确结局并锁定续章入口；检查断线时 SSE 是否通过 AbortController 中止 LLM 请求以避免 token 浪费。项目代码开源可查，可进一步核验状态管理、加密存储和流式生成的实现细节。

## 来源与核验

- [原始文章](https://juejin.cn/post/7670752654530461747)
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