---
title: "AI Agent 说「已完成」，凭什么信——ChipCode 的证据链与产物门禁设计"
date: 2026-11-06T14:46:58+08:00
draft: false
entry_kind: "auto"
tags: ["掘金", "工程实践", "来源转写"]
categories: ["AI 工程"]
source: "juejin"
content_mode: "evidence_backed_rewrite"
publication_tier: "B"
source_capture_mode: "full_article"
source_snapshot_sha256: "sha256:806f479bb610dd6c752f7f665c2b31875c826da28202b78c844c419a50657c87"
source_payload_sha256: "sha256:08ee02e6eb485ca89c1856f590540cca053ae34f1791e2838d089062be2fc817"
source_published_at: 2026-11-05T18:42:14Z
timestamp_confidence: feed
extractor_version: "source-contract-v2"
discovery_method: "article_html"
source_completeness: "complete"
parent_snapshot_sha256: "sha256:f4d4ae25ba3b6ff01dfdfa6cd0994123fb76b61a13fbdd89331d50ab8269e6d7"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 42
description: "核心结论 来源指出，AI Agent 的“已完成”不能只依据对话自述。问题不只在代码是否写对，更在于“已经验证”的判定依据：如果状态由模型宣布，工具调用成功也可能只代表命令执行结束，并不代表验收条件满足。"
external_url: https://juejin.cn/post/7704640997515067418
observation_id: obs_e88db68e0a8e1f38ba00d66c863571c9da80e1ba43acac625e1b5d23f806a10d
revision_id: rev_99b3d6632878f045b67b535c785a2b282031ea4601defa8a8ed4a946318fa149
event_id: evt_369fdbf9ca50dafba7be3277fbfbe5b861ad223ea5c568d7b03a09a56464813d
lineage_relation: original
parent_observation_id: null
first_seen_at: 2026-11-06T06:45:05.521685Z
last_seen_at: 2026-11-06T06:46:58Z
---

## 转写说明

> 本文基于已校验的公开原文进行结构化转写与事实梳理，非原文转载。
> 转写保留可核验的技术事实，并将工程建议与来源观点明确分开。

- **原作者**: 蓝星科学
- **原始来源**: [https://juejin.cn/post/7704640997515067418](https://juejin.cn/post/7704640997515067418)
- **原文发布时间**: Thu, 05 Nov 2026 18:42:14 GMT

## 核心结论

来源指出，AI Agent 的“已完成”不能只依据对话自述。问题不只在代码是否写对，更在于“已经验证”的判定依据：如果状态由模型宣布，工具调用成功也可能只代表命令执行结束，并不代表验收条件满足。

ChipCode 将可信验证分为三层：语言层是 Agent 的文字结论；工具层是工具返回的成功状态；进程层是编译器退出码、标准输出、串口日志、Flash 占用等外部程序产生的事实。工具返回成功仍可能由工具实现方自行定义，因此来源强调，能够落到进程层的结论，不应停留在语言层。

其核心设计包括三点：用 append-only 的 `evidence.jsonl` 保存证据；由项目磁盘文件计算阶段状态；用产物门禁阻止状态被口头推进。工程上的可迁移原则是：状态外置、验证下沉、失败留痕。

## 能力机制

撤销不是删除原记录，而是追加带有 `invalidates` 的新记录。撤销后，原证据覆盖的条件会重新回到未证明状态。账本使用 JSONL，是因为它能逐行审查、便于并发追加、可由标准 JSON 解析，且单行写入失败不会像 JSON 数组那样破坏整份文件。

阶段状态不是 Agent 或数据库直接宣布的字段，而是根据固定产物计算的结果。来源列出的产物包括创意阶段的 `spec.json`、`spec.md`，造型阶段的 `design/shape.json`，硬件阶段的 `bom.json`、`constraints.json`，软件阶段的 `firmware/`，以及联调阶段的 `evidence.jsonl`。例如，模型或网格文件不存在、器件缺少来源链接、有效证据存在 `fail`，都会被判定为阻塞。

来源还区分“出错”和“阻塞”：出错表示已有内容损坏，需要修复；阻塞表示交付物尚未落地，需要补齐。门禁应明确缺失内容，而不是只显示笼统警告。

## 快速开始

来源提供的账本校验命令为：

```bash
python check_evidence.py evidence.jsonl c1 c2 c3
```

脚本先收集 `invalidates` 指定的失效证据，再遍历剩余记录；只有未被撤销且 `result` 为 `pass` 的证据，才会把其 `covers` 计入已覆盖条件。退出码含义为：`0` 表示全部覆盖，`1` 表示存在未证明条件或账本损坏，`2` 表示参数错误。

按来源中的实现，脚本会检查以下文件要求：账本中的每条记录都必须是合法 JSON；`pass` 证据必须完整覆盖传入的条件集合；被撤销的证据不得继续贡献覆盖。`fail` 和 `inconclusive` 都不会被当作已证明。

工程建议是，把这类检查接入 CI 或 pre-commit，并保留退出码语义。来源同时指出，人工确认应集中在验收条件、关键选型与结构、无法由进程产生的物理结果等位置；其余环节由 Agent 推进，失败则必须明确显示原因。

## 适用边界

这套方案有明确代价。每个阶段都要额外维护 spec、BOM、evidence 等文件；门禁会阻断尚未落地的阶段，探索阶段尤其容易产生负担；JSONL 没有索引、事务和并发控制，来源判断几千条以内较合适，上万条应改用正式存储。

它适合有明确交付物和验收条件的任务，尤其接近正式交付的硬件、固件或结构开发。来源明确不把产品工厂用于 PCB 设计、打样和采购。对于代码性能排查、开放式探索等难以定义验收条件的任务，不应强行套用形式化门禁。

“配置保存在本地”也不能推导为“推理数据一定不出本机”。来源只说明证据账本和阶段产物写入项目文件，并按这些文件计算状态，没有对完整的数据流或网络边界作出保证。

## 核验清单

1. 验收条件是否写入 `spec.json`，并逐条映射到证据的 `covers`。
2. 证据结果是否区分 `pass`、`fail`、`inconclusive`，而不是只记录成功或失败。
3. 是否明确记录未覆盖内容，避免把“做过验证”写成“验证了全部条件”。
4. 撤销是否通过追加 `invalidates` 记录完成，原证据是否仍可追溯。
5. 校验时是否先收集失效集合，再计算有效覆盖，避免被撤销的证据继续贡献结果。
6. 阶段状态是否由磁盘产物计算，而不是由 Agent 的对话结论或单一字段决定。
7. 模型、网格、视图、BOM 来源链接等产物是否存在，阻塞原因是否具体可查。
8. 失败、拒绝、编译错误和人工确认缺失是否保持可区分，并使用不同退出码表达。
9. 独立验证和 Agent 的结论是否指向同一组外部事实，而不是自然语言报告。
10. 任务是否确实具备明确交付物；若仍处于探索阶段，应先判断门禁是否值得引入。

## 来源与核验

- [原始文章](https://juejin.cn/post/7704640997515067418)
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