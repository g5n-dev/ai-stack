---
title: "How Fanatics Betting and Gaming built a multi-agent customer support system"
date: 2026-08-20T05:45:58+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "RAG", "AI Agent", "生成式 AI", "机器学习", "Prompt 工程", "Amazon Bedrock", "Customer Solutions"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:4d6a3b0d38ddd3625f03c46c18066fd0d0d9704e3f365a5dfdb3add2c868a67a"
source_payload_sha256: "sha256:435f546deb299a3816ad8f8b85ff301824568a4b2e5fd10bea2a6835399d8dd7"
observation_id: obs_b26ec23879c13b42dd868f69597824477ae71fe9b0285eb90563f0dfc343459e
event_id: evt_5bb1eb60132d3de84136207d1d0f6bfaca7b8b2d0158071d022611f778ee23f9
revision_id: rev_de64867f33b9993e1af00985a5e6368273d10ab6f4ebaf62da08a5fa4dfdb925
source_published_at: 2026-08-19T20:40:45Z
first_seen_at: 2026-08-19T21:42:31.769413Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 75
interpretation_sha256: "sha256:0cd3732c0641af56dc052e1aed0ebaa3068742f7d444af411ceec979ab6c486e"
description: "Fanatics Betting and Gaming 在 AWS 上构建了一套多代理客服系统，由专门的子代理分别处理账户、地区法规、负责任游戏等不同任务，主调度代理负责统一协调和返回答案。"
external_url: https://aws.amazon.com/blogs/machine-learning/how-fanatics-betting-and-gaming-built-a-multi-agent-customer-support-system
parent_observation_id: null
last_seen_at: 2026-08-19T21:42:31.769413Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/how-fanatics-betting-and-gaming-built-a-multi-agent-customer-support-system](https://aws.amazon.com/blogs/machine-learning/how-fanatics-betting-and-gaming-built-a-multi-agent-customer-support-system)
- **发布域名**: aws.amazon.com

## 要点解读

### 这是什么
Fanatics Betting and Gaming 在 AWS 上构建了一套多代理客服系统，由专门的子代理分别处理账户、地区法规、负责任游戏等不同任务，主调度代理负责统一协调和返回答案。

### 用在哪里
适用于体育博彩平台在赛事高峰期（如 NFL 季后赛、超级碗）需要快速、准确地响应大量跨州监管和客户咨询的场景，也适合需要在合规要求严格的环境下实现自动化的组织。

### 可以推断的
推测：模块化的代理结构可以在新增业务单元或监管规则时，仅通过添加对应的专用工具或子代理即可扩展，而不必改动核心调度逻辑。  
推测：系统内置的负责任游戏分类机制能够在识别高风险对话时即时转接人工，从而在保证合规的前提下降低整体人工成本。

## 来源摘要/节选

> Fanatics Betting and Gaming (FBG) built a multi-agent customer support system on AWS to solve a challenge unique to sports betting. Customers expect instant, accurate answers, especially during live events when every minute counts. Customers ask about account issues, deposit limits, state-specific regulations, and responsible gaming resources. The rules vary across every jurisdiction where an operator is licensed. Traditional chatbot solutions built on decision trees struggle with this complexity, often frustrating customers and driving up costs as human agent queues grow.
>
> Fanatics Betting and Gaming (FBG) is a sports betting platform that combines advanced technology with deep sports expertise. As part of the Fanatics family of brands, FBG operates across multiple U.S. states, serving a rapidly growing user base that demands around the clock support, particularly during high-traffic events like NFL playoffs and the Super Bowl.
>
> Facing exponential growth in support volume, FBG’s engineering team built a multi-agent AI system on AWS that resolves customer issues faster, more accurately, and at a fraction of the cost of human-only support. In this post, we walk through the architecture, the AWS services involved, and the patterns you can consider when designing your own multi-agent customer support solution.
>
> The challenge
>
> As FBG scaled, their existing support model required more human touches per interaction, creating higher operational costs that grew proportionally with their customer base. The team recognized an opportunity to improve their customers’ experience while preparing the support infrastructure for the next phase of growth. Several factors made the problem especially difficult.
>
> Every U.S. state has its own rules for payment methods, deposit limits, withdrawal timelines, and responsible gaming requirements. A customer in Indiana gets different answers than one in New Jersey. During major sporting events, support requests can surge to over 40 inquiries every two minutes, and the system needs to scale instantly without degrading response quality.
>
> The diversity of queries compounds the problem. Customers ask about everything from transaction history and account settings to betting rules and self-exclusion options. No single model or knowledge base covers it all. On top of that, operators must identify and respond to signs of problem gambling in real time. This requires a nuanced understanding of conversational context, not just keyword matching.
>
> FBG needed a system that could handle this complexity autonomously while knowing exactly when to escalate to a human agent.
>
> “As we scaled, we knew our support experience needed to evolve with us. We wanted to give our customers faster, more accurate answers while making sure we never compromised on responsible gaming or compliance. The goal was to build something that got better over time, not just bigger.”
>
> — Ian Botts, CTO, Fanatics Betting and Gaming
>
> Solution overview
>
> Rather than relying on a single monolithic chatbot, FBG designed a multi-agent system where specialized agents handle different aspects of the customer interaction. Because the team had already built deep operational expertise on Amazon Elastic Kubernetes Service (Amazon EKS), they could build on their existing container platform to deploy, scale, and iterate on each agent independently.
>
> FBG chose Amazon Bedrock for its model-agnostic access to multiple foundation models through a single API, which lets the team match each task to the best model and swap models as better options emerge. Because Bedrock runs within their existing AWS environment, the system also inherits FBG’s established security and governance controls, and Amazon Bedrock Guardrails provides the responsible AI safeguards their compliance requirements demand.
>
> The architecture follows an orchestrator pattern. A primary orchestration agent receives each customer message, coordinates with specialized tools and sub-agents, and returns a unified response. This design allows the team to add new capabilities, such as new tools, new knowledge domains, and new business units, without rewriting the core system.
>
> “We designed the system so that each agent has a clear responsibility and can be improved independently. That modularity is what allows us to move fast. When we need to support a new case type or a new business unit, we add a new tool or agent without touching the rest of the system.”
>
> — Luis Fernandez Rocha, Sr. Manager of Software Engineering, Fanatics Betting and Gaming
>
> Figure 1 illustrates the high-level architecture.
>
> Figure 1: End-to-end architecture of the multi-agent customer support system on AWS
>
> A customer message enters through the FBG mobile app, passes through Salesforce Einstein to the Spring AI service on Amazon EKS, then flows through Amazon Bedrock Guardrails and a Responsible Gaming classifier before reaching the Supervisor Agent. The Supervisor Agent invokes specialized tools, including a Retrieval Augmented Generation (RAG) pipeline, account and transaction Model Context Protocol (MCP) servers, and a transfer-to-agent tool to generate a response.
>
> How a request flows through the system
>
> A customer sends a message through the FBG mobile app, which connects to Salesforce Einstein as the chat interface layer. The request is routed through standard REST calls to the Spring AI service running on Amazon EKS. This service validates the customer token and invokes the AI agent.
>
> The request then passes through Amazon Bedrock Guardrails to help detect prompt injection before reaching the AI layer. A Responsible Gaming classification agent, powered by Amazon Nova 2 Lite, evaluates every message against a compliance-approved classification framework. High-severity classifications trigger an immediate transfer to a human agent with full conversation context.
>
> The Supervisor Agent, running Anthropic Claude on Amazon Bedrock, determines which tools to invoke based on the customer’s intent. Depending on the query, the supervisor calls one or more specialized tools, some through MCP and others local to the service:
>
> Retrieval Augmented Generation (RAG) Tool retrieves relevant knowledge from a vector store for FAQ-style questions.
>
> Account Tools (MCP) queries internal account services for customer-specific information.
>
> Transaction Tools (MCP) retrieves recent transaction history including deposits, withdrawals, and betting activity.
>
> Transfer-to-Agent Tool escalates to a human agent when the customer explicitly requests it or when the situation requires human judgment.
>
> The supervisor synthesizes the tool responses and returns a natural language response to the customer.
>
> Deep dive: Key architectural components
>
> In this section, we examine the four components that make the system work: the Amazon EKS hosting platform, the custom RAG pipeline, the responsible gaming classifier, and the guardrails that help keep conversations safe.
>
> Amazon EKS for agent hosting and MCP servers
>
> FBG runs their entire AI stack on Amazon EKS hosting their MCP server and Spring AI service as Kubernetes services. The MCP server exposes tools that make REST calls to external services like the account service and transaction-history service. Local tools live directly in the Spring AI service alongside the Claude large language model (LLM). These include the RAG tool and Transfer-to-Human tool.
>
> This approach provides several advantages for multi-agent systems. The MCP server and Spring AI service scale independently based on demand. When FBG needs to support additional business domains or features, adding a new MCP server is just another Kubernetes deployment. The team can also update individual tools without redeploying the entire system. New MCP tools are added to an existing MCP server without requiring new pod deployments.
>
> FBG uses Spring AI as its application framework, which provides native MCP support. The MCP server defines tools that the supervisor agent can discover and invoke dynamically. The team chose Spring AI because their developers had deep Java expertise, which let them move quickly. For teams working in Python, Strands Agents is an open source SDK from AWS that provides similar agent orchestration and MCP support.
>
> For teams considering a similar approach, Amazon EKS provides the container orchestration needed to manage multiple agent services at scale. MCP provides the standardized protocol for tool communication between agents. Teams that prefer a managed experience can also explore Amazon Bedrock AgentCore, a platform to build, connect, and optimize agents at scale, with any framework or model. AgentCore also supports MCP for tool integration.
>
> Custom RAG with Amazon Titan embeddings
>
> The most frequently used tool in the system is the RAG pipeline. FBG built a custom implementation rather than using a managed knowledge base, giving them precise control over the ingestion, chunking, and retrieval process.
>
> The pipeline works in this way. Support documentation is collected from upstream sources, including state-specific payment method guides, FAQ articles, responsible gaming resources, and account management guides. Documents are split using a token-based chunking strategy, meaning each document is divided into segments of a fixed number of tokens (the units of text a model processes) rather than by sentences or paragraphs. This gives the team fine-grained control over chunk boundaries. Chunks are then embedded using Amazon Titan V2, generating vector representations stored in MongoDB Atlas.
>
> When a customer asks a question, the system converts the query into a vector search-optimized form using an LLM, then performs a similarity search against the document store. For jurisdiction-specific questions, the system performs both a state-specific search and a general search, combining the results before passing them to the supervisor agent for response generation.
>
> This custom approach is particularly valuable when your knowledge base has complex retrieval requirements, like needing to combine state-specific and general documents in a single response. The knowledge base is continuously expanding, with hundreds of new documents added monthly as the team identifies gaps through conversation analysis.
>
> “Building our own RAG pipeline gave us full control over what the model sees and how it retrieves information. Every state has different rules, so we needed the ability to combine state-specific and general documents in a single response. That level of control made all the difference in accuracy.”
>
> — Sharoze Amir, Software Engineer, Fanatics Betting and Gaming
>
> Responsible gaming classification with Amazon Nova
>
> Responsible gaming is a regulatory requirement and a core value for FBG. The team worked with their compliance department to build a classification system. The system evaluates customer interactions to confirm responsible gaming standards are met and connects customers with the right resources when needed.
>
> The system uses Amazon Nova 2 Lite, a lightweight, fast classification model. The team chose a smaller model deliberately. The task is well-defined with clear examples and a limited set of outcomes, so a larger, more expensive model would add latency without improving accuracy.
>
> The model receives both the current message and the full conversation history, enabling it to detect escalating patterns rather than relying on single-message keyword matching. When the system identifies a high-severity concern, it immediately transfers the customer to a human agent with full conversation context. Lower-severity flags are recorded for compliance review while allowing the conversation to continue.
>
> This is a pattern that applies broadly: use the smallest model that meets your accuracy requirements for well-scoped classification tasks, and reserve larger models for open-ended reasoning.
>
> “Off-the-shelf support agents treat every conversation the same. Ours can’t — a question about a withdrawal might really be a responsible gaming moment, and recognizing that requires deep integration with our compliance framework. That’s why we built on AWS in-house: no vendor was going to handle those sensitive areas the way our industry demands.”
>
> — Trevor Gurgick, Head of Applied AI, Fanatics Betting and Gaming
>
> Amazon Bedrock Guardrails for security
>
> FBG uses Amazon Bedrock Guardrails to help protect against prompt injection and help keep conversations within appropriate boundaries. The team tuned their guardrail configuration to help balance security with the realities of customer service interactions, where overly restrictive filters can create friction in the customer experience.
>
> The key insight: tune your guardrails to your actual use case rather than applying maximum restrictions by default. For customer support, prompt injection protection is critical, but overly aggressive content filtering creates false positives that frustrate customers.
>
> A multi-model architecture
>
> FBG runs a multi-model architecture on Amazon Bedrock, taking a deliberate, bottom-up approach to model selection. For classification tasks like responsible gaming, they use Amazon Nova 2 Lite. It is fast, cost-effective, and sufficient for well-defined classification where clear examples exist. For supervisor and orchestration tasks such as conversation management, they use Anthropic Claude Sonnet on Amazon Bedrock. Claude handles complex reasoning, tool orchestration, and natural conversation. For embeddings in the RAG pipeline, they use Amazon Titan V2, which generates high-quality vector representations. For model availability by AWS Region, refer to Supported models by AWS Region in Amazon Bedrock.
>
> The team uses a round-robin strategy across model Regions for the supervisor agent, ensuring they never hit throughput limits during peak events. Because every model is accessed through the same Amazon Bedrock API, routing different workloads to different models requires no changes to the underlying infrastructure.
>
> Results
>
> Within the first two months of deployment, the multi-agent system delivered measurable improvements over FBG’s previous support experience, based on FBG’s internal metrics. The containment rate improved by approximately 56 percent, meaning more customer issues are now resolved without human agent involvement. Resolution rates improved by approximately 53 percent, with customers getting their problems actually solved rather than deflected. The system has resolved thousands of cases autonomously, representing significant cost savings because AI-powered interactions cost a fraction of human agent interactions. Customer satisfaction is also trending upward. Conversation quality has improved so significantly that customers frequently don’t realize they’re interacting with AI.
>
> During peak sporting events, the system handles high request volumes while maintaining consistent performance and response quality. Amazon EKS autoscaling ensures that the MCP servers and Spring AI service add capacity automatically as traffic spikes, without requiring manual intervention. This means that whether it’s a quiet Tuesday or the Super Bowl, customers receive the same fast, accurate responses regardless of how many others are asking questions at the same time.
>
> Continuous improvement: Evaluation and iteration
>
> Building the agent is just the beginning. What makes FBG’s approach stand out is the investment they’ve made in continuously improving the system after deployment. The team treats their multi-agent system as a living product, not a one-time implementation. They review conversation logs, track resolution accuracy, and use real customer interactions to refine prompts, adjust tool behavior, and identify gaps in their knowledge base. This ongoing investment ensures that the system gets smarter over time rather than degrading as customer needs evolve.
>
> At the core of their evaluation strategy is an LLM-as-a-Judge system that automatically reviews every completed conversation, classifying whether the AI successfully resolved the case or whether it fell short. An operations team reviews these evaluations daily, identifying patterns in where the agent struggles and filing improvement tickets to close those gaps. This creates a feedback loop where the agent gets measurably better over time.
>
> On the engineering side, the team monitors system health through real-time observability metrics, including hallucination detection, latency, and cost tracking. When developing new features or testing changes, they pull actual customer conversations from production and replay them against the updated architecture to surface edge cases before anything reaches customers.
>
> One discipline that has been particularly effective is the team’s approach to prompt engineering. Rather than jumping to a more powerful (and more expensive) model when performance dips, they first look at whether the system prompt can be improved or whether there are contradictions in the instructions. This keeps costs low while driving continuous quality improvements, and they only upgrade models when the prompt has been fully optimized for the task. Teams looking to systematize this discipline can use advanced prompt optimization in Amazon Bedrock, which refines prompts against evaluation criteria and compares results across multiple models before committing to a migration.
>
> Getting started: Building your own multi-agent support system
>
> If you’re looking to build a similar multi-agent customer support system, here’s a practical starting path.
>
> Define your scope narrowly
>
> FBG launched with just 4 of their over 20 case types. Starting narrow lets you prove value quickly, build evaluation infrastructure, and learn what works before expanding. Pick the case types with the highest volume and clearest resolution criteria.
>
> Set up your infrastructure
>
> Deploy your agent services on Amazon EKS for full control or use Amazon Bedrock AgentCore for a managed experience. Use MCP for communication between your orchestrator and tool services.
>
> Build your RAG pipeline
>
> Start with Amazon Bedrock Knowledge Bases, the fully managed RAG capability, or build a custom pipeline with Amazon Titan embeddings if you need fine-grained control over retrieval logic. Either way, invest time in your chunking strategy. It has more impact on response quality than model selection.
>
> Implement guardrails and compliance from day one
>
> Use Amazon Bedrock Guardrails to help protect against prompt injection. If your industry has compliance requirements (gaming, healthcare, finance), build classification agents early. They’re easier to integrate from the start than to retrofit later.
>
> Start small with model selection
>
> Use the smallest model that meets your accuracy requirements for each task. Reserve larger models for your orchestration agent where complex reasoning is needed. Amazon Bedrock makes it straightforward to swap models as you iterate.
>
> Invest in evaluation early
>
> Build your evaluation pipeline alongside your agent, not after. Track containment rates, resolution rates, and customer satisfaction from day one. Use LLM-as-a-Judge patterns to automate conversation review at scale.
>
> Conclusion
>
> Fanatics Betting and Gaming’s multi-agent architecture demonstrates how combining Amazon EKS, Amazon Bedrock, MCP, and purpose-built AWS AI services can deliver customer support that scales with your business while maintaining quality and compliance. By using specialized agents for different tasks, including orchestration, knowledge retrieval, classification, and tool execution, the system handles the complexity of state-specific regulations, real-time responsible gaming detection, and high-traffic sporting events.
>
> The patterns in this post apply broadly. Define your scope narrowly, use specialized agents with clear responsibilities, choose the smallest model that meets your accuracy requirements, and invest in evaluation infrastructure from the start.
>
> If you’re ready to build a similar multi-agent customer support system, start by defining your agent boundaries and identifying the tools each agent needs. You can deploy your agents on Amazon EKS for full control over scaling and orchestration or use Amazon Bedrock AgentCore for a managed runtime that handles infrastructure for you. For the AI layer, Amazon Bedrock gives you access to models like Anthropic Claude and Amazon Nova through a single API, and Amazon Bedrock Guardrails can help you add safety checks without custom code. To get started, see the Amazon Bedrock Getting Started guide and the Strands Agents documentation for an open-source Python framework that supports MCP-based tool orchestration.
>
> About the authors
>
> Parker Bradshaw
>
> Parker is a Senior Solutions Architect at AWS, where he helps retail, ecommerce, and sports &amp; entertainment companies put AI and data to work. From generative AI applications to large-scale storage architectures, he focuses on turning emerging technology into real business value rolling up his sleeves alongside engineering teams to build systems like the multi-agent architecture featured in this post. Parker holds an MBA from Utah Valley University and multiple AWS certifications. When he’s not building, he’s spending time with family or on the pickleball court.
>
> Luis Fernandez-Rocha
>
> Luis is a Senior Engineering Manager of Growth Engineering at Fanatics Betting and Gaming, where he works across search, machine learning, and generative AI. He focuses on customer experience, exploring how the intersection of these science-driven domains can streamline and elevate the overall user experience. When he’s not building, he’s out on the golf course or the padel court.
>
> Sharoze Amir
>
> Sharoze is a Senior Software Engineer at Fanatics Betting and Gaming (FBG) specializing in generative AI and agentic systems, where he serves as technical lead on one of the teams building AI products for the company. He led the development of FBG’s Customer Service AI Agentic platform, the first generative AI solution FBG delivered to its customers, taking it from prototype to production. With six years of experience spanning high-throughput backend systems, real-time data platforms, and agentic AI architecture and applications, Sharoze brings a blend of distributed systems and applied AI expertise that enables him to build robust agentic solutions that hold up in production. He previously worked at Mastercard and holds a B.S. in Computer Science from the University of Missouri – Columbia.
>
> Trevor Gurgick
>
> Trevor leads Applied AI at Fanatics, where he created the company’s enterprise AI strategy, ships AI agents, and drives internal transformation. He brings more than a decade of experience turning frontier research into real-world products, including autonomous hospital robots, next-generation fulfillment robotics at Amazon, and conversational AI for Alexa. When he’s not building, he teaches MIT research teams how to turn breakthroughs into businesses, spends his time cooking and chasing after his toddler.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。