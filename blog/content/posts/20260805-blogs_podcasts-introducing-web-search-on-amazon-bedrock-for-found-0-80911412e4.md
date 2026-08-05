---
title: "Introducing Web Search on Amazon Bedrock for foundation model grounding"
date: 2026-08-05T07:21:52+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "生成式 AI", "Prompt 工程", "Amazon Bedrock", "Announcements", "Intermediate (200)", "博客与播客"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:ca2dd475bb9d5b486cadb29cfcaf73d881f3aa7e94798f5d9f98c231b7615f13"
source_payload_sha256: "sha256:0db1c6c532f191aa577bf8eba6339ce8b9087e84952682c7ab6ab48d063eeaa4"
observation_id: obs_80911412e4d1c0f0cf5f71d0adb2b01d83689d9ff1dfcfa41904e7e4252c4a99
event_id: evt_03d475bcb580e344af114928150020d0c1db404126fd90240ead9ffcc4c5e50e
revision_id: rev_e91bc1070f850a53869040ca392f58a9a2edcfa90f2c193a6a872f5931b2d00d
source_published_at: 2026-08-04T18:39:14Z
first_seen_at: 2026-08-04T23:18:53.691477Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 71
interpretation_sha256: "sha256:a1f8ecdf74a5fb40fc6f6db22740d5f184d6e58e5a76f10b84341e7166af3ac2"
description: "Amazon Bedrock 新增了内置 Web Search 功能，让模型在需要最新网络信息时直接检索网页并生成带来源的答案，无需自行集成第三方搜索服务。该功能结合亚马逊自有的网页索引与知识图谱，以语义片段形式向模型提供精炼内容。"
external_url: https://aws.amazon.com/blogs/machine-learning/introducing-web-search-on-amazon-bedrock-for-foundation-model-grounding
parent_observation_id: null
last_seen_at: 2026-08-04T23:18:53.691477Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/introducing-web-search-on-amazon-bedrock-for-foundation-model-grounding](https://aws.amazon.com/blogs/machine-learning/introducing-web-search-on-amazon-bedrock-for-foundation-model-grounding)
- **发布域名**: aws.amazon.com

## 要点解读

### 这是什么
Amazon Bedrock 新增了内置 Web Search 功能，让模型在需要最新网络信息时直接检索网页并生成带来源的答案，无需自行集成第三方搜索服务。该功能结合亚马逊自有的网页索引与知识图谱，以语义片段形式向模型提供精炼内容。

### 用在哪里
适用于在聊天机器人、代码辅助、CLI 工具或企业应用中希望模型实时获取外部信息的开发者。对关注数据合规、期望所有请求均在 AWS 环境内部完成的企业尤其有帮助。

### 可以推断的
推测：由于只需在 API 请求中加入工具参数即可启用，现有 OpenAI 兼容的应用迁移成本相对较低。  
推测：检索阶段采用语义抽取而非完整页面返回，可能降低返回的 token 数量，从而提升响应速度。

## 来源摘要/节选

> When a foundation model needs to answer a question about last week’s earnings call, yesterday’s regulatory change, or this morning’s weather forecast, it needs knowledge it was never trained on. Grounding the model in current web knowledge closes that gap – whether it’s powering chatbots, coding assistants, CLI tools, or enterprise applications, grounding helps answer questions beyond the model’s training and reduces hallucinations.  Traditionally, connecting a model to web knowledge required developers to identify, integrate, and maintain a third-party Web Search provider, a process that delays project timelines and introduces data residency risks and operational overhead.
>
> At AWS New York Summit 2026, we announced the general availability of Web Search on AgentCore. Today, we are extending it further with the general availability of Web Search on Amazon Bedrock. It is a server-side built-in tool that grounds model responses in current web knowledge. With Web Search, grounding becomes a native capability of Amazon Bedrock, with no third-party vendors to onboard, no external APIs to orchestrate, and no additional third party vendor security reviews to conduct.
>
> In this post, we walk through what Web Search on Amazon Bedrock is, why it matters, how to enable it using the OpenAI Responses API, and how to get started with the tool.
>
> What Web Search on Amazon Bedrock provides
>
> Web Search is designed for Amazon Bedrock model inference, with the following differentiators:
>
> Multi-source grounding approach: Web Search is backed by a web index that Amazon operates, spanning billions of documents and refreshed continually. It combines this index with a built-in knowledge graph that anchors the entities in a domain along with the connections between them. When a question is factual in nature; say, who wrote a particular book or what year an event took place; Web Search uses the knowledge graph to answer with strong confidence, rather than leaving the model to infer the answer from extracted page text. That can help cut down on the small factual inaccuracies that tend to slip in whenever an agent assembles an answer from fragments on its own.
>
> Context-efficient retrieval. Rather than handing the model a raw page and hoping it finds the relevant part, Web Search performs semantic snippet extraction – pulling the passages from each web page that bear on the query and returning them in a form optimized for the model’s context window. The model sees the parts that matter, with fewer tokens spent on boilerplate. Retrieval is fast, so grounded responses can be delivered with minimal latency.
>
> Single-parameter enablement. Web Search becomes a single parameter in your existing OpenAI-compatible API call, removing the need for vendor onboarding, API keys, orchestration layers, and separate SDKs.
>
> Helping with enterprise-grade compliance out of the box. By default, Web Search on Bedrock offers zero data egress, so your data never leaves your AWS environment. As we introduce new capabilities, some future features may expose data only at your explicit request. For the latest information, please refer to the Amazon Bedrock documentation . Web Search operates entirely within Amazon Bedrock’s infrastructure, supporting customers’ compliance requirements.
>
> How it works
>
> When Web Search is enabled in an API call, Bedrock handles the entire search lifecycle server-side. First, the model identifies that a query requires up-to-date web knowledge. Bedrock then formulates a search query, retrieves relevant content from Amazon’s web index and knowledge graph, and injects results – including relevant snippets, source URLs and titles – into the model’s context window. The model reasons over the retrieved content and generates a grounded response with source citations. The API returns the final response with structured citation annotations, including URL and page title for each referenced source. There’s no client-side tool-use loop to build, no external API responses to parse, and no retries or rate limits to manage – a single API call returns a grounded response.
>
> Getting started with the OpenAI Responses API
>
> The Responses API supports built-in tools natively, so Web Search can be called without defining a function schema or building a client-side loop. Enablement takes three steps: configure AWS credentials, point the OpenAI client at the bedrock-mantle endpoint, and add the Web Search tool to the request. At launch, Web Search is available for OpenAI models served through Amazon Bedrock’s next-generation inference engine.
>
> Step 1: Configure authentication and permissions. Web Search uses your existing AWS credentials – there are no separate API keys to provision. The environment must have AWS credentials available through the standard credential chain (an IAM role, the AWS CLI profile, or environment variables), which are used to authenticate requests to the bedrock-mantle endpoint. The calling identity needs two sets of permissions:
>
> Inference permissions on Amazon Bedrock, so the model call itself succeeds. Attach the AmazonBedrockMantleInferenceAccess managed policy, or grant the specific inference actions your call requires.
>
> Web Search tool permissions, so the model can call the tool during the request. At minimum grant bedrock-websearch:InvokeSearch; add bedrock-websearch:InvokeFetch to let the model read a result’s full page content. Live-web retrieval additionally requires bedrock-websearch:ExternalWebAccess, which is the default request behavior — if your identity doesn’t have it, set external_web_access: false on the tool. If InvokeSearch is denied, Web Search is effectively disabled and the model answers from its training data instead.
>
> Requests to the endpoint are authenticated with an AWS-issued bearer token, which you can mint from your existing AWS credentials using the aws-bedrock-token-generator package. This bearer token isn’t a separate API key; it’s a short-lived (up to 12 hours) credential derived from your existing AWS IAM identity via SigV4, packaged in the format the OpenAI client expects for its api_key parameter. No additional key management is required.
>
> Start from a standard call. A normal Responses API call, without grounding, looks like this:
>
> response = client.responses.create(
>
> model="openai.gpt-5.4",
>
> input="What were the key announcements at AWS re:Invent 2025?",
>
> )
>
> Step 2: Enable Web Search. To ground that same call in web knowledge, add a single tools entry:
>
> tools=[{"type": "web_search", "external_web_access": False}]
>
> The optional external_web_access field selects where Web Search retrieves from: Amazon’s pre-indexed web corpus, or live content fetched directly from the web. Today only indexed-web retrieval is served; live-web retrieval will be enabled in a future update, and the parameter is already in the API so your code won’t need to change. The default is true, which requires the bedrock-websearch:ExternalWebAccess permission. The examples below set false, which needs no additional permission.
>
> Step 3: Read the grounded response with citations. Putting it together, here’s the complete end-to-end example, including how to extract the source citations:
>
> from openai import OpenAI
>
> from aws_bedrock_token_generator import provide_token
>
> REGION = "us-east-1"
>
> client = OpenAI(
>
> base_url=f"https://bedrock-mantle.{REGION}.api.aws/openai/v1",
>
> api_key=provide_token(region=REGION),
>
> )
>
> response = client.responses.create(
>
> model="openai.gpt-5.4",
>
> input="What were the key announcements at AWS re:Invent 2025?",
>
> tools=[{"type": "web_search", "external_web_access": False}],
>
> )
>
> searches = [item for item in response.output if item.type == "web_search_call"]
>
> print(f"Retrieval steps: {len(searches)}")
>
> for call in searches:
>
> if call.action.type == "search":
>
> print(f" search: {call.action.queries}")
>
> elif call.action.type == "open_page":
>
> print(f" open_page: {call.action.url}")
>
> for item in response.output:
>
> if item.type == "message":
>
> for content in item.content:
>
> if content.type == "output_text":
>
> print(content.text)
>
> for citation in content.annotations or []:
>
> if citation.type == "url_citation":
>
> print(f" [{citation.title}] {citation.url}")
>
> The above code produces the following output (abridged):
>
> Retrieval steps: 2
>
> search: ['AWS re:Invent 2025 key announcements official AWS blog keynote recap']
>
> open_page: https://aws.amazon.com/blogs/aws/top-announcements-of-aws-reinvent-2025
>
> The biggest AWS re:Invent 2025 announcements clustered around **AI agents, custom
>
> silicon/infrastructure, and developer productivity**. ...
>
> [Top announcements of AWS re:Invent 2025 | AWS News Blog] https://aws.amazon.com/...
>
> [AWS re:Invent 2025: Amazon announces Nova 2, Trainium3, frontier agents] https://...
>
> In this sample, the request includes a Web Search entry in the tools array. Bedrock executes the search server-side and returns the grounded response in a single round-trip – there is no function schema to define and no client-side loop to manage.
>
> Each citation is a url_citation object in the message content’s annotations array. Its wire shape:
>
> {
>
> "type": "url_citation",
>
> "start_index": 120,
>
> "end_index": 303,
>
> "title": "Top announcements of AWS re:Invent 2025 | AWS News Blog",
>
> "url": "https://aws.amazon.com/blogs/aws/top-announcements-of-aws-reinvent-2025"
>
> }
>
> start_index and end_index are character offsets into output_text, letting you render inline footnotes or highlight the exact span each citation supports.
>
> Auditing and observability
>
> Web Search is integrated with AWS CloudTrail out of the box. Every call to bedrock-websearch:InvokeSearch and bedrock-websearch:InvokeFetch is recorded as a management event, capturing the calling identity, timestamp, action, source identity (including any forward-access-session originator), and the account and Region context of the request. Access-denied outcomes are always logged, and each AccessDeniedException event includes the specific condition key that caused the denial — which makes IAM misconfigurations easy to diagnose without turning on additional trails.
>
> By design, CloudTrail does not record the query text, the URLs returned by search, or the raw page content retrieved by fetch. Query text is treated the same way as an inference prompt and is never exposed in trail events. Combined with in-Region processing and zero data egress, this gives security and compliance teams a full audit trail of who used the tool when, without exposing what end users searched for.
>
> Conclusion
>
> Web Search on Amazon Bedrock removes the undifferentiated heavy lifting of connecting foundation models to up-to-date web knowledge. It delivers context-efficient, multi-source grounded results with low-latency, and simple enablement through a single API parameter – so developers can add web grounding without managing vendors, orchestration, or compliance reviews.
>
> Web Search on Bedrock is generally available in US, with in-region query handling in us-east-1, us-east-2 and us-west-2. For pricing details, see the Amazon Bedrock pricing page. To get started, see the Web Search documentation for complete API references and examples.
>
> About the authors
>
> Anuj Jauhari
>
> Anuj is a Senior Product Marketing Manager, Technical at AWS, helping customers realize business outcomes with generative AI.
>
> Vadim Omeltchenko
>
> Vadim is a Senior AI/ML Solutions Architect who is passionate about helping AWS customers innovate in the cloud. His prior IT experience was predominantly on the ground.
>
> Priya Holikatti
>
> Priya is a Senior Technical Product Manager at Amazon AGI, building web search capabilities that connect AI agents and models to real-time, trustworthy web knowledge.
>
> Rashim Gupta
>
> Rashim Gupta is a Senior Manager of Technical Product Management for Amazon Bedrock at AWS, where he leads the team building the features customers use to develop and run production applications on Bedrock.
>
> Omar Abdelwahab
>
> Omar is a Technical Product Marketing Manager at Amazon Web Services (AWS), Where he focuses on AI products including Agentic AI and Web Search. He holds a Ph.D. in Computer Science and enjoys working at the intersection of AI, technology, and go-to-market strategy to help customers build innovative applications.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。