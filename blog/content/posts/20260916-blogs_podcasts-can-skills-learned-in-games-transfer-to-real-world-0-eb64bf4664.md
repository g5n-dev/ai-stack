---
title: "Can Skills Learned in Games Transfer to Real-World Work?"
date: 2026-09-16T05:23:12+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:d4417dd9a7b965e4f48f27c8ca7a84877af0442f4f6b66dbc35fe2882cac7661"
source_payload_sha256: "sha256:b46b3ec20ab86458eb65a991263106f79343170a21ee42bc6d46fece82aca819"
observation_id: obs_eb64bf46642bd1686947e043c83b8981b93207aa9ec69f9380d39bc041e88ac0
event_id: evt_b22d3271d24a5784add8c855898f7ad6ca7c92c79a216678cfbaf1f2fd5ab704
revision_id: rev_3a41f1bab27d6386e70faacc59a1f462d47fd125fdbd65094524e7b156e6072a
source_published_at: 2026-09-15T20:11:54Z
first_seen_at: 2026-09-15T21:33:32Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 56
description: "当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。"
external_url: https://www.latent.space/p/good-start-labs
parent_observation_id: null
last_seen_at: 2026-09-16T00:00:00Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://www.latent.space/p/good-start-labs](https://www.latent.space/p/good-start-labs)
- **发布域名**: www.latent.space

## 来源摘要/节选

> “Games have always been these underrated educational tools. They’re super approachable. They’re very human.”
>
> Those are the words of Alex Duffy, co-founder and CEO of Good Start Labs, who spoke to Latent Space about why his company is turning games into training material for AI models. The company was spun out of AI media and tools company Every last October, with $3.6 million in funding from General Catalyst, Inovia, Every, and angel investors.
>
> The idea came from a 2025 Twitch stream of frontier models playing the game Diplomacy, which Duffy said normally takes “days or weeks to play.” This was when he worked at Every as its head of AI training.
>
> 2025 Twitch stream showing a Diplomacy betrayal by OpenAI’s o3 model.
>
> (For more on Diplomacy and LLMs, see our interview last year with Noam Brown, soon after he won the 2025 World Diplomacy Championship!)
>
> Watching the AI agents battle it out in Diplomacy showed Alex Duffy how each frontier model acts differently when faced with gaming scenarios. In particular, he noticed the OpenAI model (o3) winning all the games by planning a future betrayal, whereas the Claude model (Opus 4) refused to lie and thus “got destroyed.”
>
> From this, Duffy concluded that training AI models on games like Diplomacy could teach them skills like strategic thinking. Especially because those kinds of games have outcomes that can be verified. In a later article published on Every, Duffy wrote that “fine-tuning a model on the strategy game Diplomacy improved its performance on customer support and industrial operations benchmarks.”
>
> Grok 4 Fast is the least likely to betray you in Diplomacy, according to these September 2026 rankings by Good Start Labs.
>
> On the other hand, don’t trust Gemini 2.5 Pro in Diplomacy!
>
> Duffy and his co-founder Tyler Marques launched Good Start Labs with the intention of exploring other games that could teach useful skills to AI models.
>
> “It became really clear that reinforcement learning environments were one of the most reliable ways to teach models anything you could verify,” he said.
>
> The bigger idea is that the way a game is presented to an AI can determine which skills it learns, and whether those skills carry into work outside the game. And the best evidence for that so far comes from a nineteenth-century railroad game.
>
> When game training transfers to financial research
>
> Good Start Labs recently trained a 30B model inside the game 1830: The Game of Railroads and Robber Barons, described on Wikipedia as “a strategy game where the only element of luck involved is in determining the initial play order.”
>
> They then tested the same model on financial research tasks. The experiment was designed to test whether habits learned in a game could transfer outside the game.
>
> “That game has a stock market mechanic within it,” Duffy explained. “You’re bidding on stock of these railroad companies to try and create this logistics network. And we’ve set up tasks where models are going through a database to find information about how the game’s been played, putting it into an Excel file, reasoning over it, creating some functions within it, and then calculating its answer in that way. And so it mirrors what you would typically do in a finance workflow, but you’re doing it in this game.”
>
> The published results compare single-turn question answering — where the model is presented with a game state and asked to make the next move — with a “multi-turn terminal agent that uses tools to explore its environment, plan a strategy, and adapt in real time.”
>
> Both training designs improved their respective in-game objectives, but only the terminal-agent design improved performance on the Finance-Agent benchmark.
>
> Designing a learning environment to teach capabilities
>
> The 1830 result showed that the training design is key. But more generally, Duffy said Good Start Labs can also add an expert model that provides denser, stepwise rewards.
>
> The harness also allows an environment to approach the same game in different ways.
>
> “How you design that [the harness] totally changes what the model can learn,” Duffy said. “You can imagine a model that is looking at pictures is going to learn different things than one that’s reading through natural text [or] one that has everything framed as Python.”
>
> Duffy described the overall goal of Good Start Labs as figuring out “how do you design a learning environment to teach specific capabilities?”
>
> That question is explored in COS-PLAY: Co-Evolving LLM Decision and Skill Bank Agents for Long-Horizon Tasks, a paper co-authored by Duffy and Marques with researchers from several universities.
>
> In the paper, the system gives a decision agent access to what the authors call “a learnable skill bank to guide action taking.” A separate skill-bank agent studies the trajectory and makes changes to the skill bank, which is then looped back for the next run.
>
> What about the latest frontier models?
>
> I asked whether Good Start Labs has compared newer models, such as Claude Fable 5.1 and GPT-6 Astra, in the same game environments? And by extension, do increasingly capable base models make the harness and training environment less important?
>
> “We compare every new model,” Duffy replied, adding that the newer, more capable models tend to be better at the games. However, similar to what the original Twitch streams showed with the 2025 models, the new models “diverge on the personality axes: betrayal, collaboration, theory of mind, etc.”
>
> As for harnesses, he said that “a more capable model needs less handholding to finish the same task, certainly.”
>
> But for what Good Start Labs is doing — treating “the environment as curriculum” — the harness “matters more, not less.”
>
> “GPT-6 Astra reports doing less chain-of-thought and jumps to answers,” Duffy said. “If you want a model to work a certain way while solving a problem, the harness is what forces it. Astra can probably do the math in its head, but you’d rather it use code so you can trust the result.”
>
> What is Good Start Labs selling?
>
> In a recent blog post, the company described its work on “improvement loops,” which include training systems, harnesses, and observability. But how does that translate into products that Good Start Labs offers other companies?
>
> “The main thing that we sell in terms of AI improvement is data and learning environments,” Duffy replied. Its main customers are frontier labs — for which they provide reinforcement learning data to help further train their models.
>
> He describes the data part of its offering as one of two things. The first is “trajectories of agents playing games” — what an agent observed, what it decided, which actions it took and what happened afterward.
>
> The second is custom data for specific game publishers, where “agents are live in their games.” The agents can play inside those games, generating interactions that may be useful for training and evaluation. Duffy said any data sold to model developers is anonymized and stripped of personally identifiable information.
>
> The learning environments that Good Start Labs sells are “full games where models can play end to end,” he noted. It isn’t about winning the games, though. It’s more about teaching AI models to solve problems.
>
> “We’ll also make a lot of tasks where the models are using the game engine as the verifiable source of rewards, but are solving problems in a way that you might not expect.”
>
> So can game skills be transferred to real-world work?
>
> Alongside its custom work for clients, Good Start Labs is also training a general model from the expert models it has built for specific games. The idea, said Duffy, is to unify those expert models “into this general game intelligence that could be applicable everywhere.”
>
> But while the 1830 experiment suggests that agentic game training can transfer to a structurally similar financial-research task, it’s unclear if there will be broader real-world transfer. I asked Duffy what the evidence actually states today?
>
> “Today’s evidence supports pretty clearly that goal-directed execution matters, and reasoning transfers,” he replied. He pointed to a recent article by Surge AI showing that office work post-training improved coding, adding that “DeepSeek R1 showed it more broadly.”
>
> “We’ve seen it twice ourselves: the 1830 finance task, and Diplomacy training that produced a better customer support agent. Every environment we’ve built also improves tool use downstream.”
>
> So that makes the answer to our big question a qualified yes: some game skills can transfer to real-world work. But Duffy says how broadly and reliably they transfer remains an open question.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。