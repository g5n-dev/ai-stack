---
title: "AI 语言学习系统的工程边界：为什么 LLM 不该负责复习排期"
date: 2026-07-25T18:48:02+08:00
draft: false
entry_kind: "auto"
tags: ["掘金", "工程实践", "来源转写"]
categories: ["AI 工程"]
source: "juejin"
content_mode: "evidence_backed_rewrite"
publication_tier: "B"
source_capture_mode: "full_article"
source_snapshot_sha256: "sha256:b85198605cc2d5b007d0e542c522eee62a433b219f0f33b250719fb37cc49928"
source_payload_sha256: "sha256:d5b4ae231d0055fa946e0e4b5a641ebcc07115c7b2a9418c67eb22c081727472"
source_published_at: 2026-07-25T09:34:44Z
timestamp_confidence: feed
extractor_version: "source-contract-v2"
discovery_method: "article_html"
source_completeness: "complete"
parent_snapshot_sha256: "sha256:a685f896be8bd57f4a11df8470424f69172cf301bfd60551a6f5ef4956fc3c32"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 31
description: "核心结论 LLM 不负责复习排期等确定性业务逻辑。系统设计应遵循的核心原则是：LLM 处理模糊性，确定性代码维护业务事实。 一个相对稳定的职责分工如下：LLM 负责意图识别、语言解释、语义排序和记忆方法生成；端侧负责原始输入处理、OCR 临时缓存和基础清洗；确定性代码负责语言校验、去重、计划写入、复习排期和动作白名单…"
external_url: https://juejin.cn/post/7665969355775737902
observation_id: obs_56aa8ef5b6127e4694e1f20091d4024742225be46a7d7f7b6275bbf202ea02bc
revision_id: rev_b1dbf894ac1b22eeaecbaad3c320370214c27cb1ea616887c5b8b5ee9fcfa8d1
event_id: evt_5d5dbf815f3bd74fec0d1baee0c7e7d86588307d51dd55ec0dadb78ec79a707d
lineage_relation: original
parent_observation_id: null
first_seen_at: 2026-07-25T10:46:38.980604Z
last_seen_at: 2026-07-25T10:48:02Z
---

## 转写说明

> 本文基于已校验的公开原文进行结构化转写与事实梳理，非原文转载。
> 转写保留可核验的技术事实，并将工程建议与来源观点明确分开。

- **原作者**: 语歌
- **原始来源**: [https://juejin.cn/post/7665969355775737902](https://juejin.cn/post/7665969355775737902)
- **原文发布时间**: Sat, 25 Jul 2026 09:34:44 GMT

## 核心结论

LLM 不负责复习排期等确定性业务逻辑。系统设计应遵循的核心原则是：LLM 处理模糊性，确定性代码维护业务事实。

一个相对稳定的职责分工如下：LLM 负责意图识别、语言解释、语义排序和记忆方法生成；端侧负责原始输入处理、OCR 临时缓存和基础清洗；确定性代码负责语言校验、去重、计划写入、复习排期和动作白名单；RAG 结果必须回源校验；关键写操作必须经过用户确认。这套边界的价值在于：即使模型调用失败，用户仍可完成学习、复习和数据管理；模型升级时不需要重新改写整个业务系统。

## 能力机制

系统划分为四层。端侧层承担 OCR、来源解析和临时缓存；LLM 层负责意图识别、语言解释和语义重排；确定性业务层执行语言校验、去重、计划写入和复习排期；基础设施层统一控制 Provider 路由、缓存和记忆存储。

聊天能力通过类型协议实现。服务端输出包含类型标识和 Schema 版本的 SkillEnvelope，客户端在请求中声明支持的 Skill 类型和最高 Schema 版本。模型只生成候选参数，写操作由客户端已有流程完成，并通过动作白名单限制可执行的操作范围。

复习排期采用固定节点与动态建议时长结合的方案。当前实现使用 8 个固定节点：30 分钟、12 小时、1 天、2 天、4 天、7 天、15 天、30 天。每次建议复习时长根据首次学习投入、迟到偏移、前序缺失、历史错误、复习表现和首次测验等因素动态计算。

长期上下文通过不可变的 WorkingMemory 组织，包含角色与安全约束、结构化用户记忆、最近对话、当前学习状态、相关 RAG 记忆和当前消息。异步记忆提取按事实、偏好、经历、关系、情绪等类别写入向量库，召回时结合全文检索与向量检索。会话重置通过维护递增的 Epoch 防止旧数据写入。

TTS 成本按缓存未命中计费。缓存键由 provider、model、voice、language、audioParameters 和 normalizedText 的哈希值构成。成本估算公式为：providerCost ≈ cacheMissCount × averageSynthesisCost。

## 快速开始

构建导入流水线需分阶段处理：

```
来源解析 → 内容形态识别 → 候选边界切分 → 清洗与噪声校验 → 语言过滤 → 必要时分拆 → 去重并构建学习项
```

每阶段保存中间结果并可独立测试。LLM 仅作为个别清洗步骤的补充，不作为唯一实现。

复习排期验证可通过以下测试场景：相同记录必须产生一致结果；复习迟到时建议时长不能下降；前序节点缺失时需增加复习负担；首次测验表现良好时可缩短建议时长；任何输入都不能突破时长上下限。

RAG 召回后必须查询业务主表校验有效性，丢弃失效记录后再重排返回。

## 适用边界

进程内异步任务仅能保证 Best Effort。服务重启后任务可能丢失，重要的记忆提取和索引任务需要持久化队列、重试和幂等设计。

小规模数据可使用关系数据库做精确向量扫描；数据量上升后需根据召回延迟和索引维护成本评估专用向量方案。

固定复习节点容易解释和测试，但还不是基于个人长期数据拟合的记忆模型。未来若引入个性化算法，应保留版本号、迁移策略和离线回放能力。

这些边界不会通过更换更大的模型自动消失。

## 核验清单

图片导入链路：原图留在端侧、端侧 OCR 仅上传文本、OCR 结果视为不可信数据、设置文本长度上限、写入前执行去重。

能力卡片交互：客户端声明支持的 Skill 类型和 Schema 版本、模型不直接执行写操作、最终写入经过语言对和权限校验、客户端仅接受白名单动作。

可观测性需覆盖完整闭环。按阶段记录事件：skill_routed、skill_payload_generated、skill_presented、skill_confirmed、business_write_succeeded、first_learning_completed、first_review_completed。分别建立 OCR 导入漏斗、复习到期漏斗、TTS 请求漏斗和 Skill 写入漏斗。

## 来源与核验

- [原始文章](https://juejin.cn/post/7665969355775737902)
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