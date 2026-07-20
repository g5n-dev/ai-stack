---
title: "[AINews] Thinky's Inkling: 975B-A41B multimodal, new best American Apache 2.0 open model (with Inkling-Small, 276B-A12B)"
date: 2026-07-16T22:25:30+08:00
draft: false
entry_kind: "auto"
tags: ["博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:31d30a4aa5be081bb020345311c941d3d3130d08dd39c8e08f2ad8f928c6c340"
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 120
description: "当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。"
external_url: https://www.latent.space/p/ainews-thinkys-inkling-975b-a41b
observation_id: obs_34ced310fc3298ab86aede96334a8a6883c6a365ddeed3ecc1db91c0d6c2fd53
revision_id: rev_8e958f4873de8844b6a70a1f299d5793b27b8d68e9081f902f8de11f3b5188fc
event_id: evt_f4184901a1d493ae9a218d26043b17c1cf9861cf3cad18c5c24209a8c2b4b38f
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-16T14:27:34Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://www.latent.space/p/ainews-thinkys-inkling-975b-a41b](https://www.latent.space/p/ainews-thinkys-inkling-975b-a41b)

## 来源摘要/节选

> Thinky only seems to come up for air once every few months; most recently with Interaction models - but each time they do they impress, showing both taste and depth. Today they introduced Inkling — not a SOTA model, but a very solid new family for a baseline American open model:
>
> Our model, called Inkling, is a Mixture-of-Experts transformer with 975B total parameters, 41B active.
>
> It supports a context window of up to 1M tokens.
>
> It was pretrained on 45 trillion tokens of text, images, audio and video.
>
> It is the first in a family of models of different sizes: alongside it we are sharing a preview of Inkling-Small, a lighter-weight model with 12B active parameters, trained with a similar recipe, that achieves strong performance with even lower cost and latency.
>
> Inkling reasons natively over text, images, and audio, and balances cost with performance through efficient and controllable thinking effort
>
> The Huggingface breakdown covers some interesting technical highlights:
>
> AI News for 7/14/2026-7/15/2026. We checked 12 subreddits, 544 Twitters and no further Discords. AINews’ website lets you search all past issues. As a reminder, AINews is now a section of Latent Space. You can opt in/out of email frequencies!
>
> AI Twitter Recap
>
> What happened
>
> Thinking Machines Lab launched Inkling, its first fully released open-weights foundation model family entry, positioning it as a customizable multimodal base model rather than a benchmark-maxed flagship.
>
> Thinking Machines announced Inkling as an open-weights model that “reasons efficiently across text, image, and audio modalities,” with full weights available and immediate support on its Tinker platform and Playground @thinkymachines.
>
> Mira Murati described Inkling as the company’s “first model,” “trained from scratch,” with open weights and same-day fine-tuning on Tinker @miramurati.
>
> Soumith Chintala framed it as Thinking Machines’ “first general model,” stressing open weights, 975B parameters, native multimodality, and availability on Tinker, Hugging Face, and partners @soumithchintala.
>
> John Schulman added timeline context: pretraining began last winter, and from mid-January a small team built coding, reasoning, and agentic training on top @johnschulman2.
>
> Lilian Weng characterized Inkling as a foundation model aimed at “solid performance across a broad categories of capabilities” and intended for practical use plus customization @lilianweng.
>
> TML staff repeatedly emphasized that this is a day-1 release and a foundation for future iterations rather than their final frontier push @soumithchintala, @cHHillee, @keirp1.
>
> The release landed with unusually broad day-0 ecosystem support across vLLM, SGLang, Modal, Baseten, Databricks, Hugging Face, and quantization/community tooling @vllm_project, @lmsysorg, @modal, @baseten, @Yuchenj_UW, @huggingface, @danielhanchen.
>
> Independent commentators immediately tagged it as the strongest U.S.-based open-weight release so far, though generally still behind the top Chinese open-weight and best closed models on some benchmarks @natolambert, @ArtificialAnlys, @scaling01.
>
> Core facts and specs
>
> Model size, modality, licensing, context
>
> Inkling is reported as 975B total parameters / 41B active parameters in most posts @soumithchintala, @vllm_project, @ArtificialAnlys, @kimmonismus.
>
> One tweet says 974B @Yuchenj_UW, and another says 952B @multimodalart; the overwhelming consensus in the tweet set is ~975B.
>
> It is a Mixture-of-Experts model with 41B active parameters per token @VictoriaLinML.
>
> It is Apache 2.0 licensed according to multiple reactions and summaries @natolambert, @Yuchenj_UW, @multimodalart.
>
> It supports text, image, and audio inputs, with text output @soumithchintala, @TheRundownAI, @ArtificialAnlys.
>
> Open-weights checkpoints support up to 1M context @vllm_project, @lmsysorg, @ArtificialAnlys.
>
> Tinker/API context is described as 256K, with pricing differentiated for 64K and 256K contexts @ArtificialAnlys.
>
> Training and release details
>
> TML says Inkling was trained from scratch @miramurati, @LiorOnAI.
>
> Community readers extracted 45T training tokens from the release materials @eliebakouch, @ArtificialAnlys, while one post says 48T @mervenoyann. The more repeated figure in this dataset is 45T.
>
> Inkling includes controllable reasoning effort / numerical effort levels @LiorOnAI, @TheRundownAI, @danielhanchen.
>
> Tinker customers highlighted concise reasoning and strong tool calling rather than maximal raw benchmark chasing @tinkerapi, @MichaelElabd.
>
> Architecture details surfaced in reactions
>
> Several technically literate reactions extracted architectural choices from the release:
>
> Hybrid/sliding-window attention with a 5:1 local-to-global layer ratio and window size 512 @eliebakouch, @ariG23498.
>
> Relative positional encoding / relative attention bias instead of RoPE; multiple posters called this one of the most novel large-scale choices @stochasticchasm, @eliebakouch, @rasbt, @arohan, @ChangJonathanC.
>
> Short convolution layers added around attention/FFN streams; commenters flagged this as unusually scaled-up usage of short convs @eliebakouch, @stochasticchasm, @rasbt, @SonglinYang4.
>
> MoE with shared expert sinks / 2 shared experts, noted as atypical since many recent MoEs use 1 shared expert @eliebakouch, @ariG23498.
>
> DeepSeek-style auxiliary-loss-free load balancing was cited in community readings of the architecture @eliebakouch.
>
> muP and Muon/weight decay variants were inferred from the writeup and confirmed by optimizer expert reaction: Aaron Defazio said they are using his corrected weight decay approach, “MuonC/AdamC” @aaron_defazio, while community readers also pointed out muP @stochasticchasm, @Laz4rz.
>
> 8 MTP heads for speculative decoding were highlighted by vLLM @vllm_project.
>
> Variants
>
> Inkling-Small is repeatedly referenced as an upcoming or separately discussed smaller model @LiorOnAI, @teortaxesTex.
>
> Community summaries describe Inkling-Small as 276B total / 12B active and unexpectedly competitive versus the larger model on several evaluations @eliebakouch, @nrehiew_.
>
> Performance and benchmarks
>
> Independent benchmark framing
>
> Artificial Analysis said Inkling debuts at 41 on the Intelligence Index, making it the leading U.S. open-weights release and ahead of Nemotron 3 Ultra (38), Gemma 4 31B (29), and gpt-oss-120b (24) @ArtificialAnlys.
>
> Artificial Analysis also said Inkling averages 25K output tokens per Intelligence Index task, vs 43K for GLM-5.2 max, 38K for Kimi K2.6, and 37K for DeepSeek v4 Pro max, framing it as relatively token-efficient @ArtificialAnlys.
>
> Natolambert called it a “clear step up from Nemotron Ultra” and “new best American model,” but still “a bit behind GLM 5.2 on agentic benchies, and Kimi K 2.6 on multi modal” @natolambert.
>
> Design Arena said Inkling entered Agentic Web App Arena at #9 overall, Elo 1257, in the same band as Claude Opus 4.6 and Gemini 3.5 Flash, and called it the highest-ranking U.S.-based open-weight model for agentic workloads @DesignArena.
>
> Arena added Inkling to Agent Arena / Text / Vision / Code Arena on launch day @arena.
>
> Specific benchmark numbers cited
>
> From Artificial Analysis:
>
> GDPval-AA v2 Elo 1238, higher than Kimi K2.6 (1190) and DeepSeek v4 Flash max (1189) @ArtificialAnlys.
>
> τ³-Banking 24%, above Kimi K2.6 (21%) and slightly above DeepSeek v4 Flash max (23%) @ArtificialAnlys.
>
> Qualitative performance takes
>
> Positive:
>
> “Sharp and concise” reasoning, not rambly @MichaelElabd.
>
> Strong tool calling and good long-horizon error recovery on agentic tasks @MichaelElabd.
>
> Good “quality of mind” / unsycophantic flavor @skirano, @tinkerapi.
>
> Alex Kirillov claimed Inkling avoids the common “audio in = intelligence penalty” seen in many omni models, though another user asked for stronger supporting evidence and benchmarks @alex_kirillov, @giffmana, @alex_kirillov.
>
> More mixed / critical:
>
> Scaling01 argued the benchmarks are “not that great,” describing it as roughly “another Kimi-K2.6” and behind all closed models and GLM-5.2, speculating the release may have been timed ahead of Kimi-K3 and DeepSeek-V4-GA @scaling01.
>
> Stochasticchasm said it seems “very strong for multimodal” but “not super strong for terminal bench etc.” @stochasticchasm.
>
> JJitsev pushed back on hype around “only open-weight model trained without distilling,” saying Inkling uses distillation from open weights and underperforms GLM 5.2 on TerminalBench-style evals @JJitsev.
>
> TeortaxesTex offered a contrarian positive spin: mediocre benchmark-maxing may actually suggest less corner-cutting/distillation contamination and a more independent data pipeline @teortaxesTex.
>
> Inference, systems, and launch ecosystem
>
> Official and partner infrastructure facts
>
> NVIDIA said Inkling was trained on GB300 NVL72 and that an NVFP4 checkpoint was available on Hugging Face on day 0 @NVIDIAAI.
>
> vLLM said day-0 support includes NVFP4 and BF16, optimized for Blackwell and Hopper, reaching up to 380 tok/s/user on 4× GB200 with MTP @vllm_project.
>
> Inferact detailed system work: sconv-aware tensor-parallel sharding, low-latency fused collectives (5× faster at bs=1), and direct integration of TML’s FA4 sheared-bias kernel @inferact.
>
> LMSYS/SGLang said Inkling architecture support was implemented natively, including ShortConv, relative positional attention, shared expert sink MoE, prefill full CUDA graph, MXFP8 KV cache, full parameter and LoRA RL in customized Megatron backend, routing replay, cross-runtime parameter sync, and DFlash speculative decoding from Modal @lmsysorg.
>
> Modal said Inkling on Modal uses a custom DFlash speculator for 67% higher throughput and interactivity @modal.
>
> Soumith Chintala separately amplified that Modal’s DFlash speculator is “much faster than MTP” @soumithchintala.
>
> Community optimization observations
>
> Lysandre reported replacing TML’s causal Conv1D with causal-conv1d yielded +4% tok/s, and replacing attention with FlashAttention-4 yielded another +11%, for ~15% total throughput gain without retraining @LysandreJik.
>
> Unsloth released 1-bit GGUF quants said to be 86% smaller (270GB vs 1.9TB) while retaining 74.2% of top-1% accuracy, with vision and audio support @danielhanchen.
>
> Pricing and availability
>
> Artificial Analysis listed Tinker pricing as:
>
> 64K context: $1.87 / 1M input, $0.374 cached, $4.68 output
>
> 256K context: $3.74 / 1M input, $0.748 cached, $9.36 output
>
> @ArtificialAnlys
>
> Available on Tinker, Hugging Face, and via launch partners including Databricks, Baseten, Modal, vLLM/SGLang stacks @soumithchintala, @Yuchenj_UW, @baseten, @modal.
>
> Facts vs opinions
>
> Factual claims directly supported by launch and partners
>
> Open weights/full weights released @thinkymachines.
>
> Trained from scratch @miramurati.
>
> 975B total / 41B active MoE, multimodal text-image-audio input, 1M context on weights, 256K on Tinker/API @soumithchintala, @ArtificialAnlys.
>
> Apache 2.0 license @natolambert, @Yuchenj_UW.
>
> Pretraining began last winter; agentic/coding/reasoning work started mid-January @johnschulman2.
>
> Day-0 support on major serving stacks, with concrete performance claims from vLLM/Inferact/Modal/NVIDIA @vllm_project, @inferact, @modal, @NVIDIAAI.
>
> Interpretations and opinions
>
> “Best American open model” / “saved American open-source frontier” are judgments, albeit repeated by several respected observers @natolambert, @karinanguyen, @saranormous.
>
> Claims that Inkling is especially important because it is not distilled from OpenAI/Anthropic are disputed. Jxmnop called it “the ONLY open-weight model” without such distillation @jxmnop, then partially walked it back: “apparently they did distill lol. but only a tiny bit” @jxmnop. Andrew Carr also contested the purity framing, noting use of Kimi 2.5 for SFT traces @andrew_n_carr.
>
> Claims that Inkling was “rushed” ahead of Chinese releases are speculation from critics, not evidenced by the launch materials @scaling01.
>
> Claims that relative attention gives TML a finetuning moat because backward is hard are speculative @typedfemale.
>
> Claims that Inkling avoids multimodal intelligence loss are promising but not yet benchmark-complete in the tweet set @alex_kirillov.
>
> Different perspectives
>
> Supportive / bullish
>
> Open-weight and permissive license as strategic win: Many saw the Apache-2.0 release as a major boost to the U.S./Western open ecosystem @latkins, @saranormous, @brexton, @hyperindexed.
>
> Customization over leaderboard chasing: Researchers and builders praised the explicit framing that Inkling is a broad, tunable foundation rather than a benchmark-maxed point solution @gneubig, @ben_burtenshaw, @thealexker.
>
> Strong release quality: Several users praised the transparency, grounded tone, and comprehensive technical documentation @lvwerra, @saranormous, @rasbt.
>
> Architecture interest: The non-RoPE positional choice and scaled short-conv usage drew positive attention as evidence TML is willing to make meaningful architecture bets @stochasticchasm, @rasbt, @ChangJonathanC.
>
> Neutral / analytical
>
> Strong but not top overall: The most balanced reads place Inkling as the new U.S. open-weight leader, but behind GLM/Kimi/DeepSeek or top closed models on some fronts @natolambert, @ArtificialAnlys, @stochasticchasm.
>
> Good base model thesis: Multiple analysts read the release as a systems/business move: ship a solid, efficient, post-trainable base and let Tinker plus downstream RL/fine-tuning create differentiation @ben_burtenshaw, @kimmonismus, @tinkerapi.
>
> Critical / skeptical
>
> Not frontier overall: Critics argued it is still clearly behind top Chinese open-weight models and the strongest closed models @scaling01, @JJitsev.
>
> Purity claims overstated: Some pushback focused on exaggerated claims that it is uniquely “pure” or non-distilled; the thread set includes both hype and corrections @jxmnop, @jxmnop, @andrew_n_carr, @JJitsev.
>
> Benchmark middlingness as concern: Some readers saw the moderate benchmark profile as evidence it may simply lag current Chinese open frontier rather than inaugurate a new frontier @scaling01.
>
> Context: why this matters
>
> First major TML public model: This is the first true external model release from Thinking Machines after months of anticipation around a lab staffed by ex-OpenAI leaders and researchers. That made the choice of open weights itself notable @Hesamation, @TechCrunch.
>
> A U.S. open-weight answer to Chinese momentum: Many reactions explicitly compare Inkling to GLM, Kimi, DeepSeek, and Qwen. The release lands amid concern that Western open-weight models have trailed Chinese ones on capability and release cadence @scaling01, @teortaxesTex, @sriramk.
>
> Open base + post-training stack thesis: TML’s messaging strongly suggests a strategy similar to “ship a competent open substrate, then differentiate via customization/fine-tuning/RL infrastructure.” That aligns with Tinker distribution and with user reactions centering controllable reasoning, concise outputs, and adaptation rather than raw leaderboard supremacy @thinkymachines, @MichaelElabd, @ben_burtenshaw.
>
> Inference ecosystem maturity: The release also showcases how far open inference stacks have come. Day-0 support for a 1T-class multimodal MoE with new architectural components and multiple kernel-level optimizations would have been far less plausible a year earlier @vllm_project, @inferact, @LysandreJik.
>
> Architectural experimentation at scale: Relative positional bias instead of RoPE and large-scale short-conv usage are the kind of choices researchers watch closely because they may indicate future architecture trends if they prove robust under scaling and post-training @stochasticchasm, @rasbt, @ChangJonathanC.
>
> Release style as signal: Several commentators praised the unusually restrained release language, explicit admission that it is not the strongest overall model, and detailed technical notes. For expert audiences, that improved credibility relative to more benchmark-maxed launches @eliebakouch, @lvwerra, @thealexker.
>
> Read more

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。