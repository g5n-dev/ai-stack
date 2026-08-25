---
title: "我给自己写了个「AI 代言人」"
date: 2026-08-25T12:57:25+08:00
draft: false
entry_kind: "auto"
tags: ["掘金", "工程实践", "来源转写"]
categories: ["AI 工程"]
source: "juejin"
content_mode: "evidence_backed_rewrite"
publication_tier: "B"
source_capture_mode: "full_article"
source_snapshot_sha256: "sha256:19254133469a8da474ecc5beca0f9be47805a27e53767289d0c75165e4e330ce"
source_payload_sha256: "sha256:54087b5a893eddd9600b1cd7ec6bece4a567919a29acf1864ed8a1044c73edd0"
source_published_at: 2026-08-25T03:18:32Z
timestamp_confidence: feed
extractor_version: "source-contract-v2"
discovery_method: "article_html"
source_completeness: "complete"
parent_snapshot_sha256: "sha256:82771a30d7165c5989b18a6534a7490b8af22df070e059ca044e1c63975324b7"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 15
description: "核心结论 这是一个用于面试前简历预研的个人工具。候选人维护一份简历，面试官通过密码访问 AI 进行基于简历原文的自动问答。系统以「不编造」为硬约束——命中不了简历内容时直接返回固定文案，而非让模型自由发挥。"
external_url: https://juejin.cn/post/7677502358059827252
observation_id: obs_a9e2b38dbf611209729928c2c383ec46074b45ed8c086d41f81d348f14524170
revision_id: rev_c7ce14078ae4196686cc4540ef6164591451f117e3b87e1ea6941cc22deed661
event_id: evt_1b445c5f1bbd0ff1ab15f9916bb57da9fa5b3fd2ccebdff3da6a9080b7f0ce5f
lineage_relation: original
parent_observation_id: null
first_seen_at: 2026-08-25T04:53:42.853218Z
last_seen_at: 2026-08-25T04:57:25Z
---

## 转写说明

> 本文基于已校验的公开原文进行结构化转写与事实梳理，非原文转载。
> 转写保留可核验的技术事实，并将工程建议与来源观点明确分开。

- **原作者**: 函数小陈
- **原始来源**: [https://juejin.cn/post/7677502358059827252](https://juejin.cn/post/7677502358059827252)
- **原文发布时间**: Tue, 25 Aug 2026 03:18:32 GMT

## 核心结论

这是一个用于面试前简历预研的个人工具。候选人维护一份简历，面试官通过密码访问 AI 进行基于简历原文的自动问答。系统以「不编造」为硬约束——命中不了简历内容时直接返回固定文案，而非让模型自由发挥。

技术栈为 Vue 3 + Vite + Pinia 构建前端，后端使用裸 node:http + TypeScript，不依赖 Express 或 vue-router。数据库为 MySQL，AI 接入 FastGPT 与 DeepSeek 双引擎，可通过环境变量切换。

## 能力机制

### 双引擎切换

系统通过 `USE_FASTGPT` 环境变量控制 AI 路径。两条路径在检索、生成、出处记录上各自独立：FastGPT 模式同步简历到其知识库进行向量检索；关闭后改用内存切片检索直连 DeepSeek。切换时只需修改环境变量并重启，前端接口不变。

### 防幻觉机制

简历未命中或涉及薪资、离职原因等禁区时，系统直接返回「简历未提及」固定文案 `ABSENT_TEXT`，配合提示语引导面试官在正式面试中向候选人本人确认。问答流程的第一个条件判断为空问题、简历无内容或命中禁区时，跳过所有模型调用。

### 身份写锁

「同一身份同时只许一人写」通过 MySQL 条件更新实现。`tryLock` 函数在 `WHERE` 子句中判断锁为空或已过期时允许写入，`affectedRows` 为 0 表示抢锁失败。锁默认 15 分钟后自动释放，面试官关闭浏览器不会导致永久阻塞。抢锁失败者降级为只读模式。

### 热门问题统计

白天 `GET /api/chat/templates` 直接读取 `hot_board` 表零延迟返回，凌晨 0 点（上海时区）运行定时任务：统计前一个自然日提问 → 交给 DeepSeek 近义合并 → 写入榜单。模型挂掉或无提问时沿用旧榜，不清空数据。

### 分享链接绑定

面试官通过 `/?s=` 分享链接跳过密码门。第一位访问者选择的关联公司锁死在该链接上，后续使用同一链接的人只能新建身份。链接作废则释放绑定，重新生成链接则公司绑定保留。

## 快速开始

环境要求：Node.js 运行时、MySQL 5.7 及以上。

后端依赖通过 npm 安装，启动前需配置数据库连接及以下环境变量：数据库连接参数、`ADMIN_PASSWORD`（管理端密码）、`CHAT_PASSWORD`（面试官密码）、`USE_FASTGPT`（切控 AI 引擎）、`DEEPSEEK_API_KEY`（DeepSeek 接口凭据）、`FASTGPT_API_KEY`（FastGPT 接口凭据，FastGPT 模式启用时需要）。前后端均支持 Docker 部署或手动构建。详细部署步骤需参考原项目文档。

## 适用边界

此方案适合个人维护简历、用于面试前预研的场景，在接口数量少（原文列举为 25 个）、页面数量少（5 个）、迭代快速阶段能够降低框架抽象带来的心智负担。

已知的明确限制包括：定时任务依赖 Node 进程存活，进程退出则凌晨统计不运行；PDF 存储在本地磁盘而非数据库；免费版 FastGPT 额度有限，正式使用需切换到 DeepSeek；公司名称搜索仅支持模糊匹配，不支持拼音或错字纠正。

## 核验清单

实现效果可从以下维度核验：问答是否严格基于简历原文，拒绝编造；写锁是否阻止同一身份多人并发写入；凌晨统计任务在模型异常时是否保留旧数据；分享链接是否正确绑定公司并限制后续访问者修改；PDF 解析结果是否经过人工确认后才写入表单。

## 来源与核验

- [原始文章](https://juejin.cn/post/7677502358059827252)
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