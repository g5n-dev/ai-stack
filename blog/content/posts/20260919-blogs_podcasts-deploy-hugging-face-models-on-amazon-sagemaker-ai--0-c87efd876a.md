---
title: "Deploy Hugging Face models on Amazon SageMaker AI with coding agents"
date: 2026-09-19T22:26:57+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "生成式 AI", "机器学习", "深度学习", "Amazon SageMaker AI", "Intermediate (200)", "Technical How-to"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:77020a2422353c1089bc543b275b6db4a2e706e789a41d46e07ec66c3d3c208e"
source_payload_sha256: "sha256:a374570734a94ec00c8ef730345ac668d9c9b4452988fb99f862cdf53298423a"
observation_id: obs_c87efd876aae4ae7c6acc1d475e2b83c9d8fc57abdb7c37d24f6b4673cfcfffd
event_id: evt_76f43842794f8a4762c7527fd36977e802a726c4d8f56001d8975f6955e8bbdb
revision_id: rev_96b34c3a68fc8f43bc14df36efa754f5871fc17e297ad87367ab38c634f453dd
source_published_at: 2026-09-18T15:25:23Z
first_seen_at: 2026-09-19T14:36:05Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 68
interpretation_sha256: "sha256:457e6f3430ff24d1bee24e244f78991b605b2bc1c554bc65f9279253e14a8bf8"
description: "该内容介绍了利用编程代理配合 Hugging Face Skills 在 Amazon SageMaker AI 上部署模型的方法。无引导的编程代理容易因缺乏最新的部署知识而选错容器、配置不当，导致多次失败和额外计费。"
external_url: https://aws.amazon.com/blogs/machine-learning/deploy-hugging-face-models-on-amazon-sagemaker-ai-with-coding-agents
parent_observation_id: null
last_seen_at: 2026-09-20T00:00:00Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/deploy-hugging-face-models-on-amazon-sagemaker-ai-with-coding-agents](https://aws.amazon.com/blogs/machine-learning/deploy-hugging-face-models-on-amazon-sagemaker-ai-with-coding-agents)
- **发布域名**: aws.amazon.com

## 要点解读

### 这是什么

该内容介绍了利用编程代理配合 Hugging Face Skills 在 Amazon SageMaker AI 上部署模型的方法。无引导的编程代理容易因缺乏最新的部署知识而选错容器、配置不当，导致多次失败和额外计费。通过预置的六个 Skills，代理能够在部署前选择正确的容器镜像、自动配置弹性伸缩和监控告警，并确保资源可被正确清理。

### 用在哪里

该内容适用于需要在 AWS SageMaker 上将 Hugging Face 模型投入生产的开发者或团队，尤其是希望借助自动化工具减少重复决策负担的使用者。内容偏向实操，对已有一定云部署经验且希望了解当前最佳实践的读者帮助更大。

### 可以推断的

推测：随着模型种类和云服务版本的快速迭代，仅依赖模型权重更新时间来判断部署知识是否过时并不稳妥，需要有专门的机制来维护部署配置的时效性。

推测：编程代理在执行结构化、规则明确的任务（如云资源配置）上表现较好，但在需要实时领域知识的环节仍需外部补充，其自主推理能力并不能完全弥补信息滞后的问题。

## 来源摘要/节选

> Deploying a Hugging Face model to production means making a dozen decisions: choosing the right serving container for the model’s architecture, confirming the current image tag for your AWS Region, and matching an instance type to the model’s memory footprint. Beyond infrastructure, you must wire autoscaling so you don’t burn GPU hours on an idle endpoint. You also set Amazon CloudWatch alarms that catch silent failures before your users do. After you’ve made those decisions, Amazon SageMaker AI collapses that work into hours.
>
> This kind of structured, repeatable work is exactly what coding agents, like Kiro and Claude Code, are built for. It’s tempting to describe a model to deploy in a coding agent, walk away, and come back to a working endpoint. In practice, an unguided coding agent might make wrong decisions, producing endpoints that are fragile, costly, or quietly wrong. The problem gets worse for newer models, since their training data might not include the latest deployment knowledge.
>
> In this post, you learn how to deploy production-ready Hugging Face models on SageMaker AI using agent skills. You install six skills from Hugging Face Skills, point a coding agent at a Hugging Face model, and get back a real-time endpoint with autoscaling, Amazon CloudWatch alarms, the correct serving container from the AWS Deep Learning Containers (DLC) catalog, and a verified teardown path. Real-time endpoint is the default, but the skills also support real-time with scale-to-zero, serverless inference, asynchronous inference, batch transform, and Amazon Bedrock Custom Model Import. The skills are open source, use only Python and the AWS Command Line Interface (AWS CLI), and work unchanged on macOS, Linux, and Windows.
>
> The problem with an unguided coding agent
>
> To show what the skills actually prevent, it helps to watch what a capable agent does without them. We tested both Kiro (with Auto or Claude Fable 5) and Claude Code (with Opus 4.8) for the request:
>
> deploy the small [Qwen/Qwen3-0.6B] (https://huggingface.co/Qwen/Qwen3-0.6B) model to a real-time endpoint, write the plan to a file first, and keep a log of every action.
>
> Both coding agents initially chose Text Generation Inference (TGI) as the serving container to deploy, an understandable choice given that TGI was the default for years and model training data is full of tutorials that reach it. But the TGI build available in the Region predated Qwen3’s architecture and couldn’t load the model. The endpoint failed its health check. The agent bumped the TGI version, redeployed, failed again, and pivoted to vLLM. This resulted in multiple deployment failures, each of which billed GPU time as it started and then crashed.
>
> The second request failed more quietly. We asked the same agent to deploy a multimodal mixture-of-experts (MoE) diffusion model released only weeks before the test. The coding agents confirmed it existed, and again wrote a script built on TGI, a text-generation server with no backend for a discrete-diffusion image-text model. Nothing failed loudly. You would find out only when the endpoint refused to come up.
>
> The two runs share the same root cause: missing deployment facts, not reasoning failure. The agent planned and debugged well. What it lacked was current, specific knowledge. Recent Qwen models need vLLM. Python 3.13 has no working wheels for much of the machine learning (ML) stack. Container images should be resolved from the published AWS Deep Learning Containers catalog. This knowledge changes faster than model weights get updated. So we make it into editable skill files rather than rely on the latest release of a model to absorb it.
>
> Table 1 compares the model deployment made by the unguided agent against the agent with skills installed.
>
> Deployment concerns
>
> Unguided agent
>
> With skills
>
> Serving container
>
> TGI first → health-check failure → vLLM
>
> vLLM, chosen before any resource was created
>
> Image URI
>
> Discovered by trial and error
>
> Resolved from the AWS DLC catalog, with fallback when the registry query was denied
>
> Autoscaling
>
> None
>
> Target tracking, 1–2 instances
>
> Monitoring
>
> None
>
> Three CloudWatch alarms (latency, errors, overhead)
>
> Documentation
>
> README recommended TGI, the SageMaker SDK, and Python 3.13
>
> Plan and scripts matched what actually ran
>
> Region, role, environment
>
> Correct natively
>
> Correct by rule
>
> Teardown
>
> A script you could run
>
> Run, then verified the resources were gone
>
> Table 1: The same request, run by the agent without and with the skills installed
>
> The rest of this post shows how we deploy Hugging Face models on SageMaker AI endpoints (the right-hand column of Table 1) using agent skills.
>
> Agent skills for deploying Hugging Face models on SageMaker AI
>
> Six skills from the Hugging Face Skills GitHub repo cover the end-to-end deployment workflow. The planner skill orchestrates the other five, as shown in the following diagram.
>
> hf-cloud-sagemaker-deployment-planner (orchestrate, ask only what's needed)
>
> │
>
> ├── hf-cloud-aws-context-discovery (discover local AWS context)
>
> ├── hf-cloud-python-env-setup (set up an isolated Python environment)
>
> ├── hf-cloud-sagemaker-iam-preflight (verify a usable execution role)
>
> ├── hf-cloud-serving-image-selection (select the right container family and image URI)
>
> └── hf-cloud-sagemaker-production-defaults (deploy with autoscaling, alarms, and tags)
>
> An agent skill example
>
> An agent skill is an open standard package consisting of a folder with a required SKILL.md file. This file includes metadata (name and description, at minimum) and instructions that tell an agent how to perform a specific task. Skills load through progressive disclosure. An agent reads a skill on demand when the current task matches its description. The following is a trimmed version of the hf-cloud-serving-image-selection skill.
>
> ---
>
> name: hf-cloud-serving-image-selection
>
> description: Pick the right serving container for a SageMaker model deployment and find its current image URI. Use this skill whenever about to deploy a model to a SageMaker endpoint and an image URI needs to be chosen --- including when the user says "deploy this LLM", "host this HuggingFace model", "serve this fine-tuned model", "deploy this embedding model", "host a reranker", "serve a sentence-transformers model", or when about to hardcode any container URI in deployment code. HuggingFace-curated Deep Learning Containers are ALWAYS preferred: HuggingFace vLLM (LLMs and generative rerankers), HuggingFace vLLM-Omni (multimodal), TEI (embeddings/cross-encoder rerankers), HF Inference Toolkit (other transformers). Generic images (AWS vLLM, DJL-LMI, SGLang) are used only when no HuggingFace image is compatible --- never merely because they carry a newer version. Never hardcode a container URI from memory and never default to TGI. Prevents stale-image failures and wrong-region URIs
>
> ---
>
> Serving Image Selection
>
> The serving container is the single thing most likely to break a deployment
>
> that "looked correct on paper". Wrong container, stale tag, or wrong AMI all
>
> produce the same opaque `Failed to pass health check` error.
>
> End-to-end model deployment phases
>
> The skills drive five AWS services. Amazon SageMaker AI hosts the endpoint, AWS Identity and Access Management (IAM) provides the execution role. Amazon Elastic Container Registry (Amazon ECR) and AWS Deep Learning Containers supply the serving image, while Amazon CloudWatch powers the alarms. All helper scripts in skills call these services through Boto3 and the AWS Command Line Interface (AWS CLI), which retains full control over what gets created. The SageMaker Python SDK works too, but the skills default to Boto3.
>
> The deployment follows six phases:
>
> Discover the AWS context (profile, Region, account, and caller identity) with read-only calls.
>
> Set up an isolated Python environment with a supported Python version and a current boto3.
>
> Find an existing SageMaker AI execution role and create one only if none exists and you have permission.
>
> Select the serving container family and resolve a current image URI from the AWS DLC catalog.
>
> Create the model, endpoint configuration, and endpoint, and then attach autoscaling and Amazon CloudWatch alarms.
>
> Run a smoke test against the live endpoint and report the result.
>
> Prerequisites
>
> To follow along, you need the following:
>
> An AWS account with permission to use Amazon SageMaker AI, including an existing SageMaker AI execution role. The skills can find one automatically or create one if none exists and your credentials allow it.
>
> AWS CLI v2, configured with credentials for that account.
>
> Python 3.10, 3.11, or 3.12. Python 3.13 or later isn’t supported because much of the ML stack does not yet publish wheels for these versions.
>
> A coding agent that supports skills. This post uses Kiro IDE.
>
> Git, to clone the skills repository.
>
> This post deploys Qwen/Qwen3-0.6B to a single ml.g5.xlarge real-time inference instance in US East (N. Virginia) Region (us-east-1). Confirm your account has available quota for this instance type before you start.
>
> Note that a real-time endpoint bills continuously whether it serves traffic, so delete the endpoint when you’re done or follow the teardown steps at the end of this post.
>
> Install the skills
>
> Kiro supports two skill scopes: workspace and global. The workspace skills reside in your project under .kiro/skills/ and apply only to project-specific workflows. The global skills reside under ~/.kiro/skills/ and are available across all workspaces.
>
> To install the six skills from the Hugging Face Skills GitHub repo in the current workspace, enter the following request in a Kiro default agent chat session:
>
> Install six agent skills from the huggingface/skills repo, pinned to commit
>
> f3186efbbc322121eb5d0f31e8a1d669ee961159, into this workspace.
>
> Source: https://github.com/huggingface/skills.git
>
> Commit: f3186efbbc322121eb5d0f31e8a1d669ee961159
>
> Skills live under the repo's skills/ directory:
>
> - hf-cloud-sagemaker-deployment-planner
>
> - hf-cloud-aws-context-discovery
>
> - hf-cloud-python-env-setup
>
> - hf-cloud-sagemaker-iam-preflight
>
> - hf-cloud-serving-image-selection
>
> - hf-cloud-sagemaker-production-defaults
>
> Kiro summarizes the installed files as shown in Figure 1. Note that this post tested and used the repo with a specific SHA: f3186efbbc322121eb5d0f31e8a1d669ee961159.
>
> Figure 1: Kiro finishes installing the six agent skills
>
> To confirm all six skill directories are present, enter / in the Kiro chat session to see available skills as slash commands, as shown in Figure 2.
>
> Figure 2: Enter / to see available skills in the Kiro chat session
>
> Deploy a model with Kiro
>
> With the skills installed, you describe the model to the agent in plain language, and the planner skill takes over. You don’t specify which container family to use, how to find the execution role, or which production defaults to attach, because those decisions live in the skills.
>
> Enter the following request in the Kiro chat session:
>
> I need to deploy a model on AWS SageMaker, and I don't want to deal with all the console selecting and boto3 myself. The model is Qwen3 0.6B, pinned to commit `c1899de289a04d12100db370d81485cdf75e47ca`, called from an internal app. Figure out the best way to deploy it and walk me through it. Write the plan to a file first, and keep a log of every action you take.
>
> To deploy the model, complete the following steps:
>
> Review the plan. The agent writes a deployment plan to a file and waits for your approval before creating any billable resources.
>
> AWS context discovery and container selection. The agent discovers the AWS context (profile, Region, account). The hf-cloud-serving-image-selection skill selects vLLM for Qwen3 and resolves the image URI from the AWS DLC catalog.
>
> Approve the deployment when the agent asks. The hf-cloud-sagemaker-production-defaults skill creates the model, endpoint configuration, and endpoint as a unit, then attaches autoscaling and CloudWatch alarms.
>
> Verify. Review the smoke-test result the agent reports after the endpoint reaches InService.
>
> The following lines come from the deployment log the agent kept during the run:
>
> ## Step 5: Serving Image Selection
>
> | Value | Resolved to |
>
> | Image URI | `763104351884.dkr.ecr.us-east-1.amazonaws.com/huggingface-vllm:0.28.0-transformers5.15.0-gpu-py312-cu130-ubuntu24.04` |
>
> | InferenceAmiVersion | `al2-ami-sagemaker-inference-gpu-3-1` |
>
> | `SM_VLLM_MODEL` | `Qwen/Qwen3-0.6B` |
>
> | `SM_VLLM_HOST` | `0.0.0.0` (else vLLM binds localhost, ping fails, container dies) |
>
> | `SM_VLLM_TRUST_REMOTE_CODE` | `false` |
>
> | `SM_VLLM_MAX_MODEL_LEN` | `8192` |
>
> For a gated model, add a HUGGING_FACE_HUB_TOKEN environment variable.
>
> Resolve the execution role
>
> Deployments often stop at the execution role when calling iam:CreateRole fails on a corporate account whose AWS IAM Identity Center session has no IAM write access. The hf-cloud-sagemaker-iam-preflight skill reverses the order: find first, create only as a last resort.
>
> Its check_role.py script searches the account for existing roles that match patterns such as AmazonSageMaker-ExecutionRole-* and *SageMaker*Execution*, and ranks them by last-used date. It also validates the trust policy and returns the Amazon Resource Name (ARN). It creates a role only when none exists and the caller has iam:CreateRole permission. Note that the created role carries AmazonSageMakerFullAccess. We recommend updating the role to grant only the permissions it needs, following the principle of least privilege.
>
> Apply production defaults
>
> The hf-cloud-sagemaker-production-defaults skill turns an endpoint from a demo into a production deployment. It applies the defaults in Table 2 to every endpoint, establishing an operational baseline. For production deployment, you need to add user-specific configurations, such as Amazon Virtual Private Cloud and AWS Key Management Service configurations.
>
> Resource
>
> Name
>
> Billing
>
> Model
>
> qwen3-06b-internal
>
> none
>
> Endpoint config
>
> qwen3-06b-internal-20260904-1913-config
>
> none
>
> Endpoint
>
> qwen3-06b-internal-20260904-1913
>
> $1.408/hr per instance
>
> Autoscaling target + policy
>
> endpoint/.../variant/AllTraffic, min 1 max 4
>
> none
>
> CloudWatch alarms x3
>
> &lt;endpoint&gt;-Invocation5XXErrors, -ModelLatencyP99, -OverheadLatencyP99
>
> negligible
>
> Table 2: Production defaults the skill applies to every endpoint
>
> Decisions the coding agent made on its own
>
> Agent skills define the workflow, but the coding agent still makes judgment calls within it. In one case, when the agent queried Amazon ECR for the newest image tag, the call was denied because the IAM Identity Center role lacked ecr-public:DescribeImages permission. Rather than fail the deployment, the agent fell back to the known-good tag the skill ships as a safety net and recorded the reason in the log. In another case, after the smoke test returned HTTP 200, the agent noticed that the actual answer was never emitted. This is because the model’s reply was truncated at max_tokens while still inside the Qwen3 reasoning block. The agent flagged this in the log as a configuration issue: the calling application should raise the token limit rather than treat the test as a pass.
>
> Clean up
>
> A real-time endpoint bills for its instance the entire time it exists. Delete the resources you created to avoid ongoing charges. The sagemaker-production-defaults skill includes a teardown.py script that removes the deployment resources and then confirms they’re gone.
>
> To clean up, complete the following steps:
>
> Ask the agent to tear down the deployment or run teardown.py directly with the endpoint name and Region.
>
> Confirm the script reports the endpoint, endpoint configuration, and model as deleted. The script verifies the deletion.
>
> Check that the autoscaling policy and CloudWatch alarms have been removed. Delete any that remain.
>
> Conclusion
>
> Six reusable agent skills turn an unguided coding agent into one that deploys Hugging Face models on SageMaker AI endpoints with production-ready features. Each deployment includes the proper container, autoscaling, CloudWatch alarms, and a verified teardown path. Without these skills, agents reach for outdated containers, skip production safeguards, and leave misleading documentation. This post walks through each skill: AWS context discovery, Python environment setup, IAM role resolution, container selection from the AWS DLC catalog, and deployment with production defaults.
>
> To get started, install the skills from the Hugging Face Skills GitHub repo and deploy your first model. The skills are open source and contributions are welcome.
>
> Teams can also use Amazon SageMaker JumpStart to deploy a set of popular Hugging Face models directly from the console, and Inference Recommendations to automatically benchmark and select the optimal instance type for their workload.
>
> Learn more
>
> Amazon SageMaker AI Developer Guide – Real-time inference
>
> AWS Deep Learning Containers documentation
>
> About the authors
>
> Dario Salvati
>
> Dario holds a master’s degree in Artificial Intelligence. He is an engineer at Hugging Face, where he works on cloud partnerships, including with AWS, and developer tooling. His work sits at the intersection of ML infrastructure and systems, focused on making it easier to deploy and train machine learning models at scale.
>
> Álvaro Bartolomé
>
> Álvaro Bartolomé is a Technical Lead at Hugging Face, where he focuses on building and optimizing scalable machine learning infrastructure across cloud platforms. Álvaro is passionate about productionizing generative AI models, high-performance inference, and making state-of-the-art ML accessible through open source and open science.
>
> Qiong Zhang
>
> Qiong (Jo) Zhang, PhD, is a Senior Solutions Architect at AWS, specializing in Data and AI. Her current areas of interest include distributed training and AI-Driven Software Development. She holds 30+ patents and has co-authored 100+ journal and conference papers. She is also the recipient of the Best Paper Award at IEEE NetSoft 2016, IEEE ICC 2011, ONDM 2010, and IEEE GLOBECOM 2005.
>
> Sanhita Sarkar
>
> Sanhita Sarkar, PhD, drives global AI/ML and generative AI partner solutions at AWS. She brings extensive leadership experience across edge, cloud, and data center environments, holds several patents, has published research papers, and serves as chair for technical conferences.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。