---
title: "How GoDaddy transformed its analytics with Amazon Quick"
date: 2026-08-27T01:04:33+08:00
draft: false
entry_kind: "auto"
tags: ["AI Agent", "生成式 AI", "机器学习", "Amazon Quick Sight", "Amazon Quick Suite", "Business Intelligence", "Customer Solutions", "博客与播客"]
categories: []
source: "blogs_podcasts"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:294e5f347a3a31c03ba2d8772e172553582ee47fd26762f2d41039bb3db18d8f"
source_payload_sha256: "sha256:0be9516e3a0482dd2ce395f716b67fa3e906d88230d95eb47172907b737bd391"
observation_id: obs_e71c780b6d875f94ab9ec400f88212626c8d9478b4bd58ce9a1bd39accb602b1
event_id: evt_5d1959cc4d9bfb235647f0f41e878914e7c02fd042c7e3b3f8ea9fc9dbcd023c
revision_id: rev_aa1487f1e92837918d65e3f6ea5200140077244cbbad3f04628f76a54c0a1561
source_published_at: 2026-08-26T16:51:53Z
first_seen_at: 2026-08-26T17:00:37.655232Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 55
description: "当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。"
external_url: https://aws.amazon.com/blogs/machine-learning/how-godaddy-transformed-its-analytics-with-amazon-quick
parent_observation_id: null
last_seen_at: 2026-08-26T17:00:37.655232Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/how-godaddy-transformed-its-analytics-with-amazon-quick](https://aws.amazon.com/blogs/machine-learning/how-godaddy-transformed-its-analytics-with-amazon-quick)
- **发布域名**: aws.amazon.com

## 来源摘要/节选

> GoDaddy is one of the world’s largest domain registrar and web hosting companies, serving more than 20 million customers and managing approximately 82 million domain names. At that scale, access to timely business data directly affects how quickly the company can act. When GoDaddy’s analytics infrastructure faced challenges under the weight of thousands of dashboards, mounting infrastructure costs, and performance that left business users waiting upward of 15 minutes for a single report to load, the company knew it was time for a fundamental change.
>
> In this post, you will learn how GoDaddy migrated from their legacy business intelligence (BI) tool to Amazon Quick. This was a two-year transformation that delivered results across every dimension of the business: 15,000 hours saved annually, 50% reduction in dashboard count, rendering times cut to under 5 seconds, and AI-powered self-service analytics now accessible to every employee. GoDaddy’s analytics team walks through the journey and shares the architectural decisions, cultural shifts, and automation capabilities that made it possible.
>
> “We migrated to Amazon Quick and cut dashboard rendering from 15 minutes to under 5 seconds. But the bigger win was cultural: with custom agents and automated flows, data-driven decisions became the norm across GoDaddy, not something reserved for analysts. Our teams saved over 15,000 hours annually and shifted to higher-value work.”
>
> – Jake Minette (Sr. Manager, Business Analytics), GoDaddy
>
> The challenge: When BI infrastructure becomes a bottleneck
>
> By the early 2020s, GoDaddy’s BI environment reflected the natural evolution of a fast-growing, data-driven organization. The company had built more than 5,000 dashboards — a testament to how deeply analytics had become embedded across the business. But with that scale came familiar challenges: dashboard rendering times could stretch beyond 15 minutes, and rising data volumes brought increased operational and licensing costs.
>
> Like many enterprises at this stage of analytics maturity, GoDaddy’s model relied on a centralized BI team to serve requests from marketing, finance, product, and customer experience. The team delivered strong work, but demand consistently outpaced capacity — a dynamic that made true self-service analytics difficult to achieve at scale. GoDaddy’s leadership saw an opportunity to take the next step: rather than continuing to add dashboards, they envisioned an approach that would put insights directly into the hands of the people who needed them, without requiring specialized technical skills.
>
> Evaluating the alternatives
>
> In early 2023, GoDaddy’s Data and Analytics Products team began a formal evaluation of the BI landscape. The team assessed their current BI tool’s own roadmap alongside several competitors including Amazon Quick Sight (BI capability of Amazon Quick). Three factors ultimately drove the decision toward Quick Sight.
>
> First, native integration with AWS services—including Amazon Redshift, Amazon Simple Storage Service (Amazon S3), and Amazon Relational Database Service (Amazon RDS)—meant that GoDaddy could build on the cloud infrastructure that it already operated rather than managing a separate BI stack. The serverless, auto scaling architecture removed the infrastructure overhead that burdened their previous BI tools deployment. Second, the pay-as-you-go pricing model offered a significantly more predictable and cost-effective path at enterprise scale. Third, the built-in machine learning (ML) capabilities of Quick Sight, including anomaly detection, forecasting, and natural language querying, offered a path toward democratized, self-service analytics.
>
> The migration journey
>
> The migration process from GoDaddy’s legacy BI tool to Amazon Quick Sight took roughly two years. This effort was driven by the substantial volume and intricate nature of their existing dashboards. The team made its decision in mid-2023 and completed a soft launch in the third quarter of that year. The remainder of 2023 was spent on foundational setup: establishing AWS integrations, building governance frameworks, migrating the first wave of dashboards, and onboarding the initial cohort of users. Throughout 2025, the team accelerated migration across business units, and by December 2025, the legacy BI tool was shut down entirely. Quick Sight had become GoDaddy’s primary BI solution.
>
> The migration was not a lift-and-shift exercise. Rather than recreating the 5,000-plus dashboards, the team used the transition as an opportunity to rationalize the portfolio. Redundant and underused dashboards were retired. The result was a leaner, more purposeful set of assets (fewer than 2,500 dashboards) that delivered more value with less maintenance overhead.
>
> By the end of 2025, GoDaddy had more than 4,298 active users, including 828 authors and 3,128 readers, with 2,532 dashboards and 229 topics in production.
>
> A hero use case: Reimagining the “Cash Dash”
>
> One of the clearest examples of migration’s impact is GoDaddy’s flagship financial analytics dashboard, known internally as the Cash Dash. Developed in partnership with the Business Analytics and Commercial teams, the Cash Dash serves as the company’s single source of truth for financial performance — used daily by finance teams, executive leadership, and operational stakeholders across the organization.
>
> The dashboard surfaces GoDaddy’s most critical financial and customer metrics in real-time. Users can drill into performance by product line, geographic region, date range, and transaction type — providing the kind of granular visibility that supports both day-to-day operational decisions and strategic planning at the executive level. Given its central role in how GoDaddy monitors business health, the Cash Dash was a natural candidate to showcase what a modern BI platform could deliver.
>
> After migration to Quick Sight, the same dashboard renders in under five seconds, a more than 10x improvement in dashboard performance that has fundamentally changed how GoDaddy’s teams interact with their data. The performance improvement alone was transformative, but the team went further. The rebuilt Cash Dash incorporates automated anomaly detection, so the finance team can operate on what they call a ‘1/10/60’ model. A 1/10/60 model is an incident response framework where anomalies are detected within one minute, investigated within ten minutes, and resolved within sixty minutes. This rapid response cycle prevents small issues from becoming major discrepancies. Alerts are routed through integrated communication channels, and weekly executive summaries are generated automatically through Data Stories and delivered directly to leadership via email. The dashboard also features intuitive drilldowns by product, region, date range, and transaction type, capabilities that previously required a data engineering request to access.
>
> Expanding into Amazon Quick
>
> In October 2025, Amazon Quick Sight evolved into Amazon Quick, bringing a new set of AI-powered capabilities alongside the core BI functionality that GoDaddy already adopted. Quick introduced Quick Research for deep-dive analysis across enterprise and public data sources, Quick Flows for natural language workflow automation, and custom Amazon Quick chat agents that allow teams to interact with their data through conversational interfaces.
>
> GoDaddy has also fully embraced Quick’s collaborative approach to knowledge sharing. They’ve created 30 Quick spaces to keep institutional knowledge organized and accessible, with a standout Dashboard Documentation Space that serves 50 active users so that the insights built today remain discoverable and actionable tomorrow.
>
> By November 2025, the Quick deployment was approximately 80 percent complete, and the results were already measurable.
>
> Custom chat agents: A data analyst for every employee
>
> GoDaddy has deployed seven custom chat agents within Quick, each tailored to a specific team or use case. The Dashboard Navigator agent helps users identify which existing dashboards are most relevant to their questions, reducing the time spent searching for the right resource. The Dashboard Assistance agent functions as an on-demand analytical resource. It has been described by users as having a data analyst sitting next to them, providing guidance, interpretation, and analysis support without requiring a formal request to the BI team.
>
> Other agents serve more specialized functions. The Domain Auction Assistant provides targeted insights for the team managing GoDaddy’s domain auction operations. The Top Accounts Growth Analyst supports the Premier Services team with analytics tailored to high-value account management. Additional agents serve the customer experience and product management organizations, so teams can conduct deep-dive analysis independently without SQL or Python skills and to understand customer behavior, care agent performance, and net promoter scores in real time.
>
> In April 2026 alone, GoDaddy recorded 1,999 agent queries across its deployed chat agents. Across the organization, the chat agent capability is estimated to save approximately 6,000 hours annually.
>
> Quick Flows: Automating the weekly business review
>
> Perhaps the most tangible demonstration of the automation potential of Quick at GoDaddy is the transformation of the Weekly Business Review (WBR) process.
>
> Before Quick Flows, preparing for a WBR was a manual, time-intensive exercise. Analysts across the organization spent hours each week navigating multiple dashboards, extracting key trends and insights, and assembling findings into a format suitable for executive presentation. The process was repetitive, and consumed analyst capacity that could have been directed toward higher-value work.
>
> The following image shows an example of how Amazon Quick Flows was used to automate the manual process of Weekly Business Reviews, using AI to scan each dashboard and surface key trends and insights.
>
> With Quick Flows, GoDaddy automated this entire workflow. The flow uses AI to review each relevant dashboard, identify key trends and anomalies, and synthesize findings into a structured summary ready for executive review. Since the beginning of 2026, the automated flow has been executed more than 100 times. Across all flows the estimated annual time savings exceeds 1,900 hours.
>
> Combined with the savings from chat agents, GoDaddy’s total estimated annual time savings from Quick automation now stands at more than 7,900 hours.
>
> A cultural shift toward data-driven decision-making
>
> The technical outcomes of GoDaddy’s Quick adoption are significant, but the more profound transformation was cultural, a shift from a centralized BI model. Teams that previously depended on centralized BI resources to answer data questions can now explore data independently, build custom reports, and act on insights without waiting in a queue.
>
> The reduction in dashboard count from more than 5,000 to fewer than 2,500 reflects a deliberate move away from a dashboard-centric model toward one focused on accessible, actionable insights. The introduction of natural language querying and conversational AI agents has extended that accessibility to users who would not have engaged with a traditional BI tool. Data-driven decision-making has shifted from a capability reserved for analysts to a norm across the organization
>
> Technical architecture and integration
>
> GoDaddy’s Quick deployment is built on a straightforward architectural foundation. Amazon Redshift serves as the primary data connection layer, with all data connections routed through Amazon Redshift as a recommended best practice. Authentication is handled through single sign-on using Okta, providing secure access consistent with GoDaddy’s broader ecosystem security model.
>
> The preceding image illustrates GoDaddy’s architecture diagram.
>
> The team has also invested in embedded analytics—integrating Quick dashboards directly into GoDaddy’s internal operational tools where users already work, rather than requiring them to switch to a separate BI application. This insights where you work approach increases adoption because users don’t need to remember to check a separate dashboard. The first embedded deployment was within Hivemind, GoDaddy’s internal experimentation platform, where Quick Sight dashboards now surface enriched insights from operational reporting powered by the Hivemind metadata service. A custom Quick Sight Embedding Service enables wide adoption across web applications, reducing dashboard deployment time from weeks to days.
>
> In the near future, GoDaddy plans to extend Quick to Slack, Outlook, Jira, and Confluence. These integrations will enable anomaly alerts and analytical insights to flow directly into the communication and project management tools GoDaddy teams use every day.
>
> Lessons learned
>
> Our two-year migration journey to Amazon Quick yielded several important insights that we believe can guide other enterprises embarking on similar transformations:
>
> Governance before scale.We built governance frameworks during our Q3 2023 soft launch, which prevented the same dashboard sprawl that plagued our legacy tool. Without early guardrails, we would have grown Quick to 5,000 dashboards again within a year. This proactive approach to governance ensured sustainable growth and maintainability from day one.
>
> AI adoption is a pull problem, not a push problem.Our seven chat agents weren’t built by IT and pushed to teams, we built them for specific team use cases (domain auctions, premier services, CX). Having teams define each agent’s purpose drove the 1,936 queries/month adoption that we’re seeing today. Generic ask anything agents would likely have seen a fraction of that usage. The lesson we learned: solve real problems for real teams, and adoption follows naturally.
>
> Embedded analytics &gt; standalone dashboards.We integrated Quick into Hivemind (GoDaddy’s experimentation platform) where people already work, which drove higher adoption than asking users to open a separate BI tool. The lesson: meet users in their workflow, not in yours. By reducing friction and embedding insights where decisions are made, we maximized the value of our analytics investment.
>
> Start with your highest-pain use case, not your easiest.We led with Cash Dash—GoDaddy’s flagship executive dashboard that folks avoided using because of 15-minute load times. Proving a 10x improvement on the most visible asset-built momentum faster than migrating low-traffic reports nobody cared about. This strategy generated immediate credibility and executive sponsorship that accelerated our broader migration.
>
> These lessons underscore a fundamental truth that we discovered: successful enterprise AI and analytics transformations require as much attention to organizational change management as they do to technical implementation.
>
> Looking ahead
>
> GoDaddy is actively exploring the next wave of Quick capabilities. The team is expanding its automation footprint beyond the WBR, identifying additional workflows where Quick Flows can remove manual effort and speed up decisions. Anomaly detection automation is being extended to additional data domains, with adoption growing among both leadership and analyst communities. As pending integrations with Slack, Outlook, Jira, and Confluence receive security approval, the team expects to further close the gap between insight and action.
>
> Conclusion
>
> GoDaddy’s move to a unified analytics solution shows what a focused cloud migration can deliver. The numbers tell part of the story: more than 15,000 hours saved annually, a 50 percent reduction in dashboard count, rendering times cut from 15 minutes to under five seconds, and more than 4,298 active users across the organization. But the deeper story is about a company that chose to rethink what analytics could be, not just faster reports, but a solution that surfaces relevant insights for each team automatically.
>
> For organizations evaluating their own BI modernization path, GoDaddy’s experience offers a clear proof point: the combination of cloud infrastructure, AI automation, and conversational analytics can deliver real business results for large organizations.
>
> Ready to start your own BI modernization journey? Begin by auditing your current dashboard usage—identify which dashboards are accessed regularly versus those gathering dust. Then, pilot Amazon Quick with a single high-value use case like GoDaddy’s Cash Dash. After you’ve proven the performance improvement, expand to automated workflows using Quick Flows for repetitive reporting tasks.
>
> To get started with Amazon Quick, see the resources below:
>
> Amazon Quick – Product Overview
>
> Amazon Quick – Customer Stories
>
> Reimagine business intelligence: Amazon Quick Sight evolves to Amazon Quick
>
> Amazon Quick Documentation
>
> Enhance Amazon Quick dashboards with on-demand data refresh
>
> About the authors
>
> Jake Minette
>
> Jake Minette is a Principal Analyst at GoDaddy with more than 20 years of experience leading data and analytics transformation. He focuses on designing and implementing agentic AI capabilities within the Analytics team, using Amazon Bedrock and Amazon Quick.
>
> Varun Malhotra
>
> Varun Malhotra is a Principal Customer Solutions Manager at AWS supporting the GoDaddy account team. He partners with executive leadership to strategize and implement generative AI solutions, driving revenue transformation for digital platform companies. He specializes in driving end-to-end revenue transformation for Digital Platform Companies, orchestrating integrated go-to-market strategies, and fostering cross-functional alignment for seamless delivery.
>
> Jake Wells
>
> Jake Wells is a Principal Account Manager at Amazon Web Services (AWS) who works with enterprise companies to develop and deploy AI, machine learning, and cloud platforms at scale. He partners closely with executive and technical leadership to align emerging technologies—such as generative AI and autonomous agents—with real business outcomes. Jake focuses on helping organizations modernize data infrastructure, accelerate AI adoption, and build production-grade AI systems on AWS.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。