---
title: "从 LLM 到 Agent：一篇文章搞懂 AI 圈热词！"
date: 2026-08-10T03:03:57+08:00
draft: false
entry_kind: "auto"
tags: ["掘金", "工程实践", "来源转写"]
categories: ["AI 工程"]
source: "juejin"
content_mode: "evidence_backed_rewrite"
publication_tier: "B"
source_capture_mode: "full_article"
source_snapshot_sha256: "sha256:bd3e04b37868c36c4c1916d642a91c3dd7a889dc2386d30b59fad8f9f81007b4"
source_payload_sha256: "sha256:9650998ecc795f3f857a6caf97857236da8a1f617e098cab450657bf94f0a0d7"
source_published_at: 2026-08-09T14:00:36Z
timestamp_confidence: feed
extractor_version: "source-contract-v2"
discovery_method: "article_html"
source_completeness: "complete"
parent_snapshot_sha256: "sha256:249593c0563493833e75bb39adfec496aaf6b529308c3ddf989749017a210b18"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 28
description: "核心结论 大语言模型经过海量文本训练，具备代码生成、逻辑推理、文本理解和任务规划等基础能力。模型以 Token 为计量单位处理信息，上下文窗口限制了一次交互可处理的信息总量。"
external_url: https://juejin.cn/post/7671591776068599854
observation_id: obs_08daeba8c0375f3cf51e642ea449e04aff76edb3e02b0fa6f72ddafb9801d45c
revision_id: rev_8f0e668b274bb7f73a5e098a39c718abb4eec2f38bf14a3ae311199e15e33879
event_id: evt_c2cd23b1ac0c42307ebe04aa8ecf501fff34b725a17978fff4694ebe733d69bb
lineage_relation: original
parent_observation_id: null
first_seen_at: 2026-08-09T19:00:35.365014Z
last_seen_at: 2026-08-09T19:03:57Z
---

## 转写说明

> 本文基于已校验的公开原文进行结构化转写与事实梳理，非原文转载。
> 转写保留可核验的技术事实，并将工程建议与来源观点明确分开。

- **原作者**: JacksonChen
- **原始来源**: [https://juejin.cn/post/7671591776068599854](https://juejin.cn/post/7671591776068599854)
- **原文发布时间**: Sun, 09 Aug 2026 14:00:36 GMT

## 核心结论

大语言模型经过海量文本训练，具备代码生成、逻辑推理、文本理解和任务规划等基础能力。模型以 Token 为计量单位处理信息，上下文窗口限制了一次交互可处理的信息总量。

在基础模型之上，RAG 通过外挂知识库解决私有数据缺失问题，Fine-tuning 改变模型的行事方式而非知识边界，Tool Calling 让模型能够调用外部工具执行实际操作。Memory 和 Skill 分别提供外部信息管理和任务流程复用能力，MCP 协议则尝试建立 AI 与工具之间的统一连接标准。

从聊天机器人到 Agent 的演进，关键在于任务执行的控制权归属：提前写死的流程属于自动化，由模型动态决定下一步则更接近 Agent。ReAct 循环是 Agent 的经典工作模式，通过思考、行动、观察的反复迭代完成任务。

当前工程实践中，Context Engineering 关注为模型构建完整的信息环境，Loop Engineering 关注控制 Agent 的执行循环避免无限消耗。模型本身的能力有天花板，真正决定系统表现的，是围绕模型构建的整个运行框架。

## 能力机制

**模型层**

LLM 基于海量文本训练，核心任务是预测下一个最可能出现的 token。模型并非直接理解文字，输入前需将文本切分为 Token。Token 可以是单词、子词或字符，中文切分通常更细。上下文窗口决定模型一次交互能处理的信息总量，包括当前输入、历史对话、系统提示词、工具信息和模型输出。超过窗口范围的内容模型无法感知，这与人类实习生桌上的 A4 纸面积有限类似。

**检索与知识增强**

RAG 的流程包括：将资料切分并转换为向量，存入向量数据库，用户提问时搜索相关内容，把检索结果提供给模型参考。Embedding 将文字转换为数字向量，使系统能理解语义相似性。实际工程中通常采用混合检索，结合向量相似度匹配和关键词精确匹配，以提高准确率。

**模型行为调整**

Fine-tuning 重新训练模型以改变其工作方式，适用于需要统一输出风格、固定格式或专业领域优化的场景。与 RAG 不同，RAG 改变模型知道什么，Fine-tuning 改变模型怎么做事。

**工具与外部交互**

Tool Calling 允许模型在生成文本的同时输出结构化的工具调用请求，由外部程序负责实际执行。模型负责判断何时调用、执行由代码完成。MCP 协议尝试为不同 AI 应用与工具之间建立统一的连接标准，降低逐一对接的重复开发成本。

**Agent 架构要素**

**上下文与循环工程**

Context Engineering 关注的是模型完成任务所需整体信息环境的设计，包含 Prompt、RAG 数据、Memory、Tool、Skill、历史上下文等多个要素。Harness Engineering 则是围绕模型构建的完整运行框架，包含系统提示词、权限控制、沙箱环境、错误处理等。Loop Engineering 关注控制循环次数、避免 Token 无限消耗、确定人工介入时机等，防止 Agent 陷入死循环。

## 快速开始

构建基于大模型的 Agent 系统，典型的启动流程涉及以下环节的确认与配置：API 端点用于模型通信，API 密钥以环境变量方式注入，请求中设置上下文窗口大小以匹配任务复杂度，模型选择影响推理能力边界。

面向开发者的提示词工程实践可从角色设定、任务描述、上下文补充、输出约束四个维度入手。角色设定明确模型应采用的应答身份，任务描述清晰定义目标，上下文补充提供必要背景，输出约束限定格式与风格。

构建完整信息环境时需确认：RAG 数据源是否接入，工具定义是否完整，记忆持久化方案是否启用，Skill 库是否包含对应任务的处理规范。这些要素的可用性直接影响 Agent 的任务完成能力。

## 适用边界

**适合使用 Agent 的场景**

涉及多步骤分解的复杂任务，需要模型自主判断下一步操作；任务流程存在变数，无法全部提前穷举；需要整合多种外部数据源和工具；任务执行过程中需要基于中间结果动态调整策略。代码生成、自动化测试、文档处理、多系统协调等任务类型属于典型适用场景。

**不适合或效果有限的场景**

简单的一次性问答，用户明确只需要单一答案；实时性要求极高且需要毫秒级响应的场景；完全没有结构化数据的纯手工操作；任务边界极其模糊且无法定义成功标准的情况。

**需要注意的限制**

模型依赖训练数据，知识存在时效性；无法真正主动操作外部世界，需要通过工具调用间接实现；上下文窗口有限制，长任务需要分段或压缩处理；每次 API 调用按 Token 计费，复杂 Agent 循环可能产生较高使用成本。

## 核验清单

构建基于来源文章描述的 Agent 系统时，应逐项确认以下要素的覆盖情况：模型基础能力是否满足任务需求，包括代码生成、逻辑推理和文本理解等方面；上下文窗口是否足够容纳单次任务的完整信息；RAG 知识库是否覆盖任务所需的专业领域知识；Embedding 模型是否与知识库语言类型匹配；Fine-tuning 是否有必要，相比 RAG 的方案选择是否合理；工具调用接口是否完整定义，调用权限是否受限；Memory 持久化方案是否满足长期任务的信息复用需求；Skill 库是否包含目标任务的预定义处理规范；MCP 协议兼容性是否满足多工具对接需求；循环退出条件是否明确设置，防止无限执行；错误处理与重试机制是否完整配置；人工介入的触发条件是否清晰定义；Token 消耗监控是否建立，避免异常情况下的成本失控。

## 来源与核验

- [原始文章](https://juejin.cn/post/7671591776068599854)
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