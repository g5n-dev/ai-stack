---
title: "[AINews] Kimi K3 2.8T-A50B: the largest open model ever released; Opus 4.8-class at Sonnet 5 pricing"
date: 2026-07-17T11:39:12+08:00
draft: false
entry_kind: "auto"
tags: ["博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:18256fe603414f55b78587f912ce025f27a2d128797d92d5859ded98c6d6cb4f"
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: true
source_truncation_reason: "crawler_feed_content_limit"
source_support: 1.0
source_title_chars_original: 100
description: "当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。"
external_url: https://www.latent.space/p/ainews-kimi-k3-28t-a50b-the-largest
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://www.latent.space/p/ainews-kimi-k3-28t-a50b-the-largest](https://www.latent.space/p/ainews-kimi-k3-28t-a50b-the-largest)

## 来源摘要/节选

> Z.ai GLM has been getting a bit too much love recently, so it’s time for Kimi K3 to fight back! It’s hard to put the scale of today’s open model release in perspective, so thankfully Moonshot AI did it for us:
>
> Their vibe reel was entirely edited by Kimi K3 and worth a watch:
>
> You can read SimonW and Arena for standard takes and rankings, none of which will be particularly unexpected given the large size of the model, but this pic best summarizes the K2.5 to K3 jump:
>
> AI News for 7/15/2026-7/16/2026. We checked 12 subreddits, 544 Twitters and no further Discords. AINews’ website lets you search all past issues. As a reminder, AINews is now a section of Latent Space. You can opt in/out of email frequencies!
>
> AI Twitter Recap
>
> Moonshot AI launched Kimi K3 as a frontier-class open-weights model, with official claims that place it near top closed models and above prior open competitors.
>
> Moonshot officially introduced Kimi K3 as “Open Frontier Intelligence” with 2.8T total parameters, 1M-token context, native multimodal input, Kimi Delta Attention (KDA), and Attention Residuals, and said the model is live on Kimi.com, Kimi Work, Kimi Code, and API, with open weights promised by July 27, 2026 @Kimi_Moonshot
>
> Moonshot also highlighted product positioning around long-horizon agentic coding and self-evolving workflows, plus “vision in the loop” coding/game-building workflows that iterate between code and screenshots @Kimi_Moonshot
>
> Before the formal announcement, multiple accounts circulated leaked or app-sourced details that K3 was 2.8T params, calling it the largest open-weight model ever if weights ship as promised @scaling01, @scaling01, @eliebakouch
>
> The official Kimi blog went live later and was widely shared as the primary technical source @Jianlin_S, @scaling01, @Yulun_Du
>
> Moonshot’s own phrasing acknowledged a limitation: despite being highly competitive overall, K3 still has a “noticeable gap in user experience” versus Claude Fable 5 and GPT-5.6 Sol @scaling01
>
> Arena announced that Kimi K3 entered Agent Arena, plus Text, Vision, Document, and Frontend Code Arena, with community evaluations to follow @arena
>
> Arena then reported a major early result: Kimi K3 became #1 in Frontend Code Arena with 1679 points, surpassing Claude Fable 5 and jumping from #18 (K2.6) to #1, ranking #1 in 6 of 7 frontend domains and #2 in Gaming @arena
>
> Arena later added that K3 has a 76% pairwise win rate in Frontend Code Arena, versus 63% for Fable 5 and 58% for GPT-5.6 Sol @arena
>
> In Text Arena, K3 landed at #9 with 1486 points, a jump from #38, with top-10 placements in creative writing, coding, and instruction following, and #1 in several occupation slices @arena
>
> Artificial Analysis published an independent evaluation placing K3 at 57 on the AA Intelligence Index, calling it comparable to Opus 4.8 and GPT-5.5, but still behind Fable 5 and GPT-5.6 Sol overall @ArtificialAnlys
>
> AA also reported K3 at 1668 Elo on GDPval v2, 53% / #1 on AutomationBench-AA, and 1547 Elo on AA-Briefcase, with cost per task of $0.94, about 21% fewer output tokens than K2.6 across the full Intelligence Index run @ArtificialAnlys
>
> The launch immediately triggered strong reaction from engineers and model-watchers who framed K3 as an open-model milestone comparable to earlier DeepSeek moments @kimmonismus, @nrehiew_, @eliebakouch
>
> Technical details
>
> Architecture and systems details
>
> Official specs: 2.8T total parameters, 1M context, native multimodal input (text + images), text output, open weights by July 27 @Kimi_Moonshot, @ArtificialAnlys
>
> K3 uses Kimi Delta Attention (KDA), which Moonshot says enables up to 6.3x faster decoding in million-token contexts @Kimi_Moonshot
>
> It also uses Attention Residuals (AttnRes), claimed to deliver ~25% higher training efficiency at &lt;2% additional cost @Kimi_Moonshot
>
> Community readers of the blog highlighted additional architecture details: LatentMoE / Stable LatentMoE, 16 activated experts out of 896, implying an activation ratio under 2% @nrehiew_, @eliebakouch
>
> More community-extracted details from the blog/report discussion: per-head Muon, QB load balancing / quantile load balancing, and a new activation function called SiTU (Sigmoid Tanh Unit) @eliebakouch
>
> One engineer noted the architecture as notable for combining KDA + LatentMoE + AttnRes while scaling more than 2x over prior Kimi models @teortaxesTex
>
> KDA had a long incubation cycle: design reportedly started in Jan 2025 and took ~1.5 years to reach frontier scale @zxytim
>
> Inference and serving
>
> K3 pricing was reported as $3 / 1M input tokens and $15 / 1M output tokens, with cached input discounted 90% to $0.30 / 1M @scaling01, @ArtificialAnlys
>
> Several posters compared that pricing to Sonnet 5, with some noting Sonnet was temporarily cheaper until end of August, after which prices align more closely @kimmonismus
>
> A blended estimate at 80% input / 20% output came out to $5.40 / 1M tokens, vs $9 for Opus 4.8 and $10 for GPT-5.5 @jaminball
>
> Artificial Analysis estimated $0.94 average cost per Intelligence Index task, versus $1.04 for GPT-5.6 Sol and $1.80 for Opus 4.8 @ArtificialAnlys
>
> Early live serving observations: ~28 tok/s via Moonshot API on OpenRouter @scaling01, and another observer saw 26 tok/s, calling it slower than Opus and speculating that speculative decoding wasn’t yet enabled @nrehiew_, @nrehiew_
>
> Moonshot’s blog reportedly recommends deployment on supernode configurations with 64+ accelerators for best inference efficiency @teortaxesTex
>
> vLLM said Moonshot contributed a KDA prefix caching implementation directly to vLLM, with support available day 0 for official release @vllm_project
>
> Moonshot’s KDA contribution was cited as important because KDA breaks assumptions behind conventional prefix caching, so upstream runtime changes were required @vllm_project
>
> Benchmarks and evals
>
> Moonshot’s official benchmarking message, as summarized by others, positioned K3 behind only Claude Fable 5 and GPT-5.6 Sol among tested models, and ahead of Claude Opus 4.8 @scaling01, @Yuchenj_UW
>
> One cited number: 1687 on GDPval-AA v2, above Opus 4.8 and behind GPT-5.6 Sol at 1747.8 in that comparison @scaling01
>
> Artificial Analysis’ independent numbers:
>
> AA Intelligence Index: 57
>
> GDPval v2 Elo: 1668
>
> AutomationBench-AA: 53%, #1
>
> AA-Briefcase Elo: 1547
>
> AA-Omniscience: +18, with accuracy 46% vs 33% on K2.6, but hallucination rate worsening to 51% from 39% @ArtificialAnlys, @ArtificialAnlys
>
> AA also reported 132M output tokens consumed for K3 across the Intelligence Index, versus 166M for K2.6, i.e. 21% reduction while gaining 13 index points @ArtificialAnlys
>
> Arena’s frontend result was especially prominent because it is a pairwise human-preference arena, not just a static benchmark, and K3’s #1 frontend rank became one of the main launch headlines @arena
>
> Community posts also highlighted strong results on kernel optimization tasks, with some saying K3 was matching or beating Fable in certain kernel/codegen settings @nrehiew_, @scaling01
>
> One benchmark caveat came from ProgramBench author Ofir Press, who said Kimi used a metric they do not recommend: averaging implementation percentage rather than counting fully working programs, which can overstate usefulness @OfirPress, @OfirPress
>
> Facts vs opinions
>
> Facts / directly sourced claims
>
> Kimi K3 is officially announced by Moonshot @Kimi_Moonshot
>
> Officially disclosed specs include 2.8T params, 1M context, native multimodal input, KDA, AttnRes, open weights by July 27 @Kimi_Moonshot
>
> Artificial Analysis independently scored K3 at 57 Intelligence Index, with detailed task, cost, token, and benchmark data @ArtificialAnlys
>
> Arena independently ranked K3 #1 in Frontend Code Arena and later reported its 76% pairwise win rate @arena, @arena
>
> vLLM confirmed Moonshot contributed runtime support for KDA prefix caching @vllm_project
>
> Opinions / interpretations
>
> “DeepSeek moment,” “beginning of the US-China AI race,” and “everything changed” are editorial interpretations from observers, not established facts @kimmonismus, @scaling01, @kimmonismus
>
> Claims that K3 “beats GPT-5.6 Sol on 11 of 14 benchmarks” and “Fable on 6 of 14” are aggregated community summaries and should be treated as contingent on the benchmark set and exact methodology @scaling01
>
> Assertions that this implies Dario/Anthropic margin pressure, a geopolitical turning point, or near-term superintelligence are speculative commentary @teortaxesTex, @Jason
>
> Several “distillation” insinuations were explicitly framed as jokes or conjecture rather than evidence @yacinelearning, @dejavucoder
>
> Different opinions
>
> Strongly supportive
>
> Many engineers called K3 a genuine frontier open model, especially because it appears to be better than Opus 4.8 while being priced near Sonnet and planned for open-weight release @kimmonismus, @cline, @nrehiew_
>
> Supporters emphasized that this is no longer “good for open source,” but simply competitive with top public closed models @tokenbender, @TheAhmadOsman
>
> Some framed the release as evidence that open models are now within weeks or a couple months of the frontier @nrehiew_
>
> Others argued this materially raises the odds that future AGI-level systems are open @MaorShlomo
>
> Supportive but technically cautious
>
> Artificial Analysis gave a more restrained view: K3 is comparable to Opus 4.8 and GPT-5.5, but still behind Fable 5 and GPT-5.6 Sol on overall intelligence @ArtificialAnlys
>
> Simon Willison described K3 as significant, but also pointed readers toward nuanced notes and benchmark caveats rather than simple leaderboard hype @simonw
>
> Ethan Mollick’s hands-on impression: very good open-weights model, but not Sol Max or Fable @emollick
>
> One user said K3’s intelligence is strong, but it is slow, sometimes over-checks, and still trails Claude on taste/aesthetics @nrehiew_
>
> Critical / skeptical
>
> Bindu Reddy warned that K3’s benchmark story might be overstated unless validated on hidden / uncontaminated evals like LiveBench, and argued that if the model “thinks forever,” real cost could be less favorable @bindureddy
>
> ProgramBench maintainers objected to Moonshot’s metric choice, saying it can inflate partial-credit performance relative to fully working programs @OfirPress
>
> Artificial Analysis also flagged a real weakness: hallucination rate regressed on AA-Omniscience despite accuracy gains @ArtificialAnlys
>
> Multiple users noted that K3 currently appears to think a lot, preserve long reasoning history, and may require more careful harness support than simpler chat-first APIs @scaling01, @Xianbao_QIAN
>
> Some skepticism focused on economics and deployability: 2.8T open weights is impressive, but practical self-hosting may still be limited to well-funded teams @mbusigin
>
> Political / strategic interpretations
>
> A broad cluster of tweets framed K3 as proof that Chinese labs are no longer far behind and that the US lead is shrinking @tszzl, @kimmonismus, @scaling01
>
> Others counterweighted that K3 still appears to lag the very best Western models in usability / productization, even if raw capability is close @RyanGreenblatt, @scaling01
>
> Some argued that open Chinese models function as economic pressure on US labs by compressing margins and commoditizing capability @francoisfleuret
>
> Others viewed the inevitable next step as more competition on harnesses, products, and deployment systems, not just raw model weights @AravSrinivas, @theo
>
> Context
>
> Why this matters technically
>
> K3 is notable not just for raw size but for scaling a non-standard attention stack into a frontier-class model: KDA + AttnRes + sparse MoE drew repeated attention from technically literate observers @scaling01, @eliebakouch
>
> The launch is also a systems story: long-context serving, prefix caching, KDA runtime support, and deployment on large accelerator supernodes all matter if the weights are to be practically usable @vllm_project, @teortaxesTex
>
> The emphasis on kernel optimization, chip design, agentic coding, and environment simulation suggests Moonshot is optimizing for AI-improving-AI workflows, not just chatbot benchmarks @18jeffreyma, @yong_zhengxin
>
> Why this matters economically
>
> The strongest repeated theme: frontier-ish performance at materially lower price than top closed models, though not at bargain-basement open-model prices @kimmonismus, @cline, @jaminball
>
> Artificial Analysis’ task-cost framing is especially relevant for practitioners: if K3 is near GPT-5.6 Sol cost-per-task and below Opus 4.8, the real question becomes where it slots into agent stacks, coding platforms, and self-hosted infra @ArtificialAnlys
>
> Some noted the paradox that “open weights” does not automatically mean “cheap to run”: a 2.8T model with 64+ accelerator deployment guidance is frontier infrastructure territory @teortaxesTex, @mbusigin
>
> Why this matters geopolitically
>
> Many reactions explicitly tied K3 to export controls, US-China competition, and the narrowing gap between Chinese open labs and US closed labs @scaling01, @tszzl, @kimmonismus
>
> Several commentators argued that K3 weakens the common narrative that Chinese models trail by 6–8 months, because it appears to outperform a closed US model from late May only weeks later @kimmonismus
>
> Others stressed that “capability parity” is not the same as full-stack parity: product reliability, inference scale, deployment margins, and proprietary post-training may still favor US incumbents @RyanGreenblatt
>
> Early hands-on signals
>
> Users reported K3 building impressive web experiences, games, and shader/code artifacts, reinforcing the Frontend Arena result @johnlindquist, @ChrissGPT, @intheworldofai
>
> One user said K3 generated a CS:GO × Portal clone in 3 shots using ~600k tokens, costing $3.24 by API pricing, compared with claimed higher costs on Fable and GPT-5.6 Sol @ChrissGPT
>
> Another reported K3 continuously working for hours over near-1M context to build a web DOS emulator with low human intervention @bigeagle_xd
>
> At the same time, several users noted it can be verbose, slow, and heavily reliant on thinking-history preservation, implying that serving/harness defaults will matter a lot @nrehiew_, @Xianbao_QIAN, @bigeagle_xd
>
> Open-source/open-weights debate
>
> The surrounding discourse included the usual complaint that “open weight” is not “fully open,” but several commenters pushed back that this distinction is often impractical at frontier scale and that inspectable, fine-tunable weights still matter @Dan_Jeffries1, @ClementDelangue
>
> Yulun Du said the delay before weight release was to ensure a smooth rollout with inference partners, signaling that ecosystem readiness mattered as much as the checkpoint itself @Yulun_Du
>
> vLLM maintainers and others treated Moonshot’s upstream contributions as evidence that the launch is not just “marketing open,” but also includes meaningful OSS infra work @vllm_project, @woosuk_k
>
> Benchmarks, contamination, and what to watch next
>
> Several people cautioned that current public benchmark ecosystems saturate quickly, and that hidden evals or stack-level evals will be more informative @bindureddy, @gdb, @WolfBenchAI
>
> Observers specifically asked for follow-up on METR time horizons, cyber ranges, FrontierMath T4, ARC-AGI-2/3, CritPt, token usage, and broader long-horizon agent evals @scaling01
>
> The most credible near-term follow-up points are:
>
> whether the weights ship on time
>
> what third-party serving stacks achieve for throughput/cost
>
> how K3 performs on hidden evals and real production agent tasks
>
> whether Moonshot closes the UX/post-training gap they themselves acknowledged @Kimi_Moonshot, @scaling01, @ArtificialAnlys
>
> Open Models, Inference Stacks, and Retrieval Infrastructure
>
> vLLM and serving ecosystem support landed quickly: vLLM said Moonshot contributed a KDA prefix-caching implementation directly to vLLM, enabling day-0 support once weights drop. This matters because KDA breaks some conventional prefix-caching assumptions. The post underscores that long-context architectural innovation increasingly requires coordinated systems work, not just model release.
>
> NVIDIA shipped a notable open retrieval release: NVIDIA launched Nemotron 3 Embed 8B, claiming #1 overall on RTEB, and partners quickly made it deployable, including Baseten and Turbopuffer. A more detailed community summary by @kimmonismus reports 78.46 NDCG@10 on RTEB and 75.45 on MMTEB Retrieval, with NVIDIA arguing stronger retrieval reduces downstream agent token usage. The release also includes 1B BF16 and 1B NVFP4 variants, with the NVFP4 version reportedly offering up to 2× BF16 throughput on Blackwell while retaining &gt;99% retrieval quality.
>
> LiteParse added a gRPC interface for backend document pipelines: LlamaIndex introduced liteparse-grpc, exposing PDF/Office/image parsing, rendering, and OCR-complexity estimation over gRPC with protobuf definitions and generated clients. This is a practical infra improvement for polyglot microservice stacks where REST isn’t ideal.
>
> Managed vector/search infra also expanded: Weaviate announced Managed Weaviate on DigitalOcean in public preview, running the unmodified open-source engine (v1.37.1 at launch) with HA, autoscaling, backups, forks, and control-plane observability.
>
> Agents, Harnesses, and System Design Becoming the Real Product Layer
>
> Harnesses were a recurring theme across builders: Harrison Chase’s conversation with Factory AI’s Eno Reyes was repeatedly shared as a case for why “the harness matters more than the model” (Harrison, LangChain). Chase later argued teams should “own the harness,” “own the context and memory layer,” and “own model optionality” rather than rent intelligence from a single provider (thread).
>
> There’s growing interest in open standards for memory and knowledge representation: Harrison Chase promoted OKF (Open Knowledge Format) as an “open standard for memory,” while Brace Sproul detailed OpenWiki’s adoption and the benefits for search, retrieval, and codebase memory.
>
> Agent self-improvement and scheduled multi-agent workflows are becoming mainstream topics: @omarsar0 highlighted a survey on self-improving agentic systems, and elsewhere described using an “LLM Council” with recurring scheduled research updates (thread). On the product side, Google AI Studio added a free tier for Managed Agents, plus max_total_tokens for pausing/resuming long runs and native cron triggers.
>
> Perplexity’s infra direction was also notable: NVIDIA AI Infra highlighted Perplexity’s new SPACE secure sandbox platform, with early tests on NVIDIA Vera CPU showing up to 1.9× faster sandbox starts—a reminder that sandbox startup latency is now part of agent throughput engineering.
>
> OpenAI and Anthropic: Safety, Productization, and Developer Workflow Updates
>
> OpenAI acknowledged a dangerous Codex/GPT-5.6 failure mode around file deletion: Thomas Sottiaux said OpenAI investigated rare reports where GPT-5.6 unexpectedly deleted files, most commonly when full access mode was enabled without sandboxing or auto review, and when the model attempted to override $HOME for temp directories but mistakenly deleted $HOME itself. OpenAI says it is updating developer messaging, nudging users toward safer permission modes, and adding harness safeguards, with a detailed postmortem forthcoming.
>
> OpenAI continued to ship workflow features around Codex and PR review: OpenAI Devs added PR Chat and inline code editing in Codex for reviewing and editing pull requests in context. OpenAI also announced Office Hours around GPT-5.6, ChatGPT, and Codex (source).
>
> Anthropic upgraded Claude Code review depth: ClaudeDevs introduced effort levels for /code-review, from low cost/low effort to ultra, where a fleet of reviewer agents reproduces findings independently. Anthropic says low effort beats other code-review tools on findings per token, while high/ultra improve severe-issue recall and reduce false positives.
>
> Voice remains a major adoption vector: Sam Altman said he now talks to ChatGPT more than he types, calling the new voice model a threshold-crossing UX shift. Separately, OpenAI published GPT-Live usage limits in its help center, summarized by @athyuttamre: Pro users get unlimited daily usage, while Plus/Go and free tiers have bounded live minutes.
>
> Multimodal Video, Real-Time Media, and Creative Tooling
>
> Google pushed Gemini Omni into Vids: Google and Google Workspace launched Gemini Omni for video generation/editing in Google Vids, plus personal avatars built from a selfie and voice recording. Google says generated clips include SynthID watermarking and that avatars are restricted to a user’s own account/likeness (details).
>
> NotebookLM’s rebrand signals tighter Google product integration: Gemini Notebook announced that NotebookLM is now Gemini Notebook, with existing standalone behavior intact but deeper integration coming via the Gemini app and eventually Search. This looks like a packaging/integration move more than a model change.
>
> Real-time and agentic media tooling kept advancing: DecartAI introduced Lucy 2.5, a more capable realtime live AI video editor; fal made Lucy 2.5 Realtime available over WebRTC for live video-to-video editing. fal also launched LTX-2.3 Reframe for aspect-ratio conversion with generated scene completion.
>
> Meta expanded media model distribution: Meta, AI at Meta, and Alexandr Wang all announced Muse Spark 1.1 on OpenRouter, reflecting continued demand for frontier-ish generative media models via neutral routing layers.
>
> Robotics, World Models, and Embodied AI
>
> A high-reliability robotics model stood out: Tony Zhao introduced ACT-2 Preview, described as the first robotics model to unify broad generalization with high reliability. The headline claim is striking: a single fine-tuning example can teach Memo a new behavior that generalizes, with zero-shot, real unseen homes, 99% success rate.
>
> Reka discussed world-model data operations at production scale: Reka pointed to an episode on how a sub-100-person team prepares petabytes of video data for world model training, emphasizing that the bottleneck is often data platform engineering, not just model architecture.
>
> There’s continuing work on embodied world-model architectures: @lixin4ever highlighted a DAMO effort using tri-branch DiT, joint cross-modal attention, and 250M+ RGB frames with dense depth and optical flow annotations to turn a video generation model into a 4D embodied world model.
>
> Top Tweets (by engagement)
>
> Kimi K3 official release: Moonshot’s launch post was the day’s dominant technical tweet, combining model specs, architecture, and release timeline.
>
> Kimi K3 Arena breakthrough: Arena’s Frontend Code Arena #1 post drew exceptional engagement because it framed K3 as not just strong “for open weights,” but directly ahead of a top closed competitor in a visible product task.
>
> OpenAI safety incident disclosure: OpenAI’s explanation of GPT-5.6 file deletions was one of the most consequential engineering/safety updates, because it tied model behavior to permission modes, sandboxing, and harness safeguards.
>
> Anthropic’s multi-effort code review: Claude Code’s /code-review effort levels is a meaningful productization signal for agentic software engineering: not just “AI review,” but tunable cost/recall tradeoffs and subagent-based verification.
>
> AI Reddit Recap
>
> /r/LocalLlama + /r/localLLM Recap
>
> 1. Kimi K3 Launch and Frontier Benchmarks
>
> Kimi K3 weights to be released on the 27th. (Activity: 399): The announcement image states that Kimi K3 is now available through kimi.com, the Kimi app, Kimi Work desktop client, Kimi Code, and the Kimi API, with the current default “thinking intensity” set to max / extreme. Per the linked official posts (WeChat, English blog), full model weights and additional technical details are scheduled for release by July 27, 2026, which is the main technical significance of the image. Commenters are excited about the open-weight release but expect local inference to be impractical due to the model’s apparent scale, joking that even if someone runs the rumored 2.8T-parameter model on a 24 GB VRAM laptop, it would be at unusably low throughput.
>
> Commenters highlight that Kimi K3’s apparent 2.8T-parameter scale makes local inference impractical for nearly all consumer setups; one linked screenshot of the announcement/spec context is here. The discussion frames the weights release as valuable for openness and research even if typical

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。