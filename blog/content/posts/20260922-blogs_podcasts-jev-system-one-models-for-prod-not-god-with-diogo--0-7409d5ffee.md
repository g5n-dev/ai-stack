---
title: "Jev: System One models for Prod, not God — with Diogo Almeida, CEO, TypeSafe AI"
date: 2026-09-22T08:08:40+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:a971dbeed39b2e6466a2d29af84e14d7e717c91e0251900f0e0433806951457c"
source_payload_sha256: "sha256:8b895f61a3b26a06889dc663ffe1347447b0b6fa74b414f60f207cf8dc215060"
observation_id: obs_7409d5ffee8a2c05841b75acaa01a2e075c8dbdd449825ea2807d39484e82956
event_id: evt_36ea4d30af6974fba80be680c102a43af5d85c1d2b3fca8a163e5fb80e01f8ea
revision_id: rev_58476c981276a3d52130f91e28157cfe4706d6021723b67b5a8175b746df5d57
source_published_at: 2026-09-21T22:13:49Z
first_seen_at: 2026-09-22T00:19:49Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: true
source_truncation_reason: "crawler_feed_content_limit"
source_support: 1.0
source_title_chars_original: 79
interpretation_sha256: "sha256:66274da6d54f322ac0768209f21453caa12bf0edc4027e2a7f34c3cee9d56fc6"
description: "这是一段访谈，探讨 Jev 的设计思路、RLCD（基于校准决策的强化学习）训练方法以及如何让模型在软件系统中实现可靠的概率预测。"
external_url: https://www.latent.space/p/jev
parent_observation_id: null
last_seen_at: 2026-09-22T00:06:49.096466Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://www.latent.space/p/jev](https://www.latent.space/p/jev)
- **发布域名**: www.latent.space

## 要点解读

### 这是什么
这是一段访谈，探讨 Jev 的设计思路、RLCD（基于校准决策的强化学习）训练方法以及如何让模型在软件系统中实现可靠的概率预测。  

### 用在哪里
适用于需要在产品代码里嵌入 AI 的开发者、关注模型校准与可靠性的研究人员，以及想了解 RLCD 与传统 RLHF、RLVR 区别的人群。  

### 可以推断的
推测：RLCD 通过优化校准的概率而非人工偏好或可验证输出，可能降低模型在高频率调用时产生幻觉或过度自信的概率。  
推测：Jev 旨在让 AI 像正则表达式一样无声嵌入，降低在既有软件中集成智能功能的门槛。

## 来源摘要/节选

> Tickets for AIE NYC now open, and apply for the invite-only AIE CODE. Join us!
>
> We have an unusual relationship with today’s guest: for years since coauthoring the InstructGPT paper, Diogo Almeida had been saying that API-available frontier models have been going down the wrong path, everything from the alignment to refusals to reliability perspectives, that we have dropped every mode other than autoregressive chat-tuned LLMs because of the overwhelming success of ChatGPT.
>
> In a launch video now viewed ~40M times (by comparison, GPT4o was 22M, Fable 5 was 15M, Navier Stokes was 74M, and 6 Astra was 137M), Diogo introduced Jev and it immediately took over the AI timeline — we’ll skip full Jev explainers because your favorite AI influencer/educator has probably already done one. We also collected:
>
> the official patterns and cookbooks you should see first, from Allie
>
> Jev usecases
>
> speed based - games and computer use
>
> the voice + computer use example we discuss at 1h34 mins
>
> voice + browser control
>
> The must not miss Doom demo
>
> Driving cars in games
>
> Excalidraw
>
> virtual try-ons
>
> “Smart Games”/smart NPCs
>
> guided responses in text messages
>
> Jev for coding agents has an official guide
>
> jev for linting
>
> compacting tool calls
>
> reasonable pushback from Theo - Diogo has published a note on the Tyranny of the KV Cache that you should read as a followup after the pod for Jev + coding agents, because of his belief that Cache Rules Everything
>
> Programming Languages built atop Jev (Diogo’s fave)
>
> Jev for analytics replay and user journey review
>
> “dark data”
>
> entity resolution
>
> natural language search
>
> “smart software”
>
> a core goal of Jev is to “disappear into the background” - eg as unremarkable as regex
>
> Jev as a judge
>
> Jev memes
>
> Jev vs LLM capabiltiies
>
> blending transformers and classifiers
>
> about the confidence api
>
> Jev vs GLiNER (note difference/pushback, agreed, agreed, agreed)
>
> Jev on trolley problem
>
> Jev Bush
>
> Instead we’ll focus on what we can uniquely offer — a broader philosophical and mission-based understanding of how and why Jev was created, and what you should expect next in terms of future models from TypeSafe (ReasoningJev?) and what usecases and ideas you should work on vs the 55th low effort clone of Jev’s API or doing a generic JevBench benchmark - something Diogo has rejected publicly.
>
> Why RLCD: Three kinds of RLHF, and why they are ALL the wrong north star
>
> Diogo knows a good deal about RLHF, given that he was on the team that pioneered post-training at OpenAI — and traces the three branches to Christiano et al 2017 (the robot backflip demo), Stiennon et al 2020 (learning to summarize) and his baby, Ouyang et al 2022 (InstructGPT). From there on, every innovation from Function Calling to Structured Outputs to Reasoning felt like a hack on top of the string based, sequence to sequence prediction paradigm. As he mentions on the pod, from 2023-2024 he struggled unsuccessfully, due to both personal and organization underestimation, to train a model that accurately addressed what he saw as the core problem with making LLMs the heart of software: reliability.
>
> Jev’s core innovation is "Reinforcement Learning for Calibrated Decisions”, a novel, unpublished technique that optimizes for “answers with epistemically honest probabilities on System One tasks” rather than human rated feedback (RLHF) — which causes hallucinations, sycophancy, and permanent reliance on humans — or programmatically verifiable outputs with rubrics (RLVR) — which solves Navier Stokes but exacerbates jagged intelligence and doesn’t integrate well with other software.
>
> We’ve talked about the calibration problem before on the pod, but probably the single best place to understand why RLCD became necessary is Diogo’s AIE talk, which discusses why a generation of training helpful AI assistants for humans has impaired them for training models for composable, programmable AI for automation.
>
> At the end he also teases his contrarian opinion on scaling laws - which teases how to build a modern neolab without the billions of dollars the major labs have…
>
> The Bitterest Lesson: Tasks and Data beats Compute
>
> We spend a good amount of time discussing Diogo’s essay on the Bitterest Lesson:
>
> His point is that “You get what you optimize for and the bitterest lesson in ML is that the most important part of it isn’t ML at all.” - and picking the right north star, eg upvoting for user preference vs being integrated into tool calls - makes everything else fall in line.
>
> We’re excited to catch up with a freshly dyed Diogo to discuss:
>
> Why AI can solve extraordinarily hard problems but still fail to automate basic work
>
> What System One Models are and why Jev is built for software rather than chat
>
> RLHF, mode collapse, calibration, and the hidden costs of optimizing for human preferences
>
> Why refusals become a problem when AI is buried inside software dependencies
>
> Why TypeSafe rejects public benchmarks and optimizes for intelligence per dollar
>
> The “bitterest lesson”: why the right task and the right data can matter more than compute
>
> Why TypeSafe thinks of itself as a data lab rather than a model lab
>
> RLCD vs. RLHF and RLVR as fundamentally different North Stars for AI
>
> Why reliability and robustness matter more than simple determinism
>
> Jev’s programming primitives and how intelligence maps into software control flow
>
> Why developers should decompose AI workflows into small, measurable decisions
>
> How structured state replaces giant prompts and system messages
>
> Why Diogo thinks AI should eventually disappear into the background of software
>
> The “inverse SaaS-pocalypse” and how AI could supercharge existing software
>
> System One vs. System Two intelligence and the limits of reasoning models
>
> Dark data, computer use, real-time intelligence, and Jev’s biggest early use cases
>
> Why Jev could reshape coding agents built around a single-model architecture
>
> Why Diogo says he wouldn’t pre-train with $1 billion
>
> The OpenAI journey that led to TypeSafe and why he thinks many neo-labs are approaching AI incorrectly
>
> Coding agents beyond the KV cache, shared state, sub-agents, and the multi-agent future
>
> Diogo Almeida
>
> LinkedIn: https://www.linkedin.com/in/diogomda
>
> X: https://x.com/CompleteSkeptic
>
> TypeSafe AI: https://typesafe.ai/
>
> Timestamps
>
> 00:00:00 Jev Launch Week and the AI Economic Revolution
>
> 00:02:50 What Is Jev? System One Models and Programmable AI
>
> 00:05:54 RLHF, Mode Collapse, Calibration, and Yann LeCun
>
> 00:10:29 Programmatic AI, Refusals, and Safety Alignment
>
> 00:17:21 Why TypeSafe Rejects Public Benchmarks
>
> 00:20:43 The Bitterest Lesson: Data, Compute, and the Right Task
>
> 00:24:59 RLCD vs. RLHF and RLVR
>
> 00:28:42 Why Powerful AI Still Hasn’t Automated the Economy
>
> 00:39:55 Reliability, Robustness, and Determinism
>
> 00:48:11 Model Versioning, LTS, Speed, and Intelligence per Dollar
>
> 00:54:04 Inside Jev’s API and Programming Primitives
>
> 00:58:28 How to Build with Jev: Structure, Decomposition, and Small Decisions
>
> 01:18:28 The Inverse SaaS-pocalypse and AI Disappearing into Software
>
> 01:33:21 Computer Use, Dark Data, and Jev’s Biggest Use Cases
>
> 01:38:48 How Jev Could Reshape Coding Agents
>
> 01:41:00 AI Safety, Frontier Pacing, and the Limits of RLVR
>
> 01:48:03 Why Diogo Wouldn’t Pre-Train with $1 Billion
>
> 01:55:19 The OpenAI Story Behind TypeSafe
>
> 02:01:41 Why Diogo Thinks Most Neo-Labs Are Getting AI Wrong
>
> 02:08:00 Coding Agents Beyond the KV Cache and the Multi-Agent Future
>
> Transcript
>
> Introduction: Jev Launch Week and Developer Momentum
>
> Swyx [00:00:00]: Okay, we’re in the studio. A special occasion because this week, Diogo, my good buddy, launched Jev, and it’s been taking over the complete timeline. How do you feel? What’s it like to be you right now?
>
> Diogo Almeida [00:00:16]: Emotionally?
>
> Swyx [00:00:17]: Yeah.
>
> Diogo Almeida [00:00:17]: Never been worse. Like, I’m a ragged corpse of a person right now because there’s so much going on, and I’m like a technical CEO, so I have, like, a lot of fires to fight.
>
> Swyx [00:00:29]: Yeah.
>
> Diogo Almeida [00:00:29]: But mentally, I feel—I say this all the time, and I’ve been saying this kind of for years in my over-under events. Like, I feel like the entire AI field is like one of those, like, carnival house of mirrors, and everyone is just insane and saying the weirdest stuff that doesn’t make sense. And it feels like for just this week, like, I’m on a better in sync with reality and like, oh, people see it now. AI can be so much more than what was once thought.
>
> Diogo Almeida [00:01:06]: And like, yes, we are going to make. Like, an AI-based economic revolution is back on the table, and this is fucking awesome.
>
> Diogo Almeida [00:01:17]: I’m so jazzed the developers get it. It’s, it’s, Yeah, and I want to show my eternal gratitude to the developers and
>
> Swyx [00:01:25]: Yeah.
>
> Diogo Almeida [00:01:26]: I’m so jazzed about the community and everything. It’s so great.
>
> Swyx [00:01:28]: Yeah, you were saying yesterday that you decided to prioritize the town hall and not a bunch of, like, VIP, investor-type people because you wanted to make sure that they are the people that you get your most, attention, right? The engineers, the developers.
>
> Diogo Almeida [00:01:43]: Yeah, it felt a little like, oh man, I’m talking to, like, really important people right now.
>
> Swyx [00:01:47]: Yeah.
>
> Diogo Almeida [00:01:47]: I probably shouldn’t reveal who.
>
> Swyx [00:01:48]: Yeah.
>
> Diogo Almeida [00:01:48]: But it feels a little bit dirty for me to, I’m, like, perhaps overly genuine in things. Like, it feels, like, dirty if, like, in my gigantic calendar event of people to talk to, the community isn’t one of those.
>
> Swyx [00:02:04]: Yeah.
>
> Diogo Almeida [00:02:04]: And actually, in my ideal world, it would be, like, community all the time. I was thinking, “Should I host a town hall while walking to your studio?” And I’m like, “No, that’s too crazy.”
>
> Swyx [00:02:12]: Sure. Yeah. Well, you guys have been hosting town halls on Discord. Discord is now 100,000 people. Your Twitter’s
>
> Diogo Almeida [00:02:19]: I don’t follow these stats.
>
> Swyx [00:02:20]: Yeah.
>
> Diogo Almeida [00:02:20]: So holy shit.
>
> Swyx [00:02:21]: Your Twitter’s blown up. It was, it was really funny ‘cause, like, at AIE, you were like, “Yeah, follow me please,” and then you didn’t, like, provide even your handle.
>
> Diogo Almeida [00:02:29]: I’m a noob. I’m a noob.
>
> Swyx [00:02:29]: You’re such a noob.
>
> Diogo Almeida [00:02:30]: I’m a noob.
>
> Swyx [00:02:31]: But no, but that, like, that’s, like, positive aura that, like
>
> Diogo Almeida [00:02:33]: Cool
>
> Swyx [00:02:33]: You don’t know how to promote yourself.
>
> Diogo Almeida [00:02:35]: Yeah. Someone, like, called me out when I posted, like, “Holy shit, we’re all three twending-- trending topics.” And then they’re like, “That’s a personal feed.”
>
> Swyx [00:02:42]: That’s a personal, yeah.
>
> Diogo Almeida [00:02:43]: And I’m like, “Oh, no.”
>
> Swyx [00:02:44]: Of course, of course it’ll trend to you.
>
> Diogo Almeida [00:02:45]: Cringe. Yeah.
>
> Swyx [00:02:45]: Yes, ‘cause it’s what you clicked on.
>
> Diogo Almeida [00:02:47]: Yeah.
>
> Swyx [00:02:47]: So okay. Let’s, Yeah, so congrats on everything.
>
> What Is Jev? System 1 Models and Intelligence per Dollar
>
> Diogo Almeida [00:02:50]: Thank you.
>
> Swyx [00:02:50]: We’ll talk about more, details as you have them. But let’s, for people who are, like, living under a rock or just want, like, the definitive thing, what is Jev?
>
> Diogo Almeida [00:03:02]: Whew. Let me think about. That’s a hard one.
>
> Swyx [00:03:07]: Okay. And I’m happy to, like, re-ask if you wanna kind of
>
> Diogo Almeida [00:03:09]: No. I’m happy to
>
> Swyx [00:03:10]: Okay
>
> Diogo Almeida [00:03:10]: I’m happy to, like, just jam on it.
>
> Swyx [00:03:12]: Yeah.
>
> Diogo Almeida [00:03:13]: I will say, like, the first thing that I’m relieved about with this question is now I don’t have to answer that question to my parents anymore ‘cause ChatGPT can just explain it.
>
> Swyx [00:03:20]: Nice.
>
> Diogo Almeida [00:03:21]: So the way I see it is we new-- need a new class of models. We’re not attached to naming that class of models. Our-- the most accurate name we’ve come up with is System 1 models.
>
> Swyx [00:03:33]: Yeah.
>
> Diogo Almeida [00:03:33]: There will be reasons, but it’s-- there’s a reason why we don’t call them decision models, because, like, they will be. Like, System 1 is beyond that. That’s all I can say. We didn’t expect this to be our big launch, so we have stuff in the tank.
>
> Swyx [00:03:48]: You should have said low-key research preview.
>
> Diogo Almeida [00:03:52]: It kind of was, right? It kind of was. But we. So there’s a class of models that we describe them as, like, machine-native, System 1, large programmable. I think these are-- is the class of models where the goal is for code to be the consumer. So as opposed to, lar-- pre-trained large language models, which are meant for, like, autocomplete of the internet, or RLHF models, like chatbot instruction-following models, which are meant to, like, reply to text, or RLVR. It’s in a weird gray area with RLHF. Like, these are meant to have things that directly are consumed by code, hence the name type safe. So the thing we really want is to have, like, AI, like, be as powerful as possible, and we think the way to do that is to integrate it with software. And we are designing everything, beyond just the outside, the deep internals of the model to be optimized for software. So number one, Jev is our first large programmable model, or a System 1 model, whatever you want to call it. Jev is meant to be optimized for intelligence per dollar, hence the name Jev.
>
> Swyx [00:05:03]: Jevons Paradox.
>
> Diogo Almeida [00:05:03]: Jevons Paradox, yeah. And it’s optimized for intelligence per dollar. I love this debate with people about what is the most important between reliability, cost, calibration, and speed. And Jev is meant to be. Jev will be the name of models that will be on the frontier of intelligence per dollar. There’s other ways to optimize it, like, ML, or at least if you’re good at ML, it’s all about trade-offs. And we are just going all out on that.
>
> Calibration, Mode Collapse, and the Limits of RLHF
>
> Swyx [00:05:31]: Yeah. And to me, like, calibration is one of the new things that people weren’t talking about as much. We’ve done an episode In the past, with Clementine Foreia of Hugging Face, where they were like, “Yeah, actually, y- they’re just.” Or, and this is your whole argument about RLHF, is they’re more collapsing towards what you want to hear the most
>
> Diogo Almeida [00:05:50]: Ooh
>
> Swyx [00:05:50]: Or what is most likely, instead of, like, their own internal confidence about a thing.
>
> Diogo Almeida [00:05:54]: Can I soapbox on that for a second?
>
> Swyx [00:05:56]: Go ahead. Yeah.
>
> Diogo Almeida [00:05:57]: Cool. Like, I’ve been heard that your audience is the most technical, so I actually want to get into that.
>
> Swyx [00:06:02]: Yeah.
>
> Diogo Almeida [00:06:03]: And if- I went through extreme precision to make sure everything in our launch video is accurate and real. Apparently, that’s very unusual. One of the things that no one paid attention to was the downsides of RLHF, in particular mode dropping.
>
> Swyx [00:06:17]: Mode dropping or mode collapse?
>
> Diogo Almeida [00:06:19]: It’s the same thing.
>
> Swyx [00:06:19]: Is that what you call it?
>
> Diogo Almeida [00:06:20]: It’s the same thing.
>
> Swyx [00:06:20]: All right.
>
> Diogo Almeida [00:06:21]: And I wanna have a blog on this eventually, but I, like, want to tell as many people this as possible ‘cause I think it’s a very interesting thing. So the spicy take, I believe in Yann LeCun a lot. I think Yann LeCun’s takes are actually among the closest to
>
> Swyx [00:06:36]: What about this?
>
> Diogo Almeida [00:06:37]: Well, should I address this now or should I wait and go into mode collapse?
>
> Swyx [00:06:40]: No, later. Go mode, go mode collapse. I don’t know.
>
> Diogo Almeida [00:06:42]: So I actually think that among takes, Yann LeCun’s is among the most accurate. But he has this very famous/infamous slide about,
>
> Swyx [00:06:52]: The cake?
>
> Diogo Almeida [00:06:53]: LLMs are doomed.
>
> Swyx [00:06:54]: Okay.
>
> Diogo Almeida [00:06:54]: Like that one where he, like, has, like, a pie chart with, like, a tiny par-- tiny little thing- and says that as you increase sequence length, the probability of it making an error goes in. Yes, this one. This one. I love this one, because it’s one of these things that seems mathematically obvious, but is obviously wrong, right? Like, it’s mathematically obvious, but it doesn’t empirically hold. And this is my favorite thing to teach people about, like, where you
>
> Swyx [00:07:21]: What’s the disconnect, right?
>
> Diogo Almeida [00:07:22]: Exactly. And may I or you want to tell me?
>
> Swyx [00:07:27]: About mode collapse?
>
> Diogo Almeida [00:07:28]: Oh, no. Oh, so mode clop-- collapse is related to this.
>
> Swyx [00:07:31]: Yeah.
>
> Diogo Almeida [00:07:31]: The disconnect happens because if you are in a mode covering or a calibrated distribution, you are, like, not. You are not overly punished about having outliers. You’d expect, like, something. Some amount of the time you’d be out of distribution, some amount of time you’d be in distribution. That’s what happens when you cover the distribution. This was like models before GANs. They made blurry images, right?
>
> Diogo Almeida [00:07:54]: Instead, GANs mode drop. They, like, drop the minority classes and just do the really common ones. And this is why this effect doesn’t happen, right? Like, instead of be-- in order to generate really long strings, without making errors, they need to, like, be extremely conservative because it’s e- really easy to see when an error happens. It’s very hard to see when, like, a subtle thing that looks correct happens. And that calibration is, like, total poison into, like, the probability distributions of strings.
>
> Swyx [00:08:22]: Yeah.
>
> Diogo Almeida [00:08:23]: And it’s, it’s a nuanced take and like, I think that This is why this doesn’t happen, and this is why strings are so bad at, decision-making or, overloading the string models are for decision-making is, like, a bad time.
>
> Yann LeCun, JEPA, Scaling Laws, and Practical Research
>
> Swyx [00:08:38]: And while we’re on the topic of Yann, do you agree that his fix i- with-- which is like a world model, like a JEPA-type, embedding thing is the right solve? So basically, like, the. One of the reasons that it could fail is because you’re trying to reason over token outputs and then, and then just looping back again and going. Keep, continuing going until you reach, like, a end of sentence. Like, is that, And his solve is JEPA, right?
>
> Diogo Almeida [00:09:02]: Yes.
>
> Swyx [00:09:02]: Which is, like, joint ambition,
>
> Diogo Almeida [00:09:04]: Yeah
>
> Swyx [00:09:04]: Joint embedding prediction. So like, is that the solve or, like, do you have a. Do you have a take on that?
>
> Diogo Almeida [00:09:10]: Oh, man. I probably shouldn’t talk too much about the insides of ML, but I will say that my brand, other than unhinged, is practical.
>
> Diogo Almeida [00:09:20]: Like, even my take here is practical. And like, I’m. Am I a scaling law fan? Depends. It dep-- it’s, it’s, it’s, like, it’s. Scaling laws tell you how much better you get at a thing for amount in.
>
> Diogo Almeida [00:09:33]: A scaling law does mean exponentially more resources for normally sublinear gains, which looks to be a bad investment unless those, like, linear gains are, like, really valuable. But it’s all. To me, it’s all about, like, what can we do with what we have to make the biggest possible fucking difference? I can curse.
>
> Swyx [00:09:51]: Yeah.
>
> Diogo Almeida [00:09:51]: Yeah.
>
> Swyx [00:09:52]: Yeah.
>
> Diogo Almeida [00:09:52]: Yeah.
>
> Swyx [00:09:53]: We’re, we’re, we’re approved for adults.
>
> Diogo Almeida [00:09:54]: Hell yeah.
>
> Swyx [00:09:55]: And also we have a scaling law thing if you wanna go into that later.
>
> Diogo Almeida [00:09:58]: Oh, I could if we. See, that part is not super relevant right now.
>
> Swyx [00:10:02]: Yeah.
>
> Diogo Almeida [00:10:03]: I actually. If you wanna go into my bitterest lesson, I think that’s more relevant.
>
> Swyx [00:10:06]: Okay.
>
> Diogo Almeida [00:10:06]: But like, to me, I’m all about, like, pragmatics. And I think that the JEPA stuff is really cool early research. I really love awesome research. Is it practical yet?
>
> Diogo Almeida [00:10:21]: Probably shouldn’t say. But like, there’s just a lot of.
>
> Diogo Almeida [00:10:29]: I just think there’s just, like, so many diamonds in the rough let all over the research world right now that haven’t been polished because people don’t know how to, like, do the right task. And I think that what our launch did, it. Does it kickstart us as a company? Like, yes. Will it be great for us as a company? Yes. I think it’s gonna be, like, even greater for this direction of, like, programmatic AI. There was going to be, like, a gold rush on top of us for. ‘cause, like, software is super fucking charged. But I think there’s gonna be a gold rush parallel to us as well on, like, all the different ways we can expose things to make software more powerful so people can make even cooler stuff. And then we are back to, like, early internet energy?
>
> Swyx [00:11:12]: Yeah.
>
> Diogo Almeida [00:11:12]: And I think that’s why, like, the Twitter is just like, “Jev.”? It’s, it’s like. It is a party
>
> Swyx [00:11:18]: It’s inspiring because it’s, it’s, like, so different than what we’re used to, which is, “I’m sorry you can’t do this, but we do scaling laws and only the big labs can do it,” right?
>
> Diogo Almeida [00:11:28]: That. Actually, if I. I’ll, I’ll make a tangent if that’s okay.
>
> Swyx [00:11:32]: Yeah.
>
> Diogo Almeida [00:11:32]: I think you might enjoy this.
>
> Swyx [00:11:33]: Really? Our five tangents in. It’s good. It’s fun. Yeah.
>
> Diogo Almeida [00:11:35]: Oh, yeah. I get lost at all my tangents.
>
> Swyx [00:11:37]: This is gonna be horrible for the listeners to figure it out, but they’re gonna figure it out. It’s fine.
>
> Safety Alignment, Refusals, and API Philosophy
>
> Diogo Almeida [00:11:40]: Yeah, we can edit it in post.
>
> Swyx [00:11:40]: This is my response. Yeah.
>
> Diogo Almeida [00:11:41]: So popular thing on Discord, that people keep asking me, I haven’t had the time to explain it yet, is why am I opposed to safety alignment and why do we not refuse? I’m not opposed to safety as a principle, but I think that safety alignment is generally misaligned with users. And refusal is just, like, obviously a type error. Like, if you’re a human being and you’re chatting with, like, a bot or whatever, you’re cloud coding, and a refusal happens, like, “I’m sorry, I can’t read DNA.py.” that’s an annoying time. It’s anno- it’s, it’s annoying
>
> Diogo Almeida [00:12:18]: Right? But you can work with it, right? And you’re forced to work with it ‘cause of Stockholm syndrome.
>
> Diogo Almeida [00:12:23]: I have stories about that too. I need another tangent deep in here. But like, if you ever want this in a dependency running in the background, what happens if that refuses? What if someone else is using that dependency? They don’t know what that system is. Like, you want the software to just stochastically break because a user sent, like, a weird message in there?
>
> Diogo Almeida [00:12:42]: Like, that is, like, straight-up insanity. It’s coming from a place of, like, people who do not understand software, do not understand programming, and like, they are obsessed with, like, I believe this, horseless carriage of, like, AI coworker instead of unearthing, like, the full power of AI.
>
> Swyx [00:13:01]: Fair enough.
>
> Diogo Almeida [00:13:01]: Yeah.
>
> Swyx [00:13:01]: You want something that is the core kernel that is usable everywhere.
>
> Diogo Almeida [00:13:05]: Yes. Exactly. Like, the cognitive core, right?
>
> Swyx [00:13:07]: Yeah.
>
> Diogo Almeida [00:13:08]: And you need this thing to be s- like, so general, so optimized for its use cases. You want it to be, like, you want it to work on all the future use cases, all the weird shit that people are doing.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。