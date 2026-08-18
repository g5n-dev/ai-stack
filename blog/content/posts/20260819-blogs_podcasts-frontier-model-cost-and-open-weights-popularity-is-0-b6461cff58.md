---
title: "Frontier Model Cost and Open-Weights Popularity is Driving Demand for Model Routing"
date: 2026-08-19T07:39:20+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:d92f93363de9685dd5e04608a8b4df53afed67e5a7d238342599e08a21e9e89a"
source_payload_sha256: "sha256:c860e628ffc73ad1966f6af211190d0257d78617cfc6e2b2081aff9f48bda6c3"
observation_id: obs_b6461cff58b0d468ae0839c09660bc58c13f01c83a6b6bd8f1064709b5bfb032
event_id: evt_82b8f4997bc88a1abe8df76387313029aaa5f13726ae810e2877d261da076db2
revision_id: rev_e35a359c1366fffbd39aab51defc594e79cb8a5123131511ae91b71c3f25c652
source_published_at: 2026-08-18T21:41:10Z
first_seen_at: 2026-08-18T23:36:08.887178Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 83
interpretation_sha256: "sha256:b9fa540d7571f7af579a6252c5f032db2f40845a9d1d9e70f273822322898857"
description: "这段内容讲述了随着前沿模型费用持续上升以及开放权重模型的崛起，企业在 AI 部署中越来越多采用模型路由技术，以在性能和成本之间取得平衡，并以 Glean 为例展示了实际做法。"
external_url: https://www.latent.space/p/glean-model-routing
parent_observation_id: null
last_seen_at: 2026-08-18T23:36:08.887178Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://www.latent.space/p/glean-model-routing](https://www.latent.space/p/glean-model-routing)
- **发布域名**: www.latent.space

## 要点解读

### 这是什么
这段内容讲述了随着前沿模型费用持续上升以及开放权重模型的崛起，企业在 AI 部署中越来越多采用模型路由技术，以在性能和成本之间取得平衡，并以 Glean 为例展示了实际做法。

### 用在哪里
适用于企业 AI 战略制定者、技术负责人以及 AI 产品经理，帮助他们了解模型路由的商业驱动因素和实现思路，也可供投资者评估 AI 基础设施领域的机会。

### 可以推断的
推测：在成本压力下，企业会倾向于在日常任务中优先使用轻量或开源模型，仅在需要更高质量时才调度前沿模型。  
推测：模型路由技术将成为企业 AI 平台的标准组件，推动对模型选择和调度系统需求的增长。

## 来源摘要/节选

> With the intense competition among frontier model companies, together with ever-increasing power of open-weight models like Kimi K3 and Qwen3.8-Max, model routing has become a key part of AI deployment. We’ve just seen Stripe buy OpenRouter for over $7B, but the trend is equally hot in enterprises.
>
> Glean, co-founded and led by ex-Google Distinguished Engineer Arvind Jain, specializes in bringing AI to large organizations. It was last valued at $7.2B after a $150M Series F fund raise last June. This year, it reached $300 million in annual recurring revenue (ARR) — a three-fold increase over 15 months.
>
> Part of Glean’s mission is to select which model to use for each task — or indeed if an LLM is even required.
>
> “A big goal of Glean is to avoid using LLMs for tasks where we don’t need them,” Jain told Latent Space. “Sometimes you’ll see queries in Glean where people are adding two numbers or multiplying two numbers. They could have used a calculator to do that.”
>
> But what Glean is mostly trying to do is bring what Jain calls “one really powerful personal co-worker” to enterprise employees. And that means being a kind of meta-harness for leading LLMs.
>
> Glean announced its third-generation Glean Assistant last September; these days, agents are a big part of Glean’s system.
>
> “You can think of Glean today as a superset of ChatGPT, Claude, Gemini, Grok,” Jain said. “All these different AI products that we’ve been using day to day, Glean combines the power of all of them into one experience.”
>
> With enterprises, bringing AI technology into an organization is just half the challenge. The other half is bringing organizational knowledge into the AI systems.
>
> “Ultimately our business is to deeply understand your data, knowledge, and information, but also how work happens inside your company,” Jain said.
>
> How model routing is done in Glean
>
> So what does model routing mean in practice? Basically, Glean offers three levels of model selection:
>
> Employees can explicitly choose a model.
>
> Administrators can restrict models or impose usage limits.
>
> Glean’s automatic mode selects a model dynamically for each task.
>
> Configuring models for certain tasks.
>
> It turns out automatic mode is mostly chosen by Glean’s customers for economic reasons.
>
> “Why are people talking about model routing? Why are they excited about it? It’s mostly because of cost,” Jain told us.
>
> Another co-founder of Glean, engineering lead Tony Gentilcore, recently claimed that Glean “is 4x more cost-effective” than Claude Code, “averaging $0.45 per task versus $1.84 for Claude Cowork.” He put that down to Glean’s “harness and routing capabilities.”
>
> Individually, many of us are getting great value out of our $20, $100 or $200 monthly subscription to an LLM provider. But for an enterprise, the per-user costs can easily spiral out of control.
>
> “AI models have been getting expensive,” Jain said. “Like, if you look at Opus or the latest models of GPT, the most advanced models. Not only are they very powerful, they can run much more complex tasks than the previous models. But on a per token basis, they’re more expensive — sometimes double or quadruple the rates of the previous models. And then users actually use them to run much longer tasks. So you’re spending, like, 10 times, 20 times, more, on a per user basis, than what you were doing last year. So the costs have gone up a lot.”
>
> The human feedback loop
>
> Another key factor in Glean’s rise is that it gets to see how ordinary business users are using AI. The product is potentially deployed to every employee as a “coworker,” and it’s also used to build and deploy agents across all departments and functions.
>
> Among its customers, Zillow reports 80% adoption across 7,000 employees, while at Booking.com, “Glean became the first AI platform adopted company-wide.” That kind of penetration gives Glean an enviable view into how AI is being used in enterprises.
>
> “So we are getting to observe what people are actually doing with AI on a very broad basis,” said Jain. “We are getting to see when they’re on different types of tasks with AI, what models do they select first, and when they are not satisfied, when they actually upgrade to some other model [that] actually gives them the right results.”
>
> This human feedback loop, at scale, helps improve the model routing system.
>
> Here’s Waldo, gathering raw materials
>
> Another part of Glean’s architecture is a model called Waldo, which Jain described as sitting on top of the large language models. Waldo was introduced in April as “Glean’s first agentic search model.”
>
> Glean claims that Waldo, its agentic search model, “reduces latency by 50% and tokens by 25%, reserving advanced models for work that needs them.”
>
> In a technical blog post, Waldo was portrayed as a kind of filtering process for user queries: it “decides how to break down the question, which tools to use, what to read next, and when it has enough evidence to hand off to a frontier model for a high-quality answer.”
>
> This means the model routing is happening after Glean has determined what Jain calls the “raw materials” that are needed for the task.
>
> “We’re able to assemble the raw materials needed to do the work without burning LLM tokens,” he added.
>
> A corollary of this is that a cheaper model with better context may outperform a frontier model loaded with irrelevant data.
>
> The rapid rise of open-weight models
>
> Jain confirmed there is now significant interest from enterprises in open-weight models, primarily due to cost concerns. But this has only happened over the past few months.
>
> “Last year, the usage [of open source LLMs] was minuscule and nobody was really seriously considering open source,” he said. Partly that was because of the “stigma” of many of these open source models being developed outside the US.
>
> But suddenly, interest among enterprise customers has risen.
>
> Jain’s tweet on July 27, 2026, in support of open-weight models.
>
> “So in the last three months, because AI got so expensive, businesses have started to find it untenable to maintain these AI investments,” Jain said. “Given that open source is an order of magnitude cheaper to do tasks, it has created a lot of interest. Today, I can say that in most enterprises, they are considering open source models to be a key part of their AI strategy.”
>
> More than that, organizations tend not to rely on just one or two providers anymore — and the rise of open-weight models is driving this trend.
>
> “Nobody is willing anymore to rely on only one model provider, or two, and nobody thinks that they can survive without open source,” Jain said.
>
> Evals
>
> You can’t have a serious conversation about AI in 2026 without discussing evals — assessing the quality of results from LLMs. I asked how Glean goes about doing evals and how that is fed back into the model routing system.
>
> Jain said they have “internal testing systems” where they compare real-world workloads, across different query classes, with alternative options. So they let the model choose a route and in parallel they try to complete the same task with “some other models which are maybe a little bit less expensive and a little bit more expensive.”
>
> How Glean monitors quality.
>
> Glean then uses “AI-based judges” to determine “how spot-on the model router was.”
>
> “So there’s this continuous learning that gets updated with new real-world traffic, where basically what is happening is that you let the model router do the work for the user, but behind the scenes you run the same task,” Jain explained.
>
> He added that this is done for only “a small fraction” of the real-world usage, but at Glean’s scale that’s more than enough to help train and improve the model router.
>
> From enterprise search to end-to-end AI platform
>
> One of the trends we’ll be monitoring going forward on Latent Space is how AI systems are being implemented within enterprises — and how some of these organizations are going full-on AI-native.
>
> Glean is an especially interesting company to monitor for these trends, since it was one of the very first enterprise-facing AI companies. It was founded in early 2019, initially to tackle enterprise search. As Jain put it, Glean was “the first player to work with transformers and language models for businesses.”
>
> Glean’s AI Answers draws “directly from your organization’s documentation.”
>
> In April 2023, swyx interviewed Deedy Das of Glean. Das, who is now a partner at venture firm Menlo Ventures, was a founding engineer at Glean. But even at that point, in 2023 — about four years into Glean — the focus was still mostly on enterprise search.
>
> Now, in 2026, enterprises aren’t just using AI for search. AI is becoming an integral part of every employee’s workflow.
>
> That makes Glean a much ‘sexier’ AI company, as Das himself said on his return to the Latent Space podcast last November. “Broadly, one of the things that I love about Glean is it’s such a boring unsexy company that became sexy later,” he said.
>
> This brings us full circle back to model routing. Arvind Jain ended our discussion by calling Glean an “end-to-end AI platform” that gets “used very heavily” by its enterprise customers. This, he added, allows Glean to “have that data that is required to do effective model routing.”

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。