---
title: "From User Sequences to Scaling Laws: A Multi-Stage Architecture for Meta’s Ads Ranking"
date: 2026-08-06T04:42:56+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "Data Infrastructure", "ML Applications", "Production Engineering", "博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:4506bdce71a82f9b7d1c046803bdda03303c31fda0d0866acc913449deabe404"
source_payload_sha256: "sha256:e007edde1b1c594ced918024643a7617f6586148b55656bbaf6de4db41e05c68"
observation_id: obs_c1d866c5ae209a4f25c2267d9f17d6294ea68d417779d44f322e66be13dcd23e
event_id: evt_567702e8acc762ea36380b565c6a9c31fd8f7e8808a75e7aaeafcc8f052ffecb
revision_id: rev_20b2d894659181abcae3df5ec4be15fbd18dc69d6f7d61404edbe5064be5214d
source_published_at: 2026-08-05T19:20:20Z
first_seen_at: 2026-08-05T20:52:50Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 86
interpretation_sha256: "sha256:274ee0228bcaa15a4dfef9cf7a224ba8829dfa396aebb70f386fa3378949dcb7"
description: "该内容介绍了一种将离线用户序列建模与在线广告排序分离的多阶段结构，并配合基于稠密标记化与目标感知注意力的学习方式，使模型能够直接从数据中捕获特征交互。"
external_url: https://engineering.fb.com/2026/08/05/ml-applications/from-user-sequences-to-scaling-laws-a-multi-stage-architecture-for-metas-ads-ranking
parent_observation_id: null
last_seen_at: 2026-08-05T20:39:53.094264Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://engineering.fb.com/2026/08/05/ml-applications/from-user-sequences-to-scaling-laws-a-multi-stage-architecture-for-metas-ads-ranking](https://engineering.fb.com/2026/08/05/ml-applications/from-user-sequences-to-scaling-laws-a-multi-stage-architecture-for-metas-ads-ranking)
- **发布域名**: engineering.fb.com

## 要点解读

### 这是什么
该内容介绍了一种将离线用户序列建模与在线广告排序分离的多阶段结构，并配合基于稠密标记化与目标感知注意力的学习方式，使模型能够直接从数据中捕获特征交互。

### 用在哪里
适用于需要处理海量用户行为序列并在毫秒级完成大量广告排序的大规模广告推荐系统，尤其适合关注模型可扩展性和服务延迟的工程团队。

### 可以推断的
- 推测：在离线阶段预计算用户嵌入并在在线阶段复用，可降低实时计算压力并保持模型深度。  
- 推测：采用稠密标记化让注意力机制自动学习稀疏特征的交叉，相比手工特征工程更具灵活性。

## 来源摘要/节选

> Every day, Meta’s recommendation platforms handle billions of user interactions, generating rich temporal signals that capture individual preferences and intent across products, ads, and content. In our 2024 post on sequence learning for ads recommendations, we showed how modeling the order and timing of user actions (rather than relying on static, manually engineered sparse features) produces richer, sequence-aware representations of user interests and ad preferences.
>
> This post goes a step further, introducing two architectural breakthroughs that let us scale sequence learning advancements from foundational innovations into a production platform with predictable, LLM-style scaling laws: (1) a multi-stage sequence model that decouples heavy offline user modeling from lightweight online ranking tasks and (2) a learning technique based on dense tokenization and target-aware attention that efficiently learns feature interactions directly from data.
>
> Together with our broader model innovations, these advancements have contributed to a cumulative lift of 6% in conversions on Instagram, 3% in conversions on Facebook and 3.5% in ad clicks on Facebook. This unified platform for sequence modeling is a core component of Meta’s Generative Ads Recommendation Model (GEM), helps to harness the comprehensive user behavioral understanding of this learning paradigm to maximize the benefit to advertisers.
>
> The Historical Challenges of Sequence Modeling
>
> Ads recommendation systems must retrieve and rank thousands of ads within milliseconds, processing millions of candidates per second. To manage this scale, some approaches to sequence models rely on hybrid model configurations where a specific model processes user event sequences and another model handles sparse feature interactions.
>
> While effective at meeting production demands, this hybrid approach has potential tradeoffs:
>
> Lossy knowledge transfer between components
>
> Continued reliance on manual feature engineering
>
> Scaling ceilings from interference between ranking and sequence model components
>
> Scaling both temporal sequence lengths and the transformer models that process them can turn the tradeoffs of the hybrid approach into a bottleneck, limiting the ability to improve the ads experience of users and the performance of advertisers’ campaigns.
>
> We’ve made two fundamental architectural breakthroughs in sequence learning that resolve the core tension between model complexity and serving efficiency: (1) a multi-stage sequence model that decouples offline user modeling from online ranking and (2) a dense tokenization with target-aware attention learning paradigm. Together, they provide a flexible production strategy that helps generalize sequence learning models and establish an LLM-style scaling law that predictably balances model performance with compute.
>
> Introducing the Multi-Stage Sequence Model
>
> To address scaling efficiency, a multi-stage model has been developed that enables scaling of a transformer-based sequence model in a compute efficient manner. Separating the sequence model into two complementary stages (upstream/offline user modeling and downstream/online ranking), enables model capacity to scale so that performance keeps improving without proportional increases in serving resources.
>
> In Figure 1, the left panel shows the offline user model. It processes long user histories asynchronously and produces cached embeddings that capture deep behavioral patterns. The right panel shows the online ranking model that combines these cached representations with real time ad candidate signals to produce the final ranking. The arrow between the two stages carries the user feature embeddings from offline → online ranking models.
>
> Figure 1: An overview of the multi-stage model.
>
> Two Key Stages of the Model
>
> First Stage: Offline User Model
>
> User-side features are processed asynchronously using deep transformer upstream models. These models scale to several transformer layers with sequence lengths in the thousands and generate embeddings that are precomputed and cached at the user level. The upstream model strictly separates user features from ad and context features to ensure user embeddings remain independent of any particular ad candidate.
>
> Second Stage: Online Ranking Model
>
> The offline user model representations are complemented with online ranking models that use fresh user signals and ad candidate information for real time ranking. This stage is optimized for speed, meeting strict latency budgets while leveraging the deep representations computed offline.
>
> Separating the sequence modeling system into two distinct, yet complementary, stages enables an increase in model complexity along a scaling curve for the Offline User Model without causing a spike in serving costs for the Online Ranking Models.
>
> Sequence Model Architecture Innovations
>
> Dense Tokenization
>
> This tokenization approach integrates sparse features with sequential behavioral data into a single dense vocabulary, enabling attention mechanisms to discover interactions independently. Unlike traditional recommendation systems, which rely on manually engineered representations to capture sparse cross-feature interactions, this approach lets the model learn those interactions directly from the data.
>
> Target-Aware Multi-Head Attention
>
> Tokenized sparse features and ad candidate information are fused with user behavior sequences, then processed by a memory-efficient form of multi-head attention that lets each layer weigh a user’s past behaviors against the specific ad being scored. Stacking multiple aligned attention blocks with stable attention distributions allows each layer to capture higher-order interactions between the target ad and the user’s historical behavior, progressively distilling long sequences into compact representations.
>
> A Predictable Scaling Curve
>
> LLM-Style Scaling Law
>
> When running on real-world ads traffic, the multi-stage sequence model demonstrates the emergence of predictable scaling laws for ads recommendations that are analogous to those observed in large language models. Performance improvements follow a log-linear relationship with respect to compute, with a marked improvement in scaling efficiency over other transformer-based sequence models. Figure 2 conveys these scaling properties by showing the relationship between compute (FLOPs) and model performance (measured by normalized entropy, NE) across several dimensions: model depth, content/semantic enrichment, model width, and sequence length.
>
> Figure 2: Offline Model Scaling Law across several dimensions (model depth, content/semantic enrichment, model width, sequence length).
>
> Levers for Scaling
>
> Unlike LLMs, which process dense and continuous text, ads recommendation systems must integrate sparse ID features with temporal user sequences. The fact that LLM-style scaling emerged despite the structural differences provides a strong indicator of model architectural fit for further sequence learning applications.
>
> We have identified four levers that we anticipate will help unlock the frontier of the scaling law:
>
> 1. Balanced Model Shape
>
> Optimal performance requires balanced growth across model depth, width and sequence lengths. If scaling only occurs on a single axis, the other axes will likely bottleneck the performance improvements, potentially leading to diminishing returns. This mirrors findings from LLM scaling law research, a principle we call the scaling synergy principle.
>
> 2. Multi-Stage Tunability
>
> The multi-stage architecture provides a tunable lever to scale either the offline or online model up/down. Scaling the online ranking model drives steeper improvements per unit of compute that is bounded by serving/request time requirements. Scaling the offline model (shown in Figure 2) follows a more gradual curve, but its async inference avoids latency constraints, allowing scale in at an unhindered rate.
>
> 3. Sequence Composition
>
> Performance continues to improve as sequences get longer, but an impactful finding is that sequence diversity beats sequence homogeneity.  A balanced mix of action types (e.g., views, clicks, conversions) yields better results than sequences composed of a single action type. This finding suggests that a diverse mix of engagement types and broad temporal coverage produce richer behavioral representations of users than homogeneous sequences of high signal actions in isolation.
>
> 4. Semantic Feature Representation
>
> Semantic content features from foundation models complement traditional collaborative filtering (i.e. which users interacted with which items) signals. They are especially helpful in cold-start scenarios (e.g., new ads or advertisers with limited historical engagement data). By addressing this persistent challenge of recommendation systems, we improve overall signal coverage to a fundamental sparse problem in recommendation systems.
>
> The Impact of Multi-Stage Sequence Modeling
>
> The multi-stage sequence modeling architecture is delivering impact across three dimensions:
>
> Deeper User Representation
>
> By modeling thousands of user event sequences (e.g., clicks, views, and purchases) the offline model generates highly nuanced user representations. This depth of behavioral understanding improves ad relevance and conversion rates across Meta’s Family of Apps. Together with our broader modeling innovations, these sequence-derived representations drove a cumulative lift of 6% in conversions on Instagram, 3% on Facebook and 3.5% in ad clicks on Facebook.
>
> Scaling Efficiency
>
> The two-stage design delivers performance improvements with greater compute efficiency compared to hybrid approaches. Initial evaluations improved ads ranking quality with minimal impact to serving resources, confirming that model complexity and production efficiency can scale together.
>
> Platform Integration
>
> As a core part of GEM, this model architecture for sequence learning has been designed for generalization, where the same multi-stage backbone and scaling properties can extend to any ads ranking task with minimal adaptation and overhead.
>
> Current Work: Continued Scaling
>
> The sequence model scaling law shows no signs of saturation. With architectural parity achieved, scaling model complexity can draw on techniques proven in the LLM domain (e.g., mixture-of-experts, cross-user compute sharing, advanced attention mechanisms) with potential to continually scale at the optimal performance/efficiency tradeoff.
>
> Read the Paper
>
> A detailed technical publication of this model architecture and its scaling properties is available in our paper, “LLaTTE: Scaling Laws for Multi-Stage Sequence Modeling in Large-Scale Ads Recommendation.”
>
> The post From User Sequences to Scaling Laws: A Multi-Stage Architecture for Meta’s Ads Ranking appeared first on Engineering at Meta.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。