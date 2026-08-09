---
title: "用 WorkBuddy / Codex + Obsidian 搭建自生长的个人知识库实战"
date: 2026-08-09T17:04:11+08:00
draft: false
entry_kind: "auto"
tags: ["掘金", "工程实践", "来源转写"]
categories: ["AI 工程"]
source: "juejin"
content_mode: "evidence_backed_rewrite"
publication_tier: "B"
source_capture_mode: "full_article"
source_snapshot_sha256: "sha256:62b4b4437452a18f89117104abd401fe480ae235e6e01684354ee1b2e5aee522"
source_payload_sha256: "sha256:54a144965b70005075c94de32015b56aa85aa489b3d995b29e9f5a728541d65b"
source_published_at: 2026-08-09T08:36:26Z
timestamp_confidence: feed
extractor_version: "source-contract-v2"
discovery_method: "article_html"
source_completeness: "complete"
parent_snapshot_sha256: "sha256:eea4a98a455cfc88c0548c219b9a39d805a2455474b82e9295cce47408787bb4"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 44
description: "核心结论 Karpathy 提出的 LLM wiki 旨在为 AI 安排一份长期维护知识库的工作。与传统 RAG 或文件上传不同，LLM wiki 不是每次提问都重新拼接碎片答案，而是让 Agent 在处理每份资料时：已有内容被补充、新概念单独建页、观点分歧保留来源和时间范围。知识库因此具备持续积累能力，而非答完即散。"
external_url: https://juejin.cn/post/7671867883983896618
observation_id: obs_adb088fdc693f90fbe07e53f59c8df45deafb2fc03849a57d68a3d224fdacc4e
revision_id: rev_72d74a971930e44d7614aada86740f178cd56b87db8772211b22fb1e04ba9222
event_id: evt_c56d5edc4e4fcec2b19156e4847d1eaf68777527fd29379f3f6cdda4859bb5cd
lineage_relation: original
parent_observation_id: null
first_seen_at: 2026-08-09T09:02:23.220528Z
last_seen_at: 2026-08-09T09:04:11Z
---

## 转写说明

> 本文基于已校验的公开原文进行结构化转写与事实梳理，非原文转载。
> 转写保留可核验的技术事实，并将工程建议与来源观点明确分开。

- **原作者**: 苍何
- **原始来源**: [https://juejin.cn/post/7671867883983896618](https://juejin.cn/post/7671867883983896618)
- **原文发布时间**: Sun, 09 Aug 2026 08:36:26 GMT

## 核心结论

Karpathy 提出的 LLM wiki 旨在为 AI 安排一份长期维护知识库的工作。与传统 RAG 或文件上传不同，LLM wiki 不是每次提问都重新拼接碎片答案，而是让 Agent 在处理每份资料时：已有内容被补充、新概念单独建页、观点分歧保留来源和时间范围。知识库因此具备持续积累能力，而非答完即散。

整套系统采用三层架构分离职责：Raw 层保存原始资料只读不修改；Wiki 层沉淀 AI 整理出的概念、实体和主题；Schema 层通过 `AGENTS.md` 定义归档、更新、引用和冲突处理规则。Raw 保存证据，Wiki 记录理解，Schema 定规则。

## 能力机制

Obsidian 在系统中同时承担存储底座、人机操作界面和知识观察窗口三种角色。Vault 即普通文件夹，笔记以 Markdown 纯文本保存，不依赖平台数据库，适合 Agent 直接读取目录、创建页面、修改链接和维护索引。数据是否同步、同步到哪里完全由用户决定。

WorkBuddy / Codex 作为 Agent 执行层，负责读取 Obsidian Vault 中的目录和 Markdown 文件，按照 `AGENTS.md` 中的规则完成批量处理。新资料进入 Raw 层后，Agent 会先理解内容、识别概念和实体，与现有 Wiki 对照后执行增量维护：补充已有页面、创建新页面、建立相关双链，遇到不同说法时保留来源、时间和适用范围。每次处理都会同步更新索引与变更记录，整个过程不需要重建知识库。

## 快速开始

首先从 obsidian.md 下载 Obsidian 并新建 Vault。建议开启代理访问插件市场。完成后进入插件市场安装 WeSight 插件以简化后续搭建流程。

按照三层架构创建目录结构：

```
my-wiki/
├── AGENTS.md          ← Schema 规范层
├── index.md           ← 全局索引入口
├── log.md             ← 变更日志
├── raw/               ← 原始资料层（只读）
│   ├── articles/      ← 剪藏文章
│   ├── papers/        ← 论文报告
│   ├── books/         ← 书籍笔记
│   ├── chats/         ← AI对话记录
│   ├── notes/         ← 灵感碎片
│   └── meetings/      ← 会议纪要
└── wiki/              ← Wiki 层（AI维护）
    ├── sources/       ← 来源摘要页
    ├── concepts/      ← 概念理论页
    ├── entities/      ← 人物产品工具页
    └── topics/        ← 主题综述页
```

在 Vault 根目录创建 `AGENTS.md`，定义 Agent 的工作规则：处理新资料前先检索 `wiki/` 中已有页面；`raw/` 层禁止改写删除；每份原始资料建立对应来源摘要页；概念、实体和主题使用独立页面并通过双链建立关系；新旧资料出现分歧时保留不同说法；变更日志采用只追加方式。

使用 Obsidian Web Clipper 浏览器插件将文章剪藏至 `raw/articles/` 目录。然后在 WorkBuddy 或 Codex 中调用 Agent 读取新资料，严格按照 `AGENTS.md` 规则增量维护 Wiki 层。

## 适用边界

文章建议选择上下文较长的模型以支撑长链路、多轮任务。在模型选型上，DeepSeek V4 Flash 性价比突出但不支持多模态；Kimi K3 支持原生多模态；Doubao-Seed-Evolving 面向 Agent 与长程任务优化。作者明确不建议使用 Codex 中的 GPT 5.6 Sol，原因是用量消耗过大。

实际选型时建议用真实资料跑一遍完整任务，重点观察上下文是否丢失、工具调用是否稳定、输出格式是否漂移，以及单次任务的时间和成本。

这套系统适合希望将知识管理从一次性手工整理转变为持续维护机制的用户。资料搜集可配合手机端 ima 或其他剪藏工具、电脑端 Obsidian Web Clipper 插件、以及 Agent 批量收藏飞书文档等方式。哪些资料值得保留、规则如何设定、关键结论能否成立仍需要人工判断；AI 更适合承担重复、耗时且结构化的维护工作。

## 核验清单

搭建完成后应进行以下验证：

确认 `raw/` 层为只读状态，Agent 未修改原始文件；检查新增页面是否正确建立双链关系；验证 `index.md` 和 `log.md` 是否同步更新；确认 Wiki 页面中的事实性内容已标注来源，无法确认的内容标记为“待核实”；检验不同观点是否保留各自来源、时间范围和适用范围而非被覆盖；评估 Agent 检索结果是否可追溯到原始资料路径。

## 来源与核验

- [原始文章](https://juejin.cn/post/7671867883983896618)
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