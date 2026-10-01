---
title: "Why Dwarkesh is Wrong about Computer Use + How OpenAI shipped its Jev competitor in 1 Week"
date: 2026-10-01T07:52:34+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "Prompt 工程", "博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:5ff55becd104c0f0c792ebc4b3f1ae028067ce5603a3eaadf3045720f9290bf1"
source_payload_sha256: "sha256:3aaa67015b9252b6ed848b7b0cdbf1a4ff4d49b62c0e1b7242076cda674a2fa8"
observation_id: obs_cfe32cdb08fcc91ab019a4753d80f9cb52d195340914158089043086cb626d65
event_id: evt_11166925da2bab0ae98e8cfa5891e2cf21c811d16175b15234cecef0e77497be
revision_id: rev_4d5ec038b061a96cf1ae6b90d53747163805ba050a5228ef96fdb7dac2837864
source_published_at: 2026-09-30T22:23:40Z
first_seen_at: 2026-09-30T23:48:28.428719Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: true
source_truncation_reason: "crawler_feed_content_limit"
source_support: 1.0
source_title_chars_original: 90
description: "当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。"
external_url: https://www.latent.space/p/devday-2026
parent_observation_id: null
last_seen_at: 2026-09-30T23:48:28.428719Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://www.latent.space/p/devday-2026](https://www.latent.space/p/devday-2026)
- **发布域名**: www.latent.space

## 来源摘要/节选

> Three months ago Dwarkesh, who has been posting incredible blogs and episodes about RL, posted a framing question for his video essay on RLVR which upset a lot of Computer Use folks:
>
> We are no strangers to learning in public and are no strangers to the stress of getting things wrong when you have a big platform. However, we were at Anthropic for the Computer Use launch, there for Claude Cowork with the first big podcast on it, organized the first Computer Use track at AIE presenting the state of the art, and were close to the OpenAI-Sky Software acquisition that now powers the complete domination of computer use that Codex enjoys today. This is why we’re excited to bring you today’s first guest, Ari Weinstein, cofounder of Sky and now leading all the amazing CUA progress that casuals might miss:
>
> Ari explains why Computer Use is now “180 degrees different” from where it was months ago, how agents are learning to debug and recover from failures, why combining screenshots with accessibility data, the DOM, Playwright, and generated code changes the speed equation, and why the next frontier is making agents literally superhuman at using software.
>
> OpenAI clones Jev
>
> In the second half, Nikunj Handa from OpenAI’s API team breaks down the new developer stack: async tool calling, mid-turn steering, WebSockets, UltraFast inference, the Decisions API, prompt caching, pre-warming, compaction, and the Agents API. Given that we were the first Jev podcast, we particularly focus on the unusually fast sprint on the Decisions API:
>
> And why it is just a Luna wrapper for now but the team is motivated and egoless enough to clone what they consider to be good patterns.
>
> We discuss:
>
> Why OpenAI thinks Computer Use has changed dramatically in just the last few months
>
> Dots and what changes when every agent gets its own Linux computer
>
> Why Computer Use can now complete some tasks faster than the average human
>
> The path from human-level to “literally superhuman” computer use
>
> Why modern agents are much better at debugging and recovering from failure
>
> How screenshots, accessibility trees, the DOM, Playwright, and generated JavaScript work together
>
> App Shots and why they give models much richer context than ordinary screenshots
>
> Why Computer Use can close the loop between writing software and testing it
>
> Trust, permissions, and safety when agents can make payments and operate websites
>
> Async function calling and why models no longer need to stop reasoning while tools run
>
> Mid-turn steering, WebSockets, and the architecture behind more responsive agents
>
> UltraFast inference and how OpenAI is pushing frontier models toward much lower latency
>
> The rapid internal story behind the Decisions API
>
> Why Decisions API is more than structured outputs at low latency
>
> GPT Live, fast tool calling, and real-time computer control
>
> How OpenAI is already using Decisions API for support classification and internal workflows
>
> Longer prompt caching, cache pre-warming, and cache-aware applications
>
> Server-side compaction vs manual compaction for long-running agent threads
>
> What should live inside an Agents API versus a developer’s own harness
>
> OpenAI as an “AI cloud” and the search for higher-level primitives beyond raw model APIs
>
> Ari Weinstein
>
> Product &amp; Engineering, Computer Use at OpenAI
>
> X: https://x.com/AriX
>
> LinkedIn: https://www.linkedin.com/in/weinsteinari/
>
> Nikunj Handa
>
> Product, API at OpenAI
>
> X: https://x.com/nikunjhanda
>
> LinkedIn: https://www.linkedin.com/in/nikunjhanda/
>
> Timestamps
>
> 00:00:00 OpenAI DevDay: Dots, GPT-6.1, Agents API, and Decisions API
>
> 00:02:52 Dots and Personal Cloud Computers
>
> 00:04:59 Why Computer Use Is “180 Degrees Different”
>
> 00:06:04 From Sky to Self-Debugging Computer Use Agents
>
> 00:09:24 How Computer Use Sees and Operates Software
>
> 00:12:09 From Faster Than Humans to Superhuman Computer Use
>
> 00:16:03 Agents API: Trust, Permissions, and Safety
>
> 00:17:31 Computer Use for Coding, Testing, and QA
>
> 00:19:14 GPT-6 APIs, Async Tool Calling, and UltraFast Inference
>
> 00:23:21 The Rapid Story Behind Decisions API
>
> 00:25:32 What Decisions API Is and How It Works
>
> 00:30:24 What OpenAI Is Building With the New APIs
>
> 00:32:23 Prompt Caching, Pre-Warming, and API Performance
>
> 00:35:20 Context Compaction for Long-Running Agents
>
> 00:37:13 Memory, Higher-Level APIs, and the AI Cloud
>
> Transcript
>
> Introduction: OpenAI DevDay and the New Agent Stack
>
> Vibhu [00:00:00]: Okay. We’re very excited to be here. Today is OpenAI DevDay. Special podcast
>
> Swyx [00:00:08]: We’re the first podcast after your livestream.
>
> Vibhu [00:00:10]: First podcast. We have Ari here, who leads the product and engineering team for Computer Use agents. Before we kick in and dive deep on Computer Use, you wanna give a quick recap? What was announced? What’s the quick slew of announcements you guys had today?
>
> Ari Weinstein [00:00:24]: Yeah. yeah, it was a super exciting day. we just got out of the keynote. It was really sick. there were a bunch of Computer Use announcements that I think are worth thinking about. We have, Dots, which is the new, sort of personal assistant product, and, that has some really exciting Computer Use features. There’s GPT-6.1 Sol, which is this amazing new model, that I think is particularly great for Computer Use ‘cause of, sort of the cost and speed, advantages. I think, I think we shared that it’s, a fifth of the cost of Astra and a seventh of the cost if you’re looking at Computer Use specifically, which is really amazing. sorry, there were so many things. I’m trying to sort through it.
>
> Swyx [00:01:02]: And the API.
>
> Ari Weinstein [00:01:03]: Agents API, which now has Computer Use in it, which is really cool, ‘cause now developers can build on the same Computer Use, that is part of Codex, and ChatGPT. and then there were some demos of our existing Computer Use features, like app shots, where you can take the context of something you’re doing on your computer and bring it into Codex and ChatGPT really fast. And then, like, native Computer Use on your Mac, where Roman had it taking screenshots of his app, automatically, and he could do other things on his computer while Computer Use was using his applications. so yeah, really exciting keynote.
>
> Swyx [00:01:35]: And not to mention the Decisions API.
>
> Ari Weinstein [00:01:37]: Decisions API.
>
> Swyx [00:01:38]: Off the bat, are they all the same model? Like, this is. Or the same dataset distilled to different models?
>
> Swyx [00:01:44]: Like, basically, like, is Computer Use using Decisions API, or are they, like, kinda separate?
>
> Ari Weinstein [00:01:49]: So what’s really cool about the Decisions API is it, you know, it has all these new capabilities. It does inference in parallel. it doesn’t have reasoning. It’s a smaller model, than the ones we use for Computer Use. and so those capabilities make it really fast.
>
> Dots and Delegating Work to a Cloud Computer
>
> Swyx [00:02:07]: Yeah.
>
> Ari Weinstein [00:02:07]: They also make it a little bit less good at doing, like, long horizon, sort of sophisticated tasks. And so I think I would say it’s still an open area of research for how we, like, bring those approaches together. But, yeah, I’m really excited to see what people build with the Decisions API.
>
> Vibhu [00:02:24]: One of the interesting things is Dots now have attached personal computers.
>
> Ari Weinstein [00:02:28]: Yeah.
>
> Vibhu [00:02:28]: So it seems like they’re very much more persistent. You’ve been using them for a while. How should people push the bounds? Like, what should people aim for? What should they try? Personally, right now I use it for a lot of customer service. Like
>
> Ari Weinstein [00:02:41]: Cool
>
> Vibhu [00:02:41]: “Oh, this was wrong. I don’t wanna sign in. I don’t wanna authenticate.” Find whatever and just get it fixed.
>
> Ari Weinstein [00:02:45]: Yeah.
>
> Vibhu [00:02:46]: How should we push further? What should people try?
>
> Ari Weinstein [00:02:50]: Dots Are a really cool product because each Dot has access to its own Linux virtual computer in the cloud, which is different from our other products. you know, traditionally, we’ve have access to a browser in the cloud, or it has access to your own computer, but now you get your own entire Linux computer in the cloud. And so it can run full desktop applications, and it can also use a web browser. And so, yeah, you know, I think the powerful thing about Computer Use and the reason why I think it’s so, exciting is because it makes it so that the agent can do anything you as a, as a person can do, because all the software in the world was designed for humans, and now agents can use that same software, and you can delegate to the agent. So, yeah, like, anything that you would do on a computer, you can ask a Dot to do. Yeah, I think what particularly is useful is gonna really depend on who the end user is and what- what’s valuable in their life. but yeah, I would just start by thinking about, like, one of the things that you spend time on and how could you delegate those to an agent.
>
> Swyx [00:03:47]: Yeah, a lot of flight booking and shopping and honestly even, like, playing a game or whatever, right?
>
> Ari Weinstein [00:03:52]: Totally.
>
> Swyx [00:03:52]: Yeah.
>
> Ari Weinstein [00:03:53]: Yeah, I don’t know. For me, something I did recently, I’ve been working on. I’ve, subscribed to a meal prep service ‘cause I was trying to, like, eat healthy, you know? And I really like this meal prep service I found because it lets me customize the meals I order to, like, a high degree of granularity. So I can say, like, “I want this many grams of chicken and this many grams of rice.” but it was so complicated. It took me two hours to do an order, and I found that I could ask Computer Use to do it for me, and it did it in 15 minutes. so I actually saved two hours. it both did it eight times faster than I could, and it saved me two hours on GPT-6.1 Sol.
>
> Swyx [00:04:32]: Yeah.
>
> Ari Weinstein [00:04:32]: So those are the kinds of tasks that I feel like, are really powerful.
>
> Swyx [00:04:36]: As a creator, I can tell you automatically, immediately, my number one use case is automating YouTube.
>
> Ari Weinstein [00:04:40]: Nice.
>
> Swyx [00:04:40]: Because, YouTube doesn’t expose a lot of things via API.
>
> Ari Weinstein [00:04:43]: Yeah.
>
> Swyx [00:04:43]: And you have to just put it in a VM and just, like, run it, for, like, let’s say, let’s say their AB testing feature or making community posts. None of this is available by API ‘cause they hate developers.
>
> Swyx [00:04:53]: Anyway, so,
>
> Ari Weinstein [00:04:55]: I’ve heard that from our developer experience team too. They use it with YouTube a lot. Yeah. It’s really awesome.
>
> Swyx [00:04:59]: So I wanna draw for, you know. let’s say, I wanna get a little bit spicy. One of our, the leading AI podcasts, our friends, is famous for saying that Computer Use hasn’t advanced in the last two years.
>
> How Computer Use Has Changed in the Last Year
>
> Ari Weinstein [00:05:12]: Yeah.
>
> Swyx [00:05:13]: Which is a very interesting statement, and I think you’re one of the best people in the world to talk about this, like, how have things have progressed, right?
>
> Ari Weinstein [00:05:20]: Yeah. You know, they said that a few months ago, I think, and I hope they have a different perspective now because Computer Use is, like, 180 degrees different than it was.
>
> Swyx [00:05:26]: He’s a, he’s a tough guy to impress.
>
> Ari Weinstein [00:05:27]: Yeah, okay. well, we’re working on it.
>
> Swyx [00:05:30]: But, you know, you worked on. You’ve, like, basically spent your whole career working on, like, some kind of computer automation, right?
>
> Ari Weinstein [00:05:34]: Yeah.
>
> Swyx [00:05:34]: Like shortcuts
>
> Ari Weinstein [00:05:35]: Yeah
>
> Swyx [00:05:35]: At Apple, and then Sky, and then, and then joining OpenAI. Can you draw, like, what your through line is for, like, what is driving you and what- you, what wasn’t possible back then maybe
>
> Ari Weinstein [00:05:47]: Yeah.
>
> Swyx [00:05:48]: And, like, what your sort of milestones were.
>
> Vibhu [00:05:49]: I guess to add on to that as a follow-up question, what’s the major change from using Codex Computer Use from, like, last week
>
> Ari Weinstein [00:05:57]: Yeah
>
> Vibhu [00:05:57]: Through to today? Is it model? Is it dots? Is it harness? So all the history plus what really just changed in today’s announcements?
>
> Ari Weinstein [00:06:04]: Yeah. On the through line, I guess I’ve always been excited about automation and helping people automate tasks because then you can, like, save time in your life and focus on things that are more important to you than, like, operating a computer very intricately. And so, yeah, that was why we worked on some of those products. I was at Apple before. we made a company called Sky. we ended up joining OpenAI, which is really exciting. and I think something that was
>
> Swyx [00:06:27]: And almost like you have to hack around Apple until Apple was like, “Fine, like, we’ll just hire you and you can just work on the inside,” right? Like.
>
> Ari Weinstein [00:06:35]: It was, it was a cool place to get to work. what was really interesting looking back at Sky is we were, we were working on Computer Use there as well, and the models were so much less capable. And now the models, just in the last one year, have become extraordinarily capable at Computer Use. I think the biggest delta that I see is before they could, like, reliably start tasks, but then they would run into problems, and now they’re really good at debugging. They’re really good at trying again, introspecting what is and isn’t working. and I think we’ve also brought the Computer Use the Computer Use field itself has moved forward. I think we’re using more techniques. now Computer Use, often writes code. So if you actually look at it in Codex and you expand the tool calls manually, you can see that it’s not just doing one action at a time. It’s actually writing JavaScript code that it executes, that the computer executes to perform sometimes many actions at once, which is a great, you know, speed up and great capability. We use more accessibility, sort of multimodal interfaces. So, the model may use screenshots, it may use accessibility, it may use Playwright. it can use a lot of different mechanisms, based on the task at hand. and then, yeah, the model acceleration has been, has been just amazing. So, yeah, what’s different today? I think we’re making computers better all the time, so I think just, like, one day’s difference, is probably a little bit less consequential than, like, even the past month or the past two months. but, yeah, I think the Computer Use in Dot is really exciting as well as, the new model that we came out with.
>
> Measuring Computer Use and Improving the Harness
>
> Vibhu [00:08:03]: On the keynote, Tejal was mentioning 7x improvements in Computer Use speed, a lot better on a few benchmarks. How do you guys think about measuring it? Computer Use is one of those things where, as you say, you know, it’s improvements over time.
>
> Ari Weinstein [00:08:20]: Yeah.
>
> Vibhu [00:08:20]: Is it harness? Is it model? Is it post-training?
>
> Ari Weinstein [00:08:22]: Right.
>
> Vibhu [00:08:22]: How do you guys look at it internally about measuring how good it is, and what were the changes with the new model?
>
> Ari Weinstein [00:08:29]: We actually have a bunch of different ways of measuring it, some of which are on different permutations and configurations of the harness. It’s a bit of a complicated story because, you know, our production products have, you know, some more safety checks, and, you know, those are configured differently based on the needs of the, of the task at hand. So there’s a lot of ways to measure it, but I think regardless of how we measure it, we find pretty consistent gains. and those gains are, sometimes in the harness and sometimes in the model. and yeah, I was really excited by this result that GPT-6.1 is even more cost-effective for Computer Use than its baseline cost improvement as compared to Astra. It’s, like, really cool to see.
>
> Swyx [00:09:10]: Yeah. I mean, one of the visuals I really liked from the livestream was that, you’re sort of improving the Pareto frontier of, your, curve, and there was a lot of talking about how you’re improving it together with the harness.
>
> Ari Weinstein [00:09:24]: Yeah.
>
> Swyx [00:09:24]: Can you give some examples of aha moments that you had, whether it’s on, like, model driving the harness driving the model, whatever?
>
> Ari Weinstein [00:09:32]: I don’t mean to repeat myself, but I think, like, introducing more modalities has been really powerful.
>
> Swyx [00:09:36]: Okay.
>
> Ari Weinstein [00:09:36]: One more specific example of that is, in the past, I think we saw a lot of Computer Use, products had to spend a lot of time, like, scrolling, you know? So it would, like, take a screenshot. It would try to do something. It would be like, “Oh, I gotta, like, scroll down to the next page of results,” and then it would take a screenshot, and then it would try to do something. It would scroll down again. And so I think, with accessibility and other. and, direct access to the DOM and other things like that, now the language model can actually see, like, an entire page or an entire application. It can write code that can do multiple steps at once. And so I think those have been probably the biggest single aha moments. There’s, like, a lot of tiny ones that are less exciting in comparison, but actually we do find also that a lot of speed improvements are driven by, like, a lot of little paper cuts that we gotta go in and introspect.
>
> App Shots, Accessibility, and Better Computer Context
>
> Swyx [00:10:21]: Yeah. A lot of really hard engineering.
>
> Ari Weinstein [00:10:23]: Yeah.
>
> Swyx [00:10:23]: I mean, app shots in general, right? Like, I think people don’t quite get the difference if. because there’s, like, a nice visual in Codex when it
>
> Ari Weinstein [00:10:30]: Yeah
>
> Swyx [00:10:30]: When you take an app shot, but they don’t maybe they get the difference that, you are able to actually drive each button and you have the, you have each text, in a very optimal representation.
>
> Ari Weinstein [00:10:40]: Yeah. Exactly. Yeah. It’s kind of fun actually. If you wanna be, like, really nerdy about it, you can go into Codex, take an app shot by hitting the two command keys. So you grab the content from whatever app you’re working with, bring it into the, Codex or ChatGPT chat. And then the. if you click on the attachment and you click on this, like, little tiny button in the top right, you can see the raw text and you see the raw accessibility representation. And yeah, we’ve put a lot of work into, putting
>
> Swyx [00:11:04]: Just dumping everything out. Yeah.
>
> Ari Weinstein [00:11:05]: Dumping it out, but also making it token-efficient, doing it efficiently. There’s, like, a bit of an art to it. And, you know, it turns out that the same technology that was invented for humans, you know, who maybe have accessibility needs, who wanna use a screen reader technology, that technology is really helpful for them to be able to use computers. It’s also really helpful for LLMs to be able to use computers. So that’s been, like, really fun to get to work on.
>
> Vibhu [00:11:27]: For context, I feel like a lot of people don’t understand app shots. They don’t even know it’s a feature.
>
> Ari Weinstein [00:11:30]: Yeah.
>
> Vibhu [00:11:31]: It’s when you double hit command, it pulls in what looks like a screenshot
>
> Ari Weinstein [00:11:34]: Right
>
> Vibhu [00:11:34]: And you’re like, “Oh, why have I opened up just a screenshot and thrown it in?” No, it’s actually pulling all the metadata, all the code, everything.
>
> Ari Weinstein [00:11:40]: Yeah, exactly. Yeah. So it’s like, you know, if you take a screenshot of a webpage that has a link- The screenshot doesn’t include where the link goes. It doesn’t include, you know, maybe you take a screenshot of your calendar, the ca- event ti- titles are truncated, you know? But when you take an app shot, it gives, like, the language model, like, full context about everything and, that lets it, just sort of, like, do much more.
>
> Swyx [00:12:02]: Yeah. For those who wanna see more, Jason Liu, I invited him to do a full workshop on this, at AI Engineer.
>
> Ari Weinstein [00:12:07]: Amazing.
>
> Swyx [00:12:08]: Did a great job.
>
> Vibhu [00:12:09]: I have a broader vision question
>
> Toward Superhuman Computer Use
>
> Ari Weinstein [00:12:11]: Yeah
>
> Vibhu [00:12:11]: On Computer Use agents. So your example of take a screenshot, scroll page, take a screenshot is where we were.
>
> Ari Weinstein [00:12:17]: Right.
>
> Vibhu [00:12:17]: Today, they can automate a lot. what are the bottlenecks? Is it models? Is it harnesses? What. Where do you see it going in, like, two years? Do you see it just running for hours? How do we get there? Any predictions on where Computer Use goes?
>
> Ari Weinstein [00:12:32]: Yeah. I mean, I think what’s really crazy that I think, You know, the team’s accomplished over the past couple of months is that now Computer Use is, like, faster at accomplishing tasks than, like, the average human probably in most cases. and I think that the next frontier is to have Computer Use be, like, literally superhuman in its performance where it actually is as fast or faster at using software than, like, expert Computer Users like us. and I think that’ll be really consequential and exciting when that happens because I think we’ll be able to all of a sudden build products, that, provide just much more real-time experiences. And I think it’ll also. lowering the barrier to entry of, or the activation energy, I suppose, of using Computer Use I think will make us start to default to doing certain things in agents that we’ve become accustomed to doing manually. And I think that’s exciting also ‘cause it’ll save us a ton of time. and I think there’s a, you know, there are a lot of different little paper cuts and bottlenecks that are sort of standing in the way of that. I think that there’s, yeah, there’s things on the model side, there’s things on the inference side, there’s things on the harness side, there’s things in the, in the representation. You know, we find that as Computer Use gets faster, we’re increasingly bottlenecked by just, like, the speed of doing an operation. Like, for example, you know, a non-trivial amount of time in our benchmarks of Computer Use tasks is actually, like, let’s say you’re automating a task on doordash.com. Like, a lot of the time is actually waiting for doordash.com itself to load, you know?
>
> Swyx [00:14:04]: Yeah, then you just write a wait and then you execute the wait.
>
> Ari Weinstein [00:14:07]: Yeah, totally. And you wanna get. Yeah, actually, it’s actually really important that you get that de- like, you want as little delay as possible between when it finally finishes loading and when you go and
>
> Swyx [00:14:16]: Yeah
>
> Ari Weinstein [00:14:16]: Trigger the LLM to do the next action, which is actually- itself a statistical science.
>
> Swyx [00:14:20]: Like an event-driven way maybe to do that.
>
> Ari Weinstein [00:14:22]: When possible, you want it to be event-driven.
>
> Swyx [00:14:24]: JavaScript has some load events.
>
> Ari Weinstein [00:14:25]: And JavaScript has load events for. or the web browser has load events for web navigation, but there’s other types of events that actually really can’t be event-driven. So there’s a lot of complexity
>
> Vibhu [00:14:34]: The one that comes to mind is, like, chatting with customer service.
>
> Ari Weinstein [00:14:37]: Yeah.
>
> Vibhu [00:14:37]: Replies could take 30 seconds, could take three minutes.
>
> Ari Weinstein [00:14:39]: Oh, right.
>
> Swyx [00:14:41]: I have dealt with so many bots with Codex. it’s great, but I also wonder if the other side knows that they’re talking to a bot ‘cause I’m, like, answering in complete sentences. Like, I’m capitalized correctly.
>
> Ari Weinstein [00:14:50]: That’s hilarious.
>
> Swyx [00:14:51]: Like, I’m giving full num- full reference numbers and everything. Like, it’s too. it’s clearly too good. I don’t care. Like Like, I’m just, like, trying to get my support case.
>
> Vibhu [00:14:58]: I’ve prompted it to, like, you know, “Don’t pretend you’re a bot. Be very annoyed human.”
>
> Vibhu

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。