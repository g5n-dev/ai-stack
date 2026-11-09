---
title: "How Stanford Teaches AI-Native Engineering — Mihail Eric, Monaco"
date: 2026-11-09T08:53:27+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "机器学习", "Prompt 工程", "博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:66a34ff4392f0970508901b98170cf28eac3be3e61e94b41888746b023176cbd"
source_payload_sha256: "sha256:daf8ea3eeb8dce561848b78fbad14c3af4528a27a4a84b31416d81c276bf72f0"
observation_id: obs_2c00110bd6231e5944e32b7c2b10255f3721d5597aa09b393fd97b57c877a8f7
event_id: evt_b192c524a4542db04537d2b0d9fb88f43d605572fa6606a05a35b63f4dad4c81
revision_id: rev_29133cb041e2ea9535ca1285f0f629725011a7a298c35c0fe34ed3969c0620c4
source_published_at: 2026-11-08T21:41:44Z
first_seen_at: 2026-11-09T00:52:36.112955Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: true
source_truncation_reason: "crawler_feed_content_limit"
source_support: 1.0
source_title_chars_original: 64
interpretation_sha256: "sha256:3cb31a4789f43576462b9d798474c3604314685749b1e4c226299c406fdda38d"
description: "这是一段对 Stanford 课程教师、Monaco AI 负责人 Mihail Eric 的访谈，讨论 AI 时代软件工程师需要学习什么，以及编码代理如何进入课程、代码审查、故障排查和软件交付流程。"
external_url: https://latent.space/p/cs146s
parent_observation_id: null
last_seen_at: 2026-11-09T00:52:36.112955Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://latent.space/p/cs146s](https://latent.space/p/cs146s)
- **发布域名**: latent.space

## 要点解读

### 这是什么
这是一段对 Stanford 课程教师、Monaco AI 负责人 Mihail Eric 的访谈，讨论 AI 时代软件工程师需要学习什么，以及编码代理如何进入课程、代码审查、故障排查和软件交付流程。

### 用在哪里
适合正在采用编码代理的工程师与技术团队，也可用于设计 AI 编程课程、建立代理工作环境，或思考代码审查、知识管理和值班流程如何调整。

### 可以推断的
- 推测：当代码生成效率提升后，理解变更、确认意图和评估潜在影响会成为工程师的重要工作。
- 推测：要让代理稳定参与生产开发，团队可能需要提供可运行、可测试且权限边界清晰的工作环境。

## 来源摘要/节选

> The AI Engineer YouTube channel just crossed one million subscribers. Thank you to everyone who’s watched a talk, sent one to a teammate, or put something they learned into production. For this special, we wanted to sit down with someone who has to answer a question a lot of us are asking at work: what should a software engineer actually learn now?
>
> Mihail Eric has two places to test his answer. He teaches The Modern Software Developer at Stanford and leads AI at Monaco, where his colleagues use coding agents to ship software and investigate outages. I asked him to take us through the syllabus, then tell us which parts survived contact with his own engineering team.
>
> This is also meant as a preview for all of you joining us in San Francisco for AIE Code next week, as required knowledge for all the conversations with the speakers, sponsors and attendees you’re about to have. If you can see this as a LS subscriber and haven’t got a ticket yet, you can use this code for 30% off (no refunds, sorry)
>
> Last year’s homework takes one prompt
>
> The first run of CS146S had nine assignments and a capstone. In one exercise, students ran an AI code reviewer on a repo and evaluated its feedback. By the next run, Mihail figured students could one-shot a lot of those exercises. When he asked a room of Stanford sophomores and juniors how they coded, everyone he surveyed was already using an agent.
>
> So this time, part of the homework is contributing to an open-source project. The person who maintains the repo reviews the student’s patch. I like what that does to the assignment. You can ask an agent to implement a feature in an afternoon. You still have to find out whether the maintainer wants it, why the code behaves the way it does, and what else your patch might break. That conversation is also how a junior engineer gets to learn from a senior one.
>
> There’s an exercise in the episode you can borrow for your next PR. Geoffrey Litt’s explain-diff skill turns a change into a visual walkthrough, then quizzes you about it. Try it on a patch your agent just wrote. Which question do you have to reopen the code to answer? Watch the discussion.
>
> What Monaco buys, and what it builds
>
> At Monaco, the team evaluated code review products and kept using Devin. Agent workspaces went the other way. A background agent needs somewhere to run the product, reproduce a failure and test the patch. The details depend on how Monaco’s cloud is set up, so the team built its own workspaces. Mihail’s rule of thumb: “You buy to learn, and you build to keep.”
>
> One result is Hal. An engineer can ask it to investigate something that broke and open a PR. A salesperson can ask the same system how the product works. In one case the useful answer is a change someone can review. In the other, it’s an explanation you can give a customer. Give both people a wall of debugging output and you’ve only served one of them.
>
> The question I kept coming back to was what happens at the other end of the PR. An agent sees the current code. Where does it look to find out why the team rejected this same change six months ago? That takes us from Basis’s Authority Map to Mihail’s prediction that open-source repos will become agent-run software factories. It’s a good reason to send a student to a maintainer today. Someone still has to decide which change belongs in the project.
>
> If you’re building with coding agents, come join us at AI Engineer CODE. And if you’ve been teaching this stuff yourself, I’d love to hear which assignment you had to rewrite first.
>
> Show notes
>
> Stanford CS146S — The ten-week syllabus, assignments and open-source partners. You can also switch to the previous year’s course to compare.
>
> Build a coding agent and look inside Claude Code — Mihail’s walkthroughs of the tool loop and the harness around it.
>
> Understanding is the new bottleneck — Geoffrey Litt’s approach to learning what changed in an AI-written diff.
>
> Monaco’s agent-developer workspaces — The team’s reasoning for building a place where agents can run and test the app.
>
> How to Kill the Code Review and the underlying Faros study — Teams with high AI adoption merged 98% more PRs, while their PR review time was 91% longer.
>
> Basis’s Authority Map — Where an agent should look for current behavior, earlier decisions and intent.
>
> Stripe’s Minions — A production example of giving background coding agents an environment and a path to an engineer-reviewed PR.
>
> Boris Cherny’s Steps of AI Adoption — The five stages we pull up on screen near the end of the episode.
>
> Mihail on The Thinking Mode — EO Studio’s interview, excerpted at the start of ours.
>
> Timestamps
>
> 0:00 · One million AI Engineer subscribers and the CODE Summit
>
> 0:51 · Mihail Eric and Stanford CS146S
>
> 5:26 · What junior engineers need to learn now
>
> 10:02 · Open-source maintainers review the students’ code
>
> 15:04 · A tour of the ten-week syllabus
>
> 24:04 · The loop, tools and harness inside a coding agent
>
> 32:18 · Context engineering for a large codebase
>
> 38:15 · Skills that make you understand the diff
>
> 46:42 · The Monaco.com dispute and the airplane banner
>
> 50:23 · What Monaco does for sales teams
>
> 59:21 · Inside Monaco’s engineering team
>
> 1:01:40 · “You buy to learn, and you build to keep”
>
> 1:05:24 · Making repos agent-ready and closing the on-call loop
>
> 1:12:37 · When code review becomes the bottleneck
>
> 1:20:37 · Security, dependencies and permissions
>
> 1:30:13 · Background agents and Stripe’s Minions
>
> 1:34:16 · MCP portals and why infrastructure converges
>
> 1:41:22 · Building the software factory
>
> 1:45:24 · What work is left for developers?
>
> 1:52:16 · From personal adoption to team autonomy
>
> Transcript
>
> Download the complete text below. In the web edition, you can also read the transcript and click any timestamp to jump into the interview.
>
> transcript.txt152.95 KB • PLAIN File
>
> Automated transcript, aligned to the final episode. Timestamps open the corresponding moment on YouTube.
>
> 0:00 swyx · Intro — Okay, this is a pretty special episode because we're celebrating 1 million subscribers on the AI Engineer YouTube channel. So go over there and subscribe if you haven't heard about it. The guest is Mihail Eric, who is not only teaching The Modern Software Developer at Stanford, which is going viral right now, for basically covering all the AI-native development best practices, but also he is head of AI in Monaco. So he's not only a teacher, but he's a practitioner.
>
> 0:24 And those of you coming to AI Engineer CODE Summit next week, it's going to be the celebration of all the extreme progress that you've seen in coding in the last year. I'm excited about all the themes of fighting slop, of system one models, and of increasing your ambition for major rewrites of basically everything that you've seen in code. There's never been a more exciting time to be an AI engineer. And with one million AI engineers, I think it's just getting started.
>
> 0:49 So let's get into the interview.
>
> 0:51 Okay, we're in the studio with Mihail Eric, adjunct professor at Stanford and head of AI at Monaco. Welcome. Thank you. I'm glad to be here. You caught our attention because of your course that you are refreshing for the third time, third time?
>
> 1:03 Second time. Second time. Yep. The CS146, or 146S, The Modern Software Developer at Stanford.
>
> 1:09 Mihail Eric · EO Studio excerpt — This particular generation of junior developers, of junior engineers, the people that are now entering the workforce, will, I think, be the first kind of generation of that new shift.
>
> 1:18 And I looked at the syllabus and I was like, this is everything we cover. So every now and then I like to invite people like yourself who like you cover a broad range of topics and then we can sort of go topic by topic and Give people the state of the art on each of these things, which I assume you're doing with all your guests anyway For sure. Tell us the history of the course.
>
> 1:36 What made you want to Spring out CS 146? Yeah, is the second time it's being taught and I I taught it for the first time last fall, so fall 2025. This was pre 4.5, 4.6 days. even before fall 2025, the course had been about a year in the making. The genesis of the class was probably November of 2024. And I had sort of had this idea that we're seeing all this stuff happening in coding agents, and yes, they were an earlier version of the coding agents, but already it felt like there was something drastically changing in terms of how developers were doing their work, quickly we were getting work done, all that fun stuff.
>
> 2:08 And so at the time, was all just scattered blog posts, scattered things you could find online if you were trying to get into the methodology of how to do these things. And so I had this idea like, hey, well, is there a way to kind of structure a curriculum around this that's a little bit more formal?
>
> 2:23 Had the idea, and my alma mater is Stanford, and I always had this to go back and teach something and kind of pay it forward. I've always been very deep into education. And talked to Chip who also taught a class one of my good friends Chip Yen yeah Chip exactly spoke to her she had taught her I guess designing machine learning systems and so like asked her what that process was like and sort of you know took a lot of inspiration from how she designed the curriculum and thought about you know getting something the school put it together spent about nine to ten months this was now fall of 2024 through to like you know mid to late of 2025 got it through the committee,
>
> 2:58 made a case for the class to exist, you know, had to put together a proposal and everything. And that took me to fall 2025 when I heard it for the first time, was very well received. know, students were really interested in it. There was even, I guess, like a Business Insider article that was written about the class last year. And then, yeah, this year, a lot of things changed. I would say really agents, autonomous coding agents, really picked up in a way that we had not seen before.
>
> 3:23 So it felt like it was time to do this again, refresh things, and then here we are. Meanwhile, you're also head of AI at Monaco, which is also a very buzzy startup. Yes, yes. We are in the airwaves right now and having a fun time doing it. Yeah, so I do like that you're also, I guess, a practitioner. You guys are obviously implementing all this stuff at Monaco. Yeah. Any, I guess, principles or observations about just have changed from last year to this year at a high level?
>
> 3:53 Yeah, yeah. a ton. I think that when I reflect on what last year's version of the class was, I mean, coding agents had been around, but we were still in kind of that phase where companies were emerging that were tackling every single part of, like, the AIS DLC. There was, like, a coding agent for code review. There was a coding agent for spec design. There was a coding agent for SRE. And, you know, some of those, of course, some of those companies still exist.
>
> 4:16 But it felt like last year it was a lot more about a broad tour of here's everywhere you can use coding agents. And in a way, a lot of the curriculum last year was geared toward exposure. And this kind of survey, this kind of like odyssey of sorts through, hey, everything that you knew ASDLC is now changing because of AI. This year, I think there's some principles that are solidifying, right?
>
> 4:38 The idea of like very careful context engineering, the idea of like really thinking through sort of like design and architecture as a way of handling really complex tasks. And so the nature of my class is it's not intended for the like beginner programmer. That is not a replacement for like traditional computer science in the sense of like algorithms. And if in fact a lot of those classes are prereqs to what I'm doing here.
>
> 4:59 But I do know that you have a good foundation, going now toward applying that and sort of using those principles in production environments in the real world, that's something that I think is now at a place where, you know, at Monarcha we deal with massive code bases. You know, I help a lot of companies also with thinking through their massive code base designs and things like that. And so it's more of a practitioner's course for once the students, graduated or now entering the workforce, how to be the most productive members workforce.
>
> 5:25 You said you're passionate about education. I feel like students in that phase of being in college are in a pretty interesting spot. any advice and any take should people study computer science right now?
>
> 5:40 Is Claude code and codex all we need? Like, I want to, you know, hear your thoughts. Yeah, I, you know, there's a lot of anxiety from students, as you can probably imagine. And I think a lot of what I'm trying to communicate this time around is that the anxiety, a lot of it still is here. And there was anxiety last year as well. But I want to make the case that a well -trained AI native engineer, and I know that's like a buzzy word, but let's say we'll dive into maybe what aspects that are most interesting.
>
> 6:10 A well -trained and native engineer can be some of the most useful assets to any company around.
>
> 6:17 This is the first week of class, actually. Week one, first lecture, I'm like, hey, I really believe that every company needs you, but the floor is much higher. You're entering as your first job out of school, but it's not sufficient to just be an L3, in a Google term, if you're going to use that kind of leveling system there. You have to generally be better than almost at the senior level going to this.
>
> 6:39 So like what can we, how do we get there more quickly? Right? And so I'm trying to say that there is still a core bit of like foundational software engineering that is important to have. Some of these core values of sort of how software systems are built and the trade -offs of those systems. then beyond that we go and, know, that's where I think you as the humans should still be valuable rather than, and the rest of the implementation details you can kind of defer more often.
>
> 7:02 Hmm. Yeah. This is something I've said before which is almost like the controversy it's like the kind of thing you say to be spicy but I almost I do genuinely kind of believe it which is most students are cooked some of them are going to be super valuable I don't think it's a very popular thing Stanford's kids are going to be fine right they're from Stanford but like what happens to like the rest of America right that is an over question it's a weird situation because I feel like a lot of education is slow to move like I'm even curious in how do you determine where do you put the end date to curriculum in a course on it?
>
> 7:39 You're teaching a Stanford modern software. That's changing everything. You cheat. You just get the people from the coding agents to come and speak, right?
>
> 7:48 Oh, yeah. Have them be the, yeah. That's a funny. New old guest lectures. Well, yeah. I mean, that was, okay. So on the guest lectures point, I think that was, I mean, that was also last year. That was also the case. So that was by design because I, look, I came in, right, and I'm saying, I'm a practitioner, as you pointed out, swyx. Like, I'm a practitioner. I do this thing on my, you know, my day -to -day.
>
> 8:09 I design these systems. You know, build these things in Monaco have seen that many times before. And so that being said, don't want to claim that I have all the answers today. And that would be, like, very, you know, a lot of hubris to make that claim. So the structure of the class was always here's one practitioner's sort of aggregated set of insights from working in the field, from talking to a lot of people in the field.
>
> 8:33 But then there's people that are like literally on the frontier, you know, seeing things even beyond that and invite them to sort of put their proposals forward, their view of the world forward. And that's why the guest lecture is there. I think it's really impactful for students to see big names, people actually doing it, like hear from them directly, be able to ask them. Of course, you know, they want to intern, they want to get jobs.
>
> 8:56 It's good to have guest lecturers. No, I think what he's saying. So, OK, I'll sort of rephrase. No. So, OK, there, you know, we've also interviewed Ange, who teaches the Coachella course. Right. Right. Which is like, here's all the names. It's only the names. Right. Whereas like he's actually also producing, you know, here's cloud code in 200 lines of code. Right?
>
> 9:15 Which is, no one's telling you to do that. No one's gonna come speak to you to do that. But like, yeah, when you wanna teach fundamentals and a framework that you can use and working understanding, this is the kind of thing you do. That's right, that's right, yeah, yeah, exactly. And I do think that there's a balance for this kind of material, to your point, is that there is a, you can't, it's not 100 % solidified.
>
> 9:34 I mean, by design, it's a feature and maybe a bug of some kind, but a big portion of the curriculum did change from last year, right?
>
> 9:42 And so there's like a dynamism to the whole development of the curriculum. But I'm trying to at least put forward that there are some things that I believe are kind of sticking around. And yes, prompting coding agents, they've gotten smarter. What does that mean in terms of the new ways of dealing with them?
>
> 9:53 But then still, Boris is also going to know something that I don't know, right? So let's have him also come to the table and share his learnings. One of the fun things I noticed this time around is a good bit of the portion is on open source contributions. What's the thinking behind that?
>
> 10:11 You have people… Yeah, yeah. This is one of the things that I’m honestly kind of most proud of and most excited about. I mean, this is about to be week two of the class. Yeah, so this is the very gracious open-source partners that I spent the greater part of this summer just kind of talking to
>
> 10:28 and getting them kind of excited about and interested in sort of this offering. Basically the idea was, so last year when I taught the class,
>
> 10:34 we had like nine assignments, and then we had like a capstone open-ended project, right? The nine assignments were basically me sort of like coming up with these pedagogical exercises. Like, oh, here’s a repo. Use an AI code review tool to, you know, post a code review, and then see: why is it good? Why is it not good? So, relatively pedagogical, honestly pretty easy. I think for a lot of folks, they could just like one-shot it, and I thought, okay, this is not that helpful. At this point, agents are around. I mean, they have—every student that I surveyed, you know, on Tuesday, not a single person really types by hand anymore. They’re like, everyone’s using coding agents. And this is, you know, like all sophomores, juniors at Stanford.
>
> 11:10 Do you survey them? What's the market share? Was that like what, what tools they use? Okay. I haven't yet, that's a good call. You should do it. Yeah. Yeah. I will do that. Spicy, Stanford prefers. No, no. Well, I think university, I think they'd have some, like most of the providers have like an educational program, right?
>
> 11:27 I mean, yeah, they're very generous on plans for students. Right, right. So I think by default, even before the class, there's like, you know, Claude license, I imagine cursor license. There's like probably a cognition license as well. don't know, you might know that better than I do. But I was able to also just accrue on top of that was, hey, like if I don't want people to be bottlenecked by the $20 a month subscription.
>
> 11:49 I want you guys to go, if you want to token max something just to see what's possible, then you should. And so, I'll come back to the partners, but the additional thing I was able to accrue through instead of talking to folks was additional credits for students. So like factory is also getting involved, the cognition folks are getting involved. OpenAI as well. But anyway, so for the open source partners, I sort of was like, okay, one of the things I'm most concerned about when it comes to educating of students is that if everyone is saying, kind of to Suix's point, like they're cooked, like what's going to happen to them?
>
> 12:19 There's almost like this sense of them being left behind. And I think that mentorship is a really important piece of just up -leveling everyone and making sure that there isn't this massive gap that occurs between the senior people that have already been in the industry before coding agents and know what's up and they adopt coding agents and they become amazing. And then the juniors that are just like, okay, now what do we do?
>
> 12:39 So in a sense, one of the kind of goals was, hey, coding agents are really good. I want to put you guys in situations where you're dealing with complex code bases, large code bases at scale. We're going to work with someone like what I think are among the best like AI native repos, you know, that all do AI focused things or either coding agents themselves or building tools in the service of agents, you know, in the modern world.
>
> 13:00 I want you guys to get involved with these projects. I want part of your assignments to be actually contributing to these projects. In the course of being in all those projects, you will actually be talking to the maintainers. They will be reviewing your code. They will be helping you build mental models of good software. In that way, there's effectively this passing on of the guard of true good software design in a way that I don't think most students get the opportunity to do.
>
> 13:20 And then there's the benefit, of course, that I'm sure some of them will get poached and picked up as part of doing well in those assignments. Yeah. One of the interesting things, for what it's worth, get a bunch of hate if I I don't say this. I think you say cooked versus cracked for dramatic effect. know, like, it's just nice to state extremes. Sure, sure. Yeah. So maybe we should go into the sort of detail of the curriculum.
>
> 13:46 Yeah. Is there anything else you want to explore at the top level? I mean, like, that's very helpful. Yeah. All that's there. Okay. I have high -level questions about students using tools, best practices. Are you pro it?
>
> 13:59 Like individual tutors. I'm assuming this will also be picked up by students. So, you know, before we dive straight into the course, just anything you have guidance on there for. Like in terms of what. You said you're passionate about education, right?
>
> 14:13 Like, yeah, there's also a stigma of side is how do teachers, professors use it? And then how can students best use these tools? That's not just throw your assignments in. It can kind of one shot it. How do you still learn if you have anything there?
>
> 14:28 Yeah, yeah. And I think that there's, still have some assignments thrown in there, which I think are not intended to be the hardest things in the world, but are meant to be more about concepts, like more conceptual things. Like, you know, what does a skill mean?
>
> 14:39 Sort of like maybe more of the tactical of some of these tools, skills, like agent code bases, like agents MDs, things like that. So there's a certain amount of just, hey, if you haven't heard these terms, kind of get up to speed on them. I do think most of the learning, though, in terms of the of putting the tools to the test will happen both in the OSS and then also final project where it's very open -ended.
>
> 15:00 And they'll have to just kind of explore something interesting. Cool. Yeah. So maybe, yeah, I just want to talk about, well, let's go through one, two, three, four, uh, to 10. Yeah. Uh, and then we'll dive in deeper. So like breath first, basically. Sure. Sure. Yeah. So we start with internals of coding agents. That's right. You teach people how to write their own Claude Code clone. It's very helpful that it's not open source.
>
> 15:23 And then? Yeah. Yeah. So, uh, week one, it's all, uh, internals of harnesses, you know, kind of build a coding agent from scratch. Uh, week two is more, okay, now assume that there's, how do we start thinking about like, context engineering at scale. So beyond just vanilla prompting. And then I think coupled with that is just, in doing that, thinking about tool design, MCP. People, I think

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。