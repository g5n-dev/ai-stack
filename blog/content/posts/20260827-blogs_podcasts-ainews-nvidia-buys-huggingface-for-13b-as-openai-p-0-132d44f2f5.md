---
title: "[AINews] NVIDIA buys HuggingFace for $13B, as OpenAI publishes their HF incident retro"
date: 2026-08-27T17:49:49+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "Prompt 工程", "博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:fcc11c5efafa510a71f4a3880f263b6147a7f4d123ac21e764de4f931c3656e0"
source_payload_sha256: "sha256:be313499f4c80b3f665c162c4544fb7a592d538e9986b77bffde0f30141e7ceb"
observation_id: obs_132d44f2f5aac4508f25a1ee0623f9e1f8c0f581b9e0c635c87ac9233a177ad8
event_id: evt_b1feaf5390f9d69bbe4c3a2de3b2fd2b57b42ede745f35ec7a6ab51690ef02c1
revision_id: rev_e9faadb6a7b082a9f66967f0c0dfd908b1850e0eeec3aeb97e6fd3e6fa7c4166
source_published_at: 2026-08-27T01:50:54Z
first_seen_at: 2026-08-27T09:59:38Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 86
description: "当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。"
external_url: https://www.latent.space/p/ainews-nvidia-buys-huggingface-for
parent_observation_id: null
last_seen_at: 2026-08-31T00:00:00Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://www.latent.space/p/ainews-nvidia-buys-huggingface-for](https://www.latent.space/p/ainews-nvidia-buys-huggingface-for)
- **发布域名**: www.latent.space

## 来源摘要/节选

> TheInformation had the scoop, and now they have the confirmation — Nvidia is buying HuggingFace for $13B, roughly 80x their $150M ARR, having doubled its customer base in 2026. This is almost double Nvidia’s initial $7B offer in Jan 2026.
>
> What can we say? We love it when the good guys win. But in the backdrop of GLM-5.3-Flash (aka Ox Alpha) impressing everyone (except GDM vaguepoasters) and Qwen also shipping an impressive Flash model on chinese chips, perhaps the post Hot Chips conversation about Western open AI is a great backdrop for this.
>
> AI News for 8/25/2026-8/26/2026. We checked 12 subreddits, 544 Twitters and no further Discords. AINews’ website lets you search all past issues. As a reminder, AINews is now a section of Latent Space. You can opt in/out of email frequencies!
>
> AI Twitter Recap
>
> Top Story: GLM 5.3 Flash launch and reactions
>
> What happened
>
> Z.ai formally launched GLM-5.3-Flash, revealing that the previously previewed “Ox Alpha” model is its public identity.
>
> Z.ai announced GLM-5.3-Flash as a natively multimodal model with a 1M-token context window, 320B total parameters / 18B active parameters, released under the MIT License, and available via weights, API, chat, coding plan, and AutoClaw.
>
> Z.ai simultaneously positioned it as a highly price-competitive successor to GLM-5.2, claiming on its internal benchmark that it outperforms GLM-5.2 at every effort level and is on par with Claude Opus 4.8 on coding.
>
> The launch also resolved the long-running Ox Alpha mystery: multiple posters explicitly connected Ox Alpha to GLM-5.3-Flash, including SemiAnalysis, rasbt, theo, and Cline.
>
> Early third-party model infrastructure support appeared almost immediately: CoreWeave, Baseten, and Cline’s free integration in VS Code / JetBrains / CLI.
>
> Shortly after launch, Z.ai engineer Zixuan Li said the chat template had been updated and early downloaders should re-download the model, implying a day-0 packaging or prompt-format correction.
>
> Artificial Analysis first published an overview with an incorrect 400k context window, then issued a correction to 1M context, aligning with Z.ai’s original announcement.
>
> Community response was unusually strong for an open-weight release, ranging from brief shock reactions like “HOLY” to more substantive claims that the model may now be the best intelligence-per-dollar option, e.g. Artificial Analysis and zainhas.
>
> The launch got folded into a broader narrative around Chinese frontier open models, with posts arguing that open Chinese labs are converging on similar architecture choices around linear attention, sparse attention, residual path design, and Muon.
>
> Independent pushback emerged on at least one modality claim: skalskip92 argued the model looks weak on several vision/object detection tasks despite being “native vision.”
>
> Official claims and launch details
>
> Z.ai’s primary launch tweet is the factual anchor: GLM-5.3-Flash is described as:
>
> 320B total params / 18B active
>
> 1M-token context
>
> natively multimodal
>
> MIT licensed
>
> previously previewed as Ox Alpha
>
> “running entirely on Chinese AI chips”
>
> Distribution/availability at launch:
>
> Weights on Hugging Face
>
> Z.ai API
>
> Chat
>
> ZCode
>
> Coding plan
>
> AutoClaw
>
> The strongest self-reported vendor performance claim came from Z.ai’s coding thread: on the Z.ai Code Bench, GLM-5.3-Flash “clearly outperforms GLM-5.2 at every effort level and performs on par with Claude Opus 4.8”. Because this is first-party benchmarking, it is useful but should be read more cautiously than independent evals.
>
> A follow-up launch-support post from AutoClaw framed the model as suitable for vision-language understanding, code generation, and long-horizon agentic tasks and paired availability with credits/rebates, but this is mainly rollout information rather than new technical evidence: AutoClaw launch post.
>
> Independent benchmarks and cost/performance positioning
>
> The most substantive independent evaluation in the tweet set came from Artificial Analysis. Their summary: GLM-5.3-Flash scores 57 on the Artificial Analysis Intelligence Index.
>
> Artificial Analysis metrics cited
>
> AA Intelligence Index score: 57
>
> Gap vs GLM-5.3: 3 points behind GLM-5.3 at 60
>
> Cost per task: $0.09
>
> API price: $0.15 / 1M input, $0.50 / 1M output
>
> Cached input: ~$0.026–$0.03 / 1M, described as 80% discount
>
> Model size: 320B total / 18B active
>
> License: MIT
>
> Context: initially listed as 400k, later corrected to 1M
>
> Comparisons cited by Artificial Analysis
>
> Ties GPT-5.6 Terra and Muse Spark 1.2 at 57, but at much lower cost per task.
>
> $0.09/task vs $0.68/task for GLM-5.3 max.
>
> Claimed ~7.5x lower cost per task than GLM-5.3 max.
>
> Claimed ~5.7x cheaper per task than GPT-5.6 Terra and ~4.4x cheaper than Muse Spark 1.2.
>
> Token-efficiency and reasoning mix
>
> Artificial Analysis notes an interesting tradeoff:
>
> GLM-5.3-Flash used 149M output tokens to run the Intelligence Index
>
> compared with 168M for GLM-5.3
>
> but more than Kimi K3 (133M) and Qwen3.8 2.4T A95B (136M) at similar Intelligence Index score
>
> 134M of the 149M tokens (~90%) were reasoning tokens
>
> This is an important nuance: the model’s economics look excellent largely because token pricing is extremely low, not because it is especially token-frugal.
>
> Agentic/work evals from Artificial Analysis
>
> Artificial Analysis also reports that GLM-5.3-Flash is stronger than its raw knowledge metrics might imply on agentic tasks:
>
> GDPval-AA v2 Elo: 1770
>
> tied within margin of error with GLM-5.3 and Grok 4.6
>
> behind only Claude Opus 5 xhigh/max
>
> Terminal-Bench v2.1: 84.3% vs 83.9% for GLM-5.3
>
> τ³-Banking: 47.2%, trailing GLM-5.3 by 3.1 percentage points
>
> Knowledge/hallucination stats
>
> AA-Omniscience score: +7
>
> Accuracy: 28%
>
> Hallucination rate: 28%
>
> Compared with GLM-5.3:
>
> GLM-5.3 accuracy 34%
>
> GLM-5.3 hallucination rate 30%
>
> Compared with GPT-5.6 Terra:
>
> Terra accuracy 47%
>
> This suggests a recurring theme in reactions: GLM-5.3-Flash may be much stronger on practical code/agentic workflows than on broad real-world factual knowledge.
>
> Architecture and systems details
>
> Several technically informed reactions tried to reverse engineer or summarize what changed from GLM-5.2 / GLM-5.x.
>
> The most detailed public architecture breakdown in the tweet set came from rasbt, who says GLM-5.3-Flash moves from GLM-5.2’s 744B-A40B backbone to 320B-A18B, and uses:
>
> Kimi Linear-style 3:1 hybrid attention
>
> 34 KDA layers (Kimi Delta Attention)
>
> 11 MLA/DSA layers
>
> MLA = Multi-head Latent Attention
>
> DSA = DeepSeek Sparse Attention
>
> DeepSeek V4-style mHC residual path
>
> four parallel streams
>
> plus a native vision encoder
>
> The same tweet describes it as “super hybrid” because both major attention components are already “efficient” variants rather than a simple efficient/full-attention hybrid.
>
> Another useful systems-oriented summary from thealexker frames the release as an efficiency story, highlighting:
>
> compared to GLM-5.2:
>
> ~1/10 the cost
>
> active params 32B → 18B
>
> layers 92 → 45
>
> hybrid linear + sparse attention
>
> smaller average KV cache per layer
>
> lower attention compute compounding at long contexts
>
> claims that visual intelligence benefited from coding/RL style improvements
>
> says the GLM-5.3 infrastructure agent co-authored parts of the work by helping with kernels, bottlenecks, and serving stack optimization
>
> The broader context post from eliebakouch is opinionated but technically notable because it places GLM in a Chinese open-model trend:
>
> nearly all Chinese frontier models now use linear attention
>
> nearly all use sparse attention / indexer-compression designs
>
> many use fancy residuals like mHC, attention residuals, gated residuals
>
> many use Muon
>
> That post is not a direct GLM paper summary, but it helps explain why the architecture details immediately resonated with model engineers: GLM-5.3-Flash appears to be another data point in a fast-converging efficiency-first Chinese frontier OSS design space.
>
> Chinese chip angle and serving implications
>
> The hardware/serving side was one of the most-discussed parts of the launch.
>
> Z.ai itself said the model was “running entirely on Chinese AI chips”. The strongest amplification came from SemiAnalysis, which focused on the claim that 100T tokens/day are being served on Chinese chips. That tweet does not provide all the derivation, but it framed the infrastructure feat as the most shocking part of the reveal.
>
> Reactions emphasized the significance:
>
> theo: “Ox being a ‘flash’ model is insane. Serving all the traffic on Chinese chips is even more insane.”
>
> same-day OSS mood post folded GLM into a broader celebratory open-source narrative.
>
> There was also explicit back-of-envelope capacity reasoning from teortaxesTex:
>
> If inference economics are comparable to V4-Flash,
>
> 10K tokens/s/NPU is “realistic”
>
> 864M/day per chip
>
> 100T/day would imply about 116K chips
>
> suggesting 100K+ chips scale, “doable” but consuming an enormous fraction of total compute
>
> That estimate is speculative rather than confirmed, but it shows how engineers interpreted the serving claim: not as marketing fluff alone, but as an infrastructure statement implying very large domestic accelerator fleets and mature inference optimization.
>
> Adoption and distribution reactions
>
> A notable part of the reaction cycle was how quickly usage posts appeared.
>
> Cline said GLM-5.3 Flash was already its fastest growing model in Cline history, driving 11% of all traffic in less than a week, while also advertising it as free in Cline. This is partly promotional, but it is also a concrete demand signal.
>
> Infrastructure providers moved quickly:
>
> CoreWeave: “coming soon to CoreWeave Serverless Inference”
>
> Baseten: day-0 availability, emphasizing general intelligence + agentic coding, native vision, and 1M context
>
> Dell via Jeff Boudier: framed GLM 5.3 Flash and Qwen 3.8 Flash as open models ready for on-prem deployment
>
> This matters because it reinforces that GLM-5.3-Flash was not treated as a curiosity; it was immediately slotted into real inference/developer stacks.
>
> Facts vs opinions
>
> Facts / externally attributable claims
>
> Z.ai launched GLM-5.3-Flash as 320B total / 18B active, 1M context, MIT-licensed, multimodal, previously previewed as Ox Alpha.
>
> Z.ai claims the model runs on Chinese AI chips.
>
> Artificial Analysis reports AA Intelligence Index 57 and $0.09 cost/task, plus various benchmark details and pricing.
>
> Artificial Analysis later corrected its context listing from 400k to 1M.
>
> Zixuan Li said the chat template was updated and model users should re-download.
>
> Cline said the model drove 11% of all traffic in under a week.
>
> Baseten, CoreWeave, AutoClaw, and others announced support/distribution.
>
> Opinions / interpretations
>
> theo, zephyr_z9, and nicdunz expressed strong positive surprise.
>
> thealexker interpreted the release primarily as a story of efficiency engineering.
>
> eliebakouch framed it as evidence of exciting convergence in Chinese frontier open architectures.
>
> zainhas argued it is now the best intelligence-per-dollar choice.
>
> skalskip92 argued the model is bad at vision, pushing back on the launch’s multimodal framing.
>
> scaling01 alleged it was “painfully obvious” Ox Alpha was a GLM model and further alleged ZAI used hype accounts; that claim is unverified in the tweet set.
>
> Different perspectives
>
> Read more

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。