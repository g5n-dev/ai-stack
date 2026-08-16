---
title: "[AINews] SpaceXAI Grok 4.6 and Grok @Bot"
date: 2026-08-13T10:48:37+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "RAG", "AI Agent", "Prompt 工程", "博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:18c28ea4788aac337af75d78fc5f946040f82a34a321baf499fe99d4ee64ebf4"
source_payload_sha256: "sha256:e74cda8df9e47beb89e826f49ad71ed787d26e47631ca1d34bc63c9e2014531c"
observation_id: obs_4f97ae52728d37cafc3f9acdf7c697c5ae4cac02f61d9d68c6881e66b55a0078
event_id: evt_4ee0588116c059f177d66bee98daebedff4b63ccbf40617754266f20c0b38b26
revision_id: rev_ab625c4a02190f63907c43158ba0ac058460b2c43ea94898698cbb52469b4c85
source_published_at: 2026-08-13T01:53:47Z
first_seen_at: 2026-08-13T02:58:38Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 40
interpretation_sha256: "sha256:dc020c537e12009e1fad7ae44b2e72433e9188766a664c4212ae2cf64231bd97"
description: "这是一份AI行业资讯，报道了xAI发布Grok 4.6模型以及近期多个大模型更新动态，重点介绍该模型在编码代理任务上的表现和价格优势。"
external_url: https://www.latent.space/p/ainews-spacexai-grok-46-and-grok
parent_observation_id: null
last_seen_at: 2026-08-16T00:00:00Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://www.latent.space/p/ainews-spacexai-grok-46-and-grok](https://www.latent.space/p/ainews-spacexai-grok-46-and-grok)
- **发布域名**: www.latent.space

## 要点解读

### 这是什么
这是一份AI行业资讯，报道了xAI发布Grok 4.6模型以及近期多个大模型更新动态，重点介绍该模型在编码代理任务上的表现和价格优势。

### 用在哪里
适合关注AI编码工具和大模型发展的技术人员阅读，特别是需要评估新一代AI模型性能与成本比的开发者或产品决策者。

### 可以推断的
推测：Grok 4.6以较低价格提供接近头部模型的编码能力，可能使其成为中小团队或个人开发者的优先选择。  
推测：多模型竞争格局加速，各家在高性价比推理市场持续投入，未来模型选择将更加分散而非集中于单一供应商。

## 来源摘要/节选

> One of our top recurring themes of the year has been coding agents breaking containment into knowledge work, and it’s clear that the AI teammate/multiplayer/multiagent space is the next big AI battleground. With Claude Tag launching to mixed reviews and Block’s Buzz requiring a more technical user, the space was still open for a new category leader, which the now Cursor→SpaceX team has adroitly shipped to very positive reviews:
>
> This is powered by their newest model, Grok 4.6, released today as arguably the second best knowledge work model in the world (as both competitor Cognition and Elon acknowledges)… though it is surely the top by efficiency:
>
> Grok 4.6 is a confirmed 1.5T model that “builds on Grok 4.5 with a particular focus on long-running agents and more ambitious interactive and visual work”. The only training disclosure can be reproduced in full (emphasis ours):
>
> Grok 4.6 underwent a longer supplemental training run than Grok 4.5, with curated model-generated data for reasoning and advanced technical concepts, high-quality engineering data, and an improved optimizer and training recipe. This produced a stronger foundation for the SFT and RL stages that followed.
>
> We then used Grok 4.5 to regenerate the SFT trajectories across reasoning efforts, agent harnesses, and domains such as STEM, software engineering, and knowledge work, and filtered out problematic traces with model-based checks. The resulting SFT checkpoint shows strong performance and improved behavior.
>
> Grok 4.6 is trained on a wide range of agentic RL tasks, including knowledge work, general coding, and domain-specific environments for kernel optimization, web development, computer-aided design, and more.
>
> It is currently unclear if the lack of sandbox escape incidents when it came to training Grok 4.6 is a testament to their infra engineers or an indictment of their researchers.
>
> (that is a joke about current events, don’t get mad)
>
> AI News for 8/11/2026-8/12/2026. We checked 12 subreddits, 544 Twitters and no further Discords. AINews’ website lets you search all past issues. As a reminder, AINews is now a section of Latent Space. You can opt in/out of email frequencies!
>
> AI Twitter Recap
>
> Frontier Model Day: Grok 4.6, Qwen3.8-Max, DeepSeek V4 Pro, and Microsoft’s MAI-Thinking-1
>
> Grok 4.6 reaches the frontier on price/performance: xAI released Grok 4.6, described as a major step up from 4.5 at the same price. Independent evaluations from Artificial Analysis place it at 61 on the Intelligence Index, roughly in line with GPT-5.6 Sol Max, behind Claude Opus/Fable, with strong agentic results including 88.4% on Terminal-Bench v2.1, 1753 GDPval-AA v2 Elo, and competitive AA-Briefcase performance at far lower cost (AA-Briefcase note). Early arena data from Code Arena also slots it near GPT-5.6 Sol and Claude Fable on webdev tasks. Pricing is a central theme: AA highlights $2/$6 per 1M input/output tokens, materially below frontier peers, while practitioners immediately framed it as the new default for coding and bug-finding workloads (Pawel Huryn, Cognition availability in Devin). xAI says the gains came from a longer supplemental training run, regenerated SFT traces, and agentic RL over coding, web, CAD, and kernel optimization; they also report more self-testing behavior during long tasks (@kimmonismus summary). Elon also said Grok 4.7 is already in flight, with initial training complete and supplemental training on SpaceX internal data planned.
>
> Qwen3.8-Max open weights are out: Alibaba’s Qwen3.8-Max dropped as an open-weight 2.4T total / 95B active MoE. Community notes emphasize its scale, day-0 serving, and long-context/agent orientation: Yuchen Jin called it one of the largest open-weight releases to date; vLLM shipped day-0 support plus vendor-specific 4-bit checkpoints for NVIDIA B300 and AMD MI355X; Together AI and Baseten also announced immediate support. One important caveat from users: the released open-weights variant appears to be text-only, with no vision input in the initial drop (skalskip92).
>
> DeepSeek V4 Pro GA undercuts the market: DeepSeek’s V4 Pro GA rollout immediately drew attention less for “best benchmark in every column” than for economics. Multiple observers highlighted pricing around $0.435/M input and $0.87/M output (kimmonismus), with Cline calling it roughly 57× cheaper than Fable 5 while reporting meaningful gains over the preview, including a 15.8% Terminal Bench increase. Reaction was mixed on capability: some early users found it solid but not clearly ahead of Kimi/Flash on all tasks (Yuchen Jin’s roundup, scaling01, teortaxesTex), suggesting DeepSeek’s next gains may depend more on RL environment and agent work than raw scale.
>
> Microsoft enters with its own reasoning model: Mustafa Suleyman announced MAI-Thinking-1, Microsoft’s first reasoning model “built from scratch,” now available in Foundry. The initial ask from the team is notably practical—Finbarr Timbers specifically requested feedback on tool use—which suggests Microsoft is positioning it as an applied reasoning model rather than just a benchmark entrant.
>
> Solar Pro 4 also moved up a tier: Artificial Analysis reported that Upstage’s Solar Pro 4 jumped from 14 to 42 on the Intelligence Index, with especially large gains on agentic and long-context tasks, though still behind the current top frontier and open leaders on both raw score and price.
>
> Open-Weight Multimodal and Edge Models: Video, Vision, Voice, and Local Inference
>
> LTX-2.5 and the open video stack keep improving: @RisingSayak highlighted that Lightricks’ LTX-2.5 landed in Diffusers with several practical features that matter for local workflows: joint video + 48 kHz audio generation, prompt-controlled clip length, a 2-pass quality mode, tile rendering for lower memory usage, and preprocessing that re-compresses input images to better match training. Ostris AI Toolkit added support the same day. More broadly, several accounts framed the week as an unusually strong run for open multimedia releases, including MiniMax H3, LTX-2.5, LFM2.5-VL-3B, and North Micro Vision (victormustar, multimodalart).
>
> Small VLMs and local multimodal are getting serious: Cohere launched North Micro Vision, an Apache-2.0 open-source small VLM aimed at document understanding, with claims of outperforming Gemma 4 E2B and Ministral 3 3B on a broad visual benchmark mix (results thread). Liquid AI’s LFM2.5-VL-3B was also repeatedly cited as a strong compact vision model, and users demonstrated hybrid local/remote agent stacks—for example, Hermes Agent using DeepSeek V4 Flash for planning plus LFM2.5-VL-3B for local vision.
>
> Speech and sign-language releases were unusually substantive: Google DeepMind announced SL2T, a sign-language-to-text system powering ASL input on Android/Pixel 11. The follow-up notes are technically interesting: body pose tracking happens on-device, translation runs server-side, and the system is optimized for real-world constraints like one-handed signing (detail). Separately, Deepgram launched Flux TTS, a low-latency conversational TTS model claiming ~80 ms response time and mid-call adaptation for voice agents.
>
> Inference, Compression, and Systems: vLLM, Quantization, CUDA Scheduling, and Ranking Infra
>
> vLLM added important infra for giant models and long prompts: vLLM now supports Azure Blob paths for both model loading and KV connectors. The Microsoft/NVIDIA recipe matters operationally: faster weight loading via Dynamo ModelExpress (up to 7.3× faster on H100/A100) and blob-backed KV caching via LMCache + NIXL, trading recomputation for fetches on long-prompt workloads (follow-up).
>
> Compression work is extending the useful life of very large models: LLM Compressor v0.13.0 added REAP expert pruning for MoE models—dropping whole experts based on calibration saliency before quantization—as well as arbitrary 3/5/6/7-bit quantization. On the more extreme end, Unsloth claimed to shrink Qwen3.8-2.4T-A95B from 4.9 TB to 397 GB via dynamic 1-bit quantization, making local execution conceivable on 410 GB+ RAM/VRAM systems. They also showed a 2-bit Nemotron 3.5 Lightning setup sustaining long tool-use sessions in 22 GB VRAM.
>
> GPU kernel authoring is getting safer and more declarative: maharshii highlighted CuTeDSL 4.7.0 Task Scheduling kernels, which let developers explicitly declare warp roles, resources, dependencies, and schedules, enabling static checks for deadlocks, races, and barrier initialization before lowering to GPU code. The same author also posted a concise explainer on the prerequisites behind TMA async copy—acquire/release semantics, mbarriers, and CuTe arithmetic tuples—for people trying to reason about modern NVIDIA memory movement primitives (thread).
>
> Classic recommender/ranking stacks are still quietly delivering wins: François Chollet pointed to Expedia’s migration to a modern Keras 3 setup, reporting 30% faster training and 70% lower inference latency for ranking models (tweet). His follow-up stresses a more strategic point: Keras’s backend-agnostic APIs reduce lock-in if teams later need PyTorch or JAX kernels (note).
>
> Agents, Harnesses, and Developer Tooling: Reliability, Memory, Plugins, and Security
>
> The stack above the model is becoming the main product surface: Several tweets converged on the same theme: many practical gains are coming from harness engineering, memory, approvals, evals, and tools more than bespoke model training. Scott Stevenson restated the argument that RAG and harness engineering beat training most of the time because they personalize per customer, avoid privacy risks, improve in real time, and inherit base-model progress (thread, follow-up). Random Walker added a useful product distinction between delegation agents and collaboration agents, with very different optimization targets around verifiability, latency, and human control (tweet).
>
> Tooling releases reflected that shift: GitHub’s @code introduced Agent Plugins 1.0, packaging skills, MCP servers, and AI extensions together, and separately shipped UX improvements like sticky scroll and better session handling (release thread). OpenAI/Codex-side momentum showed up too, including Codex for Linux. LangChain rebuilt LangSmith dashboards for more useful trace analysis and reporting.
>
> Memory and portable agent state are becoming baseline expectations: Hermes Agent got multiple ecosystem updates, from Raspberry Pi deployment to easy profile export/import and new skills like generating reusable APIs from observed web traffic (Teknium). Managed Deep Agents examples from LangChain focused explicitly on durable memory and recurring workflows such as social-media agents (hwchase17).
>
> Security and governance for agents is becoming concrete: W&amp;B showed a side-by-side agent email example where one agent leaked SSN/card info while another blocked prompt injection and redacted secrets before the model saw them (thread start). The Turing Post raised a more architectural issue around delegated identity: if an agent uses your SaaS credentials directly, revocation and auditing become muddy (tweet).
>
> Benchmarks, Research Directions, and AI-for-Science
>
> AI-assisted math and science claims are getting harder to ignore: The most engaged technical tweet was Steven Strogatz sharing a story that a neurosurgery resident reportedly used ChatGPT 5.6 to solve a significant open problem in numerical linear algebra (tweet). Relatedly, multiple accounts noted another EpochAI open problem apparently falling (scaling01).
>
> New benchmarks target less gamed capabilities: Princeton/MIT collaborators released DiG-bench, a text-based benchmark for discovery rather than standard QA or code tasks; tri Dao specifically praised it for having some of ARC’s flavor without confounding vision issues (tweet). Redwood + Anthropic introduced the Conceptual Reasoning Index, targeting AI-risk-relevant argumentation and conceptual reasoning where feedback is sparse and hard to automate. Vals announced SRE-Bench, focused on binary reverse engineering rather than source-level cyber tasks.
>
> Post-training efficiency and long-context research stood out: Lewis Tunstall summarized Direct On-Policy Distillation, where RL is done on a smaller model and the resulting policy shift is transferred to a larger model using a dense implicit reward, roughly halving pipeline cost in the cited setup. Separately, dair.ai’s summary of new OLMo/Llama/Qwen long-context work argues that four architecture choices—normalization, GQA, pretraining context length, and sliding-window attention—can together cost up to 47% of long-context performance, even when short-context validation looks fine.
>
> Clinical and domain-specific RL is maturing: A thread summarizing Google’s ResidencyRL work reports that training Gemini 3.5 Flash over 49,870 simulated telehealth encounters increased diagnostic accuracy under adversarial conditions from 81% to 88% and reduced missed red flags by 31% (kimmonismus). Snowflake also shared a good counterexample to “bigger always wins”: a new 4B SQL autocomplete model beat their previous 30B-A3B MoE, improving user acceptance while cutting median latency 71%.
>
> Top tweets (by engagement)
>
> Grok 4.6 release: @SpaceXAI announced the model; @elonmusk amplified it; Artificial Analysis provided the most useful independent breakdown.
>
> Qwen3.8-Max open weights: @ClementDelangue, @Yuchenj_UW, and @UnslothAI captured the release, deployment, and aggressive quantization angle.
>
> DeepSeek V4 Pro GA: @synthwavedd on rollout; @cline and @kimmonismus on the unusually strong price/performance profile.
>
> AI-for-math headline: @stevenstrogatz shared the numerical linear algebra story involving ChatGPT 5.6.
>
> Accessibility milestone: @GoogleDeepMind announced SL2T for ASL-to-English input on Android.
>
> AI Reddit Recap
>
> /r/LocalLlama + /r/localLLM Recap
>
> 1. Claude Text Watermarking Rollout
>
> Claude now embeds invisible watermarks in all text outputs + signed metadata on files (Activity: 2077): Anthropic says Claude marks some AI-generated/edited content via metadata/provenance signals, not a visible text watermark; the mechanism and persistence depend on file type/workflow and may be lost after editing, export, or platform handling (support article). For plain text, commenters question whether this implies statistical linguistic watermarking versus attached metadata; based on Anthropic’s description, the robust claim is metadata/provenance marking, not an undeletable watermark embedded in arbitrary copied text. Commenters are skeptical of usefulness for text because paraphrasing through another model or local LLM could likely remove detectable signals, and some view any Claude-linkable marking as a privacy/control reason to prefer open-source models.
>
> Anthropic/Claude rollout details: commenters cite the submission statement that Claude models launched on or after August 2, 2026 will embed an imperceptible model-level text watermark intended to survive copy-paste and some editing without changing readability or semantics. Supported file outputs such as .png, .jpg, and .svg will also carry digitally signed C2PA provenance metadata, with third-party detection tooling still forthcoming and older models expected to be updated during a transition period.
>
> A technical concern raised is robustness: for text, users argue the watermark may be removable by paraphrasing through another model, especially a local/open-source one, because rewording can destroy token-level statistical patterns. Another commenter notes this is not unique to Anthropic and points to OpenAI’s provenance/watermarking work: Understanding the source of what we see and hear online.
>
> How would an “invisible watermark” in AI-generated text actually work? (Activity: 878): The thread asks how an invisible text watermark could be embedded in Claude-style LLM output without hidden Unicode; the technical answer is a keyed generation-time scheme that slightly biases token sampling toward pseudo-randomly selected “favored” tokens based on prior context and a secret key, then detects overrepresentation via a statistical score such as a z-score. Commenters note this is robust to copy/paste and minor edits, but degrades under substantial paraphrasing, sentence restructuring, or regeneration by another LLM; Google’s SynthID-Text approach, described in Nature, uses a related tournament-sampling watermarking method. The main skepticism is epistemic: “how would anyone know if it was watermarked?”—i.e., detection depends on access to the secret rule/key or a trusted detector, and robustness claims are limited once the text is heavily rewritten.
>
> A commenter describes LLM text watermarking as a keyed sampling bias: during next-token generation, the model slightly boosts a secret, context-dependent subset of tokens, producing a hidden statistical pattern while preserving fluency. Detection then recomputes the same secret rule over the text and checks whether favored tokens occur above chance, often via a z-score-like statistic; copy/paste and light edits may preserve the signal, while heavy paraphrasing can destroy it.
>
> One linked technical reference is the Nature paper “Scalable watermarking for identifying large language model outputs”, which is relevant to production-grade schemes such as Gemini-style tournament sampling. The discussion also notes that implementations vary by provider, with claims that watermarking can be added at the sampling/model-output layer rather than requiring visible text markers.
>
> A key unresolved technical concern raised is false positives: if detection is purely statistical, naturally written text could coincidentally overuse the “green-list” or favored tokens. This implies practical detectors need calibrated thresholds, long-enough samples, and measured false-positive/false-negative tradeoffs rather than treating watermark detection as a deterministic yes/no signal.
>
> 2. Frontier Model Security and Governance Flashpoints
>
> Read more

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。