---
title: "AI-driven development lifecycle using Amazon Bedrock AgentCore"
date: 2026-09-04T02:40:59+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "生成式 AI", "机器学习", "Prompt 工程", "Advanced (300)", "Amazon Bedrock AgentCore", "Technical How-to"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:87ba0ed9a4a1f88c098cdb7c7c1e3243fa481ae2703c1dad7202bab1556bc6f8"
source_payload_sha256: "sha256:54563c10827a5e91d2954057348a95933e230b71bb32b197255762d616b07d24"
observation_id: obs_b5dfb93ee9936b169e4518f3b211559104467f38c21654f28558b834220067ac
event_id: evt_898c7c8da637e947e2c458a6970afb8b4c6aeaf3aecdad52b01d25e16ae09d48
revision_id: rev_477eb15a0b0d5f4f53af105b260f1f65189c7d251ae3f2af683b4ba05efbda23
source_published_at: 2026-09-03T16:16:28Z
first_seen_at: 2026-09-03T18:52:06Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 62
interpretation_sha256: "sha256:c689a929fac2c74b96177387d02909ddaef33cc9ea5a374643833846faddfe5c"
description: "这条内容介绍了基于Amazon Bedrock AgentCore的AI驱动开发生命周期实现方案，包含两个参考案例：一个是从SQL schema自动生成ER图的工具，另一个是多代理架构的代码安全分析系统。"
external_url: https://aws.amazon.com/blogs/machine-learning/ai-driven-development-lifecycle-using-amazon-bedrock-agentcore
parent_observation_id: null
last_seen_at: 2026-09-05T00:00:00Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/ai-driven-development-lifecycle-using-amazon-bedrock-agentcore](https://aws.amazon.com/blogs/machine-learning/ai-driven-development-lifecycle-using-amazon-bedrock-agentcore)
- **发布域名**: aws.amazon.com

## 要点解读

### 这是什么
这条内容介绍了基于Amazon Bedrock AgentCore的AI驱动开发生命周期实现方案，包含两个参考案例：一个是从SQL schema自动生成ER图的工具，另一个是多代理架构的代码安全分析系统。

### 用在哪里
适用于需要自动化代码文档和持续安全检查的工程团队，特别是那些在AWS环境中使用CI/CD流水线并希望将AI能力整合到开发流程中的开发者。

### 可以推断的
推测：由于采用模块化架构，其他团队可以根据自身需求替换或扩展特定组件，而不必采用完整的解决方案。

推测：这类工具的实际应用效果可能与团队现有的文档管理习惯和代码规范程度密切相关。

## 来源摘要/节选

> Engineering teams adopting the AI-Driven Development Lifecycle (AI-DLC) with Amazon Bedrock AgentCore and coding agents like Kiro often struggle with the gap between conceptual frameworks and working code. Amazon Bedrock AgentCore is a service for building, connecting, and optimizing agents at scale with any framework or model. AI-DLC positions AI as a central collaborator across the software development lifecycle, handling routine execution while humans retain oversight of critical decisions. This post closes that gap with working reference implementations.
>
> This post walks through the architecture, design decisions, and key code patterns behind two reference implementations that demonstrate AI-DLC construction phase patterns using Amazon Bedrock AgentCore, Kiro, and local agentic coding tools. The first generates Mermaid entity relationship diagrams from SQL schemas using AgentCore runtime, a capability of Amazon Bedrock AgentCore. The second provides automated code security analysis through a multi-agent architecture that uses AgentCore Gateway, a capability of Amazon Bedrock AgentCore, and AgentCore memory, a capability of Amazon Bedrock AgentCore, along with external tool integrations. Together, they illustrate how to structure AI-driven workflows that maintain human-in-the-loop governance while accelerating delivery. Both implementations link to complete deployment instructions in their respective GitHub repositories.
>
> AI-DLC construction patterns in practice
>
> The AI-DLC construction phase positions AI to propose architecture, generate implementation plans, produce code, and create deployment artifacts, with team members providing clarification on technical decisions in real time. The implementations described here map directly to this pattern:
>
> Automated artifact generation: An agent receives structured input (SQL schema files), creates a detailed plan, generates output (Mermaid ER diagrams), and stores results for human review.
>
> Continuous code quality enforcement: A multi-agent system analyzes code pushed through continuous integration and continuous delivery (CI/CD) pipelines, producing security assessments, Common Vulnerabilities and Exposures (CVE) checks, and policy compliance reports that inform human decision-making.
>
> Both systems share a common architectural foundation built on AgentCore, demonstrating how teams can compose AI-driven workflows from modular, manageable components.
>
> Solution 1: SQL schema to ER diagram generation
>
> This AWS Samples project auto-generates Mermaid ER diagrams from SQL schema files using an agentic AI workflow on Amazon Bedrock AgentCore. After SQL code is checked in by developers, the Amazon Simple Storage Service (Amazon S3) trigger and AWS Lambda function-based workflow invokes the AgentCore runtime, which parses the data definition language (DDL) to produce an .mmd diagram saved back to Amazon S3. It reads only schema metadata (tables, constraints, and foreign keys), never row data, making it a clean reference for schema-to-diagram automation.
>
> Business challenge
>
> Database teams managing evolving SQL schemas need current entity relationship documentation. Manual creation of ER diagrams is time-intensive and documentation frequently drifts from the actual schema. When schema changes land through pull requests, teams need updated diagrams without adding manual documentation steps to the development workflow.
>
> Architecture
>
> The system uses a serverless, event-driven architecture with the following components:
>
> Figure 1: Event-driven architecture for SQL schema to ER diagram generation
>
> S3 event trigger: SQL files uploaded to an Amazon S3 bucket trigger an AWS Lambda function that initiates the analysis workflow.
>
> Authentication: Amazon Cognito provides OAuth2 machine-to-machine (M2M) authentication. Client credentials are stored in AWS Systems Manager Parameter Store.
>
> AgentCore runtime: A containerized agent built with the Strands framework runs on AgentCore runtime. The agent uses Claude Sonnet 4 through Amazon Bedrock to parse SQL DDL statements and generate Mermaid ER diagram syntax. (For model availability by AWS Region, see Regional availability by models.)
>
> AgentCore memory: Provides persistent session context with a 90-day expiry, and supports semantic search across previous analyses and incremental schema understanding.
>
> Output storage: Generated .mmd diagram files are saved to Amazon S3 under a dedicated prefix, with metadata tracking the source file and generation timestamp.
>
> The workflow proceeds as follows:
>
> A SQL file is uploaded to Amazon S3 (manually or through a CI/CD pipeline).
>
> The Lambda trigger reads the file content and authenticates through Cognito OAuth.
>
> The trigger invokes the AgentCore runtime agent with the SQL content as the payload.
>
> The agent analyzes the schema and identifies tables, columns, constraints, and foreign key relationships. It then generates a complete Mermaid erDiagram.
>
> The diagram is saved to Amazon S3 and the analysis session is stored in AgentCore memory.
>
> Implementation details
>
> The agent implementation uses the BedrockAgentCoreApp runtime wrapper with the @app.entrypoint decorator to register the handler:
>
> from bedrock_agentcore.runtime import BedrockAgentCoreApp
>
> from bedrock_agentcore.memory import MemoryClient
>
> from strands import Agent
>
> from strands.models import BedrockModel
>
> app = BedrockAgentCoreApp()
>
> model = BedrockModel(model_id="us.anthropic.claude-sonnet-4-5-20250929-v1:0", region_name="us-west-2")
>
> erdiagram_agent = Agent(model=model)
>
> memory_client = MemoryClient(region_name="us-west-2")
>
> @app.entrypoint
>
> async def generate_er_diagram(payload: Dict[str, Any]) -&gt; Dict[str, Any]:
>
> sql_content = payload.get("sql_content", "")
>
> file_name = payload.get("file_name", "unknown_file.sql")
>
> # Generate diagram, store in memory, save to S3
>
> ...
>
> Key design decisions include:
>
> Chunked processing: Large SQL files are split into manageable segments, analyzed independently, then consolidated into a unified diagram. This handles schemas with hundreds of tables without exceeding context limits.
>
> Structured prompting: The agent uses a systematic analysis prompt that extracts tables, columns, data types, primary keys, and foreign key relationships before generating diagram syntax.
>
> OpenTelemetry tracing: Every step is instrumented with spans and attributes, providing observability into processing duration, chunk counts, and error attribution.
>
> The complete implementation, including OpenAI Codex skills and MCP server integration, is available in the sample-to-create-mermaid-entity-diagrams-from-sql-using-agentic-ai-on-agentcore repository.
>
> Solution 2: Secure software handoffs
>
> This serverless code security analysis solution uses Amazon Bedrock AgentCore to automatically scan Python or Java code for security vulnerabilities, CVE risks in dependencies, and policy violations. The analysis is triggered when code is pushed from a GitLab pipeline to Amazon S3. A Strands-based agent then evaluates the code using Anthropic Claude Sonnet models on Amazon Bedrock. It calls Model Context Protocol (MCP) tools that run on AWS Lambda for CVE and policy checks. (For model availability by Region, see Regional availability by models.) Results, including quality scores from 1 to 10 and recommendations, are stored in AgentCore memory with semantic search and surfaced through a real-time, session-based web dashboard. Amazon Cognito provides authentication, and AgentCore Observability, a capability of Amazon Bedrock AgentCore, and Amazon CloudWatch provide monitoring.
>
> Business challenge
>
> Code reviews for security compliance require specialized knowledge across CVE databases, organizational coding policies, and language-specific security patterns. Manual security reviews create bottlenecks in delivery pipelines, and inconsistent application of standards across teams leads to variable code quality.
>
> Architecture
>
> This solution provides automated code security analysis through a multi-agent architecture for secure software handoffs between development stages:
>
> Figure 2: Multi-agent architecture for automated code security analysis
>
> Code files are uploaded to an Amazon S3 bucket (manually or through a CI/CD pipeline). An AWS Lambda trigger detects new uploads and initiates the AgentCore analysis workflow with OAuth2 authentication.
>
> AgentCore Gateway with MCP tools: The gateway orchestrates calls to external tool integrations:
>
> Policy Check Lambda: Validates code against organization-specific security policies.
>
> CVE Database Check Lambda: Scans dependency files for known vulnerabilities.
>
> AgentCore runtime (Strands framework): The core analysis agent performs deep code review, including structure assessment, logic quality evaluation, memory and performance analysis, security issue detection, and best practices compliance.
>
> AgentCore memory: Stores analysis results with semantic search capabilities, supporting historical comparison and trend analysis.
>
> Dashboard Lambda: Serves a web UI that provides session-based results with search and multi-tab navigation across files, violations, and quality metrics.
>
> Key capabilities
>
> Multi-dimensional analysis: The system evaluates code across structural quality, algorithmic efficiency, security posture, and standards compliance. It produces a quality score with specific recommendations.
>
> Memory strategies: Three distinct self-managed memory strategies serve different needs:
>
> Semantic strategy: Stores detailed code analysis findings, CVE results, and policy violations for retrieval by context.
>
> Summary strategy: Maintains aggregated metrics and trends for dashboard visualization.
>
> User preference strategy: Tracks dashboard layout and filter preferences across sessions.
>
> To learn more, see AgentCore memory strategies.
>
> MCP tool integration through AgentCore Gateway: This capability allows the agent to invoke external tools (policy checker, CVE scanner) as needed during analysis, without hardcoding tool-calling or external API logic into the agent itself.
>
> The analysis agent follows the same AgentCore runtime pattern as Solution 1, with the addition of MCP tool calls routed through AgentCore Gateway:
>
> from bedrock_agentcore.runtime import BedrockAgentCoreApp
>
> from bedrock_agentcore.memory import AgentCoreMemory
>
> from strands import Agent
>
> from strands.models import BedrockModel
>
> app = BedrockAgentCoreApp()
>
> model = BedrockModel(model_id="us.anthropic.claude-sonnet-4-5-20250929-v1:0", region_name="us-west-2")
>
> analysis_agent = Agent(model=model, tools=[analyze_code, check_quality])
>
> memory = AgentCoreMemory(namespace="code-analysis")
>
> @app.entrypoint
>
> async def analyze_uploaded_code(payload: Dict[str, Any]) -&gt; Dict[str, Any]:
>
> file_content = payload.get("file_content", "")
>
> file_name = payload.get("file_name", "unknown.py")
>
> session_id = payload.get("session_id", "")
>
> # Analyze code, store results in memory, return quality score
>
> ...
>
> The agent receives code content from the AWS Lambda trigger, performs multi-dimensional analysis using the foundation model (FM), then invokes external tools (policy checker, CVE scanner) through AgentCore Gateway as needed. Results are persisted to AgentCore memory for dashboard retrieval and historical comparison.
>
> Key design decisions include:
>
> Multi-agent separation: The code analysis agent focuses solely on quality assessment. Policy checking and CVE scanning are delegated to dedicated AWS Lambda functions invoked through AgentCore Gateway, keeping each component single-purpose and independently updatable.
>
> Session-based result persistence: Each analysis run creates a unique session in AgentCore memory. The dashboard retrieves results by session ID, allowing developers to compare quality scores across multiple code submissions.
>
> Gateway-mediated tool invocation: External tools are registered through AgentCore Gateway using MCP rather than direct invocation. This decouples the agent from tool implementation details and allows new tools to be added without modifying agent code.
>
> The complete implementation is available in the sample-agentic-secure-software-handoffs repository.
>
> Integrating local agentic tools: Kiro, OpenAI ChatGPT Codex and Claude Code
>
> While AgentCore provides the cloud runtime for deployed, event-driven agent workloads, the development workflow itself benefits from local agentic tools that implement AI-DLC patterns at the developer’s workstation.
>
> Kiro agents and skills
>
> Kiro supports the AI-DLC inception and construction phases through structured specifications and custom agent skills:
>
> Spec-driven development: Kiro transforms natural language requirements into structured specifications with acceptance criteria, then generates implementation plans from those specifications. This maps directly to the AI-DLC pattern of AI creating plans and seeking human validation before execution.
>
> Custom skills: Teams can define reusable Kiro agent skills that encode organizational standards (coding patterns, security requirements, architectural guidelines), so that AI-generated code consistently meets enterprise quality bars.
>
> Agentic task execution: Kiro’s agent mode handles multi-file implementation tasks with autonomous tool use (file creation, terminal commands, search) while maintaining the human-in-the-loop review at each specification checkpoint.
>
> OpenAI ChatGPT Codex (MCP server and skills)
>
> The repository also includes an OpenAI Codex integration that demonstrates how the same ER diagram generation workflow extends to additional coding agents through MCP and custom skills:
>
> MCP server for live database schema access: A local stdio-based MCP server connects Codex to MySQL or Amazon Aurora MySQL databases through INFORMATION_SCHEMA. The server exposes three tools (schema_summary, generate_er_markdown, and generate_mermaid) that allow Codex to query table structures, columns, indexes, and foreign key relationships without accessing table row data.
>
> Custom Codex skill: A SKILL.md file encodes the ER diagram generation workflow as a reusable Codex skill, guiding the agent through schema analysis and diagram creation with consistent quality.
>
> Secure credential management: Database credentials are retrieved from AWS Secrets Manager with TLS verification enforced, following the same security patterns used in the AgentCore implementation.
>
> Claude Code (local agent)
>
> Claude Code operates as a local command-line agent that complements AgentCore deployments:
>
> Rapid prototyping: Before deploying to AgentCore runtime, developers use Claude Code to iterate on agent logic, test prompts, and validate tool integration patterns locally.
>
> Infrastructure-as-code generation: Claude Code generates deployment scripts, Dockerfiles, AWS Identity and Access Management (IAM) policies, and AWS CloudFormation templates. These artifacts follow architectural specifications produced during the AI-DLC construction phase.
>
> Code review and refactoring: Local agents perform first-pass reviews against project rules and custom instructions, catching issues before code enters the CI/CD pipeline where the secure software handoff system provides the authoritative security analysis.
>
> The combined workflow
>
> A typical AI-DLC bolt (short, intense work cycle) using these tools follows this pattern:
>
> Inception (Kiro): Transform business requirements into specifications with acceptance criteria. The team validates AI-generated specs in a mob elaboration session.
>
> Construction (Claude Code and Kiro): Generate implementation code, deployment scripts, and test suites. Local agents handle file generation and iterative refinement while Kiro manages task orchestration.
>
> Validation (AgentCore): Code pushed through CI/CD triggers automated security analysis. The multi-agent system provides a quality assessment before merge.
>
> Operations (AgentCore): Production agents (like the ER diagram generator) run continuously on AgentCore runtime, triggered by events, processing workloads at scale with full observability.
>
> Best practices
>
> Based on implementing these systems, we recommend the following practices:
>
> Separate agent concerns: Design each agent with a single, well-defined responsibility. The ER diagram agent only generates ER diagrams. Composability comes from orchestration, not from overloading individual agents.
>
> Use AgentCore memory for context continuity: Persistent memory allows agents to learn from previous interactions, compare current analysis with historical baselines, and maintain state across sessions without reprocessing.
>
> Instrument with OpenTelemetry from day one: Tracing provides visibility into agent behavior, processing duration, and failure modes. This is essential for debugging prompt effectiveness and identifying performance bottlenecks.
>
> Store configuration in Parameter Store: Decouple configuration from code. Cognito credentials, memory IDs, model selections, and bucket names should all be retrievable at runtime.
>
> Implement chunked processing for large inputs: Design agents to handle inputs that exceed model context windows by splitting, analyzing independently, and consolidating results.
>
> Secure with Cognito M2M authentication: Use OAuth2 client credentials flow for service-to-service communication. Avoid hardcoded credentials or long-lived tokens.
>
> Integrate through CI/CD, not manual upload: In production, connect agents to repository events (merge requests, pipeline stages) rather than requiring manual file uploads. The S3 trigger pattern shown here translates directly to GitLab webhook or GitHub Actions integration.
>
> Apply Amazon Bedrock Guardrails for production agent outputs: Configure content filtering policies, denied topic detection, and grounding validation to make sure agent-generated responses meet responsible AI standards. For code analysis agents, guardrails can block outputs containing insecure code patterns or hallucinated CVE references. For diagram generation agents, grounding checks validate that outputs accurately reflect the source schema. Combine guardrails with automated evaluation pipelines to continuously monitor agent behavior and flag drift from expected output quality.
>
> Conclusion
>
> The AI-DLC methodology becomes practical when backed by concrete implementation patterns. Amazon Bedrock AgentCore provides the runtime infrastructure (containerized agents, persistent memory, secure gateways, and external tool integration) while local tools like Kiro and Claude Code accelerate the development workflow itself.
>
> Start with the SQL-to-ER-Diagram sample to deploy your first AgentCore agent. Follow the deployment scripts in sequence, then extend the pattern with multi-agent coordination, MCP tool integrations, and CI/CD-driven triggers using the Secure software handoffs sample.
>
> To go deeper, see Move your AI agents from proof of concept to production with Amazon Bedrock AgentCore for a complementary walkthrough of taking agents to production scale. For full-service details, API references, and configuration guidance, refer to the Amazon Bedrock AgentCore documentation.
>
> About the authors
>
> Arghya Banerjee
>
> Arghya is a Sr. Solutions Architect at AWS in the San Francisco Bay Area, focused on helping customers adopt and use the AWS Cloud for big data, data lakes, streaming and batch analytics, generative AI and agentic AI solutions.
>
> Ram Pathangi
>
> Ram is a Sr. Solutions Architect at AWS in the San Francisco Bay Area. He has helped customers in Agriculture, Insurance, Banking, Retail, Health Care &amp; Life Sciences, Hospitality, and Hi-Tech verticals to run their business successfully on AWS cloud. He specializes in Databases, Analytics and ML.
>
> Kunal Ghosh
>
> Kunal is a Sr. Solutions Architect at AWS. He is passionate about building efficient and effective solutions on AWS, especially involving generative AI, analytics, data science, and machine learning. Besides family time, he likes reading, swimming, biking, and watching movies.
>
> Ananth Kommuri
>
> Ananth is a Sr. Solutions Architect at AWS based in the San Francisco bay area. Ananth helps customers achieve operational efficiency with Data analytics, AI/ML, and IoT solutions on AWS.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。