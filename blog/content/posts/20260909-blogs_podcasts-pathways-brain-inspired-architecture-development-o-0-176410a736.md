---
title: "Pathway’s brain-inspired architecture development on Amazon SageMaker HyperPod"
date: 2026-09-09T05:53:53+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "生成式 AI", "机器学习", "深度学习", "自然语言处理", "Amazon SageMaker HyperPod", "Announcements"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:3b6f9c05a5652edd85204214a1aeb91165470cd4240de2129e842388450490a5"
source_payload_sha256: "sha256:4761d4b05788f360f4a82897a8c873b47784e1c91ec003c3464eb88b02c3b610"
observation_id: obs_176410a7368dfb07faa1294ad8c0da3182dc7d94ba7d99917f06290dfc2a0776
event_id: evt_5442deeb992708d08b5843d3b3fc1a0108a9b4e10e6337950cb7a7de12f1f9dc
revision_id: rev_720fb75f8168ec4599c68cfb676458ebbd8f6b9b4d6d3a8a975e88bb58ddf230
source_published_at: 2026-09-08T19:12:51Z
first_seen_at: 2026-09-08T22:04:05Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 78
interpretation_sha256: "sha256:a7668978c491a512c41cbc795b38eb7793bed0eeb0776cc53383100a13f8769e"
description: "这是一篇关于 Pathway 公司开发的新型脑启发式人工智能架构的报道。该架构采用不同于传统 transformer 的设计，通过在潜在空间中进行循环推理来实现智能处理，模仿大脑中神经元通过稀疏局部交互和突触状连接来维持状态的方式。"
external_url: https://aws.amazon.com/blogs/machine-learning/pathways-brain-inspired-architecture-development-on-amazon-sagemaker-hyperpod
parent_observation_id: null
last_seen_at: 2026-09-10T00:00:00Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/pathways-brain-inspired-architecture-development-on-amazon-sagemaker-hyperpod](https://aws.amazon.com/blogs/machine-learning/pathways-brain-inspired-architecture-development-on-amazon-sagemaker-hyperpod)
- **发布域名**: aws.amazon.com

## 要点解读

### 这是什么

这是一篇关于 Pathway 公司开发的新型脑启发式人工智能架构的报道。该架构采用不同于传统 transformer 的设计，通过在潜在空间中进行循环推理来实现智能处理，模仿大脑中神经元通过稀疏局部交互和突触状连接来维持状态的方式。

### 用在哪里

该架构适用于需要处理长序列、避免上下文长度限制以及对推理效率有较高要求的场景。由于其稀疏激活特性和线性注意力机制，适合在资源受限或需要高并发推理的生产环境中部署，对于希望突破 transformer 架构固有效率瓶颈的 AI 研究者和工程师具有参考价值。

### 可以推断的

推测：该架构的提出反映了当前人工智能领域对更高效推理方式的探索方向，即从依赖增加计算量的方式转向通过架构创新提升单位算力的智能水平。

推测：基于 Hebbian 学习原理的设计表明，该方法可能更适合需要持续学习和知识更新的应用场景，而非一次性训练后保持静态的模型部署方式。

## 来源摘要/节选

> As AI systems take on more complex tasks, much of the industry’s progress has come from increasing model scale, training data, context length, and inference-time computation. Instead of externalizing reasoning work as a chain-of-thought (generating extra tokens sequentially and feeding them back into later steps), Pathway’s brain-inspired BDH (Dragon Hatchling) performs reasoning in latent space. It learns from examples and refines a solution without generating an intermediate text trace. BDH moves beyond the transformer paradigm by offering a brain-inspired architecture, originally formulated as a graph of neurons that communicate through sparse, local interactions and maintain state in synapse-like connections. The model states adapt in context without test-time weight updates, and the reasoning horizon isn’t limited by a fixed-size context window or tied to a flood of inefficient chain-of-thought tokens.
>
> Large language models (LLMs) have transformed AI, changing how we approach tasks from code generation to creative writing. However, fundamental questions remain about general intelligence and their ability to reason over long time periods in a coherent way. Their architecture, kept roughly static for the past 10 years, still presents important inefficiencies both in training and inference. LLMs tend to forget during long interactions, they don’t keep knowledge between sessions, and they need to be retrained to acquire new knowledge. Pathway’s BDH-CQ updates the model’s internal memory during inference by performing iterative computation inside a recurrent latent state and decoding only its candidate answers. Models can work through a new problem without generating long, verbalized reasoning traces, and without requiring fine-tuning or retraining.
>
> Pathway’s BDH integrates with well-known frameworks such as PyTorch and uses Amazon SageMaker HyperPod to scale out their training. Amazon SageMaker HyperPod helps their applied AI scientists share compute resources in a resilient, scalable, and cost-effective way.
>
> Transformers: architecture and fundamental limitations
>
> The transformer architecture, while widely adopted for natural language processing (NLP), faces significant limitations in both training and inference workloads.
>
> During training, transformers struggle with systematic generalization beyond their training data, particularly for long chain-of-thought reasoning tasks, and require massive amounts of data and computational effort to compensate for this limitation. The transformer architecture’s dense computation patterns and full back-propagation requirements lead to substantial computational costs that scale exponentially with model size. There’s a lack of clear connections between the dynamics at the micro-scale (that is, neuron activations) and macro-behavior (that is, why the model answers what it does). It’s difficult to efficiently update its knowledge without full retraining or fine-tuning, because transformers often struggle with catastrophic forgetting, where learning something new leads to forgetting something else.
>
> At inference, transformers face other inefficiencies: the structure of their attention mechanism limits scalability, while their dense activation patterns, even with Mixture of Experts techniques, result in excessive computation and memory bandwidth usage. The fixed context window and growing KV-cache enforce limitations on sequence length processing. Furthermore, the closed-source nature of the transformer state makes it nearly impossible to interpret or monitor the model’s reasoning process, raising concerns about reliability and safety in production environments and heavily regulated industries.
>
> These challenges are fundamentally tied to the architecture’s design choices rather than only implementation details, suggesting the need for alternative approaches that better align with both computational efficiency and natural intelligence principles.
>
> “Today’s AI pays a steep token cost for reasoning, but that cost is imposed by architecture, not by any law of intelligence. Currently, every reasoning step consumes context, adds latency, and burns compute. We show that a different architecture changes the game and opens up a whole new space in terms of how much intelligence per dollar. A 150M-parameter model, built on Pathway’s BDH architecture, reasons recurrently in latent space, and sets a new state of the art in cost efficiency on ARC-AGI-1. The bottleneck was never intelligence. It was design.”
>
> — Zuzanna Stamirowska, CEO and co-founder, Pathway
>
> BDH: A unified architecture for artificial and natural intelligence
>
> Pathway’s vision is to fundamentally change the way models think. Their BDH architecture is a post-transformer model that continually learns, evolves, and reasons. BDH’s architecture represents a new way to build language models that reformulates sequence modeling as local graph dynamics on a network of interacting neuron particles. The model employs Hebbian learning, the principle that “neurons that fire together, wire together”, to implement attention mechanisms. This approach scales in a single neuron dimension (n), which reduces the complexity of distributing across compute resources that we face when deploying transformers.
>
> As in the brain, the interactions of BDH are defined to be sparse and local, and the connections between the neurons encode the memory and reasoning functions. This sparse activation profile (only 5 percent of neurons are typically active at a given time) supports efficient computation. The reduced active state means less computation is required per inference step, leading to performance improvements in production environments.
>
> BDH implements attention through a linear mechanism that operates on fixed, high-dimensional states without incurring the increased complexity characteristic of transformer models for long contexts. This allows the model to process longer sequences more efficiently, without the context length limitations of transformer architectures. The model’s states are directly mapped to synaptic connections between neuron pairs, providing visibility into the reasoning process and making the model’s decision-making easier to interpret.
>
> Recently, Pathway built BDH-CQ, a reasoning system built on top of BDH. It extends BDH with in-context learning and latent iterative reasoning for visual problem-solving.
>
> As the following sections show, BDH-CQ excels at in-context learning. Its recurrent computations over latent states support efficient parallel hypothesis exploration, where communities of neurons can represent different candidate solutions for a problem at hand. The model achieves a reasoning efficiency which can process arbitrary numbers of demonstrations at fixed memory cost.
>
> “Customers are increasingly exploring how to move advanced reasoning from experimentation into production, where performance, efficiency, and scalability all matter. Pathway’s work training BDH-CQ on Amazon SageMaker HyperPod points to a promising path toward deploying high-performing systems more cost-effectively at scale.”
>
> — Nicolas Tarducci, Head of Solution Architecture for Startups EMEA, Amazon Web Services
>
> Developing BDH architecture on Amazon SageMaker HyperPod
>
> Pathway uses Amazon SageMaker HyperPod for developing its BDH architecture. Amazon SageMaker HyperPod is a purpose-built infrastructure solution for training LLMs and foundation models (FMs) that require distributed training or inference across hundreds or thousands of GPUs. It provides a fully managed, high-performance machine learning (ML) training environment with automated cluster provisioning, optimized networking fabric, and customizable software stacks. For model producers, Amazon SageMaker HyperPod delivers three key benefits: reduced time-to-market by removing complex infrastructure setup and management, improved cost efficiency through automatic scaling, and enhanced model performance through specialized networking architecture that achieves near-linear scaling across GPU clusters. This helps ML teams focus on model development rather than infrastructure challenges while achieving faster training times and lower costs compared to traditional infrastructure approaches.
>
> For Pathway to develop AI architectures beyond transformers, comprehensive observability of their training infrastructure is critical. Amazon SageMaker HyperPod integration with advanced monitoring tools, such as Amazon Managed Service for Prometheus, provides the deep insights needed for these workloads. The combination of visualization, metrics collection, and proactive optimization capabilities using Amazon Managed Grafana dashboards, allows Pathway to visualize complex distributed training patterns, monitor GPU utilization and memory patterns, and track inter-node communication efficiency for their parallel training approaches.
>
> This comprehensive observability stack helps reduce development cycles when iterating on new architectural approaches, optimizes cost-performance ratio for resource-intensive training, and ensures reliability and reproducibility of results across training runs. For more information about this integration, and quick ways to deploy this observability stack, see the awsome-distributed-ai repository or the Amazon SageMaker HyperPod documentation.
>
> Amazon Elastic Fabric Adapter (EFA) integrates natively with the NVIDIA CUDA platform for GPU-accelerated computation and the NVIDIA Collective Communications Library (NCCL) for communication across GPUs. It allows distributing data, weights, activations, and more, in a reliable and scalable fashion. Pathway used Amazon Elastic Compute Cloud (Amazon EC2) p5en.48xlarge instances, which have up to 3200 Gbps of network performance per instance and NVIDIA’s accelerated AI infrastructure powered by NVIDIA H200 GPUs. All instances were interconnected using EFA and operated on an Amazon EC2 UltraCluster to reduce the network distance between GPUs and lower latency.
>
> Proof of BDH architecture: BDH-CQ achieving 29.2% pass@2 on ARC-AGI
>
> BDH-CQ achieved 29.2 percent pass@2 on the ARC-AGI benchmark at a cost of US $0.0007 per task.
>
> Thanks to Pathway’s new approach to reasoning, in-context task acquisition and iterative latent computation, BDH-CQ changed the cost-accuracy Pareto frontier on the ARC-AGI-1 benchmark, as of August 2026.
>
> ARC-AGI-1 presents an AI system with a small number of before-and-after examples that illustrate an unknown visual rule. The system must then infer that rule and apply it to a new grid, a capability often associated with human-like intelligence. BDH-CQ performs iterative computation inside a recurrent latent state and decodes only its candidate answers. Compared to transformers, which externalize their work as a chain-of-thought and increase latency and inference cost, BDH-CQ updates its model’s internal memory while examples are processed. It works through new problems without generating a long, verbalized reasoning trace.
>
> The pattern that ARC-AGI explores resembles real-world challenges where systems must reason reliably as information and constraints change, such as investigating cyber security incidents, coordinating transportation networks, responding to real-time industrial operations, and operating autonomous agents across long-running workflows. BDH-CQ’s new approach shows it can make these applications less costly, more responsive, and more reliable.
>
> Conclusion
>
> BDH is a new large language model architecture inspired by scale-free biological networks. It draws on principles biology got right, namely local interaction, sparse activity, persistent state, and continual adjustment, and applies them to a modern sequence model. It offers a GPU-friendly implementation. BDH provides a post-transformer architecture built around recurrent memory and local computation. BDH-CQ extends it into a reasoning system that learns from context and performs iterative computation in a continuous latent workspace, which supports efficient reasoning beyond token-by-token generation.
>
> To begin exploring and implementing the BDH architecture, you can access detailed technical documentation and a sample implementation through Pathway’s repositories. The implementation supports standard PyTorch workflows and can be readily integrated into existing ML pipelines.
>
> Teams that push the boundaries of AI model development can use Amazon SageMaker HyperPod to maintain efficiency and reliability at scale. Amazon SageMaker HyperPod training offers a robust solution to common challenges in large model training. To learn more about Amazon SageMaker HyperPod, go to the AI on SageMaker HyperPod and find workshops, code examples, and troubleshooting guides. Or read about Checkpointless training on Amazon SageMaker HyperPod to learn about its resilience features.
>
> About the authors
>
> Paulo Aragão
>
> Paulo is a Principal WW Specialist Solutions Architect focused on helping customers build their Frontier AI strategy on AWS. With over 20 years of experience dealing with High Performance Computing and AIML projects, he is passionate about working backwards from customer’s challenges and helping overcome them. To know more about his projects, go to his GitHub page.
>
> Rodrigo Merino
>
> Rodrigo is a Generative AI Solutions Architect Manager at AWS. With over a decade of experience deploying emerging technologies, from IoT to GenAI, Rodrigo guides customers to accelerate their AI/ML and generative AI journeys. He specializes in helping organizations train and build models on AWS, as well as operationalize end-to-end ML solutions. Rodrigo’s expertise lies in bridging the gap between cutting-edge technology and practical business applications, enabling companies to harness the full potential of AI.
>
> Ludovic Arnould
>
> Ludovic is a Frontier AI Model Solutions Architect at Pathway, specializing in the design and deployment of advanced AI solutions for enterprise customers. He holds a PhD in Machine Learning from Sorbonne Université and has published research at ICML, ICLR, and AISTATS. His experience spans deep learning, multimodal AI, large language and vision models, with a track record of taking research prototypes through to production-ready systems.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。