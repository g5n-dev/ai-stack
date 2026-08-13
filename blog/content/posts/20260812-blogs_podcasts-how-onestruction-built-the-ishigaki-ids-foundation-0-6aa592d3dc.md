---
title: "How ONESTRUCTION built the Ishigaki-IDS foundation model with AWS GenAIIC"
date: 2026-08-12T02:09:57+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "生成式 AI", "机器学习", "深度学习", "Amazon EC2", "AWS ParallelCluster", "Customer Solutions"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:68245e39b9dc9862b975a9b44d316fca1ea378c427f686499f253fbd90c38270"
source_payload_sha256: "sha256:809fae2a0722ce79a1c2054ca8aef66f3f9db828774e79cff4c1cf4ab61745ac"
observation_id: obs_6aa592d3dc7a40084fc26ef49c0a2a4849efce3311e7000757ceedd84f35c52d
event_id: evt_941bb1a077c2a0e05699bd13e9e9b65fc8aac6eea350685737f8f9fdf1bd0670
revision_id: rev_6d39aaca0b01dd76153863c688c033631d2e73f9b4f2d63de5f5d1bf46beafaf
source_published_at: 2026-08-11T16:14:33Z
first_seen_at: 2026-08-11T18:20:19Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 73
interpretation_sha256: "sha256:14d0dd8d0dbbd2f764273113d155ecfd3d0911f63edfe47350e1f7336a5a187f"
description: "本文描述了一家建筑科技初创公司如何在数据稀缺的 BIM 领域，利用合成数据和三阶段训练（持续预训练、监督微调、强化学习）构建面向信息交付规范（IDS）的领域专用基础模型，并借助可验证奖励提升输出质量。"
external_url: https://aws.amazon.com/blogs/machine-learning/how-onestruction-built-the-ishigaki-ids-foundation-model-with-aws-genaiic
parent_observation_id: null
last_seen_at: 2026-08-13T00:00:00Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/how-onestruction-built-the-ishigaki-ids-foundation-model-with-aws-genaiic](https://aws.amazon.com/blogs/machine-learning/how-onestruction-built-the-ishigaki-ids-foundation-model-with-aws-genaiic)
- **发布域名**: aws.amazon.com

## 要点解读

### 这是什么
本文描述了一家建筑科技初创公司如何在数据稀缺的 BIM 领域，利用合成数据和三阶段训练（持续预训练、监督微调、强化学习）构建面向信息交付规范（IDS）的领域专用基础模型，并借助可验证奖励提升输出质量。

### 用在哪里
适用于机器学习工程师在少数据场景下进行领域适配的技术选型参考，以及建筑、BIM 从业者了解 AI 如何降低行业学习门槛的实践案例。

### 可以推断的
推测：利用内部专家生成大规模合成数据可缓解专业领域训练语料稀缺的问题。  
推测：在结构化输出任务中，使用标准合规检查工具提供可验证奖励，有助于提升模型对 IDS 规范的遵循度。

## 来源摘要/节选

> This post was co-written by ONESTRUCTION, Inc. and Amazon Web Services Japan G.K. as part of GENIAC (Generative AI Accelerator Challenge) Phase 3, with technical advisory from the AWS Generative AI Innovation Center (GenAIIC).
>
> Building domain-specialized foundation models in data-scarce fields is hard. You need enough training data, specialized knowledge, and ways to verify your outputs.
>
> ONESTRUCTION, Inc. is a construction technology startup that solves industry problems through openBIM. With technical advisory from GenAIIC, the company built Ishigaki-IDS, a foundation model (FM) specialized for construction industry BIM (Building Information Modeling) workflows. BIM is a digital representation of a building’s physical and functional characteristics, used across the construction lifecycle.
>
> Japan’s construction sector faces a persistent labor shortage. BIM is promoted at the national level because it lets design, construction, and maintenance teams share information in one place. But adopting BIM requires specialist knowledge, and that learning cost has slowed wider use. A good example is IDS (Information Delivery Specifications), an XML-based standard that defines the information attached to and validated against a BIM model (an IFC (Industry Foundation Classes) model). Authoring an IDS file takes fluency in its grammar plus knowledge of IFC and its rules. Ishigaki-IDS lowers that barrier so practitioners who aren’t BIM specialists can review and manage attribute information.
>
> This post is an architectural case study of how ONESTRUCTION built Ishigaki-IDS. If you’re a machine learning (ML) engineer working on domain adaptation, or a technical leader weighing how to build specialized AI models where data is scarce, you will find a pattern you can reuse. Construction and BIM professionals will also see what AI can do in their field. Familiarity with foundation model training (pre-training and fine-tuning) and basic AWS compute concepts helps, but it isn’t required.
>
> You will learn:
>
> How to use synthetic data generation to overcome data scarcity in niche domains.
>
> How to build a three-stage training pipeline (CPT, SFT, RLVR) for domain specialization.
>
> How to use verifiable rewards for structured output generation.
>
> How to run distributed training on Amazon Elastic Compute Cloud (Amazon EC2) P5en instances with AWS ParallelCluster.
>
> Three challenges in building an IDS foundation model
>
> Three problems stood between us and a working IDS model.
>
> The first was data scarcity. IDS is a relatively new standard, published in 2024, and construction in general is a domain with limited public web content. Many other domains such as finance, healthcare, and law train models on corpora of billions to hundreds of billions of tokens, but no comparable public dataset exists for IDS. Even after collecting recent web data, the volume was small and the depth was shallow, which meant the model couldn’t pick up enough context about IDS and related topics from data alone.
>
> The second was injecting an IFC vocabulary of several thousand terms. For example, “beam” maps to IfcBeam and “air conditioner” maps to IfcUnitaryEquipment. This mapping has historically been done by hand by domain experts, and we needed the model to learn it directly.
>
> The third was IDS-specific grammar. IDS is more than plain XML: its tag structure changes depending on what information is being attached or validated, and authors must use repeated patterns and dedicated tags. General-purpose foundation models struggle to produce this structure with accuracy.
>
> Solution
>
> Our approach combined three ingredients: a multi-stage training pipeline, close collaboration with domain experts, and infrastructure built for stable distributed training. We start with the training pipeline.
>
> Three-stage training pipeline
>
> We built Ishigaki-IDS on top of Qwen3 (8B / 14B / 32B), an open-source large language model (LLM) from Alibaba Cloud known for strong multilingual capabilities and a wide range of parameter sizes. With the size range, we can experiment at smaller scales before committing to full training runs at 32B. We applied a three-stage training pipeline.
>
> First, in continued pre-training (CPT), we injected IDS and IFC domain knowledge using web corpora plus synthetic data created with our internal domain experts. We generated valid IDS files at scale and built synthetic datasets that explained IDS-related documents from multiple angles, with synthetic data covering most of the training corpus.
>
> Second, in supervised fine-tuning (SFT), we trained the model on pairs of IDS authoring instructions (in CSV or natural language) and their expected IDS output. SFT alone left expected issues, such as plausible but incorrect XML tag choices and wrong attribute values, so we designed a third stage to address them.
>
> Third, in reinforcement learning with verifiable rewards (RLVR), we used IDS-Audit-Tool from buildingSMART, the international standards body, as the reward function. The tool checks XML well-formedness, IDS structural validity, and semantic consistency, so the model can iterate against mechanical correctness signals. RLVR fits the IDS task well because it refines output quality without large amounts of supervised data—useful for a data-poor domain.
>
> Technical advisory from GenAIIC
>
> We led development with our construction and BIM domain expertise and met with GenAIIC every two weeks for technical advisory. At each milestone, we brought training results and evaluation data to these sessions, and together we worked through five key areas:
>
> Training data design – synthetic data strategies for the IDS domain and how to balance the data mix across CPT, SFT, and RLVR stages.
>
> Evaluation benchmarks – metrics covering IFC and IDS knowledge, structured generation, and general dialogue ability.
>
> Training stages and techniques – refining CPT, SFT, and RLVR, including long-context handling, reward shaping, and structured generation.
>
> Training infrastructure – parallelization, throughput, and stability for distributed training.
>
> Result diagnosis – when issues appeared, diagnosing root causes and setting direction for the next iteration.
>
> Iterating on “what change improves IDS generation accuracy and practicality” at each cycle helped us build a domain-specialized foundation model in a niche, data-poor area within a short timeline.
>
> Architecture
>
> For the training infrastructure, we used Amazon EC2 P5en instances (two p5en.48xlarge nodes with NVIDIA H200 Tensor Core GPUs), orchestrated with AWS ParallelCluster. ParallelCluster is an open source tool that simplifies deploying and managing High Performance Computing (HPC) clusters on AWS. We stored training data, synthetic data, and checkpoints on Amazon FSx for Lustre, a fully managed file system optimized for compute-intensive workloads that delivers sub-millisecond latencies and high throughput. This setup gave us stable multi-node distributed training and parallel access to large datasets.
>
> Figure 1: Ishigaki-IDS training architecture using Amazon EC2 P5en instances orchestrated by AWS ParallelCluster with Amazon FSx for Lustre for high-throughput data access
>
> Evaluation
>
> We built our own evaluation benchmark, IDS-Bench, with our internal IDS specialists. IDS-Bench measures performance across IFC version, construction discipline (architecture, structure, MEP, and common), language (Japanese and English), and the Implement, Structure, and Content axes, so the scores reflect what the model needs to handle in real work.
>
> Results
>
> In our IDS-Bench evaluation, Ishigaki-IDS scored close to 100 percent on XML structural compliance and IDS structural compliance, and above 80 percent on IDS content consistency. General frontier models told a different story: they produced well-formed XML but scored under roughly 25 percent on IDS structural compliance and near 0 percent on IDS content consistency. IDS is a specialized and relatively new area, which is the kind of problem a domain-specialized model can solve. The model also supports context-length scaling with YaRN (Yet another RoPE extensioN). YaRN extends the context window of transformer models beyond their original training length without major performance degradation. We confirmed that the model generates correctly with inputs and outputs up to roughly 120k tokens.
>
> In a joint proof-of-concept with buildingSMART, both IDS specialists and non-specialists responded positively to using the model in their work and to its ability to produce the intended IDS even from ambiguous prompts. They also gave us a list of suggestions for further development, which reinforced our view that the model is useful in practice.
>
> Figure 2: IDS-Bench scores comparing Ishigaki-IDS variants against general frontier models across XML structure, IDS structure, and IDS content consistency
>
> Lessons learned
>
> Three takeaways from this project:
>
> Synthetic data quality matters more than quantity. Our domain experts’ involvement in synthetic data creation was the difference-maker for model performance. Volume alone wouldn’t have produced the same result.
>
> Verifiable rewards accelerate iteration. Using IDS-Audit-Tool as an automated reward signal let us iterate faster than manual evaluation would allow, especially in a data-poor setting.
>
> Stable infrastructure lets us experiment freely. Reliable distributed training on Amazon EC2 P5en, AWS ParallelCluster, and Amazon FSx for Lustre freed us to focus on model improvements rather than debugging cluster issues.
>
> Conclusion
>
> Combining domain expert collaboration, synthetic data, and RLVR tied to a verification tool worked well for building a domain-specialized model in a data-poor specialty area. Continuous technical advisory from GenAIIC helped us reach the accuracy targets measured on IDS-Bench within the GENIAC Phase 3 timeline. ONESTRUCTION will continue working with AWS to bring AI tools to the construction industry.
>
> Next steps
>
> If you’re interested in building domain-specialized foundation models for your industry, the following resources are a good place to start:
>
> Explore AWS GenAIIC – Learn how the AWS Generative AI Innovation Center supports generative AI projects with technical advisory and best practices.
>
> Get started with distributed training – See the AWS ParallelCluster User Guide to set up similar infrastructure.
>
> Try Ishigaki-IDS – Access the model on Hugging Face and run it against your own IDS scenarios.
>
> About the authors
>
> Koyo Hidaka
>
> Koyo is Manager of the AI Strategy Unit at ONESTRUCTION, where he leads in-house AI development, AI integration into the company’s products, and joint AI research with clients. He has recently started entrusting everyday decisions to AI agents. His favorite science fiction is Evangelion and Steins;Gate.
>
> Ryo Kanazawa
>
> Ryo is an AI Engineer in the AI Strategy Unit at ONESTRUCTION, working on foundation models for construction × AI. In GENIAC Cycle 3 he developed Ishigaki-IDS, the IDS-specialized model. He is a second-year master’s student at Tokyo University of Science. His favorite science fiction is Steins;Gate and The Three-Body Problem.
>
> Chenguang Wang
>
> Chenguang is an Applied Scientist at Amazon Web Services Japan. He provides technical support for training LLMs, VLMs, and MLMs and for deploying agents to enterprise customers across APJC.
>
> Dayuan Jiang
>
> Dayuan is a Senior Deep Learning Architect at Amazon Web Services Japan. With more than nine years of experience in AI and machine learning, he is skilled at applying data science in business settings—modeling real-world problems and interpreting data to solve them.
>
> Angie Wang
>
> Angie is a Senior Generative AI Strategist at Amazon Web Services Japan. She helps AWS customers from generative AI strategy through production deployment. With a background in computer science and venture capital, she bridges business strategy and technical implementation.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。