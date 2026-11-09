---
title: "A single AI model simulates the behavior of many substances, from sliding sand to folding proteins"
date: 2026-11-09T15:59:24+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "机器学习", "Research", "Computer modeling", "Artificial intelligence", "Machine learning", "Simulation", "Computer graphics"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:007eaa4f98efd57120eda339e4e57b06b7b447f0f7642894b244cc41db9eca29"
source_payload_sha256: "sha256:9a5904bd4a657f17d777eaf0616c60d9a005c4180d7e511fa052bf8151b6c211"
observation_id: obs_6fbb9cbc09ce7eb4c3adf9c43170af03eb13ba8f72ea96e438a6243b06de5665
event_id: evt_c265cbb25069ba4eea5df948a7cd685a8d2aaa62b4f181aff675ed6dd0fb5c1e
revision_id: rev_ac233a0d6f32b3433418a3d6c97b74a62a77f2b19ba04dfffd5f4ec5ec0d9907
source_published_at: 2026-11-09T05:00:00Z
first_seen_at: 2026-11-09T07:57:50.583586Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 98
interpretation_sha256: "sha256:efed9ebb68de5a7a22fa25237fa4f52cb746ff4f17fcd1fe3da741eb41585333"
description: "WorldParticle 是 MIT、UBC 等研究者提出的统一深度学习模拟系统。它把材料与物理过程表示为三维粒子，学习粒子运动规律，并预测后续状态，无需为每类过程单独编写求解器。"
external_url: https://news.mit.edu/2026/single-ai-model-simulates-many-substances-behavior-1109
parent_observation_id: null
last_seen_at: 2026-11-09T07:57:50.583586Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://news.mit.edu/2026/single-ai-model-simulates-many-substances-behavior-1109](https://news.mit.edu/2026/single-ai-model-simulates-many-substances-behavior-1109)
- **发布域名**: news.mit.edu

## 要点解读

### 这是什么
WorldParticle 是 MIT、UBC 等研究者提出的统一深度学习模拟系统。它把材料与物理过程表示为三维粒子，学习粒子运动规律，并预测后续状态，无需为每类过程单独编写求解器。

### 用在哪里
它适用于流体、可变形物体、颗粒材料和蛋白质等跨类别物理模拟，例如分析晃动的油对弹性阀门的作用，或软体机器人接触沙土后的材料运动。科研人员和工程师可借此探索新材料及复杂物理过程。

### 可以推断的
- 推测：统一架构有望减少不同仿真器之间的切换与重复建模成本，尤其适合需要耦合多种物理现象的工程问题。
- 推测：若预测精度与可扩展性在更多条件下成立，这类方法可能成为通用物理模拟基础模型的一部分，但仍需针对具体工程场景验证。

## 来源摘要/节选

> Today, a scientist who wants to simulate a physical process must pick the right tool for that one job, such as a solver built for flowing water or another designed to model the way a protein folds. Each one is hand-coded around the specific equations that dictate how that process behaves.
>
> Researchers at MIT, the University of British Columbia (UBC), and elsewhere have now replaced that patchwork with a single deep-learning system, called WorldParticle, that could help engineers model different physical phenomena, from sliding sand to folding proteins, with one unified artificial intelligence architecture.
>
> Scientists and engineers could use this system to model processes that typically require separate simulators, such as a fluid sloshing against a deformable solid. This could offer a faster, more accurate way to simulate how sloshing oil might impact an elastic valve in a storage tank, for instance. It could also help engineers study where and how granular materials, like sand or soil, could move when a soft robot touches them.
>
> The system represents every material it simulates, from a dune of sand to a protein molecule, as tiny particles and predicts where those particles will move one step at a time. Because it learns the underlying dynamics rather than being programmed with an equation, the model can adapt to materials, forces, and environments it never encountered during training.
>
> In the long term, the researchers hope this work helps scientists discover new materials and explore physical processes they would be unable to effectively study with existing simulation methods.
>
> “We want to have a GPT moment for simulation,” says Peter Yichen Chen, a former MIT postdoc who is now an assistant professor at UBC, and is a co-corresponding author of an open-access paper on this technique. “Every time people want to build a simulator for a particular physical phenomenon, they need to code it up from scratch. Our vision is to have a foundation model that works out of the box for any scenario you want to simulate. This is a first step in that direction.”
>
> Chen is joined by co-corresponding and co-lead author Minghao Guo, an MIT postdoc; co-lead authors Caoliwen Wang and Siyuan Chen, UBC graduate students; Wojciech Matusik, an MIT professor of electrical engineering and computer science who leads the Computational Design and Fabrication Group within the Computer Science and Artificial Intelligence Laboratory (CSAIL); and others at UBC, Georgia Tech, Inria, Meta, the University of Pennsylvania, the University of Utah, the University of California at Los Angeles, and the University of Hong Kong. The research will be presented at the ACM SIGGRAPH Conference and Exhibition on Computer Graphics and Interactive Techniques in Asia.
>
> Unified simulation
>
> For this work, the researchers drew inspiration from world models. These powerful AI systems learn the rules that govern the physical world so they can predict how objects or environments will change over time in response to certain actions or conditions.
>
> The researchers applied these concepts to develop a unified AI architecture that can simulate multiple types of physical phenomena.
>
> “If you study deformable objects and fluids, you would need two simulators — one for each physical regime. But if you unify them into one model, maybe you could couple the physics of these two processes and gain insights into new problems?” Guo says.
>
> WorldParticle breaks an object into thousands or millions of tiny, three-dimensional dots, or particles, using what is known as a Lagrangian representation. It tracks the movement and velocity of the particles over space and time to simulate the material’s dynamics.
>
> Typically, when scientists model materials and physical processes using Lagrangian particles, they use a governing equation that defines the fundamental laws which control how that material behaves over time and space. They must convert that complex equation into a formula a numerical solver can handle, repeating these steps for each material and process they want to model.
>
> Instead, the researchers designed a neural network that learns to solve governing equations in general, eliminating the need to design a new model and solver to handle each one.
>
> Once WorldParticle converts an object into particles, a neural network takes the 3D positions and physical properties of the particles as inputs. It outputs their positions and properties for the next frame of the simulation, predicting the material’s motion over time and space in one-second increments.
>
> “It is a similar architecture to ChatGPT. But instead of predicting one word at a time to write a piece of text, we are predicting how these particles will move, one step at a time,” Chen says.
>
> Before each simulation step, WorldParticle separates the external forces that affect the physical system, like impulse forces that affect an ocean wave when it slams into a seawall.
>
> After predicting the initial states of the particles, WorldParticle integrates the external forces back into the simulation, correcting its particle predictions based on how those forces affect the object’s behavior. In this way, the system can generalize to unseen materials, changing environmental conditions, and varied forces.
>
> A general, scalable framework
>
> But because a complex object could be broken into millions of particles, the problem quickly becomes too computationally intensive for the model to handle.
>
> To streamline processing, the researchers employed a merging technique to combine and compress particles while still allowing WorldParticle to capture fine-grained details of their behavior.
>
> “We needed to do a lot of detailed engineering and employ many tweaks to the architecture for it to be truly generalizable and scalable,” Guo says.
>
> They demonstrated WorldParticle by modeling six different physical phenomena, including deformable objects, granular materials, and proteins, with higher accuracy than numerical simulation methods.
>
> For instance, WorldParticle effectively captured how a granular object would collapse into a pile while some baseline methods left sand particles floating in the air. Their method also modeled how protein structures change over time about 100 times faster than numerical simulators, Guo adds.
>
> The general-purpose framework could be applied to many materials and processes, including soft robot manipulation tasks, RNA evolution, and astrophysical phenomena like the merging of galaxies, the researchers say.
>
> Moving forward, they want to adapt WorldParticle to simulate these and other physical systems. They also want to build on this work toward the development of a full, general-purpose simulation pipeline for scientific discovery.
>
> “We see the unification of computation and science giving us new insights and tools to discover physical phenomena or explain some unexplainable physical phenomena,” Guo says. “With a unified model, we could unlock many discoveries that we can’t even imagine.”

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。