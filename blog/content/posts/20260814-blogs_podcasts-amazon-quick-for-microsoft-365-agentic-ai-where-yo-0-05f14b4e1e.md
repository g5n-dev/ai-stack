---
title: "Amazon Quick for Microsoft 365: Agentic AI where you work"
date: 2026-08-14T06:06:12+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "生成式 AI", "Prompt 工程", "Advanced (300)", "Amazon Quick Suite", "Announcements", "博客与播客"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:1acedd7be7542452ce26697ddc3e13df55e130a465345f07fec5c437f283879e"
source_payload_sha256: "sha256:c906efb09597d1b8238278250113496d0f6da9238af46b0175335a9e09603f0a"
observation_id: obs_05f14b4e1e89cd91f110a5189c0427a8a5a082c150bca048d34aaf051ae98e82
event_id: evt_5406f1f19e0b617d0426c8225851fa0d1ec1e8c59ebb7a4142f3f2f110671abf
revision_id: rev_abb6b03a2402541f92e098cac1b3e126a31363c55fface3c940861531cb6fbf3
source_published_at: 2026-08-13T15:48:15Z
first_seen_at: 2026-08-17T17:44:54.988239Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 57
interpretation_sha256: "sha256:6ebdc99da62cebb0514a4b691962e0843204934f8ff534f0bdccc2fd05e5d98b"
description: "Amazon Quick 在微软 Office 套件中推出 AI 助手，能够直接在 Word、Excel、PowerPoint、Outlook 中执行文档编辑、数据检索等操作，基于已有数据源和第三方集成完成任务。"
external_url: https://aws.amazon.com/blogs/machine-learning/amazon-quick-for-microsoft-365-agentic-ai-where-you-work
parent_observation_id: null
last_seen_at: 2026-08-17T00:00:00Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/amazon-quick-for-microsoft-365-agentic-ai-where-you-work](https://aws.amazon.com/blogs/machine-learning/amazon-quick-for-microsoft-365-agentic-ai-where-you-work)
- **发布域名**: aws.amazon.com

## 要点解读

### 这是什么
Amazon Quick 在微软 Office 套件中推出 AI 助手，能够直接在 Word、Excel、PowerPoint、Outlook 中执行文档编辑、数据检索等操作，基于已有数据源和第三方集成完成任务。  

### 用在哪里
适用于已在微软 365 环境下工作、同时拥有 Quick 环境的企业团队，尤其是需要跨系统整合信息、快速生成提案、报告或演示文稿的知识工作者。  

### 可以推断的
- 推测：在日常工作中将 AI 能力嵌入到常用的办公软件，可显著减少切换应用的频率，从而提升效率。  
- 推测：因 Outlook 对 Graph API 的权限限制，企业可能需要管理员提前授权才能实现完整功能。

## 来源摘要/节选

> Your enterprise data lives in dozens of systems, but often the work happens in Microsoft 365. Amazon Quick bridges that gap as an AI assistant grounded in your data, now available directly inside Microsoft Word, Excel, PowerPoint, and Outlook.
>
> These extensions don’t require you to adopt a new application or change how you work. Instead, they bring Amazon Quick connected data access and agentic document editing directly into the Microsoft 365 apps your teams open every morning. Your Amazon Quick Sight dashboards, Spaces, AWS data sources, and third-party integrations are now accessible without leaving Word, Excel, PowerPoint, or Outlook.
>
> In this post, we cover how installation and setup works, and workflows that you can run across each app.
>
> General availability and access
>
> Amazon Quick customers can access the new Microsoft 365 extensions now. You can install the four extensions (Word, Excel, PowerPoint, and Outlook) across both desktop and web versions of Microsoft 365. No additional licensing is required for customers on Plus, Professional, or Enterprise plans.
>
> Why this matters: The intelligence layer
>
> What really matters is how you embed AI into the workflows where business decisions happen.
>
> Most organizations also use AWS infrastructure, Amazon Quick Sight dashboards, Salesforce pipelines, Jira projects, Slack conversations, and SharePoint repositories. Quick connects these to your daily productivity tools. The value isn’t in the underlying agentic model itself. It’s in the breadth of connected data that the agent brings to your interactions.
>
> An example from my own workflow: I now draft customer request for proposal responses in hours, pulling from internal knowledge bases, past proposals, and live customer data. This used to take a team weeks to compile from scattered sources. Customized customer presentations that weave together structured data sources and unstructured documents come together in an hour rather than a day or two. The time I save goes straight into refining positioning and focusing on what matters to each customer, rather than scrambling to gather information and meet a response deadline.
>
> Figure 1: The Amazon Quick console with Microsoft 365 extensions enabled, showing Word, Excel, PowerPoint, and Outlook extensions activated and ready for deployment
>
> How it works: Agentic, not only chat
>
> These extensions aren’t a chatbot bolted onto Office, and they aren’t a standalone application that asks you to work somewhere new. They are agentic: the AI assistant does more than answer questions. It takes action directly within your documents, spreadsheets, presentations, and email messages.
>
> Quick lives inside Microsoft Word as a persistent side panel. You open it from the ribbon, ask a question or give an instruction, and the agent works within the application context. There’s no tab-switching and no copy-pasting between apps. The agent sees your document and acts on it.
>
> In Word, the agent can find and replace text, insert sections, and reformat content. It then shows you a visual comparison of what changed.
>
> Every agent action in a document is tracked. In Word, changes appear as an audit trail link, or as a visual comparison directly in the chat. Each change in the audit trail includes a selectable reference back to the affected content.
>
> Conversations don’t vanish when you close the panel either. The extension preserves history across sessions. In Microsoft Outlook, each email thread gets its own persistent conversation. Switch between email threads, and the extension remembers what you discussed in each one.
>
> Figure 2: The Amazon Quick side panel in Word displaying a visual comparison of agent-suggested edits with before-and-after change tracking. In this example I’ve asked it to rewrite the opening to this post, showing changes in both Word and the audit trail that can be displayed in the agent side panel
>
> Installation and authentication: Fewer moving parts
>
> The extensions require no client-side installation. They run entirely in the cloud, so there’s nothing to deploy to user machines. An administrator can push them to targeted users and groups through the Microsoft 365 admin center using a standard manifest. This is the same mechanism used for any Microsoft 365 add-in.
>
> Alternatively, you can install it yourself through the Microsoft add-in store. Search for “Quick,” choose Add, and the extension appears on the Office ribbon. Either way, after it’s there, updates ship automatically. Your team deploys once, and every user gets the latest version without IT intervention.
>
> The one exception is Outlook. Because most organizations restrict Graph API permissions, the Outlook extension typically requires admin approval for full functionality. Plan on admin deployment for Outlook.
>
> The authentication model uses Quick native authentication and does not require an Entra app. The result is fewer moving parts, faster setup, and fewer dependencies for your IT team to manage, while maintaining the security framework that Quick provides. If you’re on the Free or Plus Quick plan, you can sign in with your enterprise credentials or through social login (Google, Apple), with no separate identity configuration to set up.
>
> You can configure agent settings and custom branding through the Office manifest or policy settings, with no additional infrastructure required.
>
> You can access the extensions across seven Quick AWS Regions: US East (N. Virginia), US West (Oregon), Europe (Ireland), Europe (London), Europe (Frankfurt), Asia Pacific (Sydney), and Asia Pacific (Tokyo). Data stays within your selected region, and the backend infrastructure runs fully isolated with no public egress.
>
> Getting started requires an active Quick application. The extensions connect to your configured Quick environment, inheriting your existing knowledge bases, data sources, and integrations. They’re an expansion of the Quick you already use, not a separate product to purchase or provision.
>
> After the extension is in place, you find the Quick icon on the Office ribbon. Select it to open, sign in, and start working. The interface is already familiar because you stay inside Microsoft 365 apps. Your existing Spaces, dashboards, and integrations (including Salesforce, Jira, Slack, SharePoint, and more) are available immediately without additional configuration. The extensions respect your existing permissions and security policies.
>
> Figure 3: Amazon Quick extensions are available across seven AWS Regions with full data residency controls
>
> Microsoft Excel: Where numbers become decisions
>
> The agent operates within the context of the data you’re already working with.
>
> The extension handles the data retrieval and formatting in a single step, so you go from question to answer without switching between systems.
>
> This helps you decode complex spreadsheets built by others or quickly trace the source of calculation discrepancies.
>
> When you need to bring in external data, the extension pulls from cloud storage, data warehouses, Quick Sight, Salesforce, or SharePoint. It then identifies inconsistencies, cleans formatting issues, and transforms everything into analysis-ready formats.
>
> You can then validate your analysis against actual business metrics stored in Quick Sight to verify your models align with reality. This closed-loop workflow keeps your spreadsheets connected to live data throughout the analysis process.
>
> Figure 4: Quick modifies cells and explains formulas directly in the side panel, with highlighted references across worksheets. In this example, a cell is selected and you can interact with the agent to understand how a formula is derived. This example is working against the web version of Excel
>
> Consider a typical Excel workflow. Ask the agent to analyze your current sheet and flag month-over-month anomalies greater than 10 percent. Then pull Q1 revenue by Region from your Quick Sight dashboard into a new tab. If you encounter a complex formula, ask Quick to explain it and trace its dependencies. When you’re ready to present, have the agent create a chart that compares actual and forecast values.
>
> Microsoft Word: Write with enterprise context
>
> The Word extension acts as a co-editor that understands both your document and your connected data sources. It respects your document’s existing structure, including fonts, heading styles, and organizational patterns. When it adds or modifies a section, the output matches what’s already there. The new extension works directly with the native formatting model in Word, maintaining consistent styling throughout.
>
> The extension captures every edit as a before-and-after snapshot and renders it as a visual comparison in the chat panel. Each change includes a selectable reference back to the affected section. You can review what was modified, where, and in what order. This gives you a complete record of the agent’s work. The audit trail is especially valuable in collaborative environments where multiple people contribute to the same document and need to understand what changed and why.
>
> Generate tables and visualizations that pull from Quick Sight dashboards. Build executive summaries that reference Salesforce pipeline metrics or include project status updates from Jira.
>
> Rather than copying numbers from one system and pasting them into a document, the extension weaves quantitative data from multiple sources into narrative documents. The result is reports, proposals, and briefs that cite real numbers rather than placeholder text.
>
> Figure 5: Agent-suggested edits can be displayed as before and after blocks within the chat pane
>
> In practice, you might start with a long report and ask Quick to summarize it into a one-page executive brief with key takeaways.
>
> Need to reach a non-technical audience? Ask Quick to rewrite a specific section while preserving the underlying data points. For strategic documents, prompt the extension to add a conclusion section that references your Salesforce pipeline metrics from last quarter. The agent queries the data and writes the narrative in one step.
>
> Microsoft Outlook: Email informed by your enterprise data
>
> The Outlook extension automatically understands the context of the email or meeting you’re reviewing. Subject, sender, recipients, thread history, and timestamps are included with every interaction, so the agent’s responses stay relevant to that context. There’s no need to explain what you’re looking at or paste in background.
>
> Composing messages becomes faster and more informed. The agent drafts replies, reply-all messages, and new email messages with full thread awareness. It understands conversation boundaries across email clients including Outlook, Gmail, and Apple Mail, and preserves the correct thread structure in its responses.
>
> Add recipients to To, CC, or BCC fields, include attachments, and schedule sends. The side panel handles these tasks without leaving your inbox.
>
> Beyond composition, the extension helps you stay on top of your inbox. Flag, categorize, and move messages. Summarize long threads and extract action items. The extension turns Outlook from a communication tool into an intelligent workflow surface connected to your Salesforce accounts, Quick Sight metrics, and Jira tickets. Reference any of these directly in your email responses, grounding every message in actual business context.
>
> Figure 6: Quick can draft contextual replies using customer data in Quick and thread history, without leaving your inbox
>
> When responding to a customer, prompt Quick to pull the latest account health metrics from Salesforce and weave them into your response. The result is a message grounded in real account data.
>
> For long threads that have gone cold, ask for a digest that summarizes the conversation with owners and deadlines called out explicitly. Or, for threads with many participants and open items, prompt Quick to create a 30-minute meeting with everyone on the thread to align on next steps. The agent generates the attendees, title, and agenda automatically.
>
> Microsoft PowerPoint: Presentations backed by real data
>
> The PowerPoint extension generates slides programmatically and supports multi-step creative workflows that go well beyond single-prompt generation. You build presentations iteratively, refining design and content across multiple interactions with the agent.
>
> Quick uses your slide masters, layouts, fonts, and color schemes, so generated slides match the design system your team already uses. You don’t need to choose between AI assistance and your company’s templates. The agent works within your brand guidelines from the start.
>
> Define a theme or color palette in one step and apply it across slides in the next, building a narrative arc over several conversations.
>
> The extension also connects your presentations to your data. Generate charts and executive summaries that reference Quick Sight dashboards or Salesforce metrics. When you’ve built an analysis in Excel, the PowerPoint extension can generate a board deck that understands what the analysis found and structures the narrative accordingly. Context flows from data to presentation because both extensions draw on the same connected data sources.
>
> Figure 7: The PowerPoint extension generates branded slides with Quick data across a multi-step workflow. In this example we show the Quick Action feature, where you can choose a suggested action
>
> To try this, create a five-slide executive summary using your company template, pulling Q1 metrics from your Quick Sight dashboard.
>
> What’s next
>
> This release brings Quick intelligence to Microsoft 365, including Excel and PowerPoint. Visit the Amazon Quick documentation for new capabilities and updates as they become available.
>
> Get started
>
> Amazon Quick extensions for Microsoft 365 are generally available. If you’re already a Quick user, you can install extensions from the Quick Download page. If you aren’t a Quick user, you can start a free trial, install the extensions, and start using Quick in Word, Excel, PowerPoint, and Outlook.
>
> To learn more, visit the Amazon Quick documentation or sign in to the Quick console and choose the Microsoft 365 extensions from the Extensions menu.
>
> About the authors
>
> Art Chan
>
> Art is a Senior Worldwide Specialist SA for Amazon Quick at AWS. He helps customers and field teams understand how AI-powered productivity tools can reshape the way organizations work. When he’s not on the clock, he’s either logging miles for his next marathon or getting his hands dirty on his farm.
>
> Abhinand Sukumar
>
> Abhinand is a Senior Product Manager at Amazon Web Services for Amazon Q Business, where he drives the product vision and roadmap for innovative generative AI solutions. Abhinand works closely with customers and engineering to deliver successful integrations, including the browser extension. His expertise spans generative AI experiences and AI/ML educational devices, with a deep passion for education, artificial intelligence, and design thinking. Prior to joining AWS, Abhinand worked as an embedded software engineer in the networking industry.
>
> Leo Mentis Raj Selvaraj
>
> Leo is a Sr. Specialist Solutions Architect – GenAI at AWS with 4.5 years of experience, currently guiding customers through their GenAI implementation journeys. Previously, he architected data platform and analytics solutions for strategic customers using a comprehensive range of AWS services including storage, compute, databases, serverless, analytics, and ML technologies. Leo also collaborates with internal AWS teams to drive product feature development based on customer feedback, contributing to the evolution of AWS offerings.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。