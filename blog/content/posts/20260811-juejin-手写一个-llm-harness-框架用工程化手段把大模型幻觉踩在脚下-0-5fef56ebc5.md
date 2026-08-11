---
title: "手写一个 LLM Harness 框架：用工程化手段把大模型幻觉踩在脚下"
date: 2026-08-11T19:08:50+08:00
draft: false
entry_kind: "auto"
tags: ["掘金", "工程实践", "来源转写"]
categories: ["AI 工程"]
source: "juejin"
content_mode: "evidence_backed_rewrite"
publication_tier: "B"
source_capture_mode: "full_article"
source_snapshot_sha256: "sha256:9955d847eed70247f9392072173d578e87aea88d5a1ff9427846a915f61ee53e"
source_payload_sha256: "sha256:b6c98a81a062f2386b0c9fbdb134c83bf5bcfec15c707e442a7fd525cd3cc1e1"
source_published_at: 2026-08-11T10:44:02Z
timestamp_confidence: feed
extractor_version: "source-contract-v2"
discovery_method: "article_html"
source_completeness: "complete"
parent_snapshot_sha256: "sha256:9d7cae1699cc8abbf27cf8c8ddc3afeaed3fcb86b916413062b5ff691fd32310"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 36
description: "核心结论 Harness 是一种将大模型应用分解为生成、评测、择优三个阶段的流水线编排框架。生成阶段通过 与 组合并行发出 N 个请求，评测阶段由 LLM 作为 Judge 输出结构化分数，最后根据分数择优输出。该框架的核心价值在于将大模型的随机性从缺陷转化为优势，用工程手段覆盖质量波动。"
external_url: https://juejin.cn/post/7672695343738454052
observation_id: obs_5fef56ebc570c691c07bbfcba11c7c2045cb3f9c30adb5f5dff42aee7336cf4f
revision_id: rev_16f1bf954ca6de39489ee35e412f232bf7c4dd90e572419e86798406b4535647
event_id: evt_150c4f6889f90158607994b1ae9f49769542280a9f447233a1633db5a73c417b
lineage_relation: original
parent_observation_id: null
first_seen_at: 2026-08-11T13:42:18.676154Z
last_seen_at: 2026-08-11T11:08:50Z
---

## 转写说明

> 本文基于已校验的公开原文进行结构化转写与事实梳理，非原文转载。
> 转写保留可核验的技术事实，并将工程建议与来源观点明确分开。

- **原作者**: dzhd
- **原始来源**: [https://juejin.cn/post/7672695343738454052](https://juejin.cn/post/7672695343738454052)
- **原文发布时间**: Tue, 11 Aug 2026 10:44:02 GMT

## 核心结论

Harness 是一种将大模型应用分解为生成、评测、择优三个阶段的流水线编排框架。生成阶段通过 `Array.from` 与 `Promise.all` 组合并行发出 N 个请求，评测阶段由 LLM 作为 Judge 输出结构化分数，最后根据分数择优输出。该框架的核心价值在于将大模型的随机性从缺陷转化为优势，用工程手段覆盖质量波动。

框架的核心函数共五个：`askLLM` 封装所有 LLM 通信；`generateCandidates` 实现并行生成；`judge` 负责单个候选的评分；`evaluateAll` 串行评测所有候选；`pickBest` 从评测结果中选取最高分。整个实现不足 80 行代码，体现了单一职责原则在 AI 工程中的应用。

## 能力机制

框架的三阶段流水线各司其职。生成阶段调用 `Promise.all` 实现真正的高并发，请求之间无串行等待。评测阶段使用 `for...of` 串行循环处理候选，原因是评测阶段存在隐式速率限制，同一 API Key 并发请求过多可能触发限流导致整批评分失败。择优阶段采用 `sort` 按分数降序排序后取第一个元素。

`Array.from` 在此承担双重职责：创建数组结构的同时，在构造期间同步执行回调函数生成 Promise，而非先创建稀疏数组再遍历填充。这种写法在 JavaScript 单线程事件循环下实现了最高并发度。

`askLLM` 函数将客户端创建和 API 细节封装为唯一 I/O 边界，API Key、模型名、Base URL 均从环境变量读取，与代码分离。换环境只需修改配置文件。

## 快速开始

环境变量配置通过 `dotenv` 模块加载 `.env` 文件完成。必需的环境变量包括 `OPENAI_API_KEY`、`OPENAI_API_BASE_URL`、`MODEL_NAME`。配置与代码分离实现一次注入全局复用。

核心调用入口为 `harness` 函数，传入提示词字符串后自动完成生成、评测、择优三阶段流水线，返回得分最高的候选答案。

```javascript
import { config } from 'dotenv';
config();
const bestCode = await harness("请使用 JavaScript 实现一个数组去重函数");
```

## 适用边界

该框架适用于需要对抗大模型输出不确定性的场景，通过并行生成覆盖随机性，用评分筛选质量。它无法保证评测准确度，Judge 的 prompt 设计本身也是需要调参的超参数，角色锚定会显著影响评分气质。

并发度 N 的选择存在权衡：太少覆盖不到随机性，太多浪费 token 和时间。评测阶段的串行处理虽然降低了触发限流的风险，但整体吞吐量受限于 API 速率限制。框架适用于 OpenAI 兼容协议的服务端，接入千问、DeepSeek 等模型需确保其实现 `/v1/chat/completions` 接口。

三个阶段的解耦使得各环节可独立替换：生成质量可通过调整 N 值改善，评测模型可替换为更强的推理模型，择优策略可从最高分改为多数投票等形式。

## 核验清单

- 每个函数职责单一，符合单一职责原则
- 环境变量实现配置与代码分离，换环境不改代码
- 生成阶段并行、评测阶段串行，符合工程判断
- `Array.from` 构造期间同步执行回调实现真正并发
- 评测结果解析包含容错兜底，不假设输出必为数字
- 框架输出纯文本，不含 HTML、图片或外部链接
- 快速开始仅列出环境变量名称，未写入任何示例密钥值

## 来源与核验

- [原始文章](https://juejin.cn/post/7672695343738454052)
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