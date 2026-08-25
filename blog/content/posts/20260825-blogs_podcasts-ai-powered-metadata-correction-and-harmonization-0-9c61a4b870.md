---
title: "AI-powered metadata correction and harmonization"
date: 2026-08-25T22:06:13+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "生成式 AI", "机器学习", "深度学习", "自然语言处理", "Prompt 工程", "Advanced (300)"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:c3771f0b72a405167c70f1686de3c5a482d6cafe8e4af345e034237e36d48185"
source_payload_sha256: "sha256:2e127d26ef0b420e198a72ecaf639174d90ebb085b6f68024eeb1d9890db8096"
observation_id: obs_9c61a4b87029f19d0ef448a7631f53a090b90225204b7584c56d4a841bbea9d4
event_id: evt_05ddbff2c4ef473d18dae38bbf049f88c2656bf0ae26380ab13cf30004246d9a
revision_id: rev_0a1b52cabaa6d626f2c39a801b29358669c65ab4bc988eb37f2fe033965b18ac
source_published_at: 2026-08-24T15:53:03Z
first_seen_at: 2026-08-25T14:03:45.139169Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: true
source_truncation_reason: "crawler_feed_content_limit"
source_support: 1.0
source_title_chars_original: 48
interpretation_sha256: "sha256:cc58df66087df7346a25326ae018a58c4b957fc1425063de1147941367a6403d"
description: "该内容描述一种基于人工智能的元数据校正与统一工作流，能够自动识别模式不符、语义不一致等问题并生成修正建议。 工作流在自动化处理的基础上加入人工审核环节，以确保领域专家保持最终决策权。"
external_url: https://aws.amazon.com/blogs/machine-learning/ai-powered-metadata-correction-and-harmonization
parent_observation_id: null
last_seen_at: 2026-08-25T14:03:45.139169Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/ai-powered-metadata-correction-and-harmonization](https://aws.amazon.com/blogs/machine-learning/ai-powered-metadata-correction-and-harmonization)
- **发布域名**: aws.amazon.com

## 要点解读

### 这是什么  
该内容描述一种基于人工智能的元数据校正与统一工作流，能够自动识别模式不符、语义不一致等问题并生成修正建议。  
工作流在自动化处理的基础上加入人工审核环节，以确保领域专家保持最终决策权。  

### 用在哪里  
适用于需要跨来源整合并保持格式统一的科研或企业数据管理场景。  
对希望降低人工审查工作量、提升数据互操作性的团队尤为实用。  

### 可以推断的  
推测：在保持人工审批的前提下，这类系统能够显著缩短元数据清洗所需的时间。  
推测：随着自然语言处理技术的进步，自动化校正的准确性可能进一步提升。

## 来源摘要/节选

> As data collection and data generation accelerate, the gap between our ability to produce raw data and our capacity to standardize it continues to widen. Without automation, this gap becomes a critical bottleneck that delays analysis, complicates interpretation, and limits the global value of shared datasets.
>
> Metadata harmonization (standardizing labels, identifiers, and formats so datasets from different sources can work together) remains largely manual. AI-powered metadata correction and harmonization offers a way forward, transforming metadata management from a time-consuming responsibility into a process that scales with your data volume and supports open science rather than obstructing it.
>
> In this post, we demonstrate how AI-powered metadata correction works in practice, explore two implementation approaches (from human-in-the-loop validation to fully autonomous agent-driven workflows), and provide governance considerations for deploying these solutions in your organization.
>
> Metadata correction and harmonization workflow
>
> To address this challenge, we developed a centralized metadata correction and harmonization workflow built on AWS, designed to support consistency, interoperability, and accuracy across disparate metadata sources. The system uses Amazon Bedrock for large language model (LLM)-powered schema alignment and correction recommendations, Amazon Simple Storage Service (Amazon S3) for schema and result storage, Amazon DynamoDB for job tracking, Amazon Cognito for authentication, and Amazon Elastic Container Service (Amazon ECS) for compute. The workflow includes a harmonization package that aligns metadata schemas, validates data integrity, and generates correction recommendations.
>
> The metadata correction and harmonization system operates as a cyclical workflow that guides data through validation, generates recommendations, and returns control to the user for final approval. The following diagram illustrates this high-level flow:
>
> Figure 1: Metadata correction and harmonization workflow
>
> As shown in the diagram, the process begins when users upload their metadata files. The system then performs two parallel validation streams: schema alignment verifies that column structures match expected formats, while metadata field validation examines individual field values for compliance. When issues are detected, the system generates targeted correction recommendations and presents them to the user, who maintains final decision authority over changes. This human-in-the-loop approach lets automation accelerate the process while preserving researcher control and domain expertise.
>
> Schema alignment
>
> The first step in metadata correction is comparing source and target data schemas: verifying that the right columns exist and are properly aligned. Common issues include inconsistent naming conventions (synonyms, misspellings, abbreviations), missing or extra columns, and cases where columns need to be split or combined. Fuzzy string matching can handle basic naming discrepancies, but more complex alignment challenges require a different approach. LLMs available on Amazon Bedrock bring semantic understanding to this problem. Rather than relying on string similarity alone, an LLM-driven approach can recognize industry-specific synonyms, infer meaning from surrounding columns, and detect when a source column should be split into multiple target columns or vice versa. This semantic matching handles the cases that rule-based systems miss.
>
> Metadata field validation
>
> The metadata field validation component checks whether individual field values comply with schema requirements. The system evaluates each field against predefined rules and categorizes failures into three types.
>
> Required field validation identifies mandatory fields that are missing, empty, or whitespace-only. A row missing a required sample identifier, for example, is flagged before further processing occurs.
>
> Enumerated value validation compares field contents against controlled vocabularies defined in the schema. If a field accepts only specific instrument types (such as sequencing systems), values outside that list trigger a validation error. This helps prevent free-form text from introducing inconsistencies in standardized fields.
>
> Pattern validation applies regular expression matching to verify formatting conventions. Date fields might require YYYY-MM-DD format, while identifier fields might need specific alphanumeric patterns. Values that deviate from the expected format are flagged.
>
> Each validation failure is classified and documented with enough context for the recommendation system to generate appropriate corrections. The structured error reports specify the location, type, and nature of each issue.
>
> Metadata field recommendation
>
> When validation errors are detected during metadata field validation, the system generates recommendations using a layered combination of natural language processing (NLP) and AI-based techniques designed to balance cost efficiency, performance, and interpretability. By prioritizing classical NLP and embedding-based similarity before invoking LLMs, the workflow achieves accurate, scalable recommendations while keeping inference costs predictable.
>
> These techniques can operate individually or in sequence within bagging or boosting architectures, dynamically chosen based on confidence thresholds. This adaptive layering lets simpler methods handle routine corrections efficiently, while advanced models resolve only the ambiguous or novel cases that require contextual reasoning.
>
> 1. Semantic similarity through embeddings
>
> Vector embeddings let the system compare metadata values semantically, identifying close matches based on similarity thresholds. This supports precise correction of common variations such as synonyms, abbreviations, or acronyms. For example, the system can map “Human” to “Homo sapiens” or “NYC” to “New York City.”
>
> This approach relies on smaller, efficient embedding models (available on Amazon Bedrock) whose outputs can be cached, providing a cost-effective alternative to LLM-driven reasoning while maintaining accuracy.
>
> We evaluated multiple embedding models, including domain-specific biomedical models and Amazon Titan, to identify the most appropriate fit for this workload. We selected Amazon Titan for its strong performance on general and biomedical metadata tasks, commercial availability, and compatibility with Amazon Bedrock model inference. This makes it well suited for organizations that require a supported, scalable embedding solution without the operational overhead of self-managed domain-specific models.
>
> 2. Contextual inference
>
> Contextual inference lets the system recommend corrections by identifying relationships and shared patterns within the metadata itself. Many datasets exhibit internal consistency where similar rows share structural traits or repeated values across columns. By analyzing these local similarities, the model can infer missing or inconsistent metadata values using only the information present in the current upload, avoiding the need for large external training datasets.
>
> In this implementation, contextual inference operates through a hybrid approach that combines distance-weighted k-nearest neighbors with Term Frequency-Inverse Document Frequency (TF-IDF) feature representations and co-occurrence statistics. Each row in the dataset is converted into a composite vector built from its text, categorical, and numeric fields. Text fields are transformed into TF-IDF representations, categorical values are encoded through one-hot or compact learned representations, and numeric fields are scaled to comparable ranges. The system then measures the similarity between rows using cosine or Euclidean distance and predicts the missing value by performing a weighted vote among the most similar examples, where closer neighbors contribute more influence.
>
> Further refinement is achieved through co-occurrence analysis using Pointwise Mutual Information (PMI), which identifies value combinations that naturally appear together within the dataset. PMI measures statistical association beyond raw frequency, capturing patterns like “when column A contains X, column B typically contains Y.” The final recommendation combines both similarity and co-occurrence signals with configurable weights. This produces stable and explainable recommendations grounded in internal data structure rather than external training, resulting in efficiency and reliability even in small or specialized datasets.
>
> 3. Fuzzy matching
>
> Fuzzy search algorithms such as Levenshtein distance detect and correct typographical or formatting inconsistencies. They are especially effective for resolving errors in manually entered metadata, such as misspellings, spacing, or punctuation differences. Fuzzy matching is typically applied early in the correction workflow to capture low-level inconsistencies before semantic or contextual inference layers are applied.
>
> 4. LLM-based resolution (fallback layer)
>
> When earlier validation methods, including rule-based NLP and embedding similarity models, fail to reach a sufficient confidence level, LLM-based resolution through Amazon Bedrock acts as a fallback layer. These models can reason across complex metadata structures to interpret ambiguous or previously unseen patterns. LLM-based inference is invoked selectively, meaning computationally intensive reasoning is used only when simpler algorithms cannot resolve a field with high confidence. The results are then surfaced for human review to maintain accuracy and traceability in downstream data harmonization.
>
> Summary
>
> The metadata correction and harmonization workflow combines three stages: schema alignment through LLM-powered semantic analysis, field validation using a tiered rule-based approach, and recommendations driven by embeddings, fuzzy matching, and contextual inference. Simpler methods handle routine corrections, while LLM-based resolution serves as a fallback for edge cases that traditional methods cannot resolve.
>
> Prerequisites
>
> Before deploying the application, confirm the following tools are installed:
>
> Node.js 18+ for AWS Cloud Development Kit (AWS CDK) and frontend development.
>
> Python 3.11+ for the API and processor.
>
> AWS Command Line Interface (AWS CLI) configured with credentials that have permissions for Amazon ECS (AWS Fargate), Amazon DynamoDB, Amazon S3, Amazon Cognito, Amazon Virtual Private Cloud (Amazon VPC), AWS Identity and Access Management (IAM), AWS CloudFormation, Amazon Elastic Container Registry (Amazon ECR), and Amazon CloudWatch
>
> AWS CDK Toolkit (npm install -g aws-cdk)
>
> Docker for building container images.
>
> Make for running the provided Makefile commands.
>
> uv Python package manager for dependency management.
>
> node -v # 18 or higher
>
> python --version # 3.11 or higher
>
> aws --version # AWS CLI configured with credentials
>
> Getting started
>
> Step 1: Clone and install dependencies
>
> Clone the repository and install all Python and TypeScript dependencies:
>
> git clone https://github.com/aws-samples/sample-intelligent-metadata-harmonization.git
>
> cd metadata-harmonization
>
> # Create and activate Python virtual environment
>
> make createPythonEnvironment
>
> source .venv/bin/activate
>
> # Install all dependencies (Python packages, TypeScript packages, CDK, frontend)
>
> make install
>
> The make install command installs the processor, API, agent, and evaluation packages as editable Python packages using uv, and runs npm install for the infrastructure and frontend projects.
>
> Step 2: Configure the deployment
>
> Copy the configuration template and edit it with your AWS account details:
>
> cp config.yaml.example config.yaml
>
> Edit config.yaml:
>
> appName: "metadata-harmonization-app"
>
> env: "dev"
>
> dev:
>
> profile: "your-aws-profile"
>
> deploymentName: "metadata-harmonization-dev"
>
> accountNumber: "123456789012" # Your 12-digit AWS account number
>
> region: "us-east-1"
>
> deploymentStage: "dev"
>
> removalPolicy: "destroy"
>
> logLevel: "INFO"
>
> targetPlatform: "linux/amd64"
>
> Validate the configuration:
>
> make validateConfig
>
> Step 3: Deploy infrastructure
>
> Bootstrap AWS CDK (first time only), then deploy:
>
> # First-time setup: prepare your AWS account for CDK
>
> make bootstrap
>
> # Deploy all AWS resources
>
> make deploy
>
> make deploy builds the API container image, pushes it to Amazon ECR, and deploys the AWS CDK stack. This creates Amazon DynamoDB tables, Amazon S3 buckets, an Amazon Cognito user pool, and an Amazon ECS Fargate service.
>
> After deployment, generate a local .env file with the deployed resource identifiers:
>
> make createLocalDotEnvFile
>
> Step 4: Create Amazon Cognito users
>
> After deployment, create users in the Amazon Cognito user pool so they can log in to the application:
>
> Open the Amazon Cognito console.
>
> Select the user pool created by the deployment (for example, metadata-harmonization-users).
>
> Go to Users and choose Create user.
>
> Enter the user’s email address and a temporary password.
>
> Choose Create user.
>
> The user will be prompted to set a permanent password on first login.
>
> Step 5: Run the web application locally
>
> Start both the API server and the Next.js frontend:
>
> # Run both API and frontend together (recommended)
>
> make runLocal
>
> Or run them in separate terminals:
>
> # Terminal 1: API server
>
> make runApiLocal
>
> # Terminal 2: Frontend
>
> make runUiLocal
>
> Access the system at:
>
> Web interface: http://localhost:3000.
>
> API documentation: http://localhost:8080/api/docs.
>
> Step 6: Run the metadata agent
>
> With the API server running, open a second terminal and run the agent:
>
> uv run metadata-agent validate data/synthetic_dataset/simple_test.csv --interactive
>
> The agent connects to the API through the Model Context Protocol (MCP), validates the dataset, retrieves failure reports, and autonomously applies corrections.
>
> Human-in-the-loop
>
> Human oversight remains central to maintaining metadata quality and trust. The metadata correction and harmonization system is designed as a collaborative workflow that keeps data contributors in control of their submissions. The interface provides immediate feedback, recommendations, and actionable corrections, so contributors can validate and approve metadata efficiently while preserving data integrity.
>
> UI flow and interaction
>
> The human-in-the-loop process begins when a data contributor selects and uploads their metadata file through the browser interface. Contributors can inspect and modify metadata locally before initiating validation, allowing pre-submission adjustments using lightweight, client-side tools. When ready, they trigger metadata processing, which sends the dataset to the cloud for automated validation and harmonization. When the workflow executes, one of two outcomes occurs:
>
> A validation pass, where metadata aligns fully with the schema and is emitted downstream for integration.
>
> A validation failure, which generates detailed recommendations for missing or inconsistent fields.
>
> These recommendations surface directly in the interface for review and correction. Contributors can inspect flagged entries, review AI-generated suggestions, and either accept, edit, or reject them. Once satisfied, they resubmit the corrected metadata for revalidation. Successful submissions are automatically confirmed and propagated downstream, completing the harmonization cycle.
>
> Figure 2: Human-in-the-loop metadata correction workflow
>
> Each cycle reduces manual effort while preserving contributor ownership of the final output.
>
> The following video demonstrates how automation and human review coexist in a single streamlined process. Rather than relying on researchers spending days performing manual metadata alignment, the system acts as a collaborative assistant, accelerating corrections while helping validate that records reflect contributor intent and domain expertise.
>
> Title: “Metadata Upload and Validation Workflow” A 90-second demonstration showing the full end-to-end process of metadata upload, validation, and correction through the browser interface.
>
> The human-in-the-loop approach gives researchers the speed of automation without giving up control. AI-generated recommendations surface through the interface, but researchers decide what gets applied. This collaborative model builds trust in the system while keeping domain-specific knowledge central to the correction process.
>
> Agent-driven workflows
>
> While the human-in-the-loop system greatly accelerates metadata harmonization, it still requires active contributor participation in reviewing recommendations, accepting corrections, and resubmitting updates. For datasets involving hundreds or thousands of records, this human effort remains substantial. To reduce that burden and allow contributors to focus on research instead of repetitive metadata correction, the workflow can be extended through agent-driven automation.
>
> From human to agent mediation
>
> In this model, a metadata agent operates as an autonomous or semi-autonomous system capable of analyzing, correcting, and validating metadata records. It uses both deterministic and nondeterministic reasoning systems, ranging from rule-based logic to Amazon Bedrock LLM inference, to identify, resolve, and resubmit corrected metadata. Through MCP, the agent can access a set of specialized tools, including the remote metadata processing service, schema validators, and embedding-based similarity modules. When invoked, the agent can trigger validation, retrieve failure reports and AI-generated recommendations, and decide how to apply corrections based on contextual cues.
>
> Operational flow
>
> The following process illustrates the agent-driven loop, mirroring the same structure as the human workflow but replacing direct user actions with autonomous reasoning.
>
> Figure 3: Agent-driven operational flow
>
> This configuration allows the system to scale metadata curation across large datasets with minimal human intervention while maintaining an auditable correction log.
>
> Contextual awareness and organizational agents
>
> For high-value or domain-specific data, a single general-purpose agent may lack the necessary context. To improve accuracy, organization-specific agents can be deployed, each with access to that group’s private data stores, experiment logs, and research publications. By embedding global context such as ontology usage, experimental methods, and internal naming conventions into the agent’s reasoning prompt, metadata correction becomes both more precise and more consistent with local data standards.
>
> This architecture supports two levels of adaptation:
>
> Local reasoning, where the agent infers missing or ambiguous fields using the immediate dataset and prior submissions.
>
> Contextual enrichment, where the agent draws from broader organizational knowledge such as papers, protocols, and controlled vocabularies to validate and fill metadata fields automatically.
>
> The following demonstration shows an agent executing this workflow in a terminal interface. The agent interacts programmatically with the metadata validation system, using MCP tools to validate a dataset, interpret errors, and autonomously apply corrections before resubmitting.
>
> Terminal 1: Start the API server
>
> # From the project root
>
> make runApiLocal
>
> Terminal 2: Run the agent
>
> # Validation demo (runs a predefined workflow)
>
> uv run metadata-agent validate data/synthetic_dataset/simple_test.csv --interactive
>
> Title: “Autonomous metadata validation through an agent” A 1 minute 38 second demo showing a ReAct-based agent performing end-to-end metadata correction using command line interactions.
>
> Agent-driven workflows move metadata correction beyond human review cycles toward scalable, context-aware automation. By combining deterministic schema validation with LLM-based reasoning and controlled tool access, these agents reduce the repetitive workload on contributors while preserving transparency and accountability. The result is a system that adapts as data standards change and supports large-scale, multi-organization data sharing.
>
> Governance and compliance considerations
>
> Moving from proof-of-concept to production requires governance integrated throughout the development lifecycle. Four areas deserve particular attention.
>
> Data Integrity and Change Tracking: Organizations should establish clear control frameworks for how metadata changes are documented and preserved. Scientific reproducibility depends on maintaining data provenance. As demonstrated in the human-in-the-loop workflow, the system provides change summaries categorized by type and source, supporting review and approval during metadata submission. Institutions should define retention policies, audit trail requirements, and integrity controls appropriate to their regulatory environment.
>
> Architecture Governance: Organizations need to determine how AI recommendations integrate into their data workflows, specifically whether corrections require approval before being applied or can be applied automatically with post-hoc review. This decision affects data integrity, reversal capabilities, and alignment with institutional data policies. Architecture choices should be documented with clear rationale and designed to accommodate evolving standards and growing data volumes.
>
> Responsible AI and Content Safety: Production deployments that use LLM inference should incorporate Amazon Bedrock Guardrails to establish boundaries on model behavior and protect against prompt injection attacks, particularly when metadata values from external sources are passed directly into model prompts. Guardrails can be configured to filter harmful content, enforce topic boundaries, and apply grounding validation. This keeps LLM-generated correction recommendations anchored to the schema definitions and controlled vocabularies defined for the workflow. For agent-driven deployments, Guardrails can also validate against each agent’s autonomous operation boundaries to help prevent unintended corrections from being applied without appropriate oversight.
>
> Security: AI systems handling sensitive genomic data must meet the same security standards as traditional research data systems. Role-based access control, data protection throughout the validation pipeline, and (for agent-driven workflows) boundaries on autonomous operations should all be assessed against the organization’s risk profile.
>
> Cleanup
>
> To avoid ongoing charges, destroy all deployed AWS resources when you are done:
>
> make destroy
>
> This tears down the AWS CDK stack, including Amazon ECS services, Amazon DynamoDB tables, Amazon S3 buckets, and the Amazon Cognito user pool. The command prompts for confirmation before proceeding.
>
> If you set removalPolicy to "retain" in config.yaml (recommended for production), some resources will survive stack deletion. Delete retained Amazon S3 buckets and Amazon DynamoDB tables manually through the AWS Management Console or AWS CLI.
>
> To remove local build artifacts:
>
> make clean
>
> Conclusion
>
> The AI-powered metadata correction and harmonization system presented here addresses a persistent challenge in biomedical research: the time spent on data standardization instead of scientific work. The two implementation approaches, human-in-the-loop validation and agent-driven workflows, provide flexibility for organizations at different stages of AI adoption. Teams can begin with supervised corrections that build confidence in the system, then gradually transition to more automated approaches as trust grows.
>
> This system helps reduce the friction that slows collaboration across organizations. The cloud-native architecture scales with your organization, and the modular design allows customization to meet specific institutional needs. As data volumes continue to grow, automated metadata harmonization becomes increasingly important as organizations scale. Check out our GitHub repo to get started with the solution.
>
> About the authors
>
> Joseph Cottingham
>
> Joseph is a member of the AWS Generative AI Innovation Center, where he designs and delivers AI systems that move organizations from idea to production. His technical background spans firmware, software, and machine learning, with deep expertise in high-throughput, event-driven architectures that keep AI workloads performant at scale. Joseph focuses on the intersection of state-of-the-art research and operational reality, delivering solutions that materially transform organizations and the systems they operate.
>
> Haley Tien
>
> Haley is a Deep Learning Architect at the AWS Generative AI

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。