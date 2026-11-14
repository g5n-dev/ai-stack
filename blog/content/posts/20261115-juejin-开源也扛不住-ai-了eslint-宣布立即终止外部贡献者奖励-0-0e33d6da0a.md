---
title: "开源也扛不住 AI 了？ESLint 宣布立即终止外部贡献者奖励"
date: 2026-11-15T01:07:31+08:00
draft: false
entry_kind: "auto"
tags: ["掘金", "工程实践", "来源转写"]
categories: ["AI 工程"]
source: "juejin"
content_mode: "evidence_backed_rewrite"
publication_tier: "B"
source_capture_mode: "full_article"
source_snapshot_sha256: "sha256:40358b0d36114d07a4f68ec852a8b615d741aa22824426980e4675ed035edbd2"
source_payload_sha256: "sha256:41e7e6bc24bee0a09cd1af68a247ed84af75aab6e8234b48e79f5d27d6af81ec"
source_published_at: 2026-11-14T16:32:52Z
timestamp_confidence: feed
extractor_version: "source-contract-v2"
discovery_method: "article_html"
source_completeness: "complete"
parent_snapshot_sha256: "sha256:d9b5e7656ac61a9507b8172cd1ff17d564a374f08fbcedbf6add83c1db02f247"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 32
description: "核心结论 ESLint 于 11 月 13 日宣布立即终止面向外部贡献者的奖励资金池（contributor pool），并明确表示终止原因不是资金不足。该机制运行五年，累计向外部贡献者发放 51,180 美元，覆盖文档修改、代码 PR 和 Discord 答疑等贡献。"
external_url: https://juejin.cn/post/7707875510298624050
observation_id: obs_0e33d6da0ae181ce8021c6c9500e0d2187c5f707965fb196bc13667e67f5b906
revision_id: rev_dfcc11a95617e0b7bb843c3d940584447b2f7a3a37631f853d1cb1af13e80535
event_id: evt_d0712a81a87068a9ed0d937fa0822bf8414d2b24c6b02f43532e5425d7ed0f5e
lineage_relation: original
parent_observation_id: null
first_seen_at: 2026-11-14T17:05:39.518861Z
last_seen_at: 2026-11-14T17:07:31Z
---

## 转写说明

> 本文基于已校验的公开原文进行结构化转写与事实梳理，非原文转载。
> 转写保留可核验的技术事实，并将工程建议与来源观点明确分开。

- **原作者**: parade岁月
- **原始来源**: [https://juejin.cn/post/7707875510298624050](https://juejin.cn/post/7707875510298624050)
- **原文发布时间**: Sat, 14 Nov 2026 16:32:52 GMT

## 核心结论

ESLint 于 11 月 13 日宣布立即终止面向外部贡献者的奖励资金池（contributor pool），并明确表示终止原因不是资金不足。该机制运行五年，累计向外部贡献者发放 51,180 美元，覆盖文档修改、代码 PR 和 Discord 答疑等贡献。

终止背景是团队难以可靠判断 PR 是否由 AI 生成。披露要求、额外核查以及外部人员举报，使维护者需要持续投入时间审查贡献来源，并处理围绕 AI 使用的争议。ESLint 并未停止维护，v10.15.0 在宣布当天发布。

来源文章进一步提出：依赖贡献数量、投入程度或参与次数的奖励机制，都可能受到低边际成本 AI 产出的稀释；维护者的时间与审查精力可能因此成为更稀缺的资源。这一部分属于作者分析，不是 ESLint 公告之外的官方结论。

## 能力机制

原有资金池最初每月投入 1,000 美元，后来调整为每月收入的 10%。外部贡献者提交 PR、修改文档或参与社区答疑，都可能获得奖励。该设计旨在弥补外部贡献者与受薪团队成员之间报酬不对等的问题。

年度发放金额分别为：2022 年 7,900 美元、2023 年 4,500 美元、2024 年 14,100 美元、2025 年 24,680 美元。官方表示，该机制吸引了重复参与的外部贡献者，其中部分人后来成为正式团队成员。

面对 AI 生成内容增加，团队先要求在 PR 描述中披露是否使用 AI，但并非所有贡献者都会如实披露。随着模型能力提升，人工核查难度增加，随后又出现外部“AI 监督员”：在 PR 下判断内容是否由 AI 生成、依据月度报告追踪相关账号，甚至私信维护者提出质疑。最终，团队选择不再执行依赖奖励资格判断的资金池。

## 快速开始

来源没有提供可确认的安装、配置或贡献命令，因此不列出额外命令。准备参与 ESLint 贡献时，可按以下方式降低协作摩擦：

1. 阅读项目贡献规范，确认 PR 描述、测试和文档修改要求。
2. 如在贡献过程中使用 AI，应按项目规则说明使用情况；来源显示，ESLint 曾要求在 PR 描述中披露 AI 使用。
3. 提交后关注维护者反馈，不要仅以代码生成结果代替对问题成因和项目原理的理解。
4. 在提交前自行检查内容与现有实现、测试及文档是否一致，避免把可由维护者直接修正的 PR 转嫁给审查团队。

其中第 3、4 项是基于来源所揭示的维护成本提出的工程建议，不是 ESLint 公告中给出的正式流程。

## 适用边界

ESLint 终止的是外部贡献者奖励资金池，不代表项目停止维护，也不意味着社区拒绝 AI 辅助贡献。来源只说明 AI 生成内容增加了来源判断和社区核查的负担，未提供 AI 贡献的全面准入结论。

来源提出，AI 驱动的贡献能否带来与人工贡献相同的社区归属感、长期投入和协作价值，仍需观察。该判断不能直接外推为所有开源项目都会终止类似奖励计划，因为不同项目的审核规则、资金结构和社区治理方式可能不同。

同样，文章关于悬赏、积分、贡献榜单和活动奖励会被稀释的说法，是作者对同类机制风险的分析，不是经过验证的普遍结果。来源也没有提供终止资金池节省了多少费用、后续贡献者如何获得报酬等实施细节。

## 核验清单

核对本说明时，可重点确认以下事实：

- 终止对象是外部贡献者资金池，而非 ESLint 整个项目。
- 资金池累计发放 51,180 美元，运行时间为五年。
- 官方给出的终止原因不是资金不足，而是 AI 贡献难以甄别带来的审查和争议成本。
- 资金池早期按月固定发放 1,000 美元，后改为月收入的 10%。
- 2025 年发放 24,680 美元，高于 2023 年的 4,500 美元。
- ESLint 曾采用 PR 描述中的 AI 使用披露方式，但来源指出该方式无法保证所有贡献者如实披露。
- v10.15.0 在宣布当天发布，可据此确认项目当时仍处于正常维护状态。
- 关于其他开源奖励机制将被稀释、维护者时间最稀缺等内容，应标记为来源作者的分析或建议，不能写成 ESLint 官方结论。

## 来源与核验

- [原始文章](https://juejin.cn/post/7707875510298624050)
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