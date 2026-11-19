---
title: "[AINews] Gemini 4 Neon: GDM's Opus/Sol Contender"
date: 2026-11-19T21:02:28+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "ainews: weekday roundups", "博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:2217270e78727c66ade77103502229b6999dd348759db7d33483acb03c7bb3ab"
source_payload_sha256: "sha256:d537f380517318e86c50a85eabd558db684cba1bafc5c40feb733d1535291db2"
observation_id: obs_d095f837dfa59f6ca3be18e7e5a388a05edd149eebee0533bba3df7ab6cc3a81
event_id: evt_747b17aaa33d4426f21f853c732e7f85bb518fe5f58b8aea92faac6286d8fd2e
revision_id: rev_809a5b580ac1a7c9ca29453b9a9d24a91108a3a50c6302a58e83eb4391e11c6c
source_published_at: 2026-11-19T07:07:43Z
first_seen_at: 2026-11-19T13:01:07.596521Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 48
description: "当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。"
external_url: https://latent.space/p/ainews-gemini-4-neon-gdm-s-opus-sol-contender
parent_observation_id: null
last_seen_at: 2026-11-19T13:01:07.596521Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://latent.space/p/ainews-gemini-4-neon-gdm-s-opus-sol-contender](https://latent.space/p/ainews-gemini-4-neon-gdm-s-opus-sol-contender)
- **发布域名**: latent.space

## 来源摘要/节选

> Google DeepMind shipped Gemini 4 Neon, its fourth Gemini 4 model in about seven weeks. If you’re confused about the naming, you’re not alone; the 1.5 month old Argon is now retired, the old Pro and Flash from Gemini 1-3 are dead, and if you’re thinking the names are based on atomic weights, Neon (10), the midtier model is faster/cheaper than Carbon (6). This is a helpful guide to the current leading models and sizes:
>
> Because of how distillation, RL, and benchmarking works, Neon technically outperforms Carbon by some measures despite being a smaller model…
>
> Also today, Anthropic priced its IPO at $83 per share, above its initial range, and Palo Alto Networks agreed to buy Applied Compute in a $4.5B all-stock deal. Anthropic · Palo Alto Networks
>
> AI News for November 17–18, 2026. We checked 12 subreddits and 544 Twitter accounts. Browse past issues.
>
> AI Twitter Recap
>
> Gemini 4 Neon
>
> Launch and availability
>
> Pricing and specs. Neon costs $3 for input, $0.15 for cached input and $15 for output per million tokens. It has a 1M-token context window and four effort levels. Vals reports a maximum output limit of 1M tokens. Google · Vals
>
> Rollout. Neon is coming to the paid Gemini API in AI Studio and Android Studio, Gemini for business, and Antigravity for Pro and Ultra subscribers. In the Gemini app, Pro and Ultra users can select it as “Deeper analysis,” including for Tasks. Google’s rollout · Gemini app
>
> Day-one integrations. Cursor, GitHub Copilot across its app, CLI and VS Code, and LangChain Managed Deep Agents.
>
> Release cadence. Arena counted gaps of 28 days between Argon and Carbon, 15 between Carbon and Hydrogen, and six between Hydrogen and Neon. Arena
>
> Independent results
>
> High versus xhigh. At high effort, Neon matched Carbon’s 60 on the Intelligence Index for $3.74 per task. On GDP.pdf it scored 33.4% at high and 28.0% at xhigh. Artificial Analysis
>
> Agent Arena. Neon debuted second with 1,336 points across about 4,200 sessions. It had a $2.82 median task cost and placed second on steerability. Carbon still leads the separate Text Arena. Agent Arena · Text Arena
>
> Vals. Neon placed second on the Vals Index at 70.9%, about 0.4 points behind Fable 5.2 at less than half the cost per task. On Code Migration it averaged 160 turns, fewer than Carbon’s 234 or Hydrogen’s 574, and scored below both. Vals Index · Code Migration
>
> CursorBench 4.1. Neon scored 63.7% at default effort, up from Hydrogen’s 57.3%. Cursor
>
> Hands-on reports
>
> Steering and capacity. In 13 early Antigravity sessions, Kimmonismus recorded 762 tool calls and a 93% input-cache hit rate. When told to avoid the terminal, Neon ran zero shell commands in those tests. The logs also recorded 57 capacity errors and four stalled runs. Test logs
>
> How teams use it. Theo says he’s now using Neon for copy, Fable to implement changes, and Astra to playtest. Jeremy Howard praised Neon while saying he was reverting Solveit’s Astra and Sol options to their pre-6.2 versions. Theo · Jeremy Howard
>
> New results for GPT-6.2
>
> Math and formal proof. Astra and Sol took the top two spots on MathArena. Astra solved 42 of 53 ArXivLean problems. Vals separately reports what it believes is the first formalization in Lean of Smoktunowicz’s Gap Theorem, with the proof checked by an independent kernel replay. Tim Gehr · Vals
>
> Agent Arena. Astra debuted sixth. Sol placed eleventh at a $0.90 median task cost. On the separate Code Arena WebDev board, Astra placed third at a 42% lower median cost than its predecessor. Agent Arena · WebDev
>
> Background discounts. OpenAI opened a public beta for GPT-6.2 Responses API jobs that can wait. Two-hour and eight-hour targets for the first response come with 30% and 40% discounts per token, respectively. OpenAI Developers
>
> What changed after launch. OpenAI’s Tibo Sottiaux says early reviewers used builds from before the final few days of changes. Artificial Analysis found Astra’s responses got shorter and it was less likely to admit uncertainty in its behavioral evaluation. Sottiaux · Artificial Analysis
>
> Open weights and inference
>
> Correction to yesterday’s Pi adapter numbers. Yesterday’s issue cited 15 to 32 solves on the 51 hardest SWE-bench Pro tasks. Hugging Face reran affected tasks after finding a tunnel outage that hit nine base-model runs. The corrected result is 20 to 33 solves, or 39.2% to 64.7%. It also released an OpenCode adapter that moved Qwen3.8-27B from 35.3% to 51.0% on the same subset with thinking off. Corrected model card · OpenCode release
>
> Tencent releases Hy4 Flash weights. The 224B-parameter multimodal MoE activates 12B parameters per token, supports 1M context and includes a roughly 64B n-gram embedding table. Tencent released instruct, FP8 and base checkpoints. Tencent repository · vLLM
>
> vLLM 0.34.0. The extensible KV cache is on by default and Model Runner V2 is the sole GPU runner. The team reports up to 1.95× faster NVFP4 decoding on GB200. vLLM
>
> Inference capacity grew faster than peak compute. Epoch estimates that the capacity of chips sold for a fixed basket of agent workloads grew 4.6× from Q2 2025 to Q2 2026, while peak 8-bit compute grew 2.6×. Epoch AI
>
> Runway cuts serving hardware in half. It reports serving a 57B video model at 24 fps on four GPUs, down from eight. Runway
>
> Agent tooling. Prime Intellect launched Model Factory for RL, supervised fine-tuning, serving and evals. Hugging Face released the message dataset from its 1,000-agent PyBot project. Prime Intellect · Hugging Face
>
> Research and chip design
>
> OpenAI models help redesign AMD circuits. OpenAI reports up to 14% improvement against optimized baselines on blocks of AMD’s flagship GPU design. The team used Synopsys tools to check that rewritten circuits preserved behavior and to measure power, performance and area. Some changes made it into a design sent for manufacturing. OpenAI
>
> Measuring research acceleration. OpenAI published an update on internal agent use and research task completion, and proposed regular disclosure of indicators for AI research acceleration. OpenAI
>
> Smaller harness edits can save tokens. In a 40-issue held-out test, a gated approach that edited one module at a time scored 40.0% on SWE-bench Lite at 46.7K tokens per task. A full rewrite scored 42.5% at 451.6K tokens. DAIR research summary
>
> Agent teamwork. MAC Bench finds most gains from eight agents came from exploring in parallel. Opus 5.5 was the sole tested model to show an added gain from coordination. Bespoke Labs
>
> Media and voice
>
> Genie 4 reaches Project Genie. Google’s world model adds native audio and lets users change the world with text mid-session. Access is rolling out to eligible Google AI Ultra subscribers. Google DeepMind
>
> Turn detection and transcription. Inworld released weights for a voice-isolation model and its SAVA turn detector, which it says detects completed turns in a median 71 ms. AssemblyAI split its 3.7 release into models for voice agents, live transcription and recordings. Inworld · AssemblyAI
>
> Kling Image 4.0. It placed seventh in Artificial Analysis’s text-to-image rankings and sixth in editing. Artificial Analysis
>
> Industry
>
> Anthropic prices its IPO at $83. The offering covers 980M shares, about $81.3B at the offer price. About $79.4B of that comes from shares sold by Anthropic before fees. Nasdaq trading under ANT is expected November 19. Anthropic
>
> Palo Alto Networks agrees to buy Applied Compute. The $4.5B all-stock deal gives Palo Alto a platform for post-training and serving open-weight models. The companies expect to close in Palo Alto’s fiscal Q3 2027, subject to regulatory clearance and other conditions. Palo Alto Networks
>
> AI Reddit Recap
>
> Local audio
>
> Blue TTS v3. A developer says their MIT-licensed model generates audio at about 50× real time on CPU. The thread’s headline number is a throughput claim about that setup. Code and demos · Discussion
>
> Inworld voice isolation. The release includes a 64M-parameter model for offline use and a 58M model for real-time use, both at 48 kHz. Weights · Local tests and discussion
>
> AudioGhost. A local interface for Meta’s SAM-Audio lets users describe a sound in text and separate it from the rest of a recording. Project discussion
>
> Local inference and coding
>
> Experts from an SSD. TokenWing’s developer claims it can stream a majority of routed experts from SSD. A user reported 45–50 tok/s on a 120B MoE with 12 GB of VRAM and 32 GB of RAM. LocalLLM thread
>
> One job, two models. A developer paired GPT-6.2 Astra for planning and review with local Qwen3.8-27B for implementation. The reported API bill fell from $7.40 to $1.62 on that run. Workflow and discussion
>
> Neon’s place in the line-up. Readers discussed whether Neon becomes the everyday replacement for Gemini 3.1 Pro, now that Google has separate tiers for fast work and harder projects. Launch discussion · Tier discussion

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。