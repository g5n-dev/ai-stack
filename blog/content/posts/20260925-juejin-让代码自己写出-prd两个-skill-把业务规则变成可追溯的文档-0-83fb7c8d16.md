---
title: "让代码自己写出 PRD：两个 Skill 把业务规则变成可追溯的文档"
date: 2026-09-25T03:13:20+08:00
draft: false
entry_kind: "auto"
tags: ["掘金", "工程实践", "来源转写"]
categories: ["AI 工程"]
source: "juejin"
content_mode: "evidence_backed_rewrite"
publication_tier: "B"
source_capture_mode: "full_article"
source_snapshot_sha256: "sha256:90577df48282d44d2db2370a5150bfe4c49fe2ff6699c7e327a71c264fa6659c"
source_payload_sha256: "sha256:e32ca55056fa272ae10f750f7d9a5b4384432d2381d38eebe935b8e033ca4c47"
source_published_at: 2026-09-24T14:16:14Z
timestamp_confidence: feed
extractor_version: "source-contract-v2"
discovery_method: "article_html"
source_completeness: "complete"
parent_snapshot_sha256: "sha256:1260653062da90b169b341532bf4c52602adf2eba3a9390b97c43c3dba0d5c2b"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 34
description: "核心结论 codebase-graph-prd-rules 是一个业务规则提取工具，通过 AI Agent Skill 从源码中挖掘散落的业务规则，每条规则附带源码位置供追溯。该项目在 v1.0.0 版本中提供两个互补 Skill：一个覆盖全项目业务规则梳理，一个聚焦单个模块的深度分析。"
external_url: https://juejin.cn/post/7689029581950074906
observation_id: obs_83fb7c8d16ece1c56c2dd795cb13028beefa979eb572ef47137765db85ead7f0
revision_id: rev_3d57f0c61d5d5e236fe27bbb40abece3cd772f26273622da2960ffef5d745f5c
event_id: evt_f1dd2a0133660042337cabd39cd601d66a07efd12de243cd8429965dc8158a54
lineage_relation: original
parent_observation_id: null
first_seen_at: 2026-09-24T19:09:23.748902Z
last_seen_at: 2026-09-24T19:13:20Z
---

## 转写说明

> 本文基于已校验的公开原文进行结构化转写与事实梳理，非原文转载。
> 转写保留可核验的技术事实，并将工程建议与来源观点明确分开。

- **原作者**: Hey\_AI\_Coder
- **原始来源**: [https://juejin.cn/post/7689029581950074906](https://juejin.cn/post/7689029581950074906)
- **原文发布时间**: Thu, 24 Sep 2026 14:16:14 GMT

## 核心结论

codebase-graph-prd-rules 是一个业务规则提取工具，通过 AI Agent Skill 从源码中挖掘散落的业务规则，每条规则附带源码位置供追溯。该项目在 v1.0.0 版本中提供两个互补 Skill：一个覆盖全项目业务规则梳理，一个聚焦单个模块的深度分析。核心方法论为"图谱导航、源码确认"：先用代码图谱定位候选调用链，再回到源码、SQL、XML 和配置逐条确认。项目强调只分析不执行，配套 Python 发布包和验证器，确保输出可追溯且可验证。

## 能力机制

项目包含两个共享方法论的 Skill：codebase-graph-business-rules 用于全项目分析，输入项目根目录和源码范围，输出包括模块地图、实体状态、数据配置、端到端流程、各模块规则表、测试范围和追溯索引；codebase-graph-module-rules 用于单模块分析，输入功能描述或模块名，输出模块边界、关系、规则排序限制和测试矩阵。

业务规则采用三层模型严格拆分：资格过滤层判断候选是否合格，候选排序层确定处理顺序，运行时控制层处理限制、去重、并发、发送和失败回滚。每条信息标注证据等级，分为源码/SQL/配置已审、图谱 EXTRACTED、图谱 INFERRED、注释/日志/字段名、运行时结果五个层级，明确区分已知事实和待确认项。

两个 Skill 各携带 3 个评估用例，覆盖成功路径、输入不完整和范围边界场景。输入不完整时必须报告缺口，拒绝越界请求。

## 快速开始

项目以 Python sdist + wheel 形式发布，安装后可使用 verify-skill-package 控制台入口验证包结构。结构校验和敏感信息扫描通过 make check 命令执行。包验证器检查必需文件存在、SKILL.md 的 front-matter name 与目录匹配、agents/openai.yaml 的 metadata.key 匹配以及所有 .md/.yaml 文件中无凭证内容。

语义图谱提取需要配置 LLM 凭证，凭证只存在于进程环境中，不写入源码、文档、Skill 文件或输出。没有凭证时项目如实报告这一限制。

## 适用边界

该项目适合三类场景：产品经理和业务分析师梳理全项目业务规则，输出用表格和 Mermaid 图讲述业务含义而非堆砌类名；QA 工程师获取模块边界和测试矩阵，每条关键规则映射到可执行测试断言；技术负责人进行审计和变更追溯，每条规则带源码位置来源。

局限性方面，该项目 Star 数量较少，社区规模有限。Roadmap 中的 CI 工作流、Skill 注册表发布、更多真实项目示例尚未完成。静态包验证只证明结构和安全，不代表某个项目真的被分析过。包验证通过不等于模型行为验证通过。

## 核验清单

验证 Skill 包时需确认：SKILL.md 的 front-matter name 与目录名一致，agents/openai.yaml 的 metadata.key 与目录名匹配，所有 .md/.yaml 文件中不包含凭证类内容。评估用例应覆盖成功路径、输入不完整和越界请求三种场景，其中输入不完整时 Skill 必须报告缺口而非猜测，越界请求必须被拒绝。

输出文档核验时注意：规则是否包含字段、方向、空值处理、并列行为、后过滤、终止条件等完整信息；每条信息是否标注了对应的证据等级；推断出的调用关系是否经过源码确认。

## 来源与核验

- [原始文章](https://juejin.cn/post/7689029581950074906)
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