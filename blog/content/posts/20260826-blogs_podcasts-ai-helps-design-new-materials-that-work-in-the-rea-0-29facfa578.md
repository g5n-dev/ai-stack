---
title: "AI helps design new materials that work in the real world"
date: 2026-08-26T18:00:42+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "生成式 AI", "机器学习", "Research", "Artificial intelligence", "Machine learning", "Materials science and engineering", "Chemistry"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:dc0cca203a2c71a1df35b5b7fced76be89d78e49b30537f7f44ffe2699047975"
source_payload_sha256: "sha256:3eb4ef0108d07aa9412e54a0540b23528ee4b9480712b346c6b71f490322c1f7"
observation_id: obs_29facfa5780b28e748135a3ad0a66e4a2dfde9542859e17fafb22ff121d859e7
event_id: evt_b185088996d8e72549767c53877f6b19489ac61361e9abaf9d78d8daa734767c
revision_id: rev_40e54853892a8ffe33a823c41e30257e9cffe7c0a98b80a045d27cb05d1ff009
source_published_at: 2026-08-26T09:00:00Z
first_seen_at: 2026-08-26T09:57:42.227189Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 57
interpretation_sha256: "sha256:69e9ffb5a35d04694c0e8509de0dc608c0a535c7c37d4424dc3ebfad1ff4fff4"
description: "该内容介绍了麻省理工学院研发的一种材料生成框架，在生成前加入价电子壳层约束，以提升生成材料的化学稳定性，并可在保持目标性能的同时显著降低不稳定材料的比例。"
external_url: https://news.mit.edu/2026/ai-helps-design-new-materials-that-work-in-real-world-0826
parent_observation_id: null
last_seen_at: 2026-08-26T09:57:42.227189Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://news.mit.edu/2026/ai-helps-design-new-materials-that-work-in-real-world-0826](https://news.mit.edu/2026/ai-helps-design-new-materials-that-work-in-real-world-0826)
- **发布域名**: news.mit.edu

## 要点解读

### 这是什么
该内容介绍了麻省理工学院研发的一种材料生成框架，在生成前加入价电子壳层约束，以提升生成材料的化学稳定性，并可在保持目标性能的同时显著降低不稳定材料的比例。

### 用在哪里
适用于需要快速筛选出可用材料的研究团队或企业，尤其是在计算资源有限的情况下进行高性能材料（如高热导率或高介电常数材料）的设计。

### 可以推断的
推测：该技术如果与现有的扩散模型或大语言模型结合，可减少后期筛选的计算成本。  
推测：在材料研发周期紧张的领域，如半导体和航空，可能率先采用该方法以加速产品开发。

## 来源摘要/节选

> Today, anyone with a large enough artificial intelligence model can generate millions of new material designs in minutes. Unfortunately, that hasn’t led to a huge leap in the number of new materials being used to improve the performance of products like computer chips and rockets.
>
> One reason for the translation gap is that current models don’t reliably factor in the chemical stability of the materials they generate, and unstable materials aren’t very useful in the real world. That forces industries to allocate huge computational budgets to screening out all the unstable materials they generate, in some cases leaving behind a tiny fraction of usable options.
>
> Now, MIT researchers have developed a framework that can be applied at the beginning of the materials generation process to vastly improve the stability rate while achieving targeted material properties. It works by ensuring every design satisfies certain key rules of chemistry relating to the electrons around the materials’ atoms before the expensive generation step begins. The researchers call their approach “crystal generator with valence-constrained design, or CrysVCD.
>
> In a paper published today in Nature Computational Science, the researchers show how CrysVCD allowed several commonly used material models to meet those valence shell rules more often, and used it to achieve high lattice-dynamics stability — a stringent stability test — in nearly 70 percent of computational material generations. They also showed the approach could support the creation of materials with specific desired properties, like high thermal conductivity or high dielectric constant, which is important for computer chips and data centers.
>
> A hint of how the researchers envision people using their system is in the name.
>
> “If material-generating models are like DVDs, we are like the DVD player,” says associate professor of nuclear science and engineering Mingda Li. “You can plug this into any kind of model, not only existing diffusion models but also future models, where people can’t generate enough stable materials, and it can improve stability.”
>
> Joining Li on the paper are Mouyang Cheng SM ’26 and Weiliang Luo, MIT doctoral students in materials science and engineering and chemistry, respectively; Hao Tang PhD ’26, a recent graduate in materials science and engineering; Bowen Yu, a senior undergraduate in physics; Yongqiang Cheng, a staff scientist at the Oak Ridge National Laboratory; Weiwei Xie, an associate professor at Michigan State University; Ju Li, MIT’s Carl Richard Soderberg Professor in Power Engineering; and Heather Kulik, MIT’s Lammot du Pont Professor of Chemical Engineering.
>
> More efficient materials
>
> Computational approaches to materials design have been around for decades, but recent advances in artificial intelligence have increased excitement about their potential. Of particular interest are models that can start with a desired material property and work backward to deliver a material that achieves that goal.
>
> Some of those models use an AI technique known as diffusion, which is commonly used to generate images, while others use large language models like the one powering ChatGPT and Claude, but both approaches struggle to ensure their material generations achieve chemical stability or follow fundamental principles about how chemicals interact and behave.
>
> The solution has been to add another layer of computing on top of the generative process to filter out unstable materials.
>
> “It’s becoming easy to generate the material structure,” Cheng says. “But the validation process, especially the part where you test the stability, has a huge computational cost. It’s something like 90 percent of the computational cost for creating usable materials, and it can take weeks or months.”
>
> Big companies with huge computing budgets can afford to run those processes, but many small companies and research labs can’t, potentially limiting innovation in the field.
>
> “In academia, where we have fewer resources, I think we can still achieve strong performance with smarter designs and other approaches,” Kulik explains. “Generating a model and then down-selecting for stability is inefficient. There’s a high computational cost. But if we put a language model in the beginning of the process to constrain the generation, you can significantly enhance the ratio of stable materials generated.”
>
> The new study involved MIT researchers affiliated with the departments of Materials Science and Engineering, Chemistry, Chemical Engineering, Physics, and Nuclear Science and Engineering. Together the researchers combined AI diffusion models with a language model. In the first stage of their process, the language model produces chemically valid formulas. In the second stage, the diffusion model uses that formula to generate the corresponding atomic structure of the crystal material in coordination with the underlying material generation model.
>
> “Diffusion for typical material generation is a slow process — you can think of it like 1,000 steps to create one material,” Luo says.
>
> “In contrast, when our model is used in the beginning, you can think of it like five steps. It allows you to screen out the unstable materials to generate higher quality materials. And it works with any models generating materials,” Tang adds.
>
> The researchers showed their approach created more stable materials an order of magnitude more efficiently than approaches that rely on screening materials after they’re generated. When fine-tuned on stability metrics, their approach produced crystalline materials that achieved 68 percent mechanical stability and 85 percent metastability, which measures if a material stays in a stable state when undisturbed.
>
> The researchers then used their approach to generate material candidates with high thermal conductivity and easy polarization in an electric field.
>
> “These are materials useful for the semiconductor industry and high thermal conductivity materials relevant to data center cooling,” Ju Li says. “In principle, you could also use this to create other properties, but thermal conductivity has become really important for cooling data centers. There’s been a huge increase in energy use in that industry, and 30 percent of that energy goes to cooling. The industry needs materials with high thermal conductivity to more efficiently remove the heat.”
>
> Democratizing material design
>
> The new approach doesn’t work with every kind of material — it works best with solid structures with highly ordered internal arrangements. Still, the approach could be used to generate stable new crystalline materials with a host of important properties.
>
> “We are not just generating stable materials, we’re also prioritizing performance,” Cheng says. “Any time you have two goals, achieving those goals with anything over 50 percent is hard in this field. In the past, people might have a goal for specific properties and not stability, or vice-versa, and get a single-digit percentage of materials that fit their goal.”
>
> Ultimately the approach will enable more researchers to develop novel materials for a range of next-generation applications.
>
> “This will save huge computation costs and time by removing downstream selection requirements,” Li says. “That will help not only large efforts that generate hundreds of millions of materials, but also smaller research groups with targeted applications.”
>
> The work was supported, in part, by the U.S. Department of Energy, a Mathworks Engineering Fellowship, the National Science Foundation, and the U.S. Defense Threat Reduction Agency.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。