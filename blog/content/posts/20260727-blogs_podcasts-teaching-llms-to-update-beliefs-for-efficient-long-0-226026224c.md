---
title: "Teaching LLMs to Update Beliefs for Efficient Long-Horizon Interaction"
date: 2026-07-27T12:06:37+08:00
draft: false
entry_kind: "auto"
tags: ["博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:b1c6d3994420b0b55078fe5bebda3cb6036bf39dbdae55fd17fdb6500bbf05b9"
source_payload_sha256: "sha256:5d544fdbdfbd61b8b5190adead4a53acc4abe330b62bb3e4b9507292b827468d"
observation_id: obs_226026224cdbefcaaac8ea11183251aad8dc24cd3dc4a090ac8aebcfcd8c4f37
event_id: evt_b04a57357952b2ae8467fd1ad3f86c92761bf4f28ddbaaec90d86b074198ed26
revision_id: rev_17c9ff602b369c515c0d0430eedd8cc7781118904fb417470a325510767715bf
source_published_at: 2026-07-26T09:00:00Z
first_seen_at: 2026-07-27T04:05:51.126522Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 70
description: "当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。"
external_url: http://bair.berkeley.edu/blog/2026/07/26/abbel
parent_observation_id: null
last_seen_at: 2026-07-27T04:05:51.126522Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [http://bair.berkeley.edu/blog/2026/07/26/abbel](http://bair.berkeley.edu/blog/2026/07/26/abbel)

## 来源摘要/节选

> Overview of ABBEL compared to traditional recursive summarization. Beliefs replace the full interaction history as the agent’s working context, and belief grading improves performance by
>
> supervising the contents of each belief state..
>
> As task horizons grow, LLM contexts can’t scale forever. Self-summarization enables concise, interpretable contexts, but at a significant performance cost, especially for human assistance domains where high quality data is scarce, e.g., collaborative code generation. We address this with ABBEL: a framework that isolates and supervises the information content of summaries in the form of natural-language belief states.
>
> Motivation: the cost of recursive summarization
>
> For language models to effectively assist with increasingly complex tasks such as software development, they must be able to interact with us over hundreds or even thousands of steps. For such long tasks, it is impractical to keep the history of the entire interaction in context. The heuristic approach used so far has been summary generation, sometimes called context compaction. For example, Cursor’s latest model composer 2.5 uses compaction during training for improved performance (Cassano et al., 2026). Alongside composer, Grandcode (DeepReinforce et al., 2026), the first system to consistently beat all human competitors in online coding competitions, despite using one of the newest efficient attention models (Qwen 3.5-397B),1 still found it necessary to employ context summarization.
>
> But compaction has a problem. Despite seemingly low performance gaps in benchmarks, model servers like Cursor continue to recommend that users avoid compaction with their coding assistants in the middle of a task (Heule et al., 2026).
>
> To understand why, see below the performance over RL fine-tuning of a Context summary model compared to full context models in Combination Lock, a Wordle-like game that allows up to 16 guesses.2 Though both model types improve over the course of training, the summary model never closes the gap.
>
> Fig. 1: Average attempts to guess the target word on Combination Lock over RL fine-tuning (lower is better). Context-summary policies improve with training but do not close the gap to full-context policies.
>
> Making models self-summarize while completing a task increases the complexity of the learning problem. While this could typically be addressed by training with more data, the performance degradation observed in real world interactive settings likely arises from the difficulty we have in creating and using human simulators effectively to generate high quality training environments (Lin et al., 2025, Tomlin et al., 2025). Thus, the better you can learn to summarize on the limited and messy multiturn interaction trajectories you can collect, the better off your model will be for downstream users.
>
> ABBEL: acting through belief bottlenecks
>
> Fig. 2: Autoencoder-inspired belief grading. The model encodes prior belief, action and observation (bt, at, ot) into posterior belief bt+1 and is rewarded for how well select information from the history can be reconstructed from that belief.
>
> To address poor learning efficiency, we isolate the summary generation task. Drawing inspiration from recursive Bayesian estimation, we formulate summaries as belief states, which we periodically prompt the model to update based on new information.3
>
> ‹ Prev
>
> Pause
>
> Next ›
>
> 1 / 16
>
> Fig. 3: ABBEL rollout. Belief updates from the latest observation alternate with action selection conditioned only on the current posterior belief.
>
> Belief grading
>
> We then extract and supervise the contents of the belief states (Fig. 2, Belief Grading). Belief grading can be thought of as adding an auxiliary RL task, using heuristics designed to capture what makes a good belief as the reward. An example heuristic for coding could be shorter is better, but closer to being able to reconstruct the git diff is also better, so balancing these would yield a good belief. In domains where good heuristics are hard to define, we propose a general autoencoding-inspired grading function, which treats the current language model πθ as both encoder and decoder of information from
>
> the history, and the belief states as the codes. We grade each belief bt+1 by how well it can be used by the current model πθ to reconstruct the most recent observation ot:
>
> Eq. 1: Reconstruction grading objective. Here bt+1 is the updated belief, ot the latest observation, at the action just taken, bt the prior belief, pI the task prompt, and πθ the current model. Higher grades reward beliefs that retain information needed to decode the latest observation.
>
> What do we gain by grading beliefs?
>
> Collaborative coding on CollabBench
>
> We demonstrate the utility of belief grading in our motivating domain of human-driven assistive coding, with the CollabBench environment from Sweet-RL (Zhou et al., 2025).
>
> Fig. 4: CollabBench collaborative coding environment. The agent asks clarifying questions, then submits a function scored against hidden unit tests.
>
> We see that with the general reconstruction-based belief grading function we reduce the performance gap from full context models by about 50%, and train in 50% fewer steps compared to training models to summarize without belief grading (no BG). After training, ABBEL still uses significantly less memory than the full context setting, as measured by the peak context token length (Peak Tokens).
>
> Model
>
> Test Pass Rate ↑
>
> Success Rate ↑
>
> Peak Tokens × 10² ↓
>
> Training Steps ↓
>
> Full Context
>
> 0.52±0.02
>
> 0.39±0.02
>
> 14.08±0.55
>
> 100
>
> ABBEL (no BG)
>
> 0.46±0.02
>
> 0.31±0.02
>
> 4.20±0.37
>
> 100
>
> ABBEL-rec-BG
>
> 0.48±0.01
>
> 0.36±0.01
>
> 6.01±0.33
>
> 50
>
> Fig. 5: CollabBench results. With reconstruction belief grading, ABBEL-rec-BG recovers about half the gap to full context while using fewer peak tokens, and trains in 50 steps instead of 100.
>
> Combination Lock
>
> Additionally, in CombinationLock, we demonstrate that ABBEL with a belief grader which leverages domain knowledge (by computing useful statistics over the history and checking that they can be reconstructed from the belief state), enables even higher learning efficiency than full context (FULL CTX) models.
>
> Fig. 6: Average attempts to guess the target word on Combination Lock (lower is better). With domain-knowledge belief grading, ABBEL approaches or exceeds FULL CTX in this setting; without belief grading, learning is slower.
>
> Multi-objective question answering
>
> In a third environment, multi-objective question answering (from MEM1 Zhang et al., 2025, a recent work which performed end-to-end optimization in a modified version of typical recursive summarization), we demonstrate the utility of isolating belief states from reasoning, by showing that a Peak Belief length Penalty (more details in paper) significantly reduces memory usage with minimal performance degradation, unlike is commonly observed when penalizing reasoning lengths (Arora et al., 2025).
>
> Fig. 7: Exact-match score and peak memory versus number of objectives in multi-objective QA. ABBEL with a peak belief penalty (PBP) maintains comparable performance while using less memory than MEM1 and ABBEL without PBP in this evaluation.
>
> Related work
>
> Alternative solutions to managing long contexts involve different tradeoffs, and are worth considering depending on the requirements of a deployed system. Context compression methods generate dense representations which, while computationally efficient, sacrifice human-understandability (Kontonis et al., 2026, Eyuboglu et al., 2025, Gupta et al., 2025, Chevalier et al., 2023, Deng et al., 2025, Deng et al., 2025, Bulatov et al., 2022). Hand-designed summarization prompts (Wang et al., 2025, Örwall et al., 2025, Starace et al., 2025) and pruning strategies (Jiang et al., 2024) specific to target environments require expert human knowledge and don’t allow an agent to learn what to remember as part of its decision-making strategy. Methods that process long contexts into an external memory store (Packer et al., 2023, Xu et al., 2025) for the agents or subagents to query (Zhang et al., 2025) are complementary, as they may benefit from better next context creation through summarization training. We would like to point out some exciting works in the space of general recursive summarization focused on math (Wu et al., 2026), reasoning with belief generation (Zhou et al., 2025), competitive coding with a distilled summarization module using similar autoencoding objectives to our general belief grader (DeepReinforce et al., 2026), and adding continuous features to summaries (Kontonis et al., 2026).
>
> What’s next for better memory?
>
> Many more possibilities are enabled through using explicit belief states as information bottlenecks for multi-step interaction. You could reward actions based on their effect on the belief state to guide exploration, transmit the explicit belief states for better communication between agents, or even improve user controllability by directly modifying the memories on which the agents’ decisions are based.
>
> Some forms of information, e.g., what a person looks like, are not represented well by text alone. A continuously learning system will also have to capture such information. Additionally, if we want a system to learn to communicate in a brand new language or to play a brand new game better than any person in the world, the skills accumulated over the lifetime of conversations or games must be stored in a very compressed form, essentially taking on the role of the weights of the model itself.
>
> More powerful systems will likely utilize a combination of multiple forms of memory, where the contents of the context may correspond to working memory while other approaches are used for short and long-term memory. How to instantiate these other forms of memory, for instance via test-time training, adapter memories, continuous context memories, or some combination thereof, presents an exciting challenge.
>
> Acknowledgements
>
> Acknowledgements: We would like to thank Alane Suhr and Kartik Goyal for advising this research as well as Ethan Mendes, David He, Jitesh Jain, and Nicholas Tomlin for comments on early drafts of this post. We would like to thank the MEM1 authors for their email correspondence and for sharing private reviewer feedback which we found particularly insightful.
>
> Citation
>
> If abbel was inspiring for your future work, please cite us with this! And here is some advice for doing similar research!
>
> @misc{lidayan2026abbellearningnaturallanguagebelief,
>
> title={ABBEL: Learning Natural-Language Belief States for Memory-Efficient Interaction},
>
> author={Aly Lidayan and Jakob Bjorner and Satvik Golechha and Kartik Goyal and Alane Suhr},
>
> year={2026},
>
> eprint={2512.20111},
>
> archivePrefix={arXiv},
>
> primaryClass={cs.CL},
>
> url={https://arxiv.org/abs/2512.20111},
>
> }
>
> With newer models the number of tokens till 50% compute spend is on attention gets much larger than 25K. Interleaving linear attention alternatives with full attention as is done with gpt-oss and DeepSeekv4, results in massive flops reductions for the attention computation. For example with DeepSeekv4-Pro (1.6T A49B) it requires nearly 450 thousand tokens to reach the 50% tradeoff point. Grandcode uses Qwen-3.5-397B-A17B a model which hits 50% FLOPs for attention at ~150 thousand tokens.
>
> ↩
>
> This setting is technically solvable with much more computationally effective tools, but serves as a flexible test bed to study properties of recursive summarization. Bertsimas et al., 2022, showed that an exact solution for the wordle game instantiated with the original vocabulary of the javascript game can be found with dynamic programming, but evidently the general formulation of wordle as a guessing game on K letters with L attempts and some dictionary of valid words and correct words D is NP hard to determine the minimal number of moves required.
>
> ↩
>
> In practice there is an O(N/K) overhead cost for summary. N is the total number of actions. K is the number of actions till summarization is triggered. This is necessarily true for any summary approach. For ease of illustration this gif uses K = 1. In our experiments, to put more emphasis on summarization weaknesses we also use K=1. In practice overhead is small as K can be chosen to be near the efficient hardware limit.
>
> ↩

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。