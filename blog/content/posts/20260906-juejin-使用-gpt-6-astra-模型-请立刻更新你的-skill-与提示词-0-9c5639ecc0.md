---
title: "使用 GPT-6 Astra 模型 请立刻更新你的 Skill 与提示词"
date: 2026-09-06T00:07:27+08:00
draft: false
entry_kind: "auto"
tags: ["掘金", "工程实践", "来源转写"]
categories: ["AI 工程"]
source: "juejin"
content_mode: "evidence_backed_rewrite"
publication_tier: "B"
source_capture_mode: "full_article"
source_snapshot_sha256: "sha256:e4d22bb4709943797ef7e28a361982dd93b9e4d56f950a63630a206d7dfc9769"
source_payload_sha256: "sha256:c286d448a0d44612e98efe3e37c7b7fb3dd9b8e0548a4ebd79572435aae233c3"
source_published_at: 2026-09-05T15:59:09Z
timestamp_confidence: feed
extractor_version: "source-contract-v2"
discovery_method: "article_html"
source_completeness: "complete"
parent_snapshot_sha256: "sha256:ce1065a0d7af0361f74d41778ebd0225b850c11b3e23ec95fe35b73b894deecf"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 36
description: "核心结论 OpenAI 研发人员指出，随着 GPT-6 Astra 模型能力的提升，过去为旧模型设计的冗长规则和强制流程可能已转化为拖累性能的负优化。编程智能体的最佳实践正在快速演进，长期在项目中积累的 Skills、AGENTS.md 配置和任务提示词值得重新审视。"
external_url: https://juejin.cn/post/7681858280943403059
observation_id: obs_9c5639ecc003430585a38a97fced91d5098593a172e903187ed366d297d4dbf4
revision_id: rev_9b0bb51803e3cc03f38f5c197223a81cd408608ceaf7c3d924cab2de933fa627
event_id: evt_126e08a210a21356ebd4103613987c92547b5494cd1a514c06fa3f4c04f261f7
lineage_relation: original
parent_observation_id: null
first_seen_at: 2026-09-05T16:04:08.884684Z
last_seen_at: 2026-09-05T16:07:27Z
---

## 转写说明

> 本文基于已校验的公开原文进行结构化转写与事实梳理，非原文转载。
> 转写保留可核验的技术事实，并将工程建议与来源观点明确分开。

- **原作者**: BingoGo
- **原始来源**: [https://juejin.cn/post/7681858280943403059](https://juejin.cn/post/7681858280943403059)
- **原文发布时间**: Sat, 05 Sep 2026 15:59:09 GMT

## 核心结论

OpenAI 研发人员指出，随着 GPT-6 Astra 模型能力的提升，过去为旧模型设计的冗长规则和强制流程可能已转化为拖累性能的负优化。编程智能体的最佳实践正在快速演进，长期在项目中积累的 Skills、AGENTS.md 配置和任务提示词值得重新审视。Skill 文件数量过多会导致上下文压缩，冗长描述会相互干扰；强制全仓读取的指令会无谓消耗上下文；过度具体的操作配方可能束缚模型判断力。GPT-6 Astra 能够自主判断需要阅读的文档、主动运行测试，因此沿用旧指令可能产生冗余操作。

## 能力机制

Skill 文件以 Markdown 格式保存，本质上是结构化提示词，用于指导特定工作流或说明插件用法。每个 Skill 的名称和描述会全部加载到模型上下文，Codex 为适应上下文限制会主动缩短描述。$skill-creator Skill 的指南已针对实际失效模式进行多轮更新。AGENTS.md 在模型处理仓库任务时始终生效，因此其中的每条指令都需要根据任务实际需求评估必要性。GPT-6 Astra 在任务推进程度判断上更为谨慎，可能在完成初版实现后主动暂停等待审查，这种行为可通过预先定义完成条件来调整。

## 快速开始

审计现有 Skills：将冗长描述精简为简短语句，明确触发场景，移除过度具体的操作步骤。将包含多工作流的 Skill 拆分为根路由文档和辅助子文档，根文档仅提供足以判断查找方向的指导。清理 AGENTS.md 中的强制全仓读取指令，改为按需引用特定文档。对于测试指令，检查是否仍需手动要求模型执行。明确任务完成条件，若希望模型持续探索需指定探索目标和停止条件。完成后可让 GPT-6 Astra 根据上述要点执行一次项目审计。

## 适用边界

Skill 描述冗长会导致模型难以准确判断调用时机，过多 Skill 会触发上下文截断使描述不完整，矛盾的描述可能引导模型加载无益指令。强制每次编辑前读取全部文档的指令会快速耗尽上下文并拖慢速度，过度约束的指令可能使模型在用户本希望其继续的环节主动停止。新模型判断能力提升后，旧有的强硬限制措辞需要根据实际需求重新校准，模型会严格遵守边界设置。

## 核验清单

Skill 文件方面：描述是否简短且明确触发场景，是否移除了过于宽泛的适用条件，是否按渐进式披露原则设计了路由结构，是否清理了过度具体的操作步骤，是否考虑了不同模型的适用性。AGENTS.md 方面：是否仍有强制全仓读取的指令，是否仍需手动要求运行测试，是否需要补充具体工作流的授权，是否需要调整操作边界描述，是否需要明确任务完成条件。持久化方面：任务是否有清晰定义的完成标准，是否需要说明探索范围和停止条件。

## 来源与核验

- [原始文章](https://juejin.cn/post/7681858280943403059)
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