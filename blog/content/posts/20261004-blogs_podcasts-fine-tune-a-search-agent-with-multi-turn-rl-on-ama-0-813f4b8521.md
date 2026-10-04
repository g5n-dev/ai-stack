---
title: "Fine-tune a search agent with multi-turn RL on Amazon SageMaker AI"
date: 2026-10-04T01:18:56+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "RAG", "AI Agent", "机器学习", "Prompt 工程", "Advanced (300)", "Amazon SageMaker AI", "Technical How-to"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:f47d5a7970ac62ddcb21fabbbd2cafbc3407c8d715a87012d4692fed32932e0f"
source_payload_sha256: "sha256:c3930621fbbe36b19d4558f9ac76a168c1b0a183d405fda9060768401ff8659f"
observation_id: obs_813f4b8521bddb77fa640b7b64b035f4cfb1baa088ff76dbd5d50ef577520e78
event_id: evt_ddc51795d6b689694980f5d75e503035f51f77e9afa78ce8726d0fbc5601e6b3
revision_id: rev_05ba23c6b8179a611c8f01390987ae1cb8d7ee695027951c8ec93bae4527092e
source_published_at: 2026-10-02T15:44:20Z
first_seen_at: 2026-10-03T17:30:11Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 66
interpretation_sha256: "sha256:ab3e427786e23a054e5e64ce3a77999c07a8ec588a841fab9850b244b6c37aa2"
description: "该内容介绍如何通过多轮强化学习在云服务平台上微调搜索智能体，使小型语言模型能够自主决定搜索策略并在多轮交互中逐步优化检索行为。"
external_url: https://aws.amazon.com/blogs/machine-learning/fine-tune-a-search-agent-with-multi-turn-rl-on-amazon-sagemaker-ai
parent_observation_id: null
last_seen_at: 2026-10-04T00:00:00Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/fine-tune-a-search-agent-with-multi-turn-rl-on-amazon-sagemaker-ai](https://aws.amazon.com/blogs/machine-learning/fine-tune-a-search-agent-with-multi-turn-rl-on-amazon-sagemaker-ai)
- **发布域名**: aws.amazon.com

## 要点解读

### 这是什么

该内容介绍如何通过多轮强化学习在云服务平台上微调搜索智能体，使小型语言模型能够自主决定搜索策略并在多轮交互中逐步优化检索行为。

### 用在哪里

适用于需要构建企业级搜索智能体的技术团队，特别是那些受限于成本和延迟但又要求检索结果可靠性的应用场景。

### 可以推断的

推测：对于希望在实际业务中部署生成式搜索系统的开发者而言，这种方法提供了一种平衡性能和资源消耗的可行路径。

推测：多轮强化学习框架的模块化设计可能降低了对专业团队的依赖，使非深度学习专家也能参与智能体的定制和优化。

## 来源摘要/节选

> Search agents powered by large language models (LLMs) are transforming how enterprises retrieve information. Rather than requiring users to craft the perfect query, a search agent autonomously decides what to search for, which retrieval strategy to use, and when to stop searching. It does this across multiple rounds of interaction, refining its approach based on what it has already retrieved.
>
> However, getting this multi-step behavior to work well is hard. No base model arrives knowing your tools or your environment. Prompt a small model and you rarely get dependable multi-turn behavior. Prompt a frontier model and it often works, but you pay for that capability in latency and cost. Fine-tuning offers a third path: you teach a small model your tools and environment directly. The result is a small model’s speed and cost with the reliability that would otherwise require a frontier model.
>
> Even though fine-tuning is the natural next step, the traditional approaches each fall short. Supervised fine-tuning (SFT) depends on expert demonstrations of ideal multi-turn trajectories, which are costly to collect and usually don’t exist for your setup. Single-turn reinforcement learning (RL), such as RL with verifiable rewards (RLVR), scores one response at a time. But a search agent makes interdependent decisions across many turns, each one building on the context before it. Optimizing a single step in isolation misses those dependencies entirely.
>
> What you need is a training approach that optimizes the agent across the full multi-turn trajectory. The reward signal only needs to reflect whether the final outcome was good. That is exactly what multi-turn reinforcement learning (MTRL) provides. It trains the agent to make good decisions across a full sequence of steps, bakes in your environment-specific behavior, and gives you control over output quality. Because you run a smaller, specialized model, you also get faster, cheaper inference.
>
> In this post, we describe how we fine-tuned a search agent using Amazon SageMaker AI multi-turn reinforcement learning (MTRL) and share the results we observed in retrieval quality and reliability. We begin by explaining what Amazon SageMaker AI MTRL is and how it works.
>
> What is Amazon SageMaker AI MTRL?
>
> With Amazon SageMaker AI MTRL, you can fine-tune LLMs using reinforcement learning in multi-turn interaction settings. It frames an agentic task as a sequence of decisions, uses multi-turn rollouts to generate training data, and optimizes the model with policy gradient algorithms.
>
> Amazon SageMaker AI MTRL offers:
>
> Modular agent-environment interface: You keep integration low-code. You define custom rewards, custom tool loops, and multi-turn conversation shapes.
>
> Serverless execution: You get production-scale agentic RL at per-token pricing without provisioning or managing GPU clusters.
>
> Asynchronous rollout and trajectory collection: You run generation and gradient updates in parallel with bounded off-policy staleness, so training stays fast without drifting too far from the current policy.
>
> A native algorithm library: You choose from Proximal Policy Optimization (PPO), Clipped Importance Sampling Policy Optimization (CISPO), and importance-sampling (IS) losses, paired with group-based advantage estimators (GRPO, GRPO pass@k, RLOO, and more).
>
> Resumable training: You can split long training runs across multiple jobs to work beyond single-job time limits.
>
> Trajectory and reward observability: You can inspect what your agent did turn by turn and across training steps in MLflow managed by Amazon SageMaker AI.
>
> Evaluation jobs: You can report reward, pass@k, and trajectory metrics before deploying to an Amazon SageMaker AI endpoint or Amazon Bedrock.
>
> This makes MTRL a natural fit for search agents: you have a clear reward signal (retrieval quality), a multi-turn interaction loop (the agent issuing queries and receiving results), and a well-defined environment (the search tools).
>
> Environment and setup
>
> Our setup relied on the following:
>
> An AWS account with access to Amazon SageMaker AI in the US West (Oregon) AWS Region (us-west-2).
>
> Training and validation datasets uploaded to Amazon Simple Storage Service (Amazon S3) in the required format (see the MTRL documentation for details).
>
> A deployed agent endpoint that exposes BM25 and vector search tools for the MTRL environment to call during rollouts.
>
> Familiarity with Amazon SageMaker AI and Python.
>
> Solution overview
>
> In this post, we use Amazon SageMaker AI MTRL to fine-tune a Qwen3.6-27B model (supported in the US West (Oregon) Region (us-west-2)) for a search agent. The search agent is an LLM-powered system that autonomously uses search tools to find, gather, and synthesize information to answer a question or complete a task.
>
> We focus on an enterprise search setting where the agent has two tools available:
>
> Lexical search (BM25): Finds exact keyword matches by counting word frequencies. Best for queries with specific terms or identifiers.
>
> Vector search: Converts queries and documents into embedding vectors and computes similarities. This is recommended for semantic or conceptual queries.
>
> We also limit the number of turns (one turn is one round of user-assistant interaction), preventing the agent from generating excessively long responses and encouraging efficient search behavior.
>
> Training setup
>
> This section walks through the three key components of our training setup: the datasets, the reward function, and the MTRL job configuration.
>
> Datasets
>
> We use the following datasets for training and testing:
>
> Dataset
>
> Train/Test
>
> Public Link
>
> Description
>
> FRAMES
>
> Train
>
> HuggingFace
>
> Multi-hop factoid QA requiring synthesis across multiple Wikipedia articles.
>
> BRIGHT
>
> Train
>
> HuggingFace
>
> Reasoning-intensive retrieval across 12 domains, where relevance needs reasoning, not keyword overlap.
>
> Enterprise RAG
>
> Train
>
> GitHub
>
> A benchmark of over 500,000 synthetic enterprise documents and 500 questions for training and evaluating RAG systems on internal company knowledge
>
> ESCI
>
> Train
>
> GitHub
>
> A multilingual product-search dataset labeling query–product pairs as Exact, Substitute, Complement, or Irrelevant
>
> Musique
>
> Train
>
> GitHub
>
> A question-answering dataset built by composing single-hop questions into challenging multi-hop reasoning problems.
>
> MLQA
>
> Train
>
> HuggingFace
>
> A parallel extractive question-answering benchmark covering seven languages for evaluating cross-lingual comprehension.
>
> FreshStack
>
> Test
>
> HuggingFace
>
> Recent developer-tech Q&amp;A over Stack Overflow + docs for five topics.
>
> WixQA
>
> Test
>
> HuggingFace
>
> Help-center support QA over the Wix knowledge base.
>
> BrowseComp-Plus
>
> Test
>
> GitHub
>
> Hard deep-research queries over ~100K human-verified open-web documents.
>
> Wands
>
> Test
>
> HuggingFace
>
> A Wayfair product-search dataset containing over 42,000 query–product relevance judgments labeled as Exact, Partial, or Irrelevant.
>
> We preprocess the datasets into the format recognized by the MTRL service according to the documentation. We further reserve 5 percent of the training instances within each dataset as validation instances.
>
> Reward function
>
> Our main metric is nDCG@10 (Normalized Discounted Cumulative Gain at rank 10). nDCG@10 is a standard information retrieval metric that measures how well the top 10 retrieved documents match the ideal ranking. It rewards systems that place highly relevant documents near the top of the list, with a score of 1.0 meaning perfect ranking and 0.0 meaning no relevant documents retrieved. We use nDCG@10 directly as the reward function in MTRL. This is a trajectory-level reward where the agent completes its full multi-turn search, and the reward reflects how well the final retrieved documents match the ground truth.
>
> When the agent reaches the maximum number of turns or the maximum sampling tokens in a single turn, we assign a reward of -1 to explicitly teach the model to avoid these failure modes. This kind of penalty-based reward design is effective at steering the model away from undesirable behavior without needing to hand-craft complex intermediate rewards.
>
> MTRL job configuration
>
> One of the appeals of Amazon SageMaker AI MTRL is how little you need to configure to get going. We change three hyperparameters and leave everything else at the default values. The following code snippet shows how to configure and launch the training job using the MultiTurnRLTrainer SDK:
>
> from sagemaker.modules.train import MultiTurnRLTrainer
>
> trainer = MultiTurnRLTrainer(
>
> model_id="qwen3.6-27b",
>
> agent_endpoint="&lt;your-agent-endpoint&gt;",
>
> training_dataset_s3_uri="s3://amzn-s3-demo-bucket/datasets/train/",
>
> validation_dataset_s3_uri="s3://amzn-s3-demo-bucket/datasets/validation/",
>
> hyperparameters={
>
> "max_epochs": 1,
>
> "global_batch_size": 128,
>
> "rollout_max_concurrency": 32,
>
> },
>
> output_s3_uri="s3://amzn-s3-demo-bucket/output/",
>
> )
>
> trainer.train()
>
> The key hyperparameters we change are:
>
> max_epochs: 1 controls how many full passes over the training data.
>
> global_batch_size: 128 sets the number of prompts per training step.
>
> rollout_max_concurrency: 32 controls how many rollouts run in parallel during trajectory collection.
>
> That’s the whole setup. The choices that usually demand RL expertise, the algorithm, the advantage estimator, the off-policy staleness bounds, all run on defaults. Getting from the base model to the results in the next section required nothing more than the preceding configuration.
>
> Results
>
> MTRL fine-tuning improved the search agent on three of four held-out benchmarks and made it substantially more reliable across all of them. The largest gains came on BrowseComp-Plus (+23.7 percent nDCG@10) and WixQA (+18.4 percent), with a smaller gain on Wands and a slight regression on FreshStack. The reliability improvement was the more striking result. On BrowseComp-Plus, the failure rate fell from 22.89 percent to 0.68 percent. This means the agent learned not only to search better but also to finish the task within its turn and token budget. The sections that follow walk through the training curves and the per-benchmark numbers.
>
> Training progress
>
> The following figure shows the reward (nDCG@10) on both training and validation instances over the course of training. The x-axis represents training steps and the y-axis shows the nDCG@10 score. Two lines track training and validation reward, both rising steadily before plateauing. MTRL training can span multiple days and the MTRL service has a default time limit of 24 hours, which is adjustable through the CreateJob JSON schema. If a job is stopped or has failed because of timeout or infrastructure error, you can continue training from a previous checkpoint with resume support.
>
> Figure 1: nDCG@10 reward on the training and validation sets over the course of training
>
> The figure plots nDCG@10 against training steps for both training and validation sets. Both curves increase steadily as fine-tuning progresses and saturate by the end of training, suggesting further training would not be beneficial.
>
> Test performance
>
> The following table compares the fine-tuned model against the original Qwen3.6-27B on four held-out test datasets. All metrics in the table are computed from our evaluation runs on the datasets listed in the preceding section.
>
> Column definitions:
>
> Size is the number of questions in the dataset.
>
> nDCG@10 is the standard Normalized Discounted Cumulative Gain. The failed tasks are assigned nDCG@10 of 0.
>
> Failure rate is the percentage of questions where the agent hits an error (for example, exceeding the turn limit or token budget).
>
> Turns (avg) is the average number of turns per question.
>
> benchmark
>
> size
>
> model
>
> ndcg@10
>
> fail_rate
>
> turns
>
> WixQA
>
> 400
>
> Qwen3.6-27B
>
> 0.5725
>
> 0.67%
>
> 4.3
>
> WixQA
>
> 400
>
> Qwen3.6-27B-finetune
>
> 0.6781
>
> 0.17%
>
> 4.5
>
> Wands
>
> 147
>
> Qwen3.6-27B
>
> 0.5762
>
> 0.00%
>
> 2.2
>
> Wands
>
> 147
>
> Qwen3.6-27B-finetune
>
> 0.6112
>
> 0.00%
>
> 2.9
>
> FreshStack
>
> 672
>
> Qwen3.6-27B
>
> 0.4112
>
> 0.20%
>
> 3.1
>
> FreshStack
>
> 672
>
> Qwen3.6-27B-finetune
>
> 0.4089
>
> 0.05%
>
> 2.8
>
> BrowseComp-Plus
>
> 830
>
> Qwen3.6-27B
>
> 0.5136
>
> 22.89%
>
> 7.0
>
> BrowseComp-Plus
>
> 830
>
> Qwen3.6-27B-finetune
>
> 0.6354
>
> 0.68%
>
> 6.3
>
> The results show that RL fine-tuning made a meaningful difference:
>
> Better search quality: As shown in the preceding table, nDCG@10 improved on WixQA (from 0.5725 to 0.6781, a +18.4 percent gain), on Wands (from 0.5762 to 0.6112, a +6 percent), and on BrowseComp-Plus (from 0.5136 to 0.6354, a +23.7 percent gain). The score decreased slightly on FreshStack.
>
> Fewer failures: Assigning a reward of -1 for failure cases was highly effective. On BrowseComp-Plus, the failure rate dropped from 22.89 percent to only 0.68 percent.
>
> Clean up
>
> If you do explore this approach, remember to clean up the resources afterward to avoid ongoing charges:
>
> Stop or delete the MTRL training job in the Amazon SageMaker AI console if it’s still running.
>
> Delete the model artifacts in Amazon S3 if they’re no longer needed.
>
> Delete any deployed endpoints that were created for evaluation.
>
> Conclusion
>
> In this post, we described our experience using Amazon SageMaker AI MTRL to fine-tune an LLM-powered search agent with reinforcement learning. With minimal configuration, the fine-tuned model showed substantial improvements in retrieval quality, failure rate, and turn efficiency (fewer turns per question).
>
> Key takeaways from our experience with Amazon SageMaker AI MTRL:
>
> Low barrier to entry: Default configurations work well, and no deep RL expertise is required to get started.
>
> Serverless infrastructure: No need to provision GPUs or manage distributed training clusters. You pay per-token.
>
> Resumable training: Long training runs can be split across multiple jobs.
>
> Direct optimization: You train against your actual task metric rather than proxy losses.
>
> Full observability: You can inspect trajectories turn by turn in MLflow managed by Amazon SageMaker AI to understand what the agent learned.
>
> Next steps
>
> If you want to apply this approach to your own agents, here are some useful starting points:
>
> Consult the Amazon SageMaker AI MTRL documentation.
>
> Prepare your dataset in the required format.
>
> Prepare your agent and define your reward function based on your task-specific metric.
>
> Start with default configurations, which worked well in our experience.
>
> Evaluate and iterate.
>
> About the authors
>
> Huibin Shen
>
> Huibin is an applied scientist in AWS, currently working on agentic search. His main interest is applying advanced reinforcement learning and retrieval machine learning techniques to solve real-world problems.
>
> Pooja Karadgi
>
> Pooja is a Senior Product Manager at AWS on the SageMaker AI team, where she works on developer experiences and model customization, including reinforcement learning. Her focus is making advanced fine-tuning techniques practical and accessible for builders.
>
> Sifei Li
>
> Sifei is a Senior Software Engineer in Amazon SageMaker where she’s working on building Amazon AI Platforms and was part of the launch team for Amazon SageMaker Model Customization and Multi-turn RL Platform.
>
> Lorenzo Stella
>
> Lorenzo is a Senior Applied Scientist at AWS, where he works on agentic search. His interest spans training of AI models and reinforcement learning, with a focus on decision-making systems and time series forecasting.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。