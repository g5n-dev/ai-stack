---
title: "从 Token 到 RAG：我这一周搭起的大模型基础认知地图"
date: 2026-07-18T20:07:56+08:00
draft: false
entry_kind: "auto"
tags: ["掘金", "工程实践", "来源转写"]
categories: ["AI 工程"]
source: "juejin"
content_mode: "evidence_backed_rewrite"
publication_tier: "B"
source_capture_mode: "full_article"
source_snapshot_sha256: "sha256:95f0bbc852f95876d8a1a5828b8d4bab25776434f4d59f2824b395600158bd8e"
extractor_version: "source-contract-v2"
discovery_method: "article_html"
source_completeness: "complete"
parent_snapshot_sha256: "sha256:4cd566697a02a566394354f1054c07fe255c63aaef641bcb7573610468e3e40b"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 30
description: "核心结论 LLM 生成回答的完整链路可概括为：输入文本经 Tokenizer 切分为 Token ID，再通过 Embedding 表映射为向量；Transformer 通过 Self-Attention 机制处理上下文信息；生成过程中 KV Cache 复用历史 K/V 以避免重复计算；当模型需要参数之外的知识时…"
external_url: https://juejin.cn/post/7663518564783931401
---

## 转写说明

> 本文基于已校验的公开原文进行结构化转写与事实梳理，非原文转载。
> 转写保留可核验的技术事实，并将工程建议与来源观点明确分开。

- **原作者**: Lei\_official
- **原始来源**: [https://juejin.cn/post/7663518564783931401](https://juejin.cn/post/7663518564783931401)
- **原文发布时间**: Sat, 18 Jul 2026 11:44:25 GMT

## 核心结论

LLM 生成回答的完整链路可概括为：输入文本经 Tokenizer 切分为 Token ID，再通过 Embedding 表映射为向量；Transformer 通过 Self-Attention 机制处理上下文信息；生成过程中 KV Cache 复用历史 K/V 以避免重复计算；当模型需要参数之外的知识时，RAG 从外部索引检索相关资料并补充到上下文中。

## 能力机制

Token 是模型的编码单元，Tokenizer 负责将自然语言切分为 Token 并转换为整数 ID 序列。不同模型使用不同词汇表，常见规模从约 5 万到 20 万不等。已训练模型必须配合对应词汇表的 Tokenizer 使用，因为 Embedding 表和输出层均按特定 ID 映射训练。

Embedding 将 Token ID 映射为多维向量，本质是一张可训练的查找表。数学表示为 E∈R^{V×d}，其中 V 为词表大小，d 为向量维度。初始向量是 Token ID 对应的静态查表结果，未结合上下文信息。

Self-Attention 中，Query 表示当前位置的关注需求，Key 作为可匹配标签，Value 包含待聚合的信息特征。计算过程为：用当前 Q 与所有可见位置的 K 计算匹配度，经 Softmax 得到注意力权重，再用这些权重对对应位置的 V 加权求和，生成新的上下文表示。

Transformer 将多层 Decoder Block 堆叠组织。每个 Block 包含 Masked Multi-Head Self-Attention、MLP Feed Forward Network 以及残差连接与归一化。最终输出经过 LM Head 映射为词表每个候选 Token 的 logits，经 Softmax 转为概率分布后由解码策略选择下一个 Token。

推理阶段分为 Prefill 和 Decode 两个环节。Prefill 一次处理完整 prompt 并建立各层历史 K/V；Decode 每次只处理一个新 Token，复用历史 K/V 追加新计算的 K/V，预测下一个 Token。生成 N 个 Token 通常对应 1 次 Prefill 加 N-1 次 Decode。

RAG 通过检索外部知识库补充模型上下文。离线流程包括文档切片、向量化、建立索引；在线流程包括查询编码、向量检索、结果重排与上下文拼装。检索方式不限于向量相似度，也可结合关键词检索和 Agent 工具探索。

## 快速开始

理解 LLM 生成链路可从以下步骤入手：

使用在线 Tokenizer 可视化工具观察文本切分过程。需要注意 Token 与单词或汉字并非一一对应，同一文本可能因 Tokenizer 不同而产生不同切分结果。

验证 Embedding 的查表本质：同一 Token ID 每次查到相同行，初始向量是静态的上下文无关表示。向量空间中 Token 的距离只反映训练语料中的统计相似性，不能直接等同于语义关系。

理解 Attention 的 Q/K/V 投影：每个 Transformer 层和 Attention Head 各自拥有独立的 WQ/WK/WV 参数，不是全模型共享。解码时因果遮罩确保当前位置只能关注左侧已生成的 Token。

区分 Prefill 与 Decode 的职责：Prefill 建立完整的 KV Cache，Decode 阶段才体现 KV Cache 的加速价值——每次只需处理单个新 Token 而非完整前缀。

RAG 工程实现中，离线索引构建与在线检索相互独立。文档切片策略、向量维度与检索算法属于离线设计；在线阶段可混合使用向量检索与关键词检索，结果通常需要重排过滤。

## 适用边界

Token 与 Tokenizer 的匹配具有强制性。已训练模型的 Embedding 和输出层与特定词汇表绑定，推理时必须使用对应的 Tokenizer，否则 Token ID 映射会错位。

Embedding 表中同一 Token ID 对应的向量是固定的。Transformer 层输出的 hidden state 才是结合上下文的动态表示。这一区分在分析同形异义词（如不同语境的"Apple"）时尤为重要。

向量距离仅代表统计相似性，不能作为词义真值或逻辑关系的判定依据。模型对 Token 关系的理解发生在 Attention 层，而非静态 Embedding 阶段。

RAG 适用于知识存在于参数之外且持续更新、资料规模超过上下文窗口、或需要回溯具体来源的场景。翻译、改写、纯计算等不依赖外部知识的任务并非 RAG 的必要场景。

RAG 不等于长期记忆，不解决跨会话状态维护。检索结果的质量依赖索引时效性，长期不更新的索引会导致无关或过时内容被召回到上下文中。

## 核验清单

确认所用模型配套的 Tokenizer 类型与词汇表规模，验证切分粒度是否符合预期。

验证 Embedding 表维度与模型规格一致，初始向量在相同 Token ID 下是否稳定输出。

确认 Attention 计算中因果遮罩的作用范围，检查解码阶段是否存在信息泄露风险。

核实 KV Cache 的复用策略：新增上下文（如工具调用返回结果、插入 RAG 资料）后是否触发 Prefill 或完全重算。

验证 RAG 系统的索引更新机制与检索结果重排策略是否覆盖时效性、多版本和权限等维度。

评估 RAG 输出中模型对检索资料的引用准确性，避免误读或混淆多个来源。

## 来源与核验

- [原始文章](https://juejin.cn/post/7663518564783931401)
- 页面事实以原始来源及其引用的官方资料为准；版本、星标和模型能力会随时间变化。
- AI Stack 不公开抓取到的全文快照，只发布独立转写与来源入口。

---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [掘金](/tags/%E6%8E%98%E9%87%91/) / [工程实践](/tags/%E5%B7%A5%E7%A8%8B%E5%AE%9E%E8%B7%B5/) / [来源转写](/tags/%E6%9D%A5%E6%BA%90%E8%BD%AC%E5%86%99/)

### 相关文章

- [6.结构化输出](/posts/20260718-juejin-6%E7%BB%93%E6%9E%84%E5%8C%96%E8%BE%93%E5%87%BA-0-80d50ad8af/)
- [GitHub Copilot for JetBrains 架构拆解：Provider / Endpoint / Skills / Sandbox / Polic](/posts/20260718-juejin-github-copilot-for-jetbrains-%E6%9E%B6%E6%9E%84%E6%8B%86%E8%A7%A3provider-endpoint-0-2a917f4cdc/)
- [从零到一手撸 Agent 系列 — 第 1 篇：一个 Coding Agent 是什么？](/posts/20260718-juejin-%E4%BB%8E%E9%9B%B6%E5%88%B0%E4%B8%80%E6%89%8B%E6%92%B8-agent-%E7%B3%BB%E5%88%97-%E7%AC%AC-1-%E7%AF%87%E4%B8%80%E4%B8%AA-coding-agent-%E6%98%AF%E4%BB%80%E4%B9%88-0-b0628f7a64/)
- [AI 视觉连载3：RGB与通道](/posts/20260211-juejin-ai-%E8%A7%86%E8%A7%89%E8%BF%9E%E8%BD%BD3rgb%E4%B8%8E%E9%80%9A%E9%81%93-0/)
- [clawdbot无痛升级openclaw，飞书变个人AI助理保姆级教程](/posts/20260212-juejin-clawdbot%E6%97%A0%E7%97%9B%E5%8D%87%E7%BA%A7openclaw%E9%A3%9E%E4%B9%A6%E5%8F%98%E4%B8%AA%E4%BA%BAai%E5%8A%A9%E7%90%86%E4%BF%9D%E5%A7%86%E7%BA%A7%E6%95%99%E7%A8%8B-1/)