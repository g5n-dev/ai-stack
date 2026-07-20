---
title: "Introducing Grok on Amazon Bedrock"
date: 2026-07-17T04:15:17+08:00
draft: false
entry_kind: "auto"
tags: ["Amazon Bedrock", "Announcements", "Intermediate (200)", "博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:23bb2f584ce8d27db81620b3bf75eb499abea46654f9cca219c6dd439b4e4870"
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 34
description: "当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。"
external_url: https://aws.amazon.com/blogs/machine-learning/introducing-grok-on-amazon-bedrock
observation_id: obs_b81aab955185ba38ce0e119e1a04f211d4b775fea86fdd14cb839b7a61fb51c2
revision_id: rev_a4ab916d7685d2677ddf9c6dd2c5864d3735df525cfebc3f47384e33a2de5ad4
event_id: evt_7e6a88f4b36a3b05565f5724610e17c48a3f867de8e228e7ccf755445f8a4dd4
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-16T20:17:16Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/introducing-grok-on-amazon-bedrock](https://aws.amazon.com/blogs/machine-learning/introducing-grok-on-amazon-bedrock)

## 来源摘要/节选

> This post is co-written with Eric Jiang from xAI (SpaceXAI).
>
> xAI’s Grok 4.3 is now generally available on Amazon Bedrock, giving teams that build agents and AI workflows a model that reasons reliably over long inputs. With this launch, xAI joins Amazon Bedrock as a model provider. Grok 4.3 is a model with configurable reasoning effort. It offers strong tool use and instruction following for building agents, and token efficiency for high-volume inference. It accepts text and image input, and has a 1 million token context window for long documents and multi-turn sessions. The model runs on Mantle, the next-generation inference engine in Amazon Bedrock.
>
> This post covers what makes Grok 4.3 a great fit for agentic and enterprise workloads, how you access it through Amazon Bedrock, and how to use the capabilities most teams reach for first: a basic chat request, configurable reasoning effort, tool calling, structured output, image input, and stateful multi-turn conversations.
>
> Why Grok 4.3 is a great fit for agentic and reasoning workloads
>
> According to xAI, Grok 4.3 is built for enterprise work where accuracy matters. On its own benchmarks at the time of the model launch, xAI reports it outperforms various industry benchmarks. Grok 4.3 ranked #1 on the Artificial Analysis Omniscience benchmark with the lowest hallucination rate among the frontier models it compared. It also placed #1 on the Artificial Analysis Tau2 Telecom benchmark for tool calling in customer support scenarios, and #1 on the Vals AI Case Law and Corporate Finance benchmarks for document understanding. xAI also places the model on the intelligence-versus-cost Pareto frontier, which it describes as 2 to 10 times more intelligence per dollar than other frontier models.
>
> With Grok 4.3, you can control how much the model thinks before answering through an effort level on each request. You configure the effort level (none, low, medium, and high) per request and let one model serve the full range of work. A classification call can run at none effort to keep latency low. A contract analysis or case law task can run at high when depth matters more than response time. Grok 4.3 accepts text and image input and returns text, and its 1 million token context window leaves room for long documents and extended multi-turn sessions. The model handles tool calling and instruction following well, which is what makes it practical for agents that depend on function calls to take action. These traits line up with use cases such as contract review, credit agreement analysis, and financial document question answering. In these cases, the model reasons over long inputs and then calls out to systems of record.
>
> How you access Grok 4.3 on Amazon Bedrock
>
> Grok 4.3 runs on Mantle, and accessing it differs from models that use the Amazon Bedrock Runtime API. Mantle uses OpenAI-compatible APIs. You can invoke Grok 4.3 either with the OpenAI SDK or through direct HTTPS requests to the Chat Completions API or the Responses API.
>
> The Mantle endpoint URL is Region-specific and follows this pattern:
>
> For example, in us-west-2 the base URL is https://bedrock-mantle.us-west-2.api.aws/openai/v1. Note that the Responses API URL route differs slightly on the Mantle endpoint (/openai/v1/) from the Runtime endpoint (/v1/responses).
>
> To set up your SDK with Grok 4.3, set the base URL with the correct Region and path as described in the preceding section.
>
> When using Grok, note that the context window is 1 million tokens and that the defaults depart from the standard OpenAI specification in three places:
>
> temperature defaults to 0.7 rather than 1.
>
> top_p defaults to 0.95 rather than 1.
>
> max_completion_tokens defaults to 131072.
>
> Set these explicitly if your application needs different behavior.
>
> Authenticate and run a first request
>
> You have two ways to authenticate against the Mantle endpoint, and both work with the same OpenAI SDK. For production, we recommend short-term bearer tokens generated from your IAM credentials, because they expire automatically and keep access tied to your IAM identity. Use a long-term Amazon Bedrock API key for quick exploration and getting started. Restrict long-lived keys to that purpose rather than embedding them in production applications.
>
> The following example shows how to authenticate with a long-term Amazon Bedrock API key to access the model. Treat this as an exploration-only credential. You can generate one from the Amazon Bedrock console, and then install the OpenAI SDK:
>
> pip install openai
>
> Point the client at the regional Mantle endpoint and authenticate with your API key. The model ID is xai.grok-4.3:
>
> from openai import OpenAI
>
> client = OpenAI(
>
> api_key="&lt;your Amazon Bedrock API key&gt;",
>
> base_url="https://bedrock-mantle.us-west-2.api.aws/openai/v1",
>
> )
>
> response = client.chat.completions.create(
>
> model="xai.grok-4.3",
>
> messages=[
>
> {"role": "user", "content": "In one sentence, what is Amazon Bedrock?"}
>
> ],
>
> )
>
> print(response.choices[0].message.content)
>
> When you’re ready to incorporate Amazon Bedrock into applications with greater security requirements, we recommend using short-term credentials. You can generate a short-term bearer token from your existing AWS credentials at request time using the Amazon Bedrock token generator. This keeps authentication tied to your IAM identity and avoids a long-lived secret. To get started, install the aws-bedrock-token-generator package.
>
> pip install aws-bedrock-token-generator
>
> Use the provide_token function from the aws_bedrock_token_generator library in code as shown below:
>
> from aws_bedrock_token_generator import provide_token
>
> from openai import OpenAI
>
> client = OpenAI(
>
> api_key=provide_token(region="us-west-2"),
>
> base_url="https://bedrock-mantle.us-west-2.api.aws/openai/v1",
>
> )
>
> Configure reasoning output
>
> You can control how much of reasoning effort the model spends through the reasoning parameter on the Responses API. The effort levels are none (which disables reasoning), low (the default), medium, and high. Higher effort tends to help on multi-step problems where a quick answer would be wrong, at the cost of more output tokens.
>
> The Chat Completions API does not return a reasoning trace. If you want the model’s reasoning available across turns, use the Responses API. In the default stateful pattern, where you set store=True and chain calls with previous_response_id, the service retains each turn’s reasoning and feeds it back automatically, so you do not manage it yourself. Encrypted reasoning is for the stateless case. If you set store=False (for example, when your workload requires that turns are not persisted server-side), request the reasoning with include=["reasoning.encrypted_content"]. Pass it back in your next request’s input to give the model its own prior reasoning as context.
>
> This example runs a classic trick question at high effort:
>
> response = client.responses.create(
>
> model="xai.grok-4.3",
>
> reasoning={"effort": "high"}, # none, low, medium, or high
>
> include=["reasoning.encrypted_content"],
>
> max_output_tokens=4096,
>
> input=(
>
> "A bat and ball cost $1.10. The bat costs $1 more than the ball. "
>
> "How much is the ball? Answer with just the number."
>
> ),
>
> )
>
> print(response.output_text)
>
> print(response.usage.output_tokens_details.reasoning_tokens)
>
> The model worked through the algebra rather than reaching for the intuitive wrong answer of $0.10, and the usage block reports the reasoning tokens it spent internally. Drop the effort to none and that same field reports 0 reasoning tokens, which is the setting to reach for on simple, latency-sensitive calls:
>
> response = client.responses.create(
>
> model="xai.grok-4.3",
>
> reasoning={"effort": "none"},
>
> max_output_tokens=2048,
>
> input="Say OK.",
>
> )
>
> print(response.output_text) # OK.
>
> A practical pattern is to run classification, extraction, and short factual lookups at none or low, and reserve high for planning steps, math, and chains where a single early mistake derails the whole task.
>
> Call tools with Grok 4.3
>
> Tool calling is central to agentic workloads, and Grok 4.3 supports it through the same OpenAI-compatible interface. You describe the tools available, the model decides when to call one, and it returns a structured request that your code executes and feeds back. Grok 4.3 follows the standard OpenAI tool-calling shape, so you define each tool with a JSON Schema for its parameters.
>
> The following example offers a single get_weather tool and asks a question that should trigger it:
>
> tools = [
>
> {
>
> "type": "function",
>
> "function": {
>
> "name": "get_weather",
>
> "description": "Get the current weather for a city",
>
> "parameters": {
>
> "type": "object",
>
> "properties": {"city": {"type": "string"&#125;&#125;,
>
> "required": ["city"],
>
> },
>
> },
>
> }
>
> ]
>
> response = client.chat.completions.create(
>
> model="xai.grok-4.3",
>
> messages=[{"role": "user", "content": "What's the weather in Sydney? Use the tool."}],
>
> tools=tools,
>
> tool_choice="auto", # let the model decide whether to call a tool
>
> )
>
> tool_call = response.choices[0].message.tool_calls[0]
>
> print(tool_call.function.name, tool_call.function.arguments)
>
> # get_weather {"city":"Sydney"}
>
> The model parsed the city out of the question and produced a valid arguments object that matches the schema. From here you run the function in your own code, append a tool role message with the result, and call the model again so it can fold the data into a natural-language reply. This is the building block for multi-step agents on Grok 4.3.
>
> Structured output
>
> When you need the model to return data your code can parse directly, use structured output with a JSON Schema. Grok 4.3 supports the json_schema response format with strict mode, so the response conforms to the schema you provide, rather than giving free-form text.
>
> For example, the following code asks for facts about a country and constrains the shape of the answer:
>
> import json
>
> schema = {
>
> "type": "object",
>
> "properties": {
>
> "name": {"type": "string"},
>
> "capital": {"type": "string"},
>
> "population_millions": {"type": "number"},
>
> },
>
> "required": ["name", "capital", "population_millions"],
>
> "additionalProperties": False,
>
> }
>
> response = client.chat.completions.create(
>
> model="xai.grok-4.3",
>
> messages=[{"role": "user", "content": "Return facts about the country Australia."}],
>
> response_format={
>
> "type": "json_schema",
>
> "json_schema": {"name": "country_facts", "strict": True, "schema": schema},
>
> },
>
> max_completion_tokens=4096,
>
> )
>
> data = json.loads(response.choices[0].message.content)
>
> print(data)
>
> # {'name': 'Australia', 'capital': 'Canberra', 'population_millions': 26.6}
>
> Setting strict to True and additionalProperties to False keeps the response constrained to the keys you asked for, which pairs well with tool calling when a downstream system expects a fixed record format. One operational note from testing: requests occasionally return a 400 from an automated content safety check even on benign input, so build a short retry into production calls.
>
> Image input
>
> Grok 4.3 accepts images as input and returns text, which covers document understanding, chart reading, and visual question answering. You pass an image using the same pattern as the OpenAI Chat Completions API, as a content part with a data: URL holding base64-encoded bytes, or a public image URL. The text and image parts go in the same content array so the model sees the question and the picture together.
>
> import base64
>
> with open("chart.png", "rb") as f:
>
> b64 = base64.b64encode(f.read()).decode()
>
> response = client.chat.completions.create(
>
> model="xai.grok-4.3",
>
> messages=[
>
> {
>
> "role": "user",
>
> "content": [
>
> {"type": "text", "text": "Describe this image in one short sentence."},
>
> {
>
> "type": "image_url",
>
> "image_url": {"url": f"data:image/png;base64,{b64}"},
>
> },
>
> ],
>
> }
>
> ],
>
> max_completion_tokens=4096,
>
> )
>
> print(response.choices[0].message.content)
>
> In testing, the model read a generated test image and named its dominant color correctly. Use a supported image format such as PNG or JPEG and keep the encoding clean: a malformed or truncated image payload returns a validation_error rather than a best-guess answer.
>
> Stateful conversations with the Responses API
>
> The Responses API can hold conversation state on the service side, so you do not need to resend the full message history on every turn. You store a turn by passing store=True, capture the returned response ID, and reference it on the next call with previous_response_id. The model treats the earlier exchange as context.
>
> first = client.responses.create(
>
> model="xai.grok-4.3",
>
> input="Remember the number 42. Just acknowledge.",
>
> store=True,
>
> max_output_tokens=2048,
>
> )
>
> second = client.responses.create(
>
> model="xai.grok-4.3",
>
> previous_response_id=first.id,
>
> input="What number did I ask you to remember?",
>
> max_output_tokens=2048,
>
> )
>
> print(second.output_text) # 42
>
> From the second client.responses.create call in the code example, there is no message being sent except for the previous_response_id. Because the service stores each turn, the model’s prior reasoning is carried forward automatically to the next call, so you keep both the conversation and the model’s thinking in scope without managing that state yourself. One thing to know before you turn this on: storing conversation state means the service retains those turns. Review the Amazon Bedrock data protection documentation for details on the security and privacy of your stored data, and how to disable retention if needed.
>
> Service tiers and Regional availability
>
> Amazon Bedrock offers multiple service tiers so you can match cost and throughput to each workload. Standard tier on-demand inference provides pay-per-token access with no commitment, Priority offers preferential treatment in the processing queue for a higher per-token price, and Flex provides lower-cost access for workloads that are not time-sensitive. You can use Grok 4.3 with the Standard, Priority, and Flex tiers. For details, see service tiers for inference.
>
> Grok 4.3 uses in-Region inference, so you pin your client to a Region where the model is available and set the Mantle base URL to match. Geo and Global cross-Region inference are not offered for this model at launch. The examples in this post use us-west-2. For the current list of supported Regions, see the Regional availability documentation, and for pricing across the tiers, see the Amazon Bedrock pricing page.
>
> Conclusion
>
> Grok 4.3 on Amazon Bedrock gives you a reasoning-first model with configurable effort, native tool calling, strict structured output, image understanding, and server-side conversation state. You can reach the model through the OpenAI SDK pointed at the bedrock-mantle endpoint. The examples in this post do not create billable AWS resources beyond per-request token usage. But if you generated a long-term Amazon Bedrock API key for exploration, delete it from the Amazon Bedrock console when you are done. A long-term key is a standing credential, so removing the ones you no longer need keeps your account’s attack surface small.
>
> To start building, review the Grok 4.3 model card for the current Region list and parameter details, and see the Amazon Bedrock pricing page for token rates. From there, a few directions are worth exploring: wire the tool-calling loop end to end by executing the returned function and feeding the result back, thread encrypted reasoning content across Responses turns to give long-running agents continuity in how they think, and benchmark effort levels against your own workloads to find where higher reasoning stops earning its token cost. Join the discussion in the Amazon Bedrock community on AWS re:Post.
>
> About the authors
>
> Melanie Li
>
> Melanie Li, PhD, is a Senior Generative AI Specialist Solutions Architect at AWS based in Sydney, Australia, where her focus is on working with customers to build solutions using state-of-the-art AI/ML tools. She has been actively involved in multiple generative AI initiatives across APJ, harnessing the power of LLMs. Prior to joining AWS, Dr. Li held data science roles in the financial and retail industries.
>
> Saurabh Trikande
>
> Saurabh is a Senior Product Manager for Amazon Bedrock and Amazon SageMaker Inference. He is passionate about working with customers and partners, motivated by the goal of democratizing AI. He focuses on core challenges related to deploying complex AI applications, inference with multi-tenant models, cost optimizations, and making the deployment of generative AI models more accessible. In his spare time, Saurabh enjoys hiking, learning about innovative technologies, following TechCrunch, and spending time with his family.
>
> Alex Thewsey
>
> Alex is a Generative AI Specialist Solutions Architect at AWS, based in Singapore. Alex helps customers across Southeast Asia to design and implement solutions with ML and Generative AI. He also enjoys karting, working with open source projects, and trying to keep up with new ML research.
>
> Eric Jiang
>
> Eric Jiang is an engineer at SpaceXAI based in Palo Alto. He leads the API and Enterprise post-training teams, and is passionate about building products that delight users. Outside of work, he enjoys running, playing bass guitar, and trying new foods. Thanks again for your great help.
>
> Anirban Gupta
>
> Anirban is a Principal Engineer at AWS based in Seattle, USA, where he focuses on the design of secure, high-scale model-serving infrastructure for Amazon Bedrock. He has driven the technical work behind several foundation-model launches on the platform. Prior to joining Amazon Bedrock, he was a Principal Engineer on AWS Outposts, building hybrid on-premises cloud infrastructure.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。