---
title: "OpenAI联合博通推出首款定制AI芯片"
date: 2026-06-24T22:00:08+08:00
draft: false
entry_kind: "auto"
tags: ["OpenAI", "定制AI芯片", "博通", "AI加速", "推理芯片", "大模型", "硬件创新", "AI基础设施"]
categories: ["AI 工程", "系统与基础设施"]
source: hacker_news
description: "OpenAI 近日发布了其首款自研 AI 加速芯片，携手 Broadcom 完成硬件设计。该芯片针对大模型推理进行优化，在功耗与吞吐量之间实现更平衡的性能。对 AI 开发者和行业观察者而言，这一动向意味着芯片层面的竞争格局可能出现新变化，值得深入了解其技术细节与商业影响。"
external_url: https://techcrunch.com/2026/06/24/openai-unveils-its-first-custom-chip-built-by-broadcom
scenarios: ["AI/ML项目"]
---

# OpenAI联合博通推出首款定制AI芯片

---

## 基本信息

- **作者**: jamdesk
- **评分**: 340
- **评论数**: 244
- **链接**: [https://techcrunch.com/2026/06/24/openai-unveils-its-first-custom-chip-built-by-broadcom](https://techcrunch.com/2026/06/24/openai-unveils-its-first-custom-chip-built-by-broadcom)
- **HN 讨论**: [https://news.ycombinator.com/item?id=48663324](https://news.ycombinator.com/item?id=48663324)

---
## 导语

OpenAI 近日发布了其首款自研 AI 加速芯片，携手 Broadcom 完成硬件设计。该芯片针对大模型推理进行优化，在功耗与吞吐量之间实现更平衡的性能。对 AI 开发者和行业观察者而言，这一动向意味着芯片层面的竞争格局可能出现新变化，值得深入了解其技术细节与商业影响。

---
## 评论

#### 核心观点

OpenAI推出首款定制芯片是其在AI基础设施竞争中寻求自主可控的关键一步，但受制于制造能力与生态壁垒短期内难以撼动英伟达的主导地位。

#### 事实陈述

根据公开信息，OpenAI此款芯片由Broadcom代工，采用台积电先进制程。Broadcom本身就是谷歌TPU系列的主要供应商，在定制ASIC领域有丰富经验。这一合作模式意味着OpenAI无需自建晶圆厂，可借助现有半导体产业链快速落地。

#### 作者观点

我认为此举的战略意图远超技术本身。AI模型的训练与推理成本持续攀升，对算力的依赖使得芯片成为核心战略资源。OpenAI选择定制路线，一方面是为了摆脱对通用GPU的单一依赖，另一方面也是在供应链紧张背景下构建冗余能力。长远看，拥有自研芯片可帮助其针对自身模型架构做深度优化，在能效比上形成差异化优势。

#### 边界条件

然而需要注意的是，芯片从设计到量产周期长，软件生态的迁移成本同样不可忽视。CUDA生态的成熟度仍是英伟达的护城河，OpenAI即便拥有芯片，也很难在短期内建立与之匹敌的开发者社区。此外，芯片性能最终受限于制程工艺，在全球半导体产能受限的背景下，产能分配仍是未知数。

#### 推断

我的推断是，OpenAI的定制芯片短期内更可能作为内部训练补充而非大规模商用。其更现实的路径是“双轨并行”：核心业务继续依赖英伟达H系列，定制芯片则用于特定推理场景的成本优化。待产品成熟后，不排除向企业客户提供差异化算力服务的可能。

#### 实践启发

对行业而言，AI芯片的多元化趋势正在加速。企业客户应关注芯片供应商的生态兼容性与长期供货稳定性，而非仅聚焦单次采购成本。芯片设计能力的“平民化”意味着更多垂直领域玩家可能效仿这一模式，推动AI基础设施走向分层竞争格局。

---
## 学习要点

- OpenAI 推出首款自研 AI 加速芯片，携手 Broadcom，标志着其摆脱对外部 GPU 的依赖。
- 该芯片针对大模型训练和推理进行专门优化，可显著提升计算性能和能效。
- 采用 Broadcom 的先进制程（推测 5nm），实现更高的晶体管密度和功耗控制。
- 自研硬件将帮助 OpenAI 降低大规模模型训练的成本和碳排放。
- 与 Broadcom 的合作利用其在网络和芯片封装方面的技术积累，提升芯片的互连效率。
- 此举可能重塑 AI 硬件竞争格局，迫使其他 AI 研究机构加速自研芯片的进程。

---
## 引用

- **原文链接**: [https://techcrunch.com/2026/06/24/openai-unveils-its-first-custom-chip-built-by-broadcom](https://techcrunch.com/2026/06/24/openai-unveils-its-first-custom-chip-built-by-broadcom)
- **HN 讨论**: [https://news.ycombinator.com/item?id=48663324](https://news.ycombinator.com/item?id=48663324)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/)
- 标签： [OpenAI](/tags/openai/) / [定制AI芯片](/tags/%E5%AE%9A%E5%88%B6ai%E8%8A%AF%E7%89%87/) / [博通](/tags/%E5%8D%9A%E9%80%9A/) / [AI加速](/tags/ai%E5%8A%A0%E9%80%9F/) / [推理芯片](/tags/%E6%8E%A8%E7%90%86%E8%8A%AF%E7%89%87/) / [大模型](/tags/%E5%A4%A7%E6%A8%A1%E5%9E%8B/) / [硬件创新](/tags/%E7%A1%AC%E4%BB%B6%E5%88%9B%E6%96%B0/) / [AI基础设施](/tags/ai%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [Cloudflare Agent Cloud接入OpenAI模型助力企业AI代理部署]({{< relref "posts/20260413-blogs_podcasts-enterprises-power-agentic-workflows-in-cloudflare--0.md" >}})
- [a16z对话：Anthropic与OpenAI的博弈及AI基础设施投资逻辑]({{< relref "posts/20260220-blogs_podcasts-bitter-lessons-in-venture-vs-growth-anthropic-vs-o-6.md" >}})
- [a16z深度对话：Anthropic与OpenAI的博弈、Noam Shazeer及AI基础设施投资]({{< relref "posts/20260221-blogs_podcasts-bitter-lessons-in-venture-vs-growth-anthropic-vs-o-10.md" >}})
- [OpenAI与亚马逊达成战略合作，将Frontier模型引入AWS]({{< relref "posts/20260227-blogs_podcasts-openai-and-amazon-announce-strategic-partnership-0.md" >}})
- [OpenAI与亚马逊达成战略合作，将Frontier模型引入AWS]({{< relref "posts/20260227-blogs_podcasts-openai-and-amazon-announce-strategic-partnership-3.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*