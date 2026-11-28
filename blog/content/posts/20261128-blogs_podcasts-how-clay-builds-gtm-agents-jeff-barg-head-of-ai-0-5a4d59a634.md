---
title: "How Clay Builds GTM Agents — Jeff Barg, Head of AI"
date: 2026-11-28T02:58:34+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "Prompt 工程", "博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:1c341382da6780d69f195ecc66ae626c9512c4da388f52dc64df46dc2f6b5db8"
source_payload_sha256: "sha256:3ce831e2b8a22fd73a223ac2e46dd3d52eb49717270b0cfccc474df3c4eef010"
observation_id: obs_5a4d59a63415e415d375d2d7cfcf2dd7529c453790fadbd98213d26917140810
event_id: evt_3b537ecf9d51667c643791fef27514cb60a812df96b63e7d92b360279364f41f
revision_id: rev_f064a126cf0902aebf4747e148ceee4a6be4b2f1791af51cda380ef13b854630
source_published_at: 2026-11-26T23:02:48Z
first_seen_at: 2026-11-27T19:07:58Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: true
source_truncation_reason: "crawler_feed_content_limit"
source_support: 1.0
source_title_chars_original: 50
interpretation_sha256: "sha256:87e1186f82d2f4865f4335402e46864e2cb943b7a694bc748bb0010a5524876a"
description: "Clay 负责人 Jeff Barg 分享其如何构建面向市场运营的智能代理基础设施，涵盖 Sculptor 编码代理、模型路由、潜客筛选、工作流编排、代理评测与成本控制，以及为何采用 BullMQ 等自建技术栈。"
external_url: https://latent.space/p/how-clay-builds-gtm-agents-jeff-barg-head-of-ai
parent_observation_id: null
last_seen_at: 2026-11-28T00:00:00Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://latent.space/p/how-clay-builds-gtm-agents-jeff-barg-head-of-ai](https://latent.space/p/how-clay-builds-gtm-agents-jeff-barg-head-of-ai)
- **发布域名**: latent.space

## 要点解读

### 这是什么
Clay 负责人 Jeff Barg 分享其如何构建面向市场运营的智能代理基础设施，涵盖 Sculptor 编码代理、模型路由、潜客筛选、工作流编排、代理评测与成本控制，以及为何采用 BullMQ 等自建技术栈。

### 用在哪里
适合关注 AI 代理产品化、销售与获客自动化、模型选择及工程架构的团队和产品负责人，也可用于评估 Clay 这类面向 GTM 的代理平台。

### 可以推断的
- 推测：潜客筛选成本下降后，平台可能从处理有限名单转向覆盖更大的市场范围。
- 推测：当代理能访问统一客户数据与执行结果时，其复杂任务能力可能比单纯增加工具更关键。

## 来源摘要/节选

> Open video on YouTube ↗
>
> Clay wants you to get about the same results whether you use its own agent or point Claude Code at Clay. Usage is already split close to 50/50 between Clay’s agent and outside harnesses. In this episode, we chat with Jeff Barg, Head of AI at Clay, about what it takes to build go-to-market infrastructure that any agent can use.
>
> Jeff joined Clay when it acquired Avenue, the ops alerting startup he cofounded. At the time, Clay had about 50 people, and Avenue had five. AI was already a big part of how Clay thought about its product, but nobody there worked on AI. Since then, the business has grown roughly 10x, and the team is up to around 600 people. In September, Clay raised $115 million at a $7.1 billion valuation.
>
> By Jeff’s napkin math, it would cost about $1,500 to check all 40 million companies in Clay’s database against your ideal customer profile with a classifier like TypeSafe’s Jev. Models have been acing Clay’s lead-qualification evals for about a year now. Jeff sees more value in using frontier models for orchestration and deep research. We also talk about why customers hate picking a model, how Clay plans to pick one for them, and why the team still runs its agents on a system it built with BullMQ, without Temporal or LangGraph.
>
> Jeff tells us what happened when OpenAI called off Clay’s ChatGPT apps launch with two days to go. We get into why customers hated Workflows at first, how agents came to build most workflows, and when post-training pays off. We also talk about why agents still can’t debug other agents, even as Clay’s agent can count its YC customers in about a minute.
>
> Sculptor started as a tool loop. Now it's a coding agent.
>
> When Jeff took over as Head of AI, one engineer was doing all of Clay’s agent work. He soon left to start his own company. Claude Code changed what Jeff wanted to build. His first launch was Sculptor, which shipped in September 2025 on models from the Sonnet 3.5 era. It ran a set of tools in a loop with a system prompt the team had spent a lot of time tuning. It was great at adding columns but terrible at booking ten qualified meetings.
>
> The evals didn’t catch much. Clay used an LLM to judge which tools Sculptor called. That missed things people actually did with it, like asking it to analyze a table or giving it an enterprise table with millions of rows.
>
> Jeff took away three lessons. Coding agents are really good at Bash and Python. Sculptor’s tools were too limited to do much by stringing them together. And the agent couldn’t see CRM data or campaign results. So Clay rebuilt Sculptor as a coding agent on the Pi harness. It runs the Clay CLI in a cloud sandbox. A new data layer called Audiences matches records across the CRM and Gong so the agent can see them together.
>
> Jump to the Sculptor discussion →
>
> Most companies post-train too early
>
> For Jeff’s first eighteen months at Clay, the team talked about training its own models. It only started to look viable in the past couple of months. Jeff sees two ways to bring costs down. First, swap in an off-the-shelf open-weight model, which is already much cheaper than Opus. Then you can post-train a smaller model on your own tools and queries until it does as well as Opus on your tasks.
>
> Jeff sees companies make two mistakes here. One is trying to beat the frontier models, which is still really hard even in a single domain. The other is starting before you spend enough on inference for the savings to matter. Jeff puts that threshold somewhere between $10 million and $100 million.
>
> Jump to the post-training discussion →
>
> $1,500 to score every company in the world
>
> Clay hasn’t put TypeSafe’s Jev into production yet, but Jeff has run the numbers. Clay’s database has about 40 million companies. A LinkedIn page is roughly a thousand tokens, and an ideal customer profile adds about 500 more. Ask a classifier whether each company is a good fit, and the bill for all 40 million comes to around $1,500. Today, most customers qualify a list of maybe 10,000 companies. At these prices, you can start with the entire market.
>
> Jeff puts a good enrichment budget at $1 to $10 per qualified lead and $10 to $100 per booked call. He thinks qualification itself is close to solved. Models have been scoring about as high as they can on Clay’s evals for roughly a year. Just about any model from the past year can pull a company’s latest funding round. Frontier models still matter for deep prospecting research and for orchestration, where Jeff says the best plays can be ten to a hundred times as effective as an average one.
>
> Jump to the Jev discussion →
>
> Customers hate the model selector
>
> Customers complain when they see Clay’s model selector. They can’t check the evals for their use case every time a new model ships, and they shouldn’t have to. Clay is about to launch an automatic router that picks a model for each task. There’s no fancy branding. Finding Apple’s CEO is a very different job from finding the CEO of an obscure local company.
>
> The selector isn’t going away. Agency owners and power users still want control. Everyone else just wants to get on with their work. Clay has to earn their trust before they’ll leave it on auto.
>
> Jump to the model routing discussion →
>
> No Temporal, no LangGraph
>
> Clay built most of its agent stack itself. It uses BullMQ to keep agent jobs running, Postgres and ClickHouse for product data, and Snowflake for analytics. Jeff isn’t sure how BullMQ will hold up if usage grows another tenfold, but it’s held up so far. Clay recently shipped 25 to 30 new integrations. Contracts and testing took longer than the engineering work.
>
> Where Clay did run into trouble was scale. People run an agent per row, so if someone starts a run on a table of 50,000 companies, inference demand spikes all at once. Clay brought in LangSmith to see what was happening. The team also built a way to throttle requests and to pause and resume work when a provider goes down or starts rate-limiting. The harder part is keeping things fair. Someone running a workflow for ten people still needs it to run when an enterprise customer is enriching a million rows.
>
> Jump to the infrastructure discussion →
>
> Built for every agent, not just Clay's
>
> Clay plans to ship a sandboxed agent that’s free to use any of Clay’s tools and building blocks. Jeff wants someone using Clay from Claude Code to get about the same results. People should be able to use Clay wherever they already work. Usage is already much closer to a 50/50 split between Clay’s agent and outside harnesses than Jeff expected.
>
> The push came from inside Clay. Its own go-to-market team lived in Cursor and wouldn’t leave it, so they asked for a CLI. The MCP team switched over to build it, and Clay’s sales team now does deal prep in Codex. So why build a first-party agent at all? Plenty of customers live in the Clay UI and want an agent right there.
>
> Jump to the agent platform discussion →
>
> Keep building when the plan blows up
>
> Jeff thinks it takes more courage to change plans at 600 people than it did at 50. Clay was a launch partner for ChatGPT apps. In the middle of the quarter, Clay put about a quarter of its engineers on the integration for a month. Two days before launch, OpenAI postponed it indefinitely. Clay kept building on the assumption that OpenAI would change its mind. Three or four days later, it did.
>
> When Clay first showed customers Workflows, they were confused. Some were upset. They wanted their spreadsheet. Now agency owners like it, and a growing share of the work that used to run in tables runs in Workflows. Most workflows are built with the CLI or the agent. CEO Kareem Amin spent five years building Clay when almost nothing was working. Jeff still sees that persistence in the company today.
>
> Jump to the ChatGPT apps discussion →
>
> Agents still can't debug agents
>
> What Jeff wants most is a model that can read a long agent trace and tell him where the run went wrong. Today’s models tend to flag whichever step took a long time, even when the mistake was somewhere else. Clay would like to pull traces from bad runs, have an agent review them and use what it finds to improve the agent automatically. That still doesn’t work, and Clay writes a lot of its skills by hand.
>
> Models still make basic mistakes, like retrying the same CLI command with the same inputs over and over. But when Jeff wanted to know how many YC companies use Clay, he asked the agent and had the answer in about a minute. A year ago, he would’ve had to scrape the batch, get access to Snowflake and cross-reference the two by hand.
>
> Jump to the agent debugging discussion →
>
> Show notes
>
> Clay — the go-to-market platform where Jeff is Head of AI.
>
> Clay raises $115M to be the AI growth engine for every company — the September Series D at a $7.1 billion valuation, led by Wellington.
>
> Clay acquires Avenue to help growth teams act on intent signals — the January 2025 deal that brought Jeff's team to Clay.
>
> How Clay Scales GTM Agents — Jeff's LangChain Interrupt talk on running Clay's agents in production.
>
> Clay Agent Plugin (CLI &amp; API) — the CLI and API that let Claude Code and Codex work directly with Clay.
>
> Inside Clay Workflows — how Workflows was built, including the table view customers asked to get back.
>
> Sellers have a new AI edge: Clay in ChatGPT — the ChatGPT app launch from Jeff's story.
>
> Sculpt recap: Building the self-learning revenue engine — Clay's October launches, including its new agent and Workflows.
>
> TypeSafe launched Jev because sequential LLMs are "totally useless for computers" — The New Stack on the classifier model behind Jeff's $1,500 math.
>
> Timestamps
>
> 0:00 Intro
>
> 0:55 Meet Jeff Barg, Head of AI at Clay
>
> 3:27 What a GTM engineer actually is
>
> 8:21 Selling Avenue to Clay at 5 people
>
> 16:10 An AI-forward company with zero people on AI
>
> 18:45 Claygents vs. Sculptor
>
> 24:49 Why Clay rebuilt its agent around a coding agent
>
> 27:48 When post-training and open-weight models pay off
>
> 30:35 Qualifying every company in the world for $1,500
>
> 32:40 Where you still need frontier intelligence
>
> 34:16 Why users hate the model selector
>
> 37:09 How Clay evals its agent
>
> 42:15 No Temporal, no LangGraph: Clay's hand-rolled stack
>
> 45:44 What broke when agents scaled
>
> 48:26 Why Clay's agent shouldn't beat Clay + Claude Code
>
> 54:26 OpenAI cancelled Clay's launch two days out
>
> 1:00:11 Workflows: from user backlash to agent-built
>
> 1:09:59 Why agents still can't debug their own traces
>
> Transcript
>
> Automatically transcribed from the revised edit; names and wording may contain errors.
>
> 0:00 We have a a company dataset of 40,000,000 companies. You can imagine just asking a question like, is this customer a good fit for my product or service? And you could run that across every company in the world. And it comes out to, I think, around $1,500. Our users hate our model selector. I think most most customers, like, don't wanna see it. Like, they're upset when they see it. We explicitly don't want our agent to be markedly better than just using Clay and Claude Code. We were doing some analysis on just how many YC companies are using Clay. We just asked our agent for this, and it found it in, like, sixty seconds. I was just thinking, like, a year ago, this would have taken so much time from looking through so many agent traces. One, like, models are still kind of dumb. Trying CLI commands with the same inputs over and over again and just not correcting them. We were one of the launch partners for ChatGPT apps, probably 25% of the engineering team for a month. I think two days before we were supposed to launch, they were like, we're gonna postpone this indefinitely. We have Jeff Barg here from Clay. You are the head of AI. Could you maybe introduce yourself and the business? Yeah, absolutely. Well, first, thanks for having me. So, I'm Jeff. I've been at Clay for about two years. And Clay, we like to think of ourselves as a creative tool for growth. And so really what that means is we help people build lists of companies and contacts for the purpose of prospecting or getting customers or finding new and great customers for their business. So we help qualify those lists using agents and other data providers to basically add data points like the amount of revenue or funding they've gotten or who their CEO is or different locations that they have and use that to basically filter down to figure out who their best customers who their best customers are. For those watching on YouTube, you
>
> 1:30 are actually really identified with this spreadsheet for some reason. When I talk about the spreadsheet form factor with other AI builders, they usually point to Clay as the success example. Yes. And yeah, it's funny. Clay started seven years ago really as a low code tool in the spreadsheet, so it makes a lot of sense. You know, we've been around for a while and really have built up on on that spreadsheet. Yeah. And then I'll identify... You said it was a... It's a creative something. There's nothing in creative here. It says build systems to grow revenue. That's... That sounds a lot more like, yeah, like, you know, money, guys. So creative. Yeah. Actually, let's give us give us two seconds on, like, why are you guys always so cheery and noticeable? Like Clay's branding is, like, really on point. Well, I do think it's it's a core part of the thesis that go to market really is a creative endeavor. And I don't know. I think, like, actually none of our competitors really seem to believe that or or try to do that. And I think it just adds to the ethos. I think it helps us build this community of people who, I don't know, try really cool and creative stuff to grow their companies. Did you guys start that way, by the way? Like, the business was always this? I think we've always spent a lot of time thinking about brand and how we present. But no, we really narrowed in on go to market. This is before I joined the company, but I think around three years ago, we really focused in on... We were deciding like, oh, should we focus on recruiting or should we focus on go to market? Focus on go to market and then, you know, really double down there.
>
> 3:00 Yeah. What was the reason for that? Just like a thesis? There's this like little nice history chart. I don't know what this plays, but... Yeah. Yeah. Yeah. I mean, I don't know. I mean, there was probably a lot of evolution in the five years that that this started, but Yeah. You know, we really started with a bunch of different kind of ways to think about the company or to think about the business, but it started very horizontal. And then I think we just really wanted to focus in on kind of a singular persona, and that helped us sort of build the things that ended up, you know, really making Clay successful. Cool. I think, you know, the thing that a lot of people tell me about Clay is that there's a lot of parallels with how I grew latent space in AIE because I identified this sort of segment of the market called... That I called the AI engineer, and I really focus on serving them. And you guys are basically synonymous with the GTM engineer now. Can you describe what that is? You know, I think this is one of the reasons why it's interesting for Basil and I to be on this pod because Basil is focusing on the FDE. You guys are on the GTME, and I'm on the AIE. You know, we really branded this term the go to market engineer, and the idea was just companies in, let's say, the 2010s really spent a lot of time trying to build pipeline or trying to, you know, grow their companies through just throwing more people at the problem. You can probably just engineer a lot of these problems. Like you can probably actually build systems to find customers for you. And I think this kind of coincided with LLMs and the post ChatGPT era where you could actually have agents go and crawl the web or, you know, qualify customers and basically exert judgment for finding potential customers in a scale that way. And so, you know, you kind of have this confluence of things where you had these new systems that could effectively qualify or, you know, score accounts for you and just kind of a continued trend towards automation in the space. And we were seeing more people basically engineering go to market systems and tried to, you know, brand that term around it.
>
> 4:30 And what was the role of a person doing that before? I'm sure people have tried to do this for a long time, but I think it's sort of, you know, if you were to think about the different disciplines that go into go to market engineering, it's probably some agent engineering to figure out how to write the best prompts to actually qualify something, right? So it's actually, understanding LLM systems. There's probably some data engineering in there, right? Like you're actually building a bunch of lists, you're transforming them, you're enriching them, you're filtering down and building different views on top of that. And there's sort of just regular software engineering built in there too, right? Like you're, I don't know, actually orchestrating systems that when someone fills out a get in touch form on your website, probably research that company and then maybe like send it to a rep or send it to an outbound campaign, right? All of these sort of things that are kind of just traditional software engineering. Yeah. Think the old school name for this might be marketing engineer, ops person, I may have even heard of it, software engineer might be a part of it, but a growth engineer might as well be a part of it, but growth maybe is more focused on marketing and yours is more sales, right? Yeah.
>
> 6:00 I think probably, this function would have fallen into revenue operations. Like, that's probably the bucket of things. And still today, we sell into revenue operations teams. But, yeah, I think it's it's somewhat distinct as a discipline. Like, I'd say it's it's pretty new. What kinds of backgrounds do successful go to market engineers tend to have? Oh, man. It's pretty it's pretty across the board. I think we've seen a lot of actually... A lot of traditional software engineers move into the role. And so that's been pretty interesting to see. It's like actually just people approaching the problem from like very kind of first principle software engineering standpoints. Definitely, like, ambitious RevOps folks have grown into the role as well. So we've kind of seen like all different directions of people move into it. Yeah. I think, you know, one of the things that people who have never done this job before don't really appreciate is that basically there is a lot of data mining and entity resolution and a little bit of knowledge graphs, maybe you can talk about that, just to get all this kind of lists of people just for prospecting. Yeah. I'm not sure, like... I think there's probably other use case other than prospecting. Obviously, a list is a very powerful thing. That actually combines a lot of information. Like, multiple tens of billions of dollar companies are created just as a database that feeds into Clay. Right? So, like, my canonical example is, like, ZoomInfo, like, or RocketReach, like, you've you've heard of all these things where you need enrichment from, like, I have an email, that's all I have, to, like, okay, what company do they work at? What size what size is that company? Like, are they the buyer? Did they just move companies? Like, I don't know what other details are relevant there.
>
> 7:30 You know, definitely Clay... Where where Clay sits in the market, we work with a bunch of different data providers and and partners, so How many? Think it's latest number, but in the hundreds for sure. And it's really flexible as a platform. Like if I think about kind of, again, back to other competitors or different people who have tried to build sales tools in the past, think I a lot of people try to build point solutions and Clay is like really generic, right? Like to your point, you can build a lot of stuff with lists and we've seen people build crazy things in Clay and that's intentional. And it comes with a bunch of trade offs. I think it's being very flexible means there's a lot of ways that you can make mistakes. There's a lot of different ways that you can, you know, build systems that that don't work as you'd expect, but it it becomes really powerful. Can we take a step back to when you started Avenue? And then maybe, like, how that led you to joining Clay? So, yeah, could you describe Avenue a little bit? So I I joined Clay through the acquisition of my previous company Avenue Yeah. Which is a company I cofounded with a friend of mine from high school in I have it up on screen. Yeah. The website's still up. Yeah. So Avenue was a company we started in, I think, early twenty twenty. And Avenue, we so I built this with a friend of mine from high school. We actually had been building apps together back in middle school and high school. So we had one of the first 500 iPad apps on the iPad store back in the day. Nice. So we'd always been kind of tinkering on ideas. And we... My co founder had worked at Uber. I worked at Amazon out of school. And we'd both wanted to start something together and both kind of had the idea of, hey, we're kind of working on different types of ops problems in very different domains, but kind of makes sense that actually these Marketplace operations teams actually need observability solutions like engineering would. So almost like I'd say the through line even to Clay is there are a lot of kind of engineering best principles that we were trying to build to bring to operations teams. But yeah, so we worked on this for about four and a half years. We went through YC. We raised from Accel. We sold to a bunch of really cool companies like Ramp, AngelList, Valen, DoorDash.
>
> 9:00 So some really cool and interesting customers to work with. And, yeah, so, you know, in late twenty four, we ended up, you know, so the business was growing pretty well. We ended up meeting Kareem and Varun through, I think, a mutual connection. But at the time, we had been approached by some other players in the space suit, some other, I'd say, like, engineering companies and who'd always been interested in acquiring the business. And so we were kind of in that mindset of like, hey, we could raise the Series A. We're pretty excited about the business growth but weren't necessarily like, we didn't know if like this was going to be then, you know, the billion dollar outcome that, you know, we were trying to get to when we set out to to start the business. And so then it was like, well, we should probably join up with a bigger company that already has more traction. Ended up ended up just really connecting with Kareem and Varun.
>
> 10:30 So they already had a lot of traction at that point? Yeah. I mean, I... You know, the How big was the company, by the way? Sorry. It was... I think we joined right as they were 50 people. And you were how many? We were five. Okay. So you were like 10% of the company? Yeah. I think I think we underappreciated how much of a bet they were taking on us. Yeah. Like to bring in 10% of the company in just, like, one in one day is is kind of a... Yeah. It's it's a pretty big bet. Yeah. Yeah. I think it's nice to bring in a scaled team and also perhaps, like, you guys are more on the automation side. Like, what do you what do you think you spiked more versus the original Clay team? Yeah. I mean, I I think, one, just we... We're really deep in in building, I don't know, just, like, very robust systems. I think, like, maybe the the story I like to tell is, like, Clay was really focused on PLG, and they had really nailed the PLG motion. So, like, joined the company when it was maybe like 15 to 20,000,000 in in revenue, but the biggest contract was was really small. Like, we we were just like so many companies who had found Clay and who just, you know, signed up and, you know, ended up getting value out of the platform. But they hadn't really moved into mid market or enterprise sales yet. And I think that was something that we really knew how to do at Avenue was, hey, build systems that could go into DoorDash and AngelList and Valiant and all of these kind of more scaled outcome companies. Would you say that was the, I guess, biggest learning that you took from Avenue and then applied it to Clay? One of the things that I think Clay has done really

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。