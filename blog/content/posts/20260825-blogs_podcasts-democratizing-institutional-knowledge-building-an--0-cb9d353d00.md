---
title: "Democratizing institutional knowledge: Building an AI-powered knowledge management system with AWS"
date: 2026-08-25T13:50:13+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "RAG", "AI Agent", "生成式 AI", "机器学习", "Amazon Bedrock Knowledge Bases", "Generative AI", "Technical How-to"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:c585d32fe7c03c535d6d6f8e0878ba08f15054b2629085c43b1fde6f26da669e"
source_payload_sha256: "sha256:a693467890f16f92018d5ee7b5ef64cd3f3a0367400aae6e10527fc18c27a445"
observation_id: obs_cb9d353d00004b4139732ab4afd6fe6104e09ec06b9a6e0c93e8533ba14eb6ad
event_id: evt_58acb0c680dbb8ee26b67eac84e1f638d226e0e018f96070106b9862125586e5
revision_id: rev_8cb313936ead56402ca3ea287126d38e9e3d6a66a6c53af97a63e08fdb9780b1
source_published_at: 2026-08-24T18:59:15Z
first_seen_at: 2026-08-25T17:45:55.107435Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: true
source_truncation_reason: "crawler_feed_content_limit"
source_support: 1.0
source_title_chars_original: 98
interpretation_sha256: "sha256:99665d6f24efb4a9bdede906baa9373f2b8427467820ca7e995321590190b1cd"
description: "这是一个基于 AWS 构建的可扩展知识管理系统，利用云存储保存机构内部文档，通过自然语言查询和语音交互的 AI 虚拟形象向用户交付答案，并使用缓存降低重复调用的费用。"
external_url: https://aws.amazon.com/blogs/machine-learning/democratizing-institutional-knowledge-building-an-ai-powered-knowledge-management-system-with-aws
parent_observation_id: null
last_seen_at: 2026-08-25T05:47:17.644963Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/democratizing-institutional-knowledge-building-an-ai-powered-knowledge-management-system-with-aws](https://aws.amazon.com/blogs/machine-learning/democratizing-institutional-knowledge-building-an-ai-powered-knowledge-management-system-with-aws)
- **发布域名**: aws.amazon.com

## 要点解读

### 这是什么  
这是一个基于 AWS 构建的可扩展知识管理系统，利用云存储保存机构内部文档，通过自然语言查询和语音交互的 AI 虚拟形象向用户交付答案，并使用缓存降低重复调用的费用。

### 用在哪里  
适用于需要在新老员工交接或关键人员离职时保留专业知识的组织，如制造、医疗、金融、能源和政府部门。知识工作者可通过语音或文字快速检索流程和政策，而领域专家只需把文档上传至存储即可。

### 可以推断的  
推测：该系统在提供语音交互时对网络连接有持续依赖，离线环境可能无法正常工作。  
推测：在以重复查询为主的业务场景中，缓存机制能够显著减少模型推理的调用成本。

## 来源摘要/节选

> Organizations across industries struggle with managing institutional knowledge, the collective wisdom and experience accumulated over years of operations. This “tribal knowledge” often disappears when key personnel leave, creating knowledge gaps that impact efficiency and innovation. Traditional documentation methods have proven inadequate, often resulting in outdated or inaccessible information when it’s needed most.
>
> In this post, we present a customizable, smart-caching cloud-based solution that captures, maintains, and delivers institutional knowledge through an intelligent avatar system, powered by AWS services.
>
> Who should use this solution
>
> Organizations across diverse industries can use this system to preserve critical knowledge. For example, manufacturing organizations can capture production procedures and maintenance protocols before experienced technicians retire. Other organizations like healthcare facilities, financial services firms, energy companies, and government agencies can also tailor their use cases with the solution. Knowledge workers can access procedures and policies through natural language queries instead of searching multiple repositories, while subject matter experts and retiring employees can upload documentation to preserve their expertise for future generations.
>
> Organizations can deploy the system with desktop browser access for detailed research, voice interaction for hands-free operation, and text-based queries for quick reference adapting to the specific operational contexts of each industry.
>
> Solution overview
>
> Our solution uses AWS services to create a scalable, configurable knowledge management system that you can adapt to your organization’s needs. At its core, the architecture combines advanced AI capabilities with robust cloud infrastructure to deliver an intuitive, responsive knowledge delivery system.
>
> The foundation of our solution is a browser-based interface that supports both text and voice interactions, making knowledge accessible through natural conversation. This interface connects to a configurable avatar system that can work with any AI avatar solution, providing organizations with the flexibility to choose or change their preferred avatar technology.
>
> Figure 1: Solution architecture for the knowledge management system
>
> Behind the scenes, Amazon Cognito secures access management, while Amazon API Gateway provides controlled, monitored access to the system’s components. The knowledge-processing core uses Amazon Bedrock Knowledge Bases for managed Retrieval Augmented Generation (RAG): institutional knowledge stored in Amazon Simple Storage Service (Amazon S3) is the data source, and Amazon Bedrock handles chunking, embedding (using Amazon Titan Text Embeddings), and retrieval, grounding each answer in your own documents. The knowledge base is backed by an Amazon OpenSearch Serverless vector store. Amazon DynamoDB provides response caching, and AWS Lambda functions orchestrate the workflow.
>
> Cost note: The Amazon OpenSearch Serverless vector store is created in your account by the deployment and bills per OpenSearch Compute Unit (OCU) with an always-on minimum, independent of query volume. Treat this as a standing baseline cost (on the order of a few hundred USD per month at the default floor) when budgeting. It is the largest fixed component of the solution’s cost. See Cost optimization through smart caching for how caching reduces the variable inference cost on top of this baseline.
>
> Why this solution?
>
> Organizations seeking to preserve institutional knowledge have several approaches available, from building custom solutions on Amazon Bedrock to deploying text-based chat agents. This solution differentiates through three core capabilities.
>
> Voice-first, avatar-driven delivery: This solution is built around voice interaction with an AI-powered avatar rather than a text-only chat interface. Non-technical end users need little to no learning curve. They speak to the avatar and receive spoken answers, the same way they would ask a colleague. Workers in connected settings such as training rooms, control rooms, quality labs, and maintenance-planning offices can query the system hands-free while reviewing procedures. Avatar-based interaction can also increase adoption and trust among non-technical populations compared to text-only chatbots. (This is a cloud-connected design. See the connectivity requirement under Scalability and performance characteristics.)
>
> Simplicity for knowledge owners: Content management requires no technical expertise. Knowledge owners simply upload existing documents into Amazon S3 (Word, PDF, plain text, Markdown, or JSON). An ingestion sync then chunks and embeds each document into the vector store, after which it becomes queryable. New documents are queryable shortly after upload, once that automated sync completes. It is not instantaneous. There is no need to restructure content, tag metadata, or hand-build a retrieval pipeline.
>
> Rapid deployment with built-in cost optimization: The full prototype deploys in hours through AWS CloudFormation. A built-in DynamoDB cache reuses previous answers for repeated questions, reducing variable AI inference cost. In our testing, cache hit rates of 50–70 percent were achievable for workloads dominated by repeated questions. Actual savings depend on how repetitive your query mix is.
>
> How this compares to alternatives
>
> Building a custom solution on Amazon Bedrock provides full architectural control but requires independently designing and integrating voice processing, avatar rendering, caching, and retrieval pipelines. This typically takes weeks to months and assumes deep technical expertise across multiple AWS services.
>
> Text-based chat agents such as Amazon Q and custom Amazon Bedrock chat interfaces offer a faster path to deployment and excel at typed knowledge retrieval. This solution adds voice-first interaction and avatar engagement on top, which improves adoption among frontline workers who benefit from hands-free access.
>
> This solution fills the gap: a production-quality accelerator deployable in hours, voice-first with visual avatar engagement, and cost-optimized through smart caching. For organizations that need institutional knowledge in the hands of non-technical workers quickly and affordably, this accelerator alleviates the complexity of assembling these capabilities independently.
>
> When to choose this solution
>
> Choose this accelerator when your organization needs to:
>
> Deliver institutional knowledge to non-technical or frontline workers through voice and visual interaction.
>
> Deploy quickly with a proven prototype rather than building from scratch.
>
> Reduce AI inference costs through intelligent caching.
>
> Preserve knowledge from retiring experts with minimal friction.
>
> Implementation journey
>
> The implementation journey consists of three main phases: knowledge foundation setup, infrastructure deployment, and AI integration. Each phase builds upon the previous one to create a comprehensive knowledge management system.
>
> Phase 1: Knowledge foundation setup. The implementation process begins with organizing institutional knowledge. Documents are uploaded to the Amazon S3 knowledge repository, and Amazon Bedrock Knowledge Bases ingests them from there. If your source content lives in other systems or formats, you can optionally add an AWS Glue ETL job to convert it into an AI-optimized format before uploading. This ETL step is a separate, optional integration and is not created by the CloudFormation deployment. Organizations whose documents are already in the supported formats listed below can upload directly to S3.
>
> Key considerations:
>
> Supported formats: Documents can be in various formats (Word, PDF, plain text, Markdown, JSON).
>
> Optimal output: Markdown (.md) or structured JSON are recommended for best AI retrieval performance.
>
> ETL handles the conversion: If you use the optional AWS Glue ETL job, it transforms source documents into the recommended output format before they are uploaded to S3.
>
> For detailed guidance on using AWS Glue for data extraction and transformation, refer to the AWS Glue ETL documentation.
>
> Phase 2: Infrastructure deployment. The core infrastructure deployment begins with AWS CloudFormation templates, facilitating consistent and repeatable deployments. This phase includes:
>
> Setting up Amazon Cognito for secure user authentication and access controls.
>
> Configuring API Gateway endpoints to manage component communication.
>
> Establishing S3-based repositories for knowledge storage.
>
> Implementing DynamoDB for response caching.
>
> Phase 3: AI integration. The final phase integrates the AI capabilities and processing pipeline:
>
> Configuring Amazon Bedrock for knowledge processing and query understanding.
>
> Setting up Lambda functions for request orchestration and response handling.
>
> Implementing the audio processing pipeline:
>
> Amazon Transcribe for converting voice input to text.
>
> Amazon Polly for converting text responses to natural speech.
>
> Integrating the chosen avatar system for human-like interactions.
>
> The system maintains high performance through an intelligent caching algorithm that significantly reduces response times while preserving information accuracy. The combination of these components creates an experience where you can interact with the knowledge base through your preferred method of communication, whether text or voice.
>
> Implementation steps: This guide outlines the steps to deploy the Auto Demo application. The steps that follow are written and tested for us-east-1, which we chose because it has the broadest availability of the foundation models (FMs) and avatar streaming used here. If you deploy in another AWS Region, confirm that your chosen Amazon Bedrock models and the avatar provider are available there, and update the hardcoded Region in the source, before you begin.
>
> Prerequisites
>
> Initial deployment requires technical capabilities from IT or DevOps teams for one-time setup, including basic AWS Management Console navigation, infrastructure-as-code understanding, and identity management familiarity.
>
> End users require no technical capabilities. The conversational interface alleviates barriers. Users simply access a URL and interact naturally through text or voice as they would with a human expert.
>
> AWS account
>
> Access to an AWS account with permissions to create S3 buckets, CloudFormation stacks, and invoke Amazon Bedrock models.
>
> Appropriate AWS Identity and Access Management (IAM) permissions for deploying and managing AWS resources.
>
> Required IAM permissions by service
>
> The CloudFormation stack creates and manages resources across multiple AWS services. To deploy and operate this solution, the deploying IAM role or user requires permissions for the following services:
>
> Amazon Bedrock (foundation model invocation and Amazon Bedrock Knowledge Bases retrieval)
>
> Amazon S3 (knowledge base storage and application files)
>
> AWS Lambda (serverless compute for request orchestration)
>
> Amazon Cognito (user authentication and access management)
>
> API Gateway (HTTP endpoint management)
>
> Amazon OpenSearch Serverless (vector store backing the Amazon Bedrock knowledge base)
>
> Amazon Polly (text-to-speech for voice responses)
>
> Amazon Transcribe (speech-to-text for voice input)
>
> Amazon CloudWatch Logs (centralized logging)
>
> IAM PassRole (service-role delegation for the Lambda and knowledge-base execution roles)
>
> Note: For production deployments, follow the principle of least privilege by scoping resource ARNs to your specific account and Region. The CloudFormation stack automatically creates the necessary execution roles with appropriately scoped permissions for runtime operations.
>
> Foundation model access: This solution uses Amazon Titan Text Embeddings (amazon.titan-embed-text-v1) to embed documents into the vector store, and Amazon Nova Pro (amazon.nova-pro-v1:0) and Anthropic Claude 3 Sonnet (anthropic.claude-3-sonnet-20240229-v1:0) as the selectable models for generating answers. Amazon Bedrock provides automatic access to Amazon-owned serverless models, so Amazon Nova Pro and Amazon Titan Text Embeddings are available by default with no manual enablement. Anthropic Claude models aren’t covered by automatic access in all Regions: before your first Claude request, complete the one-time Anthropic model-access request in the Amazon Bedrock console and make sure your account has the required AWS Marketplace subscription permissions. Account administrators can further restrict or substitute models through IAM policies and Service Control Policies (SCPs). For more information, see Amazon Bedrock now provides automatic access to serverless foundation models in your AWS Region.
>
> Walkthrough: Code installation steps
>
> Get the application source code by cloning the public repository on the GitHub website. The application is under the bedkbauto/ folder (the src and web subfolders).
>
> Create the S3 bucket
>
> Log in to the AWS Management Console.
>
> Navigate to the S3 service.
>
> Create a new S3 bucket to store the application files.
>
> Create additional folders to follow this structure: s3://&lt;amzn-s3-demo-bucket&gt;/content/bedkbauto/.
>
> Upload application files
>
> Unzip the downloaded folder containing the application source code.
>
> Upload the unzipped folder contents to the S3 bucket created in the previous step. Only upload the src and web folders.
>
> Figure 2: The src and web subfolders to upload to Amazon S3
>
> Retrieve the S3 object URL
>
> Navigate to the S3 console.
>
> Locate the setup.json file in the src folder of the uploaded application files.
>
> Copy the URL of the setup.json file. It should look similar to this: https://&lt;amzn-s3-demo-bucket&gt;/content/bedkbauto/src/setup.json.
>
> Create the CloudFormation stack
>
> Go to the CloudFormation console.
>
> Choose Create stack, and then choose With new resources (standard).
>
> In the Specify template step, choose Amazon S3 URL, and then paste the URL you copied earlier.
>
> Figure 3: Specifying the template with the Amazon S3 URL
>
> During stack creation, provide these parameters: a stack name, your email address (which receives a one-time password for app login), a username for app login such as demo-user, and the name of the S3 bucket you created earlier such as &lt;amzn-s3-demo-bucket&gt;.
>
> Figure 4: Providing the stack parameters
>
> Leave the remaining settings as default and select the two acknowledgment check boxes, I acknowledge that AWS CloudFormation might create IAM resources with custom names and I acknowledge that AWS CloudFormation might require the following capability: CAPABILITY_AUTO_EXPAND.
>
> Figure 5: Acknowledging the required capabilities
>
> On the review page, choose Submit to create the stack.
>
> Figure 6: Reviewing and submitting the stack
>
> Verify deployment
>
> After the CloudFormation stack creation is complete, open the Outputs tab to access the application.
>
> Figure 7: Locating the FrontendURL on the Outputs tab
>
> Copy the FrontendURL value to a new tab and press Enter.
>
> Enter the username you set during stack creation and the password sent to the email address that you provided.
>
> Figure 8: Signing in with the temporary password
>
> Change to your preferred password and choose Send.
>
> Figure 9: Setting a new password
>
> You can now access the UI.
>
> Figure 10: The deployed Knowledge Base Demo interface
>
> Figure 11: The Knowledge Base Demo answering a question through the avatar
>
> Optimizing performance and user experience
>
> Our knowledge management system employs a dual-layer caching strategy to maximize response speed and efficiency. At the front end, browser-side caching stores recent interactions directly in the user’s browser memory using an LRU (Least Recently Used) algorithm. This local cache minimizes server requests for repeated questions, providing instant responses for common queries. The backend DynamoDB cache maintains a broader knowledge repository with intelligent TTL (Time-To-Live) settings that vary based on content type, longer retention for fundamental knowledge, medium-term for operational procedures, and short-term for time-sensitive information. This tiered approach makes sure information stays fresh while reducing the processing load on AI services. Note that the current implementation matches cache entries on the exact query text, so the cache is most effective when users repeat established, frequently recurring questions. Semantic (embedding-based) matching is a natural enhancement that is not included in this prototype.
>
> The avatar system serves as more than a visual interface. It’s a key component in making complex information accessible and engaging. Built on DeepBrain AI technology, the avatar provides real-time lip synchronization, contextual facial expressions, and natural gestures that match the conversation flow. Organizations can customize the avatar’s appearance, voice, and behavior to align with their brand identity and communication style.
>
> The technical implementation uses WebRTC for smooth video streaming and integrates with Amazon Polly for natural speech synthesis, while WebSocket connections enable responsive avatar control.
>
> Performance monitoring through Amazon CloudWatch provides continuous insights into cache effectiveness and response times. The system automatically adjusts its caching strategy based on usage patterns, warming frequently accessed information and optimizing TTL settings. This combination of efficient caching and natural avatar interaction creates a responsive, engaging knowledge delivery system that scales with organizational needs.
>
> Scalability and performance characteristics
>
> The serverless architecture provides automatic horizontal scaling across components, making sure the system handles growth from pilot to enterprise deployment without manual intervention. Functions provision additional execution environments as concurrent requests grow, handling traffic spikes without performance degradation. The API layer provides throttling while scaling to handle varying load, and the caching layer automatically adjusts capacity as query volume fluctuates.
>
> Concurrent user support scales with configuration. The following figures are indicative estimates from our testing, not guarantees, and depend on Region, model choice, document size, cache hit rate, and configured service quotas. The default setup handled roughly 50 to 100 concurrent users with sub-second responses for cached queries. Raising the relevant service quotas extends this to roughly 500 to 1,000 concurrent users, and enterprise-scale usage of over 5,000 concurrent users is achievable with the same architecture but requires proactive service-quota increases.
>
> Performance varies with caching effectiveness. In our testing, cached responses returned in well under a second, while fresh knowledge-base queries took roughly 2–4 seconds depending on the model and document size. Voice interaction adds speech-processing time on top. These are indicative figures, so measure against your own workload before committing to a latency target. Note that this is a cloud-dependent design: every query round-trips to AWS, and the avatar relies on live WebRTC/WebSocket streaming, which needs stable, low-latency, reasonably high-bandwidth connectivity. There is no edge, offline, or degraded-mode capability in this prototype, so it fits connected environments (training rooms, engineering and maintenance-planning offices, quality labs, control rooms, kiosk stations) rather than disconnected or intermittently connected plant-floor or OT settings. Supporting those would require a separate edge pattern such as local caching, offline fallback, and graceful degradation to text.
>
> For organizations planning growth, start with default configuration for pilots, monitor metrics to identify bottlenecks, increase capacity limits when approaching thresholds, and request service quota increases proactively for enterprise deployments. The serverless architecture makes sure you pay only for actual usage, making it cost-effective to start small and scale as adoption grows.
>
> Cost optimization through smart caching
>
> A key contributor to efficiency is the caching layer, which reduces the largest variable cost: repeated calls to foundation models. The DynamoDB cache stores and reuses answers for repeated queries, so a question that has already been answered does not trigger another model invocation. In our testing this reduced inference cost roughly in proportion to the cache hit rate. For workloads where 50–70 percent of questions were repeats, inference cost fell by a comparable amount. Because the saving is a direct function of the hit rate, we quote a single figure rather than treating the two as independent guarantees. This variable saving sits on top of the fixed Amazon OpenSearch Serverless baseline noted earlier, so budget for both.
>
> The system’s smart-caching mechanism is particularly effective for tribal knowledge use cases where many questions are related to established procedures, policies and institutional practices. By implementing time-based cache invalidation, we maintain an optimal balance between cost efficiency and information accuracy.
>
> Maintaining and evolving the system
>
> The key to long-term success lies in treating the knowledge management system as a dynamic that grows with your organization. To keep the knowledge base current, the deployment configures Amazon S3 event notifications on the knowledge repository: when a document is added or removed, the bucket invokes an AWS Lambda function that automatically starts a Bedrock Knowledge Bases ingestion job, re-embedding the change into the vector store with no manual step. Because ingestion is not instantaneous, updated content becomes queryable shortly after that sync completes. The content-type-aware TTL settings on the response cache complement this, so fundamental processes persist longer while dynamic information refreshes more frequently.
>
> To support accuracy, answers are generated with Amazon Bedrock Knowledge Bases, which grounds each response in passages retrieved from your own verified documents rather than the model’s general training data. This grounding reduces the likelihood of fabricated or off-base answers, and the knowledge base can return source citations that you can surface to users for verification. Grounding reduces but does not eliminate the risk of incorrect answers: for high-consequence or safety-relevant decisions, keep a human in the loop and treat the system as decision support rather than an authoritative source. Explicit confidence thresholds or answer-validation checks are a recommended enhancement for such use cases and are not implemented in this prototype.
>
> Security remains integral to system maintenance. Regular automated audits verify access controls and data protection measures, while modular architecture supports straightforward security updates. Organizations can integrate new security requirements or compliance measures without disrupting existing functionality.
>
> The system’s flexibility extends to content management. As teams document new procedures or update existing ones, they can upload them to the knowledge base, which automatically incorporates these changes. This continuous evolution makes sure the system remains a reliable source of institutional knowledge, adapting to organizational changes while maintaining historical context where needed.
>
> Conclusion
>
> With our knowledge management solution, you can build a powerful tool for preserving institutional knowledge. By using AWS services and following a modular design, organizations can maintain their intellectual capital while facilitating efficient knowledge transfer across their workforce. The system’s flexibility and scalability make it suitable for various industries and use cases, providing a foundation for sustainable knowledge management in the digital age. To get started, clone the sample repository on the GitHub website and deploy the solution in your own AWS account. To learn more, explore Amazon Bedrock Knowledge Bases in the Amazon Bedrock console.
>
> About the authors
>
> Nneoma Okoroafor
>
> Nneoma is a Partner Solutions Architect at AWS, where she specializes in helping organizations architect, scale, and optimize next-generation cloud and artificial intelligence solutions. With deep expertise in machine learning and generative AI workflows, she works closely with the global startup partner ecosystem to build robust, secure, and efficient cloud architectures. Outside of work she

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。