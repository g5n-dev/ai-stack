---
title: "Evolving from legacy BI to agentic AI at Tradeshift with Amazon Quick"
date: 2026-07-21T20:03:24+08:00
draft: false
entry_kind: "auto"
tags: ["Amazon Quick Suite", "Customer Solutions", "博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:9972e63bb614f74cfdc600d1bcd6768333bd0b3bb42d95f7e6e84a172b5dd534"
source_payload_sha256: "sha256:915e74c7c3dad16867030f5b9a6b223028ecaedbe2076bb8fdede3276df56e0e"
observation_id: obs_44536b884bc0758ff22aa6e4612d879fff05e4fb5040f9367bcf8898af6d3a6a
event_id: evt_62cc970ee3d1db8b2af9213890084c0fdce8ebda1ef787fdee0bf3768cdd8960
revision_id: rev_270b1572c54e69add4729337e8eb34074f950404ac8479eaf8b60fe6b9386ff3
source_published_at: 2026-07-20T16:56:48Z
first_seen_at: 2026-07-21T12:02:44.255232Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 69
description: "当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。"
external_url: https://aws.amazon.com/blogs/machine-learning/evolving-from-legacy-bi-to-agentic-ai-at-tradeshift-with-amazon-quick
parent_observation_id: null
last_seen_at: 2026-07-21T12:02:44.255232Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/evolving-from-legacy-bi-to-agentic-ai-at-tradeshift-with-amazon-quick](https://aws.amazon.com/blogs/machine-learning/evolving-from-legacy-bi-to-agentic-ai-at-tradeshift-with-amazon-quick)

## 来源摘要/节选

> This guest post is co-written by Raphael Bres, Robert Iordache, Anca Andone, Ioana Millon (Ploesteanu) of Tradeshift and Roy Yung of AWS
>
> Tradeshift is an AI-powered accounts payable (AP) and e-Invoicing compliance platform serving buyers and sellers in more than 70 countries, with a cloud-based network that processes millions of transactions. We serve both sides of a marketplace, buyers and sellers, so our analytics needs are different from most companies. When our in-house business intelligence (BI) tool couldn’t handle our growing data volumes and customer expectations, we switched to Amazon Quick.
>
> Amazon Quick is an agentic AI workspace that connects to all your applications, tools, and data. It includes multiple features such as chat agent for natural language Q&amp;A over your business data, Flows for automating multi-step workflows without coding, and Research for producing comprehensive, long-form analytical reports from multiple sources. These capabilities are built on AWS with enterprise-level security.
>
> In this post, we describe how Tradeshift deployed Amazon Quick with agentic AI capabilities to replace our legacy BI tool, resulting in query response times up to 30 times faster, a 40 percent reduction in total cost of ownership, and turned embedded analytics into a product that generates revenue.
>
> Limitations of our legacy analytics tool
>
> For several years, Tradeshift relied on a proprietary BI tool built in-house. While it served basic reporting needs in the early stages of its growth, the tool imposed constraints that became untenable as our data volumes and customer expectations increased. Maintaining the tool consumed approximately 50 percent of one full-time employee’s capacity, diverting engineering resources away from product innovation. The tool supported a maximum of 10,000 rows per query, imposed a 25 MB ceiling on scheduled reports, and retained only six months of historical data. With these constraints, large-scale trend analysis, anomaly detection, or predictive modeling couldn’t be performed.
>
> The team sought a platform that would eliminate heavy maintenance, deliver enterprise-level performance for big data workloads, allow users to access and interact with data directly, and offer AI-powered natural language querying to democratize access to insights. Tradeshift’s Accounts Payable and Finance users needed heavy statistical analysis and data crunching at their fingertips, decoupled from the technical skills traditionally required for this kind of data introspection.
>
> Beyond technical constraints, the company’s Customer Success, Data and Analytics, and Commercial teams spent hours weekly on manual reporting such as exporting CSVs, running Excel macros, and assembling reports by hand. External customers who needed deeper insights into their AP workflows had no self-service path. They depended on Tradeshift’s engineering and BI teams to produce custom reports, creating bottlenecks that slowed decision-making on both sides.
>
> These challenges pointed to two categories of solutions that only agentic AI could address. First, automated workflows were needed to schedule dataset refreshes, trigger report distribution, and orchestrate recurring analytics tasks without manual intervention. The company has delivered these capabilities through Quick’s AI-powered workflow engine Amazon Quick Flows and deep research engine Amazon Quick Research. Second, a conversational chat interface was required to interpret natural language queries and instantly retrieve document metrics and operational data, eliminating the dependency on BI teams for day-to-day questions. This was achieved by building the AP Auditor chat agent powered by Quick chat agent.
>
> The team evaluated several alternatives, but Quick was the only solution offering scalability for large datasets, multi-device embedded access, AI-powered natural language querying, workflow, and unified internal and customer-facing analytics. Its agentic capabilities, including what-if modeling, automated workflows, deep research, and a conversational chat agent, together democratize data access across the organization.
>
> Building an embedded analytics product on Quick
>
> Tradeshift’s implementation followed a phased approach. The team began with a proof of concept in early 2024, progressed through an embedded analytics minimum viable product (MVP) from August 2024 through March 2025, and launched the full Reporting and Analytics app for buyers and sellers in June 2025. By August 2025, Quick had also replaced its internal BI tooling, achieving 98 percent adoption across the organization.
>
> The architecture serves three layers of analytics capability. The first layer consists of 16 embedded Amazon Quick Sight BI dashboards delivered through secure iFrames, covering nine domains: document invoicing, purchase orders, scanning, network connections, user activity, workflow automation, compliance and anomaly detection, payment prediction, and goods receipt-invoice reconciliation. These dashboards process between one million and one hundred million transaction records and return results in under three seconds, compared to the 45 to 90 seconds the legacy tool required.
>
> The second layer provides conversational AI access to the same underlying data. Users can ask natural language questions without needing SQL knowledge or data analytics expertise, and receive instant visual responses. The third layer introduces tiered data autonomy: a Standard tier offering pre-built dashboards with basic filters and CSV export, and a Premium tier that includes Designer Mode, custom dashboard creation, What-If modeling scenarios, and access to agentic AI capabilities.
>
> Security runs through four layers. Okta single sign-on (SSO) handles user authentication. Amazon Quick custom namespaces isolate each tenant. Signed URLs provide time-limited, session-bound embedding. And row-level security (about 14,000 RLS rules) filters data to each user’s context. To learn more about multi-tenant embedded dashboard, see Support multi-tenant applications for SaaS environments using Amazon Quick Sight.
>
> The following diagram illustrates Tradeshift’s embedded Quick Sight dashboard architecture.
>
> Measurable business results
>
> With the implementation of Amazon Quick, Tradeshift observed significant improvements in operational efficiency. Its internal accounts and support teams save 8.5 hours per week that were previously spent on manual CSV reporting. External buyers save 6 to 8 hours per week per user. Manual data manipulation, including Excel macros, VLOOKUPs, and pivot table assembly, decreased by 80 percent. The time required to identify operational bottlenecks dropped from one to two days to under five seconds.
>
> From a cost perspective, the company achieved a 40 percent reduction in total cost of ownership compared to its previous solution, a 35 percent reduction in infrastructure costs by shifting queries off production databases to SPICE, Quick Sight’s in-memory data engine, and a 30 percent consolidation of licensing costs across previously fragmented BI tools. Routine maintenance now requires only 0.5 full-time equivalent (FTE), down from the 50 percent FTE burden of the legacy system.
>
> The company realized a 2 percent incremental annual recurring revenue (ARR) expansion from existing buyer accounts through our premium reporting tier. Time-to-market for custom enterprise reporting improved by 75 percent. New reports that previously took four to six weeks now deploy in approximately one week. Accounts using embedded analytics show a 10 percent higher retention rate over 12 months compared to those that do not.
>
> Tradeshift reached 50 percent active monthly adoption across targeted enterprise buyers within the first year, achieved a 2x increase in analytics utilization by non-technical staff, and saw an 80 percent reduction in analytics-related support tickets. Internally, 98 percent of the organization actively uses the platform.
>
> Solving real customer problems with Amazon Quick
>
> The following two use cases highlight how Quick’s AI and BI capabilities address everyday business challenges for Tradeshift’s customers.
>
> The first use case centers on a generative AI-powered AP Auditor chat agent, built using Amazon Quick’s custom chat agent. Previously, AP auditors lacked immediate self-service access to document data. Resolving routine queries required manual effort and cross-functional dependencies on internal BI or engineering teams. This created bottlenecks that delayed real-time decision-making. With Amazon Quick, the team defined a purpose-built agent for the AP auditor persona using natural language instructions alone, without writing code. Through Quick Spaces, administrators control exactly which data sources the agent can access, ensuring every response is grounded in permissioned data. Users can now ask “Show me pending invoices from last month” or “What’s the status of PO #12345?” and receive immediate, accurate answers without waiting on other teams.
>
> Behind the agent sits a comprehensive knowledge architecture. The AP Auditor connects to a dedicated Quick Knowledge bases containing 11 reference documents spanning platform capabilities, policies, and process guides, alongside 9 dashboards, 14 curated query topics, and 68 automated action tools accessible via the Model Context Protocol (MCP). With this architecture, the agent goes beyond simple data retrieval. It can explain metric definitions, locate source data, and provide business context that previously required consulting a subject matter expert.
>
> The following video demonstrates Tradeshift’s generative AI-powered AP Auditor chat agent
>
> The second use case demonstrates Amazon Quick’s ability to handle high-volume BI workloads with fast query performance. A client lacked visibility into the manual operational overhead. Their AP team needed to quantify human effort required, understand workload distribution, and measure total approval workflow overhead. Using Amazon Quick data cache layer SPICE, the team built a reporting solution that processes large volumes of line-level coding data at speed. The solution distinguishes manual corrections from AI-generated codes, identifies individual coders, and tracks the full approval hierarchy. The client now has near real-time and historical visibility into operations, enabling them to spot bottlenecks. The same datasets and dashboards can also serve as knowledge sources for custom chat agents, extending BI insights into conversational AI.
>
> Transforming internal operations
>
> Internally, Tradeshift migrated from its legacy BI tool to Quick Sight and collapsed 40 separate dashboards that users previously had to navigate, into more than 100 queryable datasets accessible through natural language. Its teams in Finance, Operations, Product, and Customer Success can now ask questions in plain language and get answers immediately, with no SQL or analyst required.
>
> The quarterly market analysis process previously required multiple weeks of manual data gathering, cross-referencing, and interpretation. It now completes in days or hours using Quick Research, which generates multi-source analysis and synthesized reports from a single prompt. Rather than starting from scratch, analysts build on these research artifacts to conduct further deep-dive analytics, compressing what once took days into hours. Using Quick’s chat agent, they can interrogate data directly, generate visualizations, and produce executive summaries ready to share with stakeholders.
>
> Recurring reporting now flows through automated Quick Flows, a no-code automation engine. Teams use it to orchestrate dataset refreshes, report generation, and distribution as scheduled, repeatable pipelines. More than 270 SPICE datasets refresh daily, while reports are distributed automatically on daily, weekly, and monthly cadences without manual intervention. This freed the analytics team to focus on higher-value strategic work rather than routine data pipeline maintenance.
>
> The following video shows how Tradeshift uses Amazon Quick Flows and Research to automate its quarterly market analysis
>
> What makes this approach different
>
> Tradeshift’s customers are Accounts Payable teams, finance professionals managing invoices, approvals, and payment cycles across thousands of suppliers. These users are not data analysts. Before the company embedded agentic AI into its analytics platform, getting answers from their own transaction data meant filing a ticket, waiting on a BI team, and receiving a static report days or weeks later.
>
> That is the experience most AP automation platforms still deliver today. Tradeshift chose a different path. In 2025, it became the first in the AP automation and e-invoicing market to embed Amazon Quick for natural language querying, letting customers ask plain-language questions of their own data and receive instant responses without SQL or schema knowledge. In 2026, the company was a pioneer to integrate their MCP server with Amazon Quick, so that generative AI agents can read data catalog metadata, interpret Quick Sight schemas, and produce written insights autonomously.
>
> For its customers, this pace of innovation is the difference between self-service and dependency. Because the company moves fast and collaborates closely with AWS, every new agentic capability ships to the customer base within days or weeks. Custom development would have taken months or years. Users receive answers grounded in metric definitions from its knowledge bases, complete with explanations of how each number is calculated and where the source data lives. This eliminates cross-functional dependencies on engineering and BI teams entirely, collapsing what used to be multi-day report cycles into seconds.
>
> This positions Tradeshift customers at the forefront of AP analytics innovation. They engage with their data conversationally by asking questions, generating insights, and acting on real-time information in ways that static dashboards cannot deliver.
>
> Future developments
>
> Tradeshift’s roadmap focuses on three priorities. First, the team plans to enable write access on its production MCP server. Agents can then take live action on behalf of users, not just read and analyze data. Second, the company intends to embed a generic chat agent into the Standard tier of the analytics application, giving every user access to agentic AI by default, not just Premium subscribers. Third, it is expanding the Reporting and Analytics application to seller users across our network, extending its value to both sides of the marketplace.
>
> Next steps
>
> Amazon Quick and agentic AI helped Tradeshift transform analytics from a cost center into a revenue-generating product. By replacing a constrained legacy tool with a scalable, AI-powered platform, we reduced query times by 30 times, cut total cost of ownership by 40 percent, and delivered a self-service analytics experience that customers and internal teams actively choose to use every day. For organizations managing complex AP workflows at scale, the ability to ask questions in natural language and receive immediate, accurate, contextual answers means teams spend less time on manual reporting and more time acting on insight.
>
> To get started with your own analytics solution, explore the following resources:
>
> Transform your AP data with Tradeshift’s AI-powered Reporting and Analytics app.
>
> Learn more about Quick analytics capabilities in the Amazon Quick User Guide.
>
> Join the discussion in the Amazon Quick Community.
>
> About the authors
>
> Raphael Bres
>
> Raphael is the Chief Product and Technology Officer at Tradeshift, where he leads strategic product innovation and technological transformation across the company’s B2B ecommerce and fintech solutions. With over 25 years of experience in enterprise financial applications and B2B SaaS, Bres has held senior leadership roles at Oracle, Microsoft, Workday, and Certinia.
>
> Robert Iordache
>
> Robert is the Director of Data Science, Reporting and Analytics at Tradeshift, where he leads the company’s data strategy, AI/ML initiatives, and analytics innovation. He oversees teams of data scientists, analysts, and engineers focused on delivering advanced AI solutions and business intelligence capabilities that build AI solutions and analytics tools that improve Tradeshift’s products.
>
> Anca Andone
>
> Anca is the Senior Product Manager for Data and Analytics at Tradeshift, focusing on strategic growth in AI and innovation areas and on integrating AI tools for operational excellence.
>
> Ioana Millon (Ploesteanu)
>
> Ioana is the Senior Product Marketing Manager at Tradeshift. She works at the intersection of product, marketing, and engineering to shape positioning and user engagement strategy for AI-powered functionalities, e-invoicing compliance, and B2B integration solutions.
>
> Roy Yung
>
> Roy is the Senior GenAI Solutions Architect at AWS. Roy has over 10 years of experience implementing enterprise business intelligence (BI) solutions and now specialises in generative AI. Prior to AWS, Roy delivered BI and data platform solutions in the insurance, banking, aviation, and retail industries.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。