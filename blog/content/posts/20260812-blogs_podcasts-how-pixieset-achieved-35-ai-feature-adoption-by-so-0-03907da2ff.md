---
title: "How Pixieset achieved 35% AI feature adoption by solving the right problem with Amazon Bedrock"
date: 2026-08-12T00:15:31+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "生成式 AI", "Prompt 工程", "Amazon Bedrock", "Customer Solutions", "博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:5cfb458e63d97e8a1b682de056480fcc4758b88f8df59135307d52f6692541c9"
source_payload_sha256: "sha256:1e10deaab53346ce6f0225573cb2d601ee37a3f8e533b35aa2b5cc00c5b64a96"
observation_id: obs_03907da2ffad6deeb69b2a444e4252adcd3d23c494143b585b837a6453db694e
event_id: evt_3fe2c95359d0250015e6621184b6185551808d0a24da5173b8ec1a9516bca15e
revision_id: rev_c6f5040edcb8a27170d9c5994dda8f2d8a17853aa8dedd8496159faf8cc03e90
source_published_at: 2026-08-11T16:11:15Z
first_seen_at: 2026-08-11T16:25:53Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 94
description: "当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。"
external_url: https://aws.amazon.com/blogs/machine-learning/how-pixieset-achieved-35-ai-feature-adoption-by-solving-the-right-problem-with-amazon-bedrock
parent_observation_id: null
last_seen_at: 2026-08-13T00:00:00Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/how-pixieset-achieved-35-ai-feature-adoption-by-solving-the-right-problem-with-amazon-bedrock](https://aws.amazon.com/blogs/machine-learning/how-pixieset-achieved-35-ai-feature-adoption-by-solving-the-right-problem-with-amazon-bedrock)
- **发布域名**: aws.amazon.com

## 来源摘要/节选

> This post is co-written with Ry Rainey and Graham Gibson from Pixieset.
>
> Photographers and artists are among the most skeptical audiences for generative AI. They have watched it threaten their craft and flood their industry with synthetic work. A 2025 MIT study found 95% of enterprise Generative AI pilots deliver zero measurable returns.
>
> Pixieset is an all-in-one photography business service providing photo galleries, websites, stores, studio management, and photo editing. Pixieset hosts over 8 billion photos and is trusted by millions of photographers worldwide. They cut through that skepticism by asking the right question: what tasks are our users forced to do that pull them away from their craft? The answer took them from concept to production in four months, drove significant subscription upgrades in week one, and has 35 percent of their applicable user base still using the feature sixteen months later.
>
> Each year, Pixieset runs a company-wide hackathon where teams experiment with new technology and explore what’s possible. It was through the hackathon that the team first saw what generative AI could do. When it came to product development, they brought that curiosity back to the customer problem.
>
> Pixieset Websites makes it straightforward for photographers to create a website for their business. The data showed that most photographer websites had little to no alt text. Alt text is a unique and accurate description for each image on a page. Without alt text, images are invisible to search engines. A typical photographer’s portfolio contains hundreds to thousands of images. Writing a unique and descriptive alt text for each image is tedious and time-consuming. Photographers know they should have alt text to get their business promoted, but the sheer volume of manual alt text entries makes it a task they perpetually defer.
>
> Using Amazon Bedrock, Pixieset moved from concept to production launch of an AI image alt text generator to millions of users in 4 months. Graham Gibson, Staff Product Manager at Pixieset recalls, “In the first week alone, Pixieset generated alt text for over 750,000 photos, proving that this was a part of the workflow that photographers were happy to hand over to AI.”
>
> The challenge
>
> The challenge isn’t building the feature but driving its adoption. A tool has no value if users don’t trust it, or worse it alienates the creative professionals it’s designed to serve.
>
> “We talked a lot about how this first AI feature must solve a real problem,” says Ry Rainey, Staff Engineer at Pixieset. Pixieset’s product philosophy has always been to identify moments where photographers spend time on work that isn’t photography and then alleviate that friction. The team applied this same lens to generative AI by not asking “what can this technology do?” but “where are our users losing time to tasks that are not creative?” That framing led the Pixieset team past flashier applications like AI-generated images, which would have encroached on the creative work photographers take pride in. They instead looked toward metadata, the invisible scaffolding that makes a portfolio visible to technologies and search engines but that no photographer enjoys writing.
>
> Figure 1: The AI-generated alt text review interface in the Pixieset website builder
>
> Rather than applying AI-generated alt-text across an entire website at once, the feature is available one image at a time. A photographer reviews a single suggested alt text, choosing to accept, edit, or reject it before expanding the scope. The photographer builds confidence in the output quality at their own pace. When the photographer is comfortable, they enable “auto-apply” across their portfolio, and even then, every caption remains editable. The photographer retains final say, and the AI earns trust incrementally.
>
> Solution overview
>
> The following diagram shows the end-to-end flow for Pixieset’s AI-generated alt text feature. Pixieset is built on event-driven architecture using Amazon Elastic Compute Cloud (Amazon EC2), AWS Lambda, and Amazon Simple Queue Service (Amazon SQS).
>
> Figure 2: End-to-end flow for Pixieset’s AI-generated alt text feature
>
> When a photographer uploads an image, an event is triggered. For this AI-generated alt text feature, the Pixieset team added one more step to that existing worker pipeline by sending the image to Amazon Bedrock for inference by a multimodal large language model (LLM), storing the generated caption alongside the photo, and surfacing it for review within the website builder photographers already use daily.
>
> This integration required only a single API call without new infrastructure, GPU provisioning, or model hosting. “This is one of the primary reasons we chose Amazon Bedrock,” says Graham. By using the fully managed Amazon Bedrock with secure access to leading foundation models through a single API, Pixieset scaled from zero to 750,000 inference requests in the first week without provisioning a single server.
>
> The Pixieset team needed the feature to be highly available because if a user sees empty generative AI captions or “please try again” errors, it erodes trust and hinders the adoption of the feature. Cross-Region inference in Amazon Bedrock automatically routes requests across Regions within a defined geographic boundary, maintaining throughput without requiring Pixieset to build routing logic. The Pixieset team took it one step further by catching failures from the first model and retrying with a secondary model of similar quality. As a result, this feature has had zero downtime since launch.
>
> Pixieset launched the feature at the beginning of 2025 using Anthropic Claude 3.5 Sonnet through Amazon Bedrock, selecting it for its multimodal image understanding, fast inference, and cost efficiency at scale. Because Amazon Bedrock presents a unified API across model providers, Pixieset evaluated newer models without locking into a particular version or provider and swap them without re-architecting the integration. The advanced prompt optimization in Amazon Bedrock further lowers the switching cost by adapting existing prompts to a new model’s strengths automatically. Since launch, the Amazon Bedrock model catalog has continued to expand, including the latest Claude Sonnet 5 as of June 2026. It also includes OpenAI’s GPT-5.5, Amazon Nova, and models from Meta, Mistral, Cohere and many more. This means the feature they shipped in 2025 continues to improve as the underlying models do, with minimal engineering investment.
>
> Response
>
> Upon launching the feature, the response from photographers confirmed they had asked the right question and built something truly useful:
>
> “OMG Pixieset! Okay, I don’t normally like the use of AI, but using AI to mass-generate image descriptions is absolutely fantastic. Obviously I’m checking through to approve them, but this is a game-changer!”
>
> “This new ’SEO for images’ generative AI alt-text for all pictures on website is great!! Saves me so much time. Very few minor tweaks needed here and there but overall accurate. Excellent feature Pixieset!”
>
> “I updated my subscription to benefit from this innovation thank you for your work”
>
> Three principles builders can apply
>
> Pixieset’s success with AI-generated alt text wasn’t a matter of luck or timing. Three design decisions, made before a line of code was written, shaped the outcome.
>
> Categorize your AI features into moats and must-haves
>
> Not every AI feature deserves the same level of investment. Pixieset recognized early that AI-generated alt text is a must-have, not a proprietary moat that deepens over time with unique data. It’s a table-stakes capability that most website builders will eventually offer. That distinction told the team to prioritize speed to market instead of over-engineering. That focus is how they moved from concept to production in four months rather than spending a year building differentiation that wouldn’t compound.
>
> Solve work that isn’t their craft
>
> The most adoption-resistant AI features are the ones that encroach on work users take pride in. Pixieset deliberately chose to automate metadata, the invisible scaffolding that makes a portfolio discoverable, rather than anything that touches the creative act of photography itself. The result was that photographers didn’t feel replaced but relieved of a chore they’d been neglecting, which is why the feature drives subscription upgrades rather than cancellations.
>
> Let users build trust at their own pace
>
> Even a well-targeted feature can fail if it asks users to hand over too much control at once. Pixieset introduced the AI one image at a time, letting photographers review a single caption before deciding whether to expand scope to their full portfolio. That patience paid off, and 35 percent of users eventually chose full automation on their own terms. They arrived at that confidence through direct product experience rather than a product team’s assurance.
>
> Conclusion
>
> The most striking thing about Pixieset’s AI-generated alt text feature is how little infrastructure it required. A single Amazon Bedrock inference call, embedded into an existing event-driven pipeline, delivered a feature with 35 percent user adoption that shows no signs of plateauing. But the technical simplicity is the lesser lesson. What made it succeed was the discipline of knowing which problem to solve, whose work to automate, and how much control to hand over at once.
>
> Get started with Amazon Bedrock to build your first inference-powered feature. When you’re ready to move into multi-step agentic workflows, Amazon Bedrock AgentCore provides the managed infrastructure to scale from there. If you’re building with AI from the start, the AI-Driven Development Lifecycle (AI-DLC) offers a framework for using AI as a collaborator across every phase of software development.
>
> About the authors
>
> Kinman Lam
>
> Kinman is an ISV Senior Solutions Architect at AWS, where he advises software companies executives on bringing GenAI from prototype to production. He hosts a monthly Agentic AI webinar series on building production-ready AI agents with AWS. Follow his latest work on LinkedIn at linkedin.com/in/kinmanlam
>
> Rob Yang
>
> Rob is a Senior Technical Account Manager Lead at Amazon Web Services based in Calgary, Canada. He specializes in cloud financial management and helps customers mature their financial operations on AWS. Outside of work, he enjoys planning and optimizing travel experiences for his family and friends.
>
> Graham Gibson
>
> Graham is a Staff Product Manager at Pixieset with 8 years of experience building products for photographers. He specializes in creating simple, thoughtfully designed solutions that streamline photographers’ workflows and help them spend more time doing the work they love.
>
> Ry Rainey
>
> Ry is a Staff Engineer at Pixieset with 11 years of experience building web apps for e-commerce and creative businesses. At Pixieset, he has primarily contributed to Client Gallery and Website, helping photographers succeed in a digital world.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。