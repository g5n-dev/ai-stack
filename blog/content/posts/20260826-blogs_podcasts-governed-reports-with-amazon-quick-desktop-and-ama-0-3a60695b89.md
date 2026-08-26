---
title: "Governed reports with Amazon Quick Desktop and Amazon FSx for NetApp ONTAP"
date: 2026-08-26T00:57:29+08:00
draft: false
entry_kind: "auto"
tags: ["AI Agent", "生成式 AI", "Prompt 工程", "Advanced (300)", "Amazon FSx for NetApp ONTAP", "Amazon Quick Suite", "Technical How-to", "博客与播客"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:86e91fa7ec0882f3e39d8e7d3edf1a6c055f37a335f67b2ce760f34961311617"
source_payload_sha256: "sha256:0ea06b79f682e17cf18790b5aa9a9242d53bebf600997e4a4d2d35a288c2ab36"
observation_id: obs_3a60695b895f83bc5481f486225927f7423c8a21d27008af62a43cf86d22f686
event_id: evt_4dee3dab1f4581824900695e806c7832d0d50ad4bcd0ff44d5716ba6c5ae7914
revision_id: rev_60e15fcd63bd365c00c896fe3ec4fff0e677ce9c96da2a3ce92586b8378c2666
source_published_at: 2026-08-25T16:35:01Z
first_seen_at: 2026-08-26T14:06:24.174885Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 74
interpretation_sha256: "sha256:68d466752f1f3aa7e972a725ff4b11a1bf552e48b5ede116b6a0f506326db53b"
description: "该内容展示在 Amazon Quick Desktop 中如何通过 Quick 技能把存储在 FSx for NetApp ONTAP 的业务文件连接到一个受监管的报告流程，并自动生成可分享的周报、幻灯片和 Slack 摘要。"
external_url: https://aws.amazon.com/blogs/machine-learning/governed-reports-with-amazon-quick-desktop-and-amazon-fsx-for-netapp-ontap
parent_observation_id: null
last_seen_at: 2026-08-26T00:00:00Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/governed-reports-with-amazon-quick-desktop-and-amazon-fsx-for-netapp-ontap](https://aws.amazon.com/blogs/machine-learning/governed-reports-with-amazon-quick-desktop-and-amazon-fsx-for-netapp-ontap)
- **发布域名**: aws.amazon.com

## 要点解读

### 这是什么
该内容展示在 Amazon Quick Desktop 中如何通过 Quick 技能把存储在 FSx for NetApp ONTAP 的业务文件连接到一个受监管的报告流程，并自动生成可分享的周报、幻灯片和 Slack 摘要。

### 用在哪里
适用于需要定期准备运营报告、风险更新或执行简报的业务团队和领导者，尤其是已有 FSx for NetApp ONTAP 文件存储并希望在不改变现有访问治理的前提下引入 AI 辅助报告的组织。

### 可以推断的
推测：该方案能够显著降低手工整理和格式化报告的时间，因为工作流把文件收集、检索和输出集中在一个受控的助理中完成。  
推测：通过使用现有的文件访问控制和 S3 访问点的最小权限设置，报告生成过程可以在不泄露未经批准文档的前提下保持数据安全与合规。

## 来源摘要/节选

> Amazon Quick Desktop brings governed, AI-assisted reporting to the files your team already manages on Amazon FSx for NetApp ONTAP (FSx for ONTAP), cutting weekly report preparation from hours to minutes. Today, producing those reports takes hours of manual effort each week. Teams re-read the same documents, reformat metrics, and copy summaries into Slack. Leaders need those updates quickly, but they also need to trust the source behind each metric, risk, and recommendation.
>
> In this post, you build a governed weekly reporting workflow with Amazon Quick Desktop, Amazon Quick skills, Amazon FSx for NetApp ONTAP, Amazon Simple Storage Service (Amazon S3) access points, and Slack. Amazon Quick Desktop is a native desktop application that extends Amazon Quick from the browser to the user’s computer. It provides the AI-powered capabilities of the web experience together with desktop-specific capabilities such as
>
> Local file access.
>
> Background processing.
>
> A personal knowledge graph.
>
> In Amazon Quick Desktop, you create a skill called Weekly Business Reporting Assistant. A skill is a reusable workflow that gives Amazon Quick task-specific instructions, so users can start the same reporting process each week with a trigger phrase.
>
> The workflow connects a governed set of business files to a guided reporting experience. It keeps source documents under existing storage and access controls, gives Amazon Quick access only to the selected reporting content, and keeps human review in place before artifacts or Slack summaries are shared. The examples use fictitious business data, but the pattern applies to operating reviews, forecast updates, risk reporting, executive briefings, and weekly business reviews.
>
> Solution overview
>
> This solution makes Amazon Quick Desktop the main workspace for weekly reporting. Business users open Quick Desktop, activate the Weekly Business Reporting Assistant skill, and ask questions such as “What changed since last week’s operating review?” or “Create a one-page weekly report for leadership.”
>
> The skill makes the workflow repeatable. It gives Amazon Quick task-specific instructions that cover the source collection, output formatting, citation behavior, and when to ask for clarification. This lets users start from a guided reporting process instead of a blank conversation.
>
> The source files remain in FSx for ONTAP. In this walkthrough, FSx for ONTAP stores the documents that support weekly reporting, such as final weekly reviews, operating plans, forecast summaries, risk registers, and executive templates. Keeping the files in FSx for ONTAP lets storage and business teams continue using their existing file access and governance processes.
>
> You choose one reporting folder for the assistant to use. This folder contains the files business owners approve for the workflow. Drafts, outdated files, restricted documents, and unrelated content stay outside this folder.
>
> The S3 access point gives Amazon Quick controlled read access to that selected folder. AWS Identity and Access Management (IAM) permissions limit what Amazon Quick can list and read.
>
> Amazon Quick uses the selected files to create a searchable source collection called a knowledge base. In this walkthrough, the knowledge base is named Business Reporting Archive. The Weekly Business Reporting Assistant skill uses it to answer questions, cite source documents, create reports, generate decks and PDFs, build visuals, and draft Slack-ready summaries.
>
> After the report is ready to share, you use Slack integration in Amazon Quick to draft a channel summary. You review and approve the message before posting.
>
> Figure 1 shows the workflow. Business files stay in FSx for ONTAP. The S3 access point gives Amazon Quick controlled access to the selected reporting folder. Amazon Quick prepares that content as the Business Reporting Archive knowledge base. Users work in Quick Desktop with the Weekly Business Reporting Assistant skill to create cited reporting artifacts and Slack summaries for approval.
>
> Figure 1: Governed weekly reporting workflow with Amazon Quick Desktop, Amazon Quick skills, Amazon FSx for NetApp ONTAP, Amazon S3 access points, and Slack
>
> Amazon Quick Desktop also builds a personal knowledge graph in My context, connecting people, projects, events, actions, and documents. For example, while preparing a weekly report, a user can identify related people, action items, documents, and Slack channels from connected sources. The Business Reporting Archive remains the governed source for report facts and citations.
>
> Figure 2: Example personal knowledge graph in the My context view of Amazon Quick Desktop
>
> Prerequisites
>
> This walkthrough assumes your storage and identity foundation already exists. You configure the access path, Amazon Quick knowledge base, reporting assistant, Slack action connector, and validation workflow. You don’t create the FSx for ONTAP file system itself.
>
> AWS account and Amazon Quick requirements
>
> An AWS account with access to a Region where Amazon Quick, Amazon FSx for NetApp ONTAP, and Amazon S3 access points for FSx for ONTAP are supported.
>
> An Amazon Quick Enterprise subscription with permissions to create Amazon S3 integrations, knowledge bases, and spaces.
>
> The Amazon Quick desktop application installed for the users who run the reporting workflow. Review enterprise setup requirements before a production rollout.
>
> FSx for ONTAP requirements
>
> An FSx for ONTAP file system running NetApp ONTAP 9.17.1 or later.
>
> An FSx for ONTAP volume that is mounted and has a junction path, such as /business-reporting.
>
> An S3 access point attached to the FSx for ONTAP volume, or permissions to create one. The S3 access point and the FSx for ONTAP volume must be in the same AWS Region and owned by the same AWS account.
>
> AWS Identity and Access Management (IAM) permissions to grant Amazon Quick least-privilege read access to the S3 access point and approved object prefix.
>
> An Amazon S3 path in the same AWS Region as your Amazon Quick application.
>
> Slack and testing requirements
>
> A Slack workspace, an approved channel for reviewed summaries, and permissions to configure the Slack action connector.
>
> A focused set of fictitious or approved business files for testing, such as weekly reviews, operating plans, forecast summaries, risk registers, and executive templates.
>
> Implementation
>
> The implementation has seven steps. The following sections walk through each one: prepare the source folder, create the S3 access point, grant Amazon Quick read access, create the Amazon S3 integration and knowledge base, configure Slack, create the reporting assistant, and test the workflow.
>
> Step 1: Prepare source content
>
> Start with a narrow folder scope so business users can verify citations against a known set of source files. For this walkthrough, use a mounted FSx for ONTAP volume and create or choose an approved folder such as /business-reporting.
>
> Within that folder, organize files around the reporting process. Add the last 8–12 weekly business reviews, the current operating plan, the current forecast summary, and the current risk register. Also add the standard report template that guides the output style. Remove draft, obsolete, archived, and restricted files before indexing, and confirm that file owners agree with the source scope.
>
> /business-reporting/
>
> weekly-reviews/
>
> operating-plans/
>
> forecasts/
>
> risk-registers/
>
> executive-templates/
>
> Figure 3: Example approved reporting folder structure on a mounted FSx for ONTAP volume
>
> Step 2: Create an S3 access point
>
> Attach an S3 access point to the FSx for ONTAP volume. Amazon Quick can then read the approved content through an S3-compatible path. Work with your storage or cloud administrator if you don’t own the FSx for ONTAP configuration.
>
> Open the Amazon FSx console in the Region that contains the FSx for ONTAP volume.
>
> In the navigation pane, choose Volumes.
>
> Select the mounted FSx for ONTAP volume that contains the approved reporting folder.
>
> From Actions, choose Create S3 access point.
>
> Enter an access point name that follows your naming standard, such as business-reporting-ap.
>
> Configure the access point user and network settings according to your governance model. Select a virtual private cloud restriction if your workload requires private network access.
>
> Create the access point, and then record the access point alias and Amazon Resource Name (ARN). Use the alias in the S3 URI and the ARN in IAM policies.
>
> Figure 4: S3 access point overview for an FSx for ONTAP data source
>
> Step 3: Grant Amazon Quick read access
>
> Grant only the access Amazon Quick requires to list and read the approved prefix. The following policy is a starting point. Replace the placeholders with your Region, account ID, access point name, and prefix.
>
> {
>
> "Version": "2012-10-17",
>
> "Statement": [
>
> {
>
> "Sid": "ListApprovedReportingPrefix",
>
> "Effect": "Allow",
>
> "Action": ["s3:ListBucket", "s3:GetBucketLocation"],
>
> "Resource": "&lt;access-point-arn&gt;"
>
> },
>
> {
>
> "Sid": "ReadApprovedReportingObjects",
>
> "Effect": "Allow",
>
> "Action": "s3:GetObject",
>
> "Resource": "&lt;approved-prefix-object-arn&gt;"
>
> }
>
> ]
>
> }
>
> Set &lt;access-point-arn&gt; to arn:aws:s3:&lt;region&gt;:&lt;account-id&gt;:accesspoint/&lt;access-point-name&gt;. Set &lt;approved-prefix-object-arn&gt; to arn:aws:s3:&lt;region&gt;:&lt;account-id&gt;:accesspoint/&lt;access-point-name&gt;/object/business-reporting/*.
>
> Identify the IAM role or service role that Amazon Quick uses for the Amazon S3 integration in your account. Attach the policy to that role, and grant read access to document-level access control list (ACL) or metadata files that the Amazon S3 integration requires.
>
> Before you configure the Amazon S3 integration, validate the access point alias and prefix. Verify that the role cannot read folders outside the approved reporting prefix.
>
> Figure 5: Example IAM policy editor with S3 access point permissions
>
> Step 4: Create the Amazon S3 integration
>
> Create an Amazon S3 integration in Amazon Quick and use it to create a knowledge base from the approved prefix. The console might label the path as a bucket URL even when you use an S3 access point alias. Validate the alias path in your account before you publish the assistant.
>
> Open the Amazon Quick console.
>
> Choose Knowledge.
>
> Under Amazon S3, choose Add.
>
> Choose an existing Amazon S3 data source, or choose + Add account to connect a new source.
>
> For Name, enter FSx ONTAP Business Reports. For the S3 location, enter the access point alias path, such as s3:///amzn-s3-demo-business-reporting/.
>
> On the knowledge base page, enter FSx ONTAP Business Reports as the knowledge base name. Select only the approved prefix.
>
> After the knowledge base sync, open Spaces in the Amazon Quick console.
>
> Create a new space called Business Reporting Archive.
>
> Add the FSx ONTAP Business Reports knowledge base to this space.
>
> If your reporting files require per-user or per-group permissions, configure document-level ACL and metadata settings first. Amazon Quick requires you to make the ACL decision during knowledge base creation. After you choose Create, wait for the first sync to finish.
>
> Figure 6: Amazon Quick knowledge base created from the approved S3 access point path
>
> Step 5: Configure Slack
>
> Configure Slack so the assistant can stage business summaries for review and posting to the approved channel. Choose the authentication method that matches your organization’s security requirements.
>
> In the Amazon Quick console, choose Connectors.
>
> In the Amazon Quick desktop application, choose Settings, choose Capabilities, choose Connections, and then choose Browse Connections. This opens the Amazon Quick web console to complete the connection.
>
> On the Available tab, find Slack and choose Connect. For a team-managed app or token-based setup, use the Create for your team tab.
>
> Complete the Slack sign-in or token flow and grant only the required permissions. Use the minimum required Slack OAuth scopes (for example, chat:write scoped to the approved channel), and rotate credentials on a defined schedule.
>
> If your organization requires connector approval, work with your Amazon Quick administrator to publish the Slack connector to your user or group.
>
> Confirm the approved Slack channel, such as #finance-weekly, and document who can approve messages before posting.
>
> Return to the desktop application and test with a draft message in a non-production channel before using Slack for weekly reporting.
>
> Step 6: Create the reporting assistant
>
> Create a custom skill in the Amazon Quick desktop application that loads the Business Reporting Archive space and applies reporting guardrails. The skill provides a reusable assistant that users activate with a trigger phrase. For more on skill authoring, refer to Amazon Quick skill authoring documentation.
>
> In the Amazon Quick desktop application, open a conversation and enter a condensed skill specification like the following.
>
> Save this as a skill
>
> Skill: "Weekly Business Reporting Assistant"
>
> Trigger: weekly business reviews, operating plans, financial reports, WBR summaries, trend analysis, business reporting deliverables from the Business Reporting Archive
>
> Depends on: quick_suite__spaces
>
> Workflow:
>
> 1. [Deterministic] Load Space Context --- search_spaces("Business Reporting Archive") -&gt; list_space_documents(space_id) to get full document list. On failure: "I couldn't load the Business Reporting Archive. Please check that the space is connected and accessible."
>
> 2. [Agentic] Greet and Suggest --- Show greeting with 4 example questions:
>
> - Top 5 changes since last week's operating review
>
> - Risks repeating across last 4 WBRs
>
> - One-page weekly report (highlights, risks, action items, asks, key metrics, decisions needed)
>
> - Six-slide PowerPoint deck for leadership from latest review + operating plan
>
> 3. [Agentic] Answer Questions --- Use query_topic or search_relevant_content to find relevant content. Respond using structured format: Executive Summary -&gt; Key Highlights -&gt; Risks/Issues -&gt; Action Items/Asks -&gt; Sources (with doc names + dates cited).
>
> 4. [Agentic] Generate Deliverables (if requested) --- Reports structured as: business unit, period covered, key metrics/highlights, risks/blockers, mitigation plans, requests/escalations.
>
> Response tone: Professional business. Always cite specific document name, section, and date.
>
> Safety: Only reference content from the archive. Never fabricate metrics. State gaps clearly.
>
> Lessons Learned:
>
> - Always load space context before greeting
>
> - Always cite doc name + date
>
> - Don't extrapolate metrics not in source docs
>
> - Ask user when period is ambiguous, business unit unclear, or audience/format not specified
>
> - If a metric isn't tracked, name what IS available
>
> Name the skill Weekly Business Reporting Assistant and set a trigger phrase, such as weekly business report.
>
> Save the skill and confirm that it loads the Business Reporting Archive space.
>
> Figure 7: Entering the reporting assistant skill specification in Amazon Quick Desktop
>
> Figure 8: Amazon Quick suggests skill defaults before saving the assistant
>
> Step 7: Use Amazon Quick Desktop as the reporting workspace
>
> After you create the skill, activate it from a conversation in the Amazon Quick desktop application. The following example shows a business user moving from a question to a cited report and reviewed Slack summary.
>
> Start a new conversation and enter the trigger phrase, such as I need help with business reporting.
>
> The skill loads the Business Reporting Archive space and greets you with example questions.
>
> Figure 9: Reporting assistant activated in Amazon Quick Desktop
>
> Enter a reporting request, such as What changed since the prior operating review?
>
> Figure 10: Week-over-week change analysis generated from the Business Reporting Archive
>
> Review the cited findings before you use the response. Amazon Quick Desktop shows source details and response steps so you can check the documents and dates behind the response.
>
> Figure 11: Cited key developments and action items from the weekly reporting response
>
> Figure 12: Response steps and source details for review to review before using the response
>
> Ask Amazon Quick to create a weekly report, PowerPoint deck, PDF, or executive visual from the cited insights.
>
> Review the proposed plan, suggest changes if needed, and choose Approve &amp; Build when the plan is ready.
>
> Figure 13: Report creation plan staged for review before Amazon Quick builds the artifact
>
> After you approve the plan, Amazon Quick creates the asset in the requested format.
>
> Figure 14: Generated weekly report artifact in Amazon Quick Desktop
>
> Ask Amazon Quick Desktop to draft a Slack summary for the approved channel.
>
> Review the draft in the conversation and confirm only when it is ready to post.
>
> Figure 15: Slack-ready reporting summary staged for approval in Amazon Quick Desktop
>
> Figure 16: Approved weekly reporting summary posted to the Slack test channel
>
> Test the workflow with business prompts
>
> After you save the skill, validate the end-to-end workflow with prompts that match real weekly reporting work. Each response must cite specific source documents, include a source list in generated artifacts, and ask for your confirmation before posting to Slack. The following table shows representative prompts and what to look for in the response.
>
> Test area
>
> Prompt
>
> Expected result
>
> Research
>
> What are the top five changes since the prior operating review?
>
> A cited summary with source documents and dates.
>
> Risk analysis
>
> What risks repeat across the last four weekly business reviews?
>
> Grouped risks with citations and suggested owners when the source documents include them.
>
> Report creation
>
> Create a one-page weekly report with highlights, risks, action items, asks, key metrics, and decisions needed.
>
> A structured report with cited claims and a source list.
>
> Deck creation
>
> Create a six-slide PowerPoint deck for leadership from the latest review and operating plan.
>
> A deck or deck outline with title, summary, highlights, risks, decisions, and sources.
>
> Slack distribution
>
> Create a six-bullet Slack summary and ask me before posting.
>
> A Slack-ready message staged for approval before posting.
>
> Security and governance best practices
>
> Move from the sample workflow to a shared reporting workflow in stages. Start with one approved folder path and expand after business users validate citation quality. Keep source file permissions aligned with your existing FSx for ONTAP governance model, and use least-privilege IAM permissions for the role that Amazon Quick uses to read the S3 access point.
>
> Use document-level ACLs in the Amazon S3 integration when the knowledge base requires per-user or per-group access controls. Use a dedicated Slack channel for reporting summaries, define who can approve posts, and require human review for board materials, regulatory content, investor communications, or sensitive financial reporting. Review indexed source files on a schedule and remove obsolete content from the approved folder path.
>
> Troubleshooting
>
> Refer to the following table to diagnose common setup and runtime issues.
>
> Issue
>
> What to check
>
> Amazon Quick cannot read the source path
>
> Confirm the S3 access point alias, same-Region requirement, IAM policy resource scope, and Amazon Quick service role permissions.
>
> Knowledge base sync fails
>
> Confirm that the approved prefix exists, the access point is attached to a mounted FSx for ONTAP volume, and the file system is running NetApp ONTAP 9.17.1 or later.
>
> Responses do not include citations
>
> Confirm that the Business Reporting Archive space is connected in Amazon Quick Desktop and that the knowledge base files synced successfully.
>
> Responses refer to old files
>
> Confirm the knowledge base sync status and remove obsolete files from the approved folder path.
>
> Slack posting fails
>
> Confirm the Slack connector authorization, channel access, required scopes, and whether the connector was published to the user or group.
>
> Clean up resources
>
> To avoid future charges or unused access paths, remove only the resources that you created or changed for this walkthrough. These steps reverse the Amazon Quick knowledge base, Slack action connector, S3 access point, and IAM policy changes from the preceding sections.
>
> Delete the Weekly Business Reporting Assistant skill from the Amazon Quick desktop application if you no longer need it.
>
> Delete the Business Reporting Archive knowledge base if it was created only for this post.
>
> Remove the Amazon S3 integration from Amazon Quick if no other knowledge bases use it.
>
> Delete the S3 access point if it was created only for this workflow and no other workload uses it.
>
> Remove IAM policy statements and access point policies that were added only for this walkthrough.
>
> Remove sample files from the approved folder path if they were used only for testing.
>
> Conclusion
>
> You now have a governed weekly reporting workflow that creates cited business artifacts from file content stored on Amazon FSx for NetApp ONTAP. The S3 access point exposes only the approved folder path, and Amazon Quick indexes that content through the Amazon S3 integration. Business users can research reporting questions, generate reports and visuals, and prepare Slack summaries from one workspace without moving the source files out of the managed storage workflow.
>
> For executives and business stakeholders, this pattern improves trust in recurring updates. Users review citations before they use the output and approve Slack posts before distribution. For builders, it keeps the first implementation narrow enough to validate governance, access, and reporting quality.
>
> Start with one approved folder, one reporting use case, and one reviewed distribution channel. After users trust the citations and output quality, expand the knowledge base to more business units, add document-level ACLs if required, and refine the skill instructions for your internal reporting standards.
>
> For more information
>
> To get started, identify one approved reporting folder on your FSx for ONTAP volume and work with your storage team to create an S3 access point for that path. Then create the Amazon Quick knowledge base and reporting assistant skill, and validate the workflow with your first weekly update.
>
> For more information, refer to the following resources:
>
> Amazon Quick User Guide
>
> Amazon Quick on desktop
>
> Amazon Quick skill authoring documentation
>
> Amazon S3 integration in Amazon Quick
>
> Document and visual creation with Amazon Quick
>
> Slack integration in Amazon Quick
>
> Amazon FSx for NetApp ONTAP User Guide
>
> Accessing FSx for ONTAP data with S3 access points
>
> Access point restrictions and limitations for FSx for ONTAP
>
> About the authors
>
> Ebbey Thomas
>
> Ebbey is a Senior Generative AI Specialist Solutions Architect at AWS. He designs and implements generative AI solutions that address specific customer business problems. He is recognized for simplifying complexity and delivering measurable business outcomes for clients. Ebbey holds a BS in Computer Engineering and an MS in Information Systems from Syracuse University.
>
> Eugene Thomas
>
> Eugene is a Technical Account Manager at AWS focused on agentic AI, no-code automation, resilience, security, and cost optimization. With more than 10 years in customer-facing roles, he helps builders and business stakeholders turn complex cloud topics into practical solutions. He is also an active member of the Amazon Quick community, exploring how chat agents can simplify collaboration.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。