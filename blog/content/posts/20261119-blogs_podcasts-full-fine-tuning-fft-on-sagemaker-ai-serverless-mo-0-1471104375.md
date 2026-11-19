---
title: "Full Fine-Tuning (FFT) on SageMaker AI Serverless Model Customization"
date: 2026-11-19T11:26:03+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "生成式 AI", "机器学习", "Prompt 工程", "Advanced (300)", "Amazon SageMaker AI", "Announcements", "博客与播客"]
categories: []
source: "blogs_podcasts"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:4babf0a6f709cbdb505442db6c3833d1c217857761abdbeca8af87d2bee5b8d8"
source_payload_sha256: "sha256:2ca9cc4e08c3c968b67b50bbdea6132dc18cf746892d22c8f91a17012d12087f"
observation_id: obs_1471104375f835f45826c33816d227db6fd6f7ca6dca486dfdda7b88a024c13c
event_id: evt_140d3d2f0ac7dcecf6d9317b05cbbc3b594b6da841e7081a40ec494529c02c08
revision_id: rev_c221dc8ae5c2b98fe8201252b558fb710a77063b169e661c29eea56018551d22
source_published_at: 2026-11-19T00:15:58Z
first_seen_at: 2026-11-19T03:24:42.554113Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 69
description: "当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。"
external_url: https://aws.amazon.com/blogs/machine-learning/full-fine-tuning-fft-on-sagemaker-ai-serverless-model-customization
parent_observation_id: null
last_seen_at: 2026-11-19T03:24:42.554113Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/full-fine-tuning-fft-on-sagemaker-ai-serverless-model-customization](https://aws.amazon.com/blogs/machine-learning/full-fine-tuning-fft-on-sagemaker-ai-serverless-model-customization)
- **发布域名**: aws.amazon.com

## 来源摘要/节选

> Fine-tuning is the process of continuing to train a pretrained large language model (LLM) on a company’s own data so it adapts to a specific domain, task, or style rather than relying on general-purpose knowledge alone. For businesses, the value is twofold. A fine-tuned model delivers measurably better accuracy on domain-specific work while reducing costs: a smaller specialized model can match or exceed a frontier model on your task at a fraction of the per-token inference price. Those savings compound across millions of requests. Fine-tuning has therefore become an essential process for businesses looking to get more value from LLMs at lower costs.
>
> Parameter-efficient fine-tuning (PEFT) methods like Low-Rank Adaptation (LoRA) have emerged as a practical solution for fine-tuning LLMs to downstream tasks, reducing GPU capacity requirements by updating only a small subset of LLM parameters. LoRA aims to strike a balance between efficiency and expressiveness, however, the low-rank nature of the weight update inherently limits the representation power of LoRA fine-tuned models, potentially compromising performance on complex tasks. This trade-off hampers the ability of LoRA methods to capture complex patterns needed for diverse tasks. To address these challenges, Full Fine-Tuning (FFT) updates model parameters simultaneously, overcoming the low-rank limitations so LLMs can fully absorb complex domain-specific knowledge.
>
> Amazon SageMaker AI Serverless Model Customization now supports Full Fine-Tuning (FFT), so you can achieve superior model quality without managing infrastructure. There is no GPU provisioning, cluster setup, or distributed-training configuration required. In this post, we explore when and where FFT consistently outperforms LoRA across key benchmarks, examine the spectral properties of model weight matrices that explain this quality gap, provide practical hyperparameter tuning guidelines backed by controlled experiments using SageMaker AI Serverless Model Customization, and show you how to get started with FFT on SageMaker AI.
>
> Full Fine-Tuning: Why it matters
>
> Model customization types like LoRA reduce trainable parameters by freezing the pre-trained model’s weights and injecting small, separate pairs of replacement matrices (called low-rank matrices) into the model layers. This works well for simple adaptations, but the low-rank structure inherently limits the representation power of the fine-tuned model. As tasks grow more complex and datasets scale beyond tens of thousands of examples, LoRA hits an accuracy plateau where increasing rank (and thus trainable parameters) fails to bridge the accuracy gap with standard fine-tuning. This plateau reveals that the performance gap isn’t simply because of fewer parameters. It’s caused by rank deficiency itself. The low-rank update can’t capture the full complexity of the weight changes needed for deep task adaptation.
>
> However, for complex tasks and domains where large, good-quality datasets exist, full-rank fine-tuning excels by updating model parameters simultaneously. FFT modifies the model’s weight matrix uniformly, using the full representational capacity of the model’s weight matrices rather than restricting updates to a small subspace, and without introducing the abrupt, localized distortions characteristic of low-rank methods. The result is stronger model convergence, better activation alignment across model layers, and a model that faithfully captures both the target task distribution and the richness of its pre-trained knowledge. FFT’s quality advantage grows with dataset scale: at 100K+ training examples, FFT achieved 90.0 percent on LLM-as-Judge semantic correctness across code generation tasks, as shown in the following chart.
>
> Figure 1: LLM-as-Judge semantic correctness by training method as training data scales to 100K+ examples
>
> Furthermore, the following radar chart provides a holistic view: the base model (inner polygon) shows consistently low scores across all axes. LoRA (middle polygon) shows strong, balanced improvement. FFT (outer polygon) extends further on every dimension, with particularly pronounced leads on BLEU and ROUGE-2 scores. This multi-dimensional quality lead confirms that it isn’t a metric-specific artifact but a fundamental advantage of full-rank optimization.
>
> Figure 2: Radar chart comparing the base model, LoRA, and FFT across quality dimensions
>
> The details of how we arrived at these results, the coding datasets used for model customization, and the experimentation process are explained in detail in the following sections.
>
> Experimentation and benchmark results
>
> In this post we used the Supervised Fine-Tuning (SFT) technique on a Qwen3-4B base model offered within Amazon SageMaker AI Studio and performed all the fine-tuning experiments using SageMaker AI Serverless Model Customization across LoRA and FFT training methods. Within each experiment, both methods received the same prompts, targets, and evaluation code.
>
> Dataset: Code generation 110K instruction pairs
>
> For all the experimentation, we fine-tuned the Qwen3-4B base model on the Magicoder-Evol-Instruct-110K dataset, a curated corpus of 110,000 coding instruction-response pairs spanning algorithm design, debugging, data structures, and systems programming. We applied a 90/5/5 split to the dataset: 99,000 records for training, 5,500 for validation to monitor convergence and training loss during the customization job, and 5,500 reserved as a held-out test set for unbiased evaluation of the final model, as registered in SageMaker AI dataset assets and shown in the following figure.
>
> Figure 3: The 110K instruction-pair dataset registered in SageMaker AI dataset assets
>
> Serverless Model Customization job
>
> All the model customization experiments in this post were performed on Amazon SageMaker AI Serverless Model Customization. Serverless Model Customization on SageMaker AI lets data scientists and machine learning (ML) engineers focus on model fine-tuning without managing infrastructure or GPU capacity planning. You specify the base model, dataset, and hyperparameters, and the service handles compute allocation and checkpoint management automatically in a serverless fashion. The following code snippet shows one such experiment for launching a Full Fine-Tuning (FFT) job on Serverless Model Customization using the SageMaker Python SDK.
>
> from sagemaker.train.sft_trainer import SFTTrainer
>
> from sagemaker.train.common import TrainingType
>
> trainer = SFTTrainer(
>
> model=base_model_id,
>
> training_type=TrainingType.FULL,
>
> model_package_group=model_package_group_name,
>
> training_dataset=training_dataset,
>
> validation_dataset=val_dataset,
>
> s3_output_path=output_path,
>
> sagemaker_session=sess,
>
> role=role,
>
> )
>
> # Configure hyperparameters as needed
>
> trainer.hyperparameters.learning_rate = 2e-5
>
> trainer.hyperparameters.global_batch_size = 8
>
> trainer.hyperparameters.max_epochs = 2
>
> trainer.hyperparameters.lr_warmup_steps_ratio = 0.1
>
> trainer.train(wait=False)
>
> The code triggers a serverless model customization job, shown in the following screenshot, with training performance metrics tracked in the job and viewable in the linked MLflow app.
>
> Figure 4: Serverless model customization job with training metrics tracked in MLflow
>
> Switching from Full Fine-Tuning to LoRA requires only one change: set TrainingType.FULL to TrainingType.LORA. The rest of the code remains identical:
>
> trainer = SFTTrainer(
>
> model=base_model_id,
>
> training_type=TrainingType.LORA, # ← only change
>
> model_package_group=model_package_group_name,
>
> training_dataset=training_dataset,
>
> validation_dataset=val_dataset,
>
> ...
>
> )
>
> Model evaluation and benchmarking
>
> We tested the resulting customized models across three diverse evaluation methods built into SageMaker AI Serverless Model Customization: LLM-as-Judge, PRIMECODE, and MMLU, shown in the following image. Each targets a different dimension of model quality: semantic correctness, code generation fidelity, and general knowledge retention. Together they provide a comprehensive picture of the model customization quality.
>
> Figure 5: The three built-in evaluation methods in SageMaker AI Serverless Model Customization
>
> The LLM-as-Judge metric uses a frontier model (in this post, Amazon Nova Pro) as an automated evaluator that reads the model’s generated code alongside the original prompt and judges whether the solution is logically correct. On serverless model customization you can evaluate both the customized model alongside the base model, as shown in the following figure.
>
> Figure 6: LLM-as-Judge evaluation comparing the customized model and the base model
>
> PRIMECODE is a custom scorer evaluation that measures how closely the model’s generated code matches reference solutions using deterministic text-similarity metrics: BLEU (n-gram precision), ROUGE-1/2/L (recall-oriented overlap), and F1 (precision-recall balance). These metrics are fully reproducible, making them ideal for controlled ablation studies. We used PRIMECODE as our primary metric for surface-level code quality because it quantifies how well the model has learned the coding patterns, formatting conventions, and implementation style present in the training data. A high BLEU score means the model generates code that looks structurally similar to expert-written solutions, as shown in the following results.
>
> Figure 7: PRIMECODE text-similarity scores for the customized model
>
> MMLU (Massive Multitask Language Understanding) is a built-in benchmark that tests the model across 57 academic subjects from abstract algebra and anatomy to Nutrition and Philosophy. It measures whether the model retains its broad general knowledge after domain-specific fine-tuning, as shown in the following figure. We used MMLU as our forgetting detection guardrail. Fine-tuning on code can overwrite general capabilities stored in the model’s weights. By tracking MMLU accuracy before and after fine-tuning, we can quantify exactly how much general knowledge the model sacrifices for code generation improvement, and whether our hyperparameter choices accelerate or mitigate this trade-off.
>
> Figure 8: MMLU accuracy before and after fine-tuning
>
> Rapid experimentation at scale
>
> The ease of setup and use of SageMaker AI Serverless Model Customization let us perform rapid experimentation without re-provisioning infrastructure. We changed training types between LoRA and FFT, swept hyperparameters, and tested across multiple base models. Over a short time window, we ran tens of model customization experiments across multiple supported base models (Qwen3-4B, DeepSeek-R1-1.5B, Nemotron-30B, Gemma-4-26B), systematically ablating learning rate, batch size, warmup ratio, epoch count, and dataset scale. Each experiment, from job submission to evaluation results, completed in a few hours and the resulting fine-tuned models were automatically registered in SageMaker Model Registry as versioned Model Packages, ready for review or deployment.
>
> Hyperparameter options
>
> SageMaker AI Serverless Model Customization supports many hyperparameters. In this section, we explain a few important ones, informed by the series of experiments that we ran across multiple hyperparameter configurations within the previously mentioned code generation task. While effective values will vary by task, the patterns observed across these experiments provide useful starting points when configuring FFT model customization jobs. For more information about the hyperparameters that you can configure before launching an FFT model customization job, see the hyperparameters documentation page.
>
> 1. learning_rate
>
> In full fine-tuning, the learning rate controls how aggressively every weight is updated. Unlike LoRA, where only small adapter matrices change, an FFT learning rate that is too high permanently overwrites pretrained knowledge. In our experiments, the following LR × dataset-size risk map shows that an LR of 2e-5 on a large dataset (over 100 thousand) was the safe zone.
>
> Figure 9: Learning rate and dataset-size risk map for full fine-tuning
>
> 2. max_epochs
>
> Epoch count in FFT is fundamentally a forgetting question, not a loss-curve question. Training loss will keep falling and your held-out validation will look healthy because it shares a distribution with training data, but capabilities on everything you didn’t train on quietly degrade. The LLM-as-Judge correctness score rose to 90.0 percent at 3 epochs, and extending beyond 3 epochs degraded every variant we experimented with.
>
> 3. global_batch_size
>
> Batch size determines how many examples contribute to each gradient step. At a fixed learning rate, smaller batches produce more noisy updates that behave much like a higher learning rate, increasing forgetting risk. Larger batches reduce noise but also reduce the number of optimization steps, potentially underfitting.
>
> Figure 10: Effect of global batch size on model quality
>
> Catastrophic forgetting risk
>
> FFT modifies every parameter in the model, including the parameters that encode general knowledge acquired during pre-training. When fine-tuning pushes these parameters too aggressively toward a narrow domain, the model can “forget” its broader capabilities, a phenomenon known as catastrophic forgetting. We tested for this systematically using MMLU, measuring general knowledge retention across all our fine-tuning configurations. A baseline configuration with warmup=5 percent, batch size 8, and LR=2e-5 best preserved general knowledge (MMLU), as shown in the following figure.
>
> Figure 11: MMLU general-knowledge retention across hyperparameter configurations
>
> Hence, it is important to note that FFT isn’t universally superior to LoRA, and its effectiveness is extremely sensitive to hyperparameter choices. For example, in our experiments, both FFT and LoRA underperformed the base model on MATH exact match, underscoring the challenge of preserving reasoning capabilities during domain-specific fine-tuning. Aggressive learning rates (LR ≥ 5e-5) in FFT proved particularly destructive, causing MATH scores to plummet to 2–3 percent and MMLU accuracy to drop to 3.6 percent, clear evidence of catastrophic forgetting. Additionally, LoRA slightly outperformed FFT on the LLM-as-Judge metric (81.5 percent compared to 79.5 percent), demonstrating that parameter-efficient methods can still hold an edge on subjective quality assessments. These findings reinforce that the choice between FFT and LoRA should be guided by careful experimentation, dataset characteristics, and a clear understanding of the trade-offs involved.
>
> Conclusion
>
> With Full Fine-Tuning on Amazon SageMaker AI Serverless Model Customization, your model can fully absorb domain-specific knowledge when task complexity and data scale demand it. If your use case requires deep adaptation, such as specialized reasoning, code generation, or domain-specific language understanding, and you have sufficient high-quality training data, FFT delivers measurably stronger results.
>
> You can get started with FFT on SageMaker AI Serverless Model Customization with serverless training, built-in evaluation, and without infrastructure or compute capacity planning, so you can focus on your data and hyperparameter choices. You can use the SageMaker Python SDK to configure and launch your training and evaluation jobs programmatically. You can see the documentation for supported base models available for Full Fine-Tuning on Serverless Model Customization.
>
> About the author
>
> Sandeep Raveesh-Babu
>
> Sandeep is a GenAI Specialist Solutions Architect at AWS. He works with customers through their LLM training, LLM inference, and GenAI observability. He focuses on product development helping AWS build and solve industry challenges in the generative AI space. You can connect with Sandeep on LinkedIn to learn about generative AI solutions.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。