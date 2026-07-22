---
title: "Exploring self-distilled reasoning for supervised fine-tuning with Amazon Nova"
date: 2026-07-22T00:48:57+08:00
draft: false
entry_kind: "auto"
tags: ["Advanced (300)", "Amazon SageMaker", "Best Practices", "博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:0bd803028866eacc80aaa3127607611f07ec2d0c0fe23dbc9f072ef1f6ea2c4e"
source_payload_sha256: "sha256:1141098a1824a1fc6705ed48b2e0261414dc3d300ec8fe9d741a0983315eb223"
observation_id: obs_2443bdbcb52604c43e6327b49a64cb42dc4e2379982f6c2fa8b30ab435e16d47
event_id: evt_cdf582de8ce2d5744b0cb0f5f1d30008d709b2be44732396cf706ae6dadb3418
revision_id: rev_53f2f287f4b65146666c1c5bc4ea656a310b9eeb6f80e768401d2083d842b804
source_published_at: 2026-07-21T16:23:12Z
first_seen_at: 2026-07-21T17:13:01Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: true
source_truncation_reason: "crawler_feed_content_limit"
source_support: 1.0
source_title_chars_original: 78
description: "当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。"
external_url: https://aws.amazon.com/blogs/machine-learning/exploring-self-distilled-reasoning-for-supervised-fine-tuning-with-amazon-nova
parent_observation_id: null
last_seen_at: 2026-07-22T00:00:00Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/exploring-self-distilled-reasoning-for-supervised-fine-tuning-with-amazon-nova](https://aws.amazon.com/blogs/machine-learning/exploring-self-distilled-reasoning-for-supervised-fine-tuning-with-amazon-nova)

## 来源摘要/节选

> When you fine-tune a model using Supervised Fine-Tuning (SFT), creating high-quality chain-of-thought (CoT) reasoning traces for your training data is often impractical and can be prohibitively expensive. As a result, you might choose to skip reasoning during SFT and train with only inputs and outputs. However, reasoning is a key capability of the Amazon Nova 2 family of models, and it’s been shown to significantly enhance prediction performance in Nova and other frontier models, often with performance gains on hard problems like coding and math. With Amazon Nova 2 customization, you can use the power of thinking models on your specific domains through techniques such as SFT and Reinforcement Fine-Tuning (RFT). For SFT, a key requirement to unlock these gains is the availability of golden CoT traces in the SFT dataset, that is, thinking traces from a strong teacher model that have been further validated and cleaned.
>
> In this post, we explore an idea for generating thinking tokens for datasets that lack reasoning traces in SFT customization. We first examine the reasoning suppression problem, then introduce Self-Distilled Reasoning (SDR), validate it across three benchmarks, and provide practical recommendations. SDR re-uses the chain of thought from the base Amazon Nova 2 Lite model as a stand-in for non-reasoning datasets. Through our experiments we make a few observations on the impact of introducing SDR, from improving target performance to mitigating catastrophic forgetting. This is in line with a growing body of work that is discovering the importance of distilling information from a model into itself during training, otherwise known as self-distillation.
>
> The following figure illustrates how SDR compares with vanilla SFT and model merging across target performance and math retention. Model merging is a straightforward approach to retain previously acquired skills, that takes an SFT checkpoint and merges it back to the base model (before SFT). However, merging often comes at the expense of forgoing gains obtained on the SFT checkpoint because of catastrophic forgetting which manifests as a trade-off between target and general performance. SDR on the other hand mitigates this issue with similar or better target performance as pure SFT (with no merging) while retaining most of general performance.
>
> Because of catastrophic forgetting, we observe that SFT on a dataset can lead to previous knowledge being completely lost. For instance, we find that vanilla SFT leads to Math performance dropping from 70 percent (base) to 6 percent on average (Table 2). With SDR, we’re able to almost entirely recover it back. Self-distilled reasoning allows us to retain the base model’s capabilities without compromising on target performance, and in many cases it improves target performance as well. Model merging is a common solution to mitigate catastrophic forgetting, but SDR achieves this retention more effectively.
>
> SDR provides in-training regularization by augmenting the dataset with the model’s own reasoning traces. It doesn’t require a separate teacher model or post-hoc interpolation. This approach requires no human annotation, is applicable to existing SFT datasets regardless of domain, and is more effective than model merging at preserving both target and general performance.
>
> Compared with model merging, self-distillation yields nearly identical math performance (70 percent compared to 68 percent) while improving target performance by over 6.5 percent on average at the same time. This finding aligns with recent research that advocates self-distillation as a powerful mechanism to mitigate catastrophic forgetting.
>
> Background: SFT on datasets without reasoning tokens may result in loss of reasoning ability
>
> Before introducing the approach, it is important to understand why SFT on datasets without reasoning traces leads to degraded model performance. This section examines the reasoning suppression problem, quantifies the impact of reasoning on target performance, and discusses model merging as an existing recovery mechanism.
>
> The reasoning suppression problem
>
> SFT training on non-reasoning datasets with reasoning mode active leads to a critical issue: the model loses its ability to reason during inference, even when you explicitly turn on reasoning mode. We hypothesize that this phenomenon occurs because the training objective calculates loss on both reasoning and output tokens together. When training data contains only input-output pairs without intermediate reasoning steps, the model receives no supervision signal for generating coherent reasoning traces. The loss function effectively penalizes tokens that don’t directly contribute to the final output, training the model to bypass its reasoning mechanisms. This behavior exemplifies shortcut learning, where models rely on spurious correlations rather than learning robust reasoning patterns.
>
> Quantifying the impact of reasoning
>
> Despite the suppression issue, turning on reasoning during both training and inference produces significant benefits in target performance. To confirm fair comparison, we maintain consistency between train and inference settings: comparing reasoning-on during both training and inference versus reasoning-off during both training and inference. Our experiments reveal that turning on reasoning during training and inference leads to a significant improvement. The following table demonstrates this effect on the LLaVA CoT dataset with varying LoRA (Low-Rank Adaptation) merge weights.
>
> Merge weight
>
> Target perf (reasoning on)
>
> Target perf (reasoning off)
>
> Delta
>
> 0.0 (base)
>
> 12.30%
>
> 12.30%
>
> 0%
>
> 0.3
>
> 34.38%
>
> 35.28%
>
> -0.9%
>
> 0.5
>
> 60.51%
>
> 48.80%
>
> +11.7%
>
> 0.7
>
> 66.67%
>
> 54.05%
>
> +12.6%
>
> 1.0 (full merge)
>
> 65.17%
>
> 47.90%
>
> +17.3%
>
> Table 1: Impact of reasoning and merging weight on target performance. Training and inference reasoning modes are kept consistent.
>
> Model merging as a recovery mechanism
>
> Our current recommended approach to address the reasoning suppression issue for SFT use cases without reasoning tokens is to use model merging as a mechanism to recover the reasoning skill. Similar to how model merging can restore mathematical or coding capabilities after domain-specific fine-tuning, we find that reasoning capability can be recovered through weighted interpolation between the fine-tuned model and the base model. This recovery is strongly correlated with the restoration of general performance metrics (such as math and coding benchmarks), suggesting that reasoning is a fundamental capability that underlies multiple downstream skills.
>
> To understand this better, we use the following benchmarks in this experiment:
>
> ToolACE – Tool-calling benchmark (10K samples). Evaluates the model’s ability to generate correct function calls with proper argument names and values given a user query and available tool definitions. Short context (approximately 2K tokens). Scored on strict success rate (exact match of function name and all arguments). Requires precise structured output and argument value inference.
>
> CoCoHD – Long-context structured extraction (730 samples). Evaluates extraction of 10 metadata fields (title, chamber, committee, members, dates) from U.S. congressional hearing transcripts in JSON format. Long context (35K–85K characters). Scored on key/value overlap between predicted and target JSON. Requires parsing very long documents and producing schema-conformant structured output. Extracted from GitHub.
>
> GovReport – Long-context abstractive summarization (17K samples). Evaluates generation of 250–450 word plain-text summaries of U.S. government reports (GAO, CRS). Long context (35K–85K characters input). Scored on ROUGE-L (longest common subsequence overlap with reference summary). Requires synthesizing dense policy documents into concise, factual narratives. Extracted from HuggingFace.
>
> Invoice-OCR – Multimodal document understanding (approximately 500 samples, image and text). Evaluates extraction of structured fields from scanned invoice images. Short context (single image and prompt). Scored on ANLS (Average Normalized Levenshtein Similarity). Requires visual text recognition and field-level extraction from varied document layouts. Extracted from Kaggle.
>
> CaptionGen – Video captioning (1800 samples, video and text). Evaluates generation of descriptive captions for video clips. Variable context (video frames and prompt). Scored using automated evaluation (likely CIDEr/METEOR or LLM-judge). Requires temporal understanding across video frames and natural language generation. Extracted from HuggingFace.
>
> We investigate whether reasoning emerges with model merging. On an Instruction Following benchmark, we count the number of reasoning tokens on a model that is trained without reasoning. The x-axis shows the merging weight between the custom and the base model, where 0.0 corresponds to the base model and 1.0 is the SFT model without merging.
>
> Implications for customization
>
> These findings have important implications if you’re deploying customized models. First, maintaining the same reasoning mode during training and inference is critical for optimal performance. Second, without intervention, domain-specific SFT can significantly degrade general reasoning abilities. Third, model merging offers a post-hoc solution, but requires careful tuning of the merging weight to balance competing objectives. These trade-offs motivated us to develop a training approach that preserves reasoning capability without requiring post-hoc interventions.
>
> Role of reasoning in SFT
>
> Reasoning traces in SFT serve three critical functions that connect reinforcement fine-tuning (RFT), regularization, and self-distillation paradigms.
>
> First, reasoning traces act as implicit policy regularization by constraining the fine-tuned model to stay close to the base model’s policy. This prevents catastrophic forgetting and capability degradation in a manner similar to KL-regularization in RLHF. Second, reasoning provides process supervision, analogous to step-by-step reward shaping in RFT, rather than just outcome supervision. This leads to more robust generalization. Third, self-distillation, where a model learns from its own predictions, has proven effective across domains from Born-Again Networks to Constitutional AI. Reasoning traces offer particularly rich self-supervision by capturing the model’s problem-solving process rather than just final outputs, as demonstrated in recent continual learning research.
>
> Recent work shows that effective fine-tuned models maintain proximity to the base model in parameter space, and our approach uses this insight by applying the base model’s own reasoning traces as training targets, creating a learning signal consistent with the model’s internal representations while providing dense token-level supervision throughout the reasoning process.
>
> Self-distilled reasoning
>
> We propose an effective approach that uses self-distilled reasoning (SDR) for SFT customization on datasets without reasoning traces. The process works in three stages. First, you use the base reasoning model (such as Amazon Nova 2 Lite) to generate reasoning traces for each example in the SFT dataset. Next, you augment the training data by prepending the generated reasoning traces to the original outputs. Finally, you fine-tune the model with reasoning mode turned on, providing supervision on both reasoning and output tokens.
>
> SDR offers several advantages for your SFT workflow. There is zero annotation cost because no human effort is required to create the reasoning traces. The reasoning traces are consistent with the base model’s own problem-solving approach. The technique scales to existing SFT datasets regardless of domain and gives you flexibility to use different teacher models.
>
> Constructing reasoning traces for SFT
>
> We query Amazon Bedrock to obtain reasoning traces for a given dataset. There are two approaches to construct chain-of-thought reasoning, each with different trade-offs.
>
> Basic reasoning
>
> This approach generates reasoning traces in a forward manner, where the model naturally produces its reasoning given only the question. This mimics how the model would reason during inference. The prompt template is:
>
> Think through this question naturally and show your reasoning:
>
> {user_text}
>
> Format your response with &lt;thinking&gt; tags for reasoning and &lt;answer&gt; tags for the final answer.
>
> Use a consistent reasoning style.
>
> Guided reasoning
>
> This approach uses the availability of ground-truth answers to guide reasoning generation in a backward manner. By providing both the question and answer, we ask the model to reconstruct plausible reasoning that connects them, similar to hindsight learning approaches. The prompt template is:
>
> Generate natural reasoning for solving this question.
>
> Act as if you don't know the answer yet.
>
> Question:
>
> {user_text}
>
> Answer to arrive at:
>
> {assistant_content}
>
> Format your response with &lt;thinking&gt; tags for reasoning
>
> and &lt;answer&gt; tags for the final answer. Write natural
>
> reasoning that works toward this answer without assuming
>
> you know it beforehand. Use a consistent reasoning style.
>
> To verify the model does not accidentally leak the answer into the reasoning trace (which would introduce noise), we perform a secondary filtering step that removes mentions of the answer to obtain the final reasoning trace.
>
> Implementation pipeline
>
> The following code shows how to implement guided reasoning using the Amazon Bedrock Converse API. The pipeline reads your SFT training data, generates Chain-of-Thought (CoT) reasoning traces, and assembles the final dataset with reasoningContent blocks.
>
> Setup and CoT prompt generation
>
> import json, re, boto3, time
>
> MODEL_ID = "amazon.nova-lite-v1:0"
>
> bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")
>
> COT_SYSTEM = """You are an expert evaluator. Provide a
>
> detailed Chain-of-Thought explaining why the given
>
> ground truth answer is correct and makes sense."""
>
> COT_USER_TEMPLATE = """Given the task context and ground
>
> truth annotation, provide a Chain-of-Thought.
>
> **Original System Context:** {system_prompt}
>
> **Original User Request:** {user_prompt}
>
> **Ground Truth Annotation:**
>
> ```json
>
> {ground_truth}
>
> ```
>
> ONLY provide your justification within
>
> &lt;justification&gt;&lt;/justification&gt; tags."""
>
> Invoke Amazon Bedrock and assemble the final dataset
>
> # Invoke Bedrock for each CoT prompt
>
> for req in cot_requests:
>
> response = bedrock.converse(
>
> modelId=MODEL_ID,
>
> system=[{"text": req["system"]}],
>
> messages=[{"role":"user",
>
> "content":[{"text":req["query"]}]}],
>
> inferenceConfig={"maxTokens":4096,"temperature":0.3,"topP": 0.9,"topK": 50})
>
> output = response["output"]["message"]["content"][0]["text"]
>
> time.sleep(2) # rate limit
>
> # Parse &lt;justification&gt; tags and build SFT dataset
>
> for idx, item in enumerate(original_data):
>
> tags = extract_xml_tag(inference[idx], "justification")
>
> reasoning_block = {"reasoningContent": {"reasoningText":
>
> {"text": "Based on the provided context, lets think"
>
> " step by step " + tags[0].strip()&#125;&#125;}
>
> sft_dataset.append({
>
> "schemaVersion": "bedrock-conversation-2024",
>
> "system": item["system"],
>
> "messages": [item["messages"][0],
>
> {"role": "assistant",
>
> "content": [reasoning_block, original_text]}]})
>
> Inference configuration parameters
>
> temperature: 0.3 Low randomness produces consistent, deterministic reasoning traces suitable for training data.
>
> topP: 0.9 Nucleus sampling that retains the top 90 percent probability mass. Balances coherence with enough diversity to avoid degenerate repetitions.
>
> topK: 50 Limits token candidates to the top 50 at each step. Prevents unlikely tokens from appearing in reasoning traces while keeping natural language flow.
>
> Sample input (no reasoning)
>
> {"schemaVersion": "bedrock-conversation-2024",
>
> "system": [{"text": "You are a legal expert..."}],
>
> "messages": [
>
> {"role": "user", "content": [{"text":
>
> "Review this clause: Company shall not disclose
>
> data to third parties."}]},
>
> {"role": "assistant", "content": [{"text":
>
> "[{"comment_id": "001", "severity": "Medium",
>
> "comment": "Add standard confidentiality
>
> exceptions...", ...}]"}]}]}
>
> Sample output (with reasoning prepended)
>
> {"role": "assistant", "content": [
>
> {"reasoningContent": {"reasoningText": {"text":
>
> "Based on the provided context, lets think step by
>
> step: 1. Correctness: The annotation correctly
>
> identifies an issue with the clause by suggesting
>
> standard confidentiality exceptions... 2. Severity:
>
> Medium is appropriate because... 3. Category:
>
> Privacy fits because data protection is a core
>
> privacy concern... 6. References: std-clauses.pdf
>
> validates the need for exceptions."&#125;&#125;},
>
> {"text": "[{"comment_id": "001", ...}]"}]}
>
> Our experiments (discussed in the next section) demonstrate that this approach leads to significant improvements in both target domain performance and general capability preservation, validating the hypothesis that self-distilled reasoning provides valuable inductive bias during fine-tuning.
>
> Experiments
>
> We run experiments on three benchmarks that do not have reasoning.
>
> MedMCQA is a Q&amp;A style dataset that contains 10k training samples.
>
> CoCoHD is a congressional hearing dataset that has long context (20-60k tokens) and has a task of producing a JSON with specific fields.
>
> Invoice-OCR is a multimodal dataset that has images of invoices and requires a JSON output with the fields from the image.
>
> The following table summarizes our SDR results across three benchmarks. Each column captures a specific dimension of the experimental setup: Model refers to the dataset used for fine-tuning (or the base Nova 2 Lite model when no fine-tuning is applied). Reasoning Traces indicates which model generated the chain-of-thought traces prepended to the training data. “None” means no reasoning was added to the dataset. Training Reasoning specifies whether reasoning mode was enabled during the SFT training process. Inference Reasoning specifies whether reasoning mode was enabled at prediction time. Merging indicates whether model merging (weighted interpolation between the fine-tuned checkpoint and the base model) was applied after training to recover lost general capabilities. Target reports accuracy on the domain-specific benchmark the model was fine-tuned for. Math ↑ (control) reports accuracy on a math benchmark used as a control metric to measure catastrophic forgetting. The base model scores 70 percent, so any significant drop signals that general reasoning ability has been lost during fine-tuning.
>
> Dataset
>
> Reasoning Traces
>
> Training Reasoning
>
> Inference Reasoning
>
> Merging
>
> Target
>
> Math ↑
>
> (control)
>
> Nova 2 Lite
>
> None
>
> No
>
> No
>
> –
>
> 55.60%
>
> 12.90%
>
> Nova 2 Lite
>
> None
>
> No
>
> Yes
>
> –
>
> 55.40%
>
> 70%
>
> MedMCQA
>
> None
>
> No
>
> Yes
>
> Yes
>
> 60.50%
>
> 8.30%
>
> MedMCQA
>
> None
>
> No
>
> Yes
>
> No
>
> 63.80%
>
> 0%
>
> MedMCQA
>
> Nova 2 Lite Basic
>
> Yes
>
> Yes
>
> No
>
> 66.60%
>
> 67.90%
>
> MedMCQA
>
> Nova 2 Lite Guided
>
> Yes
>
> Yes
>
> No
>
> 65.70%
>
> 59.60%
>
> Nova 2 Lite
>
> None
>
> No
>
> No
>
> –
>
> 45%
>
> 12.90%
>
> Nova 2 Lite
>
> None
>
> No
>
> Yes
>
> –
>
> 45%
>
> 70%
>
> CoCoHD
>
> None
>
> No
>
> Yes
>
> Yes
>
> 59.30%
>
> 70%
>
> CoCoHD
>
> None
>
> No
>
> Yes
>
> No
>
> 61.30%
>
> 6.30%
>
> CoCoHD
>
> Nova 2 Lite Basic
>
> Yes
>
> Yes
>
> No
>
> 55.40%
>
> 73.80%
>
> CoCoHD
>
> Nova 2 Lite Supervised
>
> Yes
>
> Yes
>
> No
>
> 61.30%
>
> 65.80%
>
> Nova 2 Lite
>
> None
>
> No
>
> No
>
> –
>
> 82.10%
>
> 12.90%
>
> Nova 2 Lite
>
> None
>
> No
>
> Yes
>
> –
>
> 81.40%
>
> 70%
>
> Invoice-OCR
>
> None
>
> No
>
> Yes
>
> Yes
>
> 82.30%
>
> 70.80%
>
> Invoice-OCR
>
> None
>
> No
>
> Yes
>
> No
>
> 88.10%
>
> 9.60%
>
> Invoice-OCR
>
> Nova 2 Lite Basic
>
> Yes
>
> Yes
>
> No
>
> 86.10%
>
> 67.10%
>
> Invoice-OCR
>
> Nova 2 Lite Supervised
>
> Yes
>
> Yes
>
> No
>
> 87.90%
>
> 67.90%
>
> Table 2: SDR results across three benchmarks. Rows are grouped by dataset. All SDR rows use merge weight 1.0 (no merging needed).
>
> SFT with partial or missing reasoning traces
>
> Reasoning data can be expensive or difficult to curate, and as a result we often encounter situations where only a portion of the SFT dataset contains reasoning. To better understand how SFT behaves in this situation we conduct an ablation study next. We also explore how SDR can help in this situation as a low-overhead and cost-effective alternative.
>
> SFT training with only partial reasoning traces
>
> In this study, we examine the effect of SFT when only a subset of the dataset contains reasoning, which simulates common real-world scenarios for many users. We ran ablations with reasoning traces for LoRA SFT on 10k training samples from LLaVA CoT benchmark. The eval benchmark for this is MathVista where the base model struggles (12.3 percent) mainly because of formatting inconsistencies and LoRA SFT shows a large improvement (34.4 percent).
>
> Math (control) benchmark — catastrophic forgetting
>
> The Math (control) benchmark measures whether the model retains general mathematical reasoning capability after SFT. This is a notable finding: without SDR prefill, general math capability collapses from 68% to 3% as you reduce the percentage of reasoning data in training. With SDR, it stays stable at 65–72 percent regardless of how much reasoning data you include.
>
> Key insight
>
> Without SDR: Reducing reasoning data below 75 percent causes catastrophic forgetting on Math control: 66.6 percent to 21.7 percent to 3.3 percent to 2.5 percent. The model loses its general math capability entirely.
>
> With SDR: Math (control) stays stable at 64–72 percent across all data percentages, even with 0 percent reasoning data. SDR prefill completely prevents catastrophic forgetting.
>
> Median reasoning tokens at inference
>
> This chart shows the token budget spent on reasoning traces during inference. SDR models produce more reasoning tokens (400–860). Models trained with less than or equal to (≤) 25 percent reasoning data and no prefill produce zero reasoning tokens. This means they have completely lost the ability to reason step-by-step.
>
> Key insight
>
> SDR teaches reasoning behavior: Even with 0 percent reasoning data in training, SDR prefill causes the model to produce 859 median reasoning tokens. Without SDR at less than or equal to (≤) 25 percent reasoning data, the model produces zero tokens. It has forgotten how to reason.
>
> Base model comparison: The base Amazon Nova 2 Lite model produces 1,254 median reasoning tokens. After SFT with 100 percent reasoning data, this drops to 367, and the model becomes more efficient (fewer tokens for the same or better accuracy).
>
> MathVista (target) — reasoning on versus off
>
> This chart compares MathVista accuracy with reasoning enabled and disabled at inference time. Enabling reasoning at inference has the greatest impact. It roughly doubles performance regardless of training data composition.
>
> Key insight
>
> Reasoning on at inference consistently delivers 35–47 percent accuracy, compared to 14–22 percent with reasoning off. This is roughly a 2x improvement.
>
> Best configuration: 50 percent reasoning data plus SDR prefill achieves 45.2 percent MathVista with 70.4 percent Math control, avoiding forgetting while maximizing target performance.
>
> Without reasoning at inference, performance drops to near base-model levels (approximately 15–22 percent), regardless of training composition. The model needs the reasoning step to perform well on this benchmark. A notable observation here is that training with SDR prefill (that is, with reasoning enabled) results in better eval performance even with reasoning disabled during inference time. For example, when only 75 percent of the dataset is missing CoT supervision, SDR prefill boosts eval performance by over 5pp even with reasoning disabled at inference (16.4 percent to 21.3 percent), indicating that SDR has an impact in how the model solves a task even when reasoning is disabled.
>
> Conclusions and recommendations
>
> Our experiments across three benchmarks (MedMCQA, CoCoHD, Invoice-OCR) and an ablation on partial-reasoning datasets (LLaVA-CoT) converge on a consistent finding: Self-Distilled Reasoning (SDR) offers a zero-cost approach that simultaneously improves target performance and preserves general capabilities, without requiring model merging.
>
> The starting point for these findings is that reasoning is fragile under vanilla SFT. Training on data without reasoning traces causes reasoning suppression: the model shortcuts to the answer and loses general skills, with Math accuracy collapsing from 70 percent to 0 percent. Model merging partially recovers these skills, but it introduces a trade-off between target and general performance that is hard to tune and adds a checkpoint-mixing step to the training pipeline.
>
> SDR removes this

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。