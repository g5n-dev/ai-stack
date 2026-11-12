---
title: "The attendee’s guide to the AWS re:Invent 2026 AI/ML track"
date: 2026-11-12T05:57:25+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "生成式 AI", "机器学习", "深度学习", "Prompt 工程", "Foundational (100)", "Uncategorized"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:ed2eca1a27f7ee922a02217cfcb3235b1621250b4841d9d365fd47d6a1e3079d"
source_payload_sha256: "sha256:4ec2d2a5d55c435aaf90d0c1a611a8a2c2994f1e32e76a437e373330f75a8ee4"
observation_id: obs_e3fb265c4a7f0c03e332381c674e35ece02aac3c1eec6df11ee65ed9b8e8bec6
event_id: evt_41d3f459fdf663c57644e0e2751ead5861c390fbdd58b9793d32be7cc3125a0a
revision_id: rev_7fc0f6c7e4d54d2501648fcece23aa3c2efe8e633afd0e9f06212fea2aa0a251
source_published_at: 2026-11-11T21:05:59Z
first_seen_at: 2026-11-11T22:10:22Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: true
source_truncation_reason: "crawler_feed_content_limit"
source_support: 1.0
source_title_chars_original: 58
interpretation_sha256: "sha256:c0bbd64d8d8543eb887fbf0a2c1e664096e9881e5d5d5b23df2ce0afb466949e"
description: "这是一份面向 AWS re:Invent 2026 AI/ML 专题的参会指南，介绍不同会话形式，并按 AI 芯片、模型训练与推理、智能体开发及管理等层级整理相关学习内容。内容还梳理了 AWS 从基础设施到智能体解决方案的 AI 技术栈。"
external_url: https://aws.amazon.com/blogs/machine-learning/the-attendees-guide-to-the-aws-reinvent-2026-ai-ml-track
parent_observation_id: null
last_seen_at: 2026-11-12T00:00:00Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/the-attendees-guide-to-the-aws-reinvent-2026-ai-ml-track](https://aws.amazon.com/blogs/machine-learning/the-attendees-guide-to-the-aws-reinvent-2026-ai-ml-track)
- **发布域名**: aws.amazon.com

## 要点解读

### 这是什么
这是一份面向 AWS re:Invent 2026 AI/ML 专题的参会指南，介绍不同会话形式，并按 AI 芯片、模型训练与推理、智能体开发及管理等层级整理相关学习内容。内容还梳理了 AWS 从基础设施到智能体解决方案的 AI 技术栈。

### 用在哪里
适合计划参加 re:Invent、观看线上直播或回放，并希望挑选 AWS AI/ML 会话的开发者和架构人员。也可用于了解 SageMaker AI、Amazon Bedrock、Trainium、NVIDIA GPU 和 AgentCore 等产品在 AWS AI 技术栈中的位置。

### 可以推断的
- 推测：初次接触 AWS AI 技术的参会者可优先从入门会话和概览开始，再按需要深入技术专题。
- 推测：希望评估 AWS AI 方案的团队，可借助该指南将芯片选型、模型服务、智能体构建、安全治理与成本控制等议题集中梳理。

## 来源摘要/节选

> From November 30th to December 4th, Amazon Web Services (AWS) will hold its annual premier learning event: re:Invent. At this event, attendees will become stronger and more proficient in various areas of AWS technology through a variety of experiences: keynotes given by AWS leaders, interactive working sessions led by AWS experts, and fun, immersive activities such as live entertainment and games at re:Play.
>
> There are over 2,000 learning sessions that focus on specific topics at various skill levels, and the AI/ML (AIM) track has more than 140 unique sessions for you to choose from. We’re here to help you identify the sessions that best fit your needs. Even if you can’t join in person, you can catch up with many of the sessions on demand and even watch the keynotes live.
>
> The basics: Session types
>
> If you can join us, then remember that we offer several types of sessions that can help maximize your learning in a variety of AWS topics.
>
> re:Invent attendees can choose to attend breakouts, chalk talks, builder sessions, workshops, and code talks. The breakout sessions are recorded and uploaded a few days after to the AWS Events YouTube channel, while the rest are live non-recorded interactive sessions. Here are the details for each session type:
>
> Breakout sessions: Attendees are in a lecture-style 60-minute informative session presented by AWS experts, customers, and partners.
>
> Chalk-talk sessions: Attendees interact with presenters, asking questions, and using a whiteboard in session.
>
> Builder sessions: Attendees participate in a one-hour session and build something.
>
> Workshop sessions: Attendees join a two-hour interactive session where you work in a small team to solve a real problem using AWS services.
>
> Code talk sessions: Attendees participate in engaging code-focused sessions where an expert leads a live coding session.
>
> Lightning talk sessions: Attendees watch a 20-minute demo dedicated to either a specific service or customer story (located in the Venetian Expo Hall or Wynn/Encore Upper Convention Promenade).
>
> With so many sessions to pick from, it helps to know how the pieces fit together. Here is how AWS thinks about its AI offerings, so you can decide where to begin and where to focus.
>
> The AWS AI stack overview and tie-in to re:Invent sessions
>
> AWS offers a comprehensive AI portfolio in the cloud. It covers everything from the physical infrastructure and AI chips that power AI workloads up through ready-to-use agentic solutions that teams can adopt today. Understanding how these services work together helps you navigate re:Invent and focus on the sessions most relevant to what you’re building.
>
> Figure 1: The AWS AI stack
>
> Global Infrastructure – It all starts with data centers designed and optimized for AI workloads. These facilities are built to handle the power, cooling, and networking demands that large AI training and inference jobs require.
>
> AI Chips – Running inside those data centers are two compute options: AWS Trainium, purpose-built for high-performance AI training and inference, and NVIDIA GPUs for teams that need GPU-based acceleration. Customers choose based on their workload, performance requirements, and cost targets.
>
> Data Foundation – AI is only as good as the data behind it. AWS Context connects your data across storage, databases, analytics, and search services, giving models and agents access to the right information at the right time.
>
> Models, Training, and Inferencing – This is where models get built, trained, fine-tuned, and served. Amazon Bedrock gives you managed access to hundreds of leading models from multiple providers through a unified API. Amazon SageMaker AI gives you full control to train, fine-tune, and deploy custom models on dedicated infrastructure. Many customers use both depending on the workload.
>
> Agent Development and Management – Amazon Bedrock AgentCore is where you build, deploy, and manage AI agents. It supports any model or provider mix, including models from both Amazon Bedrock and SageMaker AI, so teams can design agents that pick the right model for each task without being locked into a single provider.
>
> Agentic Solutions – At the top of the stack sit purpose-built agents that are ready to use. Kiro helps developers ship correctly the first time with spec-driven development. AWS Quick connects your applications, tools, and data into a personal knowledge graph that learns how you work. Amazon Connect delivers agents for customer experience, hiring, supply chain, and healthcare. AWS Marketplace gives you access to partner-built AI solutions.
>
> Security, Governance, and Cost Optimization run across every layer of the AI stack. They are built into the foundation, with hardware-level isolation at the chip layer and controls that enforce what agents can access and do.
>
> The AI-focused sessions at re:Invent span the full stack. Whether you’re evaluating AI chips, serving models in production, building custom models, deploying agents, or adopting ready-to-use solutions, this guide helps you find the sessions that matter most. Use it to build a smarter re:Invent schedule.
>
> The artificial intelligence and machine learning (AI/ML) track primarily focuses on three core layers of this stack: AI chips, models, training, and inference, and agent development and management, with security, governance, and cost optimization woven throughout. The following sections start at the chip layer and move up through models and agents. Then come sessions that tie the stack together. The guide ends with other relevant topics, such as sustainability and infrastructure where you run your AI workloads. Within each section, sessions for newcomers come first and technical deep dives come last.
>
> Want to skip ahead? Jump straight to the topic you care about:
>
> AWS AI platform sessions
>
> AI chips: NVIDIA GPUs and AWS Trainium
>
> Amazon SageMaker AI sessions
>
> Build and run AI applications and agents with Amazon Bedrock
>
> Build AI that works with documents, voice, and images
>
> Building trust in AI agents
>
> Other topics
>
> Plan your re:Invent
>
> AWS AI platform sessions
>
> These sessions cover the core AWS AI services together: Amazon Bedrock, Amazon SageMaker AI, Amazon Bedrock AgentCore, and the AI chips that they run on. They help you make architecture choices that still work as your usage grows.
>
> New to AI on AWS? Start with AIM204. It walks through the whole stack. You will see Trainium and Graviton chips, model inference on Amazon Bedrock and SageMaker AI, and production agents on AgentCore. If you’re already building, try AIM364. It helps you choose between Amazon Bedrock and SageMaker AI, and shows when to use both. The example is a real agentic coding app that runs on AgentCore.
>
> Other sessions dig into specific production problems. If you own data strategy, attend AIM363. This chalk talk shows how governed data products feed customization, inference, and agents. It also explains why cost levers like prompt caching, distillation, and batch inference work better on clean data. Need to prove the value of AI? AIM319 looks past cost to business impact. A live demo across the AI stack shows how to measure return on investment (ROI) and compare cost per outcome.
>
> Experienced builders should look at AIM443. In this 400-level chalk talk, you build a training pipeline on Amazon SageMaker HyperPod. You bring in company data and keep governance in place. Then you deploy the same model to Amazon Bedrock for inference or to AgentCore for agents.
>
> AI chips: NVIDIA GPUs and AWS Trainium
>
> AWS gives you two main choices of AI chips for training and inference: NVIDIA GPUs and AWS Trainium. Start with the one you use today, then explore the other.
>
> NVIDIA GPU sessions
>
> AWS offers a wide range of Amazon Elastic Compute Cloud (Amazon EC2) instances with NVIDIA GPUs. These sessions show how to run AI training and inference on them securely and reliably.
>
> Start with AIM2210 for the latest on GPU instances. In AIM3301, a customer shares how it gets the most from its GPU capacity by optimizing GPU scheduling. AIM392 explains when EC2 G7e and G7 instances are a good fit in place of P-series instances. Want to tune AI infrastructure with self-managed agents? Join AIM346.
>
> If you prefer hands-on learning, try AIM345 on disaggregated inference serving. In AIM344, you find the cause of real GPU cluster failures and how to recover from them. In the AIM347 workshop, you can practice GPU performance engineering.
>
> For data processing, see AIM3312. It shows how Amazon EMR with the NVIDIA cuDF plugin for Apache Spark runs jobs up to 3.7x faster on EC2 G7 instances than on comparable CPU instances without code change. The session also covers DuckDB on GPUs.
>
> AWS Trainium sessions
>
> AWS Trainium is a family of AI chips purpose-built for next-generation deep learning training and inference. It delivers high performance at lower cost. Trainium runs on AWS Neuron, the software stack that connects Trainium to familiar frameworks like PyTorch, so teams build without rewrites. Customers who adopt Trainium-based Amazon EC2 instances may see better price performance than comparable instances.
>
> If you’re new to Trainium, AIM211 is the place to start. It traces the full stack, beginning with the silicon and working up to the application. For the latest system, AIM310 shows how Trainium3 and the Trn3 UltraServer keep large mixture-of-experts models performant. If you’re still evaluating transitioning to Trainium3, the AIM2213 panel gathers four AI leaders who have already shipped real products on Trainium.
>
> Several sessions are built around specific roles. Scientists and researchers who live in PyTorch should bring their questions to AIM339, a nanochat code talk, before getting hands-on in the AIM334 distributed-training workshop. ML engineers and developers can architect a production AI assistant with Hugging Face models in AIM349, and get hands-on with inference scaling in the AIM326 workshop. Performance engineers chasing peak throughput will want AIM329 on agentic optimization loops, followed by INV511, a 500-level look inside the Neuron Kernel Interface for serious kernel designers. If you want to run Trainium on Amazon Elastic Kubernetes Service (Amazon EKS), AIM311 whiteboards a resiliency stack that holds up across deployments as large as twenty thousand accelerators. If you deploy through SageMaker AI instead, see the SageMaker AI section.
>
> For those who want to go further, world models are an emerging class that power simulation in gaming, robotics, and autonomous driving. AIM323 is a good starting point and covers serving world models with native PyTorch. From there, pick a hands-on path. In AIM304 you will deploy and optimize a real-time video world model using agentic Neuron workflows, while in AIM305 you will train vision-language-action models for physical AI. Both are builders’ sessions.
>
> Amazon SageMaker AI sessions
>
> Amazon SageMaker AI is the AWS service for customizing and deploying your own models. It handles the whole model lifecycle in one place. You can prepare data and customize a model on serverless compute. When you need more power, you can grow training jobs to thousands of accelerators. After your model is ready, deploy it on SageMaker inference endpoints or SageMaker HyperPod. You keep the model weights, and you decide where your models run.
>
> New to SageMaker AI? Start with AIM342. It shows how to build, customize, and deploy models with one service. Between sessions, stop by the Builder’s Hub and test your skills in one of three contests. Fine tune an agent, field a team in the Agentic Football Cup, or teach a robot a new task. For the latest on robotics, world models, and physical AI, hear a panel of builders in AIM2215. Still picking a model or learning to write evaluations? AIM2205 shows how to build evaluations on your own data. It also shows how to turn business knowledge into models that cost less to run.
>
> Customization starts with data. The AIM434 workshop shows how to prepare datasets for custom models. Next, AIM362 helps you pick the right compute for customization. Then fine-tune and deploy a large language model (LLM) in a few hours in AIM402. Customers will share their lessons too. In AIM393, Salesforce explains how it built and served its Koa models with open weights. Intuit tells its story in AIM361. If you build agents, AIM325 shows how to fine-tune agents that reason, using multi-turn reinforcement learning. The AIM456 workshop links evaluation, fine-tuning, and reinforcement learning into one pipeline. It spans SageMaker AI and Amazon Bedrock.
>
> And if you’re building domain-specific AI, you should join AIM2205. Learn how to test models on your own data and weigh quality against cost. The session also covers when customizing a model is worth it. In AIM398, watch the team behind Forge whiteboard a fast path to building tailored AI solutions, drawing on their end-to-end customer engagements. They will cover everything from setting the right evaluations and optimizing prompts, context, and inference serving to choosing a customization approach that modifies model weights during pre- or post-training. When you’re ready to grow training and inference, SageMaker HyperPod helps you get more from every GPU hour. Teams use it for specialized work like biology foundation models (FMs), physical AI, world models, and sovereign AI. Start with customers who push the limits. In AIM343, Tencent Games explains how it scaled to 1,000 GPUs. In AIM433, HUMAIN shows how it keeps GPU use high for both training and inference.
>
> For hands-on practice, build foundation model pipelines with Amazon EKS in AIM406, or tune AI pipelines with Ray in the AIM403 builders’ session. The AIM435 code talk teaches policy distillation, which trains a small model from a larger one. Physical AI teams can join the AIM318 workshop. It shows how to keep vision-language model training running when nodes fail. Robotics and autonomous vehicle teams can build a physical AI model factory on SageMaker HyperPod in AIM413.
>
> When it’s time to serve your models, two 200-level talks show inference in production. In AIM213, CrowdStrike explains how it runs LLM inference for threat detection with less operational work. In AIM214, Vanguard shares how it trains and serves custom LLMs on SageMaker HyperPod. To build agents on open-weight models with fast inference, try AIM405. To create fast, resilient inference endpoints, join the AIM404 workshop. Platform teams can practice governed ModelOps in the AIM348 builders’ session. They can also add observability with managed MLflow in the AIM408 workshop.
>
> Build and run AI applications and agents with Amazon Bedrock
>
> The model and inference approach you choose shapes what your AI app can do for users. Amazon Bedrock gives you a wide choice of models and helps you pick the right one for each task. It gives you the performance, security, and cost control to run AI apps in production. Some apps need to use tools and data, remember context, and act for you. For those, Amazon Bedrock AgentCore helps you build, connect, and improve agents.
>
> New to Amazon Bedrock? Start with AIM220. It covers what’s new in models, inference, security, and cost management. Then build and deploy your first Amazon Bedrock app in the hands-on AIM317 workshop.
>
> Next, think about the kind of workload you need to serve. A customer support app may need fast answers. A large document processing job may care more about cost and can wait for results. AIM448 helps you pick the Amazon Bedrock inference option that fits your needs. It weighs performance, capacity, cost, and data residency. If your app must reason across your company’s information, attend AIM308. In this session, you’ll build a knowledge assistant that finds answers across documents, images, structured data, and the links between them.
>
> Your inference plan also needs to stay affordable as usage grows. AIM437 helps you decide when to cache repeated context, route requests between models, or move work to batch inference. Model choice matters too. The newest model isn’t always the right one, and switching can change quality, speed, cost, and behavior. AIM438 shows how to test candidate models on your own use cases so you can switch with confidence. After your app is live, AIM374 covers the metrics, alarms, and operating habits to bring into production. Systems specialists can go deeper in INV517. This 500-level session looks at the scheduling and parallelism methods behind efficient large-model inference.
>
> If you want to build an agent, start with the full production picture rather than building infrastructure one piece at a time. AIM212 introduces the complete AgentCore lifecycle. Nasdaq also shares how it runs agents in a regulated industry. For a hands-on path, try AIM439. You start with a basic customer support agent. Then you add memory, tool access, identity, policies, observability, and evaluation until it’s ready for production. Ready to design a multi-agent system? AIM407 uses Strands Agents to coordinate specialized agents. You share state, handle failures, and deploy the result to AgentCore.
>
> After your agent is running, look at what happens under the hood. Each planning step, retrieval, tool call, and retry can add another model call. That changes cost, speed, and reliability. AIM429 connects agent design to inference behavior. It helps you think through context, harnesses, goals, and when an agent should stop. Developers who want to see these tradeoffs in code should follow it with AIM454. That session builds function calling, multi-step reasoning, and retrieval live.
>
> The stakes rise as agents serve more users and reach more systems. Bring your scaling questions to AIM436, where you work through traffic spikes, tool failures, model timeouts, and multi-tenancy. Platform teams that manage agents across a company should attend AIM303. It covers how to find agents, control tool access, manage identity, and see your whole fleet. If your priority is securing every step between a user request and an agent action, pair it with AIM370. Then use AIM440 to turn production traces and evaluations into a steady way to improve agent quality.
>
> Finally, pick a session that looks like the work you want an agent to do. AIM340 follows PepsiCo’s conversational ordering agent. It shows how memory, company APIs, and controls work together in a customer-facing workflow. AIM369 focuses on agents that respond to business events and run processes to the end, with human approval where needed. Software teams can get hands-on in AIM416. There, coding agents move off the laptop and run long-lived, parallel workflows on AgentCore.
>
> Build AI that works with documents, voice, and images
>
> AI apps often need to handle more than text. These sessions show how to build those skills on AWS. They add grounding, evaluation, and verification so your app holds up in real use. For document processing, start with AIM216 on Amazon Textract. Then, in AIM442, build a pipeline that turns documents into structured data you can check. Building voice apps? AIM217 introduces Amazon Polly and Amazon Transcribe, and AIM218 explores conversational AI with Amazon Nova Sonic. Go deeper with the AIM356 code talk, or build and deploy a voice agent in AIM352.
>
> Build cross-modal search in AIM357. To improve quality, add web grounding in AIM350 and automated evaluation in AIM351. You can also explore identity verification with Amazon Rekognition in AIM355.
>
> Building trust in AI agents
>
> AI agents now do real work, like approving claims, issuing refunds, and acting on customer data. Teams need a way to trust what those agents do and prove it to others. That starts with responsible AI, which helps organizations make careful choices about how AI systems are designed, built, and run. AWS builds on that with Trust in Depth. It’s an approach for giving agents more freedom without losing control.
>
> If you’re new to AI trust, start with the AIM2216 panel. It covers how to build confidence at each stage of an agent’s life. Topics include keeping an agent limited to its job and seeing exactly what it did. To see responsible AI governance in practice, attend AIM391. It shows how John Deere used AI Risk Intelligence to replace periodic manual reviews with continuous, automated governance. The change cut assessment time by more than 30 percent.
>
> Several sessions are built for specific roles. Developers can join the AIM336 workshop to audit a multi-agent claims system for responsible AI gaps. Then they fix what they find and write a report backed by evidence. Risk, compliance, and data science teams can join AIM332. This chalk talk covers testing whether agents treat people fairly when they approve loans or issue refunds. You learn how to choose fairness metrics and catch bias in outcomes that affect people’s lives. Do your agents decide things like insurance eligibility? The AIM335 workshop shows how to turn the rules behind those decisions into Automated Reasoning checks in Amazon Bedrock Guardrails. Each decision can then be proven correct and audited.
>
> For a deeper look at the science, several expert sessions cover automated reasoning. INV508 shows how subject matter experts can turn legal and regulatory policies into rules a machine can check. No coding is needed, and those rules then serve as AI guardrails. INV526 looks at what can be proven about agent behavior today, and where the limits are. The AIM451 chalk talk shows how to enforce rules that agents can’t get around. It also shows how to keep people involved in decisions machines shouldn’t make alone.
>
> Other topics
>
> A few more tracks round out your re:Invent planning, from sustainability to where you run your workloads.
>
> AWS Sustainability
>
> AWS is continuously innovating across its data centers, chips, and AI services to be more efficient and sustainable. AWS also gives you the data and tools to measure, track, and reduce the environmental impact of your own cloud and AI workloads running on AWS. These sessions discuss how we’re making our infrastructure more efficient and show how to act on sustainability data while still meeting your business goals. For the latest on the AWS Sustainability service, attend AIM201. This lightning talk covers new impact areas beyond carbon, more detailed data, and API access. In AIM205, learn how AWS makes AI infrastructure more sustainable. It uses hardware with low embodied carbon, energy-efficient custom chips, and data centers tuned by machine learning (ML). Want to understand the method behind your carbon data? Join the AIM321 chalk talk. It shows how to use that data to build AI workloads with a smaller footprint, which often cost less too.
>
> If you prefer hands-on learning, try AIM320. You build a generative AI pipeline with Amazon Bedrock that turns messy company data into sustainability insights. The session is based on how AWS handles life cycle assessment across its data centers. To go deeper, join AIM412. It uses Amazon Neptune and an Amazon Bedrock agent to map how stakeholders depend on each other. You then test ways to cut carbon on a knowledge graph.
>
> Local Zones and AWS AI Factories
>
> As teams move AI into production, where a workload runs matters as much as how it’s built. Large training jobs, fine-tuning, and real-time inference each need different things from infrastructure. AWS gives you several places to run them: AWS Regions, AWS Local Zones, AWS Dedicated Local Zones, AWS AI Factories, and AWS Outposts. Start with HMC303. It compares these options on the four factors that drive the choice: latency, data sovereignty, compute density, and scale. Databricks shares how it uses GPU capacity in select Local Zones. T-Mobile covers latency-sensitive distributed inference.
>
> In HMC307, see how Netflix supports its visual effects and animation teams from the Los Angeles Local Zone. Netflix starts Amazon EC2 G7e instances with NVIDIA RTX PRO 6000 GPUs just in time. That way, artists get ComfyUI environments when they need them.
>
> Two hands-on workshops take different paths to building agents at the edge. HMC402 takes the managed route. You connect Amazon Bedrock AgentCore agents in an AWS Region to tools and agents in hybrid and edge locations. You use Model Context Protocol (MCP) and agent-to-agent (A2A) communication. HMC403 takes the self-managed path. You design, set up, and tune your own agents across Local Zones and Outposts. Then learn how to orchestrate

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。