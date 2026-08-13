---
title: "First Orion accelerates QA automation using Amazon Nova Act"
date: 2026-08-12T03:22:40+08:00
draft: false
entry_kind: "auto"
tags: ["AI Agent", "生成式 AI", "Amazon Nova", "Customer Solutions", "博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:c4d9f86656889374917cede144c41a7a1ae6488c2a4afba7ff52a001c3377a22"
source_payload_sha256: "sha256:04103b251c39cc6a9ababb72532a5b5b7866995ace2fc098183a8b601e6acd6e"
observation_id: obs_5c3907356da7f745f17db19dcd41ed48579567790b5c66239aec34ab1dfc55f6
event_id: evt_3649201a58ca39859913ba2ebbc823f8463c57d0dcf32d850b7dcb1f568259b9
revision_id: rev_b30ad6663c012bb9a9d6e96ae4f728b49e5e915487f4897a4153754d36440808
source_published_at: 2026-08-11T16:09:06Z
first_seen_at: 2026-08-11T19:32:21Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 59
interpretation_sha256: "sha256:e83626d05158a2bab2bfb648f81c94dab8ebaf47bb1e115b68ba8068f76ea02b"
description: "First Orion 采用能够用自然语言描述测试意图的 AI 代理，实现了 UI 自动化测试的快速编写和维护，以解决传统脚本因页面结构变化而失效的问题。"
external_url: https://aws.amazon.com/blogs/machine-learning/first-orion-accelerates-qa-automation-using-amazon-nova-act
parent_observation_id: null
last_seen_at: 2026-08-13T00:00:00Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/first-orion-accelerates-qa-automation-using-amazon-nova-act](https://aws.amazon.com/blogs/machine-learning/first-orion-accelerates-qa-automation-using-amazon-nova-act)
- **发布域名**: aws.amazon.com

## 要点解读

### 这是什么
First Orion 采用能够用自然语言描述测试意图的 AI 代理，实现了 UI 自动化测试的快速编写和维护，以解决传统脚本因页面结构变化而失效的问题。

### 用在哪里
适用于拥有多个 Web 业务线且需要频繁发布新功能的企业 QA 团队，特别是从脚本化测试转向更灵活的 AI 驱动测试的组织。

### 可以推断的
- 推测：使用自然语言描述测试可以降低对编程经验的依赖，使业务分析师也能参与自动化测试编写。  
- 推测：在页面结构经常改动的项目中，这种方式能够提升测试的鲁棒性，减少因 DOM 变更导致的维护成本。

## 来源摘要/节选

> This post is co-written with Mark Himelfarb and Garrett Wilkerson from First Orion.
>
> First Orion’s engineering teams were shipping faster than quality assurance (QA) could test, until Amazon Nova Act transformed QA automation. As a branded communications company whose solutions reach hundreds of millions of phone calls across carriers in the US, Canada, UK, and Germany, First Orion needed their QA to keep pace with rapid development velocity. The solution was a shift from script-based test automation to agents driven by AI that understand web interfaces the way a human does. This post describes how First Orion adopted Amazon Nova Act, the architecture they built around it, and the results they achieved.
>
> First Orion was founded in 2008 with a single belief: every communication should be clear, trusted, and recognized. Today they have over 300 team members across offices in North Little Rock, Seattle, London, and Dubai. Their solutions run across all major US carriers including T-Mobile, Verizon, AT&amp;T, and Boost Mobile, major Canadian carriers, Vodafone in the UK, and Deutsche Telekom in Germany. Coverage is increasing with their Global Exchange. They help businesses connect with customers through branded calling, messaging, and identity solutions while protecting both parties from spam, scam, and spoofing. They serve a wide range of customers, from small businesses to global enterprises, including Fortune 500 companies. Their product suite covers the full communications lifecycle: INFORM Branded Calling, ENRICH Branded Messaging, AFFIRM Number Monitoring, SENTRY Call Blocking, and PROTECT+ Risk Detection.
>
> They believe the future of communication is built on trust, transparency, and intelligent technology, and innovation is central to their strategy. They invest in AI, conversational intelligence, and data-driven platforms to continuously improve how brands engage with their customers. That growth created an engineering challenge. As First Orion expanded into the small and medium-sized business (SMB) market alongside their enterprise customers, their web applications multiplied, and so did the QA burden of testing them.
>
> Decentralized portals outpaced QA team
>
> First Orion moved from a monolithic web portal to a decentralized, product-specific, modular, cell-based architecture. In this model, each team owns the applications for its own line of business and synchronizes only over a small, shared piece of the underlying platform. This let teams move in parallel at higher velocity, though it required substantial re-engineering of the platform to support. At the same time, as First Orion pushed further into the SMB market, the range of device form-factors and browser versions their customers used grew significantly, multiplying the combinations every application had to be tested against.
>
> UI testing quickly became the bottleneck. QA teams could not keep up with the sprawling set of web applications, and the consequences compounded: release velocity stalled, new features shipped with lower quality, and engineering time was increasingly consumed by regressions rather than new capabilities.
>
> First Orion’s QA team includes both QA Analysts and QA Automation Engineers. Automation Engineers build durable test suites from test case definitions and other documentation, while QA Analysts focus on requirement analysis, test case definition, exploratory testing, and software-quality risk management. But the incumbent test automation frameworks they relied on were inherently fragile, and three problems in particular slowed the team down.
>
> First, regression testing was not self-service. Developers needed a straightforward way to run regressions across the paths they touched before shipping to the test environment, but the existing test cases carried extensive dependencies that made them difficult to run on demand.
>
> Second, new features suffered from a test case gap. To write tests for a new feature, that feature first had to be developed and deployed to the test environment, so that QA Automation Engineers had the selectors, labels, and other elements they needed in the Document Object Model (DOM). This forced QA Analysts and Engineers to context-switch to other work while waiting, and with so many features shipping in rapid succession, the result was mounting cognitive load and constant dependency wrangling.
>
> Third, the test scripts themselves were brittle. QA Automation Engineers typically received applications only after developers finished the code, always close to release. As they worked through Selenium and Playwright scripts, element IDs, classes, and other DOM and JavaScript attributes changed faster than they could fix them. Traditional automation was not augmenting the manual effort quickly enough to matter for a given release, and releases could slip as a result. Increasing the size of the QA team helped at the margins but did not address this root cause.
>
> First Orion realized they did not need more of the same. They needed a fundamentally different approach. Instead of writing code that describes how to navigate a UI, they wanted to describe what to test in plain English and have an intelligent agent handle the rest. That requirement led them to Amazon Nova Act.
>
> Why Amazon Nova Act fits First Orion’s requirements
>
> First Orion’s requirements came down to two problems: selector-based tests that broke as the UI changed, and the time it took to author new ones. Nova Act addressed both by letting QA Analysts describe tests in plain English rather than write and maintain code. When their AWS account team introduced them to Nova Act in March 2025, First Orion became a pre-release adopter and found value well before general availability.
>
> With Nova Act, First Orion describes what they want accomplished in natural language, not how to accomplish it. For example: “Log into the portal, navigate to billing, and verify the invoice total.” The agent reasons about the current UI state, identifies elements, and runs multi-step sequences autonomously. This was the critical difference from Selenium and Playwright. Those frameworks required QA Automation Engineers to write and maintain explicit element selectors that broke with every sprint. Nova Act instead reasons about what it sees on screen: labels, layout, and context. A Nova Act instruction like “click the Submit button” works regardless of the underlying CSS class. The model adapts to changing page layouts, handles dynamic content, dismisses pop-ups, and recovers from errors without human intervention. Developers can also interleave Python code, assertions, breakpoints, and parallelization directly with Nova Act commands.
>
> For First Orion, this meant three things:
>
> QA Analysts could author tests directly — no waiting for automation engineers to translate test cases into code.
>
> Tests survived UI changes — because Nova Act does not rely on fixed selectors, scripts no longer broke every sprint.
>
> No browser infrastructure to manage — AgentCore Browser handles provisioning, session recording, and parallel execution.
>
> How First Orion uses Nova Act
>
> First Orion’s main use case for Amazon Nova Act is testing their customer portal applications. They built an end-to-end system around the Amazon Nova Act SDK that takes QA analysts from English-language test case authoring through automated execution to integrated reporting. The following diagram shows the architecture, and we walk through each component below.
>
> Figure 1: Architecture overview of First Orion’s Nova Act test automation system
>
> The workflow begins with the Test Case Authoring UI, a React frontend where QA analysts browse, create, edit, and validate test cases in plain English. A custom templating engine handles dynamic variables (phone numbers, email addresses, business names) so the same test collection generates unique, realistic data on every run. Test collections are stored as JSON in Amazon Simple Storage Service (Amazon S3), which serves as the central repository.
>
> When a QA analyst triggers a test run, the Nova Act Test Runner picks up test cases from Amazon S3. This runner is a Python application on Amazon Elastic Container Service (Amazon ECS) with AWS Fargate that orchestrates execution through the Amazon Nova Act SDK. The runner does not manage browsers directly; instead, it delegates browser operations to Amazon Bedrock AgentCore Browser. AgentCore Browser provisions managed browser instances, handles session recording, and supports parallel execution behind multi-factor authentication (MFA) without requiring changes to the target application’s auth flow. Browser profiles can start tests in a particular browser state, avoiding full login flows for every run.
>
> The Amazon Nova Act model receives natural language instructions from the test runner, reasons about the target web application’s current UI state, and executes the specified actions autonomously. Nova Act handles the browser manipulation on its own, the calling code does not need to manage selectors, waits, or page transitions.
>
> Results flow into an Allure reporting dashboard with a Microsoft Teams integration for notifications. First Orion relies on AgentCore for session recording and links video replays directly in their reports. The Microsoft Teams and Allure required custom integration. The Nova Act test runner used a Python script to orchestrate the SDK calls.
>
> Adopting this architecture has tightened integration between the QA and engineering teams. As more testing moves into the agentic flow, dependence on other vendors shrinks. First Orion also adopted the Kiro IDE for prototyping and development. Kiro’s built-in knowledge of AWS services and ability to read code bases made wiring everything up straightforward.
>
> The following figure shows an example test case as authored in the React UI. QA analysts write instructions in plain English (for example, “Navigate to the Billing page, verify the invoice total matches the expected amount, and download the PDF”). The Amazon Nova Act SDK translates these into browser actions at runtime without requiring element selectors or programming knowledge from the test author.
>
> Figure 2: Test case authored in plain English in the React UI
>
> The Allure dashboard provides test-level pass/fail status, execution timelines, and links to AgentCore Browser session recordings for debugging failed tests.
>
> Figure 3: Allure reporting dashboard
>
> Figure 4: Allure test results
>
> Before Nova Act, a QA Automation Engineer would manually identify DOM selectors, write scripts, debug brittle selectors, and iterate. This process can take days per test case. With this architecture, a QA Analyst takes the same English-language test case and runs it within minutes. The turnaround from test case definition to automated run dropped from days to minutes for supported scenarios.
>
> Results and impact
>
> While Amazon Nova Act is still in its adoption period and First Orion is adding features around it to fit their environment, they have seen as much as 20–25 percent reduction in QA cycles for specific types of testing. As coverage expands to additional application modules, they expect further efficiency gains.
>
> They estimate saving 25–30 percent of Engineering time with Nova Act, decreasing the amount of context switches between features. Engineering capacity that was previously needed to support the QA function has been redirected to feature engineering and value creation, allowing First Orion to focus on serving their customers better.
>
> Fully automated Nova Act runs allow for early regression detection and quick new feature testing, increasing their test coverage by upwards of 15 percent in some cases. By running tests against every build without waiting for manual QA availability, First Orion catches regressions earlier in the development cycle, before they reach production.
>
> Lessons learned and best practices
>
> Organizational buy-in matters. First Orion’s culture of trying new things and shipping quickly made adoption possible. Teams considering agentic automation need leadership support and room to experiment. For teams considering agentic automation: have a plan but stay flexible. This space moves fast and what failed last month can work today with a new model update.
>
> One early challenge was the predictability of the model’s navigation path. First Orion’s QA engineers wanted to confirm the agent took the same route through the site given the same preconditions, but initially Nova Act would reach the target state by different paths. By tuning parameters exposed through the Amazon Nova Act SDK, they significantly improved behavioral consistency.
>
> Another learning was the importance of clear prompts. While English test cases can be written for the SDK, the prompts still needed tuning to work well with the model. Following the AWS documentation guidance on structuring prompts increased test reliability.
>
> A related but distinct issue was that AI agents do not share institutional knowledge. Unspoken preconditions, navigation patterns, and business rules must be explicitly provided in prompts. Building this context into test case definitions was key to achieving consistent results.
>
> What’s next
>
> First Orion’s roadmap with Amazon Nova Act is ambitious. Their next step for the QA-specific use case includes automated test generation using Kiro and Model Context Protocol (MCP) servers that give AI tools access to code changes and requirements documents. By having Kiro see code changes and check requirements, First Orion envisions a fully automated test generation pipeline that feeds directly into their Nova Act implementation, further freeing QA Engineers for higher-value tasks.
>
> They also plan to use Nova Act for critical path analysis, understanding how AI navigates their sites to identify where products can improve. Feeding this information into other systems can provide feedback to web designers and marketing teams, helping them build more efficient webpages that lead to better customer experiences.
>
> Conclusion
>
> First Orion’s adoption of Amazon Nova Act demonstrates how agentic AI can transform QA workflows from a bottleneck into a competitive advantage. By shifting from brittle, selector-based automation to natural language-driven testing, First Orion reduced QA cycle times, freed engineering capacity for feature development, and improved their ability to catch regressions early. Their willingness to adopt new technology early and their close collaboration with our team as a launch partner positioned them to move faster and build a testing architecture that scales with their growing product portfolio.
>
> First Orion CTO Mark Himelfarb sums it up:
>
> “This isn’t just a tool. It’s a competitive edge. Tasks that took hours now take minutes, so we keep standards high while we scale.”
>
> — Mark Himelfarb, CTO, First Orion
>
> Ready to get started? Visit Nova Act Playground to prototype your first workflow without writing code. When you’re ready to build, install the Nova Act IDE extension for VS Code, Kiro, or Cursor to develop and deploy agents from your IDE. For a production-ready architecture guide, see Agentic QA Automation using Amazon Bedrock AgentCore Browser and Amazon Nova Act, and refer to the Amazon Nova Act documentation for more details.
>
> About the authors
>
> Avinash Ranganath
>
> Avinash is a Lead Technical Account Manager at AWS supporting large enterprise customers across the US. With 17+ years of experience in cloud architecture, cybersecurity, and networking, he helps organizations navigate complex cloud transformations — from AI/ML adoption to security modernization. Avinash is a subject matter expert for Incident Detection &amp; Response and Unified Operations.
>
> Libin Roy
>
> Libin is a Senior Solutions Architect at AWS, where he supports large enterprise customers across the United States. With 11 years of experience in cloud solution design, he helps organizations design, migrate, and modernize their infrastructure on AWS. Libin partners closely with both executive leadership and technical teams to align architecture decisions with business outcomes and accelerate cloud adoption at scale.
>
> Mark Himelfarb
>
> Mark Himelfarb, CTO of First Orion since 2009, has more than 25 years of experience in software engineering and architecture. He leads the company’s Software Architecture and Engineering practices focused on Call Protection and Branded Communication in telecommunications, while integrating Data Science and AI/ML capabilities. Mark is also responsible for adopting generative AI and state-of-the-art tools to enhance engineering practices, improve efficiencies, and foster a culture of skill and career development. He holds a B.S. in Computer Science and Mathematics/German from UALR, where he completed a NASA-sponsored capstone project in video transmission compression and telemedicine research.
>
> Garrett Wilkerson
>
> Garrett Wilkerson joined First Orion in 2021 and has approximately 5 years of experience in software engineering, spanning mobile development, backend systems, and quality assurance automation. He has held roles across multiple engineering disciplines at First Orion, including Android development, backend engineering, and test automation, with previous experience in Selenium and Robot Framework providing valuable context for agentic testing tools like Nova Act. Currently, Garrett is focused on advancing QA automation and AI-driven initiatives that integrate AI services into automation frameworks to identify defects earlier and reduce manual testing overhead. He holds a B.B.A in Accounting from the University of Arkansas at Little Rock (UALR).

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。