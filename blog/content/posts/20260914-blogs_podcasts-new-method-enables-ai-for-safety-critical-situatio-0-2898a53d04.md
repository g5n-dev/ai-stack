---
title: "New method enables AI for safety-critical situations"
date: 2026-09-14T14:19:02+08:00
draft: false
entry_kind: "auto"
tags: ["生成式 AI", "机器学习", "Research", "Computer science and technology", "Artificial intelligence", "Machine learning", "Algorithms", "Mechanical engineering"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:dc8f530e6ec4e089d083b830670f182b1926de6e4ecb7dd35bcd7f0190af0263"
source_payload_sha256: "sha256:4a93989c392aaf7f2465dbf569ab4a679316394ef3a4455cf9b83962e1a917fc"
observation_id: obs_2898a53d04394efa7e82163deffbcdb043e7687b967d92afb5df952ae466e86e
event_id: evt_f5c93b2e302d619cba3dc74f4447dea13bbb4c7b0d44687017eed93532d2a5d6
revision_id: rev_72d197e8b7822cf6b1b3b05852ec956b864a6c37c0c9a859a3da686404bbc063
source_published_at: 2026-09-14T04:00:00Z
first_seen_at: 2026-09-14T06:29:48Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 52
interpretation_sha256: "sha256:343d4ab0d28446805559be4ac51658160ea5757622267cb8b00fd78c695390a3"
description: "该技术通过在生成过程的后期才对输出施加严格约束，使预训练生成模型在不重新训练的情况下仍能满足安全、物理或任务关键的需求，同时保持较高的解决质量。"
external_url: https://news.mit.edu/2026/new-method-enables-ai-safety-critical-situations-0914
parent_observation_id: null
last_seen_at: 2026-09-15T00:00:00Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://news.mit.edu/2026/new-method-enables-ai-safety-critical-situations-0914](https://news.mit.edu/2026/new-method-enables-ai-safety-critical-situations-0914)
- **发布域名**: news.mit.edu

## 要点解读

### 这是什么  
该技术通过在生成过程的后期才对输出施加严格约束，使预训练生成模型在不重新训练的情况下仍能满足安全、物理或任务关键的需求，同时保持较高的解决质量。

### 用在哪里  
适用于机器人路径规划、物理过程控制、计算机视觉等对约束不可妥协的高风险场景，能够在部署时直接为已有模型提供可靠的约束满足能力。

### 可以推断的  
推测：在需要人机协同的制造或物流现场，这类方法有潜力降低因约束冲突导致的碰撞或失误风险。  
推测：由于无需为每种约束单独重新训练模型，开发团队可以更快地将生成式 AI 集成到安全关键的产品中。

## 来源摘要/节选

> MIT researchers have developed a new technique that helps generative artificial intelligence models find solutions to high-stakes problems.
>
> In these settings, a plausible answer is not enough: The output often must also satisfy nonnegotiable safety, physical, or task-specific requirements, known as hard constraints.
>
> The researchers developed a method that helps generative models meet these strict requirements without sacrificing the quality of their outputs.
>
> The key to their technique is to give the model more freedom during the generation process and enforce hard constraints on the final output, rather than at every intermediate step.
>
> In experiments spanning robotics, control of physical processes, and computer vision, the new method consistently satisfied the required constraints while identifying better solutions than existing techniques.
>
> This adaptable, plug-and-play technique works at deployment time, so it can be applied to pretrained generative models without retraining them. It can make such models more useful in applications where safety rules, physical laws, or other strict requirements cannot be violated.
>
> “The promise of generative AI is its ability to explore a rich space of possibilities, but the real world places boundaries on which possibilities are acceptable. Our approach lets us preserve that generative power while enforcing the nonnegotiable requirements of high-stakes or safety-critical applications,” says Navid Azizan, the Alfred H. and Jean M. Hayes Career Development Associate Professor in the Department of Mechanical Engineering and the Institute for Data, Systems, and Society (IDSS), a principal investigator of the Laboratory for Information and Decision Systems (LIDS), and the senior author of a paper on this technique.
>
> Azizan is joined on the paper by lead author Zeyang Li, a graduate student in mechanical engineering and LIDS; and Kaveh Alim, a graduate student in IDSS and LIDS. The research appears this week in the IEEE Transactions on Pattern Analysis and Machine Intelligence.
>
> Freedom to explore
>
> Pretrained generative AI models, such as diffusion models like Stable Diffusion and flow-matching models like FLUX, are now widely available. These powerful models learn to create new data by transforming random noise. Their availability has enabled people to adapt them to a wide range of applications.
>
> These highly capable models excel at providing answers that come close to satisfying most queries, but in safety-critical applications like robot path planning on a crowded factory floor, an answer that is “nearly correct” may not be good enough.
>
> For instance, a “nearly correct” path from one machine to another might still result in the robot colliding with a human co-worker.
>
> In such safety-critical applications, users often employ a technique called projection-based sampling, which repeatedly forces the model’s partial solutions, called intermediate samples, to satisfy strict requirements during the generation process.
>
> But constraining the entire generation process can prevent the model from reaching a better final solution. These methods also typically focus only on satisfying the hard constraints, missing the opportunity to improve other qualities of the solution, like reducing the length of the robot’s trajectory.
>
> “For constraint satisfaction, what ultimately matters is the model’s final output, since the internal process is discarded. By not requiring every intermediate step to satisfy the constraints, we give the model more freedom to find high-quality solutions that are still feasible in the end,” says Li.
>
> The researchers developed an algorithm called HardFlow that steers the sampling process so that the final output satisfies the user’s hard constraints without being overly restrictive and is of higher quality.
>
> Subtle steering
>
> HardFlow reformulates hard-constrained sampling as a trajectory-optimization problem, using tools from the field of optimal control. This enables the framework to steer the model’s sampling trajectory toward a goal, making subtle corrections along the way while enforcing hard constraints on the final output.
>
> “Control theory gives us a powerful framework for formalizing the optimal way of making these corrections,” Azizan says.
>
> But solving the trajectory-optimization problem around an enormous neural network was no easy task. The model may have hundreds of interconnected layers that process data.
>
> To make the problem tractable, the researchers leveraged the structure of flow-matching models to decompose the problem into a sequence of smaller, single-step subproblems. They then applied systematic transformations and approximations to derive an efficient, scalable algorithm that still finds a feasible solution.
>
> “Essentially, we transformed the trajectory-optimization problem into something that preserves the key properties of the original problem, but can be solved very efficiently at deployment time,” Azizan adds.
>
> Reformulating the task as an optimization problem allows HardFlow to incorporate additional goals that can improve the quality of the final answer. For instance, HardFlow could find a collision-free path for a robot that is also the shortest distance to its goal.
>
> “Our framework can jointly handle both aspects, which helps it perform much better than existing methods,” says Li.
>
> Across experiments in robotic manipulation, maze navigation, and text-guided image editing, HardFlow achieved perfect constraint satisfaction while consistently outperforming baseline methods on measures of solution quality.
>
> For example, it enabled a robotic manipulator to avoid collisions with obstacles while also finding the quickest path to the target object. Most other methods either resulted in collisions or found paths that took significantly more time.
>
> In addition, HardFlow’s computation time was comparable to or lower than that of most competing methods.
>
> In the future, the researchers could extend the framework to settings in which the AI model itself can also be updated, so that constraint satisfaction and sample quality can be improved in a more adaptive manner.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。