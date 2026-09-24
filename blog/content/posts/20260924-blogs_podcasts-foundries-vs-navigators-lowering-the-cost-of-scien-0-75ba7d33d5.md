---
title: "Foundries vs Navigators: Lowering the Cost of Science"
date: 2026-09-24T23:09:16+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:56841a87c2090f6b6f0f5325f0720d9ecceea835a1627f2cd992e7fc3f6277be"
source_payload_sha256: "sha256:638125854ced628b0bda86a6073e9812beab0ccefc5f785f968bcad322eee0e2"
observation_id: obs_75ba7d33d52171ac1f5b157285ea4865e9e6c6176d77009b695ea5b75414e3ae
event_id: evt_e2ffec7f6044f4cd87404e25c11838e4badb9ed0c33aa6a8ea258275aafc04be
revision_id: rev_3f776711e1c8caf6b8bb81e9660c8ce1d5823ef24217288acc18e46e59c6c649
source_published_at: 2026-09-24T15:03:16Z
first_seen_at: 2026-09-24T15:20:18Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 53
description: "当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。"
external_url: https://www.latent.space/p/foundries-vs-navigators-lowering
parent_observation_id: null
last_seen_at: 2026-09-24T15:05:39.077099Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://www.latent.space/p/foundries-vs-navigators-lowering](https://www.latent.space/p/foundries-vs-navigators-lowering)
- **发布域名**: www.latent.space

## 来源摘要/节选

> What does the future of science look like in the world of AI? Anthropic has some lofty goals for science and is even opening a wet lab. Meanwhile a quiet transformation1 is happening all across AI x Science.
>
> In this guest post, Adrian Sanborn talks about the less flashy but more immediate ways he sees AI transforming front-line scientific research in his own company, Endura Therapeutics.
>
> Adrian did a CS PhD at Stanford and spent much of it running experiments at the bench, which makes him one of the rare people who can tell you what an LLM is doing to a codebase and to a wet lab. Enjoy!
>
> Language models have transformed how software gets built. Writing code, wrangling data, and architecting systems now move at a speed unthinkable three years ago.
>
> When the product is software and the result is verifiable, cheaper coding turns directly into more software and more builders.2 But in science, everything is ultimately gated by physical experiments that take days or weeks to verify anything. Knowledge work around the experiment has become dramatically faster while AI has done little for the throughput of the experiment itself. Thinking got cheap and doing did not.
>
> We think the biotech industry has adapted in two ways:
>
> Foundries shrink the cost of doing. They industrialize the measurement, using new technology to generate data an order of magnitude faster than before. Xaira, NewLimit, Octant, Tahoe, and Endura accomplish this with next-generation sequencing and multiplexing; Insitro, Eikon, and Noetik with high-throughput microscopy; Lila and Periodic Labs with physical automation, just to name a few. AI makes that data legible and predictive, but the differentiating asset is the experimental data itself.
>
> Navigators spend the surplus of thinking. The AI models sit in the ordinary machinery of the company, driving better decisions and faster processes. They increasingly govern how the work is conducted, what tools get built, and which questions are worth an experiment. A proprietary model or a massive dataset are not required, only a willingness to evolve how the company works.
>
> Building a foundry is a genuine strategic commitment that takes capital, years, and a bet on a particular technology. Foundries are easy to see: the technology captures the imagination, the connection to AI is immediate, and there is always some new model or dataset to announce. Navigators are invisible by comparison because the gains are operational and nobody issues a press release about a path they decided against. But navigation is available to every company. The prominent change is happening at a few dozen companies, while the inconspicuous one is happening at all of them.
>
> Navigation runs fastest at early-stage startups, which have no legacy to shed: no history of software contracts, standardized processes, calcified org structure, or compliance regime. They are also under pressure to move fast with very little. When a better way to work appears, it simply becomes the new normal.
>
> The impact shows up everywhere. Experiments iterate faster when analysis takes an hour instead of a week. A category of software that would have been licensed for six figures becomes a one-day build. Disease programs get chosen from 500 candidates where a team could ordinarily evaluate five. Here’s what it looks like from the inside.
>
> Code now keeps pace with the science
>
> There is a structural tension in experimental science that software engineering has no real equivalent for. In engineering, requirements that change every few weeks are a symptom of poor planning. In research, they are the objective. The purpose of an experiment is to learn something, and that learning changes what the next experiment should be.3 If an approach has not evolved in six months, it means nothing is being discovered.
>
> A new experiment’s protocol will evolve a dozen times in the first year, and every one of those changes propagates into the analysis. Each measurement has to be processed, normalized, and interpreted with code that tracks the experiment closely. Historically this analysis was done by a second person, creating a seam between the person who understands what the experiment is measuring and the person who understands what the code is doing. From this friction arises the tendency to propose fewer experimental changes to avoid analysis rework, which compounds into options left unexplored.
>
> Now that writing code is fast, adapting the analysis to a modified protocol is an afternoon’s work rather than a project. The experiment is no longer constrained by the burden of changing the analysis pipeline. Experiments can be agile when flexibility is cheap and problems can be easily fixed; in other words, science gets to “move fast and break things.”
>
> The same shift also applies one layer up, to interpretation. An interactive visualization dashboard can now be built in minutes, down from days.
>
> An internal dashboard at Endura Therapeutics, built in a few hours.
>
> The most visible consequence is access. Previously, when every experiment was analyzed by the computational person, results waited in a queue. Now the scientist who ran the experiment and has the context presents their own results. The data is no longer gatekept behind someone else’s Python notebooks.
>
> Software can now express your opinion
>
> Every software interface has an opinion. A data system decides which comparisons are one click away and which require hunting. Every lab needs somewhere to store and display its data, and the opinion embedded in that system ends up shaping what that lab notices.
>
> For two decades that opinion was formed by someone else: a handful of vendors who build lab software that acts as the system of record. These vendors build one system for a thousand labs and necessarily design toward the lowest common denominator. Everyone accepted the approximation, because developing your own was more work than any lab could justify.
>
> This is no longer true. A data portal built in-house accommodates the quirks of the data that no commercial product would have anticipated, and is exactly as complex as the team needs, growing as their questions do. Browsing and exploring become simple and effortless, which changes behavior. Consider how little time anyone would spend on social media if seeing the next post required switching tabs and copy-pasting. Patterns that have been sitting in separate slide decks start to surface.
>
> Implementation takes just one day, but deciding what the portal should do can take weeks. Those design discussions turn out to be critical, because deciding what belongs on a single screen forces a team to articulate which comparisons actually drive its decisions. When you buy a software platform you outsource not only the engineering but the question of how you accomplish your goals.
>
> There are tradeoffs: an in-house portal is less polished and there is no support team to call. Larger organizations, with layers of validation requirements and contractual obligations, will still struggle to follow in these footsteps. But software companies have long understood that the best internal tools come from engineers embedded alongside the people who use them. Now every research team can be its own forward-deployed engineer.
>
> The old rule was “never build what you can buy”. The new rule is build the tools that shape how you think.
>
> Expert-level depth now scales
>
> Choosing which diseases to pursue is the most consequential decision a drug company makes. Everything is downstream of this decision and built to accommodate the specifics of the disease biology and its market. The choice is effectively irreversible, with a single successful program requiring about a decade and a billion dollars, so the decision gets diligenced carefully. A typical process convenes a group of internal and outside experts who gather, synthesize, and debate the scientific and market evidence for a month or more.
>
> That process assumes you already know which five diseases you’re arguing about. We didn’t have this shortlist at my company, Endura, because of the unique mechanism of our medicines. We’re developing CRISPR in a pill: a drug, taken in the convenience of your home, that forms a chemical scar on one specific genetic message and shuts off production of a disease-causing protein.4 Finding these drugs required developing a new DNA sequencing method that reads those scars across every gene at once, so a single experiment returns candidate drugs across hundreds of diseases. Instead of starting from five diseases, we had to triage the entire map of disease.5
>
> We built a two-stage triage and pointed a fleet of LLM research agents at it. The first pass covered about 500 disease targets, generating the equivalent of a three-page report on each and filtering on foundational questions: is the disease prevalent enough to justify our efforts, is the problem already addressed by existing drugs, and would the target-lowering effect of our drug actually relieve the disease. The second pass, on the roughly 100 remaining disease targets, produced the equivalent of thirty pages each, working through disease biology and the competitive landscape thoroughly. We wrote the second-pass prompts to behave like a skeptical expert rather than a summarizer: name the programs that failed, why each failed, and what would have to be true for us to succeed where they didn’t. This level of detail is necessary because, as in any market, the clearly good targets are crowded. Arriving at a defensible position means finding the specific disease and the specific reason our drug will do something that existing approaches cannot.
>
> At the old rate, the first stage would have required about one person-year of reading, and the second closer to a century of expert time. The second pass still gets checked against primary sources and selected programs receive the full human diligence it always would have.6 But a search this broad, at this depth, simply was not possible a year ago.
>
> In research, the expensive mistakes are the unknown ones. A team commits to a direction and finds out it was wrong months later when the experiment comes back negative. Often a specialist could have said so in a sentence: that pathway has been tried, this readout has never predicted anything, that company faltered on that patient population. Access to this kind of expert-level depth at scale is a game changer exactly because being told “no” early is so valuable in research.
>
> This is the shallow end
>
> Everything above happened at Endura — flexible and dynamic analysis, internal tools built in a day, a search across 500 diseases — and it is just the beginner version of navigation. Each subsequent generation of language models removes constraints we had taken for granted. Soon we could entirely skip building an analysis pipeline or data dashboard. Instead, a scientist will ask the question she actually has and the analysis and interface to answer it will be assembled from scratch. Software stops being a work product and becomes something that appears around the question.7
>
> Access to expertise at this scale opens work nobody could attempt before. One clear example is drug repurposing, where a drug already proven safe in humans turns out to act on a disease mechanism nobody was looking at. The published literature is enormous, and some number of useful conclusions are sitting in it right now, unfound because no single person has read the right combination of papers. But a model can digest it all and, with the right prompting, connect the dots. A whole ecosystem of companies is now forming around that bet, and pharma and investors are running their own versions.8 What remains to be seen is whether this produces three new drugs or 300.
>
> The navigators are testimony that the most accelerating AI in science right now is not a model trained on scientific data at all. It is the one that helps a scientist or executive figure out what is worth doing every Monday morning.
>
> Adrian Sanborn is CEO and co-founder of Endura Therapeutics. He was a founding member of Atomic AI, where he led the biology side of the technology platform and defined the company’s therapeutic strategy. He holds a PhD in computer science from Stanford, most of which he spent at the bench in Roger Kornberg’s biochemistry lab. He is @AdrianSanborn on X.
>
> Many thanks to Brandon Anderson, swyx, and Lauren Richardson for reviewing drafts of this post and providing critical feedback.
>
> 1
>
> While this blog was being polished, this paper came out that talks about early insights in AI x Science. We were excited to see many of our insights were observed empirically!
>
> 2
>
> This is the Jevons paradox, named for the 1865 observation that more efficient steam engines increased coal consumption rather than reducing it. The software version: every drop in the cost of writing code has so far been followed by more software rather than fewer engineers.
>
> 3
>
> Software product development actually also has workflows that emphasize learning and borrow the word “experiment.” Product teams run A/B tests, ship behind feature flags, and treat a release as a hypothesis about what users want.
>
> 4
>
> Most genetic medicines like CRISPR are large molecules that cannot get into cells on their own. They reach only a few tissues, and getting them there means an infusion, an injection, or, for the brain, a needle into the spinal canal. Small molecule drugs in a pill format travel through the body on their own and can be swallowed. When Roche launched an oral drug for spinal muscular atrophy, families steadily switched to it from an injected medicine that already worked.
>
> 5
>
> Most companies have good reasons to set a therapeutic area first, dictated by their pre-existing scientific expertise, clinical relationships, and business priorities. Our approach allow us to start broad to find the most productive direction and then build that depth afterwards.
>
> 6
>
> Language models are not perfect, and at this scale some reports contained errors. This is tolerable because a mistake in the first pass only means a missed opportunity, not time lost chasing a bad idea.
>
> 7
>
> Analysis generated on demand has an unresolved problem: reproducibility. If the code behind a figure was assembled for one question, its provenance is weaker than a versioned pipeline’s.
>
> 8
>
> For example, Edison Scientific is built close to this premise, and the team behind Metsera engaged its AI Scientist system to generate new company ideas.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。