---
title: "Scaling medical content review at Flo Health with Amazon Bedrock – Part 2"
date: 2026-07-15T20:45:47+08:00
draft: false
entry_kind: "auto"
tags: ["Amazon Bedrock", "Customer Solutions"]
categories: []
source: "blogs_podcasts"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:a8f661adf3fb2dac47b93f3d63be132d65af66a734b1b036ecd941643baa93cc"
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 73
description: "当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。"
external_url: https://aws.amazon.com/blogs/machine-learning/scaling-medical-content-review-at-flo-health-with-amazon-bedrock-part-2
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/scaling-medical-content-review-at-flo-health-with-amazon-bedrock-part-2](https://aws.amazon.com/blogs/machine-learning/scaling-medical-content-review-at-flo-health-with-amazon-bedrock-part-2)

## 来源摘要/节选

> This post was written by Konstantin Lekh, Sasha Zinchuk, and Eugene Sergueev from Flo Health, and Liza (Elizaveta) Zinovyeva from AWS.
>
> In this post, we share how Flo Health’s engineering team turned a proof of concept (PoC) from the AWS Generative AI Innovation Center into a production-grade, AI-powered medical content review and generation system built on Amazon Bedrock. This system reduced review time by 60 percent and tripled content throughput without expanding the medical team. We cover four areas: (1) adapting the PoC architecture for Flo Health’s content pipeline, (2) implementing specialized AI Judges for different review dimensions, (3) building an AI content generation system with Retrieval Augmented Generation (RAG), and (4) lessons learned from prompt engineering and production deployment. Part 1 of this series covers the initial proof of concept.
>
> This post reflects the perspective of the Flo Health engineering team.
>
> At Flo Health, we create diverse content to support millions of users on their health journey: from in-app stories and articles to onboarding flows and marketing materials. Every piece of content, whether textual or visual, must meet our rigorous medical accuracy standards outlined in our guidelines. While we’ve successfully integrated AI tools to accelerate content creation for editors and designers, medical review remained our critical bottleneck.
>
> Content creation challenges
>
> Our medical experts spend an average of seven working days per article, meticulously verifying facts, checking references against trusted sources, and facilitating compliance with our 10-point medical accuracy checklist. This thorough process, while essential for maintaining trust and safety, limited our ability to scale content production and keep pace with user needs.
>
> The challenge goes beyond time constraints. Scaling a medical review team presents unique difficulties: qualified medical professionals with content expertise are scarce, recruitment is hard and time-consuming, and the cost of expanding such specialized teams is substantial. The traditional scaling approach of hiring more reviewers is not sustainable or economically viable. Instead, we needed to find ways to amplify the impact of our existing medical experts by making their time more efficient and their expertise more scalable.
>
> While general-purpose AI tools have shown impressive capabilities, they present significant risks for medical content review. These systems can generate information that has no grounding in underlying references or facts, commonly referred to as hallucinations. At Flo, where millions of users rely on our educational content to better understand their bodies and health, accuracy and trust are paramount. We needed a solution designed specifically to provide information only from reliable medical sources, with clear references to every piece of information it presents.
>
> AWS proof of concept as a starting point
>
> The PoC’s success presented us with an exciting opportunity to transform how we approach medical content review. We chose a gradual adoption strategy by scaling our medical experts’ capabilities while building trust through continuous validation.
>
> Our production implementation follows a three-layer validation approach. First, the system checks content against our internal medical guidelines, flagging potential issues and suggesting corrections based on our established rules. It then validates the content against trusted external medical sources, from evidence-based clinical decision tools to peer-reviewed journals and regulatory bodies. Finally, our medical experts review the AI-annotated content in a streamlined interface that highlights which rules were applied and provides direct links to relevant sources, simplifying fact-checking.
>
> Our primary success metrics focus on two areas: reducing review time and minimizing the number of corrections required by experts.
>
> AI review system
>
> In this section, we explore how we integrated, transformed, or extended PoC solution components into a production-ready system that scales medical review capabilities.
>
> The AI Review tool reduces the feedback loop between content creators and medical reviewers. With AI Review, better quality content reaches the human review stage, and the number of iterations decreases.
>
> We began by tailoring the MACROS architecture identified during the proof-of-concept to Flo’s content model.
>
> At Flo, we created a set of AI Judges, each having its own prompt, and a set of examples for training and testing. Each Judge focuses on a specific review dimension: medical accuracy, legal compliance, brand style, and more.
>
> We test each Judge with different models and choose the best fit for each based on the required quality threshold, risk level, latency, and operating cost. For medical safety or other high-risk checks, accuracy and reliability take priority. For simpler or lower-risk checks, a lighter model is appropriate if it meets the required performance threshold. This approach allows us to improve each Judge independently by adding more examples, customizing the prompt, and improving accuracy, while keeping the other Judges unchanged, avoiding regression issues.
>
> Flo Health’s content pipeline embraces the MACROS patterns introduced by Amazon and adapts them to real-world production in Flo’s Contentful CMS. The proposed MACROS strategy of splitting text into manageable sections fits well with our existing architecture, because our graphs (surveys and chats) are stored in an already pre-chunked format, so each step is a separate content entry.
>
> Before sending for assessment, we split each step into smaller pieces, such as button text, title, description, and more.
>
> Every piece of content undergoes a series of AI Judge evaluations rather than one monolithic prompt. This means Flo runs specialized large language model (LLM) prompts for each review dimension (medical accuracy, legal compliance, brand style, and more). This way, we get detailed comments for each piece of content.
>
> After we get Judges’ replies, we use them as input for further generative AI revisions, following the MACROS flow. Using Amazon Bedrock, we generate proposals for better texts that address the concerns found. These suggestions are presented directly in the Contentful app UI, with changes highlighted, so that content editors and medical experts can review, select or edit the preferred version (or even keep the original) within their familiar workflow.
>
> The human reviewer remains in control while using AI as an expert assistant. Once a decision is made for each line, the app updates the content entry in Contentful with the final content.
>
> Pipeline
>
> The following figure shows all AI Review stages connected into one flow. Results for each step are loaded when ready, so users don’t experience delays.
>
> AI content generation system
>
> After successfully onboarding Amazon Bedrock as the foundation for our AI content review workflow, we wanted to reuse the same service to accelerate content creation.
>
> We needed an AI generation tool to automate routine operations and reduce cognitive load: Requests can be quickly drafted without the need to manually create a graph from scratch.
>
> Chain-of-thought prompting
>
> The generation pipeline uses a multi-stage chain-of-thought prompting approach:
>
> A key optimization was using different Claude by Anthropic in Amazon Bedrock AI models for different jobs. For lightweight classification and routine analysis, for example to determine how many steps the user wants to generate, we use the faster, lower-cost Claude Haiku model.
>
> For high-fidelity content generation or complex reasoning (such as drafting a nuanced medical explanation or rewriting a paragraph in a specific empathetic tone), we invoke the more powerful Claude Sonnet models.
>
> Retrieval Augmented Generation
>
> Building generative AI tools in a domain like women’s health required incorporating a lot of context that lives outside the model. We tackled this with RAG. In practice, for inference with an LLM, we gather only relevant information from our knowledge base and feed it into the model’s context. For example, when drafting content, the system retrieves relevant guidelines, rules, medical knowledge and existing templates or visual asset references for the topic at hand. These knowledge base materials are developed and maintained through an iterative process involving product, editorial, and medical review, with the medical team owning the safety scope.
>
> We also integrated trusted third-party medical sources, such as evidence-based clinical decision tools, peer-reviewed journals, and regulatory body publications. The system persists the list of sources used alongside each piece of generated content, so medical reviewers can validate references directly without manual searching.
>
> User experience
>
> We focused on clearly illustrating and explaining every stage of AI generation to users so they can identify inconsistencies early. We also mitigated idle waiting times by progressively displaying intermediate results as each stage completes, so users can begin reviewing output before the pipeline finishes. Finally, we aimed to visualize all design elements and connections between content pieces (screens), alleviating the need for users to repeatedly export and test content on their phones. The following animation demonstrates the AI generation user experience.
>
> Architecture
>
> The following figure shows our AI content generation architecture.
>
> Content creators initiate a generation request from the familiar Contentful App environment. The system then orchestrates a series of steps designed to produce medically grounded, guideline-aligned content with minimal manual effort.
>
> Requests are routed through Amazon API Gateway, which maintains real-time communication with the UI, so creators see progress instantly.
>
> The core pipeline has three steps:
>
> First, the system retrieves relevant medical guidelines, rules, and contextual information from our knowledge base in Amazon Simple Storage Service (Amazon S3) using semantic search through Amazon Bedrock. This way, the generated content is grounded in medical knowledge.
>
> Next, the system structures the content using Claude Foundation Models by Anthropic through Amazon Bedrock, pulling from our template and asset repository in Amazon S3 to maintain consistent formatting while generating the step-by-step content flow. AWS Lambda functions orchestrate this workflow.
>
> Finally, a validation step checks the generated content for medical accuracy and brand guideline compliance using Amazon Bedrock. If issues are detected, the feedback loop automatically triggers reprocessing, so content creators receive only validated output.
>
> Our knowledge base, medical reference documents, content templates, and visual assets, lives in Amazon S3, with Amazon DynamoDB managing state and metadata across the pipeline. AWS Step Functions orchestrates the end-to-end workflow, and the modular design means we can extend to new content types or validation requirements as they emerge.
>
> Impact, insights and lessons learned
>
> Developing these generative AI tools provided our team with valuable insights into the practical application of prompt engineering.
>
> YAML vs. JSON
>
> We found YAML far more robust than JSON as an output format. Its indentation-based structure is more forgiving, leading to fewer invalid outputs and easier debugging. Since our initial implementation, Amazon Bedrock has introduced structured outputs, which enforces schema-aligned JSON responses directly at the API level and could be a viable alternative for teams facing similar format consistency challenges.
>
> Examples vs. rules
>
> As the project grew, the rule set becomes massive and sometimes conflicting, making it harder for the model to prioritize correctly. Enriching rules with concrete examples showing the model what we actually mean rather than stating what to avoid led to significant error reduction. Few-shot examples consistently improved output adherence.
>
> AI as intelligent assistant, not replacement
>
> Our production strategy centered on augmenting, not replacing, human expertise across three critical workflow stages:
>
> 1. Intelligent pre-screening – AI flags potential medical claims that need validation, identifies sections requiring expert attention, and runs preliminary compliance checks against our medical guidelines. This transforms our experts’ starting point from a blank page to a pre-annotated document with clear focus areas.
>
> 2. Real-time content assistance – Writers receive immediate feedback on medical accuracy, style compliance, and citation requirements as they draft, catching issues before they reach medical expert review.
>
> 3. Enhanced expert review experience – Medical experts receive AI-annotated content with highlighted concerns, suggested revisions, and relevant pre-researched source materials, letting them focus on validating AI insights and complex medical nuances that require human judgment.
>
> The power of structured feedback loops
>
> By capturing every expert correction as reusable rules and examples rather than one-off edits, we built a system that grows smarter with each review cycle, reducing repeated errors by over 70 percent. This approach also reduced routine compliance corrections by 80 percent and cut average review time per content piece by 60 percent. It tripled content throughput without expanding the medical team.
>
> Specificity beats generalization
>
> Building specifically around our medical guidelines, source hierarchy, and content standards, and measuring each Judge against predefined test sets combining synthetic and real anonymized cases, delivered consistent improvement in first-pass accuracy and reduced the need for full re-verification of AI output.
>
> Future directions
>
> As we expand the system’s capabilities, we’re exploring confidence scoring, defined together with medical experts based on compliance history, guideline priority, and complexity, where content above certain thresholds receives expedited review, while higher-risk content gets additional scrutiny. We’re also investigating extending this approach to visual content, making sure infographics, illustrations, and other visual materials meet the same rigorous standards.
>
> For organizations considering similar implementations, we recommend the following:
>
> Start with clear, documented standards.
>
> Design for continuous learning from day one.
>
> Measure both efficiency and quality.
>
> Invest in user experience.
>
> Plan for gradual rollout, as trust builds through demonstrated success.
>
> At Flo Health, this approach has allowed us to maintain high content standards while scaling our capacity.
>
> That concludes the perspective from the Flo Health engineering team.
>
> Conclusion
>
> In this post, we showed how Flo Health’s engineering team transformed the MACROS proof of concept into a production-ready medical content review and generation system that uses Amazon Bedrock.
>
> The key to success wasn’t full automation but combining specialized AI Judges, structured feedback loops, and a tiered model selection strategy to maintain rigorous medical accuracy standards while increasing content throughput.
>
> If you’re looking to build a similar content review or generation system, start by defining your domain-specific quality standards, then use Amazon Bedrock to prototype specialized AI judges against those standards.
>
> Learn more about the AWS Generative AI Innovation Center and contact your AWS Account Manager for expert guidance and support.
>
> Visit the Amazon Bedrock documentation to explore available foundation models, structured outputs, and guardrails.
>
> Explore Amazon Bedrock AgentCore to orchestrate multi-step agentic workflows for content review and generation pipelines.
>
> Learn how to build RAG applications with Amazon Bedrock Knowledge Bases.
>
> Explore the AWS services used in this architecture: AWS Lambda, Amazon API Gateway, AWS Step Functions, Amazon S3, and Amazon DynamoDB.
>
> Read Part 1 of this series for the full proof-of-concept architecture and results.
>
> If you have questions or want to share your experience, leave us a comment.
>
> About the authors
>
> Konstantin Lekh
>
> Konstantin is a Staff Engineer at Flo, based in Amsterdam. He works in the AI Platform Team, building systems for AI-driven content generation and evaluation. His work covers both the core platform and end-to-end integrations, with a focus on driving the adoption of AI-powered products across company workflows to improve efficiency and scalability.
>
> Sasha Zinchuk
>
> Sasha is a PM at Flo Health, responsible for backend-driven onboarding and no-code survey tooling across iOS, Android, and web. He is passionate about developer experience, expression languages, and AI-powered prototyping as levers for faster product experimentation at scale. Outside of work, he enjoys vibe-coding small tools, gaming, and writing about his experience at the intersection of product and engineering.
>
> Eugene Sergueev
>
> Eugene is a Director of Engineering at Flo Health, where he leads engineering teams behind products used by over 70 million people worldwide. He is passionate about applying AI in high-trust domains, with a focus on reliable systems, evaluation, and operational safety. Outside of work, he writes about engineering leadership, technical strategy, and bringing AI into real-world workflows.
>
> Liza (Elizaveta) Zinovyeva, Ph.D.
>
> Liza is an Applied Scientist at AWS Generative AI Innovation Center and is based in Berlin. She helps customers across different industries to integrate Generative AI into their existing applications and workflows. She is passionate about AI/ML, finance and software security topics. In her spare time, she enjoys spending time with her family, sports, learning new technologies, and table quizzes.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。