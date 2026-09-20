---
title: "[AINews] Here are 6 Clones of Jev in 2 days"
date: 2026-09-19T13:56:21+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "生成式 AI", "博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:81826052242e30a7879b21b746e3a73850825fb5031b43dbdef0e577859867cb"
source_payload_sha256: "sha256:4577efbae24b09664cbdea7a3ee7fdb0ca3046c565ed1b0f86c5003146ff2e68"
observation_id: obs_fb0ebe24a1ef57575fb524e4cae242ba1a153a9697764568f11467223329a72f
event_id: evt_22758bf94e55c42e27289d5a3dd148c5991939a2a33a16039aa11f8f97611b2c
revision_id: rev_940d7d017b7c0a91cd917944fd2e754faf68c88204e00249819952fbf5496673
source_published_at: 2026-09-19T05:48:28Z
first_seen_at: 2026-09-19T06:06:33Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 43
interpretation_sha256: "sha256:b9f9d7cfc912b067ec5ababddc43056a54bb350abcf91c7e360ffd453d0a8ccc"
description: "这段内容是AINews对一种非生成式决策模型（Jev）在短短两天内被多个团队快速复现并推出克隆版的综述，概述了各克隆的技术路线和已有的工作流集成案例。"
external_url: https://www.latent.space/p/ainews-here-are-6-clones-of-jev-in
parent_observation_id: null
last_seen_at: 2026-09-20T00:00:00Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://www.latent.space/p/ainews-here-are-6-clones-of-jev-in](https://www.latent.space/p/ainews-here-are-6-clones-of-jev-in)
- **发布域名**: www.latent.space

## 要点解读

### 这是什么
这段内容是AINews对一种非生成式决策模型（Jev）在短短两天内被多个团队快速复现并推出克隆版的综述，概述了各克隆的技术路线和已有的工作流集成案例。

### 用在哪里
适用于关注AI系统中决策、路由与分类层的研发人员与产品经理，也适合对agent工具链、编码 harness 设计以及成本敏感型部署感兴趣的技术人员参考。

### 可以推断的
推测：Jev的结构较为简洁，使得不同团队能够在短时间内完成适配，说明此类轻量判别模型已具备较高的可复制性。  
推测：实际落地时，响应速度和运行成本是关键考量，这促使行业倾向于将快速决策任务从大模型转移至专用判别模型。

## 来源摘要/节选

> We covered Jev’s launch on Wednesday, and they have completely taken over the timeline, with 36M views of their launch video (by comparison, OpenAI’s Navier Stokes result got 74M views, and Anthropic’s Fable 5 got 57M views) in just two days.
>
> It wasn’t open source1, so it invited tons of speculation and great demos and examples and salty schmidhubers and bad takes, which of course only fed the hype.
>
> Here’s a list. The best guesses are ModernBert and Diffusion:
>
> Laya: 421M params, ModernBERT-large encoder with two added transformer layers that score user-supplied options, PPO over sequence embeddings to output turn-by-turn conversion trajectories (probabilities from 0.0 to 1.0).
>
> salty that he did not get recognition; claims RLCD without justification
>
> confidence is entropy-based, not calibrated
>
> DiffusionGemmaJev: tackling this from a Diffusion model basis. Pretty close on benchmarks
>
> Bespoke Nimble: LoRA finetune of Qwen3.5-9B, using contrastive data curation. (close but sllightly lower on benchmarks)
>
> SemIf (fka OpenJev) (HF): 4B and 35B causal Qwen3.5 backbone with a tiny three-class NLI classifier on the last token. comparison vs Laya
>
> Jevlike: 40K byte embedding lightweight option-attention model. Each candidate becomes a query that reads from a shared context representation, then receives a score.
>
> Kev-0.5B: LoRA adapter + a small readout head on top of Qwen2.5-0.5B.
>
> Of course, not enough people are talking about the data side, which is acknowledged to be 100% synthetic.
>
> AI News for 9/17/2026-9/18/2026. We checked 12 subreddits, 544 Twitters and no further Discords. AINews’ website lets you search all past issues. As a reminder, AINews is now a section of Latent Space. You can opt in/out of email frequencies!
>
> AI Twitter Recap
>
> Decision Models, Routing, and the “Jev” Wave
>
> Discriminative models broke out as a new systems primitive: The biggest technical conversation was around Jev, a non-generative decision model being positioned as a fast “System 1” complement to LLMs. @ankrgyl said it is now available as an eval model in Braintrust with ~400x lower scoring cost versus prior setups, while @gabepereyra highlighted calibrated-probability use cases like routing, citation selection, escalation, and legal ops decisions. The more architectural take came from @hxiao, who argued Jev could pull tool calling, routing, and MCP-style decisions back from small generative LMs toward discriminative models; @signulll pushed the same idea further, framing this class as a near-zero-marginal-cost, on-device judgment layer for notifications, UI adaptation, and sensor-driven decisions.
>
> Open reproductions and ecosystem clones appeared immediately: @madiator released Bespoke Nimble, an “open Jev” recipe built from a LoRA fine-tune of Qwen3.5-9B using synthetic contrastive data curation and constrained decoding. On its curated eval, the base Qwen improved from 66% to 90%, versus 93% for Jev, with a reported 100ms on H100 and local usability. At the smaller end, @jaredpalmer released Kev-0.5B, a tiny Jev-like model based on Qwen2.5-0.5B that can run on a MacBook Pro. The reaction split roughly along prior experience: @MParakhin noted post-ChatGPT users treated it like a revelation, while pre-GPT ML people were more puzzled by the hype. The substantive question raised by @abacaj is the right one: a lot of demos emphasized speed more than quality, and there is still no standard benchmark for this category.
>
> The first compelling integrations were in browser/computer-use workflows: @levie demoed Jev classifying Box incident reports into escalation paths; @ndrezn showed browser use with LangChain + Jev and found it strong on tasks like the Wikipedia game and structured “folding laundry” workflows; @cline shipped a plugin giving Jev a browser in Cline. @hwchase17 explicitly called browser use the best Jev application he had seen so far. Net: this looks less like a chatbot story than a workflow control-plane story.
>
> Agent Tooling, Coding Harnesses, and Claude Code Standards
>
> AGENTS.md gained real momentum as a cross-tool convention: The highest-signal product update here was @trq212 announcing that Claude Code v2.1.277 now checks for AGENTS.md when no CLAUDE.md is present, with config-level toggle support. That effectively acknowledges AGENTS.md as an emerging standard rather than a one-tool convention, and @simonw immediately noted the practical payoff: fewer shim files that just point one format to the other.
>
> Harness design is becoming a first-class variable in coding-agent performance and cost: @pidotdev highlighted the Harness Tax analysis showing that a simple tool set—read, write, edit, bash—can reach the Pareto frontier on benchmark performance while reducing unnecessary spending. Relatedly, @_akhaliq pointed to the paper An Empirical Study of Harness Design for Coding Agents, underscoring that benchmark outcomes are increasingly shaped by harness structure, context setup, turn budgets, and tool affordances rather than just the base model. This is consistent with @dexhorthy’s “software factory” argument that teams still need to read the code and deliberately design the human/agent interface.
>
> Model choice in software systems is bifurcating: Several practitioners described a split between “frontier for planning, cheap for execution.” @TheAhmadOsman summarized one stack as GPT 5.6 Sol XHigh for planning, GLM 5.3 Flash for implementation, and DeepSeek V4.1 Flash for other tasks. @kylebrussell reported an internal knowledge-base pipeline moving from Opus → Sonnet → GLM 5.2 → GLM 5.3 Flash, cutting spend by roughly two orders of magnitude since spring. Meanwhile @theo argued that in real-world coding the payoff from stronger models like Fable and Astra is not just code quality, but a subtler productivity gain in execution and iteration.
>
> Benchmarks, Recursive Self-Improvement, and Math Capability
>
> RSI discussion got more precise about what is actually “recursive”: @TheTuringPost offered a useful taxonomy: AI improving code or training methods is not, by itself, fully recursive if the surrounding improvement loop remains fixed. The key threshold is when AI can modify not just model internals, but search strategy, experience generation, research tooling, and the improvement process itself. That framing links well with @HuaxiuYaoML’s RSI-Exam update, where GPT-6-astra remains #1 at 0.5126, with Fable 5.1 entering at #2 with 0.4813, and no model yet reaching the frontier-calibrated reference.
>
> Math benchmarks continued to fall to frontier models, but interpretation remains nuanced: @EpochAIResearch reported that another FrontierMath open problem was solved in an interactive session with GPT-6 Astra. Separately, @SAIRfoundation launched Open Math Model, pitching open models and tools for mathematics shaped by the research community. Against the “verifiability explains math strength” narrative, @steve47285 shared an argument that pretraining data, not merely verifiable reward structure, is the main reason LLMs are so good at math and coding. The meta-point from @sarahcat21 is worth keeping: we need not just better benchmarks, but better benchmark maintenance and audit tooling.
>
> Computer-use benchmarks are still far from saturation: @ValsAI launched CUA-Bench, testing real-time keyboard/mouse use across 6 games (with 3 kept private) as a proxy for difficult human-easy tasks. Follow-up numbers from @ValsAI suggest this remains genuinely hard: all frontier models score below 20%. In parallel, @trycua open-sourced CUA-S1-FORMS, the first in a family of small “System One” computer-use models. The direction is notable: real-time action loops, video-grounded adaptation, and continuous learning, not just text-only planning.
>
> Infra, Training Systems, and Model Architecture
>
> Long-context and large-scale training infrastructure remain active optimization fronts: @Azaliamirh released Turbo-dLLM, an open-source library for training diffusion LLMs at scale, reporting 2.48x speedup at 512K context and 7.59x at 1M context on 8x H100s via Context-Sharded Block Parallelism. That aligns with practitioner attention on million-token regimes: @andrew_n_carr flagged a sharp quality increase in DeepSeek V4.1 Flash after context extension to 1M tokens, arguing that agents are context hungry.
>
> Architecture taxonomy debates are still alive: @ahatamiz1 argued that the field is overusing SSM as a label for any linear model. His proposal is to use linear RNNs as the umbrella term, with SSMs as one sub-family, distinguishing systems like Mamba2 from the GDN family on the basis that GDN behaves more like a gradient step on a local regression loss than a discretized ODE. For engineers tracking sequence-model alternatives to transformers, this is a useful nomenclature cleanup rather than mere pedantry.
>
> Edge/local neural program execution also got a notable update: @yuntiandeng described ProgramAsWeights, where developers specify an AI function in English, compile it once, and then run a small neural program locally on CPU with Wi‑Fi off. The code and models are public. This sits interestingly adjacent to the Jev conversation: both point toward smaller, specialized, locally runnable inference artifacts rather than ever-larger universal chat models.
>
> Robotics, Vision, Audio, and Generative Media
>
> Open robotics data releases were unusually substantive: @adamrasb announced the full ABC release, including code, 400+ hours of sim data on 24 tasks, and 5,850 labeled policy-evaluation episodes. In a more detailed companion post, @redstone_hong described ABC-130K as the largest open teleop dataset to date: 3,500 hours, 130K+ episodes, 195 tasks, collected on an $8K bimanual setup, with open hardware, training code, sim, and eval. The baseline science included sim-to-real correlation r = 0.91 on task progress and studies of offline metrics, scaling laws, and conditioning.
>
> Astra is showing up across evals and products, especially for vision: @skalskip92 reported GPT-6 Astra as the strongest vision model Roboflow has tested across detection, segmentation, box prompting, counting, reasoning, and video. The tradeoff remains material: a “high effort” setting improved detection from 82.1% to 83.6% mAP@50 but roughly doubled per-image cost from $0.050 to $0.101 and latency from 11s to 32s (details). Roboflow also integrated Astra into Auto Annotate.
>
> Speech and lip-sync saw strong benchmarked releases: @ArtificialAnlys reported Grok Voice Transcribe 2.0 reaching 2.7% WER on streaming final transcripts at 0.49s after end-of-speech, improving from 3.9% on its predecessor while keeping pricing at $0.20/hour streaming and $0.10/hour non-streaming. On the video side, @fal launched H3 Max Lip Sync, claiming #1 on both speed and quality in its evals with 11s median generation time, and @isidentical said the model was built by pushing diffusion RL into a verifiable lip-sync task.
>
> AI Safety, Evaluation Governance, and Security
>
> Anthropic’s evaluator-embedding strategy became more concrete—and more controversial: @AnthropicAI announced a partnership with Accenture on independent evaluation of frontier AI, saying the two organizations expect to invest at least $1B over five years to build capacity. This follows broader calls for embedded third-party evaluators with employee-level access. The reaction was mixed to hostile: critics questioned whether a consulting firm is the right vehicle for model red-teaming and safeguard assessment, while @TransluceAI emphasized that the conditions around independence and meaningful oversight are the real issue.
>
> The “rogue agents” / Hugging Face incident continued to drive debate about containment: @polynoamial clarified that his much-mocked thought experiment was about coordination between supposedly isolated agents, not weight exfiltration via thermal sensors, and argued the lesson from the HF incident is to avoid trusting sandbox isolation as a sole defense. @martin_casado made the strongest steelman: covert channels across air gaps are old, throughput can be tiny, and the real takeaway is layered defense rather than sensationalism. At the same time, @WSJ and @jeffjarvis pushed back on “rogue AI” framing entirely, arguing these events still reduce to human-configured systems doing what people enabled them to do.
>
> Policy pressure is building around safety laws and operational accountability: @TheRundownAI reported that California Gov. Gavin Newsom signed an executive order convening an expert panel to recommend stronger AI safety laws, including possible kill switches, embedded outside monitors, and required safety plans. Meanwhile, @sayashk pointed to a mismatch between rhetoric and incentives in AI security, criticizing OpenAI’s reported $6,500 bug bounty to a researcher who broke into an internal repo and disclosed it. The common theme across these posts is straightforward: independent oversight, layered defenses, and security incentives are moving from abstract governance talk into concrete operational design.
>
> AI Reddit Recap
>
> /r/LocalLlama + /r/localLLM Recap
>
> Read more

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。