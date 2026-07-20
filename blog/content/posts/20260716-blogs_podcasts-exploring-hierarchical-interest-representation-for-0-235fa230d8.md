---
title: "Exploring Hierarchical Interest Representation For Meta Ads Deep Funnel Optimization"
date: 2026-07-16T07:15:32+08:00
draft: false
entry_kind: "auto"
tags: ["AI Research", "博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:a5e4fd4f73cf65c230d700a3e63e85fd99b03d4b192e53c2cf5dc277c3722c81"
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 84
description: "当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。"
external_url: https://engineering.fb.com/2026/07/15/ai-research/exploring-hierarchical-interest-representation-for-meta-ads-deep-funnel-optimization
observation_id: obs_235fa230d8103318ceecd98d1c0f446430e16476bd14eb2cb5167b58203f331f
revision_id: rev_28761c53811b6d766c4e53e9c323ce4b3a0de7d528b79b3572fb62097738894f
event_id: evt_c8cf05ac47d250b0a92749ac7989b693f1be538a428146224a2b0800b26761a7
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-15T23:17:25Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://engineering.fb.com/2026/07/15/ai-research/exploring-hierarchical-interest-representation-for-meta-ads-deep-funnel-optimization](https://engineering.fb.com/2026/07/15/ai-research/exploring-hierarchical-interest-representation-for-meta-ads-deep-funnel-optimization)

## 来源摘要/节选

> Hierarchical Interest Representation is a research area for Meta Ads. We’re exploring an upstream representation layer over the universe of Ads entities – users, advertisers, products, services – learning unified embeddings that connect users’ inferred interests with the breadth of what advertisers offer in their deep funnel ads.
>
> The innovations in Hierarchical Interest Representation are an in-house transformer based graph learning with bias-aware attention and self-supervised cross-view distillation, learning multi-hierarchical interest representations across a large graph.
>
> Hierarchical Interest Representation blends real-world knowledge with engagement signals – multimodal advertiser and product content processed through LLMs enriches sparse interactions, enabling generalization to rare and unseen entities.
>
> Hierarchical Interest Representation outputs universal embeddings for ads entities and Bag-of-Meaning interest tokens that have the potential to power new personalization, retrieval, supervision, and specialized ranking architectures across the ads stack.
>
> Trained end-to-end on real Meta ads data at the scale of billions of interactions.
>
> Hierarchical Interest Representation is an upstream representation layer designed to improve upon Meta’s deep funnel ranking optimization. It aims to connect businesses with the population of people on our platforms who carry the most genuine, latent interest in what they offer. The system is intended to function across Meta’s broader recommendation ecosystem, such as Meta’s Generative Ads Model (GEM), Andromeda, and the Adaptive Ranking Model, to advance deep funnel optimization.
>
> People come to Meta’s apps and platforms to connect with people and content, expressing preference with every scroll. Engagement signals are used to understand both inferred and explicit interests and improve relevance of content across our platforms. Utilizing frontier AI to map latent interests from sparse engagement signals and aligning them with the vast landscape of advertiser offerings is a transformative approach to addressing the challenges of signal scarcity and driving up deep funnel ad performance.
>
> The mission is to strengthen reasoning relationships throughout the landscape of ads entities – spanning users, businesses, and products – utilizing multi-hierarchical granularities that allow our models to navigate between stable, high-level interest anchors and the specialized, sparse signals of deep funnel intent.
>
> How Hierarchical Interest Representation Enhances Deep Funnel Optimization
>
> Hierarchical Interest Representation pioneers a structural shift in representation modeling by navigating long-range graph topologies and distilling sparse engagement signals into unified interest clusters at various granularities. By fusing real-world knowledge with a semantic grasp of advertised products, it effectively strengthens the connection between ads and user intents.
>
> Hierarchical Interest Representation encourages discovery-oriented ad experiences by extracting stable interest anchors from massive engagement datasets and grounding them in multi-modal world knowledge enrichment. This aims to enable the delivery of more relevant ad content to optimize deep funnel ads.
>
> The Technical Challenges
>
> User engagement with ads entities is naturally graph-structured: users and ads entities (advertisers, products, services, campaigns etc.) are nodes, and the activities and events connecting them are edges. At Meta’s scale, this is one of the largest graph networks in the industry. Learning the interest representation bears the following challenges:
>
> User Inferred Signal Dynamics
>
> Meta provides users with tools to help tailor their experiences, like providing ‘Interested/Not interested’ feedback on posts they see. In addition, inferred interests based on engagement signals continue to play an important role for improving deep funnel ads.
>
> Large Networks With Sparse Connections:
>
> Every month, Meta’s ads network serves millions of ads, from millions of advertisers, to billions of people across our platforms. While this “vocabulary” is large, ad impression opportunities are limited and deep funnel user feedback is scarce.
>
> Long-Range, Global Relationships
>
> Given the sparsity of the individual connections in the deep funnel, it is useful to observe common patterns from long range, graph connected entities and users and encode into representation. Capturing long-range relationships within large graph networks is computationally demanding. Even as hardware capabilities scale, the pursuit of modeling accuracy necessitates the design of memory-efficient attention kernels and high-performance learning algorithms.
>
> Introducing Hierarchical Interest Representation
>
> Our latest research area is an upstream representation layer for learning universal, relational knowledge representations of users and ads entities. The representations capture users’ ads engagement patterns, absorb real-world world semantics, and cascade through multiple hierarchical granularities into latent-space projections at each level. Based on the graph data structure, four design properties drive the system end to end:
>
> Dimension Reduction
>
> Hierarchical Interest Representation projects a raw graph into a configurable super-graph where each super-node is a learned latent interest primitive. User-ad edges that are sparse at the raw graph become meaningfully denser at the primitive interest graph. Inherently, the primitive interest graph is more stationary and stable in vocabulary, even though the ads business is more dynamic.
>
> Knowledge Enrichment
>
> Hierarchical Interest Representation enriches heterogeneous entities, in particular advertiser and product types, with multimodal content features such as text, images, and video. These features are pulled from structured page metadata and advertiser catalog attributes and processed through vision or language models. This extra information complements existing engagement data. Instead of just knowing how users interact with something, it captures what that thing actually is. Even for entities it hasn’t seen before it understands the underlying businesses and products.
>
> Unified Relational Representation
>
> Hierarchical Interest Representation learns thorough knowledge representation for users and entities, together with their latent interest primitives representation in a single metric space. It can infer entities’ mutual relationship and affinities across or within types. Using embedding operations, Hierarchical Interest Representation can determine primitive-to-primitive and cluster-to-cluster relationships. It can also estimate user proximity to interest primitives; how closely an ad/advertiser serves certain interest primitives; and what are the similar users, ads, and products that are closest neighbors.
>
> Multi-Hierarchical Granularities
>
> Given the overall sparsity of deep funnel information, there is a trade-off on how to project into primitive interests. Dense and stable relationships usually imply a coarser and higher-level abstraction, while sparse and specific connection looks at finer level of abstraction. Hierarchical Interest Representation learns super graphs, which cascade through multiple hierarchical layers for this flexibility, accommodating ranking modeling architecture, personalization, or retrieval applications.
>
> The Hierarchical Interest Representation Architecture
>
> Hierarchical Interest Representation builds representations by combining world knowledge of advertisers and products with user direct temporal engagement data. Its LLM-inspired transformer architecture is applied to large-scale graphs, using sparse attention to capture long-range relationships. The system is designed to power various applications across the ads platform from retrieval to final stage ranking.
>
> The following sections detail the architectural design of each component within the Hierarchical Interest Representation system.
>
> Enriched Engagement Graph
>
> Heterogenous Graph Structure
>
> Hierarchical Interest Representation is built on a typed, weighted, time-decayed graph that unifies multiple entity types – users, ads, advertisers, campaigns, products, and pixels. These entities are connected by typed engagement edges including businesses creating ads artifacts and the users-ads interaction journey. Each edge carries its action type and timestamp that balances recency intent against long-term interest. This typed, heterogeneous structure is what lets a single downstream representation reason about someone’s lifestyle, an advertiser’s catalog reach, and the products that connect them – all in one unified space.
>
> Scaling to Meta Production Data
>
> The graph spans billions of users, entities and their interactions on a monthly basis, served both online for production freshness and offline for evaluation and rapid iteration. Each node carries rich initial embeddings fusing pretrained semantic features with behavioral statistics. Frequent nodes add a learnable ID embedding via deep hash embeddings, a small shared neural network applied to a vector of hashes of the node ID, keeping ID memory bounded as the vocabulary scales to tens of billions.
>
> Hierarchical Encoder
>
> A transformer based hierarchical encoder is our modeling design to scale the representation learning at this gigantic graph size. It has considered several significant technical designs.
>
> World Knowledge
>
> World knowledge serves as a means to connect the dots given, which is abundant on relatively stationary entities, such as advertisers, products, etc. We retrieve the multimodal information in summary text, images, and video and process it through a customized LLM inference engine that produces encoded feature inputs for our representation learning.
>
> Structure Encoders
>
> The hierarchical encoder’s input layer combines rich complementary encoders. A node encoder fuses node-type, deep-hash-controlled node-ID, world knowledge features, and per-type metadata/features so each node enters the learning model with both its semantic identity and its real-world content. A position encoder applies position encoding over the sampled view from the graph to inject local topology with random walk, importance-prioritized strategies. An edge encoder prepares edge type, edge weight and temporal signals to flow into the attention learning mechanism.
>
> Bias Composition
>
> Transformers measure pairwise relationships between tokens through attention. Graphs, by construction, encode pairwise relationships between nodes. These two ideas naturally complement one another. Graph-structural signals (such as node-type transitions along event edges and shortest-path distance for local connectivity) enter the model as attention biases that augment the query-key dot product in every layer.
>
> This is what makes the model topology-aware. Rather than treating a subgraph as a bag of nodes, the Hierarchical Encoder attends with explicit knowledge of how nodes are structurally related, capturing long-range relationships that standard message-passing tends to over-smooth.
>
> Attention Kernel
>
> Adding graph-structural bias to attention is normally expensive: the standard implementation materializes a full pairwise bias matrix, forcing a fallback from memory-efficient attention. We adopt FlexAttention, which computes each bias term on the fly so the pairwise matrix is never materialized. Variable-length subgraphs are packed into a single block-masked sequence, avoiding padding waste and cross-graph leakage. New bias terms slot in as small scoring rules, no low-level kernel work needed. The result is memory-efficient attention with full graph-structural awareness.
>
> Training the Hierarchical Encoder
>
> Cross-View Distillation
>
> The Hierarchical Encoder is trained with self-supervision through a paired teacher-student scheme. For each anchor node, we sample a broad teacher view and a narrow student view, both passing through the Hierarchical Encoder. The student is trained to predict the same interest cluster as the teacher. Because the teacher sees a broader view of the graph, its prediction is more confident, giving the student a clear target to match. This extends supervision well beyond the small fraction of users who produce deep-funnel conversions, addressing much of the engagement sparsity that motivated Hierarchical Interest Representation. Sinkhorn-Knopp balanced assignment prevents single-cluster collapse, a known failure mode of self-supervised methods.
>
> Engagement Prediction
>
> Self-distillation discovers the latent interest primitives of the graph by teaching the model that different views of the same node should cluster together. Engagement prediction adds to the complementary supervised objective – given two node representations, an engagement type, and a time, predict whether a real engagement edge exists at that time. Together, they give Hierarchical Interest Representation both view-invariant structural priors and direct grounding in observed user behavior, turning it into a general-purpose scoring function across the delivery stack.
>
> Online Graph Infrastructure
>
> The raw heterogeneous graph lives on Meta’s online graph engine. The same data source powers both training and online serving, ensuring the same distribution across both. For training, subgraph fetches and node-feature reads are pipelined with GPU compute. Multiple workers prepare upcoming batches in parallel while the model trains on the current one, hiding data-loading latency behind the forward and backward passes. During the testing phase, this achieved a 30x wall-clock speedup over the synchronous baseline and kept GPU model FLOPs utilization high. Bit-exact reproducibility is preserved end to end, so infrastructure migrations and checkpoint recovery never silently shift model behavior.
>
> Causality
>
> To prevent information leakage, training and evaluation strictly respect the temporal order of events. The graph engine applies a cutoff timestamp on each call and masks any node or edge dated after that point.
>
> Edges are split chronologically into train, validation, and test windows. Batches are shuffled only within fixed time chunks, giving the optimizer gradient diversity without crossing temporal boundaries. The model only learns from information that would have been available at the time, so accuracy gains reflect real learning rather than future leakage.
>
> Tokenization
>
> Bag-of-Meaning Tokens
>
> Continuous universal embeddings are powerful for ranking, but they are not naturally suited for inverted-index retrieval, set aggregation, or human interpretation. We discretize them into Bag-of-Meaning (BoM) tokens – a compact, unordered vocabulary of interest concepts produced by composite quantization. A user is represented by the BoM tokens describing their interests. An ad or advertiser is represented by the BoM tokens of the interests they serve.
>
> Activating Hierarchical Interest Representation Across the Delivery Stack
>
> Hierarchical Interest Representation is designed to plug learned interest representations into the ads delivery stack to eventually improve deep funnel ranking across existing components such as GEM, Andromeda, and the Adaptive Ranking Model. For example, BoM tokens augment engagement-based personalization and supervision with user latent interest, and enable fast, compact recall for retrieval with inverted index lookup. Hierarchical Interest Representation’s multi-hierarchical structure supports specialized architectures, such as Mixture of Experts generative distribution learning routed by super-interest categories, and enables hierarchical reasoning over stable interest anchors for user-ad affinity.
>
> The Future of Hierarchical Interest Representation
>
> We will continue to advance training scaling efficiency, embedding freshness, knowledge compression, and memory-efficient attention kernels for greater representational expressiveness. We are also investigating parameter-efficient, objective conditional fine-tuning of the upstream Hierarchical Interest Representation, enabling segment-level specialization for heterogeneous deep funnel optimization objectives on top of a shared encoder.
>
> Acknowledgements
>
> We would like to thank Sammy Bald, Shaoqing Yuan, Chuan Hu, Chris Hayduk, Wenfan Xu, Liang Xu, Piyush Dak, Ikuhiro Ihara, Ashish Kalbhor, Manjari Jha, Priya Krishnamurthy, Xulei Liu, JC Lyu, Yuqi Bi, Vivek Bitla, Krishna Poola, Jiayin Ge, Santanu Kolay, Matt Steiner, Sandeep Pandey, Gunjit Singh, Marvin Kim and the entire team behind the development and production of the Hierarchical Interest Representation Project.
>
> The post Exploring Hierarchical Interest Representation For Meta Ads Deep Funnel Optimization appeared first on Engineering at Meta.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。