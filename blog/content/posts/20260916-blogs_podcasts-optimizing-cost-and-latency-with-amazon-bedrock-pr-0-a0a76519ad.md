---
title: "Optimizing cost and latency with Amazon Bedrock prompt caching"
date: 2026-09-16T02:14:39+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "RAG", "Prompt 工程", "Advanced (300)", "Amazon Bedrock", "Technical How-to", "博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:558f728ec6a4fc4dcc67c0799e2073513bdf14ac20dd6d21c8f860d32541fb4c"
source_payload_sha256: "sha256:77382bd45cfc6926427724f54e1fcf7855039af931314533f994e01a78c705b1"
observation_id: obs_a0a76519ad261018b2db18c7cceaf8b2e3bc4dadb0298f00013751155608c146
event_id: evt_fcd5cc4a816b3aeac9fa727e79201946a0e837cdd73374587a6668fef5d7fc68
revision_id: rev_514e32dfe613102436666402b488e860b5542ffa77fd9060b054a7675cb7a764
source_published_at: 2026-09-15T16:18:19Z
first_seen_at: 2026-09-15T18:25:44Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: true
source_truncation_reason: "crawler_feed_content_limit"
source_support: 1.0
source_title_chars_original: 62
interpretation_sha256: "sha256:b1282d48e2930bb05f2c9ec94e87ef6bff1032f2b29f98506a223d9a7f8bf8b0"
description: "这篇内容介绍了一种在Amazon Bedrock中实现的缓存机制，通过在后续请求中复用已处理过的输入内容来降低 token 处理成本和首 token 响应时间。内容涵盖了六种实际应用场景和相关的定价说明。"
external_url: https://aws.amazon.com/blogs/machine-learning/optimizing-cost-and-latency-with-amazon-bedrock-prompt-caching
parent_observation_id: null
last_seen_at: 2026-09-15T18:12:41.948607Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/optimizing-cost-and-latency-with-amazon-bedrock-prompt-caching](https://aws.amazon.com/blogs/machine-learning/optimizing-cost-and-latency-with-amazon-bedrock-prompt-caching)
- **发布域名**: aws.amazon.com

## 要点解读

### 这是什么
这篇内容介绍了一种在Amazon Bedrock中实现的缓存机制，通过在后续请求中复用已处理过的输入内容来降低 token 处理成本和首 token 响应时间。内容涵盖了六种实际应用场景和相关的定价说明。

### 用在哪里
适合在需要反复向模型发送相同上下文但配合不同问题的应用中使用。例如对同一份长文档进行多轮问答，或在 agent 工作流中重复引用相同的工具定义。面向需要在 AWS 环境中优化模型调用成本的开发者或架构师。

### 可以推断的
推测：在大型文档分析或多轮对话场景中，缓存机制能够显著降低单位请求成本，适合成本敏感的长期运行应用。
推测：该功能依赖特定的 token 阈值和存活时间设置，实际收益与业务请求模式密切相关，开发者需要评估缓存命中率以判断投入产出比。

## 来源摘要/节选

> Prompt caching in Amazon Bedrock can reduce your input token costs by up to 90 percent when you repeatedly send the same context to foundation models, based on Amazon Bedrock prompt caching pricing. Without caching, a 10,000-token contract sent alongside 50 user questions means 500,000 input tokens billed at full price for content the model has already processed.
>
> You can mitigate this issue by shortening prompts, reducing context windows, or implementing application-level caching. Each option involves a trade-off:
>
> Shortened prompts reduce token count but might also reduce context quality.
>
> Smaller context windows lower cost at the expense of the model’s ability to reason over complete information.
>
> Response caching handles identical queries well, yet provides no benefit when the same context is paired with different questions.
>
> Prompt caching in Amazon Bedrock helps reduce this challenge at the infrastructure level. When you cache parts of your conversation context (system prompts, documents, tool definitions), Amazon Bedrock reads the cached tokens on subsequent requests instead of reprocessing them. This can reduce time-to-first-token (TTFT) and lower costs for cached input tokens by up to 90 percent on cache hits, without changing your model or prompt quality.
>
> This post walks through six practical prompt caching scenarios using the Converse API in Amazon Bedrock, progressing from basic to advanced patterns:
>
> Message content caching: Cache long documents for multi-question analysis.
>
> System prompt caching: Cache persona definitions and instructions across conversations.
>
> Tool definition caching: Cache tool schemas for agentic workflows.
>
> Mixed TTL caching: Assign different cache lifetimes to different content tiers.
>
> Tenant isolation: Implement per-tenant cache separation in multi-tenant applications.
>
> LangChain integration: Use prompt caching with the LangChain framework.
>
> How prompt caching works
>
> Prompt caching stores a snapshot of partially processed input so that subsequent requests with the same prefix skip redundant computation. This section covers the request flow, supported models, and pricing.
>
> When you include a cachePoint marker in your request, Amazon Bedrock evaluates whether the content preceding that marker matches an existing cache entry. If it does (a cache hit), the model can skip reprocessing those tokens and begin generation from the cached state. If no match exists (a cache miss), the model processes the full content and writes the result to cache for potential future requests.
>
> This diagram shows the flow:
>
> Figure 1: Prompt caching request flow, where the first request writes to cache and the second request reads from cache, reducing TTFT and input token cost
>
> With this flow in mind, four key concepts determine how caching behaves in practice:
>
> Cache scope: Cache entries are scoped to individual AWS accounts and AWS Regions.
>
> Token thresholds: Each cache checkpoint must meet a minimum token threshold to activate. For example, Anthropic Claude Sonnet 4.5 and Sonnet 4.6 require at least 1,024 tokens per checkpoint, while Opus models require at least 4,096.
>
> Time-to-live (TTL): Cache entries expire based on the TTL specified in the request. The default is 5 minutes, with select models supporting up to 1 hour.
>
> Model-agnostic syntax: The Converse API cachePoint syntax is identical across supported model families, including Anthropic Claude and Amazon Nova.
>
> For the latest model support information, see the Amazon Bedrock Prompt Caching documentation.
>
> Pricing
>
> Prompt caching introduces two token categories in addition to standard input and output tokens:
>
> Token Type
>
> Description
>
> Cost vs Standard Input
>
> cacheWriteInputTokens
>
> Tokens written to cache (first request)
>
> 25% higher than standard input
>
> cacheReadInputTokens
>
> Tokens read from cache (subsequent requests)
>
> 90% lower than standard input
>
> cacheWriteInputTokens (1-hour TTL)
>
> Tokens written to cache with 1-hour TTL
>
> 100% higher than standard input (2x)
>
> For workloads with repeated context, the savings reach approximately 75 percent on input token costs. For example, if you send a 10,000-token document with 10 different questions, the first request incurs a cache write cost. The remaining nine requests each read from cache at 90 percent reduced cost, resulting in a net savings of approximately 75 percent on input token costs for that document context. This assumes all subsequent requests occur within the TTL window. Requests after expiration trigger a new cache write, reducing the net savings. See Amazon Bedrock pricing for detailed pricing information.
>
> Prerequisites
>
> Before getting started with the scenarios, make sure you have the following:
>
> An AWS account with Amazon Bedrock access in a supported AWS Region (such as us-west-2).
>
> Model access enabled for the target model. The examples in this post use Anthropic Claude Sonnet 4.5 (global.anthropic.claude-sonnet-4-5-20250929-v1:0). See Manage model access for instructions. For the latest model and Region availability, see Supported models by AWS Region in Amazon Bedrock. This is a cross-Region inference profile. Requests automatically route across Regions, which can occasionally increase cache write frequency.
>
> Python 3.10 or later with the following dependencies installed:
>
> pip install boto3&gt;=1.43.0 langchain-aws&gt;=0.2.12 matplotlib pandas
>
> Note: Boto3 1.43.0 or later is required for the ttl parameter in cachePoint used in Scenario 4 (Mixed TTL).
>
> AWS credentials configured through the default profile or environment variables. See Configure the AWS Command Line Interface (AWS CLI) for setup instructions.
>
> Scenario 1: Message content caching
>
> A common use case for prompt caching is caching long documents or reference content that you query repeatedly. For example, in a Retrieval Augmented Generation (RAG) application, you ask multiple questions about the same document, or a coding assistant references a large codebase.
>
> In this scenario, you place a cachePoint marker between the static document and the dynamic question. Amazon Bedrock caches the document on the first call and might reuse it on subsequent calls.
>
> How message content caching works
>
> Place a cachePoint content block after the static content and before the dynamic question. Amazon Bedrock caches everything before the checkpoint and reuses it on subsequent requests:
>
> content = [
>
> {"text": "&lt;static document content&gt;"},
>
> {"cachePoint": {"type": "default"&#125;&#125;, # cache everything above
>
> {"text": "&lt;user question&gt;"} # dynamic, changes per request
>
> ]
>
> The following code puts this pattern into practice with a complete working example.
>
> Implementation
>
> First, set up the Amazon Bedrock runtime client and define a sample document. In a production application, this document can be a PDF, a knowledge base article, or other content exceeding the 1,024-token threshold:
>
> import boto3
>
> import json
>
> import time
>
> MODEL_ID = "global.anthropic.claude-sonnet-4-5-20250929-v1:0" # Minimum token requirement to activate cache: 1,024 tokens
>
> AWS_REGION = "us-west-2"
>
> bedrock = boto3.client("bedrock-runtime", region_name=AWS_REGION)
>
> # Document LARGE enough (&gt;1024 tokens required for Claude Sonnet 4.5)
>
> DOCUMENT = """
>
> The universe is a vast and mysterious expanse that has captivated human imagination for millennia. From the earliest civilizations who looked up at the night sky and wondered about the nature of the stars, to modern astronomers using sophisticated telescopes and spacecraft to explore distant galaxies, our quest to understand the cosmos continues unabated. This comprehensive overview covers the major components of our universe, from the smallest asteroids to the largest galaxy clusters.
>
> Our solar system, located in the Milky Way galaxy, is home to eight planets, numerous dwarf planets, and countless smaller objects including asteroids, comets, and meteoroids. The Sun, a middle-aged G-type main-sequence star, provides the energy that sustains life on Earth and influences the dynamics of all objects within its gravitational reach.
>
> Mercury, the innermost planet, experiences extreme temperature variations due to its proximity to the Sun and lack of substantial atmosphere. Venus, often called Earth's twin due to its similar size, has a thick atmosphere composed primarily of carbon dioxide, creating a runaway greenhouse effect that makes it the hottest planet in our solar system. Earth, our home, is the only known planet to harbor life, with its unique combination of liquid water, moderate temperatures, and protective magnetic field.
>
> Mars, the Red Planet, has long been a subject of fascination and speculation about the possibility of extraterrestrial life. Its rusty appearance comes from iron oxide prevalent on its surface. The planet features the largest volcano in the solar system, Olympus Mons, and a canyon system, Valles Marineris, that dwarfs the Grand Canyon. Recent Mars missions have discovered evidence of ancient river systems and the presence of water ice beneath the surface.
>
> The asteroid belt, located between Mars and Jupiter, contains millions of rocky objects ranging from small boulders to the dwarf planet Ceres. These remnants from the early solar system provide valuable insights into planetary formation and the conditions that existed billions of years ago. Scientists study these asteroids to understand the building blocks of planets and the early solar system's chemical composition. Some asteroids contain valuable metals and minerals that may one day be mined for space-based industries.
>
> The terrestrial planets share common characteristics: rocky compositions, relatively small sizes compared to gas giants, and solid surfaces. Mercury's heavily cratered surface resembles our Moon, preserving a record of impacts from the early solar system. Venus's dense atmosphere traps heat so effectively that its surface temperature exceeds that of Mercury, despite being farther from the Sun. Earth's plate tectonics continuously reshape its surface, while Mars shows evidence of past geological activity including ancient volcanoes and water-carved channels.
>
> Jupiter, the largest planet, is a gas giant composed primarily of hydrogen and helium. Its Great Red Spot, a persistent anticyclonic storm, has been observed for over 400 years. Jupiter's intense magnetic field and numerous moons, including the four Galilean satellites discovered by Galileo Galilei in 1610, make it a miniature solar system in its own right. Europa, one of these moons, is believed to have a subsurface ocean that could potentially harbor life.
>
> Saturn, famous for its spectacular ring system, is another gas giant with dozens of moons. Titan, its largest moon, has a thick atmosphere and liquid hydrocarbon lakes, making it one of the most intriguing bodies in the solar system for astrobiological research. The Cassini-Huygens mission provided unprecedented details about Saturn and its moons during its 13-year exploration.
>
> Uranus and Neptune, the ice giants, reside in the outer reaches of our solar system. Uranus rotates on its side, likely due to a massive impact early in its history. Neptune, the windiest planet, features storms with wind speeds exceeding 2,000 kilometers per hour. Both planets have ring systems, though less prominent than Saturn's.
>
> Beyond Neptune lies the Kuiper Belt, a region populated by icy bodies including the dwarf planet Pluto. The New Horizons mission's flyby of Pluto in 2015 revealed a geologically active world with nitrogen glaciers and a hazy atmosphere. Even further out is the Oort Cloud, a hypothetical spherical shell of icy objects that may extend halfway to the nearest star.
>
> The outer solar system remains largely unexplored compared to the inner planets. Only Voyager 2 has visited both Uranus and Neptune, conducting brief flybys in the 1980s. Future missions are being planned to study these ice giants in more detail, potentially including orbiters and atmospheric probes. The moons of the outer planets present exciting targets for astrobiology, with Europa, Enceladus, and Titan all showing signs of environments that could support life.
>
> Gas giants and ice giants differ fundamentally in composition. While Jupiter and Saturn are primarily hydrogen and helium, Uranus and Neptune contain significant amounts of water, ammonia, and methane ices. This distinction gives the ice giants their characteristic blue-green colors and different internal structures compared to their larger neighbors.
>
> Exoplanet research has revolutionized our understanding of planetary systems. The Kepler space telescope discovered thousands of planets orbiting other stars, revealing that planets are common throughout our galaxy. Some of these exoplanets reside in the habitable zone of their stars, where liquid water could exist on the surface.
>
> The search for extraterrestrial intelligence, known as SETI, uses radio telescopes to listen for signals from advanced civilizations. While no definitive signals have been detected, the Drake Equation provides a framework for estimating the number of communicating civilizations in our galaxy.
>
> Black holes, regions of spacetime where gravity is so strong that nothing can escape, represent some of the most extreme objects in the universe. Stellar black holes form from the collapse of massive stars, while supermassive black holes, containing millions to billions of solar masses, reside at the centers of most galaxies including our own.
>
> The James Webb Space Telescope, launched in 2021, observes in infrared to study the earliest galaxies and probe planetary atmospheres for signs of life. Understanding the universe requires collaboration across disciplines including physics, chemistry, biology, and engineering.
>
> Stellar evolution describes how stars change over their lifetimes. Stars form in molecular clouds when gravity causes dense regions to collapse. Nuclear fusion in the core converts hydrogen to helium, releasing enormous amounts of energy. When stars exhaust their nuclear fuel, their fate depends on their mass: smaller stars become white dwarfs, medium stars may become neutron stars, and the most massive stars explode as supernovae, potentially leaving behind black holes.
>
> Galaxies, containing billions of stars, come in various shapes including spiral, elliptical, and irregular. The Milky Way is a barred spiral galaxy approximately 100,000 light-years in diameter. Galaxies often cluster together, forming groups and superclusters connected by cosmic filaments of dark matter and gas. The observable universe contains approximately two trillion galaxies, each harboring hundreds of billions of stars.
>
> The cosmic microwave background radiation, discovered in 1965, provides a snapshot of the universe approximately 380,000 years after the Big Bang. Detailed measurements of this radiation have confirmed the Big Bang theory and revealed information about the early universe's composition and geometry. Dark matter and dark energy together comprise about 95% of the universe's total mass-energy content.
>
> Space exploration has achieved remarkable milestones since the launch of Sputnik in 1957. Human spaceflight began with Yuri Gagarin's orbit in 1961 and culminated in the Apollo Moon landings. The International Space Station has hosted continuous human presence in space since 2000. Future missions aim to return humans to the Moon through the Artemis program and eventually send astronauts to Mars. Private space companies have transformed the industry, developing reusable rockets that have dramatically reduced launch costs.
>
> The study of astrobiology examines the origin, evolution, and distribution of life in the universe. Scientists search for biosignatures in planetary atmospheres and analyze extremophiles on Earth to understand the limits of life. The discovery of organic molecules on Mars and in the plumes of Enceladus fuels speculation about the possibility of life elsewhere in our solar system. Modern telescopes have detected exoplanets using multiple methods including transit photometry, radial velocity measurements, and direct imaging.
>
> Gravitational wave astronomy represents one of the newest frontiers in space science. The LIGO and Virgo detectors have observed mergers of black holes and neutron stars, confirming predictions from Einstein's general theory of relativity. These observations have opened an entirely new window on the universe, allowing scientists to study phenomena that are invisible to traditional electromagnetic telescopes. The future space-based LISA mission promises to detect gravitational waves from even more exotic sources, including the mergers of supermassive black holes at the centers of galaxies.
>
> """
>
> Next, define the caching function. The key elements are the cachePoint block placed between the static document and the dynamic question:
>
> def converse_with_cache(document, question):
>
> """Query a document with prompt caching enabled."""
>
> content = [
>
> {"text": document},
>
> {"cachePoint": {"type": "default"&#125;&#125;,
>
> {"text": question}
>
> ]
>
> response = bedrock.converse(
>
> modelId=MODEL_ID,
>
> messages=[{"role": "user", "content": content}],
>
> inferenceConfig={"maxTokens": 512}
>
> )
>
> return response["usage"]
>
> Run two requests to observe the caching behavior. The initial call populates the cache, and a subsequent call with a different question reuses it:
>
> # Request 1: cache write (first time seeing this content)
>
> usage1 = converse_with_cache(DOCUMENT, "What are the key points?")
>
> print("Request 1 (cache write expected):")
>
> print(json.dumps(usage1, indent=2))
>
> time.sleep(1)
>
> # Request 2: cache read (same document, different question)
>
> usage2 = converse_with_cache(DOCUMENT, "Summarize the conclusions.")
>
> print("\nRequest 2 (cache read expected):")
>
> print(json.dumps(usage2, indent=2))
>
> Reading cache metrics
>
> The response usage object includes two cache-specific fields:
>
> Field
>
> Description
>
> cacheWriteInputTokens
>
> Tokens written to cache (appears on first request)
>
> cacheReadInputTokens
>
> Tokens read from cache (appears on subsequent requests)
>
> In our testing with Anthropic Claude Sonnet 4.5 and a document exceeding 1,024 tokens, the initial response shows a cache write:
>
> {
>
> "inputTokens": 28,
>
> "outputTokens": 253,
>
> "cacheWriteInputTokens": 1898,
>
> "cacheReadInputTokens": 0
>
> }
>
> A subsequent request with the same document prefix produces a cache read:
>
> {
>
> "inputTokens": 28,
>
> "outputTokens": 294,
>
> "cacheWriteInputTokens": 0,
>
> "cacheReadInputTokens": 1898
>
> }
>
> Notice that cacheReadInputTokens now reflects the 1,898 tokens read from cache. The entire document prefix was reused without reprocessing. Only 28 tokens (the question itself) were processed as standard input. These cached tokens are billed at the reduced cache-read rate (90 percent lower than standard input).
>
> Simplified cache management
>
> Claude models on Amazon Bedrock support simplified cache management. You can place a single cachePoint, and Amazon Bedrock automatically checks for cache hits on prefixes up to approximately 20 content blocks before that marker. You do not need to manually place multiple cache checkpoints to get cache hits on earlier portions of your conversation.
>
> For more granular control, you can place multiple cachePoint markers after each section of content:
>
> content = [
>
> {"text": SECTION_1},
>
> {"cachePoint": {"type": "default"&#125;&#125;,
>
> {"text": SECTION_2},
>
> {"cachePoint": {"type": "default"&#125;&#125;,
>
> {"text": SECTION_3},
>
> {"cachePoint": {"type": "default"&#125;&#125;,
>
> {"text": QUESTION}
>
> ]
>
> This approach supports partial cache hits. If only the first two sections match a previous request, the model reuses the cache for those sections and processes the remaining content.
>
> Streaming variant
>
> The same caching syntax works with converse_stream. The key difference is that cache metrics arrive in the metadata event at the end of the stream rather than in the immediate response:
>
> def converse_stream_with_cache(document, question):
>
> content = [
>
> {"text": document},
>
> {"cachePoint": {"type": "default"&#125;&#125;,
>
> {"text": question}
>
> ]
>
> response = bedrock.converse_stream(
>
> modelId=MODEL_ID,
>
> messages=[{"role": "user", "content": content}],
>
> inferenceConfig={"maxTokens": 512}
>
> )
>
> text = ""
>
> usage = {}
>
> for event in response["stream"]:
>
> if "contentBlockDelta" in event:
>
> text += event["contentBlockDelta"]["delta"].get("text", "")
>
> elif "metadata" in event:
>
> usage = event["metadata"].get("usage", {})
>
> return usage, text
>
> TTFT benchmark
>
> To quantify the latency improvement, you can measure TTFT with and without caching:
>
> def measure_ttft(document, question, use_cache=True, iterations=5):
>
> """Measure TTFT using ConverseStream."""
>
> ttfts = []
>
> for i in range(iterations):
>
> if use_cache:
>
> content = [
>
> {"text": document},
>
> {"cachePoint": {"type": "default"&#125;&#125;,
>
> {"text": question}
>
> ]
>
> else:
>
> content = [{"text": document + "\n\n" + question}]
>
> start = time.time()
>
> response = bedrock.converse_stream(
>
> modelId=MODEL_ID,
>
> messages=[{"role": "user", "content": content}],
>
> inferenceConfig={"maxTokens": 512}
>
> )
>
> for event in response["stream"]:
>
> if "contentBlockDelta" in event:
>
> ttft = time.time() - start
>
> ttfts.append(ttft)
>
> for _ in response["stream"]:
>
> pass
>
> break
>
> time.sleep(0.5)
>
> return ttfts
>
> Prompt caching can reduce TTFT, with the benefit growing as the cached prefix size increases. For smaller documents (approximately 2,000–5,000 tokens), the improvement may not be statistically significant across a small number of iterations. The exact improvement varies based on document size, model, and current load. For large cached prefixes (over 10,000 tokens), the reduction in TTFT becomes more pronounced.
>
> Scenario 2: System prompt caching
>
> Many applications use detailed system prompts that define the model’s persona, guidelines, and domain expertise. These system prompts can span thousands of tokens and remain constant across user interactions. With system prompt caching, you pay the full processing cost once and reuse the cached system prompt for every subsequent message.
>
> The cache point goes inside the system parameter, separate from user messages.
>
> Configuration
>
> The Converse API system parameter accepts an array of content blocks. Place a cachePoint after the system text:
>
> system = [
>
> {"text": "&lt;detailed system prompt&gt;"},
>
> {"cachePoint": {"type": "default"&#125;&#125;
>
> ]
>
> The next example shows this in a full request with a detailed persona prompt.
>
> Implementation
>
> The following example defines a comprehensive system prompt: an Expert Space Science Advisor persona with detailed response guidelines. The prompt exceeds the 2,048-token threshold required for caching:
>
> SYSTEM_PROMPT = """You are an Expert Space Science Advisor, a highly knowledgeable
>
> AI assistant specializing in astronomy, astrophysics, planetary science, and space
>
> exploration. Your role is to provide accurate, comprehensive, and engaging information
>
> about many aspects of space science.
>
> ## Core Expertise Areas
>
> ### Planetary Science
>
> You possess deep knowledge of planetary formation, composition, atmospheres, and
>
> geology across our solar system and beyond. This includes understanding the inner
>
> rocky planets (Mercury, Venus, Earth, and Mars), gas giants (Jupiter and Saturn),
>
> ice giants (Uranus and Neptune), dwarf planets such as Pluto and Ceres, and the
>
> countless smaller bodies that inhabit our solar system.
>
> You understand the processes that shape planetary worlds: volcanism, tectonics,
>
> atmospheric erosion, meteorite impacts, cryovolcanism, and planetary differentiation.
>
> You can explain how planetary magnetic fields arise and protect atmospheres, how
>
> seasons change on different worlds, and how water and other volatiles behave under
>
> varying planetary conditions.
>
> Your expertise extends to moons and satellite systems. You know the fascinating
>
> moons of the solar system: Jupiter's volcanic Io, Europa with its subsurface ocean,
>
> Saturn's Titan with its methane lakes, Enceladus with its water geysers, Neptune's
>
> Triton with its frozen nitrogen, and our own Moon with its unique formation history.
>
> You understand how tidal forces shape these worlds and how they may harbor habitable
>
> environments.
>
> ### Astrophysics and Cosmology
>
> Your expertise extends to the fundamental physics governing the universe. You
>
> understand stellar evolution from star-forming nebulae to supernovae and black holes.
>
> You can explain the life cycle of stars, from long-lived red dwarfs to short-lived
>
> blue giants, and how stellar mass determines a star's fate.
>
> You comprehend the structure and evolution of galaxies, including our Milky Way.
>
> You know the different types of

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。