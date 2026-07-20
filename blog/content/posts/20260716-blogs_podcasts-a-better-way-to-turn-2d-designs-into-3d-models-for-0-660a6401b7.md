---
title: "A better way to turn 2D designs into 3D models for rapid prototyping"
date: 2026-07-16T14:34:01+08:00
draft: false
entry_kind: "auto"
tags: ["Research", "Computer science and technology", "Artificial intelligence", "Machine learning", "Algorithms", "Design", "Systems design", "Computer modeling"]
categories: []
source: "blogs_podcasts"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:6636199e86ff20deedc455aaf324092cb4b4fb78196f076ee520df81c01643d2"
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 68
description: "当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。"
external_url: https://news.mit.edu/2026/turning-2d-designs-into-3d-models-for-rapid-prototyping-0716
observation_id: obs_660a6401b7178f7c3b8f12536335eece845af4d240f750ec8a9f8c4866f66eae
revision_id: rev_eda4027d21289ffbc7c9b0eab5a9c25ff45f27fa26b80ae6ac7d03cbcbfcfdde
event_id: evt_75a0d9d71db5fdf32ee7a019afdb0e9fb6791133e9fad4a790df79727202b56d
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-16T06:35:58Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://news.mit.edu/2026/turning-2d-designs-into-3d-models-for-rapid-prototyping-0716](https://news.mit.edu/2026/turning-2d-designs-into-3d-models-for-rapid-prototyping-0716)

## 来源摘要/节选

> Engineers often use vision-language models to produce new designs, such as for airplane or automobile components. To simulate how those components will perform in realistic situations, they’ll use tried-and-true computer-aided design (CAD) software to generate 3D models of those designs, which they can put through virtual crash or durability tests.
>
> Researchers from MIT and elsewhere have now developed a system that can teach a vision-language model to automatically convert 2D designs into CAD programs that are much more accurate and functional compared to other approaches, while using only a fraction of the computation.
>
> By improving the performance and efficiency of AI-driven CAD generation, this technique could streamline the rapid prototyping process and reduce costs. It could also help engineers identify beneficial design choices they might otherwise overlook.
>
> The system generates new data based on the model’s abilities as it attempts to convert a 2D image into a CAD program. The framework corrects the model’s failures and incorporates them into a dataset with its successful solutions.
>
> It uses these data to teach the model how to fix specific mistakes and tackle tricky problems it would struggle with on its own.
>
> “We want engineers to be able to point our framework at an underperforming CAD model, set a compute budget, and let the system take over — turning the model’s own mistakes into better training data,” says lead author Giorgio Giannone, a research affiliate in the Design Computation and Digital Engineering (DeCoDE) Lab at MIT and a principal research scientist on the AI Innovation Team at Red Hat.
>
> He is joined on the paper by Anna Claire Doris, a mechanical engineering graduate student at MIT; Amin Heyrani Nobari, an MIT postdoc; Kai Xu of RedHat; and co-senior authors Akash Srivastava, director of Core AI at IBM and a principal investigator at the MIT-IBM Computing Research Lab; and Faez Ahmed, associate professor of mechanical engineering at MIT, leader of the DeCoDE Lab, and a principal investigator at the MIT-IBM Computing Research Lab. The research was recently presented at the International Conference on Machine Learning.
>
> “Nearly every physical product around us, from airplanes to appliances, begins its life as a CAD model. Industry teams are eager for AI that can help speed-up the creation of these designs, but today's models often produce simple shapes inadequate for practice. What excites me about this work is that it gives many image-to-CAD-code models a way to improve themselves, learning from their own errors rather than waiting for more human-made data — and that brings trustworthy AI design tools much closer to everyday engineering,” says Ahmed.
>
> Model-aware data
>
> The researchers are working toward building vision-language models (VLMs) for CAD generation. These VLMs take a 2D image and some descriptive text, and output Python code that can be executed in a CAD software program to generate a 3D model of a physical object.
>
> They studied the challenges of deploying existing VLMs for this task and determined the main bottleneck that limits their capabilities is the lack of diverse, high-quality CAD datasets to train them.
>
> To remedy this, they sought to create new data to teach a model how to perform CAD generation, using a process known as data augmentation.
>
> In data augmentation, scientists typically create new data by randomly tweaking existing data to generate more samples, often by adjusting the color, size, and shape of objects in images.
>
> Instead, the MIT researchers built a data augmentation system called GIFT (which stands for Geometric Inference Feedback Tuning) that generates data designed to improve the performance of one VLM for a specific task.
>
> GIFT develops an understanding of the model’s strengths and weaknesses by testing it. Then it uses this knowledge to generate data that could improve the model’s performance on the CAD generation problems it struggles to solve.
>
> “We want to obtain data augmentation that is informed by the model itself,” Giannone says.
>
> Learning from mistakes
>
> To do this, GIFT asks the model to generate code that solves a CAD generation problem multiple times in parallel. It checks the correctness of these guesses to understand how well the model can solve this problem.
>
> “For a model, generating CAD query code that is almost correct is not that hard, but generating code that is perfectly correct and can be executed is much more challenging for a standard VLM,” Giannone says.
>
> For guesses that are nearly correct, GIFT adjusts them to become successful solutions. It saves these “near-misses” and successful solutions in a new dataset that can teach the model how to overcome problems that would usually trip it up.
>
> “If we sample the model 10 times and it generates 10 correct answers to the same problem, then there is not much for it to learn. We care about the in-between cases, where the model might only solve the problem 50 percent of the time,” he says.
>
> Using these in-between cases allows GIFT to generate data augmentations that are both model-aware and task-aware. In addition, by incorporating multiple correct solutions to the same problem, the new data expand the model’s general knowledge of CAD code generation.
>
> This automatic system does not require human intervention to correct the model’s mistakes.
>
> GIFT creates data augmentations from a pre-trained VLM using a process known as inference-time scaling. This process allows a static model, which has already been trained, to generate better outputs without the high computational costs of retraining the entire model.
>
> Using inference-time scaling, the user can determine how much computation they want to use for GIFT, tailoring it to their time and budget constraints.
>
> GIFT outperformed several competing techniques, generating CAD programs that were more accurate while using only about 20 percent as much computation. The CAD models generated by VLMs using GIFT were better aligned with the shapes of ground-truth models.
>
> “With GIFT, we started with geometry because with engineering problems, if the geometry of a 3D shape is not correct, nothing else will be correct, but there are many other aspects to consider,” Giannone says.
>
> In the future, the researchers want to expand GIFT so the framework can teach models to generate CAD programs that improve the performance and manufacturability of 3D models. They also want to apply the system to larger models and more diverse CAD generation tasks.
>
> This research was funded, in part, by the MIT-IBM Computing Research Lab.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。