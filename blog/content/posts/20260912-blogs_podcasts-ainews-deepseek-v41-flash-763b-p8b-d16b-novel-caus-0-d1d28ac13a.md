---
title: "[AINews] DeepSeek v4.1-Flash: 763B-P8B-D16B novel causal Encoder–Decoder architecture with vision marks the Return of the Whale"
date: 2026-09-12T17:24:29+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "Prompt 工程", "博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:a8cc36fed88cfb1887d50ed17b85afbd40b4df591e5da1b9944bd889a846d194"
source_payload_sha256: "sha256:43f85b23400e4d3448a62b6cf42b534a8a0e9cc7e65823da7dc60e8270e0a735"
observation_id: obs_d1d28ac13afc9a2440ec7617cdb40d2605964fc2717139c659c5df522ce97a7c
event_id: evt_d68aa487477b57d0449b44ae212d995b214f971fe6e9a0631e44231bb5ec6dc4
revision_id: rev_30630dfa0b011a1bee9164db33660ae10f5bea3c4294a46f1952718d4deca4df
source_published_at: 2026-09-12T05:56:05Z
first_seen_at: 2026-09-12T09:21:01.038232Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: true
source_truncation_reason: "crawler_feed_content_limit"
source_support: 1.0
source_title_chars_original: 127
interpretation_sha256: "sha256:9bda4fe1b5a372df271f003bb96c70ff9f87f383c807712d529794d5d7c4a5c4"
description: "这条内容报道了DeepSeek发布的最新开源模型v4.1‑Flash。该模型采用因果编码器‑解码器结构，并在输入与输出阶段使用不同的激活参数规模，同时加入视觉输入能力，专注于在保持性能的同时显著降低推理时的计算和缓存成本。"
external_url: https://www.latent.space/p/ainews-deepseek-v41-flash-763b-p8b
parent_observation_id: null
last_seen_at: 2026-09-12T09:21:01.038232Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://www.latent.space/p/ainews-deepseek-v41-flash-763b-p8b](https://www.latent.space/p/ainews-deepseek-v41-flash-763b-p8b)
- **发布域名**: www.latent.space

## 要点解读

### 这是什么
这条内容报道了DeepSeek发布的最新开源模型v4.1‑Flash。该模型采用因果编码器‑解码器结构，并在输入与输出阶段使用不同的激活参数规模，同时加入视觉输入能力，专注于在保持性能的同时显著降低推理时的计算和缓存成本。

### 用在哪里
适用于需要在长上下文或长时间运行的代理场景中进行高效推理的开发者，以及对成本敏感、期望利用开源模型进行生产的团队。

### 可以推断的
推测：由于输入与输出阶段的参数规模不同，模型在预填充阶段对显存的需求相对更低，适合部署在显存受限的环境。  
推测：该模型的低定价与宽松许可证可能会促使更多开源项目快速采用并集成，尤其在需要兼顾成本与性能的线上服务中。

## 来源摘要/节选

> We are late to this but better than never. Have been busy finalizing the second AIE NYC, which is happening in one month. Get your tix before prices go up - we will announce speakers from Bridgewater, Ramp, Coatue, Mastercard, Vanguard, Coinbase, Blackrock, Fidelity, Point72, Capital One, JPMC, Wells Fargo, Bloomberg, A24 (yes the movie studio) Labs, Two Sigma, Apollo Global, and more next week!
>
> The way DeepSeek pursues their research agenda is nothing short of fascinating. In between major DeepSeek versions, from v2 to v3 to v4, they have released intermediate papers with a hyperfocused architectural improvement and basically a 100% hit rate, from Math (esp GRPO), Coder, and R1, not to mention more recent work on Manifold Constrained Hyperconnections and Compressed Sparse Attention. After the enormous attention in 1H2025 from the R1 paper, DeepSeek started laying low, and for about the past year, was happy to let peers like GLM and Kimi take the lead on Open Models.
>
> It looked dicey for a little bit, but true whalebros never wavered, and now DeepSeek are sending a weirdly mixed message by doing a completely new architecture, retiring V4 Pro and going all in on this new model, and yet only titling it v4.1 Flash, it seems to be a test of whether or not you know how to read through the basic headlines to understand true advances.
>
> Yes, v4.1 Flash is technically behind other open models in some benchmarks. But that’s because we don’t yet have benchmarks that concisely capture what v4.1, and the broader research agenda of DeepSeek, is aiming for - the most creative and efficient use of context we have ever seen openly explained.
>
> If you are the sort to only read model versions and benchmark headlines, you are exactly the type of superficial person that DeepSeek is looking to fool. The best way to understand DeepSeek’s enormous advance here is to look at Sebastian’s meme:
>
> Same model name, but hardly a 0.1 bump by anyone’s standards, and they even threw in vision without making you wait for a separate model. For a better visualization you can look at all the model innovations stacked up over time from the OG encoder-decoder architecture from Attention is All You Need:
>
> If you read our V4 Pro writeup and Engram you should be up to date on the basic architectural reading for DeepSeek as of April 2026, but what we are HUGE fans of is the prefill/decode separation introduced here, 8B in prefill (input tokens), 16B in decode (output tokens), causing our alphabet soup of “DeepSeek v4.1-Flash: 763B-P8B-D16B” if you extend the established notation for MoEs. That’s a sparsity of 1-2%, and if you read the DeepSeek v4.1 Flash tech report, combined with new tweaks like Sliding-Window Attention Bounded Replay, makes for a KV cache footprint up to 1/8 that of V4 Flash… which make it much better/faster/cheaper for long running agents:
>
> We are so glad that DeepSeek is back publishing SOTA research. Our last highlight is their comments on post-training, where they largely seem to agree with Prof Jie Tang:
>
> AI News for 9/9/2026-9/10/2026. We checked 12 subreddits, 544 Twitters and no further Discords. AINews’ website lets you search all past issues. As a reminder, AINews is now a section of Latent Space. You can opt in/out of email frequencies!
>
> AI Twitter Recap
>
> DeepSeek launched V4.1-Flash as a new open-weight flagship focused on extreme inference efficiency and low cost.
>
> Independent benchmark account Artificial Analysis reported that DeepSeek V4.1 Flash surpasses DeepSeek V4 Pro 0813 despite being much cheaper, scoring 40 on the Artificial Analysis Intelligence Index, just below GLM-5.3-Flash and above the latest V4 Pro, while being priced at $0.30 / 1M input tokens and $1.20 / 1M output tokens with cached input at $0.006 / 1M and an additional 50% off-peak discount; they also describe it as a 763B total-parameter model with 8B active input and 16B active output parameters, 1M-token context, text+image input, MIT license, and US/API availability via DeepSeek first party @ArtificialAnlys, @ArtificialAnlys, @ArtificialAnlys
>
> Vals called it the new #1 open-weight model on the Vals Index, ahead of Kimi K3, at just $0.30 per test, the cheapest model in the open-weight top 10; they also note the eval ran with 1M context, 384 max output tokens, temperature 1, default top-p/top-k, and high reasoning effort @ValsAI, @ValsAI, @ValsAI
>
> Baseten shipped day-0 support and summarized the product positioning as smarter, faster, and more efficient than DeepSeek v4 Pro 0813, with text and vision, US-only, ZDR, and 1M context @baseten
>
> Ollama began rolling it out to Max and Team accounts, later expanding to Pro plan subscribers @ollama, @ollama, @ollama
>
> Architecture and paper-level technical details
>
> The most discussed technical novelty is a causal encoder-decoder design aimed at lowering active compute and KV/cache costs.
>
> Artificial Analysis says the model uses a new causal Encoder–Decoder architecture, with 8B active parameters for input/prefill and 16B active parameters for output/decode @ArtificialAnlys
>
> Sebastian Raschka characterized V4.1 as a “big overhaul” and said they “should have called it DeepSeek V5,” explicitly highlighting the encoder-decoder setup as the key break from prior DeepSeek generations @rasbt
>
> Multiple technical readers reacted to the design as unusually hybrid: one called it “a very interesting mix of very conservative and sometimes old ideas in research and potentially cutting edge efficiency and hardware design in engineering” @_xjdr
>
> A concise architecture read from Stochastic Chasm compared the design philosophy to HySparse, NSA, and DeepSeek’s own CSA/HCA from V4, summarizing it as a local sliding-window branch plus sparse retrieval branch, suggesting this sparse/local hybrid is becoming a broader pattern @stochasticchasm
>
> The same account noted multimodal changes were not radical, saying DeepSeek mostly “lets the backbone handle most of it and give it visual tokens,” with 3x3 pixel unshuffle instead of the more common 2x2 @stochasticchasm
>
> They later flagged a “big difference from K3 on vision encoders,” implying the vision front-end diverges materially from recent Chinese peers @stochasticchasm
>
> TeortaxesTex observed a recurring DeepSeek pattern of doing something unusual in the first N layers—previously dense or hash-routed, now SWA-only—speculating this may reflect repeated training difficulties in early layers @teortaxesTex
>
> Later, the same account argued the stack is “down to 40 layers, arguably only 20 legit decoder layers,” underscoring just how aggressively DeepSeek may be compressing effective depth in decode-critical paths @teortaxesTex
>
> Another thread fragment from TeortaxesTex suggested DeepSeek is doing multiple compression frequencies, “it’s just all CSA2,” in response to architectural discussion around memory compression @teortaxesTex
>
> Nrehiew’s technical notes emphasize KV cache compression as central to the design, calling it a case study in “how obsessing over KV Cache compression gets you a hyper-efficient frontier model” @nrehiew_
>
> In a follow-up, nrehiew highlighted infrastructure specifics from the report: dispatch strategy to reduce long-tail stalls, router replay from previous checkpoints, management of shorter-completion off-policy effects via dataset-level capping, discard schemes, bounded off-policy ratio and loss masking, and persistent KVs and routers when a new checkpoint is updated; they also mention a final stage with full-vocab OPD on 40+ teacher models @nrehiew_
>
> Nrehiew concluded that the design looks cleaner than the older HSA + CSA combination in V4, saying it was “very clearly designed for inference,” and cited a striking ~890 bytes/token KV size for the benchmarked score regime @nrehiew_
>
> Stochastic Chasm inferred QAT for the KV cache, saying this would explain why the model performs better than peers under FP4 KV cache @stochasticchasm
>
> Benchmark results and numbers
>
> Independent evals consistently paint V4.1-Flash as unusually strong on cost-adjusted intelligence, long context, and automation, with a major caveat around verbosity.
>
> Artificial Analysis’ headline: 40 AA Index, above V4 Pro and below GLM-5.3-Flash @ArtificialAnlys, corroborated separately by Scaling01 @scaling01
>
> Artificial Analysis reported AutomationBench-AA: 69%, tying GPT-6 Astra (69%) and above Grok 4.6 (67%), while improving 15 points over V4 Flash 0731 and sitting 12 points above V4 Pro 0813 (57%) and 7 points above GLM-5.3 (62%) @ArtificialAnlys
>
> On GDPval-AA v2 it reportedly gains 164 Elo, from 1468 to 1632, overtaking Kimi K3 at 1584 @ArtificialAnlys
>
> On AA-LCR v1.1 it scores 84%, on par with GPT-5.6 Sol and Gemini 3.8 Flash at 84% @ArtificialAnlys
>
> Artificial Analysis also says V4.1 Flash is among the most verbose models measured, averaging 89k tokens per Intelligence Index task—25% more than GLM-5.3 (71k), 29% more than GLM-5.3-Flash (69k), 62% more than V4 Pro 0813 (55k), and even above Fable 5.1 (78k) and Claude Opus 5 (73k) @ArtificialAnlys
>
> Even with that verbosity, AA estimates just $0.27 per Intelligence Index task, roughly 7x below GLM-5.3 ($2.01) and Kimi K3 ($2.00), and ~2.5x below V4 Pro 0813 ($0.67) @ArtificialAnlys
>
> Vals’ result reinforces cost leadership: $0.30/test, #1 open-weight on their board @ValsAI
>
> A separate reaction thread summarized DeepSWE-style claims more aggressively, saying V4.1 Flash offered better performance than GPT-5.6 Sol and Opus 5 in DeepSWE at 94% lower API costs, but that statement is secondhand summary rather than a primary benchmark post in this dataset @kimmonismus
>
> Running it locally and inference engineering reactions
>
> A large fraction of discussion centered on the surprising ease of running V4.1-Flash on commodity-ish local hardware through offload and SSD streaming.
>
> Fraser Price reported full-precision DeepSeek 4.1 Flash + DSpark at 200 TPS on 4 Max-Qs with just 64GB system RAM, offloading a 200GB Engram/hash table to NVMe; he says this made keeping the full structure in RAM unnecessary and promised a vLLM recipe @fraserpricee
>
> He later improved that to 300+ TPS on 4 RTX Pros, still at full precision, with &lt;32GB peak system RAM, using a custom vLLM fork and SSD support @fraserpricee
>
> Antirez showed DwarfStar running V4.1 Flash on a 128GB M5 Max, saying SSD streaming made it unexpectedly fast; he speculated both recent SSD-streaming changes and the possibility that DS4.1 “uses the same experts more” contributed @antirez
>
> TeortaxesTex reacted that it is “incredible you can run frontier models mostly off SSD” @teortaxesTex
>
> Elie Bakouch posted a reaction meme explicitly about the inference engineer view of the V4.1 Flash architecture, reflecting how strongly the launch resonated with systems folks @eliebakouch
>
> vLLM’s new release also included DeepSeek-V4 shared experts fused into MegaMoE, plus Mooncake Store can offload decode KV, relevant context for why serving this class of model is rapidly becoming easier in open infra @vllm_project, @vllm_project
>
> Facts vs. opinions
>
> Facts and directly attributed claims
>
> V4.1 Flash launched and was quickly supported by Ollama and Baseten @ollama, @baseten
>
> Independent benchmarks reported AA Index 40, AutomationBench-AA 69%, AA-LCR 84%, GDPval-AA v2 1632 Elo, 1M context, MIT license, and low API pricing @ArtificialAnlys
>
> Vals reported #1 among open-weight models on its index, at $0.30/test, with 384 max output tokens under its harness settings @ValsAI, @ValsAI
>
> Local deployment reports claimed 200 TPS and later 300+ TPS on 4-GPU setups, plus successful M5 Max SSD-streamed operation @fraserpricee, @fraserpricee, @antirez
>
> Interpretations and opinions
>
> Raschka’s “they should have called it V5” is an opinion about how substantial the architectural change is @rasbt
>
> TeortaxesTex’s speculation that DeepSeek “repeatedly struggled to train first layers properly” is inference, not a confirmed statement from DeepSeek @teortaxesTex
>
> Nrehiew’s framing that the report is “cleaner” than the prior HSA/CSA design and likely unlike what OpenAI/Anthropic would do because of their custom chips is informed opinion @nrehiew_
>
> The “DeepSeek ships internal research artifacts and not products” critique is an external judgment, not a factual release note @teortaxesTex
>
> Assertions that “data is all that matters” or “research is over” were themselves criticized as overreactions @shikibmehri
>
> Different opinions and reactions
>
> Supportive / impressed
>
> Strong positive reactions came from benchmarkers and researchers emphasizing the price/perf step: Vals’ “new #1 open-weight model,” Artificial Analysis’ cost-adjusted headline, and general praise like “interesting release / breath of fresh air vibe” @ValsAI, @ArtificialAnlys, @dejavucoder
>
> Raschka called it “super cool and refreshing” @rasbt
>
> XJDR liked the engineering thinking despite some aesthetic reservations @_xjdr
>
> Nrehiew called it “yet another banger tech report” @nrehiew_
>
> Stochastic Chasm ended by saying the paper was “dense” but appreciated the multi-agent training angle and sparse design ideas @stochasticchasm, @stochasticchasm
>
> Neutral / analytical
>
> Some observers mainly dissected the design rather than cheering it: sparse/local hybridization, first-layer oddities, multimodal tokenization, KV quantization, colocated async RL, etc. @stochasticchasm, @stochasticchasm, @nrehiew_
>
> Gordic Aleksa used the paper as evidence in a broader pretraining-data taxonomy, placing DeepSeek in the organic data camp and noting surprise that, based on publications, they do not appear to use even synthetic rephrasing @gordic_aleksa
>
> Critical / skeptical
>
> TeortaxesTex repeatedly pushed back on external impressions, arguing DeepSeek often shows high internal evals, weaker external robustness, brittleness, and weird skill gaps, because it “ships internal research artifacts and not products” @teortaxesTex
>
> The same account called some eval results “very strange,” particularly AutomationBench #1 and a CritPt regression, and asked the DeepSeek team to “meditate on this” @teortaxesTex
>
> They also argued that V4 GA had benefited massively from tool/skills harness access, whereas V4.1 appears less dependent on harness scaffolding and better in “minimal harnesses” @teortaxesTex
>
> In hands-on use, they reported that multi-agent “DSH agent teams” could degrade quality unless the project has very clear modularity, with V4.1 solo outperforming team mode in at least one example because subagents produced slop or wasted tokens on unnecessary research @teortaxesTex, @teortaxesTex
>
> Jared Z’s broader product-market critique—that users now care deeply about token cost, and daily-driver coding models should be both cheap and smart—fits V4.1 Flash’s positioning even though it wasn’t about the model specifically @imjaredz
>
> Context
>
> Why this matters technically and strategically
>
> The launch lands amid a broader shift from “bigger dense chat models” toward systems-optimized, sparse, long-context, agent-oriented models that can actually be served cheaply and locally.
>
> V4.1 Flash’s positioning is unusually aggressive: open-weight, MIT-licensed, 1M context, multimodal input, low active parameter counts, extreme cache discounts, and demonstrated viability on SSD/offload-heavy consumerish setups @ArtificialAnlys, @fraserpricee, @antirez
>
> The benchmark pattern suggests a meaningful trade: very high verbosity but still exceptionally low total task cost thanks to ultra-cheap token pricing @ArtificialAnlys
>
> The architecture also reflects a broader industry trend toward splitting prefill and decode economics, making long-context and agentic workloads more practical without paying frontier dense-model costs on every token.
>
> The release reinforces the idea that open models are increasingly competitive not just on raw weights availability, but on servability—the ability to fit into offload pipelines, quantized KV stacks, local deployment, and open inference servers.
>
> It also sharpened debate over what matters most in 2026 model progress: architecture, RL/inference co-design, data quality, or systems work. Shikib Mehri explicitly pushed back on the claim that DeepSeek’s paper means “research is over,” arguing instead that the lever surface has expanded from architecture into data-factory and reward-design research @shikibmehri
>
> Finally, DeepSeek remains a polarizing lab identity-wise: admired for shipping unusual research artifacts and detailed reports, but also seen by some practitioners as less polished than product-centric competitors, with odd eval gaps and brittle behaviors that appear more clearly in real workflows than in internal headline numbers @teortaxesTex, @teortaxesTex
>
> OpenAI’s Voice, Agents, and Enterprise Push
>
> OpenAI launched GPT-Live-1 into the API and quickly seeded an ecosystem around it: the new model is positioned as a full-duplex voice interface that can listen while speaking and delegate tool use or reasoning to a backend model. The core launch came from @OpenAIDevs, with additional detail that developers can control tone, pacing, expressiveness, response length, and language here. OpenAI’s own benchmark post claimed improvements over GPT-Realtime-2.1, including 83.6% first-attempt task completion on Tau3 when paired with GPT-6 Astra, 97.3% on Artificial Analysis Conversational Dynamics, and 0.798s response onset latency on Full Duplex Bench v1 details.
>
> The surrounding toolchain is maturing toward hosted agent infra: OpenAI also announced a public-beta Agents API with the Codex harness, plus OpenAI-hosted sandboxes for code execution, files, and artifacts via managed cloud agents launch. This aligns with a broader industry move to collapse model, runtime, and sandbox into one surface. Integration announcements from LiveKit, HeyGen, Telnyx, Speak, and Cognition’s Devin Voice suggest GPT-Live-1 may become a default substrate for production voice agents faster than the earlier realtime stack did.
>
> Enterprise data access is becoming a first-class product primitive: OpenAI’s product-side announcement of a Data agent in ChatGPT Work promises dashboards, answers, and actions over connected company data sources @ChatGPT, while Box framed its integration as “the file system for AI” bringing governed enterprise context into ChatGPT. Combined with Google’s docs-for-agents push and Cursor’s new persistent workspaces, the trend is toward stateful, organization-aware agent environments, not stateless model endpoints.
>
> Cognition, Cursor, and the Shift Toward Persistent Coding Agents
>
> Cognition had a notably strong day: it released SWE-2, described as “our closest model yet to the frontier,” claiming parity on leading coding evals at up to 70% lower cost and explicitly stating it scaled RL to multiple trillions of parameters launch. Additional context from ybenpan emphasized that the team built algorithm, infra, and data in-house, while silasalberti highlighted a practical RL finding: a simple linear length penalty preserved a training-time Pareto curve shape across effort levels.
>
> The Devin stack is becoming more multimodal and more integrated with developer workflows: beyond SWE-2, Cognition launched Devin Voice powered by GPT-Live and SWE-2 tweet, and announced that Dioxus Labs is joining Cognition to contribute to Devin’s VM, computer use, and testing while continuing support for Dioxus and related Rust OSS Cognition. This is a concrete example of coding-agent vendors acquiring infra and systems talent, not just model researchers.
>
> Cursor’s new “Projects” feature points to the same destination from the IDE side: Cursor introduced persistent threads with a coordinator agent, shared memory/artifacts across agents, and sync across user devices and agent computers. In practical terms, this is a move away from “one chat per task” toward a long-lived software project substrate where subagents accumulate state over time. Read together with Claude Code’s new pane pop-outs and managed-agent session viewer / auto mode, the market is converging on the idea that coding agents need persistent context, inspectable sessions, and explicit orchestration controls, not just better completions.
>
> Agent Research: Harnesses, Horizons, Parallel Retrieval, and Self-Evolution
>
> Several papers pushed on a common theme: the harness is now a core optimization target. A widely shared Salesforce paper summary from omarsar0 showed that training a weaker model on a stronger expert’s full trajectories can hurt performance by 4–30 points after harness evolution, because the fine-tuned model adopts an incompatible planning style. The proposed fix—rewrite only the failing turn in the weaker model’s own rollout—preserves model-harness fit. In parallel, Sumanth_077’s writeup of ByteDance’s HarnessDev described agents that build and iteratively improve their own runnable harnesses, with mixed generalization: only 34/64 changes transferred directionally to held-out tasks.
>
> Long-horizon and long-context agent training also got more principled treatments: dair_ai summarized Qwen work on Elastic Horizon, a closed-loop controller that tracks the 90th percentile of successful trajectory lengths to adjust the maximum interaction horizon, improving success while saving up to 25% of trajectory tokens. Separately, omarsar0 highlighted PARSER, which replaces sequential chunk reading with parallel frozen subagents + an RL-trained lead agent over iterative scatter-gather rounds; reported gains include +12 points at 896K context and up to 11x lower latency.
>
> Skill and tool-use data generation are being formalized too: dair_ai on SkillAdam framed skill self-evolution as a discrete optimization problem, borrowing Adam-like first/second-moment ideas to stabilize update direction and edit magnitude. Meanwhile, Google Research’s ToolGrad generates ground-truth tool-use chains before prompts, reporting near-100% pass rate for dataset creation and downstream tool-use gains. Taken together, this batch of work suggests the field is shifting from “prompt the model harder” toward closed-loop optimization of scaffolds, trajectory budgets, skill documents, and tool traces.
>
> Safety, Misuse, Monitorability, and Model Governance
>
> Anthropic’s threat intelligence report dominated the safety discussion: the company published its most detailed misuse report so far, covering attempts to use Claude for cyberattacks, influence ops, surveillance, biology, and weapons, and said it disrupted every operation described launch tweet. Much of the discourse focused on reported extraction / routing patterns involving rival labs and state-linked misuse, with high-engagement reactions from pradeepXkapoor, logangraham, and former Meta threat-disruption lead David Agranovich, who argued Anthropic deserves credit for this level of transparency even if some framing should be debated.
>
> A second thread focused on reasoning monitorability and “neuralese” risk: Redwood Research proposed transparency norms for architectures that may weaken or eliminate chain-of-thought visibility, and Ryan Greenblatt argued companies should publish evidence and policies before deploying architectures that substantially reduce CoT dependence. Related commentary from Neel Nanda interpreted GPT-6 Astra as a potentially concerning jump in no-CoT reasoning, possibly indicating architectural changes beyond ordinary scaling.
>
> There was also visible disagreement among frontier-lab employees and alumni about risk culture: Chris Hayduk emphasized AI’s humanitarian upside, while balesni and jkcarlsmith openly endorsed &gt;10% extinction-risk views. On governance, Thom Wolf announced a new Open Alignment team at Hugging Face, and Richard Ngo published a sharp critique of Paul joining OpenAI’s board and of what he sees as the safety community’s capture by AGI companies.
>
> Top tweets by engagement
>
> Anthropic threat intelligence report: @AnthropicAI published a detailed account of sophisticated Claude misuse across cyber, influence, biology, surveillance, and weapons.
>
> OpenAI pauses new $200 Pro signups for Astra capacity reasons: @thsottiaux said existing users are unaffected and API/other plans remain available.
>
> GPT-Live-1 API launch: @OpenAIDevs launched the new full-duplex voice model into the API.
>
> ChatGPT Work Data agent: @ChatGPT announced a data-connected enterprise agent for dashboards, answers, and

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。