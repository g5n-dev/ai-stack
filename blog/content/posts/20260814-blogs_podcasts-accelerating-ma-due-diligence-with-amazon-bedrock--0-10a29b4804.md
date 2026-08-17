---
title: "Accelerating M&A due diligence with Amazon Bedrock AgentCore"
date: 2026-08-14T05:05:58+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "RAG", "AI Agent", "生成式 AI", "Amazon Bedrock AgentCore", "Intermediate (200)", "Technical How-to", "博客与播客"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:24ffeb6367fcf4a2575f525a778fcbc4607856af2cea0b95a49026834bc3dda3"
source_payload_sha256: "sha256:7e1fb877bb8ab4a36e0fa5bc67aabe9d7a7b171d7da021d75f0828d38b1b76e9"
observation_id: obs_10a29b4804e0e8482f58543b09461165ed139ffe5c09dda6219b0ee18fdea803
event_id: evt_dee7c001a56fdf8ba683bd91f9df25393632e33ed2120b3e84e1a6010623f56f
revision_id: rev_de23b845486ced1f4ebb263a67935233426b478283600b5eef0195fc00b239f0
source_published_at: 2026-08-13T15:52:44Z
first_seen_at: 2026-08-17T17:44:54.982239Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 60
interpretation_sha256: "sha256:8888e6505d4e7fff2b54bd696ac983076114f0b148998e7bbd5a594d7c28b4a0"
description: "使用 Amazon Bedrock AgentCore 构建多代理尽职调查方案，通过自主查询财务、市场和法规数据源，并结合检索增强生成与治理控制，实现并购目标的快速评估与审计追踪。"
external_url: https://aws.amazon.com/blogs/machine-learning/accelerating-ma-due-diligence-with-amazon-bedrock-agentcore
parent_observation_id: null
last_seen_at: 2026-08-17T00:00:00Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/accelerating-ma-due-diligence-with-amazon-bedrock-agentcore](https://aws.amazon.com/blogs/machine-learning/accelerating-ma-due-diligence-with-amazon-bedrock-agentcore)
- **发布域名**: aws.amazon.com

## 要点解读

### 这是什么
使用 Amazon Bedrock AgentCore 构建多代理尽职调查方案，通过自主查询财务、市场和法规数据源，并结合检索增强生成与治理控制，实现并购目标的快速评估与审计追踪。

### 用在哪里
适合并购团队、投行、律师事务所以及企业内部审计部门在需要对大量目标进行筛选、分析和合规检查的场景，尤其是运输物流等行业的案例研究。

### 可以推断的
推测：系统能够在数小时内完成原本需要数周的分析师检索与汇总工作，显著提升效率。  
推测：内置的引用校验和运行时策略控制能够满足合规团队对信息来源可追溯性的要求。

## 来源摘要/节选

> Mergers and acquisitions (M&amp;A) teams face a persistent challenge: conducting thorough due diligence on multiple acquisition targets while maintaining speed and analytical rigor. Teams often spend weeks manually reviewing targets before identifying viable opportunities. Amazon Bedrock AgentCore is a platform to build, connect, and optimize agents at scale, with any framework or model. It can accelerate this process by orchestrating AI agents that handle data gathering, analysis, and compliance checks autonomously within defined guardrails.
>
> In this post, we show how to build a multi-agent due diligence system on Amazon Bedrock AgentCore. We present a reference architecture that combines agent orchestration, knowledge retrieval, and governance controls, then walk through deploying and running the solution using a complete sample repository.
>
> The M&amp;A due diligence challenge
>
> In transportation and logistics, for example, analysts pull data from financial databases, market research applications, regulatory filings, and internal knowledge bases, then reconcile that information by hand. The process is slow and resource intensive.
>
> The problem compounds when teams duplicate work. Industry research, valuation models, and competitive analyses get recreated for each new deal instead of building on institutional knowledge from prior transactions. Meanwhile, governance concerns slow AI adoption because legal and compliance teams require confidence that AI-generated insights are accurate, traceable, and supported by source citations.
>
> These four pressures (slow cycles, fragmented data, duplicated effort, and governance requirements) create an opportunity for AI agents to fundamentally change how due diligence operates.
>
> How AI agents transform due diligence
>
> AI agents address each of these challenges through a combination of autonomous data gathering, intelligent routing, persistent memory, and built-in auditability.
>
> On the data-gathering front, agents autonomously query multiple sources (financial databases, knowledge bases, market data APIs) and synthesize the results into preliminary assessments. In our testing, work that previously required weeks of analyst time was completed in hours because the agent handles the repetitive search-and-summarize loop without human intervention.
>
> For prioritization, agents evaluate opportunities against strategic criteria and route high-priority deals to the right specialists. Rather than reviewing every target sequentially, the system surfaces the most promising candidates first and flags the specific dimensions (financial performance, strategic fitness, compliance risk) that warrant deeper analysis.
>
> Agents also build institutional knowledge over time. Each completed analysis enriches a shared memory layer so that future deals benefit from prior research, valuation assumptions, and integration lessons. Teams stop recreating context from scratch.
>
> Governance is built into the agent workflow from the start, not added as an afterthought. The system is configured so that each assertion the agent emits is grounded in a citation, validated by the citation-check evaluator. Each agent invocation produces an audit trail, and guardrails enforce organizational policies at runtime. Compliance teams can trace each cited claim back to its source document.
>
> Architecture decision: integrated suite or custom build
>
> We present two implementation paths, each suited to different organizational needs.
>
> Option 1: Amazon Quick (integrated solution)
>
> Amazon Quick provides ready-to-use AI capabilities tailored for business intelligence and research workflows. It offers a fast path to production if your needs align with standard analysis patterns. Amazon Quick Research generates professional, exportable in-depth reports. Amazon Quick Flows automates repetitive tasks with pre-built workflows. Amazon Quick Index delivers unified search across connected data sources.
>
> Choose Amazon Quick if you want to deploy rapidly, your workflows align with standard business intelligence patterns, and you prefer fully managed services over custom development. For additional information and reference architecture, see the Announcing Amazon Quick.
>
> You can also extend Quick with custom Amazon Bedrock AgentCore agents for specialized requirements such as proprietary valuation models or strategic fit frameworks. For a practical example of this pattern, see Building Intelligent Contract Management with Quick and AgentCore. That post demonstrates how Amazon Quick handles document management and the user interface while Amazon Bedrock AgentCore powers specialized agent collaboration.
>
> Option 2: Custom architecture with Amazon Bedrock AgentCore
>
> Amazon Bedrock AgentCore gives you fine-grained control over agent behavior, memory, and coordination. This approach suits M&amp;A teams with proprietary methodologies, complex multi-agent coordination requirements, integration with specialized internal systems, or a need for complete control over agent behavior and model selection.
>
> The remainder of this post explores this custom architecture in detail using a transportation-and-logistics due diligence scenario as context. We deploy a working multi-agent system, invoke it against synthetic targets, and validate outputs through an automated citation-check evaluator.
>
> Reference architecture
>
> For M&amp;A teams choosing the custom path, the following reference architecture shows how the pieces fit together end to end.
>
> Figure 1: Multi-agent M&amp;A due diligence architecture with Amazon Bedrock AgentCore
>
> The architecture uses Amazon Bedrock AgentCore to orchestrate a multi-agent due diligence workflow. A supervisor agent coordinates four specialist agents, each responsible for a distinct phase of the due diligence process. Users interact through a Jupyter notebook or terminal interface, while AgentCore runtime manages agent execution and collaboration. The system combines Retrieval Augmented Generation (RAG), structured financial analysis, external tool integration, memory, and policy-based governance to support production-ready due diligence workflows.
>
> Agent orchestration layer
>
> Amazon Bedrock AgentCore runtime coordinates multiple specialized agents through the Strands Agents SDK. The supervisor agent uses the agents-as-tools pattern to route requests to domain-specific specialists based on task requirements.
>
> The Target Screening Agent identifies acquisition candidates by converting natural-language queries into SQL and executing them against Amazon Aurora PostgreSQL. When analysts ask for “mid-market logistics companies with revenue between 100M and 500M USD and EBITDA margins above 12 percent,” the agent translates that into a parameterized query. It then retrieves matching rows and enriches the results with narrative context from the knowledge base.
>
> The Financial Analysis Agent performs valuation analysis using structured and unstructured data sources. It applies standard valuation methodologies including discounted cash flow (DCF) analysis and comparable company analysis, pulling market multiples through an AgentCore Gateway-backed tool. The agent generates preliminary valuations with supporting assumptions documented inline and flags management projections that diverge from historical performance.
>
> The Strategic Fit Agent evaluates integration risks, synergies, and organizational alignment. It retrieves context from prior transactions stored in AgentCore memory (using a dedicated prior_deals namespace). It then compares the current target’s profile against completed acquisitions and identifies integration risks with citations to source memos.
>
> The Compliance Validation Agent audits responses against the M&amp;A governance checklist. It invokes a custom citation-check evaluator (implemented as an AWS Lambda function) that examines every factual claim in a response and flags assertions that lack a supporting source citation.
>
> Key architecture components
>
> The architecture combines structured and unstructured enterprise data to ground agent responses in verified sources.
>
> Amazon Aurora PostgreSQL Serverless v2 stores structured financial and operational datasets. The Target Screening Agent generates SQL from natural language and executes queries through the RDS Data API, providing fast access to target-company metrics without requiring analysts to write SQL themselves.
>
> Amazon Bedrock Knowledge Bases, the fully managed RAG capability in Amazon Bedrock, indexes due diligence documents including confidential information memoranda (CIMs), financial statements, press packs, and internal governance checklists. Agents retrieve relevant passages and cite them inline.
>
> AgentCore Gateway, a capability of Amazon Bedrock AgentCore, lets agents securely interact with external tools and services through Model Context Protocol (MCP)-compatible integrations. In this architecture, agents invoke an AWS Lambda-based market data service through the gateway, with Cedar policies enforcing deterministic access controls over tool usage and agent interactions.
>
> AgentCore memory maintains contextual state and reusable institutional knowledge across interactions. Session memory preserves conversation continuity, while a long-term prior_deals namespace stores lessons from completed acquisitions that inform future analyses.
>
> AgentCore Evaluations, a capability of Amazon Bedrock AgentCore, uses Lambda-based evaluators to automatically validate output quality, citation accuracy, and domain-specific criteria. The citation-check evaluator returns a structured pass/fail result with counts of supported and unsupported claims.
>
> Amazon Bedrock Guardrails enforces safety and response controls throughout the workflow, applied at the supervisor level so specialist outputs pass through organizational policy checks.
>
> Every invocation produces an Amazon CloudWatch log stream and an AWS X-Ray trace that captures the full supervisor-to-specialist-to-tool call hierarchy, providing end-to-end observability.
>
> Security
>
> M&amp;A due diligence involves some of the most sensitive data a company handles: unreleased financials, deal terms, and integration plans. Security is therefore a first-class part of the architecture. Every IAM permission the agents can invoke is scoped to a specific Amazon Resource Name (ARN) rather than a wildcard. The AgentCore Gateway market-data tool goes a step further with a Cedar policy engine that enforces default-deny, attribute-based authorization. The tool runs only when the requested industry code matches an approved vertical. Everything else is denied before it runs. The database tier lives in private, internet-isolated subnets behind virtual private cloud (VPC) endpoints. Data stores are encrypted at rest with KMS, and Amazon Bedrock Guardrails screen every supervisor response for harmful content and personalized financial advice. This layered model of IAM, Cedar, network isolation, and encryption covers different failure modes for systems that handle confidential deal data.
>
> Deploy and run the sample
>
> The complete reference implementation is available in the M&amp;A Due Diligence Multi-Agent Sample repository. It ships with synthetic data (no real companies, financial data, or personally identifiable information), one-command deployment, and a Jupyter notebook walkthrough. The estimated cost for a full deploy-run-cleanup cycle is under USD $5.00.
>
> Prerequisites
>
> Before deploying, verify you have:
>
> An AWS account with Amazon Bedrock model access enabled for Anthropic Claude and Amazon Nova. For model availability by AWS Region, refer to Supported models by AWS Region in Amazon Bedrock.
>
> AWS Command Line Interface (AWS CLI) v2.15 or later.
>
> Python 3.11 or later.
>
> Node.js 20 or later.
>
> AWS Cloud Development Kit (AWS CDK) v2 (npm install -g aws-cdk).
>
> You don’t need Docker installed locally. The agent container image is built on AWS CodeBuild.
>
> Deploy to one of the supported Regions: us-east-1, us-west-2, ap-southeast-2, or eu-central-1.
>
> Step 1: Deploy the stack
>
> Clone the repository and run the deploy script. First-time deployment takes 20–25 minutes.
>
> # macOS / Linux
>
> git clone https://github.com/aws-samples/sample-ma-due-diligence-agentcore.git
>
> cd sample-ma-due-diligence-agentcore
>
> ./deploy.sh
>
> # Windows
>
> git clone https://github.com/aws-samples/sample-ma-due-diligence-agentcore.git
>
> cd sample-ma-due-diligence-agentcore
>
> .\deploy.ps1
>
> The deploy script verifies your Region and model access, creates a virtual environment, runs cdk deploy --all, seeds synthetic data, and executes a post-deploy smoke test. It also installs the project in editable mode, which registers the mna command-line tool that you use to invoke agents in the next step.
>
> Step 2: Invoke the agents
>
> Use the mna CLI to send prompts to individual specialists or let the supervisor route across them:
>
> # Let the supervisor orchestrate across specialists
>
> mna invoke supervisor "Screen the mid-market logistics targets with revenue 100M-500M, then run a DCF on the top hit." --session-id walkthrough-session-00000000-0001
>
> # Target Screening: text-to-SQL on Aurora + KB narrative enrichment
>
> mna invoke target_screening "Screen the target pipeline for transportation companies with revenue between 100M and 500M USD, EBITDA margin above 12%, and fleet size above 200. Surface the top three and tell me what the CIM says about the leader's growth trajectory." --session-id walkthrough-session-00000000-0001
>
> # Financial Analysis: KB retrieval + Gateway-backed market data tool
>
> mna invoke financial_analysis "Run a DCF on Example Corp using the CIM in the knowledge base. Flag any management projection that diverges from historical performance by more than 20% and pull comparable multiples for transportation-logistics mid-market." --session-id walkthrough-session-00000000-0001
>
> # Strategic Fit: AgentCore Memory long-term retrieval
>
> mna invoke strategic_fit "Compare Example Corp' integration profile against our three most recent completed acquisitions. Identify the top three integration risks and cite the source memos." --session-id walkthrough-session-00000000-0001
>
> Every invocation prints a trace_id in its footer. Use mna trace &lt;trace_id&gt; to inspect the full X-Ray trace for that call.
>
> Step 3: Validate outputs with the evaluator
>
> The mna evaluate subcommand runs the citation-check evaluator against a specialist’s output:
>
> # Capture a response in JSON format
>
> mna --json invoke financial_analysis "Run a DCF on Example Corp using the CIM." --session-id blog-demo-session-00000000-000002 &gt; run.json
>
> # --session-id accepts any string between 33 and 256 characters --- AgentCore Runtime enforces this length range for runtimeSessionId. The value above is just an example; use a unique string per session (a UUID works well) if you want to keep invocations isolated or omit --session-id entirely to let the client generate one for you.
>
> # Extract response text and citations
>
> python -c "import json,pathlib;d=json.loads(pathlib.Path('run.json').read_text());pathlib.Path('response.txt').write_text(d['text'])"
>
> python -c "import json,pathlib;
>
> d=json.loads(pathlib.Path('run.json').read_text());
>
> pathlib.Path('citations.json').write_text(json.dumps(d['citations']))"
>
> # Run the citation-check evaluator
>
> mna evaluate --response-file response.txt --citations-file citations.json
>
> The evaluator returns a structured result indicating pass or failure, with counts of total claims, supported claims, and any unsupported assertions. The exit code is 0 on pass and 1 on fail, making it composable in CI pipelines.
>
> Step 4: Explore the notebook
>
> For a guided, cell-by-cell tour of the same workflow:
>
> jupyter lab notebooks/walkthrough.ipynb
>
> The notebook walks through environment validation, data overview, one cell per specialist agent (with rendered responses and citations), and trace inspection.
>
> Clean up
>
> To avoid ongoing charges, destroy all deployed resources as soon as you finish exploring:
>
> # macOS / Linux
>
> ./cleanup.sh
>
> # Windows
>
> .\cleanup.ps1
>
> The cleanup script runs cdk destroy --all --force to tear down every stack in reverse dependency order. It then executes a verification sweep that scans for orphaned resources:
>
> S3 buckets matching mna-*.
>
> ECR repositories matching mna-*.
>
> Amazon Bedrock Knowledge Bases with mna in the name.
>
> AgentCore runtimes, memories, and gateways.
>
> AWS CloudFormation stacks starting with Mna.
>
> The verification script prints copy-paste commands for resources it finds so you can confirm a zero-cost end state. If the script output is empty for every sweep, all billable resources have been removed. For additional details on CDK resource cleanup, see the AWS CDK documentation.
>
> Next steps
>
> We encourage you to extend this architecture for your own use cases. Here are several paths forward:
>
> Add a production front end. The Full-Stack Starter Template for AgentCore (FAST) provides a React-based UI, Amazon Cognito authentication, and Amazon CloudFront distribution that integrates directly with AgentCore runtime.
>
> Build additional specialist agents. The sample’s CONTRIBUTING.md documents the file layout, Strands pattern, and supervisor registration process for adding new agents (for example, a regulatory-filing agent or an ESG-scoring agent).
>
> Explore advanced orchestration. The Strands Agents SDK supports multiple coordination approaches including agents-as-tools, swarms, and agent graphs. The multi-agent collaboration patterns documentation covers each approach in detail.
>
> Connect additional data sources. AgentCore Gateway supports HTTP APIs, MCP servers, and Amazon API Gateway targets beyond the single Lambda tool demonstrated here.
>
> Conclusion
>
> In this post, we showed how to build a multi-agent system on Amazon Bedrock AgentCore that automates M&amp;A due diligence in transportation and logistics. We walked through the architecture that coordinates specialized agents for target screening, financial analysis, strategic fit assessment, and compliance validation. We then deployed the working sample and invoked it against synthetic acquisition targets.
>
> The reference implementation demonstrates how each architectural layer (agent orchestration, knowledge retrieval, structured data access, institutional memory, and automated evaluation) contributes to a system that is both capable and auditable. The patterns shown here extend naturally to other due diligence domains including healthcare, financial services, and technology acquisitions.
>
> To get started, clone the sample repository, deploy the stack in your AWS account, and try modifying a specialist agent or adding a new one. The FAST template provides the path from this sample to a hosted application with authentication, observability, and a polished UI.
>
> Resources
>
> Amazon Bedrock AgentCore
>
> M&amp;A Due Diligence Multi-Agent Sample – GitHub repository
>
> About the authors
>
> Anand Komandooru
>
> Anand is a Principal Solutions Architect on the Well-Architected AI team at AWS, where he focuses on AI-driven architecture guidance for agentic systems. He has over 20 years of experience building software and previously spent four years helping customers design and deliver cloud-native applications in AWS Professional Services.
>
> Sachin Doshi
>
> Sachin is a Senior Application Architect in AWS Professional Services. He helps customers design and build production-ready solutions using generative AI, serverless architectures, and cloud-native AWS services. He is based in the New York metropolitan area.
>
> Ray Elkins
>
> Ray is a Senior Solutions Architect at Amazon Web Services. With 15 years of enterprise cloud and security experience, he partners with customers to solve complex security and compliance challenges on AWS. Ray focuses on the intersection of agentic AI and cloud security, helping customers adopt frontier agents to automate threat detection and response at scale.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。