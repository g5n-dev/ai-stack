---
title: "Build an end-to-end RFI questionnaire workflow using Amazon Quick Automate"
date: 2026-09-11T17:44:34+08:00
draft: false
entry_kind: "auto"
tags: ["AI Agent", "生成式 AI", "Prompt 工程", "Advanced (300)", "Amazon Quick Suite", "Amazon Simple Storage Service (S3)", "Technical How-to", "博客与播客"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:ccc573de6bfadbe42d39e356863dceda5114e3bdc2aaf65af165396ff12369d4"
source_payload_sha256: "sha256:51a776fe8e48f064372d0eef355a3d31cca5f2b8ffaebaff633be107c7338141"
observation_id: obs_842b571c183eead66594afac781aec1946d670d73e7ca2d1b4861c5249c9e1f4
event_id: evt_e89927c1c02e3dc58d71031949479d850a2c259d423401e7c539cf8938e3ee05
revision_id: rev_bd727a0759c32af33fe661ae7cc37ab359b2ee4f2ca59d24f1d4a71a3f356d04
source_published_at: 2026-09-10T16:08:57Z
first_seen_at: 2026-09-11T09:55:13Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 74
interpretation_sha256: "sha256:7d13d42662ca94ec06cecd49287829fe9a3e13e550d7cfc26aedbbbedf2d23dc"
description: "这段内容展示了如何使用 Amazon Quick Automate 构建一套从 Amazon S3 读取多标签 RFI 工作簿、提取结构化问题与分类信息、并将结果输出为 CSV 的完整自动化流程。它通过自然语言描述处理逻辑，由生成式 AI 逐步生成、迭代并验证工作流，最后可导出至其他账户或区域。"
external_url: https://aws.amazon.com/blogs/machine-learning/build-an-end-to-end-rfi-questionnaire-workflow-using-amazon-quick-automate
parent_observation_id: null
last_seen_at: 2026-09-12T00:00:00Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/build-an-end-to-end-rfi-questionnaire-workflow-using-amazon-quick-automate](https://aws.amazon.com/blogs/machine-learning/build-an-end-to-end-rfi-questionnaire-workflow-using-amazon-quick-automate)
- **发布域名**: aws.amazon.com

## 要点解读

### 这是什么
这段内容展示了如何使用 Amazon Quick Automate 构建一套从 Amazon S3 读取多标签 RFI 工作簿、提取结构化问题与分类信息、并将结果输出为 CSV 的完整自动化流程。它通过自然语言描述处理逻辑，由生成式 AI 逐步生成、迭代并验证工作流，最后可导出至其他账户或区域。

### 用在哪里
适用于企业采购或合规团队——他们每年需要处理大量的 RFI 文档，常因文档结构不统一、手工提取信息而导致响应延迟和错误。业务人员只需在 Quick Automate 中用自然语言描述需求，即可快速搭建并部署适配新问卷格式的自动化。

### 可以推断的
推测：因流程以自然语言生成和调整，企业内部的非技术用户也能参与自动化创建，降低了对开发资源的依赖。  
推测：自动化通过读取和写入同一 S3 桶，实现数据的闭环存储，便于后续系统直接消费处理后的结构化数据。

## 来源摘要/节选

> Build an end-to-end Request for Information (RFI) questionnaire workflow using Amazon Quick Automate to solve a challenge organizations face at every scale. A typical enterprise might handle hundreds of RFI questionnaires each year, and each arrives as a complex, multi-tab workbook packed with hierarchical question sets, category metadata, and varied response types. The volume, variety, and complexity of these documents create a significant operational challenge. Manually extracting, structuring, and resolving RFI questions requires repeated coordination, delays responses, and can introduce errors each time the questionnaire format changes.
>
> Amazon Quick Automate handles multi-agent automation for supported enterprise processes that can span across departments, systems, UI and API interactions, and third-party systems. It uses a team of agents to simplify business process management and cut down on maintenance overhead. You describe your processing goals in plain language, and Quick Automate can produce an executable workflow covering ingestion, transformation, validation, and output. You can refine the workflow through conversation, run it against your data, and promote validated versions across AWS Regions. This approach can help you respond to RFIs faster and reduce formatting inconsistencies and errors. The automation is designed to scale with your workload, and you can adapt it to new questionnaire formats by updating the natural-language instructions.
>
> In this post, we show you how to build an end-to-end automation that reads a multi-tab RFI workbook from Amazon Simple Storage Service (Amazon S3), extracts and structures the questionnaire data, and writes clean output back to Amazon S3. This tutorial uses Amazon Quick Automate and Amazon S3. Review Amazon Quick pricing and Amazon S3 pricing for cost details.
>
> Solution overview
>
> This walkthrough automates the processing of an RFI workbook stored in Amazon S3. When procurement teams receive an RFI questionnaire, they need to extract each question and preserve its category and response type. The goal is to produce a structured dataset that downstream teams can consume, interpret, and act on. In this example we present a solution that automates the process using Amazon Quick Automate. You start by connecting Amazon Quick Automate to the Amazon S3 bucket where your RFI workbooks are stored. Then you create an automation project, which is where you select your data connectors and organize your workflows. With the project in place, you can describe your processing logic in plain language: what to read, how to structure it, and where to write the output. The result is a working automation that reads a multi-tab RFI workbook, extracts and structures the questionnaire data, and outputs a clean comma-separated values (CSV) file. It does this without requiring custom code for common scenarios. The following diagram shows the high-level sequence of steps.
>
> Figure 1: High-level sequence of steps for the RFI workbook automation
>
> The diagram takes you from connecting your data source through deploying the finished automation in a production environment. Check the AWS Regions page for the latest availability.
>
> The solution follows these steps:
>
> Set up an Amazon S3 action connector – Connect Amazon Quick Automate to your S3 bucket.
>
> Add the S3 integration to an automation group – Share the S3 action with the automation group that will use it.
>
> Create an automation project – Create the project where you describe your processing logic.
>
> Describe the processing logic – Enter a natural-language prompt and let the generative AI assistant build the workflow.
>
> Refine through conversation – Iterate on the generated workflow by requesting targeted changes.
>
> Validate results – Run the workflow and verify output in your pre-production (development) AWS account.
>
> Promote with Import/Export – Export the validated version and import it into your production account or target AWS Region.
>
> Now that we have reviewed the high-level steps for the solution, we will go over the environment requirements.
>
> Prerequisites
>
> Before you begin, confirm that your environment meets the following requirements.
>
> An Amazon Quick Enterprise subscription with Amazon Quick Automate access.
>
> An Amazon S3 bucket in the same AWS Region as the Amazon Quick application.
>
> Familiarity with AWS Identity and Access Management (IAM) roles and policies.
>
> Basic understanding of Amazon S3 buckets, prefixes, and objects.
>
> IAM baseline for this walkthrough
>
> You need an IAM role that grants Amazon Quick Automate permission to access your S3 bucket. If you don’t already have one, follow these instructions to create it now:
>
> Open the IAM console.
>
> In the navigation pane, choose Roles, then Create role.
>
> For Trusted entity type, choose Custom trust policy and paste the following trust policy:
>
> {
>
> "Version": "2012-10-17",
>
> "Statement": [
>
> {
>
> "Effect": "Allow",
>
> "Principal": {
>
> "Service": "quicksight.amazonaws.com"
>
> },
>
> "Action": "sts:AssumeRole"
>
> }
>
> ]
>
> }
>
> Choose Next and attach a permissions policy that grants s3:GetObject, s3:PutObject, and s3:ListBucket on your target bucket.
>
> Name the role (for example, QuickAutomate-S3-Role) and choose Create role.
>
> Copy the role Amazon Resource Name (ARN). You will need it when configuring the S3 connector.
>
> With the IAM role created and the role ARN copied, you’re ready to configure the connection between Amazon Quick Automate and your S3 bucket.
>
> Set up the S3 connector
>
> After prerequisites are confirmed, configure the S3 connector in the Amazon Quick console.
>
> In the Amazon Quick console, choose the user icon in the upper-right corner.
>
> Open Manage Account, then go to Permissions &gt; AWS Actions.
>
> Figure 2: AWS Actions page in the Amazon Quick console
>
> Choose New action, then select Amazon S3.
>
> Configure the connector:
>
> Enter a connector name (for example, ExampleBucket-S3-Connection) and a description.
>
> Paste the ARN of the IAM role you created in the prerequisites step.
>
> Figure 3: Amazon S3 action connector configuration
>
> The console validates the role trust policy automatically. Confirm that the status shows a successful connection.
>
> Share the connector with users and groups who build and run workflows.
>
> Create an automation group
>
> In the Amazon Quick console, go to Automations &gt; Create Group.
>
> Figure 4: Create Group option on the Automations page
>
> Name the group (for example, RFI-Processing-Group).
>
> On the Add actions page, select the Amazon S3 connection you created earlier, then choose Next.
>
> Figure 5: Selecting Amazon S3 for the automation group
>
> With the connector and the automation group configured, create the automation project that will hold your workflow.
>
> Create an automation project
>
> The automation project is where you describe your processing logic and where the generated workflow lives.
>
> On the Automations page, choose the Projects tab, then choose Create Project.
>
> In Provide project details, enter a name for the project, select the automation group you created, and optionally add a description and upload existing documentation.
>
> Choose Next: Business case.
>
> The business case section is optional and is used for tracking return on investment. To complete it, enter hours saved per case, cases per year, project priority, and a target launch date.
>
> Choose Create.
>
> Your project opens on a summary page with Summary, Versions, and Deployments tabs, and a status panel showing the current state of the project.
>
> With the connector, the automation group, and the project in place, you are ready to describe your workflow logic.
>
> Describe the processing logic in natural language
>
> In Amazon Quick Automate, you describe what the automation should do using natural language. You can type directly into the prompt area or upload a file with your requirements. The AI assistant interprets your instructions and generates executable workflow steps.
>
> Step 1: Connect to S3 and read a sheet
>
> In the automation project, you see a text area where you describe your processing requirements. Enter a prompt that covers the data source, transformation logic, and the output you want. For example:
>
> “Connect to my S3 bucket using the ExampleBucket-S3-Connection connector. Read the file SampleDepartment_Version2.xlsx from the sample-folder prefix. Open the Strategy sheet and extract all survey questions. Identify main questions and subquestions based on numbering and indentation. Structure the data with columns for Serial Number, Category, Question, and Response Type. Write the output as a CSV file to the output-folder prefix in the same bucket.”
>
> Figure 6: Entering the processing prompt in the automation project
>
> Step 2: Review the generated workflow
>
> After you submit the prompt, the AI assistant generates a multi-step workflow. Each step maps to a part of your instructions:
>
> Read data – Connects to S3, downloads the workbook, and reads the target sheet with headers.
>
> Extract and transform – Identifies main questions and subquestions by numbering and indentation, and pulls category metadata from column headers.
>
> Structure output – Converts subquestions into standalone records by merging parent context. Defines the output schema.
>
> Write results – Saves structured output as a CSV file to the specified S3 location.
>
> Figure 7: Generated multi-step workflow
>
> Because the AI assistant relies on generative AI, the exact steps and wording it produces might vary between runs. The workflow you see might differ slightly from this example, but it covers the same logical operations based on your instructions.
>
> Step 3: Run and validate
>
> Choose Run to execute the workflow against your workbook. Review the output to confirm:
>
> All questions are extracted (main and subquestions).
>
> Category text matches the source column headers exactly.
>
> Subquestions include parent context.
>
> Response types are preserved as-is from the source.
>
> Figure 8: Workflow run output
>
> Refine the workflow through conversation
>
> When the output needs improvement, use the conversation interface to request targeted changes. Reference the specific step and describe the expected behavior.
>
> Example refinement prompts:
>
> “The step that reads the Strategy sheet should also capture column headers as metadata.”.
>
> “The category field does not match source headers. Update extraction to use exact header text.”.
>
> “In the subquestion transformation step, merge parent context into the question text.”.
>
> Follow this iterative cycle:
>
> Identify the issue – Compare output against your expected results.
>
> Request a targeted update – Describe the change in natural language, referencing the specific step.
>
> Review the updated workflow – The AI assistant modifies the relevant step and shows you the change.
>
> Re-run and validate – Execute again and confirm the fix.
>
> Best practices
>
> Before promoting your automation to production, follow these best practices:
>
> Validate incrementally – Run and check output after each refinement, rather than batching multiple changes.
>
> Handle edge cases explicitly – Describe how the workflow should behave when data is missing, duplicated, or formatted inconsistently.
>
> Promote automations with Import/Export
>
> Amazon Quick Automate Import/Export supports controlled promotion from pre-production to production and consistent reuse across AWS Regions.
>
> Export a version
>
> Open the source automation.
>
> Go to Versions.
>
> Choose Export version for the validated release.
>
> Figure 9: Exporting a validated automation version
>
> Copy the generated version link.
>
> Note: The export link expires after a set period. Copy and use it promptly, or generate a new link if it has expired.
>
> Figure 10: Generated export version link
>
> Import a version
>
> Open or create an Amazon Quick Automate project in the destination account or AWS Region.
>
> Choose Import version.
>
> Paste the version link and choose Start.
>
> Review version details and complete the import.
>
> Figure 11: Importing an automation version
>
> Configure required connectors, credentials, and deployment settings in the target environment.
>
> Figure 12: Configuring the target environment after import
>
> Clean up
>
> Delete the automation project and the automation group.
>
> Remove the S3 connector if no other workflows use it.
>
> Delete test IAM roles and test S3 objects when no longer required.
>
> For detailed cleanup guidance, see Using Amazon Quick Automate.
>
> Conclusion
>
> In this post, you built an end-to-end automation for processing RFI questionnaires stored as multi-tab Excel workbooks using Amazon Quick Automate. You connected your data through an Amazon S3 action connector, described your processing logic in natural language, refined the automation through conversation, and promoted it across AWS accounts and Regions using Import/Export.
>
> You can extend this approach to other business workflows, such as:
>
> Intelligent document processing (IDP) – Extract structured data from invoices, contracts, or forms.
>
> Report consolidation – Merge multi-sheet financial reports into a unified dataset.
>
> UI automation – Automate repetitive browser-based tasks that feed into downstream analytics.
>
> Survey data aggregation – Consolidate survey responses from multiple sources into a single output.
>
> For more on automation capabilities, action connectors, and natural-language workflows, see the Amazon Quick documentation. Visit Getting started with Amazon Quick to start using Amazon Quick Automate today.
>
> About the authors
>
> Chaytanya Kumar
>
> Chaytanya is an AI Builder at AWS Professional Services, helping enterprise and public sector customers accelerate their generative AI and cloud journeys. With deep expertise in AI enablement, agentic AI, and digital transformation, he builds intelligent solutions that drive measurable business outcomes. Outside work, he recharges by exploring oceans and mountain trails.
>
> Anneline Sibanda
>
> Anneline is an AI Builder at AWS, specializing in the architecture and delivery of agentic and generative AI solutions. With 10+ years of experience delivering solutions for Healthcare, Higher Education and FSI customers, she is a key technical partner for enterprises bridging the gap between innovative concepts and production-ready applications.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。