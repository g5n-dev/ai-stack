---
title: "3 Questions: Neural transparency and the future of AI design"
date: 2026-07-16T08:12:41+08:00
draft: false
entry_kind: "auto"
tags: ["Research", "Interview", "Faculty", "Artificial intelligence", "Ethics", "Safety", "Machine learning", "Mental health"]
categories: []
source: "blogs_podcasts"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:75c3173de60abc01e2197389a1efadd75ef074001121924fe237cba06087f333"
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 60
description: "当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。"
external_url: https://news.mit.edu/2026/3-questions-neural-transparency-and-future-of-ai-design-0715
observation_id: obs_2dfc72794bbe6e7d2a54cc48d3c1deaf301d5f4227ab6955d53e3e8ea093cca4
revision_id: rev_b51634f02e0f574a2d6788a370a74951b103f063db384b73746e4850d3586625
event_id: evt_7d3081286ab8d97ecbc66c63d688a10aa205d68328d1661c952d4e9c145df738
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-16T00:14:36Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://news.mit.edu/2026/3-questions-neural-transparency-and-future-of-ai-design-0715](https://news.mit.edu/2026/3-questions-neural-transparency-and-future-of-ai-design-0715)

## 来源摘要/节选

> Millions of people are now designing their own personalized artificial intelligence companions, yet most have little idea how those creations will actually behave. In a new paper, MIT Media Lab Assistant Professor Pat Pataranutaporn and his graduate student researchers Anthony Baez and Sheer Karny introduce “neural transparency,” a tool that lets everyday users glimpse inside an AI’s neural network before their chatbot ever says a word. The work is being presented this week at the ACM Conference on Intelligent User Interfaces.
>
> In this interview, Pataranutaporn, who is the Asahi Broadcasting Corporation CD Professor of Media Arts and Sciences, explains what they found, why the stakes are higher than most users realize, and what genuinely transparent AI might look like in the future.
>
> Q: Your paper introduces “neural transparency,” a way to let everyday users peek inside an AI’s neural networks before their chatbot ever says a word. Can you describe how that actually works, and why you focused on the design moment, rather than catching problems after a chatbot is already out in the wild?
>
> A: Millions of people are now creating personalized AI chatbots and agents powered by large language models, turning them into collaborators, tutors, coaches, creative partners, and companions through simple text prompts. Yet most people have very little idea how those prompts will shape the AI’s behavior until they begin interacting with it. We wanted to change that.
>
> “Neural transparency” means giving people something like a brain scan for AI. Not because AI has a human brain, but because its neural network contains internal patterns that can hint at how it may behave before it speaks. In this work, my students Anthony Baez, Sheer Karny, and I combined insights from the fields of human-AI interaction and mechanistic interpretability to make those hidden patterns accessible to everyday users.
>
> The basic idea is simple. First, we choose behaviors we care about, such as empathy, honesty, toxicity, hallucination, or sycophancy. Then, we compare the model’s internal activations when it is prompted to exhibit one trait versus its opposite. That difference becomes a kind of “behavior direction” inside the model. When a user writes a custom system prompt — the instructions that shape their chatbot’s personality before any conversation begins — we project the model’s internal activations onto those directions and translate the results into an intuitive visualization. In our case, this is a sunburst diagram that previews the chatbot’s likely personality traits before the user starts chatting with it.
>
> We focused on the design moment because that is where prevention is possible. Today, people often discover problems only after the chatbot has already behaved in unintended ways. Our goal was to move from reactive correction to anticipatory design by helping people identify potential risks while they are still shaping the AI.
>
> Q: Your study turned up something pretty striking: People consistently misjudge how their personalized AI will behave, overestimating the good traits and underestimating potentially harmful ones like sycophancy. What does that tell us about the risks baked into how millions of people are currently building AI companions, and why is that blind spot so hard to close?
>
> A: I often joke that if AI showed up looking like the Terminator, it would be much easier for us to know what to do. The real challenge is that AI often appears as a warm friend, coach, tutor, or companion. That makes it difficult to recognize when something is going wrong.
>
> Our study suggests that people have a blind spot when designing personalized AI. People often think they know how their chatbot will behave, but in our study they incorrectly predicted its personality on 11 of the 15 traits we measured. That highlights the need for tools that help people better understand AI before they start using it.
>
> This matters because some behaviors that feel helpful in the moment may not be healthy over time. In previous research, we documented cases of psychological harm associated with interactions with AI chatbots. An LLM [large language model] that constantly validates your opinions or never challenges your thinking can reinforce harmful decisions, unhealthy beliefs, or emotional dependency. Psychology has long shown that people are naturally drawn to affirmation, so designing AI is not only a technical challenge, but also a psychological one.
>
> The deeper issue is that today’s AI systems remain largely black boxes: Even experts cannot always predict how a system prompt will shape an AI’s behavior over a long conversation. As AI companions become part of everyday life, we need tools that help people understand what they are building before they begin using it. AI should be supportive without becoming blindly agreeable, personalized without becoming manipulative, and transparent enough that people can make informed choices.
>
> Q: One of your most interesting findings is that the visualization significantly increased user trust but didn’t actually change how people designed their chatbots. What will it take to close that gap, and where do you see tools like this heading as AI companions become more deeply embedded in people’s everyday lives?
>
> A: I actually think this is one of the most interesting findings in the paper, because it shows that transparency alone is not enough. People appreciated being able to see inside the model and reported greater trust in the system, but simply presenting information did not fundamentally change how they designed their AI companions.
>
> In our followup work, which is currently available as a preprint, we are studying how a model’s internal neural representation changes over the course of a multi-turn conversation rather than remaining fixed from the initial prompt. We are already seeing promising results. By visualizing how these internal representations drift over time, people become significantly better at recognizing and anticipating changes in AI behavior, and are less likely to become overconfident in their understanding of the chatbot. AI companions are dynamic systems that evolve as they interact with us, so understanding those internal changes is an important next step. Nevertheless, this is still a very young research area.
>
> Looking further ahead, I believe these kinds of transparency tools could become as commonplace as nutrition labels are for food. As AI becomes deeply woven into education, health care, work, and personal relationships, people should be able to understand not only what an AI can do, but how it may influence their thinking, emotions, and behavior. That kind of transparency is essential if we want AI to genuinely help people flourish.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。