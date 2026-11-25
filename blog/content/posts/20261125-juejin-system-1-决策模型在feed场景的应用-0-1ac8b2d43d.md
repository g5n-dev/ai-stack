---
title: "System 1 决策模型在Feed场景的应用"
date: 2026-11-25T10:26:12+08:00
draft: false
entry_kind: "auto"
tags: ["掘金", "工程实践", "来源转写"]
categories: ["AI 工程"]
source: "juejin"
content_mode: "evidence_backed_rewrite"
publication_tier: "B"
source_capture_mode: "full_article"
source_snapshot_sha256: "sha256:412ab3d04683608a041dbe9c6230ecb08a8cad3aa7b95d497687b9ae60643cd2"
source_payload_sha256: "sha256:d326ab17181600166fcd447f009a9acf4f03b3da7f373cdc4379a5830dd4821b"
source_published_at: 2026-11-25T02:15:27Z
timestamp_confidence: feed
extractor_version: "source-contract-v2"
discovery_method: "article_html"
source_completeness: "complete"
parent_snapshot_sha256: "sha256:a814a098ebf7f07d41df6566f248e7841e7dbe1b0a695eb005de58e2f1e4aaa8"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 23
description: "核心结论 System 1 决策模型把推荐任务表达为带类型的概率输出，例如判断候选内容是否会被点击，而不是生成一段文本再解析答案。来源以 、 在 MIND-small 和内部数据集上验证：未微调时 AUC 约为 0.539，接近随机；简单微调后提升至 0.6 以上。"
external_url: https://juejin.cn/post/7711679772027928602
observation_id: obs_1ac8b2d43dc3f841e88d9b4d0fb510117f25a1be38c632ab180cafac25c83e20
revision_id: rev_e1f2f05993406532789aa559c94466914d9dcd72a1aea41f68ee2cee6d7a1ad8
event_id: evt_24b5635d95c240f7a37e56d2f6a01b143b49c8fb85d2999cab785f2e6b68a143
lineage_relation: original
parent_observation_id: null
first_seen_at: 2026-11-25T02:24:52.960928Z
last_seen_at: 2026-11-25T02:26:12Z
---

## 转写说明

> 本文基于已校验的公开原文进行结构化转写与事实梳理，非原文转载。
> 转写保留可核验的技术事实，并将工程建议与来源观点明确分开。

- **原作者**: 百度Geek说
- **原始来源**: [https://juejin.cn/post/7711679772027928602](https://juejin.cn/post/7711679772027928602)
- **原文发布时间**: Wed, 25 Nov 2026 02:15:27 GMT

## 核心结论

System 1 决策模型把推荐任务表达为带类型的概率输出，例如判断候选内容是否会被点击，而不是生成一段文本再解析答案。来源以 `laya-multilingual`、`Jev-API` 在 MIND-small 和内部数据集上验证：未微调时 AUC 约为 0.539，接近随机；简单微调后提升至 0.6 以上。首轮线下评估还显示，该方案超过线上粗排基线，并在低活用户上优于精排 uAUC。

工程上的主要矛盾不是单次预测能力，而是同一用户需要给约 1800 条候选打分时，如何避免重复编码用户上下文。Encoder、Decoder 和双塔三条路线分别对应不同的缓存能力、交互强度与上线成本。

## 能力机制

Encoder 使用双向注意力，新增 token 会改变前序 token 的表示，因此用户部分难以充分预计算。其优点是可直接融合用户与候选信息；来源记录，Laya 在约 1k token 下可达到个位数毫秒的单条延迟，但 32k token 测试接近 1.5 秒。FP8、libtorch、tilelang、知识蒸馏及 batch、扇出调优，使 Encoder 小流量成本降至初始版本约三成，但推全成本评估仍约为数万张 GPU。

Decoder 使用因果注意力。用户信号位于候选之前时，user-state 的 Prefill 可以提前执行一次，并被约 1800 条候选共享；预计算还可与预筛阶段并行。来源给出的粗略计算显示，在忽略模型规模和网络结构差异时，单用户批量预估的计算量可由 `1000×1800` 降至 `750×1+250×1800`，约为原来的 25%。当前 Decoder 小流量方案按比例推算的推全成本在一万张 GPU 以内。

双塔将交叉编码器拆为用户塔与物品塔，物品向量可离线生成并按小时级更新，线上只需编码用户。代价是细粒度交互减少，精度通常低于交叉编码器，更适合低成本实验。

降本还包括任务蒸馏、LoRA、冻结底层及共享前缀打包。来源实验中，任务蒸馏后的 uAUC 为 0.652，高于原模型的 0.649，单条耗时由 20+ ms 降至 10+ ms。

## 快速开始

1. 准备用户状态、候选内容和问题定义。示例状态包含用户近期查询、近期消费内容及候选标题、摘要；点击问题使用布尔类型，并规定“会点击”和“不会点击”的标签含义。
2. 使用来源确认过的 `laya-multilingual` 或 `Jev-API` 对候选进行概率打分，先在 MIND-small 与内部场景数据上比较微调前后的 AUC、uAUC，而不是只观察准确率。
3. 微调时加入有判别力的内容字段，并筛选用户特征组合；来源指出，不同用户特征组合会直接影响 Feed 排序效果。
4. 线上验证优先确认候选规模、batch、扇出和用户缓存命中情况，再决定使用 Encoder、Decoder 或双塔。Decoder 路线应让 user-state 在候选请求前完成 Prefill，并验证多个候选确实复用同一份缓存。
5. 来源未提供可确认的安装命令、接口参数或密钥配置方式，因此这里不补写命令和密钥。

## 适用边界

来源认为，该方案较适合低活用户、新内容、长尾内容及用户与内容兴趣匹配场景。低活用户历史点击少，传统精排可用的 ID 特征和统计量有限，而决策模型可借助语言理解与预训练世界知识进行判断。案例中，决策模型分别将相关政策解读和突发时政内容排入前 5%，而当时系统排序靠后。

对于重度用户，传统精排已有充足点击行为，来源判断新增收益会趋近于零。双塔适合先验证低成本收益，但不宜把其离线效果直接等同于交叉编码器。

Encoder 虽然交互充分，但扩展长上下文时延迟上升明显。Decoder 和双塔的上述 GPU 数量均来自来源中的成本推算，不等同于已完成全量上线。来源也未给出统一的数据规模、硬件配置、线上流量比例或全量收益，不能据此推断最终推全效果。

## 核验清单

- 复现未微调与微调后的 AUC、uAUC，并与粗排、精排基线使用相同数据和评估口径比较。
- 同时记录准确率与排序指标；来源指出点击样本占比较低时，全部预测“不点”也可能获得较高准确率。
- 检查低活用户、新内容、长尾内容等分组的独立结果，避免只用总体指标掩盖收益差异。
- 记录单条延迟、批量吞吐、P80/P90 耗时、候选扇出和 GPU 占用，复核约 1800 条候选场景。
- Decoder 上线前核对 user-state 是否只计算一次、候选是否复用缓存，以及 user-id 到固定卡片的映射是否稳定。
- 降本实验分别核对 FP8、蒸馏、算子优化和 batch 调优的独立贡献，不把组合优化后的结果归因于单一手段。
- 双塔方案需验证物品向量更新时效，并比较其与交叉编码器的排序损失，再决定是否扩大流量。
- 来源没有给出完整训练配置、线上 A/B 周期或全量回滚标准；这些项目应作为工程补充记录，不能写成已经验证的成果。

## 来源与核验

- [原始文章](https://juejin.cn/post/7711679772027928602)
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