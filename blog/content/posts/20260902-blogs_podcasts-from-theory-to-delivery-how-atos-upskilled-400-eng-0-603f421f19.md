---
title: "From theory to delivery: How Atos upskilled 400 engineers in agentic AI"
date: 2026-09-02T22:32:34+08:00
draft: false
entry_kind: "auto"
tags: ["AI Agent", "Prompt 工程", "Amazon Bedrock", "Amazon SageMaker", "Customer Solutions", "博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:794de8d5fe55e5f037a8ef786c74d97861a03320f661a8ed7c310540d987588a"
source_payload_sha256: "sha256:92acae19b32b70246eff18dd3db9e9e417b715b933996e69aa02a5b41638a254"
observation_id: obs_603f421f19ad47cccd1e570b55e6dc8715a4283bbca07dd4ea5dc7a7cd1ab675
event_id: evt_aa845b4dd46ae9c95177c893f42fa13388ff8fb4d4e96429de3e5534b4dd5a2c
revision_id: rev_e35b126e628d8b8fa0a2fc9a6a9790aab076643549ce7d74eee7017a7890025e
source_published_at: 2026-09-01T16:17:54Z
first_seen_at: 2026-09-02T14:29:28.254034Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 71
description: "当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。"
external_url: https://aws.amazon.com/blogs/machine-learning/from-theory-to-delivery-how-atos-upskilled-400-engineers-in-agentic-ai
parent_observation_id: null
last_seen_at: 2026-09-02T14:29:28.254034Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/from-theory-to-delivery-how-atos-upskilled-400-engineers-in-agentic-ai](https://aws.amazon.com/blogs/machine-learning/from-theory-to-delivery-how-atos-upskilled-400-engineers-in-agentic-ai)
- **发布域名**: aws.amazon.com

## 来源摘要/节选

> When Atos set out to upskill 400 engineers from theory to delivery in agentic AI, the team faced a familiar challenge: how to build real-world capability, not only theoretical knowledge. Online courses and classroom-based instruction build foundations, but they do not always give teams the confidence or practical experience needed to apply AI effectively to business problems.
>
> Through the Atos partnership with AWS, we had already seen that hands-on learning was the missing ingredient in effective AI enablement. We had previously delivered practical upskilling in reinforcement learning through AWS DeepRacer and in model fine-tuning through AI League in 2025.
>
> In 2026, Atos partnered with AWS to run an agentic AI League event for 400 engineers. Over three days, engineers moved from limited hands-on experience to building multi-agent systems with pathfinding, guardrails, memory, and fine-tuned models. They competed on a live leaderboard that scored both performance and efficiency.
>
> Participant skill levels varied widely. Some were developers with existing AWS experience. Others were using AWS for the first time or held less technical roles such as product owners and project managers.
>
> 5% had no prior knowledge of agentic AI.
>
> 25% had basic awareness of the topic.
>
> 50% understood the topic but had no hands-on experience.
>
> 20% had practical experience with agentic AI services.
>
> This post explains why we chose the AI League format, what engineers built and learned, which AWS services were involved, and what other enterprises should consider when running a similar event.
>
> Why the AWS AI League?
>
> Atos has a strategic commitment to agentic AI, including the development of Sovereign Agentic AI Studios in multiple locations worldwide. We needed a way to upskill our engineering teams rapidly in agentic AI patterns, not through passive training, but through hands-on delivery. Traditional workshops teach concepts. The AI League built capability through practical work under conditions that more closely reflected real delivery.
>
> The AI League format offered several advantages over conventional training:
>
> Immediate practical application – engineers built working agentic systems, rather than simply reading about them.
>
> Competitive motivation – the leaderboard created urgency and engagement that passive learning rarely achieves.
>
> Real AWS services – everything built during the event used native AWS services that engineers could apply in client delivery, including Amazon Bedrock, Amazon Bedrock AgentCore, AWS Lambda, Kiro, and Amazon SageMaker.
>
> Measurable outcomes – AI League leaderboard scores reflected functional completeness and solution efficiency.
>
> Time commitment and format
>
> AWS AI League is a turnkey solution, so setup was straightforward. Setup required only a few calls with AWS to agree on logistics and event details, plus a mechanism to advertise the event and collect participant information.
>
> Because AWS AI League was delivered through the AWS Workshop Studio, the event could be run over one to three days. To give engineers maximum flexibility, we chose a three-day format. Participant time commitments were as follows:
>
> Initial kick-off workshop (2 hours) – introduced the AI League, the AWS services used, and the format of the challenges.
>
> Daily office hours call (1 hour) – provided support for engineers who needed help or wanted to share ideas.
>
> Top three finale (1 hour) – where we crowned our 2026 champion.
>
> Outside these scheduled sessions, engineers were free to iterate on their agentic AI solutions around their existing commitments.
>
> The AI League challenge
>
> Engineers built an autonomous AI agent that navigated a dungeon maze. The agent had to find a path through the map, solve challenges on various tiles, avoid traps, and reach the treasure. All of this had to be completed within a time limit and with limited lives.
>
> The following figure shows an overview of an AWS AI League map.
>
> Figure 1: Overview of an AWS AI League map
>
> The scoring model rewarded:
>
> Successful challenge completion – correct answers earned points, while incorrect answers cost lives.
>
> Coin collection – unlike challenges, coins carried no risk and required no additional time to collect.
>
> Map completion – engineers received a treasure bonus for reaching the treasure within the allotted time.
>
> Life retention – each remaining life at the end of the challenge earned additional points.
>
> Efficiency – concise agent responses outscored more verbose ones.
>
> Fine-tuning – developing specialist small language models earned bonus points.
>
> The challenge types tested different AI engineering skills:
>
> Challenge
>
> Skill tested
>
> AWS Service(s)
>
> Violent Violet
>
> AI safety and content filtering
>
> Amazon Bedrock Guardrails
>
> Blue Brain
>
> Code generation and execution
>
> AWS Lambda,
>
> AgentCore Code Interpreter, a capability of Amazon Bedrock AgentCore
>
> Memento
>
> Context retention across interactions
>
> AgentCore memory, a capability of Amazon Bedrock AgentCore
>
> Dark Prophet
>
> Information retrieval from web sources
>
> AWS Lambda,
>
> AgentCore Code Interpreter
>
> Bonehead
>
> General knowledge with token efficiency
>
> Amazon Bedrock (prompt engineering)
>
> Healthcare API
>
> Structured data extraction
>
> Amazon Bedrock (prompt engineering)
>
> Keys &amp; Doors
>
> Context retention across interactions
>
> AgentCore memory
>
> Spikes &amp; Coins
>
> Pathfinding and risk assessment
>
> AWS Lambda
>
> The following diagram shows the solution architecture.
>
> Figure 2: Overview of the AWS AI League architecture
>
> Amazon Bedrock
>
> With Amazon Bedrock, engineers accessed the models that powered the agent’s reasoning. For model availability by Region, refer to Supported models by AWS Region in Amazon Bedrock:
>
> Select appropriate models for different tasks, beginning with a well-known model and then performing inference against their own fine-tuned model.
>
> Engineer effective system prompts to answer questions efficiently or delegate to sub-agents and tools.
>
> Manage token usage and cost.
>
> Amazon Bedrock AgentCore
>
> With Amazon Bedrock AgentCore, a platform to build, connect, and optimize agents at scale with any framework or model, engineers orchestrated multi-agent systems. Engineers used the following AgentCore capabilities during the AI League:
>
> AgentCore runtime, a capability of Amazon Bedrock AgentCore – engineers hosted their agent containers, which processed challenge tiles and returned scored responses within the time limit.
>
> AgentCore Gateway, a capability of Amazon Bedrock AgentCore – engineers routed tool calls from agents to Lambda functions through the Model Context Protocol (MCP) for pathfinding, web scraping, and code execution.
>
> AgentCore memory, a capability of Amazon Bedrock AgentCore – engineers persisted context across interactions so agents could recall previous events like collected keys and solved challenges.
>
> AgentCore Code Interpreter, a capability of Amazon Bedrock AgentCore – engineers executed code securely in an isolated sandbox for computational challenges.
>
> Amazon Bedrock Guardrails
>
> With Amazon Bedrock Guardrails, you can filter content to protect against harmful inputs and outputs. Engineers configured:
>
> Denied topics – specific content that had to be blocked.
>
> Content filters – thresholds for hate, violence, and misconduct.
>
> Input and output blocking with custom messages.
>
> AWS Lambda
>
> With AWS Lambda, you can build custom tool functions for tasks that models cannot reliably handle on their own:
>
> Pathfinding – navigating the map using algorithms such as Breadth-First Search (BFS).
>
> Code Interpreter – executing code for computational challenges.
>
> Web scraping – fetching and parsing web pages for information retrieval.
>
> Amazon SageMaker
>
> With Amazon SageMaker, you can build your development environment and fine-tune models. Engineers used Reinforcement Learning from Verifiable Rewards (RLVR):
>
> Amazon SageMaker Studio provided the development environment, including an integrated development environment (IDE) with built-in AI development tools.
>
> Serverless fine-tuning trained custom models on participant-created datasets.
>
> Fine-tuned models were then deployed to inference endpoints to serve traffic.
>
> The following figure shows the fine-tuning model workflow.
>
> Figure 3: Fine-tuning model overview
>
> What our engineers learned
>
> The AWS AI League surfaced several practical engineering lessons that are directly applicable to production agentic AI work.
>
> Prompt engineering under constraints
>
> One of the clearest lessons was that success did not come from writing prompts alone, but from writing prompts that worked under real constraints. Every extra token cost points. Every unnecessary tool call consumed time and cost points. Engineers quickly discovered that getting a solution to work was only the first step. Making it efficient was where the competition became most relevant to real customer scenarios.
>
> Multi-agent architecture decisions
>
> Engineers had to decide how many agents to include in their architecture, from single-purpose agents with specialist tools to more multifunctional agents. Each approach involved trade-offs in token usage, latency, and reliability. This closely reflects real production decisions about agent design.
>
> The following figure shows how different agentic systems answered challenges during the finale.
>
> Figure 4: Overview of different agentic systems answering challenges
>
> Guardrail configuration
>
> The Violent Violet challenge highlighted an important lesson: guardrails had to be precise enough to block undesirable content, without over-blocking legitimate queries. If they were too aggressive, engineers failed other challenges. If they were too permissive, they failed the guardrail challenge. This translates directly into a practical lesson in production AI safety.
>
> Pathfinding algorithm design
>
> Building the pathfinding tool required engineers to think about:
>
> Multiple strategies for different scenarios (speed versus score maximization).
>
> Risk assessment (spikes cost lives, while walls end the game).
>
> Time budgeting (should we visit every challenge, or go straight for the treasure?)
>
> Dependency ordering (for example, collecting the key before attempting the door).
>
> The following figure shows examples of multiple pathfinding strategies on the same map.
>
> Figure 5: Example of multiple different pathfinding strategies
>
> The value of observability
>
> Engineers who checked their Amazon CloudWatch Logs between runs appeared to improve more quickly. Those who guessed what had gone wrong often made slower progress. This reinforced a core engineering principle: instrument the solution properly and observe before acting.
>
> The following figure shows how to troubleshoot a Lambda function using Amazon CloudWatch Logs.
>
> Figure 6: Troubleshooting a Lambda function with Amazon CloudWatch Logs
>
> Using AI to build agentic AI solutions
>
> Engineers who used AI developer tools such as Kiro often made rapid progress. Those who shared the full context of the challenge with their AI tools tended to achieve better results more quickly. This reinforces a broader lesson: AI tools deliver more value when grounded in the specific problem being solved.
>
> Results and outcomes
>
> The event delivered:
>
> Based on the event registration data, 400 engineers gained hands-on experience in agentic AI.
>
> Engineers developed practical skills in Amazon Bedrock, Amazon Bedrock AgentCore, AWS Lambda, Amazon Bedrock Guardrails, Kiro, and Amazon SageMaker.
>
> Internal champions emerged with greater confidence in applying agentic AI in client engagements.
>
> The competitive format encouraged knowledge sharing and helped break down barriers between teams.
>
> The top-performing solutions demonstrated thoughtful engineering. They included custom pathfinding strategies, carefully tuned guardrails, memory-aware agents, and fine-tuned models designed to reduce token usage. Congratulations to our top three performers: James Ponter, Adam Różewicki, and Eduard-Cosmin Socol. Our winner, James Ponter, Head of Hyperscalers – UKI Cloud and Infrastructure, summed up the event:
>
> “Academic learning gives you the foundation, but the AWS AI League puts it under pressure in a way that genuinely changes how you think. Building a production-style multi-agent architecture on real AWS infrastructure, not a toy project, but something scored on both performance and efficiency, forces you to internalize concepts rather than just understand them. You can’t look up the answer when the clock is running. That time pressure, combined with the fact that your decisions have real consequences on the leaderboard, creates a depth of engagement that’s hard to replicate in any other learning environment. It bridges the gap between knowing and doing in a way that sticks.”
>
> The following figure shows the finale leaderboard.
>
> Figure 7: Our finale leaderboard
>
> A closing comment from Chris Byrne, Global Head of AWS Alliance at Atos, on the benefits of the gamified learning approach taken to AWS upskilling:
>
> “Taking the step from theoretical knowledge to hands-on experience can be daunting on the one hand, and challenging knowing where and how to start on the other. Atos has successfully used the AWS leagues for Reinforcement learning with AWS DeepRacer, model fine-tuning with AI League, and now Agentic AI in this year’s league, to give our teams the forum in which to gain experience and develop their skills in an engaging and fun environment, without the pressure to perform in a real-world project. The level of participation across the company and the results achieved by Atos entrants in the public leagues speaks to the effectiveness of this approach to learning.”
>
> Getting started
>
> AWS AI League is available for enterprise events throughout 2026, and at select AWS Summits and virtual events. The format is flexible, ranging from half-day workshops to multi-day hackathons, and AWS provides the infrastructure, accounts, and facilitation support.
>
> To explore running an AI League event for your organization:
>
> Visit the AWS AI League page to learn about the program.
>
> Contact your AWS account team to discuss a private event.
>
> Join the AWS AI League Builder Space for official announcements and the AI Community space to share ideas with the community.
>
> AWS AI League is more than a competition. It is an effective way to accelerate practical AI skills development and encourage idea sharing. To learn more or explore running an event for your organization, visit the AWS AI League page or contact your AWS account team.
>
> Learn more about the AWS AI League’s agentic AI and model customization challenges in AWS AI League: Model customization and agentic showdown.
>
> See how a student went from beginner to champion in From beginner to champion: A student’s journey through the AWS AI League ASEAN finals.
>
> For guidance on taking agentic AI from competition to production, see AI agents in enterprises: Best practices with Amazon Bedrock AgentCore.
>
> About the authors
>
> Rajesh Babu Nuvvula
>
> Rajesh is a Senior Solutions Architect on the Worldwide Public Sector team at Amazon Web Services (AWS), collaborating with public sector partners and customers to design and scale well-architected solutions for cloud migration and application modernization. His areas of expertise include distributed enterprise applications, data and analytics, AI/ML, and databases. Outside of work, Rajesh enjoys exploring emerging technologies and long walks.
>
> Ruchi Bhatia
>
> Ruchi is a Technical Product Marketing Manager at Amazon Web Services, where she drives product marketing for model training and customization on Amazon SageMaker AI and leads marketing for the AWS AI League. She holds a master’s degree in Information Systems Management from Carnegie Mellon University and is the youngest triple Kaggle Grandmaster across the Notebooks, Datasets, and Discussion categories. Her expertise has led to speaking invitations at Google Cloud Next, NVIDIA GTC, and the University of Oxford, and she is passionate about mentoring early-career professionals breaking into the tech industry.
>
> Mark Ross
>
> Mark is the Chief Architect for AWS within Atos’ Cloud and Modern Infrastructure engineering function, bringing over two decades of technology experience across Financial Services, Government, Health, Utilities, and Media sectors. He is passionate about helping customers build, migrate, and exploit AWS technology, and is recognized as an AWS Ambassador, AWS Community Builder, and has held the coveted AWS Golden Jacket since 2021. Outside of work, Mark loves travelling and rugby union.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。