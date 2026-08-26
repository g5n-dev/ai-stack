---
title: "Generating scenarios for extreme events, without extreme data"
date: 2026-08-25T17:53:20+08:00
draft: false
entry_kind: "auto"
tags: ["机器学习", "Prompt 工程", "Research", "Algorithms", "Natural disasters", "Weather", "Computer modeling", "Climate"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:f5d819c0549035094fef11ca74de2e6e8f5599c31f2a9d9cfa18c41d7b8009d8"
source_payload_sha256: "sha256:e3235aa8b1ebd66bc99753aec7bd5a59c0e98d69eb658ea9fdb6e0bae94bb36a"
observation_id: obs_d9b6e80ff3477f595cdba27dc23f8bcccc2b24c016f80eb652966d0818308ac9
event_id: evt_fde1d175a10d34e488bbb70e53cb71df9ba26e4927defa55bff4ca85aa16de50
revision_id: rev_4001bb0b0668d85d4e0be48479c25c2084a11da752415f8fd5ef33a8d603b3c3
source_published_at: 2026-08-24T18:00:00Z
first_seen_at: 2026-08-26T14:06:23.693434Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 61
interpretation_sha256: "sha256:fba288dfaa8d79d75c2c0fa1772a46fb1218bc739ceb9f547264afdc9de1777e"
description: "这是一套基于机器学习的算法，能够在缺乏历史极端事件数据的情况下，依据日常气象记录和空间分布图，生成未来可能出现的情景及其强度、持续时间和影响范围。"
external_url: https://news.mit.edu/2026/generating-scenarios-extreme-events-without-extreme-data-0824
parent_observation_id: null
last_seen_at: 2026-08-26T00:00:00Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://news.mit.edu/2026/generating-scenarios-extreme-events-without-extreme-data-0824](https://news.mit.edu/2026/generating-scenarios-extreme-events-without-extreme-data-0824)
- **发布域名**: news.mit.edu

## 要点解读

### 这是什么
这是一套基于机器学习的算法，能够在缺乏历史极端事件数据的情况下，依据日常气象记录和空间分布图，生成未来可能出现的情景及其强度、持续时间和影响范围。

### 用在哪里
适用于城市防灾规划、电力系统韧性评估、应急资源部署等需要评估罕见自然灾害的场景，也可用于金融市场等非气象领域的极端波动研究。

### 可以推断的
推测：算法在训练时仅依赖常规数据而不需要极端记录样本，因而可以在数据稀疏的地区或新兴领域部署。  
推测：通过结合点统计和空间映射，生成的极端情景能够提供大小、强度和影响范围的近似估计，帮助决策者进行最坏情况的预案演练。

## 来源摘要/节选

> Can a city’s seawall stand up to a blockbuster storm? Will a region’s power grid hold against record-breaking heat? And can a town’s fire-fighting resources contain a major wildfire?
>
> To answer these questions, communities will first need to know how such extreme events could unfold. How far is a wildfire likely to spread? How much of a region might a storm impact? How long could a heat wave last?
>
> But extreme events are notoriously difficult to anticipate. By their nature, they are outliers. In the history of record keeping, extreme events are sporadic and rare. Yet most methods that assess a region’s risk depend on extreme events of the past to characterize even more extreme, worst-case scenarios in the future.
>
> Now, MIT engineers have developed a tool that generates plausible extreme events and worst-case scenarios, and maps their characteristics, such as an extreme storm’s likely duration, intensity, and area of impact. The key to their method is that it does not need to know about previous extreme events in order to generate plausible future extreme events.
>
> Instead, the method, in the form of a machine-learning algorithm, learns from a dataset, such as a region’s daily weather records and maps. This record may or may not contain past extreme deviations, such as record-setting heat or rain. The team’s algorithm takes a statistical approach to learn from the available data, to exclude implausible weather scenarios. The method then generates plausible extreme events that are likely to occur in a region with a given frequency (such as once every 100 years), and projects how those extreme events might look in terms of their size, intensity, and duration.
>
> “We are trying to model extreme, unprecedented events that no one has seen before, that are not in the dataset,” says Kai Chang, an MIT graduate student in mechanical engineering and affiliate of the MIT Center for Computational Science and Engineering.
>
> “An event like Hurricane Katrina is something that happens every 30 to 40 years,” adds Themis Sapsis, the William I. Koch Professor of Mechanical and Ocean Engineering at MIT, a core member of the Center for Computational Science and Engineering, and an affiliate of the MIT Institute for Data, Systems, and Society. “What will be the Katrina that happens every 100 years? How bad will it be? That’s exactly what we’re trying to quantify, to help planners prepare for plausible extreme scenarios.”
>
> Beyond weather events, the approach, which the team has dubbed Extreme Event Aware, or “η-learning,” can be applied to other fields, such as robotic navigation and financial markets.
>
> “Financial market crashes are extreme events that are a complicated combination of things, involving many different sectors,” Chang says. “What is the interaction that leads to a market crash? That is something that this method could explore.”
>
> Sapsis and Chang detail their new method in an open-access paper that appeared on Aug. 20 in the journal Nature Communications.
>
> “Riskier than everything”
>
> To estimate a region’s risk of an extreme weather event, planners, policymakers, and insurance companies typically ask questions such as “What does a once-every-100-year storm look like for New York City?” For answers, they use computer simulations that must be trained on data that includes extreme, once-in-a-century events, in order to learn the conditions leading up to those events and generate scenarios of how those events might look in the future.
>
> “These methods assume there are very disastrous events that we have seen in the dataset, and they build a method to either estimate the risk of those events, or they try to predict exactly the events that have happened,” Chang says. “We are trying to see: What do unprecedented extreme events look like that are riskier than everything that has happened before and yet are still plausible?”
>
> For example, if the most extreme rainfall measurement ever recorded in New York City is 200 millimeters, what kind of storm would produce an even more extreme measurement, of 300 millimeters? Such an event has never been recorded before and yet could still be plausible. City planners would want to know where such a storm would hit, how big an area it would cover, and how intense it would be. A simulation of the storm could help them assess infrastructure and plan reinforcements.
>
> “We want to predict maps of these worst-case scenarios,” Sapsis says. “There is no method that does this efficiently to predict events that happen rarely.”
>
> Extreme learning
>
> The team’s new algorithm generates plausible, unprecedented extreme scenarios, without needing to train on previous extreme event data. To do so, the algorithm combines and learns statistics, or probabilities, about the relationships between two types of data: point statistics and spatial maps.
>
> To demonstrate, the researchers applied the method to generate maps of future extreme precipitation events over the continental United States. The researchers began with 25 years of hourly precipitation maps, which they pooled into daily maps. From the full record, they computed point statistics describing how often the maximum rainfall across a map reached a given level. They then trained the algorithm on paired low- and high-resolution spatial maps from just the first six months of the record, which contained few or no examples of the most extreme rainfall levels.
>
> From these data, the algorithm learned how patterns in low-resolution maps correspond to detailed, high-resolution precipitation maps. It then used the point statistics to constrain the rainfall extremes represented in those maps. This combination enables the algorithm to generate plausible spatial patterns for events more extreme than those represented in the training data — for instance, the possible locations, sizes, and intensities of a once-in-a-century rainfall event with a maximum of 300 millimeters.
>
> A user can prompt the trained algorithm with a question such as, “What could a once-in-a-century storm look like in New York City?” The algorithm then generates maps of statistically plausible storms that are likely to occur with that frequency, including characteristics such as the storm’s size, area of coverage, and intensity of rainfall.
>
> “Someone can say, ‘I’m interested in building things to withstand the risk of an event that happens every 100 years,’” Chang says. “What we can do then is produce thousands of possible realizations that will happen with this sort of rare frequency.”
>
> As long as relevant point statistics and spatial data are available, the method could be applied to visualize other unprecedented events such as extreme floods and wildfires.
>
> “Extreme events have become a strategic concern, not just an environmental one — we’ve optimized global systems for efficiency, and the price of that efficiency is that there’s very little slack left anywhere. A single extreme event propagates through supply chains, energy markets, and food systems in weeks,” Sapsis says. “Being able to put a probability on an event that hasn’t happened yet is now a question of national and economic resilience.”
>
> This research was supported, in part, by a Vannevar Bush Faculty Fellowship and the U.S. Air Force Office of Scientific Research.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。