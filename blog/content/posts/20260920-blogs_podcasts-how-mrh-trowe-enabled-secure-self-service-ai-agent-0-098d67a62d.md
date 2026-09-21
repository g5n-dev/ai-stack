---
title: "How MRH Trowe enabled secure self-service AI agents in financial services"
date: 2026-09-20T14:17:20+08:00
draft: false
entry_kind: "auto"
tags: ["RAG", "AI Agent", "生成式 AI", "Amazon Bedrock AgentCore", "Customer Solutions", "博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:ad5a42917a6bfe730116d06246fa6fafeedfa63518c12e3453601ff81feefe8a"
source_payload_sha256: "sha256:2f4e3289bfce98b3b2bfef53332ec01b89f7b6d0a02f657010e22ab4e3774b25"
observation_id: obs_098d67a62da719d6324a3943771aa31f3832f5d9ced271f4b9dd9b6476218d01
event_id: evt_a7db655f2fa2232db5f50fc2bd426ce2ab2b1baa447a57536c79a8ef4fa8b811
revision_id: rev_f240c3399b02c3a49b00ebbbf5c6d9c23b9a69c8aa85a77dc5574ec22aca69de
source_published_at: 2026-09-17T15:36:42Z
first_seen_at: 2026-09-20T06:26:54Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 73
interpretation_sha256: "sha256:a340251a5cbe4f67366be947a793455be23ad72e0ee354cd98b564d0996426aa"
description: "该案例介绍了德国保险经纪公司MRH Trowe通过结合开源SDK、云计算平台和可定制的聊天界面，为员工搭建了受监管的安全AI代理系统，使非技术人员能够快速创建和使用AI代理处理业务任务，同时满足金融行业对数据安全、合规性和成本可控的要求。"
external_url: https://aws.amazon.com/blogs/machine-learning/how-mrh-trowe-enabled-secure-self-service-ai-agents-in-financial-services
parent_observation_id: null
last_seen_at: 2026-09-21T00:00:00Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/how-mrh-trowe-enabled-secure-self-service-ai-agents-in-financial-services](https://aws.amazon.com/blogs/machine-learning/how-mrh-trowe-enabled-secure-self-service-ai-agents-in-financial-services)
- **发布域名**: aws.amazon.com

## 要点解读

### 这是什么

该案例介绍了德国保险经纪公司MRH Trowe通过结合开源SDK、云计算平台和可定制的聊天界面，为员工搭建了受监管的安全AI代理系统，使非技术人员能够快速创建和使用AI代理处理业务任务，同时满足金融行业对数据安全、合规性和成本可控的要求。

### 用在哪里

适用于金融、保险等受监管行业的企业，这些组织需要让员工在不拥有深厚技术背景的情况下使用AI工具，但又必须确保所有操作符合行业监管要求、保持数据安全并实现成本透明。案例中的具体实现场景是将Teams会议自动转换为结构化会议记录。

### 可以推断的

推测：受监管行业的AI应用落地往往需要在灵活性与控制力之间取得平衡。该案例采用开源框架与商业云平台结合的方式，既保留了技术灵活性，又借助云平台的安全隔离和合规认证降低自身的合规负担。

推测：此类解决方案的推广可能会经历从单点场景（如会议记录）逐步扩展到更多业务流程的过程，因为初始应用的成功能够为组织积累经验和信心，同时也能更清晰地识别出AI代理在复杂任务中的局限性。

## 来源摘要/节选

> Basic AI chat isn’t enough for financial services organizations that need secure, self-service AI agents. In financial services, employees need AI that can work with internal systems and sensitive client data, stay inside a governed environment, and remain auditable and cost-transparent. All of this must happen without every team standing up its own tools.
>
> This post shows how MRH Trowe, one of Germany’s leading commercial and industrial insurance brokers, gave approximately 400 employees secure access to self-service AI agents. The rollout reached this scale in the first month of production. The framework combines Strands Agents, Amazon Bedrock AgentCore, and LibreChat to deliver the security, data residency, and compliance controls required in the German financial sector. The initial production cost was approximately $14 per seat in the first month, with a clear path to reduce infrastructure costs by about 40 percent through right-sizing and scheduled scaling.
>
> About MRH Trowe
>
> MRH Trowe is an owner-managed commercial and industrial insurance broker operating primarily in Germany, Switzerland, and Austria. Growing through both organic expansion and acquisitions, MRH Trowe was among the first German insurance brokers to operate on an exclusively cloud-based IT infrastructure. AWS is the preferred partner for this strategy, and the use of AI is a strategic corporate goal, specifically to streamline internal processes and enhance efficiency.
>
> The challenge: Self-service AI without losing control
>
> As a commercial insurance broker in a highly regulated industry, MRH Trowe saw growing demand from employees across the business to use generative AI in their daily work. Individual teams were beginning to experiment with AI on their own, which created the risk of fragmented, unmanaged tools and potential exposure of sensitive client and insurance data.
>
> MRH Trowe needed a way to let employees build and use AI agents themselves, quickly and without deep technical skills. At the same time, everything had to stay within a secure, centrally governed environment that meets the data protection and compliance requirements of the financial sector. The core tension was clear: balance broad, self-service access to AI with the security, control, and cost transparency the organization required. The MRH Trowe vision: “every question should be first answered by AI before any human intervention, and repetitive processes should be automated by those who did them in the past.”
>
> Basic chat interfaces fell short on several capabilities the business needed:
>
> Contextual responses – Grounded in internal data, not only generic model knowledge.
>
> Multi-step workflows – Tasks that require gathering information, reasoning over it, and taking action across several steps.
>
> Institutional data integration – Secure connections to internal systems and document repositories.
>
> Centralized governance – A single, governed application rather than shadow AI tools spread across teams.
>
> The building blocks
>
> The solution brings together three technologies, each addressing a specific part of the challenge.
>
> Strands Agents
>
> MRH Trowe’s builders use Strands Agents, an open source SDK that creates agents in a few lines of code. Strands handles the agent patterns, such as orchestration and reasoning, and scales from a builder’s laptop to production, so teams focus on the use case rather than the infrastructure.
>
> Amazon Bedrock AgentCore
>
> To run agents in production, MRH Trowe uses Amazon Bedrock AgentCore as a platform to build, connect, and optimize agents at scale, with any framework or model. AgentCore was the deciding factor for MRH Trowe: it natively supports open source frameworks such as Strands Agents, isolates each agent session at the compute and filesystem level, and offers a consumption-based model that gives the team cost transparency as adoption grows. This means the team keeps the flexibility of Strands without giving up the security and session isolation as a regulated broker requires.
>
> LibreChat
>
> LibreChat is an open source alternative to commercial AI chat interfaces. It gives MRH Trowe a familiar, brandable chat experience that drives immediate adoption, with the controls a regulated organization needs:
>
> User management – Robust authentication and authorization to manage access across the employee base with appropriate permissions.
>
> Token budgets – LibreChat’s built-in token budget system avoids unexpected costs.
>
> Multi-model support – Flexibility to choose the most appropriate models per use case while avoiding vendor lock-in.
>
> Conversation management – Employees can organize their AI interactions, creating a structured environment.
>
> Customizable interface – Branded to match MRH Trowe’s identity.
>
> In practice: From a Microsoft Teams meeting to a structured protocol in minutes
>
> The first agent MRH Trowe put into production turns a Microsoft Teams meeting into ready-to-use meeting minutes. In LibreChat, an employee asks, in German, for a recent meeting with a given participant. The agent finds the meeting on the employee’s calendar, retrieves the transcript, and drafts a structured meeting summary with date, participants, agenda, topics, and action items. Manual note-taking after every call turns into a one-line request.
>
> Two design choices make this safe for a regulated broker. First, every request runs as the signed-in employee. LibreChat authenticates through Microsoft Entra ID and passes the user’s identity to the agent server-side, so an agent can only reach that employee’s own calendar and transcript. The identity can’t be set from the chat box. Second, processing stays in-Region: the agents, model, and data run in the AWS Europe (Frankfurt) AWS Region, keeping client and meeting data in Germany. Amazon Bedrock AgentCore and the foundation models used in this solution are available in the Europe (Frankfurt) Region (eu-central-1). Service and model availability varies by AWS Region.
>
> Solution architecture
>
> The solution is deployed in a single AWS account inside a virtual private cloud (VPC), with employees connecting from the corporate network. The following diagram shows the solution architecture, including the connectivity, application, data, and agent layers described in this section.
>
> Figure 1: Solution architecture spanning the connectivity, application, data, and agent layers
>
> The main components are:
>
> Secure connectivity – Employees access the system from anywhere using a transit gateway implementation combined with a zero-trust provider, keeping traffic on a private, dedicated connection rather than the public internet. An internal Application Load Balancer (ALB) routes requests to the application tier.
>
> The following network view expands the secure-connectivity path, showing how on-premises users connect through the AWS networking account to the internal load balancer in the application account’s private subnet.
>
> Figure 2: Network path from on-premises users through the AWS networking account to the internal load balancer
>
> Application tier (LibreChat) – The chat experience runs as containerized services on Amazon Elastic Container Service (Amazon ECS) with AWS Fargate as the launch type, including the LibreChat service, a Retrieval Augmented Generation (RAG) API service, and a MeiliSearch service for fast text search without vectorizing the data.
>
> Data layer.
>
> Amazon DocumentDB (with MongoDB compatibility) for users, sessions, and conversation data.
>
> Amazon ElastiCache for caching and session state.
>
> Amazon Relational Database Service (Amazon RDS) for PostgreSQL as the relational and vector store backing LibreChat’s RAG API for uploaded documents.
>
> Amazon OpenSearch Service as the vector store for Amazon Bedrock, supporting retrieval over content ingested from Confluence.
>
> Amazon Elastic File System (Amazon EFS) for MeiliSearch indexes.
>
> Amazon Simple Storage Service (Amazon S3) for uploaded files and chat artifacts.
>
> Agent layer (Strands + AgentCore) – Strands Agents are hosted on AgentCore runtime, a capability of Amazon Bedrock AgentCore, and exposed to LibreChat through custom endpoints backed by AWS Lambda and Amazon API Gateway. With this pattern, the team can load new agents in LibreChat without updates or downtime to the chat application and roll out new agentic applications independently as adoption grows.
>
> The following screenshot shows the usage dashboard MRH Trowe built to track adoption and cost, including unique users, token consumption by model, and cost per user.
>
> Figure 3: Usage dashboard tracking unique users, token consumption by model, unique chats, and cost per user
>
> How a request flows
>
> The following steps describe how a typical request travels through the system, from the employee’s browser to the agent and back.
>
> An employee opens LibreChat and selects an agent from a switch panel.
>
> LibreChat authenticates the user through MRH Trowe’s existing identity provider, Microsoft Entra ID. Access control lists (ACLs) in the LibreChat admin panel determine which endpoints and models the user can access.
>
> When the user invokes an agent, LibreChat calls a custom endpoint through API Gateway, secured with an API key. Or if the endpoint supports On-behalf-of (OBO) authentication flow, this can also be used for user authentication.
>
> A Lambda function uses an AWS Identity and Access Management (IAM) role to invoke the Strands agent running on AgentCore runtime.
>
> The agent reasons over the request, calls its tools and authorized data sources, and returns the response through LibreChat, within an isolated, governed session.
>
> Security and compliance for a regulated environment
>
> Operating in the German financial sector means data protection and governance are not optional. The architecture applies a layered approach:
>
> Data residency in Germany – Sensitive client and insurance data stays within the chosen AWS Region.
>
> Private connectivity – A transit gateway setup combined with zero trust keeps employee traffic off the public internet.
>
> Session isolation – AgentCore runtime isolates each agent session at the compute and filesystem level.
>
> Central governance – A single, managed environment replaces fragmented, unmanaged tools, giving the organization visibility and control over how AI is used.
>
> Strong authentication and authorization mechanism – Active Directory group-based roles and access for single sign-on (SSO) and zero-trust solution.
>
> With this foundation, MRH Trowe can serve employees in a secure and highly flexible environment. AI is now at the fingertips of every employee, and exploration is encouraged, while the AWS implementation keeps security and governance at scale.
>
> Results and business impact
>
> The solution ran at an infrastructure-and-token cost of about $14 per seat per month.
>
> The environment has also become a factory for new use cases. The most recent is “talk to your data”, which supports business-led analyses such as cross-sell and upsell reviews that combine CRM data with publicly available information.
>
> To drive adoption, MRH Trowe paired the rollout with organizational change:
>
> Run use case workshops across teams to create and maintain a power user group.
>
> Use adoption data to identify power users and promote their workflows across the organization.
>
> “If you and your colleague are doing things twice, consider creating a LibreChat agent!”
>
> — Leonid Karlinsky, Board member, MRH Trowe
>
> Beyond cost efficiency, the framework delivered a secure, self-service way for employees to build and use AI agents without deep technical skills, all within a centrally governed environment that meets the compliance requirements of a regulated financial services organization.
>
> Conclusion
>
> MRH Trowe shows that a regulated financial services organization can have both broad, self-service access to AI and the control its industry demands. By combining the flexibility of open source (Strands Agents and LibreChat) with the security, scalability, and reliability of Amazon Bedrock AgentCore, MRH Trowe gave roughly 400 employees a centrally governed way to build and use AI agents in their first month with a clear path to make it even more economical as adoption grows.
>
> By shaping a Data and AI Community of Practice, MRH Trowe aims for 10–15 agents created and maintained by subject matter experts by the end of 2026.
>
> To learn more about building AI agents on AWS, visit the Amazon Bedrock AgentCore detail page and the Amazon Bedrock AgentCore documentation. To get started with open source agent development, see the Strands Agents SDK.
>
> About the authors
>
> Dr. Malte Polley
>
> Dr. Malte has been working with AWS solutions since 2018, working both as an external consultant and as an internal solution architect, developer, and product owner. Since entering the insurance world at HDI in 2020, new areas of focus have been added to his work, such as regulatory compliance and ISO 27001 compliance. Having implemented two modern data platforms at HDI and MRH Trowe, as well as building a data science platform at HDI, Malte is very familiar with the pitfalls and requirements, but also the added value of such projects in the field of FSI. Malte finds relaxation and new ideas in his vegetable garden and on long walks in the forest with his dog.
>
> Marouane El Bostahi
>
> Marouane is a Technical Account Manager at AWS. He helps enterprise customers mature in their cloud journey, influencing stakeholders with a data-driven approach.
>
> Safat Al Fahim
>
> Safat is a Customer Solutions Manager at AWS on the EMEA scale CSM team. He helps FSI customers through enterprise transformation, driving large migrations, modernization and AI adoption acceleration programs and adoption of new services and processes.
>
> Anna Sonntag
>
> Anna is an Account Manager at AWS working with regulated enterprise customers. She supports them across their cloud journey, from migrations and modernization to AI adoption, with a focus on aligning AWS capabilities with customers’ strategic business priorities.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。