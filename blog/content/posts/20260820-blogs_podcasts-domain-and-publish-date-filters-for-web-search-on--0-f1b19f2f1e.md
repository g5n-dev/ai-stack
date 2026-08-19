---
title: "Domain and publish date filters for Web Search on AgentCore"
date: 2026-08-20T07:38:53+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "Prompt 工程", "Amazon Bedrock AgentCore", "Announcements", "Intermediate (200)", "博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:6e0cef5976d60a973459a50cfb301fa98df254f23f41208145244252db2cad6d"
source_payload_sha256: "sha256:14ee1409c7e501fe3d26d5a002bfa1c3e147d727799f6c69ca5f2ad053cd8177"
observation_id: obs_f1b19f2f1e664660449c3325cc5739c9544b8ac6d3a742c44dc51f1e0c625a28
event_id: evt_6c33f1520832222e71512979095736f9cde3c5d244aafb8178b795d312a18439
revision_id: rev_06bf756bd904c5395ad418b1fed03366ea52c34cc114e6f7cd843a1756a9041c
source_published_at: 2026-08-19T22:13:20Z
first_seen_at: 2026-08-19T23:36:24.945603Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 59
interpretation_sha256: "sha256:276dafdf1ab6fb21dd51b6ffce8241bdab15730ab8b87bb62b316b662d4b5c51"
description: "这是一项让开发者在调用时自行设定搜索范围和内容时效的功能，可在服务器端直接过滤掉不符合要求的网页来源和过旧的内容，而无需额外的编排流程。"
external_url: https://aws.amazon.com/blogs/machine-learning/domain-and-publish-date-filters-for-web-search-on-agentcore
parent_observation_id: null
last_seen_at: 2026-08-19T23:36:24.945603Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/domain-and-publish-date-filters-for-web-search-on-agentcore](https://aws.amazon.com/blogs/machine-learning/domain-and-publish-date-filters-for-web-search-on-agentcore)
- **发布域名**: aws.amazon.com

## 要点解读

### 这是什么

这是一项让开发者在调用时自行设定搜索范围和内容时效的功能，可在服务器端直接过滤掉不符合要求的网页来源和过旧的内容，而无需额外的编排流程。

### 用在哪里

需要严格管控信息来源和内容时效的场景会用到，例如合规审查类 agent 只应检索特定类型站点，或情报汇总类 agent 要求结果必须来自近期发布的内容。该功能同样适用于需要在同一平台为不同租户动态分配不同搜索策略的多租户服务。

### 可以推断的

推测：组织层面的域名白名单与运行时传入的过滤条件会结合生效，后者的约束范围只能在前者基础上收窄，无法突破前者已设定的边界。

推测：搜索请求全程在服务提供商的基础设施内处理，不经过外部网络，这可能有助于满足部分地区对数据本地化的合规要求。

## 来源摘要/节选

> When an AI agent uses Web Search to ground its answers on behalf of a customer, the organization behind that agent needs domain and date filters to control which sources the agent consults and how fresh those sources must be. A financial-services agent shouldn’t ground its answers in an unvetted blog. A product-information agent shouldn’t cite pricing or inventory data from three years ago when the user asked about current availability, as stock levels and pricing change rapidly.
>
> Today, we’re announcing runtime domain and published-date filtering for Web Search on Amazon Bedrock AgentCore, a platform to build, connect, and optimize agents at scale with any framework or model. This capability ships as part of the web-search connector version 1.2.0. These capabilities give developers per-call control over which web domains their agents can search and what publication-date window results must fall within, all enforced server-side. No external orchestration is required. When combined with existing admin-level domain policies, organizations have a layered filtering model that enforces enterprise governance while giving individual API calls the flexibility to narrow scope dynamically, per request.
>
> Alongside runtime filtering, this release also expands Web Search availability to two new AWS Regions: eu-west-1 (Dublin) and ap-northeast-1 (Tokyo). Customers in Europe and Asia Pacific can now invoke Web Search from a regional endpoint closer to their workloads, reducing latency and providing an EU-based entry point for organizations with data proximity requirements. AgentCore uses a zero-egress architecture where search queries remain within AWS. This regional expansion gives regulated customers in these regions a path to grounded agents without routing traffic across the Atlantic.
>
> In this post, we walk through what runtime filtering is, why it matters, how the layered admin-plus-runtime model works, how to get started with the new API parameters, and what regional availability means for your workloads.
>
> What’s new in connector version 1.2.0
>
> This launch introduces two new capabilities within the filters object of the Web Search tool input schema:
>
> 1. Runtime domain filtering
>
> Pass an include (allowlist) or exclude (denylist) list of domains on every tools/call invocation. This gives per-request control over which sources the agent may consult.
>
> Field
>
> Description
>
> filters.domainFilter.include
>
> Results from these domains are returned
>
> filters.domainFilter.exclude
>
> Results from these domains are suppressed
>
> Each list supports up to 100 domains, counted independently.
>
> 2. Published-date filtering
>
> Restrict results to content published within a specific date range using ISO-8601 UTC bounds:
>
> Field
>
> Description
>
> filters.publishedDateFilter.from
>
> Earliest publication date (inclusive)
>
> filters.publishedDateFilter.to
>
> Latest publication date (inclusive)
>
> Both filters are optional and applied per request. Omitting them preserves the existing behavior where all indexed content is eligible.
>
> Why runtime filtering matters
>
> Real-world agent workloads demand more granular control than organization-wide policies alone can provide:
>
> Per-task source restriction: A compliance agent analyzing regulatory updates should only search .gov domains and approved publishers, not the open web.
>
> Temporal scoping: A market-intelligence agent summarizing “this week’s earnings calls” should never surface results from prior quarters, even if they rank highly for the query.
>
> Dynamic allow/deny at call time: A multi-tenant platform serving different customers may need different domain policies per request, without creating separate targets for each tenant.
>
> Content freshness guarantees: A customer support agent answering “what changed in the latest release” should only return documentation published in the past 7 days.
>
> Runtime filtering addresses these needs by moving control into the API call itself.
>
> How it works: The request flow
>
> The following diagram shows the lifecycle of a filtered search request: your agent sends a tools/call with query and filters, the Gateway merges your runtime filters with the admin-level policy, executes the filtered query against the web index, enforces compliance on the raw results, and returns only verified results for your agent to ground its response on.
>
> Figure 1: Lifecycle of a filtered Web Search request, from tools/call to verified results
>
> The entire lifecycle is server-side. There’s no client-side filtering loop, no post-processing, and no additional roundtrips.
>
> The layered filtering model: Admin + runtime
>
> A key design principle of this launch is that runtime filters can narrow but never expand the scope set by an administrator. This ensures enterprise policy is always enforced, regardless of what a runtime caller requests. The admin-level domain lists are set up during creation of the connector resource.
>
> Merge logic
>
> The following diagram illustrates how admin-level and runtime filter lists combine: include lists merge by intersection (only domains present in both lists survive) while exclude lists merge by union (a domain blocked at either level stays blocked). Notice how d.com is dropped from the effective allowlist because it appears only in the runtime list, not the admin policy.
>
> Figure 2: How admin and runtime domain lists merge, intersecting include lists and unioning exclude lists
>
> Domain include (allowlist): The effective allowlist is the intersection of admin and runtime lists. If the admin allows [a.com, b.com, c.com] and the runtime call includes [b.com, c.com, d.com], only b.com and c.com are searched. The domain d.com is outside the admin domain list and is silently dropped.
>
> Domain exclude (denylist): The effective denylist is the union of admin and runtime lists. If the admin blocks [x.com] and the runtime call excludes [y.com], both are blocked.
>
> Note: A runtime caller can’t search a domain the admin hasn’t allowed and can’t unblock a domain the admin has denied. Runtime filters can only further restrict the search space.
>
> Filter compliance behavior
>
> When filters are active, Web Search prioritizes precision over recall. Results that can’t be verified against your filter criteria are excluded rather than returned unfiltered:
>
> Domain filter active: Results without a recognizable domain are excluded from consideration.
>
> Date filter active: Results without a recognized publication date are excluded.
>
> You might receive fewer results when filters are active, but every result you do receive satisfies your specified filter criteria.
>
> Cap enforcement
>
> There are four lists: admin include, admin exclude, runtime include, and runtime exclude. Each supports up to 100 entries independently. For full configuration details and composition rules, see Configure domain filtering in the Developer Guide.
>
> Getting started
>
> Web Search is delivered through AgentCore Gateway, a capability of Amazon Bedrock AgentCore that provides a managed endpoint, compatible with the Model Context Protocol (MCP), for connecting agents to tools. Follow these steps to enable runtime domain and date filtering for your Web Search target.
>
> Prerequisites
>
> An Amazon Bedrock AgentCore Gateway with a Web Search target pinned to connector version 1.2.0 or later.
>
> AWS Identity and Access Management (IAM) permissions: your calling agent or application needs bedrock-agentcore:InvokeGateway on the gateway Amazon Resource Name (ARN), and the Gateway’s service role needs bedrock-agentcore:InvokeWebSearch. See Configure the Gateway Service Role for the complete policy.
>
> The latest AWS SDK (Python, JavaScript, Java, .NET, Go, Ruby, or PHP).
>
> Step 1: Create a Web Search target with version 1.2.0
>
> Use AWS SDK for Python (Boto3) to create (or update) a target pinned to version 1.2.0, with admin-level domain policies. If you already have a Web Search target on version 1.1.0, you can use UpdateGatewayTarget to pin it to version 1.2.0 instead of creating a new target. For additional setup options, including the AgentCore CLI and console, see Set up Web Search Tool.
>
> import boto3
>
> gateway_client = boto3.client("bedrock-agentcore-control", region_name="us-east-1")
>
> # Create a Web Search target pinned to version 1.2.0 with admin-level domain filtering
>
> target = gateway_client.create_gateway_target(
>
> gatewayIdentifier="your-gateway-id",
>
> name="web-search-filtered",
>
> targetConfiguration={
>
> "mcp": {
>
> "connector": {
>
> "source": {"connectorId": "web-search", "version": "1.2.0"},
>
> "configurations": [
>
> {
>
> "name": "WebSearch",
>
> "parameterValues": {
>
> "domainFilter": {
>
> "include": [
>
> "approved-wire-1.com",
>
> "approved-wire-2.com",
>
> "sec.gov",
>
> "investor.gov",
>
> ],
>
> "exclude": ["unreliable-source.net"],
>
> }
>
> },
>
> }
>
> ],
>
> }
>
> }
>
> },
>
> credentialProviderConfigurations=[
>
> {"credentialProviderType": "GATEWAY_IAM_ROLE"}
>
> ],
>
> )
>
> print(f"Target ID: {target['targetId']}")
>
> print(f"Status: {target['status']}")
>
> Step 2: Invoke with runtime filters
>
> Imagine your agent monitors SEC enforcement actions for a legal team. The team only trusts sec.gov as a primary source, and they need actions from the current month, not historical filings. Here’s the tools/call payload your agent sends:
>
> {
>
> "jsonrpc": "2.0",
>
> "id": "1",
>
> "method": "tools/call",
>
> "params": {
>
> "name": "WebSearch",
>
> "arguments": {
>
> "query": "latest SEC enforcement actions 2026",
>
> "filters": {
>
> "domainFilter": {
>
> "include": ["sec.gov"],
>
> "exclude": []
>
> },
>
> "publishedDateFilter": {
>
> "from": "2026-07-01T00:00:00Z",
>
> "to": "2026-08-04T23:59:59Z"
>
> }
>
> }
>
> }
>
> }
>
> }
>
> The agent receives only results from sec.gov published in the last five weeks. There’s no third-party legal commentary or outdated filings in the results.
>
> Note: The tool name in your tools/call request is the name discovered through tools/list, which follows the pattern &lt;target-name&gt;___WebSearch. For the target created earlier, that’s web-search-filtered___WebSearch. The runtime include list (sec.gov) intersects with the admin list (approved-wire-1.com, approved-wire-2.com, sec.gov, investor.gov). Because sec.gov appears in both, it is searched. If you passed some-other-site.com, it would be silently dropped because it’s not in the admin allowlist.
>
> Sample code examples
>
> Here are some examples of how you can use the MCP client created from the AgentCore Gateway with the new filters at runtime. Code sample to create MCP client for calling tools
>
> Example 1: Clinical research assistant with regulatory citation requirements
>
> You’re building a research assistant for a pharmaceutical company’s regulatory affairs team. Company policy mandates that every answer cite only FDA, NIH, or ClinicalTrials.gov. A citation from a health blog isn’t only a quality issue. It’s a compliance violation that could surface in an audit. The agent needs to enforce this on every search, regardless of what query the model constructs.
>
> import json
>
> # Pharma research assistant: only approved regulatory sources
>
> compliance_request = json.dumps({
>
> "jsonrpc": "2.0",
>
> "id": "req-001",
>
> "method": "tools/call",
>
> "params": {
>
> "name": "WebSearch",
>
> "arguments": {
>
> "query": "FDA drug approval process 2026 guidance",
>
> "maxResults": 10,
>
> "filters": {
>
> "domainFilter": {
>
> "include": ["fda.gov", "nih.gov", "clinicaltrials.gov"]
>
> }
>
> }
>
> }
>
> }
>
> })
>
> # Send via your MCP client (SigV4-signed or OAuth-authenticated)
>
> response = mcp_client.send(compliance_request)
>
> results = json.loads(response)
>
> # Every result is from fda.gov, nih.gov, or clinicaltrials.gov
>
> for result in results["result"]["content"]:
>
> print(result["text"])
>
> Every result your agent cites is now verifiably from an approved regulatory source. Even if a WebMD article ranks #1 for the query, it never enters the model’s context window.
>
> Example 2: Stock-update agent, only this week’s coverage
>
> Your trading desk runs an agent that generates stock updates throughout the trading day. The problem: when a trader asks “what’s the latest on semiconductor stocks?”, the agent used to surface a highly-ranked analysis from last quarter, and a trader who acts on stale coverage loses money. You need every result to be from the past 7 days, no exceptions.
>
> from datetime import datetime, timedelta, timezone
>
> # Calculate the 7-day window
>
> now = datetime.now(timezone.utc)
>
> seven_days_ago = now - timedelta(days=7)
>
> stock_update_request = json.dumps({
>
> "jsonrpc": "2.0",
>
> "id": "req-002",
>
> "method": "tools/call",
>
> "params": {
>
> "name": "WebSearch",
>
> "arguments": {
>
> "query": "semiconductor stocks latest developments",
>
> "maxResults": 15,
>
> "filters": {
>
> "publishedDateFilter": {
>
> "from": seven_days_ago.strftime("%Y-%m-%dT%H:%M:%SZ"),
>
> "to": now.strftime("%Y-%m-%dT%H:%M:%SZ")
>
> }
>
> }
>
> }
>
> }
>
> })
>
> response = mcp_client.send(stock_update_request)
>
> The agent’s stock updates now draw only on coverage published in the last seven days. That highly-ranked analysis from last quarter? It never reaches the model, so it can never mislead a trader.
>
> Note: Results without a recognized publication date are excluded when the date filter is active. This ensures every returned result is verifiably within your time window.
>
> Example 3: Investor-relations compliance, primary sources, current quarter only
>
> Your investor-relations team uses an agent to prepare earnings analysis drafts. Two hard rules: (1) only primary sources: SEC filings and official investor pages: never crowdsourced financial commentary sites, and (2) only publications from this quarter, because citing last quarter’s numbers in a current-quarter analysis is a material error. You need both constraints enforced simultaneously on every search.
>
> # IR compliance agent: primary sources + current quarter only
>
> financial_request = json.dumps({
>
> "jsonrpc": "2.0",
>
> "id": "req-003",
>
> "method": "tools/call",
>
> "params": {
>
> "name": "WebSearch",
>
> "arguments": {
>
> "query": "AMZN quarterly earnings report Q2 2026",
>
> "maxResults": 10,
>
> "filters": {
>
> "domainFilter": {
>
> "include": ["sec.gov", "investor.gov"],
>
> "exclude": ["example-crowd-commentary-1.com", "example-crowd-commentary-2.com"]
>
> },
>
> "publishedDateFilter": {
>
> "from": "2026-04-01T00:00:00Z",
>
> "to": "2026-08-04T23:59:59Z"
>
> }
>
> }
>
> }
>
> }
>
> })
>
> response = mcp_client.send(financial_request)
>
> The agent’s draft now cites only official filings and wire reports from Q2 and Q3 2026. Crowdsourced commentary and opinion pieces are blocked even if they match the query perfectly. Anything from prior quarters is excluded regardless of source.
>
> Example 4: SaaS platform with per-tenant source policies
>
> You operate a research-agent SaaS platform serving healthcare, legal, and financial-services customers. Each tenant has contractually agreed source policies. Your healthcare customer’s Business Associate Agreement (BAA) requires citations from PubMed, CDC, and approved medical research databases only. Your legal customer insists on Cornell LII and official court records. Your finance customer mandates SEC, the Federal Reserve, and approved wire services. You can’t spin up a separate gateway target per tenant (you have 200 tenants and counting), so you apply tenant-specific filters at runtime using the Strands Agents SDK.
>
> from strands import Agent
>
> from strands.models import BedrockModel
>
> from strands.tools.mcp.mcp_client import MCPClient
>
> from mcp.client.streamable_http import streamablehttp_client
>
> # Per-tenant domain policies (from your config database)
>
> TENANT_POLICIES = {
>
> "tenant-healthcare": {
>
> "include": ["pubmed.ncbi.nlm.nih.gov", "who.int", "cdc.gov"],
>
> "exclude": ["example-consumer-health-site.com"],
>
> },
>
> "tenant-legal": {
>
> "include": ["law.cornell.edu", "supremecourt.gov", "uscourts.gov"],
>
> "exclude": [],
>
> },
>
> "tenant-finance": {
>
> "include": ["sec.gov", "federalreserve.gov", "example-approved-wire.com"],
>
> "exclude": ["example-social-forum-site.com"],
>
> },
>
> }
>
> def search_for_tenant(tenant_id: str, query: str, days_back: int = 30):
>
> """Execute a policy-compliant web search for a specific tenant."""
>
> from datetime import datetime, timedelta, timezone
>
> policy = TENANT_POLICIES[tenant_id]
>
> now = datetime.now(timezone.utc)
>
> date_from = (now - timedelta(days=days_back)).strftime("%Y-%m-%dT%H:%M:%SZ")
>
> def create_transport():
>
> return streamablehttp_client(
>
> gateway_url,
>
> headers={"Authorization": f"Bearer {get_token()}"},
>
> )
>
> mcp_client = MCPClient(create_transport)
>
> model = BedrockModel(
>
> model_id="us.anthropic.claude-sonnet-4-20250514-v1:0",
>
> max_tokens=2048,
>
> )
>
> with mcp_client:
>
> tools = mcp_client.list_tools_sync()
>
> agent = Agent(model=model, tools=tools)
>
> # The agent's system prompt instructs it to pass these filters
>
> # on every WebSearch invocation
>
> system_prompt = f"""You are a research assistant. When using WebSearch,
>
> ALWAYS include these filters in your tool call:
>
> - domainFilter.include: {policy['include']}
>
> - domainFilter.exclude: {policy['exclude']}
>
> - publishedDateFilter.from: {date_from}
>
> Never search outside approved domains."""
>
> result = agent(query, system_prompt=system_prompt)
>
> return result.message
>
> # Usage
>
> answer = search_for_tenant(
>
> "tenant-healthcare",
>
> "What are the latest clinical trial results for GLP-1 drugs?"
>
> )
>
> One gateway target serves 200 tenants, each with their own source policy, enforced dynamically at call time. Your healthcare tenant’s agent will never cite Reddit or WebMD, and your finance tenant’s agent will never cite a blog post, even though they share the same underlying infrastructure.
>
> Important: System-prompt-based filtering (as shown earlier) relies on the agent following instructions. It isn’t hard enforcement. For hard enforcement, configure allowed domains at the target level (admin include list). Runtime filters passed directly in the tools/call payload provide API-level enforcement that cannot be bypassed by the model.
>
> Input schema reference
>
> The filters object introduced in connector version 1.2.0 adds domainFilter (include/exclude lists, up to 100 domains each) and publishedDateFilter (inclusive ISO-8601 UTC bounds) alongside the existing query and maxResults fields. For the complete input schema and field-by-field reference, see Input schema in the Amazon Bedrock AgentCore Developer Guide.
>
> Availability and zero data egress
>
> Runtime domain and date filtering is available today in the US East (N. Virginia) (us-east-1), Europe (Ireland) (eu-west-1), and Asia Pacific (Tokyo) (ap-northeast-1) Regions for Web Search on Amazon Bedrock AgentCore.
>
> Web Search benefits from the zero data egress architecture of AgentCore: search queries are served entirely within AWS infrastructure. Customer queries are not sent to a third-party search engine or routed outside AWS. For organizations in regulated industries, such as financial services, healthcare, and government, this removes an entire category of compliance review.
>
> Backward compatibility
>
> These features are fully backward compatible:
>
> No breaking changes. Version 1.2.0 is a minor release. The new fields are additive and the filters object is optional. Existing API calls without filters continue to work exactly as before.
>
> SDK support. Available across AWS SDKs (Python (Boto3), JavaScript/TypeScript, Java, .NET, Go, Ruby, and PHP SDKs), AWS Command Line Interface (AWS CLI) and AgentCore CLI.
>
> Console support. The AWS Console for AgentCore Web Search targets now surfaces both include and exclude domain-list inputs in the connector configuration UI.
>
> Conclusion
>
> Runtime domain and published-date filtering give developers building on Amazon Bedrock AgentCore Gateway the per-call precision they need to build trustworthy, policy-compliant agents without sacrificing the simplicity of a managed, server-side search tool.
>
> Whether you’re restricting an agent to approved regulatory sources, scoping results to the last 24 hours, or dynamically applying tenant-specific policies, Web Search on AgentCore keeps you in control with zero data egress, IAM-native authentication, and no external dependencies.
>
> These features are available today in US East (N. Virginia) (us-east-1), Europe (Ireland) (eu-west-1), and Asia Pacific (Tokyo) (ap-northeast-1) AWS Regions for Web Search on Amazon Bedrock AgentCore.
>
> Get started today:
>
> Web Search filtering in the Amazon Bedrock AgentCore Developer Guide
>
> Amazon Bedrock AgentCore pricing
>
> Web Search on AgentCore product page
>
> About the authors
>
> Gaurav Deshmukh
>
> Gaurav is a Senior Software Development Engineer at Amazon AGI with nine years of experience at Amazon building large-scale distributed systems. He works on the information retrieval, grounding, and agentic AI services that power foundation models and AI agents, including capabilities available through Amazon Bedrock AgentCore. His work helps AI agents access accurate, real-time information and perform complex research tasks, improving the reliability of agentic applications at scale.
>
> Mike Erickson
>
> Mike is a Principal Engineer in the AGI for AWS organization, specializing in search. Currently, he is focused on optimizing search tools for use in agentic workflows, including search ML model performance, scalability, tool design, experiment design, and evaluation.
>
> Kalyan Garimella
>
> Kalyan is a Principal Product Manager at Amazon AGI, where he leads the development and launch of web search capabilities for Amazon Bedrock AgentCore. His work focuses on solving a core limitation of modern AI agents — their inability to access real-time, factual information — by enabling agents to ground their reasoning in live web data. Kalyan lives in the Bay Area with his family.
>
> Omar Abdelwahab
>
> Omar is a Technical Product Marketing Manager at Amazon Web Services (AWS), where he focuses on AI products including Agentic AI and Web Search. He holds a Ph.D. in Computer Science and enjoys working at the intersection of AI, technology, and go-to-market strategy to help customers build innovative applications.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。