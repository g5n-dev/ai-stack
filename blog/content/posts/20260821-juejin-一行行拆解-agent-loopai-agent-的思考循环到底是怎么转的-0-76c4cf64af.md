---
title: "一行行拆解 agent-loop：AI Agent 的\"思考循环\"到底是怎么转的"
date: 2026-08-21T06:47:22+08:00
draft: false
entry_kind: "auto"
tags: ["掘金", "工程实践", "来源转写"]
categories: ["AI 工程"]
source: "juejin"
content_mode: "evidence_backed_rewrite"
publication_tier: "B"
source_capture_mode: "full_article"
source_snapshot_sha256: "sha256:86581e5bded13dd07dc629fab3961d8ad3c7cab37fe3082fe04edc29a0a1a3c3"
source_payload_sha256: "sha256:c0db0060d2b3cf1d2446dc1e81d1ba27e5da9087d7dc7ce8444e05f7dbb52369"
source_published_at: 2026-08-20T15:36:57Z
timestamp_confidence: feed
extractor_version: "source-contract-v2"
discovery_method: "article_html"
source_completeness: "complete"
parent_snapshot_sha256: "sha256:74824ec49716ded25f576c6b2a6968fc2820cef758efb04d5c00c348d82a3207"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 40
description: "核心结论 agent-loop 是驱动 AI Agent 运转的核心引擎，采用双层循环结构实现任务执行与状态管理。**turn（轮次）** 是控制边界，定义从用户输入到决策停止的完整交互；**step（步骤）** 是模型请求边界，每次模型调用及其触发的工具执行构成一个 step。两者都是可中止的单元。"
external_url: https://juejin.cn/post/7676104122001195051
observation_id: obs_76c4cf64af1ce1ef088344643bf28bcf349a9e62a7fe91665c44dc131ee77f18
revision_id: rev_5742a68a366bc2bdc7043b9b28e6dcf72a0868bd3a80ab02d1a922c4c2ea44b9
event_id: evt_8fc17be28b5cb16d729a698b459c311a402da07c2e34a3bacb31762f91a3df96
lineage_relation: original
parent_observation_id: null
first_seen_at: 2026-08-20T22:45:02.358375Z
last_seen_at: 2026-08-20T22:47:22Z
---

## 转写说明

> 本文基于已校验的公开原文进行结构化转写与事实梳理，非原文转载。
> 转写保留可核验的技术事实，并将工程建议与来源观点明确分开。

- **原作者**: 怕浪猫
- **原始来源**: [https://juejin.cn/post/7676104122001195051](https://juejin.cn/post/7676104122001195051)
- **原文发布时间**: Thu, 20 Aug 2026 15:36:57 GMT

## 核心结论

agent-loop 是驱动 AI Agent 运转的核心引擎，采用双层循环结构实现任务执行与状态管理。**turn（轮次）** 是控制边界，定义从用户输入到决策停止的完整交互；**step（步骤）** 是模型请求边界，每次模型调用及其触发的工具执行构成一个 step。两者都是可中止的单元。

系统内部维护一个 Phase 状态机，包含 idle、maintenance、running 三种状态，通过事件分发驱动消息处理与工具调度。所有执行动作均生成可回放的事件日志，每条 tool/call 必有对应的 tool/result。

## 能力机制

agent-loop 的消息传递依赖 Inbox（收件箱）机制。Inbox 维护两个槽位：next-turn 接收用户消息，在新 turn 开始时领取；next-step 接收工具执行产生的上下文消息，在当前 turn 的后续 step 中领取。消息进入 inbox 时会触发 inserted 事件，被丢弃时触发 discarded 事件，被领取时触发 claimed 事件。

工具执行采用并发调度模型。execution mode 为 exclusive 的工具形成 barrier，后续调用必须等待其完成；mode 为 parallel 的工具进入 rolling pool，可并行执行。调度器保证 dispatch 可以重叠，但结果必须按模型顺序提交。abort 发生时，系统会 drain 已启动的调用并为未启动调用合成带有 TOOL_ABORTED_BEFORE_DISPATCH 错误码的跳过事件，以保持日志完整性。

事件分发机制包含三种模式：waterfall（瀑布链式）、serial（串行阻塞）和 durable（持久追加）。waterfall 允许监听器修改配置后继续传递；serial 保证顺序执行且监听器可向 inbox 注入续跑消息；durable 用于日志追加，确保 step/start、assistant/chunk、tool/call、tool/result 等事件被持久化记录。

## 快速开始

agent-loop 源码位于 `packages/core/agent-loop/` 目录，核心文件为 `agent.ts` 和 `tool-calls.ts`。状态机在 `setPhase` 方法中更新 phase 并对外暴露 agent/status 事件，可通过监听该事件获取 agent 状态变化。

消息发送调用 `agent.send(message, target, wakeup)` 方法，target 指定目标槽位，wakeup 决定是否唤醒 agent 循环。wakingAfterAbort 逻辑会将中断后的唤醒消息重定向至 next-turn 槽位，确保不污染已中止的 turn。

pre-step 决策通过 `dispatch.waterfall('agent/pre-step')` 分发，可监听该事件修改消息内容或返回 reject 阻止 step 执行。模型请求配置通过 `dispatch.waterfall('agent/request')` 分发，监听器可修改 provider、model、reasoningEffort 等参数。

## 适用边界

turn 的结束条件是 turn-stopping serial 事件通过且 next-step inbox 为空。serial 事件检查两次 inbox 的设计允许监听器在第一次检查后注入续跑消息，实现动态续跑逻辑。如果 pre-step 返回 reject，当前 turn 直接以 blocked 结束，不会产生任何 step。

step 的结束原因分为三种：max-tokens 表示达到 token 上限、completed 表示无 tool_call、null 表示仍有 tool_call 等待执行。max-tokens 具有 sticky 语义——一旦某个 step 因 max-tokens 结束，后续 step 的正常完成不会降级 turn 结束原因。

外部可见的 agent 状态只有 idle 和 running 两种。maintenance 状态对外表现为 idle，因为此时不在执行模型请求，但内部区分维护状态是为了处理「清理过程中收到新消息」的场景，避免消息被错误地纳入已结束的 turn。

## 核验清单

agent-loop 的事件日志是完整的回放链：每条 assistant/message 携带 sourceEventSeqs 指向产生它的 assistant/chunk 序列号，每条 tool/result 通过 callSeqs 关联对应的 tool/call。这保证了日志可用于精确回放与问题追踪。

Phase 状态机的转换路径为：idle 经 wakeup 进入 running，running 结束 turn 后进入 maintenance，maintenance 清理完成后返回 idle，或在收到 wakeup 时直接进入新的 running。

工具调度的三个 waterfall 事件按顺序为 tools/pre-execute、tools/execute、tools/post-execute，分别在工具执行前后提供扩展点。inbox 不是简单的 FIFO 队列，而是有优先级和目标槽位的调度结构，这是区分 turn/step 边界的关键设计。

## 来源与核验

- [原始文章](https://juejin.cn/post/7676104122001195051)
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