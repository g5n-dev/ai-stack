---
title: "How to predict the behavior of molecules from scant data"
date: 2026-11-07T04:54:51+08:00
draft: false
entry_kind: "auto"
tags: ["机器学习", "Research", "Drug discovery", "Chemical engineering", "Artificial intelligence", "Machine learning", "Chemistry", "School of Engineering"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:9768bd46faa1bab8a6d7ad231ce6c8b3446a39234d87e49f3a9eb82ae2d3c3db"
source_payload_sha256: "sha256:ed7b7e66a272a873389998ed7a418d97c864dddaf0c2eab6553880a03bc90b11"
observation_id: obs_0bb49f96544d94ecd80e77ab083459a74cffd73257f1c75429a36d100ed1f6b6
event_id: evt_cd3561f842c0907333a36b94ffc5aa11142644d97c075c4b3bddf3879ff2a85e
revision_id: rev_969058541a9dbddec845bafc8dc819f9fd58b6b952593ffc410b6293a7822d6d
source_published_at: 2026-11-06T19:00:00Z
first_seen_at: 2026-11-06T21:05:41Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 56
interpretation_sha256: "sha256:2ec12a250a3bc7578af47b5495c1e126339a3e188314bdb637204c0c3a97dc51"
description: "MIT 团队提出分子性质预测模型 CheMeleon：通过预训练学习分子结构与化学描述符之间的关系，再用少量任务数据微调，以预测溶解度、黏度、生物活性等性质。"
external_url: https://news.mit.edu/2026/how-to-predict-molecule-behavior-with-scant-data-1106
parent_observation_id: null
last_seen_at: 2026-11-09T00:00:00Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://news.mit.edu/2026/how-to-predict-molecule-behavior-with-scant-data-1106](https://news.mit.edu/2026/how-to-predict-molecule-behavior-with-scant-data-1106)
- **发布域名**: news.mit.edu

## 要点解读

### 这是什么
MIT 团队提出分子性质预测模型 CheMeleon：通过预训练学习分子结构与化学描述符之间的关系，再用少量任务数据微调，以预测溶解度、黏度、生物活性等性质。

### 用在哪里
它适用于药物和材料研发中需要筛选候选分子的场景，尤其适合目标性质数据较少、实验合成与测试成本较高时。模型基于 ChemProp 开源，可供制药企业及研究人员使用和调整。

### 可以推断的
- 推测：相较每次从零训练模型，少样本微调可能更适合数据积累不足的研发早期阶段。
- 推测：开源工具和多家制药公司的实际采用，可能降低团队试用并评估这类预测模型的门槛。

## 来源摘要/节选

> Discovering new molecules for specific uses is a major driver of progress in a wide variety of industries, whether it’s pharmaceutical companies looking for new drugs, or electronics or energy companies seeking new materials with particular properties. But it’s also largely a trial-and-error process, because there is not yet any way to perfectly predict how a given chemical compound will behave in terms of the myriad different properties and responses materials can exhibit.
>
> Recent progress has been made on using artificial intelligence and machine learning to supplement or speed up laborious calculations based on physical principles that can at least provide some initial guidance on which compounds might be worth synthesizing and testing. Now, a new method developed at MIT shows that when there are few data on some technologically relevant property, such as ligand affinities for a recently discovered cellular target for a potential drug, this approach can outperform other existing methods for winnowing down the field of possible molecules that might be worth looking at.
>
> The findings were reported in the Sept. 14 issue of the Journal of Chemical Information and Modeling, in a paper by MIT graduate student Akshat Shirish Zalte and recent graduate Jackson Burns PhD ’26, Research Scientist Charlles Abreu, Professor William Green, and three researchers from the chemical company BASF.
>
> An earlier version of the paper has been online since last year, and the open-source model the team developed, called CheMeleon, has already found regular use by several pharmaceutical companies. CheMeleon was built using ChemProp, an open-source machine-learning package also developed and maintained by the Green group at MIT, and anyone can download CheMeleon through ChemProp and fine-tune it for their own purposes.
>
> Earlier this year, there was a contest organized by OpenADMET for trying to predict the properties of a variety of new molecules that had not previously been synthesized, says Green, who is the Hoyt Hottel Professor of Chemical Engineering. “It was a big contest, a lot of people participated,” he says. When the winners were announced, it turned out that nine of the top 20 entries had used CheMeleon in their process. “So then we started getting all kinds of inquiries from the pharma companies about this, but our paper had just been submitted; it wasn’t even peer-reviewed or anything yet.”
>
> While the paper went through that review process, its influence was already spreading. At least one pharma company, Green says, “sent a message to all their people, and said ‘Anytime you’re modeling a property, start with CheMeleon, that’s our new company policy’” when making initial decisions about which molecules to pursue.
>
> The key to CheMeleon was pre-training a machine-learning model with detailed data about a million different molecules, so that it gets to learn correlations between the structure of a given molecule and how it behaves with respect to a catalog of about 1,600 descriptors that have been developed by chemists over decades. CheMeleon can then be fine-tuned to predict well-known properties like solubility and viscosity, to more esoteric properties such as bioactivity or reactivity, with a certain protein or enzyme.
>
> Those million molecules are a minuscule fraction of the innumerable ways that atoms can bond together, but they provide enough examples so that once the AI system has been trained on them, it can work out on its own many underlying patterns and relationships, and then apply those to a new, unknown molecule that’s presented to it.
>
> “Most of today’s deep-learning models require more data than traditional methods,” says Zalte. Some successful models use extensive data from the published literature in chemical journals, he says. “We don’t look at the literature at all. We just calculate a bunch of molecular descriptors like molecular weight or number of oxygens, among others.” Then predicting those descriptors forms the basis for their pre-training task.
>
> CheMeleon is a pre-trained foundation model. Inspired by the well-known foundation models in language such as ChatGPT and Claide, which essentially are developed by feeding them massive amounts of information from the internet, CheMeleon uses molecular descriptors of a million molecules from PubChem, a large, freely available database of chemical information maintained by the U.S. National Institutes of Health.
>
> With classical expert-driven models, on the other hand, specialists in a field manually input detailed knowledge about their subject. In developing these classical models, he says, for example, people know from experiments that a certain property of interest, say solubility, may relate to particular descriptors of the same molecules, “like molecular weight, or the number of oxygens that are present, or how branchy or bulky the molecule is.”
>
> With this team’s approach, they can start with an existing neural network architecture and train it to learn underlying principles. “We’re not training it for a specific property, but as a general model that understands some level of chemistry, so that even if you fine-tune it with just a few data points for the task you care about, you can still get some good performance,” he says. That’s thanks to the fact that the model is “not having to learn everything from scratch.”
>
> To verify its usefulness, “We compared our model not only against other foundation models that are out there, but also with classical models leveraging expert-designed principles,” Zalte says. Comparing its performance across 58 test cases, “we see that our model comes out on top.”
>
> Green adds, “The CheMeleon foundation model drastically reduces the number of molecules that need to be tested experimentally to accurately predict the properties of new molecules. This is a huge advantage, since synthesizing and testing a large number of molecules is slow and expensive."
>
> Besides the MIT members, the team also included Jochen Sieg, Christian Feldmann, and Miriam Mathea, researchers at BASF SE in Germany. The work was supported by the Machine Learning for Pharmaceutical Discovery and Synthesis consortium, along with fellowship support from U.S. Department of Energy and MathWorks.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。