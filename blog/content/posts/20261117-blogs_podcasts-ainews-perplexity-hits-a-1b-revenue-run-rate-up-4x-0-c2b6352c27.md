---
title: "[AINews] Perplexity hits a $1B revenue run rate, up 4x in 2026"
date: 2026-11-17T21:23:27+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "Prompt 工程", "ainews: weekday roundups", "博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:7620c1506a483d93959c0ef2b8c31c02b72de0709c527e153b63bccc3d45434f"
source_payload_sha256: "sha256:216a04c3939b2aa3af2a1ac0bf488084cc0e1006b0010b299abc59ae583e3ea6"
observation_id: obs_c2b6352c27cb01c4de0b5aa7f96be2b7b1572fff9becd4055f886b8d802f7df1
event_id: evt_4c2e0493d2b998a7879df2151f9ac8f4f44732d32cb8c034aca75c0fc46f1366
revision_id: rev_cf9bb891215a2caec4591ffd16dbeab25f5f44556eb4b06a2a5c28046e3744c9
source_published_at: 2026-11-17T09:24:56Z
first_seen_at: 2026-11-17T13:31:48Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 62
interpretation_sha256: "sha256:093bf9135b0d73c0339967e6305694a00da14d364ef52a170ea6c610cea196a5"
description: "这期 AI 行业简报重点关注 Perplexity 年化收入突破 10 亿美元及估值变化，同时汇总 Qwen4-Max、模型安全评估、智能体基础设施和推理性能等进展。"
external_url: https://latent.space/p/ainews-perplexity-hits-a-1b-revenue-run-rate-up-4x-in-2026
parent_observation_id: null
last_seen_at: 2026-11-17T13:22:13.679637Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://latent.space/p/ainews-perplexity-hits-a-1b-revenue-run-rate-up-4x-in-2026](https://latent.space/p/ainews-perplexity-hits-a-1b-revenue-run-rate-up-4x-in-2026)
- **发布域名**: latent.space

## 要点解读

### 这是什么
这期 AI 行业简报重点关注 Perplexity 年化收入突破 10 亿美元及估值变化，同时汇总 Qwen4-Max、模型安全评估、智能体基础设施和推理性能等进展。

### 用在哪里
适合关注 AI 产品商业化、模型竞争、安全审计与算力优化的从业者，用于快速把握近期值得深挖的产品和技术动态。

### 可以推断的
- 推测：Perplexity 若能维持单位经济性，其融资预期与行业估值讨论可能进一步升温。
- 推测：Computer 承接持续性任务，意味着产品竞争重点可能从单次问答质量转向工作流完成能力与可靠性。

## 来源摘要/节选

> Perplexity crossed a $1B annual revenue run rate today, CEO Aravind Srinivas told Semafor at a live event. The Information reported previously under $250M at the start of the year and over $750M by August, with Computer driving some of the growth. At usual agent lab multiples (eg Cognition also crossed $1B, with Cursor crossing $4.6B), this would roughly mean that Perplexity is now worth $30-50B — if the unit economics hold up. This is a nice bump on the $20B round in September 2025, and qualifies for our “&gt;$10B fundraise” rule for title stories.
>
> Gathering up some recent Perplexity launches for those catching up:
>
> Computer. September’s Automations let it pick up recurring tasks where it left off. November’s Teammates take on ongoing jobs. Computer also runs fully locally on supported Macs.
>
> Monitor API. Watch a topic or page and get a webhook when something relevant changes.
>
> Frontier Research. The new research lab has access to 10,000+ GPUs and plans to publish papers, data, models, and code.
>
> Sponsored by Deepgram
>
> Deepgram is the voice AI infrastructure behind natural conversation—bringing speech-to-text, text-to-speech, voice-focused LLMs, and agents to teams building with voice AI. For any stack and any tools you already love building with, Deepgram slots in as your foundational voice AI technology. So you have control. And we have the context to listen, understand, and speak like a human.
>
> Learn more about the Real-time Context Standard.
>
> AI Twitter Recap
>
> Qwen4-Max in the wild
>
> Friday’s Qwen4-Max preview is now a shipping model. At the highest reasoning setting, Qwen4-Max scored 43 on the Intelligence Index, up from 34. Average cost fell from $10.02 to $3.27 per task. Alibaba cut output pricing from $6 to $4.50 per million tokens, and the model generated about 39% fewer of them. Kimi K3.1 Pro cost $3.68 per index task and scored 67% on Terminal-Bench 4.0 to Qwen’s 48%. Artificial Analysis
>
> Inside the model. Alibaba kept the total parameter count at 2.4T and reduced the number active per token by 25% to 71B. The model takes images and text, with a 1M-token context window. Smaller open-weight Qwen4 models are still to come. Alibaba
>
> Arena and Vals: Arena ranks it #14 overall on Agent Arena, the top Chinese model, with +7.5% net over 14.7k sessions (Arena).
>
> WebDev: It placed #6 in Code Arena WebDev at 1750, +74 over its predecessor (WebDev). It also placed #6 in Image-to-WebDev, just above Claude Opus 5 and GPT-6 Sol (I2WebDev).
>
> Vals Index: It is #11 overall, with large gains in coding and finance (Vals).
>
> Legal-benchmark caveat: On HLAB it gets 95.7% of checklist items right but passes only 21.3% of tasks, and its output tokens rise 3.6x (HLAB).
>
> Vision results (independent): Roboflow calls it underwhelming on its VLM benchmark, with Google, OpenAI and Anthropic now far ahead. At high reasoning effort, however, it is ~4.5x faster and ~68% cheaper per image than Qwen3.8-Max (Roboflow).
>
> Safety, alignment and eval integrity
>
> OpenAI embedded assessments: OpenAI is giving Apollo, METR, Transluce and Goodfire internal access to its models and systems (OpenAI).
>
> Scope by group: Apollo places six evaluators onsite for four months (Rundown). METR reviews OpenAI's largest RL run, with access to transcripts, monitor records and checkpoint snapshots (METR). Transluce runs a six-week audit of post-training alignment evals, with a fuller follow-up in early 2027 (Transluce). Goodfire embeds interpretability researchers to monitor training runs (Goodfire).
>
> Limits: METR says its scope excludes the misalignment incidents OpenAI has disclosed and is narrower than METR proposed (scope).
>
> Criticism of the access terms: Critics say the deals fall short of Sam Altman's promise of "employee-like access."
>
> Reported gaps: Assessors get no Slack access, OpenAI selects which staff they interview, and they cannot access weights or run training-based elicitation (Neel Nanda, Alex Mallen).
>
> Former-employee account: Mikita Balesni says assessors cannot quote employees, even anonymously, and some may be barred from publishing on internal-only models (balesni).
>
> Goodfire acquisition talks: The Information reports OpenAI explored buying the interpretability startup for more than $5B. Goodfire reportedly wanted to stay independent so it could sell to multiple labs (report).
>
> Other integrity signals:
>
> Benchmark contamination: Claude appears to have memorized details of the LinuxArena control eval (Karvonen).
>
> Incident taxonomy: OpenAI published a v0.1 framework for classifying AI control incidents (framework).
>
> Disclosure policy: Anthropic is cutting its coordinated disclosure window from 90 to 30 days for high- and critical-severity vulnerabilities (policy).
>
> Inference systems and agent infrastructure
>
> Together moves on from hand-tuned megakernels. Its first design made it into production for one customer. Agents now search for smaller groups of GPU operations to fuse. Together reports 28% higher throughput on Llama 3.2 1B on B200. Engineering writeup
>
> DeepSeek V4.1 Flash on Vera Rubin: vLLM with Dynamo on SemiAnalysis's AgentX benchmark shows 63.4x per-chip throughput over GB300 NVL72 at 400 tok/s/user, and 93.3x at 600 (vLLM).
>
> Batch-1 latency: SGLang-adjacent work reaches ~2,500 tok/s at batch size 1 on TP4, 1.7x its GB300 result (saltyph). Baseten reports a similar 1.7x over its 4xB300 numbers (Baseten).
>
> Agent-driven optimization: An agent shared Engram tables across HBM via NVLink symmetric memory to recover prefix-cache capacity (Liu). Another team says agents found optimizations that made its B300 step time 10% faster (Halex).
>
> Agentic serving research: MIT's Evolving Infra replaces fixed prefill/decode disaggregation with online adaptation. Against NVIDIA Dynamo on up to 256 GB300s, it reports up to 4.1x lower latency and 14x lower P95 TTFT (Evolving Infra).
>
> Pipeline-parallel prefill: Inferact finds PP2 on MiniMax-M3.1-Flash sustains 23% more requests per GPU than DEP2 at a 2s TTFT target (Inferact).
>
> Prefix-cache pitfalls: Ollama found that a single system-prompt timestamp or a change in reasoning effort can wipe the cache (Ollama).
>
> Sandboxes and training:
>
> External sandboxes: Simon Willison describes running agents on a Mac while executing their code in WebAssembly, QEMU or Apple Container sandboxes. The pattern includes allow-list proxies and credential replacement (post).
>
> MLPerf: In MLPerf Training v6.1, a GB300 NVL72 trained GPT-OSS-20B in 19.7 minutes, 2.86x faster than H100 (Lambda).
>
> One endpoint for open models. Hugging Face Inference Providers now runs on OpenRouter using the same endpoint and token. Hugging Face
>
> Research, benchmarks and evals
>
> PyBot: A swarm of 1,000 DeepSeek-V4.1-Flash agents spent a week writing a rule-based chatbot with no neural network (lewtun).
>
> Scale: The agents exchanged ~175k messages and merged ~8k PRs.
>
> Result: The bot is 630k lines of Python with zero dependencies and is reported on par with SmolLM-360M on everyday questions.
>
> Self-improvement and training:
>
> AutoRL: Agents supervising a live RL run lifted Qwen3 on AIME 2024 from 46.67% to 66.67% (omarsar0).
>
> Benchmark-gaming caveat: A roundup warns that many self-improving agent gains come from learning the benchmark rather than the task (TuringPost).
>
> Weight-space programming: Opus 5.5 hand-wrote transformer weights that solved algorithmic tasks with a median of 166 parameters (dair_ai).
>
> Data curation: DatologyAI published the tech report behind its claimed 6x pretraining compute multiplier (Datology).
>
> Distillation reproduction: A small-scale replication confirms perturbed-input distillation helps when the student trains from scratch, but finds it hurts when distilling into a pretrained student (Maini).
>
> New benchmarks:
>
> GradeBench: The best frontier model agrees with instructors only 57% of the time when grading handwritten physics answers (GradeBench).
>
> Time to First Audio: AA's new TTS latency benchmark finds a median of 376 ms for streaming models versus 2.0 s for non-streaming ones (AA).
>
> SpeedRunBench: Inkling-2-Small cleared SuperTux 1-1 in 1,988 frames, ahead of Opus 5 and GPT-5.6 Sol (SpeedRunBench).
>
> Science models and developer tools
>
> Gemini 4 Carbon: DeepMind says Carbon powered AlphaProof Code agents that verified Signal's cryptographic code. It also spotted wet-lab errors and found 40x more related protein sequences (details).
>
> Science access: Google expanded free Carbon access for 10,000 scientists through Antigravity (program).
>
> Context window: Antigravity doubled the context window for Argon, Carbon and Hydrogen, cutting compaction 3.5x per user turn (Mohan).
>
> User reports (anecdotal): One researcher says Carbon solved a problem that waves of Astra and Fable attempts had not (anecdote).
>
> OpenAI for science and health: OpenAI is opening free frontier access to up to 200,000 scientists, with applications from Nov 23 (program).
>
> Productivity study: OpenAI reports scientists roughly doubled their productivity in a study of 1,800 participants (study).
>
> Physics showcase: Physicist Nathaniel Craig used GPT-6 Astra to develop a candidate lattice definition of the Standard Model (blog).
>
> Healthcare: ChatGPT for Healthcare adds computer-use agents and more than 20 plugins (healthcare).
>
> Claude Code: The desktop app now runs iPhone Duo in the iOS simulator and can fold and unfold the device to test layouts (ClaudeDevs).
>
> Verification: The team published how it uses cheap tests, benchmarks and end-to-end runs to let Claude verify its own work (blog).
>
> Unreleased model (unconfirmed): A "Silicon 2" entry spotted in Devin is suspected to be an Anthropic model (rumor).
>
> Liquid d1.2-ultra: It ranks #1 on AA's Decision Index at $0.042 per M input tokens (AA).
>
> Sage S2.1 Flash: The open-weight science model reports leading MLE-bench Lite and OfficeQA Pro results (Sage).
>
> FLUX-mimic-x: A 7B video-action robotics model ranks #1 on RoboLab among real-time models (mimic).
>
> Unsloth computer use: Local models can now drive desktop apps and game engines through Unsloth (Unsloth).
>
> Industry and policy
>
> Nvidia. The US Commerce and Justice departments issued a joint statement on the Megaspeed investigation. Commerce
>
> Financing and M&amp;A:
>
> Noeri: Yejin Choi and Carlos Guestrin's continual-learning lab raised $110M (Choi).
>
> Corma: The cyber-defense model company raised a $125M Series A at a $1B valuation (Corma).
>
> World Labs: The team is joining AMD (Fei-Fei Li).
>
> Market data: Anthropic's S-1 shows $16.3B revenue in H1 2026 and compute costs falling from 251% to 48% of revenue (The Batch).
>
> Enterprise adoption: Databricks reports open-model token share rose from 7.3% to 30.9% in 3.5 months (summary).
>
> AI Reddit Recap
>
> Local models and hardware
>
> What fits in 16 GB? Unsloth expects a smaller Qwen4-27B to run in 16 GB. Local users want to see the quantization and how much memory is left for the context window. One developer already splits coding jobs between Opus for specs and a local Qwen3.8-27B for implementation. Memory discussion · Local workflows
>
> Hy4 Flash. Tencent’s multimodal model has 224B parameters and activates 12B per token. At $0.070 per million input tokens and $0.281 per million output tokens, it gives developers a cheaper way to try Hy4’s 1M context window. Tencent’s release · Discussion
>
> EUROPA. A reported test run on the JUPITER supercomputer trained a roughly 952B-parameter mixture of experts with 32.8B parameters active per token. The local-model community’s question is why the team chose that scale for its first model. Training run and discussion
>
> Where do two quantizations diverge? inside-llm loads two GGUFs with the same tokenizer and lets you step through their predictions side by side. Watch the first token where they disagree, then compare the probabilities they assigned to the alternatives. Project · Demo and discussion
>
> Basalt’s 770 tokens/sec headline depends on what you generate. The developer reports up to 776 tokens/sec for structured output from Qwen3.8-27B, 262 in chat and 194 for prose. Readers asked for longer quality tests of the 4-bit prefill. Basalt · Benchmark thread
>
> An FPGA running Qwen 27B. Valley Semiconductor reports 7.9 tokens/sec on short prompts and about 5.5 in live chat. Its 50 tokens/sec target at 20 W is a projection for a future chip. Live demo · Hardware discussion
>
> Agents in use
>
> Claude Meetings. A CTO describes inviting Claude into a 30-minute Google Meet. It updated project records in Notion and called the team’s own tools to update bids during the meeting. Field report
>
> A Minecraft test for Hydrogen. A developer asked Gemini 4 Hydrogen to recover missing source and build a datapack for 11 Minecraft versions. The agent reportedly launched two graphical clients to test fixes for dropped items and raycasts. Developer’s account
>
> What teams hire a harness developer to do. One example from the discussion: a coding agent can propose a change, while the harness decides which repository it may write to, which CI test counts as passing and when a person needs to approve the next step. Claude Code discussion
>
> Vision and video
>
> Testing a video model’s physics. After a second MiniMax H3 demo, commenters proposed a harder test: describe the scene, leave the outcome out of the prompt and see whether the model predicts what the objects will do. Demo and discussion

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。