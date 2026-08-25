---
title: "Agentic observability with Amazon OpenSearch Service MCP Apps"
date: 2026-08-26T03:49:01+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "Prompt 工程", "Advanced (300)", "Amazon OpenSearch Service", "Announcements", "博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:9e0d620b18addd53149a113cf9765833488fda2d663794e15915d940760049bd"
source_payload_sha256: "sha256:2c50e7a2340606947a36fdab914923d160144866ff36febd20009e1529da2434"
observation_id: obs_ec596dac47b8163fa8f2f8957cf7431728879180b9e9df177844bd9d0a647272
event_id: evt_10adee7df7b6ab41a6d21c43ebe3583fe6ad75ba1475a9f025960be67dea812a
revision_id: rev_216e593d82d5002205848e30a75240d92416bbb1e0004c98516aba45e5db816a
source_published_at: 2026-08-25T19:00:09Z
first_seen_at: 2026-08-25T19:59:21Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 61
interpretation_sha256: "sha256:c41dbdf82d8eff2bce6d7f6afcb013eebd0aa3045c6939514d1730cd0ccdd9af"
description: "该内容介绍了通过扩展模型上下文协议，使可观测性代理在返回文本结论的同时，能够直接在对话界面中渲染交互式图表，从而省去在多个工具之间切换的手动验证环节。"
external_url: https://aws.amazon.com/blogs/machine-learning/agentic-observability-with-amazon-opensearch-service-mcp-apps
parent_observation_id: null
last_seen_at: 2026-08-25T19:47:21.268133Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/agentic-observability-with-amazon-opensearch-service-mcp-apps](https://aws.amazon.com/blogs/machine-learning/agentic-observability-with-amazon-opensearch-service-mcp-apps)
- **发布域名**: aws.amazon.com

## 要点解读

### 这是什么

该内容介绍了通过扩展模型上下文协议，使可观测性代理在返回文本结论的同时，能够直接在对话界面中渲染交互式图表，从而省去在多个工具之间切换的手动验证环节。

### 用在哪里

适用于需要快速定位分布式系统故障的工程师，特别是在使用可观测性平台且希望在同一环境中完成问题调查与结果核验的团队。

### 可以推断的

推测：在可观测性代理的实际使用中，验证步骤往往是效率瓶颈，此类将可视化结果直接嵌入对话的做法有望提升故障排查的整体速度。

推测：本地运行的方式更符合对数据主权有严格要求的组织，它们倾向于在自有基础设施内完成查询而非依赖外部服务。

## 来源摘要/节选

> Observability agents are fast. They query alerts, correlate logs with traces, and produce a root cause hypothesis in minutes. The part that still takes time is verification. You read the agent’s text summary, open your observability tools in a browser, navigate to the trace waterfall, check the service map to scope impact, and cross-reference what the agent told you against what you see on screen. The agent saved you the query time. It did not save you the tab-switching, context-carrying, manual-verification time. That is still your job.
>
> Amazon OpenSearch Service MCP Apps close that gap. MCP Apps extend the Model Context Protocol so that each tool call responds with an interactive visualization — a trace waterfall, a service topology, a log pattern view — rendered directly in your AI assistant’s chat window alongside the text response. You ask the agent to investigate. The agent queries Amazon OpenSearch Service. The response arrives with both a text explanation and the relevant dashboard widget. You verify in the same thread where you asked the question, without opening a separate browser tab or re-running a query.
>
> In this post, we explain how MCP Apps change your observability workflow and walk through setup step by step.
>
> The problem: Verification still requires leaving the agent loop
>
> The typical investigation loop proceeds as follows. First, the engineer asks the agent and gets a text-based root cause hypothesis. Next, they leave the IDE to open a browser and log in to a separate observability UI. They then re-run queries manually to reproduce what the agent found, in a different tool. After verifying visually by comparing the agent’s text output against actual dashboards, they return to the agent and resume the conversation, having lost their place in the investigation.
>
> The agent generates a response in seconds, but you must leave the agent’s environment to verify. This means logging in to a separate observability experience and navigating dashboards manually. This external verification loop is the bottleneck. It forces you into a tool-switching role that undermines the speed advantage of agentic automation.
>
> Organizations running agentic observability locally chose control and cost efficiency over vendor-provided AI. But this choice has historically come with a trade-off: local agentic setups sacrifice ease of use and sometimes agent performance compared to vendor-hosted solutions that tightly couple AI with their services. For these teams, the verification gap is the primary operational burden. They optimized for autonomy, yet verification still happens at human speed, in a separate observability tool.
>
> The solution: MCP Apps bring an observability UI into your IDE
>
> Amazon OpenSearch Service now supports MCP Apps, a capability that extends MCP with a dual response pattern.
>
> When your AI agent calls an MCP App tool, the response contains two parts. The first is a text summary with concise, structured data. The second is an interactive visualization rendered in the same conversation thread for you to review. OpenSearch MCP App generates the visualization by executing code against the same data sources that power your dashboards. Because of this, the results are deterministic. You’re not trusting the AI’s interpretation. You’re seeing the actual query result rendered as an interactive chart, trace waterfall, or service map.
>
> Figure 1: MCP App rendering an observability report inside the agentic IDE, showing error counts by service alongside AI-generated root cause analysis
>
> How it works
>
> The MCP Apps capability consists of a local MCP server, your IDE, and your OpenSearch UI application working together. This section explains the architecture, the protocol extension mechanism, and the end-to-end flow of a single tool call.
>
> Architecture
>
> A local MCP server runs on your machine. It acts as a secure bridge between your agentic IDE and your OpenSearch UI application. The server exposes observability tools that your AI agent can call. Each tool call goes through the MCP server to your OpenSearch UI endpoint, executes the query, and returns the dual response back to your IDE. OpenSearch UI is the serverless interface for unified observability that works with OpenSearch domains, serverless collections, CloudWatch, and Amazon Managed Service for Prometheus (learn more about OpenSearch UI).
>
> The following diagram shows the request flow:
>
> Your IDE or AI desktop client (Claude, VS Code, Cursor, etc.)
>
> ↓ tool call
>
> Local MCP server (runs on your machine)
>
> ↓ authenticated query
>
> OpenSearch UI application (connected with your data sources)
>
> ↓ dual response
>
> Your IDE ← text summary + interactive MCP App visualization
>
> You maintain full control. The MCP server runs locally. Your data stays in your AWS account. Your credentials, your policies, your domains.
>
> How MCP Apps extend the MCP protocol
>
> Standard MCP tool calls return text-only responses. The agent sends a JSON-RPC request specifying the tool name and parameters, and the server returns a text result that the agent incorporates into its reasoning. MCP Apps extend this pattern by adding a second response channel: a visualization payload that the IDE renders as an interactive widget alongside the text.
>
> When the local MCP server receives a tool call, it authenticates using your configured AWS credentials and forwards the request to your OpenSearch UI application endpoint as an HTTP API call. OpenSearch UI executes the query against your connected data sources and returns both a structured text summary and a rendered visualization artifact. Supported data sources include OpenSearch domains, serverless collections, and Amazon Managed Service for Prometheus. The MCP server packages these into a single MCP response containing the text content for the agent and the visualization content for the IDE host to render.
>
> The IDE host detects the visualization payload and renders it as an interactive widget in the conversation thread. OpenSearch MCP App generates the visualization server-side by executing code against your actual data. Therefore, the rendered output is deterministic and matches what you would see in your OpenSearch dashboards.
>
> A tool call end-to-end
>
> To illustrate the dual response pattern in practice, consider a trace investigation. The following walkthrough shows what happens when your agent calls the trace investigation MCP App tool.
>
> What the agent sends. Your agent issues a tool call to the trace investigation MCP App, passing parameters such as the trace ID or a filter like service name and time range. This call travels from your IDE to the local MCP server over the standard MCP protocol.
>
> How the server executes it. The local MCP server receives the tool call, authenticates against your AWS credentials, and forwards the request to your OpenSearch UI application endpoint. OpenSearch UI executes the trace query against your connected data sources, retrieves the matching spans, and assembles the response.
>
> What the dual response contains. The MCP server returns two outputs in a single response. The text portion contains a structured summary. It includes the trace ID, total duration, span count, the critical path, and an analysis of where the failure originated. The visualization portion contains an interactive trace waterfall rendered as an MCP App inside your IDE, showing the span hierarchy, timing, and error annotations.
>
> How the agent and human each consume it. From the text summary, your agent extracts context for its next reasoning step, for example correlating the failing span with related log entries. Meanwhile, you see the interactive trace waterfall in the same conversation thread. You can expand individual spans, inspect attributes, and confirm the root cause visually, without opening a separate browser tab.
>
> Available MCP Apps
>
> The MCP Apps support observability investigation across the lifecycle, with tools that chain together across investigation stages.
>
> Core investigation tools
>
> A typical investigation begins with triage and response tools, which surface active alerts, correlate related alerts across data sources, and present severity breakdowns so your agent can prioritize the issue. After the agent identifies the affected service, log investigation tools search for error patterns and cluster similar log entries to isolate the failure signature. From there, trace investigation tools locate the specific distributed trace, display the span hierarchy and latency breakdown, and pinpoint where the failure originated.
>
> Context and visualization tools
>
> To quantify the impact, metric investigation tools execute PromQL queries and perform threshold analysis, while service performance tools provide RED metrics (rate, errors, duration) at the service level. Topology tools render the service map as a dependency graph. The graph shows call volume and error rates across edges so you can scope the impact. Throughout the investigation, dynamic visualization tools generate line, bar, area, and metric charts from queries you specify, and datasets and correlations tools support cross-signal joins and data summaries.
>
> Specialized tools
>
> Specialized tools address emerging needs. AI and agent observability tools trace large language model (LLM) calls and render agent trace maps for teams building their own AI workflows. Stack health tools report cluster status and shard allocation. Instrumentation scoring tools detect telemetry quality gaps so teams can improve their observability coverage.
>
> Figure 2: Trace investigation MCP App showing span hierarchy, timeline, and failure origin analysis inside the IDE
>
> Revisiting the on-call scenario
>
> With MCP Apps, the same on-call investigation now looks like this.
>
> The engineer asks the agent: “What’s causing the spike in checkout errors?” The agent investigates by querying logs, correlating with traces, and checking the service map. A dual response arrives containing both a text summary and interactive visualizations (alert view, trace waterfall, and service map) rendered in the same thread. The engineer reviews inline by scrolling through the MCP App visualizations and selecting span details to confirm the scope of impact, without leaving the IDE. Finally, they instruct the agent to draft the issue summary or trigger a remediation.
>
> The engineer never leaves the IDE. Investigation, verification, and resolution happen in a single conversation thread. For on-call engineers, this means faster resolution and a more straightforward experience to collaborate with AI agents.
>
> Figure 3: Service map MCP App showing dependency graph with error rate color coding and call volume edge widths
>
> Getting started: Set up the MCP server
>
> Follow these steps to connect your agentic IDE to your OpenSearch UI application.
>
> Prerequisites
>
> Before you begin, check that you have the following:
>
> An OpenSearch UI application with an Observability workspace connected to at least one data source (Amazon OpenSearch Service domains, serverless collections, or Amazon Managed Service for Prometheus).
>
> A compatible agentic IDE (Claude Desktop, VS Code GitHub Copilot, Goose, ChatGPT, or Cursor).
>
> Node.js 22 or later installed locally.
>
> AWS credentials configured with es:ESHttpGet and es:ESHttpPost permissions.
>
> Step-by-step setup
>
> The following procedure walks through downloading the server, configuring your IDE, and verifying the connection.
>
> Step 1: Download and extract the MCP server
>
> Download and prepare the MCP server package:
>
> Navigate to the OpenSearch observability MCP server download page.
>
> Download the MCP server .zip file.
>
> Extract the archive. The extracted directory contains a server/server.js file. Note the full path to this file.
>
> Step 2: Add the MCP server to your IDE
>
> Each supported IDE has an MCP configuration file. The following list shows where to find it:
>
> Claude Desktop: Settings → Developer → Edit Config.
>
> VS Code GitHub Copilot: .vscode/mcp.json in your workspace, or User Settings → MCP Servers.
>
> Cursor: Settings → MCP → Add Server.
>
> Goose: ~/.config/goose/mcp.json (through extensions).
>
> ChatGPT: Settings → MCP Plugins → Add.
>
> Open the configuration for your IDE and add the following:
>
> {
>
> "mcpServers": {
>
> "opensearch-observability-stack-mcp": {
>
> "command": "node",
>
> "args": ["/path/to/opensearch-observability-stack-mcp/server/server.js"],
>
> "env": {
>
> "OS_UI_ENDPOINT": "application-foo-bar.us-west-2.opensearch.amazonaws.com",
>
> "AWS_REGION": "us-west-2",
>
> "AWS_PROFILE": "my-profile"
>
> }
>
> }
>
> }
>
> }
>
> Replace the placeholder values with your OpenSearch UI endpoint, AWS Region, and profile.
>
> To find your OpenSearch UI endpoint:
>
> Open the Amazon OpenSearch Service console.
>
> In the navigation pane, choose Applications.
>
> Select your OpenSearch UI application.
>
> Copy the Application URL (for example, application-abc123.us-west-2.opensearch.amazonaws.com).
>
> Step 3: Verify the connection
>
> After saving the configuration, restart your IDE or reload the MCP server list. Then enter the following prompt in your IDE:
>
> “List available observability data sources”
>
> If the agent returns your connected data sources (Amazon OpenSearch Service domains, serverless collections, or Amazon Managed Service for Prometheus workspaces), the MCP server is configured correctly.
>
> If you receive an error, check that your AWS credentials are active and that your AWS Identity and Access Management (IAM) policy includes the es:ESHttpGet and es:ESHttpPost actions for your OpenSearch UI application ARN.
>
> Tip: To test without production data, deploy the OpenTelemetry Demo application to generate sample traces, logs, and metrics in your Amazon OpenSearch Service domain.
>
> Clean up
>
> To remove the MCP server configuration, open your IDE’s MCP settings and delete the opensearch-observability-stack-mcp entry. Then delete the extracted MCP server directory from your local machine. This setup provisions no cloud resources, so you don’t need AWS side cleanup.
>
> Why this matters
>
> The following table summarizes how MCP Apps change the on-call workflow:
>
> Without MCP Apps
>
> With MCP Apps
>
> Agent returns text → open browser → log in → navigate → verify manually
>
> Agent returns text + interactive visualization → review inline
>
> You cannot see the underlying data in AI output
>
> MCP App results are deterministic (OpenSearch MCP App executes code)
>
> Context-switching between IDE and dashboard tabs
>
> Single conversation thread in your IDE
>
> Agent reasons only on its own output
>
> Agent reads MCP App results as additional structured context
>
> Human verification takes minutes across external platforms
>
> Verification compressed to seconds, inline with the agent
>
> Conclusion
>
> With MCP Apps, Amazon OpenSearch Service closes the verification gap in agentic observability. Your AI agent investigates, and the interactive proof arrives in the same thread: no context-switching, no separate logins, no re-running queries. For on-call engineers, this can mean faster resolution. For organizations running agentic observability locally, this provides the operational simplicity you wanted without sacrificing accuracy.
>
> Get started today: For setup instructions, see Agentic observability with MCP Apps in the Amazon OpenSearch Service Developer Guide.
>
> About the authors
>
> Arthur Hang Zuo
>
> Arthur is a Senior Product Manager with Amazon OpenSearch Service. Arthur leads OpenSearch UI platform and agentic AI features to enable observability and search use cases. Arthur is interested in the topics of Agentic AI and data products.
>
> Joshua Li
>
> Joshua is a Senior Software Engineer at Amazon OpenSearch Service. Joshua focuses on Observability features, UI experiences, and agentic AI integrations in OpenSearch Dashboards and OpenSearch UI.
>
> Shenoy Pratik Gurudatt
>
> Pratik is a Senior Software Engineer at Amazon OpenSearch Service. Pratik focuses on the intersection of Observability, Search, and ML, and contributes to critical OpenSearch mechanisms including Data Prepper, Reporting, Query Workbench, and the Observability Stack.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。