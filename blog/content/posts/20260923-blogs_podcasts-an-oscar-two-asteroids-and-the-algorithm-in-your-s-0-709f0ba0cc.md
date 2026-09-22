---
title: "🔬 An Oscar, Two Asteroids, and the Algorithm in Your sklearn: John Platt on AI for Science"
date: 2026-09-23T06:10:44+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "机器学习", "博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:e1d1bd74887179482d75e4a5841f35cf08051818c40ec46f2ebe1c1453ae19dd"
source_payload_sha256: "sha256:21f1d665b5bccd88babe60f7c2df1f6bd81f0cfaac1e94409af87a414021816e"
observation_id: obs_709f0ba0cc6c91a33f3c44e186bbe1262e3f8448e34d7d12f6d37902856efe77
event_id: evt_da5a6cf8380e3778026c2f27a7a2c2199bc922cbe651b37ed4b7611ee2c98525
revision_id: rev_797c67076cf671869d13e5151626ab6e8b2902017774c274640ff32403debb96
source_published_at: 2026-09-22T21:07:39Z
first_seen_at: 2026-09-22T22:08:46.321148Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 90
interpretation_sha256: "sha256:49e2d09fb9647d3f11396258543e8dcbb9308e81b7b93577b05bb8a4529b3ff1"
description: "这是一段播客访谈的文字记录，受访者是机器学习领域的知名研究者。内容围绕其团队开发的一套自动化科研辅助系统展开，该系统能够将科学问题转化为可评分任务，并借助大语言模型自动生成和优化实验方案。同时探讨了人工智能在气候变化研究中的实际应用案例。"
external_url: https://www.latent.space/p/john-platt
parent_observation_id: null
last_seen_at: 2026-09-22T22:08:46.321148Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://www.latent.space/p/john-platt](https://www.latent.space/p/john-platt)
- **发布域名**: www.latent.space

## 要点解读

### 这是什么

这是一段播客访谈的文字记录，受访者是机器学习领域的知名研究者。内容围绕其团队开发的一套自动化科研辅助系统展开，该系统能够将科学问题转化为可评分任务，并借助大语言模型自动生成和优化实验方案。同时探讨了人工智能在气候变化研究中的实际应用案例。

### 用在哪里

适合关注人工智能前沿进展、特别是了解语言模型如何辅助科学研究的技术从业者阅读。也可作为了解科研自动化工具发展现状的参考资料。对人工智能在气候建模等实际科学问题中的应用感兴趣的读者也能从中获得启发。

### 可以推断的

推测：自动化科研工具正在从概念走向实用，这类系统若能降低科研门槛，可能加速多个学科的发现速度。

推测：线性模型在入门阶段仍有其价值，研究者在追求复杂方法前，打好基础仍是务实的选择。

## 来源摘要/节选

> How often do you get to talk to a guest who has both an Academy Award and who invented textbook machine learning algorithms? John Platt has an Oscar, two textbook algorithms, two named asteroids, and an Erdos-Bacon number of 6. This was easily the most fun bio of all the guests we’ve read to date. And the result was an epic and fun chat covering Google’s Empirical Research Assistance (ERA), how AI can help battle climate change, and tons of great stories about the co-evolution of science and AI.
>
> John’s colleague Dave Bacon likes to tease John that his career has been defined by being twenty years early to the next big thing. This may be convolutional neural networks (some credit him with coining the term), fusion research, quantum computing. John and Google have been working on solving some of humanity’s hardest problems with AI and computation for well over a decade now. Recently John and his team set their sights on using AI to solve any scientific problem that can be written down as a score.
>
> Google’s Empirical Research Assistance (ERA)
>
> John’s team has taken on many hard scientific problems over the years. In solving these, they noticed a pattern, many scientific problems can be reduced to what John calls a “scoreable task”. Once you have the score function, the goal is to find some code that maximizes the score. The hard part is in formulating the score, but once you have the score finding the maximizer can still be quite a lot of effort.
>
> John’s team set out to automate solutions to this general problem. This came out of the idea of an “auto-Kaggle” AI, which can solve any Kaggle problem you can throw at it. Kaggle is owned by Google, so all the data was ready and easily available to them!
>
> The result is Google’s Empirical Research Assistance or ERA (paper, github, blog).1 ERA is surprisingly simple conceptually. Gemini (or your LLM of choice) keeps a running tree of past experiments (notebooks) and where they’re going. It’s a close cousin of Monte Carlo Tree Search: at each iteration the Upper Confidence Bound rule picks which notebooks are most promising to mutate. This is optimistic, not greedy, so sometimes even the fifth-best notebook gets chosen. Gemini then proposes mutations for each one, about ten at a time. The history of each branch is shared, so different leaves can learn from each other.
>
> “It’s almost like having a hyper-eager grad student who doesn’t sleep.”
>
> Evolutionary algorithms have been around since the 70s, but this works because Gemini actually knows where to look! What’s even more interesting is that there was a step change between Gemini 2.0 and 2.5, and this went from just not working to working great.
>
> ERA is so powerful that John and his team solved many outstanding problems with it, resulting in at least ten papers. Some of these were climate change related, which we talk about in the next section.
>
> So, we had to ask: if you have an optimization god how do you avoid fooling yourself? John’s answer is that ERA provides predictive models. It’s up to the scientist to make sure they’re truly descriptive. Some of this just involves good old-fashioned careful machine learning science. “It’s a power tool. It can slice your fingers off.” This led to some fun discussion about Kaggle competitions, and the fun ways people can overfit to datasets without meaningfully solving the problem you actually care about: Google’s contrail-detection competition was won by entrants who noticed a half-pixel error in the labels (is the origin at the corner of the pixel or the center?) and this turned out to be a part of the winning special sauce. Great for winning $15,000, not so helpful if you actually want to solve contrails.
>
> “People themselves will act like these LLMs and try to reward hack. It goes back to Goodhart’s law: any metric that becomes a target is no longer good as a metric.”
>
> His advice for where to start instead?
>
> “Always just fit linear regression. Just do it. Just do it. Just do it. Or SVM.”
>
> Tackling Climate Change with AI
>
> John and his team have worked extensively to mitigate the effects of climate change. We talked about several of their initiatives.
>
> Perhaps the most interesting result we talked about was reducing the effects of condensation trails (contrails) from airplanes. Those little streaks you see running behind planes somehow account for 1% of all human-induced global warming?!? Some of these trails of ice crystals can hang out for days. These crystals are black in the infrared, acting like a thermal blanket that traps heat day and night.
>
> It’s easy to understand what’s happening here, a region of atmosphere becomes “ice supersaturated”,2 and a tiny bit of exhaust seeds water vapor that instantly crystallizes. The scale here is astounding, with a single gram of exhaust resulting in ten kilograms of ice crystals.
>
> The solution to all of this is quite simple, in principle! We know what parts of the atmosphere are most likely for the trails to form. Just have the planes drop a flight level or two. Problem solved, right? Well, the hard part is accounting for how much warming was prevented. This is a counterfactual problem, parts of which stumped John’s team for over two years. They had a working model for the heat-trapping half, but not for the reflected sunlight. ERA was able to find a simple model with some confounders they hadn’t considered. Cracked it!
>
> Modeling climate generally is a hard problem. Climate is best thought of an attractor of many different possible weather outcomes.3 This makes it much harder to model.
>
> “Weather is where you are on the attractor, and climate is the statistics of the attractor. The problem with climate is that we’re altering it. The attractor itself is changing, it’s moving.”
>
> John and his team have worked on treating both the symptoms and the disease of climate change, with several other works in the area. Another fun example we briefly cover is FireSat, a way of using a constellation of satellites to rapidly identify fires before they grow too big to put out. For anyone living in California, you understand the problem. In dry years a small fire can result in hundreds of thousands of acres. If you could find this fire when it’s the size of a room, it could be put out. By the time it hits an acre we have a much harder problem.
>
> Where is this all going? Looking forward by looking back
>
> By now it should be clear John has an incredible and unique view over the intersection of science, computation, and AI. John talked about a class on physics of computation4 he took with Richard Feynman back in 1982. This was when quantum computing was an ill-defined concept with no theory or experimental backing. John recalls every Tuesday was a guest lecture, and every Thursday was Feynman explaining why the Tuesday guest was wrong. John also recalls doing science back when there was essentially no compute, a million operations per second was cutting edge.
>
> What is John’s recommendation: the most important skill is developing deep domain expertise. There’s no other way to develop taste than to tackle hard problems. One surprising part of this is that John recommends spending time doing things the old fashioned way. Play with tools, and just implement things yourself.
>
> “You could drive up the mountain, or you could hike up the mountain, and maybe it’s okay, even fun, to occasionally hike.”
>
> Summing it up, John’s message to the audience is that there will still be a place for scientists, and that if anything it will just open up more opportunities for “the creative stuff, the rigorous stuff, the philosophy stuff.” But don’t forget to spend time doing the grunt work.
>
> “There just seems to be this strong impetus in the world to optimize and squeeze everything out. But you do lose something when you hyper-optimize. It’s overfit.”
>
> And whatever tools you end up using, John’s advice is the same one Feynman gave him forty years ago: you must not fool yourself, and you are the easiest person to fool.
>
> We had a great time talking with John. We hope you enjoy!
>
> Also in this episode
>
> Fusion is three years away, not thirty, if you ask John. And why the Lawson criterion means every fusion approach has an Achilles heel.
>
> Why superconducting qubits are still finicky.
>
> The asteroid he named after his mom, which turned out to have a moon.
>
> The looming helium shortage nobody talks about.
>
> How NeurIPS started as people crashing a private workshop at Snowbird, and why Hopfield networks are all you need.
>
> Being Carver Mead’s sysadmin on a VAX with an 80 MB disk the size of a dishwasher.
>
> Finding asteroids in 1985 with film, a stereoscope, and a letter to Brian Marsden. The Vera Rubin Observatory found 11,000 in six weeks.
>
> The Feynman effect: total clarity in the room, none once you leave.
>
> Quantum echoes, the NISQ era, and why he thinks quantum is neither thirty years away nor tomorrow.
>
> A startup that wants to inject mercury into a fusion reactor and sell the transmuted gold. “It might not work.”
>
> John’s 20% time rule for his own group: do stuff for learning, and you don’t even have to tell him what.
>
> 1
>
> The ERA GitHub repo features an open source implementation that ran Gemini but can be used with any LLM. ERA is not currently available as a Google product.
>
> 2
>
> “Ice-supersaturated” is about water vapor, not liquid water. Cold air can hold a given amount of vapor, and there are two different limits: the amount in equilibrium with liquid water, and the smaller amount in equilibrium with ice. Below freezing, a pocket of air can sit between those two limits. It has more vapor than ice can tolerate, but not enough to condense into droplets, and ice won’t form directly from vapor without a seed. So the vapor just hangs there, metastable, sometimes for days, until something seeds it.
>
> 3
>
> We recently covered the weather-climate crossover in our episode with Anima Anandkumar, and we plan on covering both weather and climate more in future episodes.
>
> 4
>
> This was really about quantum computing, but in the early days before anyone really knew what this meant and it was just a vague idea Feynman and a few others were kicking around.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。