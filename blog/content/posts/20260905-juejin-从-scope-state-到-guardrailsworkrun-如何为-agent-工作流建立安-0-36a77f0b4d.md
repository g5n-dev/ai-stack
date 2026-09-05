---
title: "从 Scope State 到 Guardrails：Workrun 如何为 Agent 工作流建立安全边界"
date: 2026-09-05T17:08:02+08:00
draft: false
entry_kind: "auto"
tags: ["掘金", "工程实践", "来源转写"]
categories: ["AI 工程"]
source: "juejin"
content_mode: "evidence_backed_rewrite"
publication_tier: "B"
source_capture_mode: "full_article"
source_snapshot_sha256: "sha256:846715eb400adcd37fe4a4c17ee6f92e21aa7bb776be19419bb1eb98e03ac945"
source_payload_sha256: "sha256:3d6fe8824b625d426b57eee80da16436b7c8ba5aaa36599ecb460cf8daadbf07"
source_published_at: 2026-09-04T01:31:59Z
timestamp_confidence: feed
extractor_version: "source-contract-v2"
discovery_method: "article_html"
source_completeness: "complete"
parent_snapshot_sha256: "sha256:63f2d4288ea14f3e4fe55083788aaa58d332fb2a67a8c4751cf8756cf6ce8c76"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 54
description: "核心结论 Workrun 通过架构约束而非 Prompt 劝导实现 Agent 工作流的安全边界。该工具将工作流状态拆分为 Visible State 与 Raw State 两套视图，Prompt 只能访问脱敏后的可见状态，敏感数据仅在工具执行时通过受控绑定机制恢复。"
external_url: https://juejin.cn/post/7681202345804988416
observation_id: obs_36a77f0b4d363d0a92924462aefaee1d97f0206788852c5253a852465dab7243
revision_id: rev_dfb04b2c689eaeac0fa2a005c1c629b038bf67137c0325b447fc33c9bc2f8f56
event_id: evt_18fbb00b234419d00a3b8da6745bf0491fc10d26de445f38fa30cac6d8db8532
lineage_relation: original
parent_observation_id: null
first_seen_at: 2026-09-05T09:04:49.399792Z
last_seen_at: 2026-09-05T09:08:02Z
---

## 转写说明

> 本文基于已校验的公开原文进行结构化转写与事实梳理，非原文转载。
> 转写保留可核验的技术事实，并将工程建议与来源观点明确分开。

- **原作者**: 梦想很大很大
- **原始来源**: [https://juejin.cn/post/7681202345804988416](https://juejin.cn/post/7681202345804988416)
- **原文发布时间**: Fri, 04 Sep 2026 01:31:59 GMT

## 核心结论

Workrun 通过架构约束而非 Prompt 劝导实现 Agent 工作流的安全边界。该工具将工作流状态拆分为 Visible State 与 Raw State 两套视图，Prompt 只能访问脱敏后的可见状态，敏感数据仅在工具执行时通过受控绑定机制恢复。系统在输入端、工具调用端和输出端均部署了 Guardrails 硬规则，任何未经授权的数据访问都会被直接阻断而非静默放行。

## 能力机制

**Scope State 数据隔离机制**

Workrun 为每个节点分配独立的 State Namespace。节点输出默认私有，需显式配置才能对外暴露。敏感字段在工作流输入层通过 `sensitiveFields` 标记，被标记的字段自动转为占位符形式存在于 Visible State 中。

工作流存在三套状态视图：Raw State 保存原始输入仅存于内存；Visible State 用于 Agent Prompt、UI 和日志展示；节点私有 State 包含该节点产生的所有字段。配置 `globalKeys` 可将特定字段发布到全局可见范围，配置 `readers` 可授权下游节点访问本节点已发布的 State。

**Tool State Binding 工具状态绑定**

当 Agent 生成的参数值为占位符时，系统在工具执行前检查节点是否拥有对应 statePath 的 `rawReaders` 授权。若已授权，根据 AST 路径在 Raw State 中查找真实值并精准替换；若未授权，保持占位符并拒绝执行工具。绑定仅替换模型显式生成的参数路径，不会将整份 Raw State 注入请求。

**Guardrails 边界硬规则**

输入 Guardrail 在用户 Prompt 进入模型前进行扫描。常规 PII（邮箱、电话、IP、身份证号等）转换为脱敏占位符后放行；认证凭证（Bearer Token、`sk-` Key、GitHub/AWS Token、PEM 私钥）直接拒绝执行并报错。

输出 Guardrail 在工具结果写回 Agent 上下文、工作流日志及前端 UI 事件前介入，将敏感数据强制清洗为脱敏形式。流式输出场景下，需经过输出 Guardrail 的消息在 Rust 后端做 Chunk 汇聚缓存，待完整消息形成并脱敏后统一推送。

## 快速开始

工作流配置流程如下：

在工作流设置中添加输入字段，将 `crmToken` 标记为敏感字段，并在 Raw input readers 中仅授权需要原始值的节点。创建 Tool App 时配置输入参数与输出 Schema，工具代码使用 workrun_sdk.tool 装饰器。在节点 Inspector 中配置 State 访问权限：通过 `globalKeys` 发布需共享的字段，通过 `sensitiveFields` 强制脱敏特定字段，通过 `rawReaders` 授权 Raw State 访问。配置 Tool State Binding 将工具参数映射到 State 路径。

## 适用边界

该安全机制适用于需要严格数据隔离的 Multi-Agent 工作流。当不同节点对数据的可见范围有差异化需求时，Scope State 能够在架构层面强制执行隔离策略，避免依赖模型自身的指令遵循能力。

对于需要调用外部 API 且必须使用真实凭证的工具场景，Tool State Binding 提供了一种受控的数据恢复路径。凭证无需出现在 Prompt 中，工具执行时按需注入，降低了 Prompt 注入攻击的风险窗口。

## 核验清单

验证安全机制有效性需确认以下要点：

节点 Prompt 中敏感字段是否显示为占位符形式，而非明文。未配置 `rawReaders` 的节点在工具调用阶段是否收到拒绝执行错误。工具执行时是否能够获取到真实值（通过日志或调试输出确认）。输出 Guardrail 是否成功清洗工具返回结果中的敏感信息。流式输出场景下，单个 Chunk 是否无法匹配敏感数据正则。

## 来源与核验

- [原始文章](https://juejin.cn/post/7681202345804988416)
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