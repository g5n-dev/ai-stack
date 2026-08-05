---
title: "AI Engineering 五代演进史：Prompt、RAG、Agent 到 Graph 的架构革命"
date: 2026-08-03T19:46:03+08:00
draft: false
entry_kind: "auto"
tags: ["掘金", "工程实践", "来源转写"]
categories: ["AI 工程"]
source: "juejin"
content_mode: "evidence_backed_rewrite"
publication_tier: "B"
source_capture_mode: "full_article"
source_snapshot_sha256: "sha256:a70400cd1c8664a36f39cc33e86c94cc2363e7069fbcae4e988c577d4e227a9c"
source_payload_sha256: "sha256:d3c3b8e9a4f4ec619d09611fecdfa9c033464e2df7912e87c1f8f7b21f704ace"
source_published_at: 2026-08-03T10:58:20Z
timestamp_confidence: feed
extractor_version: "source-contract-v2"
discovery_method: "article_html"
source_completeness: "complete"
parent_snapshot_sha256: "sha256:bb0e38e64688dcb3f1855cb836c725c762522e9cc6e31aeeae4fb52c25712df6"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 51
description: "核心结论 大模型工程在不到五年间经历了五代技术演进：Prompt Engineering、Chain、Vector RAG 与 Workflow、Agentic RAG 与 Multi-Agent、Graph Engineering。这一演进并非技术替代，而是每代都在解决前代无法应对的核心问题。"
external_url: https://juejin.cn/post/7669620584251129908
observation_id: obs_987d2ee03ec347db7491660d83e159e2c08fcf9fa4fee02bf8ac74010b0061c5
revision_id: rev_23c6ccefaa24c982f8e9dab2c95fbcc392766b9f936f2c58ba8dd991923728e7
event_id: evt_31f5ce868d6a759b797b8e66e71167842a5bb45a16dfa31f78f1abe5214a21f3
lineage_relation: original
parent_observation_id: null
first_seen_at: 2026-08-03T19:57:14.224757Z
last_seen_at: 2026-08-03T11:46:03Z
---

## 转写说明

> 本文基于已校验的公开原文进行结构化转写与事实梳理，非原文转载。
> 转写保留可核验的技术事实，并将工程建议与来源观点明确分开。

- **原作者**: shengjk1
- **原始来源**: [https://juejin.cn/post/7669620584251129908](https://juejin.cn/post/7669620584251129908)
- **原文发布时间**: Mon, 03 Aug 2026 10:58:20 GMT

## 核心结论

大模型工程在不到五年间经历了五代技术演进：Prompt Engineering、Chain、Vector RAG 与 Workflow、Agentic RAG 与 Multi-Agent、Graph Engineering。这一演进并非技术替代，而是每代都在解决前代无法应对的核心问题。Prompt 解决了与大模型的沟通问题；Chain 解决了多步推理的编排问题；RAG 解决了模型缺乏企业知识的问题；Agent 引入了自主决策的循环机制；Graph 则开始解决工业化场景中复杂 Agent 的编排与管理问题。整个演进的主线是将 AI 从“一次推理”逐步演进为“持续运行、可管理、可观测的智能系统”。

## 能力机制

第一代 Prompt Engineering 基于上下文学习能力，通过指令、示例、角色等元素引导模型输出，本质上仍属单次推理。第二代 Chain 将复杂任务拆解为多个 Prompt 串联，形成 Pipeline，提升了可维护性和可复用性。第三代 Vector RAG 与 Workflow 结合了向量检索与任务编排，使模型首次具备外部知识访问能力。第四代 Agentic RAG 与 Multi-Agent 引入了 ReAct Loop，模型可自主执行“思考-行动-观察”的循环迭代，具备自我修正和持续探索能力。第五代 Graph Engineering 采用图结构作为核心数据结构，能够统一表达条件分支、循环控制、状态恢复、并发执行、异常处理等复杂逻辑，解决了 Agent 时代流程失控的问题。

## 快速开始

来源未提供可执行的命令示例或代码片段。关于工具选型，来源列举了五代技术对应的代表性框架：LangChain、LlamaIndex、Haystack、Dify、Flowise 等用于 Workflow 阶段；LangGraph、Google ADK、CrewAI Flow、OpenAI Responses API、Anthropic Agent SDK 等用于 Graph 阶段。具体技术选型需根据实际场景和项目需求评估，来源未给出推荐配置或必选组件。

## 适用边界

Prompt Engineering 受限于单次推理范式，无法访问实时数据或执行外部操作。Chain 虽然支持多步推理，但本质仍为有向无环图，不具备循环回退能力。RAG 系统缺乏主动纠错机制，当检索失败或结果不准确时无法自主重试。Agent 在复杂任务中容易陷入循环调用、上下文膨胀和 token 成本失控，尤其当涉及多个 Agent 协作时，冲突与重复问题更为突出。Graph Engineering 虽在表达能力上更为完整，但图结构的设计复杂度较高，对开发者提出了更高的系统设计要求，且来源未明确指出其性能边界或规模化部署的具体限制。

## 核验清单

检查文章的核心论点是否与来源一致：大模型工程经历了五代清晰的技术跃迁，每代解决的问题分别为沟通协调、多步编排、外部知识、自主决策、复杂管理。确认技术代际划分：Prompt 为第一代，Chain 为第二代，Vector RAG 与 Workflow 为第三代，Agentic RAG 与 Multi-Agent 为第四代，Graph Engineering 为第五代。核实代表性工具名称：LangChain、LlamaIndex、LangGraph 在来源中明确出现。验证 Loop 机制描述：ReAct Loop 的“思考-行动-观察”循环在来源中有完整阐述。确认演进主线的表述：来源明确指出核心主线是让 AI 从一次推理演进为持续完成任务。需注意来源未提供性能数据、具体配置示例或可执行的命令序列。

## 来源与核验

- [原始文章](https://juejin.cn/post/7669620584251129908)
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