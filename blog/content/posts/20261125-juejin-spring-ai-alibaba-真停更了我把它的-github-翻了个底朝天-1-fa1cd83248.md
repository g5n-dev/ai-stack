---
title: "Spring AI Alibaba 真停更了？我把它的 GitHub 翻了个底朝天"
date: 2026-11-25T20:51:49+08:00
draft: false
entry_kind: "auto"
tags: ["掘金", "工程实践", "来源转写"]
categories: ["AI 工程"]
source: "juejin"
content_mode: "evidence_backed_rewrite"
publication_tier: "B"
source_capture_mode: "full_article"
source_snapshot_sha256: "sha256:95efa672b00abff9f14c47b6fc1cebe1641d7042539078fb497489b4d2fb0701"
source_payload_sha256: "sha256:fe16ee960475100df26f16298a251b9a83dd745c1bfb2e1c61b93c591cd8b8ac"
source_published_at: 2026-11-25T12:14:21Z
timestamp_confidence: feed
extractor_version: "source-contract-v2"
discovery_method: "article_html"
source_completeness: "complete"
parent_snapshot_sha256: "sha256:96f3fbeaa7a58c226654f67016ec0e4f22bc5f83c7b40f6e17dd10d9021fbf84"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 41
description: "核心结论 根据来源对 GitHub Releases、提交记录、分支状态和 issue 面板的核查，Spring AI Alibaba（SAA）并非自 2026 年 3 月后完全没有发布：仓库在 2026 年 6 月 25 日发布了预发布版本 。"
external_url: https://juejin.cn/post/7711957412785340456
observation_id: obs_fa1cd8324815dd03889aeb439ccd9c5a8d4a9ed2cd7cb8fcfa8dacd106ca5154
revision_id: rev_d64f5a225e22ae2d4ac3350ff0969582f04a89ecb5027381e4e8d8725f130bea
event_id: evt_733dae42008f04b9ac6961027a687a553293a204d5cd62e1b5e4085ccbe6f298
lineage_relation: original
parent_observation_id: null
first_seen_at: 2026-11-25T12:50:24.344366Z
last_seen_at: 2026-11-25T12:51:49Z
---

## 转写说明

> 本文基于已校验的公开原文进行结构化转写与事实梳理，非原文转载。
> 转写保留可核验的技术事实，并将工程建议与来源观点明确分开。

- **原作者**: Flynt
- **原始来源**: [https://juejin.cn/post/7711957412785340456](https://juejin.cn/post/7711957412785340456)
- **原文发布时间**: Wed, 25 Nov 2026 12:14:21 GMT

## 核心结论

根据来源对 GitHub Releases、提交记录、分支状态和 issue 面板的核查，Spring AI Alibaba（SAA）并非自 2026 年 3 月后完全没有发布：仓库在 2026 年 6 月 25 日发布了预发布版本 `v2.0.0-M1.1`。但此后确实没有新的正式版，最新正式版仍是 2026 年 3 月 10 日发布的 `v1.1.2.2`。

提交活动也明显减少。`main` 分支最后一次提交为 2026 年 10 月 7 日，内容是合并 README 全角冒号修复；此前一项功能或测试相关提交发生在 8 月 25 日。承载 2.0 适配的 `2.x` 分支最后一次提交停留在 7 月 26 日，此后约四个月没有更新。

因此，更准确的描述不是“完全停更”，而是：正式版发布停滞、2.x 适配长期未落地、仓库仅保留少量社区维护活动，同时没有归档、停更公告或明确的维护进度说明。来源认为项目可能处于“不官宣、不归档、不投入”的状态，但也指出这属于作者判断，无法完全证实。

## 能力机制

`v2.0.0-M1.1` 将基础版本从 Spring AI 1.1.2 提升到 2.0.0-M1，并将 Spring Boot 目标版本提升到 4.0.0。该预发布版本还移除了 MySQL、PostgreSQL、Oracle 显式驱动版本，改由 Spring Boot BOM 管理。

SAA 在 Spring AI 之上提供 graph 编排和 multi-agent 模式，包括 routing、supervisor、handoffs 等。其最后一个正式版还增加了 `spring-ai-alibaba-starter-agentscope`，用于将 AgentScope Java 的 `ReActAgent` 接入 SAA 图编排。

项目曾设置 `2.0.0.0-RC1` milestone。issue #4717 中，collaborator 表示社区正在适配，并称计划在下一周发布 RC1；但来源核查时该版本尚未出现在 Releases，milestone 仍为 open 状态。该时间差是来源判断适配进展受阻的主要依据。

## 快速开始

来源给出的核查路径是：

1. 在 GitHub Releases 页面查看正式版与预发布版本，记录版本号、发布时间及是否标记为 prerelease。
2. 使用 GitHub API 查询最近提交，并查看 `main` 与 `2.x` 分支的提交时间、提交说明和关联 PR。
3. 检查 issue #4717、`2.0.0.0-RC1` milestone，以及与 Spring Boot 4、Spring AI 2.0 适配相关的 issue。
4. 对照同一生态中的 `agentscope-ai/agentscope-java`，观察其分支是否仍有提交。

来源中的 API 查询命令使用 `curl` 和 `jq`，分别提取 Releases 的 `tag_name`、`published_at`，以及 commits 的作者时间和首行说明。由于正文不包含外部地址，发布时应由来源链接统一关联原始仓库与核验入口。

## 适用边界

来源支持将仍在使用 `1.1.2.2` 的项目继续视为存量可用状态；其依据是该框架未被描述为损坏，也没有来源显示出现安全故障。但“存量可用”不等于官方会继续维护，也不代表后续生态适配、缺陷修复和问题响应能够保持原有节奏。

等待 Spring Boot 4 或 Spring AI 2.0 适配的用户，应把 RC1 尚未发布这一事实纳入排期评估。来源建议，若 graph 编排或 multi-agent 能力并非刚需，可直接评估 `spring-projects/spring-ai` 2.0；若这些能力是刚需，则可继续关注 AgentScope Java。

这些属于工程建议，而不是仓库维护者的正式路线图。来源没有证明团队已经终止维护，也没有确认人力已经转移至 AgentScope Java，因此不能把作者推测写成确定事实。

## 核验清单

- Releases 中最新正式版是否仍为 `v1.1.2.2`。
- 是否出现新的 prerelease、RC1 或正式版。
- `main` 分支是否出现功能、测试和文档之外的实质提交。
- `2.x` 分支是否恢复更新，是否同步到新的 Spring AI、Spring Boot 版本。
- `2.0.0.0-RC1` milestone 是否关闭或重新设定日期。
- issue #4717 是否出现维护者给出的明确进度、版本说明或停更公告。
- 相关 issue 是否从 stale、零回复状态恢复。
- AgentScope Java 是否继续更新，以及其与 SAA 的能力边界如何变化。

来源称核查仅依赖 GitHub API 和 Releases 页面；上述项目均应重新查询，不能仅凭单次观察推断长期维护承诺。

## 来源与核验

- [原始文章](https://juejin.cn/post/7711957412785340456)
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