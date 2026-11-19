---
title: "肝了一周，我把 Super Agent 的架构融入到了我的 AI Native 工作台中"
date: 2026-11-19T21:02:28+08:00
draft: false
entry_kind: "auto"
tags: ["掘金", "工程实践", "来源转写"]
categories: ["AI 工程"]
source: "juejin"
content_mode: "evidence_backed_rewrite"
publication_tier: "B"
source_capture_mode: "full_article"
source_snapshot_sha256: "sha256:68a45fdcd94b0f0f20382d2d1d3e10d83ee36ac3fd8dca5103607cb91d3c7046"
source_payload_sha256: "sha256:a8a74892fc4eddf9b5cf74e048e001c888cdf156f1dfc37db6157d8d21a534e0"
source_published_at: 2026-11-19T12:56:21Z
timestamp_confidence: feed
extractor_version: "source-contract-v2"
discovery_method: "article_html"
source_completeness: "complete"
parent_snapshot_sha256: "sha256:4492c4c1e4e23eb474e426143e4f67ae55bfc2ab849576010da65bd431eae024"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 44
description: "核心结论 来源实践的核心不是简单增加 Agent Session 数量，而是把调度单位从“对话窗口”提升为“任务”，再由唯一的 Router 统一协调多个 Worker。 任务状态不直接保存，而是根据窗口上报结果和交互事件实时推导；Router 只负责分诊、派活与协调，不编写代码，也不能代替用户完成任务验收。"
external_url: https://juejin.cn/post/7709708111435153408
observation_id: obs_547fdd5c5432e700f67a8df81dc05d8a86adb1364cf7204357b070a22a65df31
revision_id: rev_bf9f8f03d40f6eb8828b9e505e6f03f78541c20b1f155f280159e6acadea2252
event_id: evt_81f778dd23c493689c1dd9e95d13f20369a1bd80f09eabe29db45ee9a0580f17
lineage_relation: original
parent_observation_id: null
first_seen_at: 2026-11-19T13:01:05.458412Z
last_seen_at: 2026-11-19T13:02:28Z
---

## 转写说明

> 本文基于已校验的公开原文进行结构化转写与事实梳理，非原文转载。
> 转写保留可核验的技术事实，并将工程建议与来源观点明确分开。

- **原作者**: LV技术派
- **原始来源**: [https://juejin.cn/post/7709708111435153408](https://juejin.cn/post/7709708111435153408)
- **原文发布时间**: Thu, 19 Nov 2026 12:56:21 GMT

## 核心结论

来源实践的核心不是简单增加 Agent Session 数量，而是把调度单位从“对话窗口”提升为“任务”，再由唯一的 Router 统一协调多个 Worker。

任务状态不直接保存，而是根据窗口上报结果和交互事件实时推导；Router 只负责分诊、派活与协调，不编写代码，也不能代替用户完成任务验收。这样可以降低多会话切换、优先级插队和异常中断造成的任务遗忘。

工程上先保证单个任务的定义、验证与失败恢复能力，再扩大并发规模。否则任务越多、提问和异常越频繁，最终仍会受人的注意力上限约束。

## 能力机制

工作台采用三层结构：

- 项目对应代码仓库，并包含多个任务。
- 任务是一块画布，承载需求、spec、线框图、设计稿、开发报告和验收记录。
- Agent Session Window 是画布下的执行单元，可运行 Claude Code、Codex 等 CLI 或 GUI Agent。

任务具有未规划、待办、进行中、待审核、待验收、已完成、已取消七种状态。窗口每轮结束时通过 CLI 报告 `ready`、`blocked` 或 `dropped`；未报告便停止的窗口被视为“停了没说明”。任务综合自身全部窗口和用户交互事件计算状态。没有任何 Agent 报告能直接把任务置为已完成，用户验收后才会结束任务。

“精灵总管”是工作台唯一 Router，默认使用 Claude，也可在设置中切换。它能够批量创建任务、查询状态、调度 Agent Session，并处理历史任务的售后跟进。其权限边界是只调度、不实施：外部触发器只能把需求送入待办队列，是否立即开工仍由用户决定。

外部触发器可连接 GitHub、飞书群和 Jira。GitHub issue 根据过滤规则分诊，具备复现步骤的 bug 进入待办，模糊描述需要询问用户；验收通过后自动回写评论并关闭 issue。飞书机器人仅接受白名单成员触发，真实需求会创建任务与 Session，群内话题用于汇报进度，后续消息直接传给订阅该任务的 Session。

## 快速开始

先建立项目和任务画布，在任务下启动一个或多个 Agent Session。窗口每轮结束时，根据实际结果上报：

```bash
canvas-agents report ready
```

```bash
canvas-agents report blocked
```

```bash
canvas-agents report dropped
```

`ready` 表示完成并等待验收，`blocked` 表示需要用户回答，`dropped` 表示该工作项无需继续。若窗口停止但没有报告，应先在任务看板中检查等待原因。

需要外部需求时，将对应来源接入触发器：GitHub 用于 issue，Jira 用于工单，飞书用于群内请求。触发器创建的任务先进入待办，用户确认后再点击“立即开工”。执行期间由 Router 查询状态和调度窗口，完成后仍需用户验收。

## 适用边界

该架构适合需求需要多窗口并行、外部渠道持续进入任务、历史任务需要重新打开，以及用户希望从会话管理转向结果管理的场景。

Router 不承担编码和验收，外部输入不能直接驱动 Agent 修改代码；涉及结束任务、立即开工等关键动作时，仍保留人工确认。飞书触发还受白名单限制。

来源实现以本地配置为基础，但这一点不能推导为推理数据一定不离开本机。该方案依赖 Agent Session 的运行位置、触发器接入方式及外部系统配置，不能据此宣称数据隔离范围。

来源列出的技术栈包括 Excalidraw、Cloudflare Workers、D1、R2、Durable Objects、Daemon、Skill 与 CLI。来源称项目部署在 Cloudflare 服务上，每月成本 5 美元且包含其他项目，但未提供可独立核验的成本明细。

## 核验清单

来源事实核验：

- 任务是否覆盖七种状态，且状态由事件与窗口报告推导，而非直接保存？
- 窗口结束时是否区分完成、阻塞、放弃和未说明？
- Agent 是否只能把任务推进到待验收，无法自行完成任务？
- 是否只有一个 Router，且它没有编码和越权验收行为？
- GitHub 触发是否只创建待办任务，并保留“立即开工”的人工动作？
- 飞书触发是否配置白名单，并能把后续消息直接传给订阅 Session？
- 验收通过后，GitHub 评论与 issue 关闭是否实际执行？
- 单个任务能否回答定义正确、验证正确、失败可恢复三个问题？

实施建议是先用少量任务验证事件上报、阻塞恢复和人工验收，再接入更多触发器与并行窗口；后者属于由来源经验推导的落地顺序，并非来源给出的性能承诺。

## 来源与核验

- [原始文章](https://juejin.cn/post/7709708111435153408)
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