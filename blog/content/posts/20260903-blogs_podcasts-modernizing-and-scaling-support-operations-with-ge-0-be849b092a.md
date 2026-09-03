---
title: "Modernizing and scaling support operations with generative AI on AWS"
date: 2026-09-03T02:45:09+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "RAG", "AI Agent", "生成式 AI", "机器学习", "自然语言处理", "Advanced (300)", "Customer Solutions"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:0c292bad371c7c6e7e141cdd70eaa1b16290fbd4f1333c4f48c607bca5461205"
source_payload_sha256: "sha256:bdae6506b98d10e01171cee09b565e827f212faa44e8e885e3af50b201f18d48"
observation_id: obs_be849b092a65b95dd81a8834fc8814c0756e5b23f029f2f0644c2b1a51f8c4c4
event_id: evt_068def15f5b93caf9ac2bde496b462838a6fd2ee372ec6a41e7f5890ac6c6841
revision_id: rev_356829348ac540956c8e940749e2d255b430c1e7fe8910d281ef06cd61bfd7a2
source_published_at: 2026-09-02T18:26:35Z
first_seen_at: 2026-09-02T18:55:15Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: true
source_truncation_reason: "crawler_feed_content_limit"
source_support: 1.0
source_title_chars_original: 68
interpretation_sha256: "sha256:62c8bcf885ef6b77879a330c306e2ffb1c76f931b004501ad527d2213f88525b"
description: "该内容描述了利用生成式 AI 在云平台上捕获分散的操作知识、自动为工单提供指引、利用机器学习预测工作负载与 SLA 风险，并通过工作流实现标签、评论、状态更新等常规任务的自动化，同时保留人工审查以确保准确性。"
external_url: https://aws.amazon.com/blogs/machine-learning/modernizing-and-scaling-support-operations-with-generative-ai-on-aws
parent_observation_id: null
last_seen_at: 2026-09-03T00:00:00Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/modernizing-and-scaling-support-operations-with-generative-ai-on-aws](https://aws.amazon.com/blogs/machine-learning/modernizing-and-scaling-support-operations-with-generative-ai-on-aws)
- **发布域名**: aws.amazon.com

## 要点解读

### 这是什么
该内容描述了利用生成式 AI 在云平台上捕获分散的操作知识、自动为工单提供指引、利用机器学习预测工作负载与 SLA 风险，并通过工作流实现标签、评论、状态更新等常规任务的自动化，同时保留人工审查以确保准确性。

### 用在哪里
适用于需要处理大量客户服务请求、追求更快响应速度并满足严格服务等级协议的企业；尤其适合已有跨部门流程但缺乏统一知识管理的中大型组织，以及希望借助 AI 辅助提升运维或客服效率的技术团队。

### 可以推断的
推测：该方案通过把非结构化的操作记录、培训视频等转化为可检索的知识片段，能够在一定程度上缓解“知识孤岛”导致的重复查询和对个人经验的依赖。  
推测：在实际落地时，需要对工单数据进行标准化并持续更新知识库，否则自动生成的指引可能因信息陈旧而失去效用。

## 来源摘要/节选

> Scaling support operations requires handling rising ticket volumes, meeting strict Service Level Agreements (SLAs), adapting to evolving compliance requirements, and maintaining documentation that quickly becomes outdated, all without proportional increases in headcount. In many teams, the knowledge required to resolve tickets is fragmented across SOPs, recordings, and tribal expertise, forcing analysts to spend significant time searching for guidance instead of resolving issues.
>
> To address these constraints, teams can use generative AI on AWS to capture knowledge from operational workflows, apply it during ticket resolution, and surface risks before they impact SLAs. Rather than optimizing individual tickets or documents in isolation, this approach focuses on improving the underlying processes that determine how work flows across teams. This post demonstrates how you can design and implement a generative AI-based support operations solution on AWS that automates Standard Operating Procedure (SOP) creation from training videos, applies Retrieval Augmented Generation (RAG) to guide ticket resolution, and uses machine learning (ML) to optimize workload distribution and predict SLA risk. The solution also automates operational tasks such as ticket tagging, commenting, and status updates through agentic workflows, while maintaining human in the loop for control and accuracy. This post illustrates the architecture through a real-world operational use case, and shows how the solution can be adapted for other industries, such as financial services, healthcare, logistics, manufacturing, and energy.
>
> The operational challenge
>
> Enterprise support operations rely on process knowledge. However, as organizations grow, that knowledge becomes fragmented across documentation, people, and tools. The result is not a single failure point, but a chain of small inefficiencies that compound into slow resolution, inconsistent quality, and reactive decision-making.
>
> Documentation exists, but knowledge does not persist
>
> Support teams maintain hundreds or thousands of SOPs describing how to handle requests, approvals, and system changes. However, these are typically developed on an as-needed basis for specific functions, not designed from a systems perspective. Each team documents its own slice of the process without visibility into how that work connects to upstream inputs, downstream handoffs, or cross-functional dependencies. The result is documentation that covers individual tasks but rarely reveals how work actually flows end to end. When processes change, updates happen locally (if they even happen), widening the gap between what’s documented and what’s real. At the same time, most operational knowledge is shared through training calls, walkthroughs, and troubleshooting sessions. After the meeting ends, the knowledge remains locked inside long recordings. Months later, teams often rewatch past sessions just to reconstruct how a task was performed. Instead of accumulating knowledge, organizations repeatedly rediscover it. For documentation to remain accurate, teams must capture knowledge directly from operational activity and preserve it in a structured, searchable format.
>
> Tickets arrive faster than guidance can be found
>
> Every incoming ticket must be interpreted and matched to the correct procedure before work can begin. When tickets arrive faster than analysts can process them (a violation of takt time principles from Lean Six Sigma), the system accumulates backlog and delays compound. Analysts spend significant time searching for SOPs across wikis, shared drives, chat threads, and recordings to determine the right steps. Even when the right SOP is found, it typically covers only one function’s view of the process. Analysts must mentally stitch together multiple documents, tribal knowledge, and past experience to reconstruct the full resolution path, a task that depends heavily on individual expertise rather than organizational design. In many instances, tickets bounce back because the wrong issue was addressed or the resolver did not have the complete picture. In practice, only a portion of procedures are formally documented. The remainder exists as tribal knowledge held by a small number of experienced analysts. Junior staff rely on escalation, while senior staff become bottlenecks for routine questions. Instead of requiring people to locate instructions manually, the system must identify guidance automatically from the content of the request itself.
>
> Work is executed, but the process is invisible
>
> Even when tickets are handled successfully, teams rarely see how work actually flows across roles and systems. Some requests require multiple approvals and cross-team coordination, while others are resolved in minutes. From the outside, both appear as simple tickets. Without visibility into handoffs and dependencies, managers cannot distinguish between high workload and high complexity. Work distribution becomes uneven, analysts carry disproportionate load, and mentoring replaces standardization. Improving consistency requires visibility into how work moves through the organization, not just how many tickets exist. This invisibility is a direct consequence of how SOPs are created, function by function, without mapping the end-to-end process. When documentation doesn’t reflect the full workflow, neither can the operational view.
>
> Priorities are often identified too late
>
> Service targets depend on recognizing which tickets are risky before they breach deadlines. However, while priority is often automatically assigned within customer relationship management (CRM) systems based on impact and urgency, these inputs are typically assessed by analysts from ticket details rather than derived from measurable indicators. This challenge is compounded by data quality at intake: when a significant portion of tickets enter the system with inaccurate or incomplete information, even experienced analysts struggle to assess true urgency. High-impact (or high visibility) requests therefore compete with routine ones until delays become visible. Teams often discover problems only after performance metrics decline. By the time escalation occurs, the breach has already happened. To operate proactively, teams need early signals indicating which requests are most likely to miss targets.
>
> Leaders see reports, not operations
>
> Over time, fragmented knowledge, uneven workload, and reactive prioritization reinforce each other. Expertise concentrates in a few individuals, onboarding slows, and scaling requires adding people rather than improving process efficiency. Leaders typically rely on retrospective reporting to understand performance. However, reports explain what happened, not what is about to happen. Without continuous operational visibility, bottlenecks are discovered late and capacity decisions are delayed. Scaling support operations therefore requires visibility into how process design decisions (SOP structure, approval paths, handoff points) translate into operational outcomes like resolution time, SLA risk, and rework rate. That means real-time operational insight and guidance, not just historical metrics.
>
> Solution overview
>
> To address the limitations of manual documentation, fragmented ticket handling, and reactive workload management, the solution integrates execution and analytics into a single operational system on AWS.
>
> The solution is organized into two tightly coupled layers: an operational intelligence workspace used by analysts for day-to-day work, and an analytics and decision intelligence layer used by both analysts and leaders for real-time insight and optimization. This second layer surfaces actionable intelligence directly within the workflow, so front-line analysts understand the true impact and urgency of each ticket based on connected data streams, while also providing leaders with an aggregated view for monitoring performance and guiding decision-making.
>
> Figure 1: End-to-end architecture of the support operations solution on AWS
>
> 1. Operational intelligence workspace (Amazon Bedrock and AWS Strands Agents SDK) – This layer serves as the primary execution environment for analysts and operators, bringing together documentation, ticket analysis, and value stream intelligence in a unified interface. It consists of three core capabilities:
>
> 1.1 Video-to-SOP:The tool automatically converts training recordings and system walkthroughs into structured SOPs through a multi-step pipeline of model invocations on Amazon Bedrock. Then it transforms visual context, spoken instructions, and interface interactions into step-by-step procedures with embedded screenshots and validation guidance.
>
> 1.2 Ticket analyzer:This component analyzes incoming tickets using natural language processing, semantic retrieval, and RAG to identify relevant procedures and generate contextual resolution guidance. The system combines retrieved SOPs and policy documents with foundation models on Amazon Bedrock to generate accurate recommendations aligned with organizational standards. In addition, it uses agentic workflows built with the AWS Strands Agents SDK, where multiple autonomous agents collaborate to perform operational tasks such as ticket tagging, commenting, and status updates. It executes these actions within a human-in-the-loop framework to support accuracy, control, and compliance.
>
> 1.3 Value stream intelligence:Resolution workflows are presented as interactive swim lane maps that show how work moves across teams and systems, highlighting bottlenecks for continuous improvement. It connects datasets across upstream and downstream processes. Stakeholders can quickly identify delays, approval friction, and coordination gaps.
>
> 2. Analytics and decision intelligence layer (Amazon Quick) – The analytics layer provides leaders with centralized visibility into workload distribution, ticket volumes, and SLA risk through dashboards built on Amazon Quick. It empowers teams to monitor operational health, identify emerging risks, and prioritize work proactively. This layer consists of three core capabilities:
>
> 2.1 Workload management and capacity visibility: The dashboards show how tickets are distributed across analysts by volume and complexity, using availability indicators and trend views to highlight overload and underutilization.
>
> 2.2 ML-based ticket categorization and SLA risk prediction: ML models group tickets into functional categories and assign SLA risk scores, surfacing high-risk cases so teams can prioritize based on predicted impact.
>
> 2.3 Embedded agentic experience: An intelligent Amazon Quick agent delivers actionable recommendations for workload rebalancing and prioritization, which are reviewed and executed through supervised workflows with full audit trails.
>
> Critically, these layers are not independent. They form a compounding loop. Video-to-SOP captures process knowledge that was previously locked in recordings and tribal expertise. The ticket analyzer applies that structured knowledge to guide real-time resolution. The value stream intelligence reveals end-to-end workflow patterns that were not visible when SOPs were written function by function. Each resolved ticket and each new SOP strengthens the knowledge base, making the next resolution faster and more accurate. Over time, the system shifts from documenting what happened to anticipating what should happen next.
>
> The following sections describe the technical design behind each component, and explain how they integrate into a unified, production-ready architecture on AWS.
>
> 1. Operational intelligence workspace (Amazon Bedrock and AWS Strands Agents SDK)
>
> The operational intelligence workspace consists of three core capabilities: video-to-SOP, ticket analyzer, and value stream intelligence.
>
> 1.1 Video-to-SOP
>
> Support and operations teams often rely on screen recordings, training sessions, and live demonstrations to transfer knowledge. These artifacts capture valuable institutional expertise, but traditionally they had to be manually reviewed and translated into written procedures. This process was slow, inconsistent, and highly dependent on subject-matter experts, often resulting in outdated or incomplete documentation.
>
> The video-to-SOP tool replaces this manual workflow with a fully automated, multimodal documentation system built on Amazon Bedrock and advanced video understanding models. By combining large-scale video embedding, semantic retrieval, and generative modeling, the tool converts unstructured recordings into production-ready SOPs in only a few minutes. The following figure shows the SOP Generator user interface used to upload recordings and generate SOPs end to end.
>
> Figure 2: The SOP Generator interface for uploading recordings
>
> Multimodal video understanding
>
> When a video is ingested, it is first processed using the Marengo Embed 2.7 model through Amazon Bedrock. The model chunks the video into small, configurable segments and processes them asynchronously making it suitable for long format videos. This model generates dense multimodal vector embeddings that jointly represent visual content, spoken language, and interface context. Beyond text-only embeddings, these representations capture how on-screen actions, user intent, and system responses relate to operational workflows.
>
> The system indexes the generated embeddings in Amazon OpenSearch Serverless, which functions as the system’s scalable vector store. This supports low-latency similarity search across large video libraries and historical recordings. As a result, teams can retrieve relevant workflow segments for documentation updates, identify procedural gaps, and reuse existing knowledge assets. Over time, this retrieval layer transforms isolated training videos into a persistent, searchable knowledge base.
>
> In parallel, the same video content is analyzed using the Pegasus 1.2 model for generative video understanding. The two models serve distinct roles: Marengo handles retrieval, encoding videos into searchable vectors so relevant content can be found across a growing library, while Pegasus handles understanding, reading the video and producing the structured text that drives SOP generation. Pegasus performs fine-grained video-to-text transformation, producing step-level summaries, chapter segmentation, and structured descriptions of actions and UI states. It extracts operational metadata such as required inputs, system outputs, conditional logic, and approval checkpoints, creating a machine-readable representation of each process.
>
> Structured SOP generation
>
> These outputs are combined into a unified semantic model that aligns temporal video segments with extracted actions and decision points. Frame sampling and visual filtering techniques are applied to select representative screenshots that correspond to meaningful workflow transitions, such as configuration changes, form submissions, or system confirmations. These images are automatically linked to the relevant procedural steps.
>
> Then, it passes the structured video understanding to the Claude Sonnet 4.6 model available on Amazon Bedrock, which generates formal documentation. This generation layer transforms the intermediate representation into a complete SOP that includes structured step sequences, embedded screenshots, validation checks, and expected outcomes.
>
> Interactive verification with timestamp-linked playback
>
> A key differentiator of the system is its interactive SOP preview editor. Every procedural step in the generated SOP is annotated with interactive timestamps that correspond to the exact moment in the source video where that action occurs. When a reviewer chooses a timestamp, the original video opens at that precise point, so they can verify the documented step against the source material in real time. This creates a direct traceability link between the written procedure and its video evidence, which serves as the source of truth. Reviewers can validate each step with a human in the loop, without scrubbing through entire recordings.
>
> Figure 3: Interactive SOP preview editor with timestamp-linked playback
>
> The editor also supports live editing: reviewers can refine wording, reorder steps, or add clarifications directly in the browser, then export the finalized SOP as a formatted Word document with embedded screenshots.
>
> Flexible templates and organizational standards
>
> To support diverse governance and compliance requirements, the tool offers multiple built-in SOP templates, including Comprehensive, Quick Reference, Training-Focused, and a ProServe SOP with Controls format that includes control point matrices, roles and responsibilities tables, and business outcome mappings. Teams can also upload their own template files or define a fully custom section structure, and the generation pipeline dynamically adapts its output to match.
>
> A configurable terminology dictionary recognizes team-specific acronyms, internal tools, and domain vocabulary, improving consistency and reducing ambiguity across documents.
>
> Continuous knowledge capture
>
> When workflows change or new videos are added, revised SOPs can be generated without requiring manual re-authoring. This scales knowledge capture in parallel with operational growth.
>
> In production environments, this architecture has reduced SOP creation time by 80 percent while maintaining quality through human-in-the-loop validation and review. Beyond efficiency gains, it supports faster onboarding, improves audit readiness, and helps critical institutional knowledge remain accessible regardless of personnel changes.
>
> 1.2 Ticket analyzer
>
> After SOPs are captured, the next challenge is applying them consistently in real-world operations. Support tickets often arrive with incomplete context, ambiguous language, and attachments that require manual interpretation. Analysts typically spend significant time searching for relevant documentation and validating each step.
>
> The ticket analyzer component addresses these challenges by combining Natural Language Processing (NLP), semantic retrieval, and RAG to deliver contextual guidance directly within the ticketing workflow. As shown in the following figure, the interface brings together prioritized issues, recent ticket history, and in-context guidance within a single analyst view.
>
> Figure 4: The ticket analyzer view within the analyst workspace
>
> When a new ticket enters the system, its content is normalized and enriched using Large Language Models (LLMs). Key entities, intent signals, and dependencies are extracted from free-text fields and attachments, while operational metadata is incorporated to provide additional context.
>
> The enriched representation is converted into vector embeddings and stored in Amazon OpenSearch Serverless.
>
> To generate resolution guidance, the system applies RAG. It first retrieves the most relevant SOPs, policies, and historical resolutions, and then provides this material as context to a foundation model on Amazon Bedrock. The model generates step-by-step guidance grounded in verified organizational knowledge, reducing hallucinations and supporting policy alignment. The deployment uses Amazon Bedrock Guardrails for content filtering and grounding validation to verify that generated guidance aligns with organizational policies.
>
> Beyond guidance, the system incorporates agentic workflows built with the AWS Strands Agents SDK, where multiple autonomous agents collaborate to execute operational tasks such as ticket tagging, commenting, and status updates. These actions are performed within a human-in-the-loop framework, so analysts can review and approve recommendations before execution to verify accuracy, control, and compliance.
>
> Recommendations are dynamically updated as new information becomes available. Confidence scores highlight cases that require additional review, while built-in feedback mechanisms allow analysts to flag documentation gaps and trigger updates to the knowledge base.
>
> The following figure shows an overview of the AWS Lambda architecture.
>
> Figure 5: Architecture of the ticket analyzer
>
> 1.3 Value stream intelligence
>
> The component presents resolution workflows as interactive swim lane maps that show how work moves across teams and systems, highlighting bottlenecks, inefficiencies, and non-value-added activities. By connecting datasets across upstream and downstream processes, the system empowers stakeholders to assess whether workflows are ready for automation, identifying what should be eliminated, optimized, or retained as manual before scaling. This provides a structured foundation for continuous improvement, helping teams quickly identify delays, approval friction, and coordination gaps.
>
> The following illustration provides a simplified representation of the value stream intelligence visualization to highlight key concepts.
>
> Figure 6: Simplified value stream intelligence visualization
>
> By connecting execution data with process maps, the visualizer supports root-cause analysis and continuous improvement initiatives. Teams can use these insights to streamline approval paths, reduce coordination overhead, and prioritize automation opportunities.
>
> 2. Analytics and decision intelligence layer (Amazon Quick)
>
> While automated documentation and guided resolution improve individual ticket handling, support leaders also need clear visibility into workload distribution, ticket volumes, and SLA risk. The ML-powered operational analytics component provides this visibility through a centralized dashboard built on Amazon Quick Sight.
>
> The dashboard combines two core capabilities: workload management and ML-based ticket analysis. Together, they empower teams to monitor operational health, identify risk early, and prioritize work more effectively.
>
> 2.1 Workload management and capacity visibility
>
> The workload management view shows how tickets are distributed across individual analysts in a team by complexity. The dashboard summarizes overall capacity using availability indicators, highlighting which analysts are operating at optimal levels and which are overloaded. Workload allocation by individual is displayed using stacked bar charts segmented by ticket complexity, making it clear how high, medium, and low-effort work is distributed.
>
> Figure 7: Workload management and capacity dashboard
>
> In addition to this view, the dashboard includes weekly workload trends that show how assignments evolve over time for each analyst. These trends help managers identify persistent overload, underutilization, or sudden workload spikes and rebalance assignments accordingly. By centralizing this information in a single view, the dashboard supports more consistent and data-driven workload planning.
>
> 2.2 ML-based ticket categorization and SLA risk prediction
>
> In parallel, the analytics system applies ML models to analyze ticket content and predict the risk of a ticket not meeting its SLA.
>
> The process begins with an Amazon Redshift query that extracts active tickets along with computed operational features. A data processing layer performs feature engineering, creates derived attributes, and validates data types before passing the dataset into the modeling stage. Engineered variables include operational signals such as the number of days a ticket has been open, number of days remaining in the month, ticket complexity level, number of prior escalations, historical resolution patterns, and workload indicators.
>
> Tickets are first categorized using rule-based classification logic into seven business clusters (for example, General Support, Exception Management, Access &amp; Permissions, and Account Merges). The dashboard showcases these clusters to provide real-time visibility into ticket distribution and workload composition.
>
> For SLA risk prediction, the system uses an XGBoost model that outputs a probability score (0–1) representing the likelihood of an SLA miss. This score is scaled to a 0–100 SLA score and mapped to risk categories using predefined thresholds:
>
> High Risk: ≥ 0.7 probability of SLA miss.
>
> Medium Risk: ≥ 0.4 probability of SLA miss.
>
> Low Risk: &lt; 0.4 probability of SLA miss.
>
> Finally, it writes the results to Amazon Simple Storage Service (Amazon S3) as partitioned Parquet files with timestamps and surfaced in Amazon Quick dashboards. The following chart provides an illustrative example of how ticket distribution across business clusters is visualized on the dashboard.
>
> Figure 8: Ticket distribution across business clusters
>
> A

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。