---
title: "Estimating suicide risk from text"
date: 2026-09-25T06:26:43+08:00
draft: false
entry_kind: "auto"
tags: ["机器学习", "深度学习", "Research", "Mental health", "Health care", "Medicine", "Neuroscience", "Brain and cognitive sciences"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:ed616aa527d85cb609dc5b87484b93da02c42a46eb1f1a1a42bb3be441e9cc6d"
source_payload_sha256: "sha256:d6ff30448ea229e2547ab3ee8cb0ddf7f32007874778be5e1440f580aede38f8"
observation_id: obs_972cdcddc42f338f41110cfeb5550eb2b54084fd86b369f9cc8b3bdf3b0330be
event_id: evt_c790d1b0521e1cb9b2ea380bde2b23514204157dcf6e82fd435857cc7361239d
revision_id: rev_17d6a05bd508019db976f3fa0ad1cec6e1a9a8ce6d84ce97f8256a3be0fa2b33
source_published_at: 2026-09-24T21:00:00Z
first_seen_at: 2026-09-24T22:35:58Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 33
interpretation_sha256: "sha256:23f8f582fb3ab80898abd89c50b95c65fdd957cd0a604f18f3eb26b5041e754b"
description: "这是一款基于词库的文本分析工具，能够在危机对话中快速评估自杀风险，并定位与最高风险相关的因素。"
external_url: https://news.mit.edu/2026/estimating-suicide-risk-from-text-0924
parent_observation_id: null
last_seen_at: 2026-09-26T00:00:00Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://news.mit.edu/2026/estimating-suicide-risk-from-text-0924](https://news.mit.edu/2026/estimating-suicide-risk-from-text-0924)
- **发布域名**: news.mit.edu

## 要点解读

### 这是什么
这是一款基于词库的文本分析工具，能够在危机对话中快速评估自杀风险，并定位与最高风险相关的因素。

### 用在哪里
适用于危机热线辅导员在实时文本交流时进行风险分层，也可为临床机构提供自杀风险筛查的辅助参考。

### 可以推断的
推测：该工具通过突出显示与高风险相关的关键词，有望提升危机干预的响应优先级。  
推测：虽然模型可快速打分，但仍需人工复核，以弥补词库对语境和隐喻表达的理解不足。

## 来源摘要/节选

> When people reach out during a mental health crisis, a top priority for counselors is identifying those with a high risk of suicide. The distressed person’s language holds critical clues, and a new tool developed by scientists at MIT’s McGovern Institute for Brain Research is designed to pick up on and rapidly evaluate those signals.
>
> The language-processing tool was developed by Daniel Low, a former graduate student in Senior Research Scientist Satra Ghosh’s Senseable Intelligence Group who is now a research scientist at the Child Mind Institute, where he leads its AI, Risk, and Contemplative Science Lab, as well as a visiting scholar at Harvard University. It uses a custom-built list of words and phrases linked to 49 suicide risk factors, searching text for these and using them to estimate an individual’s risk.
>
> Ghosh, Low, and colleagues report today in the Journal of Psychopathology and Clinical Science that their tool accurately predicts suicide risk from text conversations with crisis counselors. It is already helping to clarify which suicide risk factors matter most in times of crisis. With more validation, it could help with risk assessment in clinical settings and crisis-support situations.
>
> Identifying key risk factors
>
> Suicide attempts are notoriously difficult to predict. Dozens of risk factors have been linked to suicide, and even trained clinicians struggle to identify who will make an attempt among those who have some form of suicidal ideation. Among the factors that can make suicidal thoughts and behaviors more likely are certain psychiatric symptoms and disorders, like depression, borderline personality disorder, and post-traumatic stress disorder, as well as environmental and social stressors, like poverty, incarceration, discrimination, and loneliness.
>
> “You see all these 50 risk factors, and they're all interacting in ways we don't really understand,” Low says. “Many different pathways could lead to someone feeling they want to escape their internal pain,” he says — and it’s challenging to know whose path will lead to a suicide attempt or death.
>
> Ghosh and Low wanted to understand which risk factors counselors and clinicians should most look out for during a mental health crisis. To do that, they collaborated with the Crisis Text Line, whose trained volunteers provide confidential text-based support to people in distress.
>
> Crisis Text Line, a global mental health nonprofit that provides free, 24/7, confidential mental health support for people in need, provided specialized training and controlled access to this restricted dataset. The researchers analyzed de-identified texts from approximately 16,000 conversations with Crisis Text Line’s volunteer crisis counselors. Based on Crisis Text Line’s assessments, those conversations were grouped into three different risk levels: non-suicidal, suicidal ideation without imminent risk, and imminent risk. It was this imminent risk group — those with a plan for suicide, or who have an intent to die within the next 48 hours — that the researchers most wanted to understand.
>
> “We wanted to know what type of symptoms predict the highest suicide risk,” Low says. This question has been studied before, he says — but typically through epidemiological surveys that ask a person to recall their symptoms and experiences, often after their mental health crisis has passed. In contrast, he says, “Crisis Text Line gives us an opportunity to assess many different symptoms and potential risk factors as people are having the crises.”
>
> Reading between the lines
>
> Before analyzing the crisis line texts, the research team built a suicide-risk lexicon. They turned to artificial intelligence to generate a preliminary list of words and phrases tied to established suicide risk factors, including factors associated with suicidal ideation, suicide attempt, and suicide death. Then they manually reviewed and curated that list. Their final lexicon includes about 60 words or phrases for each of 49 risk factors, with the relevance of each one confirmed by expert clinicians.
>
> Then they trained a machine learning model to search the crisis conversations for words and phrases in their lexicon and use these to predict suicide risk. Because the lexicon links each word or phrase to a specific risk factor, they could use these data to determine which risk factors are most closely tied to imminent risk among people in crisis.
>
> What they found was consistent with patterns found in previous research, although not always intuitive. For example, depression is a well-known risk factor for suicidal ideation, but their model found that mentions of lethal means and substance use were more likely to be expressed by the highest-risk group than depressed mood or fatigue. Expressions of active suicidal ideation and self-injury were also strong predictors. Intermediate predictors included anxiety, post-traumatic stress disorder, and emotional pain.
>
> The predictive model assigns a weight to each risk factor based on its contribution to risk. For example, mentions of lethal means for suicide, like “cut” or “pills,” are weighed heavily, whereas terms related to hopelessness, like “don’t know what to do” or “hopeless,” contribute to a lesser degree. After training their model, the team found they could use it to accurately predict risk severity in new conversations the model had not previously seen.
>
> One limitation of lexicons, the researchers note, is that they do not consider the context of terms, and they can miss terms that are similar to those in the lexicon, but not explicitly included. Large language models have reasoning abilities, and Low and colleagues have developed ways of using large language models to detect suicide risk in other projects. However, they say they often use their lexicon in parallel to guarantee flagging certain terms, as well as to maintain data privacy.
>
> Low stresses that while the team used the power of a large language model to develop its lexicon, its prediction model is a simpler, “lightweight” model. Unlike large language models, which require massive computational power, it can be run easily on a personal computer, reducing both cost and privacy concerns. Just as importantly, it is interpretable: Rather than merely generating a risk estimate like some deep learning models can do more effectively, it tells users how it got there. Words of concern can be flagged so users understand the basis for each assessment and act on that information. They are working on similar explainability approaches with large language models.
>
> That’s critical, because the stakes are so high. “This is such a complex space that having a human in the loop is, I think, going to be critical for a long, long time,” says Ghosh, who is the director of the Open Data in Neuroscience Initiative at the McGovern Institute. Likewise, the researchers add that any predictive model must be thoroughly validated before clinical use, and might need to be continually refined to keep up with changes in language use or target populations.
>
> Because a reliable lexicon opens doors to new ways of understanding mental health, Ghosh and Low are widely sharing not just their suicide risk lexicon, but also the software package they developed to build it. Researchers can use that tool to efficiently build lexicons for other mental health conditions. Meanwhile, Low says, the suicide risk lexicon is already being used to explore how text data from a variety of sources, from social media to electronic health records, might help researchers and clinicians better estimate risk.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。