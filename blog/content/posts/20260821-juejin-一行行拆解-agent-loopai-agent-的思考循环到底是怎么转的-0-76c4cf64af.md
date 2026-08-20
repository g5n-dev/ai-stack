---
title: "一行行拆解 agent-loop：AI Agent 的\"思考循环\"到底是怎么转的"
date: 2026-08-21T00:53:24+08:00
draft: false
entry_kind: "auto"
tags: ["掘金", "工程实践", "来源转写"]
categories: ["AI 工程"]
source: "juejin"
content_mode: "evidence_backed_rewrite"
publication_tier: "B"
source_capture_mode: "full_article"
source_snapshot_sha256: "sha256:b45d256cb03ea9b0fcd9896af6b31cee66d7b643b6307a0e46a0b1cdb998cb9a"
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
description: "核心结论 DeepSeek Harness 的 agent-loop 存在两个层次的执行边界。Turn 是控制边界，由用户输入触发，到 agent 决定停止结束，一个 turn 包含零个到多个 step。Step 是模型请求边界，每次 step 执行一次模型调用以及该调用产生的全部工具调用。"
external_url: https://juejin.cn/post/7676104122001195051
observation_id: obs_76c4cf64af1ce1ef088344643bf28bcf349a9e62a7fe91665c44dc131ee77f18
revision_id: rev_5742a68a366bc2bdc7043b9b28e6dcf72a0868bd3a80ab02d1a922c4c2ea44b9
event_id: evt_8fc17be28b5cb16d729a698b459c311a402da07c2e34a3bacb31762f91a3df96
lineage_relation: original
parent_observation_id: null
first_seen_at: 2026-08-20T16:50:22.155071Z
last_seen_at: 2026-08-20T16:53:24Z
---

## 转写说明

> 本文基于已校验的公开原文进行结构化转写与事实梳理，非原文转载。
> 转写保留可核验的技术事实，并将工程建议与来源观点明确分开。

- **原作者**: 怕浪猫
- **原始来源**: [https://juejin.cn/post/7676104122001195051](https://juejin.cn/post/7676104122001195051)
- **原文发布时间**: Thu, 20 Aug 2026 15:36:57 GMT

## 核心结论

DeepSeek Harness 的 agent-loop 存在两个层次的执行边界。Turn 是控制边界，由用户输入触发，到 agent 决定停止结束，一个 turn 包含零个到多个 step。Step 是模型请求边界，每次 step 执行一次模型调用以及该调用产生的全部工具调用。

Agent 内部通过 inbox 收件箱接收消息，inbox 分为 next-turn 和 next-step 两个槽位，分别服务于下一个 turn 和当前 turn 的下一个 step。核心状态机有三个相位：idle 表示空闲等待，maintenance 表示 turn 结束后的清理阶段，running 表示正在执行 step。外部仅暴露 idle 和 running 两种状态。

## 能力机制

Agent 的事件流从 turn/start 开始，依次经过 pre-step 决策、step 执行和 turn-stopping 判断。pre-step 阶段分发 waterfall 事件，监听器可以修改消息内容或拒绝进入 step。step 执行时，先从 inbox 领取消息，再组装 system prompt，然后发起模型请求并流式处理返回的 chunk，最后根据模型是否输出 tool_call 决定是执行工具还是结束 step。

工具调度支持两种执行模式。exclusive 模式形成 barrier，后续调用必须等待它完成。parallel 模式进入 rolling pool，多个调用可以并发执行。调度器保证 dispatch 可以重叠，但结果必须按模型给出的 tool_call 顺序提交到日志。这一设计确保了消息历史的顺序一致性。

abort 处理采用 drain 策略：停止启动新调用，等待已启动的调用完成，为已启动调用正常提交结果，为未启动调用追加带 TOOL_ABORTED_BEFORE_DISPATCH 错误码的合成结果事件。max-tokens 结束原因具有 sticky 语义，一旦某 step 因达到 token 上限结束，后续 step 即使正常完成也不覆盖该结束原因。

## 快速开始

本节内容基于源码拆解，不涉及直接可执行的命令。若要基于 agent-loop 设计类似架构，需要关注以下实现要点：

消息进入 inbox 使用 send 方法，可指定目标槽位为 next-turn 或 next-step，并支持 waking 参数在 abort 后重新触发 turn。状态切换通过 setPhase 方法执行，同时分发 agent/status 事件通知外部。turn-stopping 判断在检查 inbox 为空后分发 serial 事件，监听器可在该阶段注入续跑消息。

工具调度的核心函数是 executeToolCalls，位于 packages/core/agent-loop/src/tool-calls.ts，通过 executionMode 判断每个调用的执行模式。

## 适用边界

本文档描述的机制适用于需要实现多轮交互式 agent 的场景。Turn 和 step 的分离设计适合需要动态决定调用次数的复杂任务。Inbox 机制适合需要灵活调度用户消息与工具执行结果的消息驱动架构。

Phase 状态机的三层设计适合需要优雅处理中断和清理的场景。serial 事件机制适合需要在 turn 结束前提供最后一次拦截机会的扩展需求。

不适合的场景包括：单次请求即可完成的任务不需要 turn/step 分离；需要严格实时响应的场景不适合流式处理和状态机开销；需要完全同步执行的场景不适合 rolling pool 并发调度。

## 核验清单

检查 agent-loop 实现的完整性时，可按以下维度验证：

架构层面：确认 Turn 与 Step 的边界定义清晰，控制流是否正确区分了控制边界与模型请求边界。Inbox 槽位是否正确区分 next-turn 和 next-step，消息重定向逻辑（wakingAfterAbort）是否正确实现。

状态机层面：三个 phase 的定义是否完整，转换路径是否覆盖所有场景，外部状态暴露是否准确反映了内部状态。turn-stopping 的双重检查逻辑是否正确处理了监听器注入消息的情况。

事件流层面：pre-step waterfall 是否支持消息修改和拒绝进入。agent/request waterfall 是否支持配置修改。流式输出的 chunk 是否正确追加日志并关联到 assistant/message。

工具调度层面：exclusive 和 parallel 两种模式的 barrier 与 rolling pool 是否正确实现。结果提交顺序是否与模型顺序一致。abort 时的 drain 策略和合成事件是否完整。

特殊语义层面：max-tokens 的 sticky 语义是否正确实现，sourceEventSeqs 是否正确关联 chunk 序列号。

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