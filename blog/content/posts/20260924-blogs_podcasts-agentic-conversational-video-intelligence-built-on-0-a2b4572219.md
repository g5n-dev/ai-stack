---
title: "Agentic conversational video intelligence built on AWS"
date: 2026-09-24T07:43:18+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "机器学习", "Prompt 工程", "Amazon Bedrock", "Intermediate (200)", "Technical How-to", "博客与播客"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:38cd4c62d14145af9e66e2dac30da43436ccf99315c99a6bd7870d571b354011"
source_payload_sha256: "sha256:a8a9ea6234eed6001607d3745489014e0597ec1576397578985d16ee365ddacf"
observation_id: obs_a2b457221961f9263e3ee4cb7a7028384c9748a857491fd2b0b1c09a3f4dccc5
event_id: evt_7755d96b23a9a3af7242041015a3b4137ff66439db40217e7dc923949ed2b15c
revision_id: rev_3c8ad35c41d523b14f70efcb8898e1c1e2c1848ce04ff6d67e9eb7d2dc7deef8
source_published_at: 2026-09-23T18:21:54Z
first_seen_at: 2026-09-23T23:41:57.554588Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: true
source_truncation_reason: "crawler_feed_content_limit"
source_support: 1.0
source_title_chars_original: 54
interpretation_sha256: "sha256:d89f2ae72088dd3982824aad778bfaef24ea8bd5c8454c122db727547dae05b5"
description: "这是一种基于云平台的视频智能查询方案，允许用户用自然语言向系统提问关于视频内容的问题，系统自动判断需要调用哪些分析服务来生成答案。用户无需为不同类型的问题分别构建处理流程。"
external_url: https://aws.amazon.com/blogs/machine-learning/agentic-conversational-video-intelligence-built-on-aws
parent_observation_id: null
last_seen_at: 2026-09-23T23:41:57.554588Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/agentic-conversational-video-intelligence-built-on-aws](https://aws.amazon.com/blogs/machine-learning/agentic-conversational-video-intelligence-built-on-aws)
- **发布域名**: aws.amazon.com

## 要点解读

### 这是什么

这是一种基于云平台的视频智能查询方案，允许用户用自然语言向系统提问关于视频内容的问题，系统自动判断需要调用哪些分析服务来生成答案。用户无需为不同类型的问题分别构建处理流程。

### 用在哪里

适用于组织内部积累了大量视频但缺乏高效检索手段的场景，比如会议录像的信息提取、安保监控视频的片段查询、或现场检查视频的后续查阅。从事媒体内容分析、安全事件调查或需要从视频中提取特定信息的从业者可能会使用这类工具。

### 可以推断的

推测：通常针对不同类型的视频分析需求需要分别构建处理管线，这种方案通过引入智能调度机制，用单一系统适配多种查询场景，可能降低开发维护的复杂度。

推测：视频内容的检索长期以来依赖人工观看或定制化的机器学习流程，该方案提供的自然语言交互方式可能帮助用户更快定位到所需的视频片段或关键信息。

## 来源摘要/节选

> With video intelligence powered by agentic AI, you can ask natural language questions about uploaded videos and get answers within seconds. Organizations across media, security, insurance, and professional services are generating more video than their teams can review. Meeting recordings accumulate in shared drives, and security cameras capture weeks of unreviewed footage. Field inspection videos sit in object storage long after the initial review. The information inside these videos is often valuable: a design decision discussed three weeks ago, the exact moment a person arrived at a door, or the sequence of events leading to a vehicle collision. But accessing it has traditionally required watching hours of content manually. The alternative, building custom machine learning (ML) pipelines for each specific question type, demands significant development effort. Each new use case meant new development work:
>
> A transcription pipeline for meeting queries.
>
> A computer vision pipeline for visual search.
>
> A face-matching integration.
>
> In this post, we walk through the architecture and key patterns for building a video intelligence solution that accepts natural language questions and returns answers from video content. The solution uses an agentic architecture that decides at runtime which AWS services to invoke. For previously analyzed content, responses return in under a second. Initial analysis of new videos takes 5–10 minutes depending on length and services required. The complete implementation is available in the companion GitHub repository.
>
> Rather than pre-building a fixed pipeline for each question type, we use the Strands Agents SDK to create a single AI agent that orchestrates Amazon Bedrock, Amazon Rekognition, and Amazon Transcribe based on what the user asks. A major media and entertainment company adopted this approach during an AWS Professional Services engagement. With this solution, their consultants can query recorded discovery session content, extracting design decisions, action items, and stakeholder positions. The result: a reduction in manual review time of approximately 80 percent across a backlog of more than 200 multi-hour recordings, based on the customer’s internal before-and-after comparison of analyst hours per recording (not independently verified).
>
> Solution overview
>
> The solution is an AI agent that accepts video files and makes their content instantly queryable through natural conversation. A user can upload a 90-minute meeting recording and ask “What decisions were made in this meeting?” or “Did anyone mention the budget timeline?” The agent determines whether to invoke transcription, visual analysis, or both, then synthesizes the results into a coherent answer. The same system handles security footage queries (“Did this person appear?”), content analysis (“Summarize the first 30 minutes”), and investigative questions (“Which vehicle changed lanes before the collision?”). No separate processing pipelines are required for each use case.
>
> The following screenshot shows the interface that provides a chat panel for natural language queries and a sidebar for file uploads and analysis mode selection.
>
> Figure 1: The video intelligence chat interface
>
> The key insight is that the pipeline is determined at runtime. The agent calls Amazon Transcribe for spoken-content questions, turns to Amazon Rekognition for face matching, and reuses cached results for follow-up questions about previously processed content. The model handles the routing, not application code.
>
> Prerequisites
>
> To follow along with the implementation in this post, you need:
>
> An AWS account with access to Amazon Bedrock (Anthropic Claude Sonnet enabled) and Amazon Simple Storage Service (Amazon S3). For document processing, either Amazon Bedrock Data Automation (BDA) or Amazon Rekognition and Amazon Transcribe is required. See Supported models by AWS Region in Amazon Bedrock.
>
> Python 3.11 or later with the Strands Agents SDK installed (pip install strands-agents strands-agents-tools).
>
> AWS Command Line Interface (AWS CLI) configured with AWS Identity and Access Management (IAM) permissions for the services listed earlier.
>
> Basic familiarity with AI agent concepts such as tool use and reasoning loops.
>
> Architecture
>
> The system consists of an agent orchestrator connected to multiple AWS AI services, with Amazon S3 providing storage for uploaded videos and cached analysis outputs. The agent orchestrator is the reasoning engine. It’s built with the Strands Agents SDK and powered by Amazon Bedrock, using Claude Sonnet or another large language model (LLM) that supports tool use. It receives natural language queries from users and determines which tools to invoke based on the question, sequences multiple service calls when needed, and synthesizes the results into conversational responses. The agent maintains conversation history, so follow-up questions build on prior analysis without reprocessing.
>
> Figure 2: Solution architecture
>
> Amazon Rekognition provides visual analysis, including detecting objects, scenes, activities, and faces in video frames. The agent invokes Amazon Rekognition when the user’s question concerns something visible in the video. Amazon Transcribe converts spoken audio to text with automatic language detection across more than 100 languages (see Amazon Transcribe supported languages) and speaker diarization. The agent uses Transcribe when the question relates to spoken content. Amazon Bedrock Data Automation (BDA) offers an alternative analysis path that combines video summary, chapter detection, and full transcription in a single API call. This is useful when the user wants comprehensive analysis in one step, or when Amazon Rekognition or Transcribe aren’t available. All uploaded videos and analysis outputs are stored in Amazon S3 with per-user prefixes for multi-tenant isolation.
>
> These three services are the starting set, not a fixed one. Because the agent selects tools from their descriptions rather than from hard-coded workflow logic, the same architecture accepts additional services as tools. We return to this point in Extending beyond video. For production deployments, we recommend adding Amazon Bedrock Guardrails to enforce content filtering and grounding checks on agent responses, particularly for face-matching and surveillance use cases where responsible-AI controls are essential.
>
> How agentic orchestration works
>
> In a conventional video analysis application, the developer defines a fixed processing pipeline: upload the video, run transcription, perform visual analysis, present results. This approach processes every video through the same steps regardless of the specific query, and users wait for the full pipeline to complete before asking questions. The agentic approach inverts this model. With minimal pre-processing limited to uploading video files to an S3 bucket, the agent reasons about each question independently and calls only the services needed to answer it.
>
> When a user submits a query, the agent first parses the intent: the user wants a transcript summary, a visual search, or a face match? Then it checks whether relevant analysis has already been performed and cached. If not, it selects the appropriate tools, executes them (potentially in sequence when one tool’s output feeds another), and combines the results into a natural language answer. In our testing with 60-minute videos, the first question about a video typically takes 5–10 minutes (while transcription or visual analysis runs). Subsequent questions about the same content return in under a second because the agent reuses cached results. Actual times vary based on video length, resolution, and the AWS services invoked.
>
> Configuring the agent
>
> The following code shows the complete agent setup. We define the model provider, a system prompt that guides the agent’s reasoning behavior, and the set of available tools. With Strands, the entire orchestration logic (deciding which tools to call, in what order, and how to combine their outputs) is handled by the LLM rather than application code. We show two representative tool implementations (search_faces_in_video and analyze_with_bda). The remaining tools, including transcribe_video and analyze_video_visuals, follow the same pattern and are available in the GitHub repository.
>
> from strands import Agent
>
> from strands.models.bedrock import BedrockModel
>
> from tools import (
>
> transcribe_video, analyze_video_visuals,
>
> search_faces_in_video, analyze_reference_image,
>
> analyze_with_bda, upload_video
>
> )
>
> model = BedrockModel(
>
> model_id="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
>
> max_tokens=4096
>
> )
>
> SYSTEM_PROMPT = """
>
> You are a video intelligence assistant. For each user query:
>
> 1. Determine whether it requires spoken content analysis,
>
> visual content analysis, or both
>
> 2. Check if prior analysis results are already cached
>
> 3. Invoke the appropriate tools
>
> 4. Synthesize results into a clear answer with timestamps
>
> """
>
> The production system prompt spans approximately 250 source lines. The following abbreviated example illustrates three representative policies (cache reuse, service fallback, and multi-modal orchestration) rather than reproducing the prompt verbatim:
>
> # --- Cache management (excerpt) ---
>
> CACHE_GUIDANCE = """
>
> Before invoking any analysis tool, check the cache:
>
> - Call get_cached_result(video_id, analysis_type) first
>
> - If cached results exist and are &lt; 24 hours old, use them
>
> - If the user says "re-analyze" or "fresh analysis", bypass cache
>
> - After any new analysis, store results with cache_result()
>
> # --- Tool fallback behavior ---
>
> If a tool call fails or returns low-confidence results:
>
> - Transcribe failure: suggest BDA as fallback
>
> - Rekognition low confidence (&lt;60%): report uncertainty to user
>
> - BDA timeout: fall back to individual Transcribe + Rekognition calls
>
> # --- Multi-modal orchestration ---
>
> When the query requires both audio and visual understanding:
>
> 1. Run Transcribe and Rekognition in parallel when possible
>
> 2. Correlate timestamps across modalities
>
> 3. Synthesize a unified answer referencing both sources
>
> 4. Cite specific timestamps for each claim
>
> """
>
> agent = Agent(
>
> model=model,
>
> system_prompt=SYSTEM_PROMPT,
>
> tools=[transcribe_video, analyze_video_visuals,
>
> search_faces_in_video, analyze_reference_image,
>
> analyze_with_bda, upload_video]
>
> )
>
> The rest of the production prompt inventories the available tools and defines workflows for file selection, cache reuse and explicit re-analysis, BDA setup and access-denied fallback, reference-image search, transcription and captions, sports highlights, architecture diagrams, and choosing between BDA and service-specific analysis. It also standardizes unified multi-file responses, requires confirmation before cleanup, reuses prior results for follow-up questions, and applies scope and upload-progress guardrails.
>
> With this configuration, the agent handles the routing, tool sequencing, and response synthesis autonomously. Adding a new capability (for example, detecting on-screen text) requires only defining a new tool function and adding it to the tools list. No workflow logic changes are needed.
>
> Defining tools with the @tool decorator
>
> Each AWS service is exposed to the agent as a Python function decorated with @tool. The function signature defines the parameters, and the docstring tells the agent when and how to use it. This docstring is critical: It serves as the agent’s instruction manual for the tool. The following example shows the face search tool that wraps Amazon Rekognition:
>
> from strands.tools import tool
>
> import boto3
>
> @tool
>
> def search_faces_in_video(
>
> video_s3_key: str,
>
> collection_id: str,
>
> confidence_threshold: float = 80.0
>
> ) -&gt; dict:
>
> """Search for a specific person in video footage.
>
> Use this tool when the user provides a reference photo
>
> and asks whether that person appears in a video.
>
> Requires a face collection created first via
>
> analyze_reference_image.
>
> Args:
>
> video_s3_key: S3 key of the uploaded video
>
> collection_id: Rekognition collection with the
>
> indexed reference face
>
> confidence_threshold: Minimum confidence for a
>
> match (default 80%)
>
> Returns:
>
> Dict with matched_faces containing timestamps
>
> and confidence scores for each appearance
>
> """
>
> rek = boto3.client("rekognition")
>
> response = rek.start_face_search(
>
> Video={"S3Object": {
>
> "Bucket": BUCKET, "Name": video_s3_key&#125;&#125;,
>
> CollectionId=collection_id,
>
> FaceMatchThreshold=confidence_threshold
>
> )
>
> job_id = response["JobId"]
>
> # Poll for completion and collect results...
>
> return {"matched_faces": matches}
>
> The following example shows the BDA tool, which provides comprehensive video analysis (summary, chapters, and transcript) in a single API call:
>
> @tool
>
> def analyze_with_bda(
>
> s3_uri: str,
>
> analysis_types: list[str] = ["SUMMARY", "CHAPTERS", "TRANSCRIPT"]
>
> ) -&gt; dict:
>
> """Perform comprehensive video analysis using Amazon Bedrock Data Automation.
>
> Use this tool when the user wants a full video summary, chapter
>
> breakdown, or complete transcript, or when Rekognition/Transcribe
>
> are unavailable. Returns all requested analysis types in one call.
>
> Args:
>
> s3_uri: S3 URI of the uploaded video (s3://amzn-s3-demo-bucket/key)
>
> analysis_types: List of analysis types to perform.
>
> Options: "SUMMARY", "CHAPTERS", "TRANSCRIPT", "IAB"
>
> Returns:
>
> Dict with keys for each requested analysis type,
>
> including timestamps and confidence scores
>
> """
>
> bda = boto3.client("bedrock-data-automation-runtime")
>
> response = bda.invoke_data_automation_async(
>
> inputConfiguration={"s3Uri": s3_uri},
>
> dataAutomationConfiguration={
>
> "dataAutomationArn": BDA_PROJECT_ARN
>
> },
>
> outputConfiguration={"s3Uri": f"s3://{BUCKET}/bda-output/"}
>
> )
>
> invocation_arn = response["invocationArn"]
>
> # Poll for completion...
>
> result = poll_bda_result(invocation_arn)
>
> return {
>
> "summary": result.get("summary"),
>
> "chapters": result.get("chapters", []),
>
> "transcript": result.get("transcript")
>
> }
>
> Multi-step reasoning in action
>
> To illustrate how the agent chains multiple tool calls, consider a user who uploads a reference photo and asks “Did this person appear in my security footage?” The agent must first index the reference face, then search for it in the video. These are two sequential operations that depend on each other. The following trace shows the agent’s internal reasoning:
>
> [Think] This is a face-matching query. I need to index
>
> the reference photo first, then search the video.
>
> [Act] analyze_reference_image(image="reference.jpg")
>
> [Observe] {"faces_detected": 1, "face_id": "face_001",
>
> "confidence": 99.8}
>
> [Think] Face indexed. Now searching the video.
>
> [Act] search_faces_in_video(
>
> video_s3_key="security_cam_july5.mp4",
>
> collection_id="user_collection")
>
> [Observe] {"matched_faces": [
>
> {"timestamp": "00:14:32", "confidence": 97.2},
>
> {"timestamp": "00:47:15", "confidence": 94.8}]}
>
> [Response] Yes, the person appeared twice: at 14:32
>
> (97% confidence) and 47:15 (95% confidence).
>
> The agent determined the correct sequence of operations and handled the dependency between them (the face search requires an indexed collection). It then presented the results conversationally. No application code defined this sequence. The model reasoned through it based on the tool descriptions and the user’s question.
>
> For comprehensive analysis (when the user asks “analyze this video” or “summarize this recording”), the agent can invoke Amazon Bedrock Data Automation (BDA) instead of calling Amazon Rekognition and Transcribe separately. BDA produces a video summary, chapter-by-chapter breakdown with timestamps, and full transcript in a single asynchronous API call:
>
> [Think] The user wants a full summary. BDA provides summary +
>
> chapters + transcript in one call, more efficient than
>
> running Rekognition and Transcribe separately.
>
> [Act] analyze_with_bda(s3_uri="s3://amzn-s3-demo-bucket/meeting.mp4")
>
> [Observe] {"summary": "Team discussed Q3 roadmap...",
>
> "chapters": [{"title": "Introductions", "start": "00:00"},
>
> {"title": "Roadmap Review", "start": "05:32"}, ...],
>
> "transcript": "Welcome everyone. Let's start with..."}
>
> [Response] Here's the meeting summary with chapters:
>
> Summary
>
> The team discussed the Q3 roadmap...
>
> Chapters
>
> - 00:00 - Introductions
>
> When results are ambiguous, the agent communicates uncertainty explicitly. A borderline confidence score (for example, 62 percent) produces a qualified answer: “I found a possible match at 14:32, but the confidence is low, so you may want to verify manually.” If transcription fails because of poor audio, the agent suggests alternatives: “The audio quality is too low for reliable transcription. Would you like me to try visual analysis of the presentation slides instead?”
>
> Example use cases
>
> The agentic pattern applies broadly to scenarios where users need to extract specific information from video content without knowing in advance which analysis type is required.
>
> Meeting intelligence – A team member joining a project mid-stream uploads prior meeting recordings and asks targeted questions: “What architecture decisions were made in April?”, “When did the team agree to use GraphQL?”, or “Summarize discussions about the authentication approach.” The agent transcribes, searches, and summarizes, returning answers with timestamps that reference the specific moment in the recording.
>
> Security and access monitoring – A building manager uploads lobby camera footage with a photo of an expected visitor and asks “Did this person enter the building this week? When?” The agent runs face matching against the video and returns specific timestamps with confidence scores.
>
> Claims investigation – An insurance adjuster uploads dash-cam footage and asks “Describe the sequence of events before the collision” or “Which vehicle was in the wrong lane?” The agent combines visual scene analysis with audio (verbal reactions, horns) to reconstruct the event timeline.
>
> Extending beyond video with a stable tool contract
>
> The three examples above all analyze video, but nothing about the architecture is video-specific. The agent selects tools from their docstrings, so adding a new capability (or a new modality entirely) is a matter of wrapping another service as a @tool function and describing when to use it. No workflow logic changes. The same orchestrator, cache, and per-user isolation apply unchanged.
>
> Figure 3: Extending the pattern to other modalities
>
> That makes the pattern a general template for multi-modal AI assistants, using either AWS services or third-party models:
>
> Document and diagram understanding with Amazon Textract. A discovery session rarely lives only in video. Add a Textract tool to extract text, tables, and form fields from architecture diagrams and working documents supplied as PDFs, and the agent can cross-reference what was drawn on a whiteboard with what was said in the recording. This enriches the same conversational session that already answers questions about the meeting audio.
>
> Clinical conversations with AWS HealthScribe. Point the same pattern at a clinician-patient audio file and a HealthScribe tool returns a structured clinical note (a turn-by-turn transcript plus extracted sections such as chief complaint and treatment plan), so a user can ask “What follow-up was recommended?” against the recording.
>
> Entity and sentiment extraction, or a third-party model. An Amazon Comprehend tool can pull entities, key phrases, and personally identifiable information (PII) from any transcript the agent produces. A model available on Amazon Bedrock (including third-party models) can be wrapped the same way for domain-specific reasoning.
>
> In each case the extension point is the tool contract, not the pipeline. A team that has built the video assistant already has the scaffolding (orchestration, caching, authentication, and per-user isolation) to stand up an AI assistant for a different modality by adding tools.
>
> Cost considerations
>
> The per-query cost depends on which AWS services the agent invokes. After the initial analysis (transcription or visual processing), follow-up questions about the same video only incur Amazon Bedrock reasoning costs because results are cached. The following table shows approximate costs for a 60-minute video:
>
> Service
>
> Operation
>
> Approximate cost
>
> Amazon Transcribe
>
> 60-minute audio transcription
>
> $1.44
>
> Amazon Rekognition
>
> Face search (60-min video)
>
> $6.00*
>
> Amazon Rekognition
>
> Label detection (60-min video)
>
> $6.00*
>
> Amazon Bedrock
>
> Agent reasoning (per turn)
>
> $0.05–$0.15
>
> Amazon S3
>
> Storage (500 MB, 24 hours)
>
> &lt;$0.01
>
> The $6.00 Amazon Rekognition cost is one-time per-video costs (subsequent queries only incur Bedrock reasoning costs).
>
> Based on AWS service pricing as of July 2025 and the preceding cost table, a typical transcript-based query on a 60-minute video costs approximately $1.50 for the initial transcription plus Bedrock reasoning. Subsequent questions about the same transcribed content cost only $0.05–$0.15 per turn, covering only the Bedrock inference call. Actual costs depend on model selection, input length, and AWS Region. For current pricing, see Amazon Bedrock pricing, Amazon Transcribe pricing, and Amazon Rekognition pricing.
>
> Deployment
>
> The solution deploys on Amazon Elastic Container Service (Amazon ECS) with AWS Fargate. The Streamlit application and the agent runtime run in Fargate tasks behind an internal Application Load Balancer, and an Amazon CloudFront distribution is the only public entry point. CloudFront reaches the load balancer through a virtual private cloud (VPC) origin, so the load balancer stays in private subnets with no route to an internet gateway and isn’t directly reachable from the internet. CloudFront also terminates viewer TLS using its default *.cloudfront.net certificate, which provides a publicly trusted HTTPS endpoint without a custom domain or an AWS Certificate Manager certificate. Amazon Cognito handles authentication (invitation-only, with mandatory multi-factor authentication (MFA) through a time-based one-time password (TOTP) by default), and uploads and cached output are stored in Amazon S3 under per-user prefixes with a 24-hour lifecycle policy.
>
> Figure 4: Deployment architecture on Amazon ECS and AWS Fargate
>
> A single script (./deploy/deploy-ecs.sh) builds the container image, pushes it to Amazon Elastic Container Registry (Amazon ECR), and deploys the AWS CloudFormation stacks. Deployment typically completes in 15–20 minutes, most of which is CloudFront propagation. Full deployment prerequisites, the AllowSelfSignup parameter and its trade-offs, and step-by-step instructions are in the repository README.
>
> Development workflow
>
> Kiro is an AI-powered development environment that supports spec-driven software development by turning high-level ideas into structured requirements, designs, and implementation tasks. We used its spec workflow, persistent project context, and agent hooks to move from concept to a deployable sample while building security into each capability as it took shape.
>
> Specs defined each capability before implementation. The face-matching spec defined inputs (reference photo plus video), expected behavior (index the face, search, and return timestamps), and edge cases (no face detected, low-confidence matches). The transcription spec covered multi-language detection, speaker diarization, and cache behavior for repeated queries. Kiro generated implementation tasks from each spec and maintained context across the full feature lifecycle. Based on the team’s prior experience building similar integrations, this compressed what they estimated would typically be a multi-week effort into a focused sprint.
>
> Threat modeling ran alongside the specs, not after them. As each capability was specified, we modeled how it could be abused and captured the result in a living threat model (see docs/threat-model.md in the companion repository). The model works through concrete kill chains (authentication bypass, network exposure, agent exploitation through prompt injection, over-privileged IAM, and audit evasion) and assigns each threat a disposition. Every Critical and High finding was remediated in the sample. The items that remain open are recorded there with an explicit decision (accepted residual, or a documented production change). The controls described in the next section are outputs of that process rather than an afterthought.
>
> Security scanning was embedded in the development loop.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。