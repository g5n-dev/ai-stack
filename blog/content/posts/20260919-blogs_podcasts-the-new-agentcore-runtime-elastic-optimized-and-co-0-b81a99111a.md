---
title: "The new AgentCore runtime: Elastic, optimized, and consistently fast starts"
date: 2026-09-19T18:59:25+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "机器学习", "Amazon Bedrock AgentCore", "Announcements", "Expert (400)", "博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:9b9d05d02154ce9c6d42e65b2a846f3ca8c8cc8e079bf38d71766fa8157e1691"
source_payload_sha256: "sha256:cb24be3fc8047ed8e8757a9b305650d1b07451227603fb0e784e16c09978b906"
observation_id: obs_b81a99111a5a86711c99d41ed073572ee8ddebce77cc7e3eead3a07ff5c3a222
event_id: evt_deb87cdd51a8b0ba0abfeb62a7a7c677e8f90cf2c8262f7030a4120592f3c6c4
revision_id: rev_08df231fea8b631e6173985248634920174cfd9bb5e1ffe8bed6dab210a1c294
source_published_at: 2026-09-18T15:31:34Z
first_seen_at: 2026-09-19T11:09:50Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 75
interpretation_sha256: "sha256:f1ad8a8925521bc97c0ef6b29793148deec5ec262fe94da826f0e3d16ad5d77a"
description: "这是一套面向构建和运行 AI 代理的托管计算层，旨在通过在会话结束后立即释放不再使用的内存，并保持容器启动时间不受并发量或镜像大小的影响，实现弹性、优化的运行时性能。"
external_url: https://aws.amazon.com/blogs/machine-learning/the-new-agentcore-runtime-elastic-optimized-and-consistently-fast-starts
parent_observation_id: null
last_seen_at: 2026-09-21T00:00:00Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/the-new-agentcore-runtime-elastic-optimized-and-consistently-fast-starts](https://aws.amazon.com/blogs/machine-learning/the-new-agentcore-runtime-elastic-optimized-and-consistently-fast-starts)
- **发布域名**: aws.amazon.com

## 要点解读

### 这是什么
这是一套面向构建和运行 AI 代理的托管计算层，旨在通过在会话结束后立即释放不再使用的内存，并保持容器启动时间不受并发量或镜像大小的影响，实现弹性、优化的运行时性能。

### 用在哪里
适用于需要在生产环境中长时间运行、并发量波动大且对成本敏感的 AI 代理开发团队，帮助他们省去自行维护预留资源和优化启动延迟的繁琐工作。

### 可以推断的
推测：该改进能够在会话频繁出现突发流量时，显著降低因峰值内存占用而产生的费用。  
推测：对于交互式代理，稳定的启动时延有助提升用户感知的响应速度。

## 来源摘要/节选

> Agents are no longer experiments. They process claims, write and review code, coordinate across systems, and run for hours without supervision. As agents take on more complex, longer-running work, the infrastructure underneath them must evolve just as fast.
>
> We built Amazon Bedrock AgentCore to help developers build, connect, and optimize agents securely at scale. AgentCore runtime, a capability of Amazon Bedrock AgentCore, is the managed compute layer that gives developers a fully managed environment to deploy and run agents without building or maintaining infrastructure.
>
> Since launch, thousands of teams have used it to run production agents. Every conversation with those teams teaches us something about what agents need next: faster responsiveness as workloads scale, finer control over resource allocation, and economics that track actual usage precisely.
>
> Today, we are announcing the new AgentCore runtime, purpose-built for the speed, flexibility, and cost efficiency that production agents demand.
>
> It brings better memory management, reclaiming memory as a session releases it instead of holding it at the peak. It also delivers consistent cold start times regardless of container size or agent concurrency. You get the serverless model you already liked, now more elastic. Memory is released back the instant a session ends, startup times stay consistent regardless of size or concurrency, and the bill tracks the work your agent does.
>
> From conversation to workload
>
> Many agents started as chat bots: you asked, it answered, and the exchange ended in seconds. Then came coding agents that work for minutes to hours, holding context across many steps, running while you watch or step away. Now agents are becoming ambient, always on, triggered by events, running unattended, surfacing only when a job finishes or hits a decision that needs a person. And there are far more of them: no longer novelties but running everywhere. They are embedded in products, behind everyday features, and increasingly launched by other agents.
>
> The first version of AgentCore runtime built a strong foundation for this spectrum of agents: serverless, session isolation, scale to zero, and pay only for what you use. Today’s launch of the new runtime extends that foundation across the full spectrum, staying fast and consistent for interactive agents, and durable and affordable for long-running, more autonomous agents.
>
> What AgentCore runtime provides
>
> With AgentCore runtime, you can focus on the agent instead of worrying about the scalable infrastructure needed underneath it. Two things make that possible, and they’re the reasons customers reach for it:
>
> You pay only for what you consume, and not for idle CPU waiting for I/O. Billing follows resource usage, so there’s no standing charge for capacity you provisioned “just in case.”
>
> The platform scales all the way down to zero. When an agent isn’t handling work, there’s nothing running and nothing to pay for. When work arrives, the platform gets you the capacity you need.
>
> Together they make it cheap to keep many agents idle most of the time and even cheap to run one that stays busy. The consumption model bends to the workload instead of forcing the workload to bend to it.
>
> As agents move from short question-and-answer sessions to ambient, always-on work, that same model runs into two challenges.
>
> Memory is expensive, and today you pay the peak. A session holds on to memory from the moment it allocates it until the session ends, because nothing reclaims it along the way. This works when the allocated memory is used to serve subsequent resources without incurring the latency to fetch it again. However, a long-running or bursty agent keeps paying for its high point the whole time it runs, well after it has stopped using that memory. For an agent that spikes now and then but sits idle most of the day, that is the gap between paying for the peak around the clock and paying for the real usage.
>
> Startup times vary. Every new session has to start before it can do any work, so fast, predictable startup is central to a good experience. It matters most when a person is waiting on an agent that paused for input and needs to resume. The catch is the hardware-enforced isolation these sessions depend on: a session that lands on an already-initialized environment starts in under 100 milliseconds, but keeping environments hot enough to guarantee that means holding compute in reserve. So most sessions begin with a cold start: booting a fresh environment, pulling the image, and initializing the agent before the first request runs. That latency penalty grows with image size and concurrency, and it’s worst under bursty traffic, exactly when most sessions arrive and the fewest ready environments remain. That inconsistency is what a waiting user feels.
>
> The workarounds are heavy. To cover both challenges, customers often build the machinery themselves: holding spare environments ready so requests avoid a cold start, optimizing memory allocation, and tearing it all down again to keep the bill in check. Keeping capacity ready ahead of demand is costly and complex for anyone to run. It reserves scarce compute whether or not that compute is working, and it still gives way when a burst outruns what was set aside. This is undifferentiated work, and none of it is the agent itself.
>
> Benefits of the new AgentCore runtime
>
> The enhanced AgentCore runtime takes care of both challenges for you, starting with lower memory consumption tracked to what you use. The new runtime now starts each session from a small, efficient memory profile rather than a full provisioned footprint. Additional memory is allocated and paged in on demand as the workload needs it. Based on an analysis of allocation patterns across billions of sessions, we tuned the new runtime to reclaim memory when it goes cold and is unlikely to be accessed again. It no longer holds that memory until the session ends. With the original runtime, allocated memory remained held even if it wasn’t used by subsequent requests, so the usage tracked the high watermark. With the new runtime, memory that is released or goes cold is reclaimed, and the bill tracks those changes over the lifetime of the session.
>
> Figure 1: Session memory usage for the original runtime compared to the new runtime
>
> Faster, more consistent cold starts come as a direct benefit of smaller profiles at startup. The enhanced runtime prepares the environment once, snapshots it, and restores that snapshot for each new instance. Because the snapshot stays small and consistent, so do the starts, no matter the image size or how much concurrency you run. Rather than repeating the boot-and-initialize work on every cold start, the platform restores an environment that is already up. The runtime now delivers consistent starts in a tight, predictable range.
>
> What we measured. To isolate what the platform itself adds to a cold start, we tested an empty echo agent that returns its input and calls no model and no tools. The timing reflects the runtime’s start path rather than any application work. A Python client on an Amazon Elastic Compute Cloud (Amazon EC2) instance in us-west-2 called agents in us-east-1 over the public internet with no virtual private cloud (VPC) peering, using the boto3 SDK. These are client-side numbers, so each one includes the round trip between the two AWS Regions on top of the platform’s own start time. We sent 5,000 cold invocations per agent across both versions and five image sizes, within default account quotas.
>
> Measured this way, the new runtime delivers a P75 cold start latency of about 2 seconds from a 200 MB image all the way to 2 GB, because image size has no effect on it. The original runtime’s latency, by contrast, rises with image size, from roughly 5.4 seconds to nearly 30 seconds.
>
> To put this latency in perspective, it helps to separate cold start latency from what a user waits on. Start time is how long it takes to get a ready environment before your agent code handles its first request. It is not the time the agent spends working. In a production agent, most of the wall-clock time a user experiences comes from the agent loop and its model calls, often several seconds each. In our echo test, the agent’s own code ran in about 34 milliseconds at P75, so nearly everything here is platform start time. The new runtime makes the platform’s portion of the start time fast and predictable, which matters most when a person is waiting on an interactive agent.
>
> A practical tip for interactive agents. You can hide the start time almost entirely by beginning the session as soon as the user engages, for example when they open a chat, even before they type in the input box, rather than waiting for them to submit. The session warms while they are greeted and while they type their first request, so by the time they send that message, the environment is ready.
>
> Figure 2: P75 cold start latency across image sizes for the original and new runtime
>
> How the new runtime works
>
> The next generation of the runtime reworks how sessions use memory, how agents load, and what you pay for.
>
> Page memory in on demand and reclaim it when it is freed. Instead of holding on to a session’s peak memory after it’s allocated, the new runtime now backs the session with a smaller resident footprint and brings in more memory as the workload touches it. When your agent lets memory go, by releasing per-request buffers and by letting cached data expire between requests, the platform takes it back rather than letting it stay claimed until the session ends.
>
> Load the agent once, then snapshot it. When you create or update an instance of the new runtime, AgentCore launches your container and waits for it to report healthy, then captures a snapshot of the running environment. By that point, your one-time initialization has already run, so work such as loading model artifacts and fetching static config is baked into the snapshot. Every new instance then starts by restoring that snapshot rather than initializing from scratch. The expensive startup work is paid once, and each instance inherits it instantly.
>
> Keep the snapshot small and its size steady. A naive snapshot of a running process captures far more than a restored instance needs, including caches and transient memory that pad the snapshot and make restore time grow with image size. The new runtime strips that excess, so the snapshot holds only the working state an instance needs to resume, not its full resident footprint. The result is a snapshot whose size stays roughly flat as the container image grows, and that is what holds restore latency steady across a wide range of image sizes.
>
> Higher rate, lower bill. The new runtime bills you for the memory that  your agent uses, loaded on demand and reclaimed when idle, not for holding your whole container image in memory all session. You pay a higher rate but on far fewer GB-hours, and for most agents the footprint drops more than the rate rises, so the bill goes down.
>
> What’s next (coming soon)
>
> Beyond what we shipped today, several capabilities are on the way to give you more choice over pricing, compute, compatibility, and control.
>
> Committed baseline discounts. Today’s consumption-based pricing stays and works well for spiky and scale-to-zero workloads. Alongside it, the new runtime will add a baseline pricing option: you reserve a memory floor for a session and burst above it on demand. Baseline pricing suits steady, always-active agent sessions that want predictable cost, while consumption pricing continues to provide greater elasticity.
>
> Larger compute and storage. Expand your agent’s environment with more RAM, vCPU, and session storage.
>
> x86 support. Run the agent, tool, or environment you already have with x86 microVMs. Teams whose code or dependencies target x86 can move an agent, a tool, or an execution environment to AgentCore as-is.
>
> Greater lifecycle control. Suspend and resume sessions with memory snapshotting. Attach to runtime hooks to serialize state before an active session terminates, so sessions can resume indefinitely.
>
> Scoped identity for unattended agents. Unattended agents raise a question a chat turn never did: what is this agent allowed to do when no one is watching it act? Session context keys will give each session its own scoped identity, so an unattended agent, tool, or environment acts with exactly the permissions defined for it and nothing more.
>
> Getting started
>
> To get started with the new runtime, set the platformVersion parameter to V2 when you create or update a runtime. See the AgentCore Developer Guide for more details on using the runtime.
>
> You can find samples in the AgentCore GitHub samples repo. An accompanying load test example shows the new runtime’s consistent cold start latency in your own AWS account.
>
> About the authors
>
> Evandro Franco
>
> Evandro is a Sr. Data Scientist working on Amazon Web Services. He is part of the Global GTM team that helps AWS customers overcome business challenges related to AI/ML on top of AWS, mainly on Amazon Bedrock AgentCore and Strands Agents. He has more than 18 years of experience working with technology, from software development, infrastructure, serverless, to machine learning. In his free time, Evandro enjoys playing with his son, mainly building some funny Lego bricks.
>
> Mark Roy
>
> Mark is a Principal AI Architect for AWS, helping customers design and build agentic AI solutions. Mark’s work covers a wide range of use cases, with a primary interest in AI agents at enterprise scale. He is a worldwide tech lead for Agentic AI, including Bedrock AgentCore. Mark has helped companies in insurance, financial services, media and entertainment, healthcare, utilities, and manufacturing. Prior to joining AWS, Mark was an architect, developer, and technology leader for over 25 years, including 19 years in financial services.
>
> Shishir Bharathi
>
> Shishir is a Principal Engineer in AWS, currently building Amazon Bedrock AgentCore Runtime. His experience spans the full agentic stack, drawing on deep work across AI systems, from developing conversational agents in Alexa and LLM post-training and customization to recommender systems in Prime Video. He now focuses on making the infrastructure that powers production agentic systems more reliable, efficient, and scalable.
>
> Abhishek Singh
>
> Abhishek is a Senior Software Development Engineer at AWS on the Bedrock AgentCore team. He is the tech lead for AgentCore Runtime and has led the design and development of multiple AgentCore services from the ground up, including Runtime, Code Interpreter, and Browser. He has 12 years of experience building distributed systems, previously on Bedrock and SageMaker. Outside of work, he likes playing soccer and tennis, and spending quality time with family.
>
> Aniketh Manjunath
>
> Aniketh is a Software Development Engineer at AWS on the Amazon Bedrock AgentCore team, working on AgentCore Runtime with a focus on the performance and efficiency of agent execution at scale. He has over five years of experience building large-scale distributed systems at Amazon, previously on Amazon SageMaker, and now works on making the infrastructure behind production agentic systems faster and more reliable as it scales to meet growing demand. Outside of work, he enjoys hiking, watching movies, and playing cricket.
>
> Rahul Nama
>
> Rahul is a Software Development Engineer at AWS, where he builds AgentCore Runtime systems that enable AI agents to run reliably at scale. He is passionate about building distributed systems and optimizing infrastructure to simplify the lifecycle of AI agents. Outside of work, he plays semi professional cricket and enjoys exploring the outdoors.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。