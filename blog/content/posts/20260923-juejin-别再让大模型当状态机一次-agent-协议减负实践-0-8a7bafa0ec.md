---
title: "别再让大模型当状态机：一次 Agent 协议减负实践"
date: 2026-09-23T02:57:15+08:00
draft: false
entry_kind: "auto"
tags: ["掘金", "工程实践", "来源转写"]
categories: ["AI 工程"]
source: "juejin"
content_mode: "evidence_backed_rewrite"
publication_tier: "B"
source_capture_mode: "full_article"
source_snapshot_sha256: "sha256:7df2bdaea6fcf192ddb21ec1b734f0015c53f9bbd24af05bc90b0800d46b2bde"
source_payload_sha256: "sha256:6f68b6df142214c070a3f6f9ab2bcc1734d7a074263c8c39f4b53dc7a813e94b"
source_published_at: 2026-09-22T17:16:41Z
timestamp_confidence: feed
extractor_version: "source-contract-v2"
discovery_method: "article_html"
source_completeness: "complete"
parent_snapshot_sha256: "sha256:f10d79e96ced9f306b818a86bdc53af6d7d6476c308eb2cd40bb949aa21aecbe"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 26
description: "核心结论 运行时应持有客观系统事实，模型负责语义理解和下一步提议。这两条原则构成Agent协议设计的核心约束：运行时已经知道的，不要让模型再维护；运行时不知道的，不要假装它知道。"
external_url: https://juejin.cn/post/7688282672251207718
observation_id: obs_8a7bafa0eca399599c8155f45911e49165f268b00413914afb7c33418f92aadf
revision_id: rev_e3eae257acc0d8bf545ddb58849eaae6f060cd4b9fbea0e5397e397839cdbe9d
event_id: evt_2b814548769249a03d5885bbb4c70f5438943a2dc1f4053eabca4eed15f6040a
lineage_relation: original
parent_observation_id: null
first_seen_at: 2026-09-22T18:54:28.578792Z
last_seen_at: 2026-09-22T18:57:15Z
---

## 转写说明

> 本文基于已校验的公开原文进行结构化转写与事实梳理，非原文转载。
> 转写保留可核验的技术事实，并将工程建议与来源观点明确分开。

- **原作者**: hpoenixf
- **原始来源**: [https://juejin.cn/post/7688282672251207718](https://juejin.cn/post/7688282672251207718)
- **原文发布时间**: Tue, 22 Sep 2026 17:16:41 GMT

## 核心结论

运行时应持有客观系统事实，模型负责语义理解和下一步提议。这两条原则构成Agent协议设计的核心约束：运行时已经知道的，不要让模型再维护；运行时不知道的，不要假装它知道。

早期的结构化AgentTurn协议让模型同时承担语义研究和系统状态维护，导致状态镜像漂移、模型注意力分散，以及任何字段失配都可能触发整轮重试。实验表明，当协议字段增多时，模型输出的正确率会显著下降。

更优的路径是采用原生工具调用：模型只提出语义动作（search、read、publish、finish），运行时负责授权、工具执行、持久化、执行回执和终态门控。删除的是模型生成的整轮状态协议，而非主机持有的ModelTurn边界。

## 能力机制

Agent中存在两类复杂度必须分开处理。语义复杂度包括用户真实意图、下一步调查方向、资料冲突判断和结论解释方式。系统复杂度包括工具权限、调用执行、结果落库、引用范围和终态判断。前者需要模型开放式的语义判断，后者是系统可客观验证的事实。

运行时持有权限、工具可见性和作用域。模型持有工具选择能力。工具可见性由运行时根据用户权限、任务限制和数据源状态派生，无需模型维护availableTools状态镜像。当模型申请新能力获批时，工具契约改变，旧响应中的后续动作不应跨新契约边界执行，应开启下一ModelTurn让模型在新工具集合下重新决策。

finish()是语义结束提议，不是终态写入权限。运行时只校验客观条件（是否有正式输出、引用是否有效、是否存在未结算调用），不判断答案完整性或风险说明充分性。

## 快速开始

将模型协议从整轮状态描述简化为语义动作提议。核心变化体现在协议结构：

旧路径是模型输出AgentTurn JSON描述完整状态。改为模型直接调用search、read、publish等原生工具，运行时固化ModelTurn后执行并返回结果。

finish()调用方式示意如下，模型在满足语义研究结束时提出：

```
finish()
```

主机在ModelTurn闭合后记录：本轮内容、提出的调用、调用的顺序、已执行的调用、已落库的结果和每次执行的回执。

环境变量命名示例（不包含具体值）：

```
API_KEY
RUNTIME_STATE_PATH
```

## 适用边界

这套协议设计适用于需要严格工程边界的Agent系统，包括投资研究、文档分析、数据处理等多轮对话场景。核心前提是系统需要持久化、审计、权限控制和恢复能力。

不适用于纯提示式交互场景，此时工程控制需求较弱，模型直接输出答案即可。

需要区分的是：运行时可强制执行显式权限、作用域、持久化、调用顺序和终态条件。但不能根据自由文本措辞伪装成客观规则去判断意图、完整性或答案质量。这些属于开放语义判断，应让模型表达不确定或提议澄清。

## 核验清单

在新增模型字段或运行时状态时，应逐项确认：

此信息是否为运行时唯一拥有的客观事实，模型输出是否仅为状态镜像而非模型独有的语义判断。

字段表达的是模型语义判断还是系统已发生的事实。finish()调用是语义结束提议还是偷偷写入系统终态。

恢复依据是否为真实落库事实和执行回执，而非模型上次自报状态。

局部错误是否仅产生局部结果，允许模型在下一Turn中自行决定修正，而非重新生成完整协议。

历史压缩中用户原始约束是否仍由Runtime保留原始输入，事实所有权是否未转交给摘要模型。

## 来源与核验

- [原始文章](https://juejin.cn/post/7688282672251207718)
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