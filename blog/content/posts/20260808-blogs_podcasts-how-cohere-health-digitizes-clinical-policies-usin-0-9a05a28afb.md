---
title: "How Cohere Health digitizes clinical policies using Amazon Bedrock AgentCore"
date: 2026-08-08T01:11:37+08:00
draft: false
entry_kind: "auto"
tags: ["AI Agent", "生成式 AI", "机器学习", "Prompt 工程", "Amazon Bedrock", "Amazon Bedrock AgentCore", "Artificial Intelligence", "Customer Solutions"]
categories: []
source: "blogs_podcasts"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:8269d3a56b3a1dd0aaa0086b86d2864b777403a0194cb4ab69de5338802f1245"
source_payload_sha256: "sha256:07eea6d7eb984d450af91e6ec27b5a43b38d5e52528cc018394245b53b7e216e"
observation_id: obs_9a05a28afb7c8eb8e003cdda5e7988e79896dcd5d467549a81c874733a81edaf
event_id: evt_ca46849000270afb87b79c4b47a93c08857e4ec725e6fa361dc23517c1d850fb
revision_id: rev_025834907bcb082a0e736bad84e11e7d95d4c6d01b4402a14d29df51be99a7cf
source_published_at: 2026-08-07T16:26:58Z
first_seen_at: 2026-08-07T17:21:30Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 76
description: "当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。"
external_url: https://aws.amazon.com/blogs/machine-learning/how-cohere-health-digitizes-clinical-policies-using-amazon-bedrock-agentcore
parent_observation_id: null
last_seen_at: 2026-08-09T00:00:00Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/how-cohere-health-digitizes-clinical-policies-using-amazon-bedrock-agentcore](https://aws.amazon.com/blogs/machine-learning/how-cohere-health-digitizes-clinical-policies-using-amazon-bedrock-agentcore)
- **发布域名**: aws.amazon.com

## 来源摘要/节选

> Prior authorization is the approval process health plans require before covering certain medical services or medications. It remains one of the most manual processes in healthcare, not because the medical reasoning for requiring approval is flawed, but because the policies that govern it are trapped in static, unstructured formats that resist automation. This content is at the core of day-to-day clinical operations impacting hundreds of millions of patients each year. However, the policy content varies by clinical area, geography, line of business, and health plan, and evolves as medicine and technology advances. Historically, health plans did not have a systematic way to manage, analyze, and optimize them. Digitizing these clinical policies into structured, machine-readable data using standard terminologies reduce a critical operational bottleneck by supporting more consistent, computable workflows and helping health plans modernize prior authorization operations at scale while maintaining appropriate clinical oversight.
>
> Cohere Health(R), a clinical intelligence company that powers health plan operations, built Cohere Policy Studio(TM) using Amazon Bedrock AgentCore, which provides the multi-tenant isolation required for their health plan customers and a managed agent runtime that accelerates deployment without rebuilding infrastructure. The application uses a flexible, multi-tenant agentic architecture to accelerate policy digitization with extensive workflow management and automatic version tracking.
>
> In this post, you learn how Cohere Health built a multi-tenant agentic architecture on AgentCore using AgentCore Runtime’s secure MicroVM isolation, unified tool access through AgentCore Gateway, AgentCore Memory, and the Agent Skills open standard to rapidly scale policy digitization capabilities, while preserving transparency, version control, and human oversight.
>
> Challenge: The policy digitization bottleneck
>
> Realizing the value of AI-assisted workflows in prior authorization depends on a foundational challenge: transforming the rules trapped in static documents and PDFs into structured, machine-readable data that AI systems can use more consistently, while medical professional remain responsible for clinical review where clinical judgment is required. Health plans face a complex challenge of managing clinical policies to support rapidly changing requirements. Automating policy digitization helps health plans adapt to these changes.
>
> Cohere Health identified three challenges in building an AI solution for this workflow:
>
> Government regulations – Per Centers for Medicare &amp; Medicaid Services (CMS) regulations, health plans are required to support API-based electronic prior authorization by January 2027.
>
> America’s Health Insurance Plans (AHIP) – The AHIP commitments require health plans to achieve 80 percent real-time approvals for electronic prior authorization submissions. Each line of business has unique requirements, increasing the need to quickly manage, audit, and deploy clinical policies.
>
> Technical architecture demands – The solution needed to ingest multiple input formats and produce different representations of each policy for different downstream consumers, each with its own feedback loop.
>
> AgentCore addresses these challenges with managed runtime infrastructure, session isolation, and unified tool access.
>
> Solution overview
>
> The following diagram shows how Cohere Policy Studio connects AgentCore Runtime, Gateway, and Memory into a unified agentic system for policy digitization.
>
> The Policy Studio application is built on AgentCore using the Agent Skills open standard. To scale out representations in Cohere Policy Studio, Cohere Health added new skills to an existing AgentCore Runtime that was already decomposing policies. This runtime had access to the policy skills, policy APIs as Model Context Protocol (MCP) tools through AgentCore Gateway, and session memory for policy analysts’ feedback loops, helping teams refine outputs within a governed, human-in-the-loop process.
>
> The team completed three tasks:
>
> Deployed AgentCore Runtime with AgentCore Gateway and AgentCore Memory for a full agentic system using LangChain.
>
> Configured AgentCore Gateway to fetch tools and skills.
>
> Wrote skills with clinical policy experts and evaluated them using Cohere Health’s standardized observability process based on Arize AI.
>
> You can apply these same patterns to build your own multi-tenant agentic system.
>
> Deploying AI agents with reusable Amazon Elastic Container Registry (Amazon ECR) base images
>
> Cohere Health serves multiple health plans that require strict data isolation between tenants. AgentCore Runtime’s secure microVM isolation enforces this with dedicated compute, memory, and filesystem resources per session.
>
> When deploying multiple AI agent instances across teams, maintaining consistency while allowing customization is important. Each team needs its own agent configuration, but rebuilding the entire runtime environment for every deployment creates unnecessary overhead and drift. You can use the following base image pattern to deploy new agents to AgentCore Runtime microVMs with a minimal Dockerfile.
>
> Base image and consumer pattern
>
> Cohere Health developed a two-tier deployment architecture that separates the stable runtime environment from team-specific configurations:
>
> FROM {account_id}.dkr.ecr.{aws_region}.amazonaws.com/cohere-agent:v1
>
> COPY agent_config.yaml /app/src/agent_config.yaml
>
> The FROM line pulls the shared base image containing the LangChain agent framework and common dependencies. The COPY line adds the team-specific agent_config.yaml, which controls the following options:
>
> Memory modes – Choose between stateless (NO_MEMORY) or persistent (AGENTCORE) conversation history.
>
> Storage strategies – full_trace for correction workflows or conversation_only for clean history.
>
> Session context caching – Automatically caches skill definitions and documents to avoid redundant Amazon Simple Storage Service (Amazon S3) fetches.
>
> Prompt caching – Can help reduce costs and latency by caching system prompts and frequently used content.
>
> Flexible tool configuration – Enable/disable tools per deployment.
>
> Model configuration – Base model on Amazon Bedrock with configurable token limits, temperature, and other inference parameters.
>
> LiteLLM configuration – Configure LiteLLM as the reverse proxy between the model and the agent.
>
> With the runtime deployed, the next step was connecting it to tools and skills.
>
> Unified tool and skill access with AgentCore Gateway
>
> Cohere Health’s agents access multiple tool types, including AWS Lambda functions for fetching skills and documents, and internal APIs, maintained across different teams. AgentCore Gateway consolidates these behind a single authenticated endpoint, so teams add new tools without redeploying the agent.
>
> AgentCore Gateway architecture
>
> Cohere Health implemented this using AgentCore Gateway with separate targets for shared tools and project-specific tools.
>
> Tool Lambda function structure
>
> AgentCore Gateway invokes an AWS Lambda function for each tool request. The function routes to the correct handler based on the tool name passed in the gateway context.
>
> # jobs/generic-tools-lambda/app.py
>
> import json
>
> from tools.fetch_skill import handler as fetch_skill_handler
>
> # Routing dictionary for tool discovery
>
> TOOL_HANDLERS = {
>
> "fetch_skill": fetch_skill_handler
>
> }
>
> def lambda_handler(event, context):
>
> """Gateway-compliant Lambda handler with MCP routing"""
>
> # Extract tool name from gateway context
>
> tool_name = context.client_context.custom.get('bedrockAgentCoreToolName', '')
>
> # Strip gateway prefix (gateway adds {target}__ to tool names)
>
> if '__' in tool_name:
>
> tool_name = tool_name.split('__', 1)[1]
>
> # Route to appropriate handler
>
> if tool_name not in TOOL_HANDLERS:
>
> return {
>
> "statusCode": 404,
>
> "body": json.dumps({"error": f"Tool {tool_name} not found"})
>
> }
>
> try:
>
> result = TOOL_HANDLERS[tool_name](event)
>
> return {
>
> "statusCode": 200,
>
> "body": json.dumps(result)
>
> }
>
> except Exception as e:
>
> return {
>
> "statusCode": 500,
>
> "body": json.dumps({"error": str(e)})
>
> }
>
> Tool implementation
>
> Each tool handler fetches data from a specific source. The following example retrieves a skill definition from Amazon S3.
>
> # tools/fetch_skill.py
>
> import boto3
>
> import os
>
> def handler(event: dict) -&gt; dict:
>
> """Fetch skill definition from S3"""
>
> skill_id = event.get('skill_id')
>
> if not skill_id:
>
> return {"error": "skill_id required"}
>
> # Use environment variables for configuration
>
> bucket = os.environ.get('SKILLS_BUCKET')
>
> prefix = os.environ.get('SKILLS_PREFIX')
>
> s3 = boto3.client('s3')
>
> try:
>
> response = s3.get_object(
>
> Bucket=bucket,
>
> Key=f"{prefix}/{skill_id}.yaml"
>
> )
>
> content = response['Body'].read().decode('utf-8')
>
> return {"content": content}
>
> except Exception as e:
>
> return {"error": f"Failed to fetch skill: {str(e)}"}
>
> Agent configuration
>
> The agent configuration defines which gateway targets the agent can access and how it authenticates.
>
> # agent_config.yaml
>
> mcp:
>
> gateway_url: {gateway_url}
>
> allowed_targets:
>
> - generic-tools # AIP-maintained tools
>
> - digitization-tools # Project-specific tools
>
> auth_mode: "bearer_token"
>
> With the runtime and tools in place, Cohere Health turned to building the domain expertise layer.
>
> Skills development and evaluation
>
> AI agents need domain-specific knowledge to perform specialized tasks effectively. Generic prompts produce inconsistent results, require extensive token usage, and lack the nuanced understanding that domain experts bring. Each new use case traditionally required rebuilding agent infrastructure from scratch, creating bottlenecks in deployment velocity. A modular skills framework addresses this by decoupling domain expertise from infrastructure. For Cohere Health, this means clinical policy experts can author and refine new skills directly, helping ensure the system supports policy workflows in ways that remain grounded in expert review and governance.
>
> Modular skills framework
>
> Teams deploy new capabilities through modular, versioned skill definitions without rebuilding the agent.
>
> Development workflow
>
> Cohere Health follows a structured workflow to develop and validate each skill before it reaches production.
>
> Evaluation process
>
> Evaluating skills requires collaboration between machine learning engineering and data science. The process starts with reference datasets that contain ground truth outputs for each skill. The team defines success metrics (accuracy, completeness, and consistency) and runs an evaluation suite against these test cases. When a skill fails, the team analyzes the failure mode and iterates on the skill definition before retesting.
>
> After a skill passes the evaluation suite, data science reviews the results against acceptance criteria and approves the skill for production deployment.
>
> After deployment, Arize AI tracks effectiveness metrics in production. Clinical policy analysts annotate sample outputs to catch errors the automated metrics miss. The team monitors for skill degradation over time and uses these data points to prioritize optimization work.
>
> Skill versioning and deployment
>
> Skills move to production through a layered versioning scheme and a staged deployment pipeline.
>
> Dual-layer versioning
>
> Skills use dual-layer versioning: semantic versioning for capability tracking and Amazon S3 object versioning for deployment history. The first layer tracks capability changes in SKILL.md, with each version tagged in git (for example, skill/policy_ingestion/v1.2.3). Amazon S3 object versioning provides the second layer, maintaining immutable history for every upload with rollback capability and separate non-prod/prod buckets.
>
> Deployment flow
>
> Developer commits and opens a PR to develop.
>
> Continuous integration and continuous delivery (CI/CD) packages skill.tar.gz with metadata on merge.
>
> The pipeline uploads to the Amazon S3 non-prod bucket and updates the manifest.
>
> Evaluate in non-prod environment.
>
> Open PR to main.
>
> Deploy to prod with gradual rollout and monitoring.
>
> Results and impact
>
> Through this implementation, Cohere Health achieved measurable improvements across policy digitization speed, deployment velocity, and coverage.
>
> Policy digitization efficiency: Overall time spent on policy digitization reduced by 30 percent, from 2 hours 15 minutes to 1 hour 35 minutes per policy. Cohere Health has digitized thousands of policies to date using manual and semi-automated workflows. The agent-based framework targets further time reduction per policy as it scales across the existing policy library.
>
> Deployment velocity: Full agent deployments in the product decreased from 3–4 months to 2–6 weeks. The reusable ECR base image pattern lets teams stand up a new agent with a minimal Dockerfile, and the modular skills framework means new capabilities ship without rebuilding the agent runtime. The system abstracts DevOps concerns, so traditional machine learning (ML) and data science engineers can deploy agents without extensive coding experience. The policy digitization product runs a single-agent, multi-skill architecture with one agent, a primary skill with a sub-skill, and three reference injections.
>
> Policy coverage: Cohere Policy Studio represents policy content with verbatim text and a standard codified evidence layer, packaged together and available across original policy formats and sources.
>
> “Prior authorization policy review has always demanded an extraordinary level of clinical attention—every word in a policy document can carry downstream consequences for patients. But that attention has historically been split between interpretation and verification: not just understanding what a policy means clinically, but confirming which version of it governed a given decision, and whether that same version is what the health plan published to providers. Those aren’t administrative questions—they’re questions that bear directly on clinical integrity. Amazon Bedrock AgentCore gave us the architecture to address both simultaneously—AI-powered agentic workflows that assist with navigating the interpretive complexity of clinical language, with built-in memory and version tracking that make provenance a first-class concern rather than an afterthought. Structured, versioned policy outputs make the clinical basis of a decision traceable and reviewable by design, and AgentCore’s secure, multi-tenant runtime means we can deliver that capability across every health plan we serve without compromising isolation.”
>
> — Brian Covino, M.D., FAAOS, Chief Medical Officer, Cohere Health
>
> Apply these patterns to achieve similar results: reusable base images for consistent deployments, unified tool access through a single gateway, and modular skills that scale without rebuilding infrastructure.
>
> Future: Connecting policies through a knowledge graph
>
> Building on Cohere Policy Studio’s success with AgentCore, the next evolution introduces an intelligent knowledge graph which is already underway. Working with the AWS Generative AI Innovation Center, Cohere Health prototyped the foundational semantic layer mapping clinical policies to standardized ontologies (UMLS, SNOMED) to support greater interoperability using standardized healthcare terms. Using Amazon Neptune, this grounds policy concepts in a structure that AI can traverse and trace. That graph connects clinical policies with decisioning products across expanded indications.
>
> Enhanced architecture
>
> The knowledge graph layer sits between the policy representation engine and downstream decisioning systems, creating a semantic network that:
>
> Maps relationships between policies, clinical guidelines, medical codes (ICD-10, CPT, HCPCS), drug formularies, and prior authorization criteria across therapeutic areas.
>
> Scales indication coverage by identifying patterns and similarities across clinical domains, so that new policy types deploy rapidly without manual configuration.
>
> Connects policy fragments to multiple decisioning contexts, so that a single policy update propagates correctly across affected authorization workflows.
>
> Key capabilities
>
> As new policies are digitized through AgentCore, the knowledge graph is designed to help identify relevant connections, flag potential conflicts, and suggest reusable patterns to support reviewer and policy team workflows. The graph learns from policy structures across clinical areas, suggesting templates and accelerating time-to-deployment for new indication types from days to hours. Decisioning engines query the knowledge graph using natural language or Fast Healthcare Interoperability Resources (FHIR) resources to retrieve potentially relevant policy fragments with full provenance and version history. The graph also maintains bidirectional links between CMS requirements, AHIP commitments, and internal policy representations, supporting regulatory alignment at scale.
>
> These capabilities deliver comprehensive indication coverage without proportional engineering effort, real-time policy updates across connected decisioning products, automated conflict detection to help prevent inconsistent authorization outcomes, and sub-second policy retrieval for authorization requests.
>
> This knowledge graph foundation supports Cohere Health’s ability to help health plans achieve 80 percent of electronic prior authorization approvals in real time. The graph maintains the security, multi-tenancy, and audit capabilities established in the current AgentCore architecture.
>
> Conclusion
>
> In this post, you learned how Cohere Health used AgentCore and three architectural decisions to reduce AI agent deployment from months to weeks. Three patterns (reusable ECR base images, unified tool access through AgentCore Gateway, and modular skills development) helped Cohere Health support more scalable policy digitization workflows across formats while reducing digitization time by 30%.
>
> The ECR base image pattern alleviates redundant infrastructure work, so teams can deploy new agents with a minimal Dockerfile. Cohere Health can scale the AI system without rebuilding the runtime. The AgentCore Gateway architecture provides a single authenticated endpoint for the tools, whether they’re utilities based on AWS Lambda or OpenAPI services. The skills framework, built on the Agent Skills open standard, separates domain expertise from agent mechanics, supporting rapid iteration with continuous evaluation through Arize AI and clinical policy analysts.
>
> The future of healthcare AI depends on systems that can adapt quickly to changing requirements while maintaining reliability and security. With AgentCore and these architectural patterns, you can build that system today.
>
> To get started with these patterns in your own environment, explore the following resources:
>
> Learn more about Cohere Health and try Cohere Policy Studio.
>
> Read the Amazon Bedrock AgentCore Developer Guide to deploy your first agent runtime.
>
> Set up AgentCore Gateway for unified tool access with MCP compatibility.
>
> Adopt the Agent Skills open standard for maintainable, versioned domain expertise.
>
> Review the AgentCore interfaces guide to choose the right SDK and framework for your use case.
>
> Learn about Cohere Health’s other AgentCore deployment of a medical necessity review agentic assistant in this re:Invent session.
>
> If you’re a startup building production-ready AI agents, AWS Activate provides the credits, technical guidance, and architecture support to help you move from prototype to production. Get started today.
>
> If you have feedback or questions about this post, leave a comment in the comments section.
>
> About the authors
>
> Oleksiy Kononenko
>
> Oleksiy is a Solutions Architect on the State and Local Government team at AWS, where he partners with government agencies to use cloud technologies to improve citizen services. With his previous Healthcare and Life Sciences Startups experience at AWS, he brings a unique builder’s perspective to architecting solutions that solve real-world problems. When not working with customers, you’ll find him exploring new tech or mountain biking.
>
> Kenji Fujita
>
> Kenji is a Staff AI Platform Engineer at Cohere Health, where he has worked for the past six years. Throughout his tenure, he has developed many of the capabilities across the various platforms that the new agent framework is scaling out to support. You can find Kenji suffering while watching the Mets and running in his free time.
>
> Vikas Mehta
>
> Vikas is a Machine Learning Engineer at Cohere Health, where he started as a co-op during his MSCS at UMass Amherst. He is a contributor to the framework outlined in this post. When he’s not working, Vikas enjoys swimming, board games with friends, and exploring parks and restaurants around the city.
>
> Anna Wang
>
> Anna is a Software Engineer at Cohere Health, where she started as an intern during her undergraduate studies at Tufts University. She is a contributor to the framework outlined in this post. Outside of work, Anna’s current obsessions are sourdough and distance running.
>
> Ebad Ahmadzadeh
>
> Ebad is a Principal Machine Learning Engineer at Cohere Health, where he has worked for the past four years. He led research and implementation for many of the ML products at the company. Ebad enjoys learning about music theory, spends time with his family, and goes on dog walks.
>
> Adwait Patil
>
> Adwait is a Machine Learning Engineer at Cohere Health, where he started as a co-op during his MSDS at Northeastern’s Khoury College of Computer Sciences. He has worked extensively on Cohere Policy Studio. Adwait can usually be found hiking or playing badminton or basketball, often using it as the perfect excuse to explore new food spots.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。