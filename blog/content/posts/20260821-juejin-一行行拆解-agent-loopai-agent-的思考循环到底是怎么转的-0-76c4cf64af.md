---
title: "一行行拆解 agent-loop：AI Agent 的\"思考循环\"到底是怎么转的"
date: 2026-08-21T05:45:57+08:00
draft: false
entry_kind: "auto"
tags: ["掘金", "工程实践", "来源转写"]
categories: ["AI 工程"]
source: "juejin"
content_mode: "evidence_backed_rewrite"
publication_tier: "B"
source_capture_mode: "full_article"
source_snapshot_sha256: "sha256:047dfe8a5f7895995238747624599faa9a93d894c0cb7b8ab7410a2071dbecc0"
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
description: "核心结论 agent-loop 的执行模型围绕两个层次构建。turn 是控制边界，从用户输入到达开始，到 agent 决定停止结束，一个 turn 可以包含零个或多个 step。step 是模型请求边界，每次模型调用及其触发的所有工具执行构成一个 step。"
external_url: https://juejin.cn/post/7676104122001195051
observation_id: obs_76c4cf64af1ce1ef088344643bf28bcf349a9e62a7fe91665c44dc131ee77f18
revision_id: rev_5742a68a366bc2bdc7043b9b28e6dcf72a0868bd3a80ab02d1a922c4c2ea44b9
event_id: evt_8fc17be28b5cb16d729a698b459c311a402da07c2e34a3bacb31762f91a3df96
lineage_relation: original
parent_observation_id: null
first_seen_at: 2026-08-20T21:43:00.389445Z
last_seen_at: 2026-08-20T21:45:57Z
---

## 转写说明

> 本文基于已校验的公开原文进行结构化转写与事实梳理，非原文转载。
> 转写保留可核验的技术事实，并将工程建议与来源观点明确分开。

- **原作者**: 怕浪猫
- **原始来源**: [https://juejin.cn/post/7676104122001195051](https://juejin.cn/post/7676104122001195051)
- **原文发布时间**: Thu, 20 Aug 2026 15:36:57 GMT

## 核心结论

agent-loop 的执行模型围绕两个层次构建。turn 是控制边界，从用户输入到达开始，到 agent 决定停止结束，一个 turn 可以包含零个或多个 step。step 是模型请求边界，每次模型调用及其触发的所有工具执行构成一个 step。step 结束时若模型未输出 tool_call，turn 即进入停止判断流程。

消息分发通过 inbox 机制实现。inbox 不是简单的先进先出队列，而是具有 next-turn 和 next-step 两个目标槽位的调度结构。用户消息进入 next-turn 槽位，工具执行产生的上下文消息进入 next-step 槽位。waking 类型的消息在 abort 状态下会被重定向到 next-turn 槽位，以启动新的 turn。

Phase 状态机管理 agent 的生命周期。idle 状态表示空闲，maintenance 状态执行 turn 结束后的清理，running 状态正在执行 step。maintenance 对外表现为 idle，但内部保留该区分是为了处理清理过程中收到新消息的场景。

工具调度支持并发执行。exclusive 模式形成 barrier，后续调用必须等待完成；parallel 模式进入 rolling pool，多个调用可同时执行。dispatch 可以重叠，但结果按模型给出的 tool_call 顺序依次提交到日志，这是为了保证日志中 tool/result 事件的顺序与模型后续请求的上下文一致。

## 能力机制

agent-loop 产生的事件分为多个层次。turn/start 和 turn/end 标记控制边界的起止。step/start 和 step/end 标记模型请求边界的起止。step 执行过程中会产生 user/message（领取的消息）、system-prompt/assemble waterfall（组装提示词）、agent/request waterfall（可修改模型配置）、llm/stream waterfall（流式输出）、assistant/chunk（流式分片，逐 token 追加日志）、assistant/message（组装后的完整回复，带 sourceEventSeqs 指向产生它的 chunk 序列号）、tool/call（工具调用，执行前记录）、tool/result（工具结果）、step/end 等事件。

inbox 提供 inserted、discarded、claimed 三个事件，分别在消息被插入、丢弃、领取时触发。dispatch 区分 waterfall 和 serial 两种分发模式。waterfall 事件按顺序执行各监听器，前一个监听器的输出作为下一个的输入，可用于 agent/pre-step 拦截消息或 agent/request 修改模型配置。serial 事件同样顺序执行，但监听器可以通过向 inbox 注入消息来影响后续流程，agent/turn-stopping 采用此模式以支持续跑决策。

turn-stopping 判断逻辑在 inbox 检查上执行两次。先检查 next-step inbox 是否为空，然后分发 serial 事件，最后再次检查 inbox。若 serial 监听器注入了新消息，turn 将继续执行。

工具调度的执行结果包含 concluded 标记，标记为 true 时表示工具认为任务完成，step 以 completed 结束。若 step 因 max-tokens 达到 token 上限结束，该结果具有 sticky 语义，后续 step 即使正常完成也不会降级 turn 的结束原因。

abort 处理时，调度器停止启动新调用，等待已启动的调用完成，为已启动的调用正常提交结果，为未启动的调用追加合成的跳过事件并标记 TOOL_ABORTED_BEFORE_DISPATCH 错误码。

## 快速开始

源码位于 packages/core/agent-loop/ 目录，核心文件为 agent.ts 和 tool-calls.ts。agent.ts 定义 Phase 类型，包含 idle、maintenance、running 三种状态。agent 对象通过 Inbox 类管理消息队列，构造函数接收 session 和回调配置。

Inbox 的 splice 方法用于向指定槽位添加消息，第一个参数为目标槽位 next-turn 或 next-step，后续参数为消息数组。send 方法是向 inbox 发送消息的入口，支持指定目标槽位和唤醒标记。claim 方法在 turn 或 step 开始时领取消息。

executeToolCalls 函数是工具调度的入口，接收工具调用块列表、执行信号和上下文回调，返回包含 concluded 和 aborted 标记的结果对象。每个工具调用块可查询 executionMode 确定是 exclusive 还是 parallel 模式。

## 适用边界

turn 边界由 turn-stopping 决定。停止条件为 agent/turn-stopping serial 事件执行完成且 next-step inbox 为空。若 serial 监听器注入了续跑消息，turn 将继续执行。

step 边界由模型输出决定。step 以 completed 结束当且仅当模型返回无 tool_call；step 以 max-tokens 结束当且仅当达到 token 上限；step 以 null 继续当且仅当存在 tool_call 且 concluded 标记为 false。

inbox 消息优先级由目标槽位决定。用户输入消息和 abort 后的 waking 消息进入 next-turn 槽位；工具执行产生的上下文消息进入 next-step 槽位。同一槽位内消息按插入顺序处理。

工具并发度由 execution mode 决定。parallel 模式的调用可同时执行但结果必须按顺序提交；exclusive 模式的调用形成 barrier，后续所有调用必须等待其完成。

## 核验清单

验证 Turn 与 Step 关系时需确认：1 个 turn 包含 0…N 个 step；turn 结束需要 turn-stopping 通过且 inbox 为空；step 结束有 completed、max-tokens、null 三种结果。

验证 inbox 机制时需确认：next-turn 槽位存放用户消息；next-step 槽位存放工具上下文；waking 消息在 abort 状态下被重定向到 next-turn。

验证 Phase 状态机时需确认：idle 可被 wakeup 唤醒进入 running；running 的 turn 结束后进入 maintenance；maintenance 清理完成后进入 idle；maintenance 中收到新消息可跳过 idle 直接进入 running。

验证事件分发模式时需确认：waterfall 事件允许监听器修改后续输入；serial 事件允许监听器向 inbox 注入消息；agent/turn-stopping 的两次 inbox 检查是设计而非实现缺陷。

验证工具调度时需确认：parallel 模式的调用结果按原始顺序提交；abort 时已完成调用的结果正常提交，未启动的调用合成跳过事件；dispatch 重叠但提交有序是为了保证日志顺序与模型上下文一致。

验证 max-tokens sticky 语义时需确认：一旦某 step 触发 max-tokens，后续 step 的 completed 结果不覆盖 turn 的结束原因。

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