---
title: "Looking beyond natural sequences"
date: 2026-08-28T04:33:19+08:00
draft: false
entry_kind: "auto"
tags: ["机器学习", "Research", "Biology", "Proteins", "Biological engineering", "Artificial intelligence", "Machine learning", "Computer science and technology"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:b05485cadc655927420ec9d220469b393c7b15d49209e60a5ff4559f3042d04d"
source_payload_sha256: "sha256:c5b01c81e2daf03f0fc40120678a6487956522f7ab4924e1dead126fde82518c"
observation_id: obs_6116da9c839ce21791a2b2ad6c48476a554224d32ffffb3eff24f8e9267b382e
event_id: evt_abc2bd6003f23d1354dc716a3731840940661f2bf3e46d7bedbeebb20ce45476
revision_id: rev_5531cb7a5d8d65869e6212edff29f5a567b392a4ddcffc43aae0b4709eb6fe08
source_published_at: 2026-08-27T19:20:00Z
first_seen_at: 2026-08-27T20:42:03Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 32
interpretation_sha256: "sha256:3fb6cecb61548c0ff0ce3f55206f83d6bd85c4beb6f1f65819731e54baf32edc"
description: "这条内容介绍了一种名为 PottsMPNN 的新型机器学习框架，它将支配蛋白质结构的物理原理整合进序列生成过程，从而更准确地评估序列能量关系并预测突变对稳定性的影响。"
external_url: https://news.mit.edu/2026/looking-beyond-natural-sequences-0827
parent_observation_id: null
last_seen_at: 2026-08-31T00:00:00Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://news.mit.edu/2026/looking-beyond-natural-sequences-0827](https://news.mit.edu/2026/looking-beyond-natural-sequences-0827)
- **发布域名**: news.mit.edu

## 要点解读

### 这是什么  
这条内容介绍了一种名为 PottsMPNN 的新型机器学习框架，它将支配蛋白质结构的物理原理整合进序列生成过程，从而更准确地评估序列能量关系并预测突变对稳定性的影响。

### 用在哪里  
适用于蛋白质设计的研究者和工程师，特别是在需要设计全新结构、摆脱天然序列限制的场景，如合成生物学、酶工程或药物候选蛋白的开发。

### 可以推断的  
推测：利用该框架，研究者在设计非天然蛋白质时可以更自信地评估其结构可行性，减少实验验证的次数。  
推测：框架对序列能量关系的更精确建模，可能提升对突变影响稳定性的预测精度，从而帮助定向进化实验的设计。

## 来源摘要/节选

> A protein’s function is determined by its structure, and structure — the way a protein folds — is determined by its sequence of amino acids, the building blocks of proteins.
>
> Many methods for designing novel proteins, including examples that could bind to a disease-causing molecule in our cells, involve a two-step process: The structure comes first, and then a machine-learning framework generates a repertoire of sequences that could potentially adopt that structure.
>
> In nature, many different amino acid sequences can fold into the same structure. At the same time, one amino acid sequence can potentially adopt different structures depending on the protein’s flexibility or a functional trigger. Therefore, when researchers use artificial intelligence to design new proteins, the challenge is to guide AI to “see” that there are many potentially useful answers — that many sequences can adopt the same fold
>
> “For years, the field has measured success by asking whether a model can reproduce the protein sequence that evolution happened to select — our work shows that this isn’t the best metric for protein design,” says Amy E. Keating, Department of Biology head, Jay A. Stein (1968) Professor of Biology, professor of biological engineering, and senior author of a paper recently published in PNAS.
>
> PottsMPNN, a new machine-learning framework developed in the Department of Biology, incorporates the physical principles that govern protein structure and stability, improving sequence generation and the ability to predict how mutations will affect a protein’s stability. In other words, the model has a better understanding of the sequence-energy landscape, meaning the relationship between the identity of each amino acid and the stability of the protein.
>
> Adding this framework to a protein design pipeline will allow researchers to design structurally feasible proteins with sequences that don’t resemble those of any native protein.
>
> “If we’re thinking about a completely novel, designed structure, there would be no native sequence to compare it to,” says graduate student and lead author Foster Birnbaum. “What we actually care about is how likely the generated sequences are to fold into the desired structures, how well the model understands the sequence-energy landscape, and how well it can predict the effect of mutations on the stability of the protein.”
>
> Beyond the noise
>
> In the same way that AI has recently powered some dramatic social changes, so too has machine learning impacted the pace and breadth of fundamental biological research. Only recently has it become possible to reliably use a computational model to generate a protein structure or sequence. Perhaps the most widely used model today, however, was released in 2022.
>
> “For a field that’s moving as fast as machine learning in biology, that model has not been surpassed — we’ve been trying to understand why that is, and what it is about that model that makes it so useful,” Birnbaum says.
>
> Birnbaum was first interested in strategic applications of something researchers call “noise,” or adding variations to a protein structure during training. Noise decreases the tendency of the model to overly mimic native sequences, increasing the diversity of structures for which it’s able to generate sequences.
>
> PottsMPNN also uses a pairwise distribution to capture interactions between amino acids. The ability to account for the physical interactions between all 20 possible sequence options at a pair of positions in the protein is a key reason that PottsMPNN more accurately models the sequence-energy landscape than other methods.
>
> Finally, Birnbaum says, they introduced sets of evolutionarily related sequences into training the PottsMPNN framework to teach the model how different sequences can adopt the same folded structure.
>
> Birnbaum acknowledges that in trying to shift away from adhering to native sequences, incorporating evolutionary information is, in some ways, still a reliance on them. But PottsMPNN succeeded in demonstrating that as the model depends less and less on native sequences, structural compatibility and energy prediction, including for novel proteins, improve.
>
> Protein design in the age of AI
>
> “Once we can design any protein we want, that enables us to do a potentially scary amount of biological engineering,” Birnbaum says. “It’s a difficult task, but I’m really optimistic about this century’s progress in biology.”
>
> Birnbaum hopes that the model could be further improved and fine-tuned for a specific task, which has in the past led to better predictions, for example, on the outcome or consequence of a particular mutation.
>
> Ultimately, according to Keating, “Our methods move the field toward designing useful new-to-nature proteins for diverse applications while providing a stronger foundation for future advances.”

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。