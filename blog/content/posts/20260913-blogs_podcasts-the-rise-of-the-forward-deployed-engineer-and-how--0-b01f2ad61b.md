---
title: "The Rise of the Forward Deployed Engineer — and How To Do the Job Right"
date: 2026-09-13T01:11:37+08:00
draft: false
entry_kind: "auto"
tags: ["AI", "博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:544481b4cc08cb99ff3856161f6332a71808b0c7fc8e006c1087e434b90d2401"
source_payload_sha256: "sha256:5402f4e5929bf05864300740e98835e8d185cd89df043ecb529ad5602d19f9fc"
observation_id: obs_b01f2ad61bd017c9f37a1a617c68ae6c479c68ebbe2216a4d51ffc2367073745
event_id: evt_ef20289b1c52e0316c8e1626d4e6be557f8435e9feb2138f56912d31b49c2cea
revision_id: rev_880103f48a113389e1f20f0374e64e843a2775be8b4787aecb636020f2e50482
source_published_at: 2026-09-12T15:01:19Z
first_seen_at: 2026-09-12T17:09:29.878266Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 71
interpretation_sha256: "sha256:a451a1c3f8afcedab7309adab8bd366b5953657f1791d53ee40f47deb52c951f"
description: "这篇文章由曾在 Palantir、Citadel 与 Kepler 负责前线部署工程（Forward Deployed Engineer）的从业者撰写，概述了该角色的职责、与传统咨询的区别，并通过项目 Frontline 的实践以及一次因数据不一致导致的存储系统崩溃案例，展示了在实际现场中识别并弥补设计缺陷的重要性。"
external_url: https://www.latent.space/p/forward-deployed-engineer-best-practices
parent_observation_id: null
last_seen_at: 2026-09-12T17:09:29.878266Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://www.latent.space/p/forward-deployed-engineer-best-practices](https://www.latent.space/p/forward-deployed-engineer-best-practices)
- **发布域名**: www.latent.space

## 要点解读

### 这是什么
这篇文章由曾在 Palantir、Citadel 与 Kepler 负责前线部署工程（Forward Deployed Engineer）的从业者撰写，概述了该角色的职责、与传统咨询的区别，并通过项目 Frontline 的实践以及一次因数据不一致导致的存储系统崩溃案例，展示了在实际现场中识别并弥补设计缺陷的重要性。

### 用在哪里
适用于技术团队负责人、招聘经理以及对前线工程师岗位定义不清晰的从业者，帮助他们了解在不同组织中该职位的实际定位及日常工作场景。

### 可以推断的
推测：在数据存储系统进入真实业务环境后，测试阶段未覆盖的异常数据往往会导致系统资源耗尽或崩溃。  
推测：前线工程师若能够亲临客户现场观察系统运行，能够更早发现设计与实现之间的差距，从而推动平台改进。

## 来源摘要/节选

> The difference between FDE and consulting; diagram by Vinoo Ganesh
>
> FDEs have the hottest job in AI. Labs, startups and PE firms are all hiring engineers to sit inside their customers’ operations and solve their problems. Almost none of them agree on what those engineers are supposed to accomplish, or what the strategy underneath the hiring actually is.
>
> I’m Vinoo, CEO of Kepler, the deterministic infrastructure for AI. I’ve built pieces of the forward deployed function three times, at three different institutions, over the course of over a decade. Here’s what I’ve seen work, what I’ve seen fail, and where I think this goes.
>
> The first was Palantir. I started there on product development, building storage and retrieval systems, and was later deployed as an FDE across commercial, DoD and NatSec, healthcare, and oil and gas. I also led Project Frontline, the rotation that took our software engineers and turned them into forward deployed engineers. Around 250 people went through this program, and a lot of them run forward deployed teams now at companies like OpenAI, Anthropic, xAI and Anduril.
>
> The second was Citadel, where I ran business engineering. Our customers were portfolio managers, and the only question that mattered was whether the data and software products we built helped them generate alpha.
>
> The third is Kepler, where the forward deployed function sits inside product rather than sales, in a domain where a plausible wrong answer is worse than no answer at all.
>
> FDE misunderstandings
>
> A few months ago, a16z launched the Forward Deployed Engineer Fellowship and I was nominated as one of the fellows, alongside a handful of people I used to work with. It’s a great program and I’ve enjoyed so many of the conversations. Last week I went to my first fellow dinner in SF.
>
> Around the table were FDEs from Snowflake, Anthropic, and a number of startups I’d been reading about, and over the course of the evening it became clear that we were all using the same two words (forward deployed) to describe jobs that had almost nothing in common. In one part of the conversation an FDE was a sales engineer who joined ‘the second call,’ somewhere else it was a quota-carrying rep who could write Python, and a few seats down it was closer to a consultant with a laptop and a statement of work, brought in to deliver something the product couldn’t.
>
> A few days later, someone earnestly asked our WhatsApp group how their FDE team should split scope with the consulting firm already sitting in the account. That’s a reasonable question to ask, but a strange one to have to answer, at least based on my own belief about what constitutes an FDE.
>
> To be clear, I’m not interested in gatekeeping a term; and meanings shift, this one faster than most. But what’s interesting is that folks in this group, the current experts at FDE, are describing fundamentally different jobs, with different reporting lines and different incentives. It’s no wonder half the comments on any YouTube video about FDEs are some version of “isn’t this just reinventing consulting?”
>
> So in the rest of this article, I will tell you the story of Project Frontline, through the narrow lens of a mistake I helped make, how that mistake turned me into an FDE, and how it eventually informed the rotation that turned our software engineers into FDEs.
>
> The history of Project Frontline
>
> First, some context. From nearly the beginning, Palantir was split into two separate functions. The first, Product Development (PD), built the platform. The second was Business Development (BD), which despite the name contained both the technical BD folks (already called FDEs) and non-engineering customer-oriented folks (we called them Embedded Analysts, or Deployment Strategists).
>
> PD, in the vast majority of situations, wasn’t directly engaging with customers; and BD, in the vast majority of situations, wasn’t directly contributing to building the core, generalized platform. PD tended to do customer discovery secondhand, by chatting with BD or by consuming the successful build-in-the-field features into the core product. None of that was a process, though. It ran on relationships — such as which FDE happened to know which PD engineer well enough to grab them. So a good insight from the field made it into the platform (or was dropped) depending on who was in the room.
>
> Me forward deployed in Bagram Airfield, Afghanistan.
>
> In 2013, in my early days at Palantir, I got to work on a transaction store called Phoenix. The store was designed by some of the best engineers I’ve ever worked with, and it had an abundantly clean design scoped to a clear set of customer use cases. The use cases, though, had been relayed to us second-hand. We knew and understood the design requirements, which had a focus on the commercial requirements of retention periods, and had clever solutions to bucket data in a way that enabled storing a rolling window of data. It behaved exactly as specified in every environment we controlled.
>
> Then we deployed it at a bank, and real financial data turned out to have holes in it that our test data never did. A blank timestamp fell through to the epoch, so the retention logic dutifully requested a ten-minute bucket for every window between January 1st 1970 and the present day. That came out to some 2.3 million keyspaces against a system where Cassandra (the backing tech) needed roughly five megabytes per file handle. The server rightfully OOMed [Out-Of-Memory] and starting it up again would have required 14 terabytes of RAM. Meaning this process was effectively dead on arrival.
>
> The root cause here wasn’t a lack of user research, as you might guess. We had a spec, we understood our use case, and we had read plenty about how institutions like this store their data. What we had never done was stand inside the building while the system ran against their production data. This meant that nobody on our side owned the gap between the design and the daily reality. Everything we knew about that bank had been relayed secondhand and by well intentioned people for whom bad data was just another normality.
>
> That’s how I became an FDE, which is a generous description of what actually happened. As Phoenix rolled out across Palantir’s commercial fleet I found myself flying out to fix what we’d shipped, and that put me in front of our actual users for the first time. In this case the users were Palantir’s own FDEs, which was lucky for me, because they could tell me what was wrong in the language I already spoke. I started building and expanding systems in service of what they were trying to do.
>
> So this is also the story of how I learned the FDE mindset viscerally rather than intellectually.
>
> This is where the ordinary version of this story ends, with some lesson about paying attention to your users. Phoenix turned into something more interesting than that. It became a platform, and Palantir’s FDEs started building on top of it across cybersecurity, KYC, AML, and a long tail of use cases nobody had scoped for. Eventually, we (Product Development) had to think about how to expand the Phoenix platform to support all of these use cases.
>
> I didn’t see it at the time, but that iteration cycle is the whole idea. An FDE solves customer problems in order to earn the insight that informs what gets built next. The role is an extension of the product team.
>
> FDEs today
>
> The reality is that none of this is the mentality of the vast majority of FDEs you see today. The term has been co-opted to mean something close to “a person who does something that vaguely involves a customer,” which is how you end up with job posts for a forward deployed equity researcher, or a forward deployed sales engineer. The instinct underneath the co-option is correct, even when the titles are silly, because customers matter more now than they did five years ago, and they matter more for a specific reason.
>
> The low-hanging fruit is gone. The problems that could be solved by a well-designed product sold identically to a thousand companies have largely been solved. What’s left is the work that sits inside the walls, in workflows that are messy and undocumented and nearly impossible to proxy from the outside. That’s why everyone is suddenly “forward deployed.” You cannot infer from a discovery call how a specific company closes its books, and the part of the problem that resists inference is now the part that’s left.
>
> Which means the holy grail has quietly moved. For a long time it was the repeatable motion, the same SaaS product sold the same way over and over; and that’s still the right ambition if what you sell is tokens or bytes or something physical. For everyone else the value has migrated to customization, to the last mile, to the twenty percent of the workflow that no product could have anticipated and which determines whether the other eighty percent gets used at all. Being forward deployed has become synonymous with solving that last mile.
>
> But solving it is only half of what the role is for. The last-mile problem you solve at one customer is the signal that tells you which piece of your platform needs to become generalizable. An FDE function that solves last miles without ever sending that signal home is a services/consulting team with a better title.
>
> So what are today’s FDEs supposed to be doing?
>
> I’d contend that your job as an FDE should be to collect nouns and verbs. Let’s break that down.
>
> Spend a week inside a company and you’ll notice that the same concept usually has at least four different names. Sales says customer, ops says client, finance books a billing entity, engineering writes org_id, and every seam between those teams hides a translation that breaks the moment somebody changes a definition. Those names are the surface and underneath them is the operating model. Meaning, you can really proxy the way a company works by learning their nouns and verbs.
>
> The nouns are what the people in a business treat as real. It’s usually a “thing.” A position, or a trade, or a counterparty. Usually, on a per-team basis, there are a handful of objects the whole operation turns on, and none of them are defined the way a textbook would define them. That’s because two firms will describe a position identically on a slide and completely differently in the code. That’s not a bug, that’s just what makes companies unique. I mean that if every company had the exact same set of nouns, then you would really just need one company.
>
> The verbs are how nouns move. Things like how a trade gets booked, or what has to be true before the books can close, or who signs off on an exception at eleven at night and what happens when that person is on vacation.
>
> Almost none of this is written down — it’s lived. It’s the system of operations through which an organization lives. It’s culture. It lives in the heads of the six people who have been there long enough to stop noticing it, and in a spreadsheet somebody built four years ago that the entire team now quietly depends on. That’s why it’s worth so much, and it’s also why you can’t ask for it.
>
> The names are the surface and underneath them is the operating model.
>
> Usually, the people who hold this knowledge don’t know they have it. In one of my last startups, we spent close to a year trying to move a customer from CSV to Parquet, and one data quality engineer blocked it every single time. We could never understand why and the reasons would always change, but would always be some variation of “a parquet is worse,” “it doesn’t work,” “it doesn’t make sense to me,” et cetera. We used the customer storage reduction argument, the compute minimization argument, the pipeline optimization argument…and none of it moved her, because none of it was about the actual problem.
>
> Then we had one of our FDEs go in and watch this particular data quality engineer work. She was pulling CSVs down from S3 onto a Windows laptop, double-clicking them open, and eyeballing the rows. That was the data quality check. Parquet had no native viewer at the time, so what we were proposing would have taken away the only data quality instrument she had and handed her nothing back. She wasn’t being difficult, she was just protecting the one thing that let her do her job.
>
> We built a Parquet viewer that night, she approved the migration two days later, and pipeline execution went from about seventeen hours to two. She would never have said any of this in an interview. From where she sat, the reason was obvious and not worth mentioning.
>
> Understanding and defining the system of operations, or nouns-and-verbs, of this analyst enabled us to not just understand the problem, but build a solution that we could then deliver across a fleet of customers with the same problem.
>
> The output needs to be a product
>
> Understanding the nouns and verbs contextualizes problems, but the output needs to be a product rather than just one happy customer.
>
> The nouns and verbs tell you what a problem actually is. They don’t tell you what to do about it; and this is where most FDE functions quietly go wrong, because solving the problem in front of you is satisfying and legible, and someone will thank you for it that same week.
>
> Keeping the customer happy is a real job and a good one. It belongs to solutions architects, who are rightly measured on it. The forward deployed engineer is there to turn what the field teaches into the thing every future customer gets. An FDE engagement that ends with one delighted account and nothing changed upstream has failed at the only thing the role exists for. You got the context and you spent it locally.
>
> I learned that one expensively. In one case a customer needed a data retention job, so I hacked together a groovy script named “vinoo.groovy” to hold them over — an afternoon of work that was never meant to survive the week. A year later, it was running across a customer of nearly a hundred thousand people, with my name fused to it. It became such a ridiculous story that my team started calling me vinoo.groovy. We fixed the problem, but never turned the fix into a product — so we spent years maintaining a hack that should have died immediately. Every shortcut you ship becomes something you own. The discipline is knowing which fixes belong in the platform and which ones you throw away on purpose the moment they’ve done their job.
>
> The fork
>
> This is where the whole thing splits. Do the work with nothing underneath it and you learn one company’s model, ship something shaped exactly to it, and lose all of it when the engagement closes. The next customer starts from zero, and so does the one after that. That’s consulting. It pays well, the people are excellent, and it doesn’t compound.
>
> Put a platform underneath the same work and every company you map makes the next deployment faster and the product sharper, because what the engineer brought home has somewhere to live. That’s the difference between selling hours and building an asset, and my honest read of this gold rush is that most of the companies in it are building the first one and describing the second to their board.
>
> That’s your job: build the platform.
>
> What we do at Kepler and what you can take from it.
>
> At Kepler, we set the function up this way from day one, before we had the customers to justify it. The alternative is to discover in month fourteen that your engineers have been optimizing for the wrong thing. From the beginning, our FDEs act as an extension of the product team; and that is the structural decision everything else follows from.
>
> We sell to hedge funds, investment banks, PE firms, and other financial institutions. These are fundamentally different institutions with different mandates, but all of them share a single non-negotiable: numbers have to be right, and someone has to be able to show why they are right. That is the constraint we design against and it turns out to be a useful one, because it forces the operating model into the open. No firm we’re involved with can produce a work product without a clear trail of provenance behind every number in it. That invariant defines our platform and gives us a bedrock to execute against.
>
> These problems are universal. The vocabulary is not.
>
> Every one of these firms is running some version of the same ontology underneath, and every one of them describes it differently. A position means one thing on a credit desk and something adjacent on an equities desk at the same bank. Two funds will use identical language for a return calculation and disagree about what goes into the denominator. Most of these differences exist because somebody made a reasonable decision in (say) 2011 and the decision outlived the person; also, it’s not written down anywhere that you can find.
>
> Identifying and filling that gap is the job of an FDE. A schema tells you what is stored. It does not tell you what is meant, and the distance between the two is exactly where a system that sounds right produces a number that is wrong.
>
> Provenance is a correctness requirement for our customers, but for us it does something else as well: it makes the field work compound. A system that can improvise around a bad encoding will never tell you the encoding was bad. Our system does not improvise. When we misunderstand how a firm defines something, that misunderstanding surfaces as a failure rather than as an answer that merely looks reasonable. The engineer who got it wrong finds out from the system, rather than from a client in a meeting six weeks later.
>
> The deployments then tell us what to extend in the platform, which is a narrower question than it sounds. We are not trying to learn which feature a given fund would like to have. We are trying to find the places where the platform is too narrow to hold what we keep running into. Three firms asking for the same feature is easy to notice and worth relatively little. Three firms needing something the provenance layer cannot express is the signal we actually care about; and it usually arrives quietly, in the form of an engineer working around the same limitation for the third time.
>
> If you are building somewhere else, here is the part I would take from all of this.
>
> Product leverage is what buys you the right to experiment. Every capability that lands in the platform makes the next deployment cheaper to attempt, and cheap attempts are how a small company learns anything at speed. Without that leverage, you get one expensive guess per customer. You scope carefully, build for months, and if the guess was wrong you have spent an account and a quarter finding out. We would rather be wrong four times in a month, because each of those attempts costs less than the one before it.
>
> Which is why the reporting line is not an administrative detail. Point the function at sales and the incentive becomes closing the account in front of you — which is a real job and one that somebody at the company should be doing. It is not this one. Point the function at product and every deployment is asked to produce something the next deployment can start from.
>
> Where the moat is
>
> So here’s where I’d put the moat in this era. It isn’t the model, which cheapens by the month and which you’re renting from somebody else regardless. It isn’t the talent either, because every lab is bidding for the same few hundred people and that price has already been discovered.
>
> It also isn’t the map of any one customer. That was true even a few years ago and it’s the same now, because extraction is nearly free and anyone can draft how a firm operates in an afternoon.
>
> The draft is not the asset. Knowing which parts of it are wrong is the asset, and that only comes from having been corrected.
>
> So, for us, the moat is the accumulated, current, verified understanding of how firms in a vertical actually operate, held in a platform that keeps it current and can prove it. Each of those words is load-bearing. Accumulated, because one deployment is an anecdote and the tenth is a pattern. Current, because operations drift and a stale model fails silently underneath an AI system in a way it never did in front of an analyst. Verified, because a plausible encoding and a correct one look identical until something breaks, and the whole point of insisting on provenance is that you find out which one you have.
>
> That is not purchasable. A competitor can hire your engineers, copy your interface, and read this article (ours try to do all 3!). What they cannot shortcut is the sequence of being wrong inside a customer, being corrected, folding the correction into the platform, and arriving at the next firm already knowing which questions are load-bearing. Every cycle of that makes the next one cheaper, and that compounding is the thing you own.
>
> I’ve watched this function get built three times and the pattern held every time. The engineers who mattered weren’t the ones who shipped the most for customers, but the engineers who came back and changed what we built.
>
> Hiring forward deployed engineers buys you exactly one thing, which is the right to identify which problems are worth solving. Most companies never get that far. But it’s the entry fee, not the prize.
>
> I’m Vinoo Ganesh, CEO of Kepler, where we’re building the layer this piece is about, the ground truth that lets an AI product trace every number back to source. Before Kepler I led Spark at Palantir and built Project Frontline, then ran business engineering at Citadel. If you’re building here, or you think I’ve got a piece of this wrong, you can argue with me on LinkedIn.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。