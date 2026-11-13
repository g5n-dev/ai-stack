---
title: "New AI “copilot” helps engineers design better structures"
date: 2026-11-13T15:56:52+08:00
draft: false
entry_kind: "auto"
tags: ["生成式 AI", "机器学习", "Research", "Algorithms", "Design", "Artificial intelligence", "Machine learning", "Computer modeling"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:4128e0525a3c8aa4f8afe142025bba463335a9c0bc3145b2e6b71adb7134d0ff"
source_payload_sha256: "sha256:ef33514fe00b2fd450f682774dfd666385a315fe99e958f406a49f11373227bd"
observation_id: obs_babb1d695637283d5ca3646f8300aeecbe29c83848d74c59fb63eb8c9b884bb8
event_id: evt_51b342f359c37e1a71af385f6b9469d4f0c1dcba8a74024c6d65e671996500be
revision_id: rev_e407595aeef608d45e6572ecf9b2b8d58d902b15f78826b6d4dc26a4e59a8d22
source_published_at: 2026-11-13T05:00:00Z
first_seen_at: 2026-11-13T07:55:44.301257Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 57
interpretation_sha256: "sha256:e81d8e48bc1f4fbc5888a2acd24ee57579fa35cbb3d96230fa96c95dcd24342a"
description: "MIT 团队提出了一种“人在回路中”的拓扑优化系统：算法生成结构时，由机器学习快速标出设计师可能需要调整的区域，让人边设计边反馈。它希望兼顾计算效率、结构性能、制造可行性与工程师对结果的掌控感。"
external_url: https://news.mit.edu/2026/new-ai-copilot-helps-engineers-design-better-structures-1113
parent_observation_id: null
last_seen_at: 2026-11-13T07:55:44.301257Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://news.mit.edu/2026/new-ai-copilot-helps-engineers-design-better-structures-1113](https://news.mit.edu/2026/new-ai-copilot-helps-engineers-design-better-structures-1113)
- **发布域名**: news.mit.edu

## 要点解读

### 这是什么
MIT 团队提出了一种“人在回路中”的拓扑优化系统：算法生成结构时，由机器学习快速标出设计师可能需要调整的区域，让人边设计边反馈。它希望兼顾计算效率、结构性能、制造可行性与工程师对结果的掌控感。

### 用在哪里
适用于飞机、汽车、赛车等复杂结构设计，也面向建筑、桥梁及对安全性和可制造性要求较高的工程场景。对于既依赖算法性能、又需要人工判断的团队尤其有价值。

### 可以推断的
- 推测：把人工反馈提前到生成阶段，可能比设计完成后再返工更容易降低工程成本。
- 推测：允许工程师直接干预关键区域，可能有助于提升其对算法设计结果的信任。

## 来源摘要/节选

> The use of algorithms to design structures has led to new parts optimized for ultralight aircraft, high-bandwidth antennas, and F1 racing cars.
>
> But the best algorithmic design techniques still require lots of computation and time: Users only see the final design after it’s complete, after which they often must start the design process all over again to make changes. That process also makes it harder to trust that the final designs are structurally sound.
>
> MIT researchers are making algorithmic designs more collaborative with a system that acts like an AI copilot. As the algorithm is generating the structure, it presents regions to the human designer for feedback.
>
> In an open-access Communications Engineering paper describing the system, the researchers showed it led to more easily manufacturable structures with higher buckling loads while adding only 15 seconds to the total design time compared to all-algorithmic approaches.
>
> The researchers believe the approach, which uses a design technique known as topology optimization, could make algorithmic design more accessible and manufacturable for a broader class of design engineers.
>
> “Right now, the human doesn’t have any agency or control over the design process as it’s playing out,” explains lead author Dat Ha PhD ’26, a recent MIT civil and environmental engineering doctoral student who is now a structural designer at LeMessurier. “For these really complex designs, we wanted to also tap into our brain, which is the most complex machine there is, to solve these design problems in a way that’s more practical to industry.”
>
> Joining Ha on the paper are Ferdous Alam, a former MIT postdoc who is now an assistant professor at Georgia Tech; Markus Buehler, the MIT Jerry McAfee (1940) Professor of Engineering; Faez Ahmed, MIT associate professor of mechanical engineering; and senior author Josephine Carstensen, MIT associate professor of civil and environmental engineering.
>
> Bringing a human in the loop
>
> Topology optimization is one of the most advanced and promising algorithmic design techniques. It uses formal optimization techniques to iteratively fill in the space given for a design in a way that maximally achieves the stated goals. For most applications, the process requires a lot of computation and time. When it’s finally done, the designs can be impractical to build or have other issues the engineer didn’t consider. For instance, some designs might have eight or more beam connections at a single point, which would be difficult to make in the real world.
>
> “Engineers are always very skeptical of computer programs, especially if they give you very weird-looking or unexpected designs,” Ha says. “On paper, topology optimization is really powerful and can achieve great, high-performing designs, but its black box nature has made it less widely adopted in industry.”
>
> Topology optimization has gotten traction in the automotive and aerospace industries, but it’s been used less to design buildings or bridges, partly because design engineers need to know they can trust the output.
>
> “A big limiting factor has been that the design engineer has very little influence over how the design evolves and therefore can’t control undesirable features,” Carstensen explains. “The lack of control and lack of ownership also inhibits its use.”
>
> To address those problems, the researchers made topology optimization more collaborative in an approach that Carstensen compares to having a design copilot.
>
> Prior attempts at adding human judgment slowed things down dramatically. The researchers’ new system uses machine learning to quickly identify the most likely regions of an algorithmic design that a human would want to change. To train the machine-learning model, the researchers created a synthetic dataset of probable human feedback to thousands of designs that critiqued things like aesthetics, performance criteria, and manufacturability.
>
> “We thought if we could create a record of where humans have made changes to these programs, then perhaps there’s a pattern to those choices, which is not very different from other types of machine-learning approaches,” Ha says.
>
> Carstensen sees the system as bringing together the best of algorithmic and human design approaches.
>
> “The idea is to tap into the brains of the designers and get them to infuse their domain knowledge as the design evolves,” Carstensen says.
>
> In demonstrations, the researchers showed their human-in-the-loop approach improved manufacturability and linear buckling load by 39 percent while only modestly increasing the total design time.
>
> Right now, the approach only allows users to make structures within identified regions thicker or thinner, but they hope to add other options for modification in future versions.
>
> “The hope is that by addressing these hurdles, we open up topology optimization to a much wider audience, not only in industry but also to researchers and students in academia,” Carstensen says.
>
> From designs to structures
>
> The researchers see their approach complementing AI only-approaches to design.
>
> “We are arguing there’s room for both,” Carstensen says. “If you are in a discipline that has a lot of computational resources, you can use the other approach. But if you really need the human input, you can use this collaborative approach.”
>
> Adding human input also serves to increase trust.
>
> “In some settings, the humans need to make the final decisions before advancing the final design,” Carstensen says. “By involving humans, we can get higher-performing designs to the real world to create higher-performing structures. Because it’s not just about designing good artifacts; it’s about creating good artifacts that humans will actually accept and make.”
>
> The work was supported, in part, by the MathWorks Engineering Fellowship Fund, TATA Steel, and the MIT Generative AI Impact Consortium.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。