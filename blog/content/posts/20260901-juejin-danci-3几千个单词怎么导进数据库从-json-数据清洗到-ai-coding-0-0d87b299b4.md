---
title: "danci 3：几千个单词怎么导进数据库？从 JSON 数据清洗到 AI Coding"
date: 2026-09-01T07:53:41+08:00
draft: false
entry_kind: "auto"
tags: ["掘金", "工程实践", "来源转写"]
categories: ["AI 工程"]
source: "juejin"
content_mode: "evidence_backed_rewrite"
publication_tier: "B"
source_capture_mode: "full_article"
source_snapshot_sha256: "sha256:4f2f8c4a50a9305c1d5ad686322e704e27a8693f3bb3fecf30929b8caae26baf"
source_payload_sha256: "sha256:c578d35f4c2e1e40f1b674698eb771f8f37868e014b34f5ad11fc2178353f56b"
source_published_at: 2026-08-31T15:45:46Z
timestamp_confidence: feed
extractor_version: "source-contract-v2"
discovery_method: "article_html"
source_completeness: "complete"
parent_snapshot_sha256: "sha256:6fa2473d06705f3c399a855a43407f8aeb9ce3a2b7d7f83d6ca60383321f4e3f"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 43
description: "核心结论 大量单词数据导入数据库时，直接使用外部 JSON 而不经过处理会产生字段不匹配、数据重复、格式不一致等问题。数据清洗的核心在于把外部数据整理成符合当前系统业务约束的格式，而不是简单的格式转换。"
external_url: https://juejin.cn/post/7680066396043280430
observation_id: obs_0d87b299b4c1584939131eb06d1b688dd52935ccb5d5d074ccb3f3cb7c8071b7
revision_id: rev_0bf1b5b4308a1bbfed6d63ad8edac983239e9949808110825d93a05069a23aba
event_id: evt_c3ebab06246eab66db3c833553c6196f3adf9c1f90fda56992bea8b12c43b99e
lineage_relation: original
parent_observation_id: null
first_seen_at: 2026-08-31T23:51:00.651893Z
last_seen_at: 2026-08-31T23:53:41Z
---

## 转写说明

> 本文基于已校验的公开原文进行结构化转写与事实梳理，非原文转载。
> 转写保留可核验的技术事实，并将工程建议与来源观点明确分开。

- **原作者**: 东风破\_
- **原始来源**: [https://juejin.cn/post/7680066396043280430](https://juejin.cn/post/7680066396043280430)
- **原文发布时间**: Mon, 31 Aug 2026 15:45:46 GMT

## 核心结论

大量单词数据导入数据库时，直接使用外部 JSON 而不经过处理会产生字段不匹配、数据重复、格式不一致等问题。数据清洗的核心在于把外部数据整理成符合当前系统业务约束的格式，而不是简单的格式转换。AI Coding 的关键思路是让 AI 生成处理工具而非直接处理数据，通过提供数据样例、目标格式和转换规则，AI 能够编写可重复执行的脚本。上下文管理的原则是给足关键上下文但不给无关上下文，避免模型在大量原始数据中消耗 token。验证和 Git 管理仍然是保障结果正确性的必要环节。

## 能力机制

AI 在数据清洗场景中能够根据少量样例生成完整的转换脚本。这种能力的实现依赖于三个要素的提供：原始数据格式示例、目标数据结构定义、转换规则说明。来源中演示了一个典型场景，从原始 JSON 的 `trans` 数组取第一个元素作为 `meaning`，过滤 `word` 为空的记录，去除重复单词，最终输出 CSV 格式。

项目长期信息可以通过 `AGENTS.md` 等文件集中管理，包含技术栈、代码规范、数据库结构等内容，使每次 Prompt 只需要描述当前具体任务，而非重复介绍项目背景。

## 快速开始

数据清洗脚本的基本工作流程在来源中有所体现。首先从外部获取 JSON 数据，然后分析原始数据结构，接着确定目标表需要的字段，定义清洗规则，由 AI 编写转换脚本。

来源中提到的目录结构示例：

scripts/convert-words.ts
scripts/validate-words.ts
scripts/import-words.ts

脚本需要完成读取 JSON、遍历记录、字段转换、去重、过滤异常、生成 CSV 等步骤。生成 CSV 后还应进行校验和抽样审核，最终导入数据库。

Git 配合 Conventional Commits 的使用流程：查看 `git diff` 进行 Review，运行测试，确认功能后提交。来源列举的类型包括 feat、fix、docs、refactor、style、test、chore。

## 适用边界

数据清洗脚本适用于 CSV、Excel、JSON、第三方 API、旧数据库、日志、爬虫数据等各类外部数据的导入场景。当数据量大且规则明确时，使用脚本批量处理优于逐条处理。

AI 生成脚本的方式适用于规则明确、数据量大、重复度高的任务。对于一次性的小数据处理，偶尔直接让 AI 处理也可以接受。

上下文范围的把控上，需要避免两个极端：一是给 AI 无脑读取所有文件，应该控制上下文范围而不是禁止上下文；二是完全不给关键上下文，导致模型只能猜测。真正应该避免的是与任务无关的文件、大量原始数据和无意义的历史材料。

验证环节是必须的，AI 生成脚本不等于结果自动正确。Git 在 AI Coding 时代反而更加重要，用于追踪改动、确认预期、发现错误和恢复。

## 核验清单

数据清洗结果需要进行的校验项包括：检查总行数是否符合预期、检查是否存在空字段、检查是否存在重复单词、进行随机抽样验证、核对典型单词的转换结果。

AI 生成代码后的验收流程：执行 `git diff` 查看改动内容、逐项 Review 修改是否符合预期、运行测试确认功能正常、确认无误后使用 Conventional Commits 格式提交。

上下文提供的检查点：项目技术栈是否明确、数据库 schema 是否已定义、字段类型和约束是否清晰、业务规则是否完整说明、需要操作的功能范围是否界定清楚。

## 来源与核验

- [原始文章](https://juejin.cn/post/7680066396043280430)
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